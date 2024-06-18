import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QLineEdit, QGridLayout, QMessageBox
import mysql.connector
from PyQt5.QtCore import Qt


class VentanaRegistroProfesor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Profesor")
        self.setGeometry(100, 100, 400, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout_principal = QVBoxLayout()
        self.central_widget.setLayout(self.layout_principal)
        
        self.grid_layout = QGridLayout()
        self.layout_principal.addLayout(self.grid_layout)
        
        self.labels = ["Cédula:", "Nombre:", "Apellido Paterno:", "Apellido Materno:", "Calle:", "Colonia:", "Número Exterior:", "Teléfono:"]
        self.campos_entrada = {}
        
        for i, label_text in enumerate(self.labels):
            label = QLabel(label_text)
            campo_entrada = QLineEdit()
            self.grid_layout.addWidget(label, i, 0)
            self.grid_layout.addWidget(campo_entrada, i, 1)
            self.campos_entrada[label_text] = campo_entrada
        
        self.boton_insertar = QPushButton("Insertar Profesor")
        self.boton_insertar.clicked.connect(self.insertar_profesor)
        self.layout_principal.addWidget(self.boton_insertar, alignment=Qt.AlignHCenter)
        
        self.setStyleSheet("background-color: #f0f0f0; color: #333;")
        
    def insertar_profesor(self):
        cedula = self.campos_entrada["Cédula:"].text().upper()
        nombre = self.campos_entrada["Nombre:"].text().upper()
        appat = self.campos_entrada["Apellido Paterno:"].text().upper()
        apmat = self.campos_entrada["Apellido Materno:"].text().upper()
        calle = self.campos_entrada["Calle:"].text().upper()
        colonia = self.campos_entrada["Colonia:"].text().upper()
        numext = self.campos_entrada["Número Exterior:"].text().upper()
        telefono = self.campos_entrada["Teléfono:"].text().upper()

        try:
            conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="root",
                database="proyecto"
            )
            cursor = conexion.cursor()

            # Verificar si la cédula ya existe en la base de datos
            cursor.execute("SELECT * FROM PROFESORES WHERE IDCEDULA = %s", (cedula,))
            resultado = cursor.fetchone()
            if resultado:
                QMessageBox.warning(self, "Error", "La cédula ya está asignada a otro profesor.")
                return

            cursor.execute(
                "INSERT INTO PROFESORES (IDCEDULA, NOMBRE, APPAT, APMAT, CALLE, COLONIA, NUMEXT, TELEFONO) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                (cedula, nombre, appat, apmat, calle, colonia, numext, telefono)
            )
            conexion.commit()

            QMessageBox.information(self, "Éxito", "Profesor insertado correctamente.")
            self.limpiar_campos()
        
        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Error", f"No se pudo insertar el profesor: {error}")
        
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def limpiar_campos(self):
        for campo in self.campos_entrada.values():
            campo.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaRegistroProfesor()
    ventana.show()
    sys.exit(app.exec_())
