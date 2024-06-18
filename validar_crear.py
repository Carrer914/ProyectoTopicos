import mysql.connector
from PyQt5.QtWidgets import QMessageBox
from conexion_db import conectar_db

def validar_cedula(cedula, ventana):
    conexion = conectar_db()
    if not conexion:
        QMessageBox.critical(ventana, "Error", "No se pudo conectar a la base de datos.")
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM PROFESORES WHERE IDCEDULA = %s", (cedula,))
        resultado = cursor.fetchone()
        if resultado:
            QMessageBox.warning(ventana, "Error", "La cédula ya está asignada a otro profesor.")
            return False
        else:
            return True
        
    except mysql.connector.Error as error:
        QMessageBox.critical(ventana, "Error", f"No se pudo validar la cédula: {error}")
        return False
        
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def validar_telefono(telefono, ventana):
    conexion = conectar_db()
    if not conexion:
        QMessageBox.critical(ventana, "Error", "No se pudo conectar a la base de datos.")
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM PROFESORES WHERE TELEFONO = %s", (telefono,))
        resultado = cursor.fetchone()
        if resultado:
            QMessageBox.warning(ventana, "Error", "El teléfono ya está asignado a otro profesor.")
            return False
        else:
            return True
        
    except mysql.connector.Error as error:
        QMessageBox.critical(ventana, "Error", f"No se pudo validar el teléfono: {error}")
        return False
        
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

