import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox
from PyQt5.QtCore import Qt 

from conexion_db import conectar_db
from validaciones_leer import validar_cedula

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Profesores")
        self.setGeometry(100, 100, 800, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout_principal = QVBoxLayout()
        self.central_widget.setLayout(self.layout_principal)
        
        self.titulo_label = QLabel("Profesores", self)
        self.titulo_label.setStyleSheet("font-size: 24pt; font-weight: bold; color: #333")
        self.layout_principal.addWidget(self.titulo_label, alignment=Qt.AlignHCenter)
        
        # Agregar combo box para seleccionar la vista de profesores
        self.combo_vista_profesores = QComboBox()
        self.combo_vista_profesores.addItems(["Activos", "Inactivos"])
        self.combo_vista_profesores.activated.connect(self.actualizar_vista_profesores)
        self.layout_principal.addWidget(self.combo_vista_profesores)
        
        self.tabla_profesores = QTableWidget()
        self.columnas = ("IDCEDULA", "Nombre", "APPAT", "APMAT", "CALLE", "COLONIA", "NUMEXT", "TELEFONO", "Acciones")
        self.tabla_profesores.setColumnCount(len(self.columnas))
        self.tabla_profesores.setHorizontalHeaderLabels(self.columnas)
        self.layout_principal.addWidget(self.tabla_profesores)
        self.setStyleSheet("background-color: #f0f0f0; color: #333;"
                           "QHeaderView::section { background-color: #4682B4; color: RED; }")
        self.cargar_profesores()
        
        self.tabla_profesores.itemChanged.connect(self.guardar_cambios)
        
    def cargar_profesores(self):
        self.tabla_profesores.setRowCount(0)
        activo = self.combo_vista_profesores.currentText() == "Activos"
        registros = self.obtener_profesores(activo)
        for fila in registros:
            rowPosition = self.tabla_profesores.rowCount()
            self.tabla_profesores.insertRow(rowPosition)
            for col, dato in enumerate(fila):
                if isinstance(dato, str):  # Verificar si el dato es una cadena
                    dato = dato.upper() 
                self.tabla_profesores.setItem(rowPosition, col, QTableWidgetItem(str(dato)))
            if activo:
                eliminar_button = QPushButton("Eliminar")
                eliminar_button.clicked.connect(self.eliminar_registro)
                self.tabla_profesores.setCellWidget(rowPosition, len(self.columnas) - 1, eliminar_button)
            else:
                reactivar_button = QPushButton("Reactivar")
                reactivar_button.clicked.connect(self.reactivar_profesor)
                self.tabla_profesores.setCellWidget(rowPosition, len(self.columnas) - 1, reactivar_button)

    def reactivar_profesor(self):
        button = self.sender()
        if button:
            # Buscar el botón en la tabla para obtener su fila
            index = self.tabla_profesores.indexAt(button.pos())
            if index.isValid():
                row = index.row()
                id_cedula = self.tabla_profesores.item(row, 0).text()
                conexion = conectar_db()
                if not conexion:
                    return
                try:
                    cursor = conexion.cursor()
                    cursor.execute("UPDATE PROFESORES SET ACTIVO = 1 WHERE IDCEDULA = %s", (id_cedula,))
                    conexion.commit()
                    QMessageBox.information(self, "Información", "Profesor reactivado exitosamente.")
                    # Recargar los profesores en la tabla
                    self.cargar_profesores()
                except mysql.connector.Error as error:
                    QMessageBox.critical(self, "Error", f"No se pudo reactivar el profesor: {error}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()
    def obtener_profesores(self, activo=True):
        conexion = conectar_db()
        if not conexion:
            return []
        
        try:
            cursor = conexion.cursor()
            if activo:
                cursor.execute("SELECT UPPER(IDCEDULA), UPPER(Nombre), UPPER(APPAT), UPPER(APMAT), UPPER(CALLE), UPPER(COLONIA), UPPER(NUMEXT), UPPER(TELEFONO) FROM PROFESORES WHERE ACTIVO = 1")
            else:
                cursor.execute("SELECT UPPER(IDCEDULA), UPPER(Nombre), UPPER(APPAT), UPPER(APMAT), UPPER(CALLE), UPPER(COLONIA), UPPER(NUMEXT), UPPER(TELEFONO) FROM PROFESORES WHERE ACTIVO = 0")
            registros = cursor.fetchall()
            return registros
        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Error", f"No se pudo obtener los profesores: {error}")
            return []
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def eliminar_registro(self):
        button = self.sender()
        if button:
            # Buscar el botón en la tabla para obtener su fila
            index = self.tabla_profesores.indexAt(button.pos())
            if index.isValid():
                row = index.row()
                id_cedula = self.tabla_profesores.item(row, 0).text()
                activo = self.combo_vista_profesores.currentText() == "Activos"
                
                conexion = conectar_db()
                if not conexion:
                    return
                
                try:
                    cursor = conexion.cursor()
                    if activo:
                        cursor.execute("UPDATE PROFESORES SET ACTIVO = 0 WHERE IDCEDULA = %s", (id_cedula,))
                    else:
                        cursor.execute("DELETE FROM PROFESORES WHERE IDCEDULA = %s", (id_cedula,))
                    conexion.commit()
                    QMessageBox.information(self, "Información", "Registro eliminado exitosamente.")
                    
                    # Recargar los profesores en la tabla
                    self.cargar_profesores()
                    
                except mysql.connector.Error as error:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el registro: {error}")
                finally:
                    if conexion.is_connected():
                        cursor.close()
                        conexion.close()
                        
    def guardar_cambios(self, item):
        row = item.row()
        column = item.column()
        id_cedula = self.tabla_profesores.item(row, 0).text()
        nuevo_valor = item.text().upper()
        columna = self.columnas[column]
        
        conexion = conectar_db()
        if not conexion:
            return
        
        try:
            cursor = conexion.cursor()
            cursor.execute(f"UPDATE PROFESORES SET {columna} = %s WHERE IDCEDULA = %s",
                           (nuevo_valor, id_cedula))
            conexion.commit()
            if self.combo_vista_profesores.currentText() == "Activos" and item.data(Qt.DisplayRole) != nuevo_valor:
                QMessageBox.information(self, "Información", "Cambios guardados exitosamente.")
            elif self.combo_vista_profesores.currentText() == "Inactivos" and item.data(Qt.DisplayRole) != nuevo_valor:
                QMessageBox.information(self, "Información", "Cambios guardados exitosamente.")
        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Error", f"No se pudo guardar los cambios: {error}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
                
    def actualizar_vista_profesores(self):
        self.cargar_profesores()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
