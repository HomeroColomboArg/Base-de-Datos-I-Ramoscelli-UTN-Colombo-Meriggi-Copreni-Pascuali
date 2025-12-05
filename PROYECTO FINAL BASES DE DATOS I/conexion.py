import mysql.connector

def conectar():
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",            # Host donde está la base de datos
            port="3306",                # Puerto de conexión
            user="root",                # Usuario de MySQL
            password="contraseña",      # Contraseña de ese usuario
            database="biblioteca_db",   # Nombre de la base de datos
            autocommit=True             # Habilitar autocommit
        )

        if mydb.is_connected():
            print("Conexión exitosa a la base de datos")
            return mydb

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    return None

