from conexion import conectar


def listar_usuarios():
    """
    Obtiene y muestra por pantalla todos los usuarios de la tabla 'usuarios'.
    """
    conexion = conectar()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        sql = "SELECT id_usuario, nombre, apellido, dni FROM usuarios;"
        cursor.execute(sql)
        filas = cursor.fetchall()

        print("\n--- LISTADO DE USUARIOS ---")
        if not filas:
            print("No hay usuarios cargados.")
        else:
            for fila in filas:
                id_usuario, nombre, apellido, dni = fila
                print(f"({id_usuario}) {nombre} {apellido} - DNI: {dni}")

        cursor.close()
    except Exception as e:
        print("Error al ejecutar la consulta de usuarios:", e)
    finally:
        conexion.close()


def listar_libros():
    """
    Obtiene y muestra por pantalla todos los libros de la tabla 'libros'.
    """
    conexion = conectar()
    if conexion is None:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        cursor = conexion.cursor()
        sql = "SELECT id_libro, titulo, autor FROM libros;"
        cursor.execute(sql)
        filas = cursor.fetchall()

        print("\n--- LISTADO DE LIBROS ---")
        if not filas:
            print("No hay libros cargados.")
        else:
            for fila in filas:
                id_libro, titulo, autor = fila
                print(f"({id_libro}) {titulo} - {autor}")

        cursor.close()
    except Exception as e:
        print("Error al ejecutar la consulta de libros:", e)
    finally:
        conexion.close()


def main():
    
    listar_usuarios()
    listar_libros()


if __name__ == "__main__":
    main()

