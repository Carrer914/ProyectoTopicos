import mysql.connector
from PyQt5.QtWidgets import QMessageBox
from conexion_db import conectar_db

def validar_cedula(cedula, eliminar=False):
    conexion = conectar_db()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM PROFESORES WHERE IDCEDULA = %s", (cedula,))
        resultado = cursor.fetchone()
        if resultado and not eliminar:
            QMessageBox.warning(None, "Error", "La cédula ya está asignada a otro profesor.")
            return False
        elif not resultado and eliminar:
            QMessageBox.warning(None, "Error", "La cédula no existe, no se puede eliminar.")
            return False
        else:
            return True
        
    except mysql.connector.Error as error:
        QMessageBox.critical(None, "Error", f"No se pudo validar la cédula: {error}")
        return False
        
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def validar_telefono(telefono):
    conexion = conectar_db()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM PROFESORES WHERE TELEFONO = %s", (telefono,))
        resultado = cursor.fetchone()
        if resultado:
            QMessageBox.warning(None, "Error", "El teléfono ya está asignado a otro profesor.")
            return False
        else:
            return True
        
    except mysql.connector.Error as error:
        QMessageBox.critical(None, "Error", f"No se pudo validar el teléfono: {error}")
        return False
        
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

