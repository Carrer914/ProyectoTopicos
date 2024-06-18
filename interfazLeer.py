import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
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
        registros = self.obtener_profesores()
        for fila in registros:
            rowPosition = self.tabla_profesores.rowCount()
            self.tabla_profesores.insertRow(rowPosition)
            for col, dato in enumerate(fila):
                self.tabla_profesores.setItem(rowPosition, col, QTableWidgetItem(str(dato)))
            eliminar_button = QPushButton("Eliminar")
            eliminar_button.clicked.connect(self.eliminar_registro)
            self.tabla_profesores.setCellWidget(rowPosition, len(self.columnas) - 1, eliminar_button)
    
    def obtener_profesores(self):
        conexion = conectar_db()
        if not conexion:
            return []
        
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM PROFESORES")
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
                
                # Validar cédula antes de eliminar
                if not validar_cedula(id_cedula, eliminar=True):
                    return
                
                conexion = conectar_db()
                if not conexion:
                    return
                
                try:
                    cursor = conexion.cursor()
                    cursor.execute("DELETE FROM PROFESORES WHERE IDCEDULA = %s", (id_cedula,))
                    conexion.commit()
                    self.tabla_profesores.removeRow(row)
                    QMessageBox.information(self, "Información", "Registro eliminado exitosamente.")
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
        nuevo_valor = item.text()
        columna = self.columnas[column]
        
        conexion = conectar_db()
        if not conexion:
            return
        
        try:
            cursor = conexion.cursor()
            cursor.execute(f"UPDATE PROFESORES SET {columna} = %s WHERE IDCEDULA = %s",
                           (nuevo_valor, id_cedula))
            conexion.commit()
            QMessageBox.information(self, "Información", "Cambios guardados exitosamente.")
        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Error", f"No se pudo guardar los cambios: {error}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

