import mysql.connector

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="proyecto"
        )
        return conexion
    except mysql.connector.Error as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None
