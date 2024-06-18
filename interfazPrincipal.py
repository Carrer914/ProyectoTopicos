import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from interfazCrear import VentanaRegistroProfesor
from interfazLeer import VentanaPrincipal

class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 400, 200)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout_principal = QVBoxLayout()
        self.central_widget.setLayout(self.layout_principal)
        
        self.boton_interfaz_crear = QPushButton("Crear")
        self.boton_interfaz_crear.clicked.connect(self.abrir_interfaz_crear)
        self.layout_principal.addWidget(self.boton_interfaz_crear)
        
        self.boton_interfaz_leer = QPushButton("Leer")
        self.boton_interfaz_leer.clicked.connect(self.abrir_interfaz_leer)
        self.layout_principal.addWidget(self.boton_interfaz_leer)
        
    def abrir_interfaz_crear(self):
        self.interfaz_crear = VentanaRegistroProfesor()
        self.interfaz_crear.show()
        
    def abrir_interfaz_leer(self):
        self.interfaz_leer = VentanaPrincipal()
        self.interfaz_leer.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = Menu()
    ventana_principal.show()
    sys.exit(app.exec_())
