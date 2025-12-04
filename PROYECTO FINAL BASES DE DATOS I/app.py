from conexion import conectar
from datetime import date, datetime


#   1) gestion de usuarios


def submenu_usuarios(conexion):
    while True:
        print("""
----- GESTIÓN DE USUARIOS -----
1. Agregar usuario
2. Ver usuarios
3. Actualizar usuario
4. Eliminar usuario (baja lógica)
0. Volver al menú principal
""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_usuario(conexion)
        elif opcion == "2":
            ver_usuarios(conexion)
        elif opcion == "3":
            actualizar_usuario(conexion)
        elif opcion == "4":
            eliminar_usuario(conexion)
        elif opcion == "0":
            return
        else:
            print("Opción inválida.")


def agregar_usuario(conexion):
    cursor = conexion.cursor()

    print("\n=== AGREGAR NUEVO USUARIO ===")

    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    dni = input("DNI: ").strip()
    email = input("Email: ").strip()
    telefono = input("Teléfono: ").strip()

    consulta = """
        INSERT INTO usuarios (nombre, apellido, dni, email, telefono, fecha_alta, activo)
        VALUES (%s, %s, %s, %s, %s, CURDATE(), 1);
    """

    try:
        cursor.execute(consulta, (nombre, apellido, dni, email, telefono))
        conexion.commit()
        print("\nUsuario agregado correctamente.")
    except Exception as e:
        print(f"Error al agregar usuario: {e}")

    cursor.close()


def ver_usuarios(conexion):
    cursor = conexion.cursor(dictionary=True)
    print("\n=== LISTA DE USUARIOS ===")

    consulta = """
        SELECT id_usuario, nombre, apellido, dni, email, telefono, activo
        FROM usuarios
        ORDER BY id_usuario;
    """

    cursor.execute(consulta)
    usuarios = cursor.fetchall()

    if not usuarios:
        print("No hay usuarios cargados.")
    else:
        for u in usuarios:
            estado = "Activo" if u["activo"] == 1 else "Inactivo"
            print(
                f"ID: {u['id_usuario']:2d} | "
                f"{u['nombre']} {u['apellido']} | "
                f"DNI: {u['dni']} | "
                f"Email: {u['email']} | "
                f"Tel: {u['telefono']} | "
                f"Estado: {estado}"
            )

    cursor.close()


def actualizar_usuario(conexion):
    cursor = conexion.cursor(dictionary=True)

    print("\n=== ACTUALIZAR USUARIO ===")
    id_usuario = input("Ingrese el ID del usuario a actualizar: ").strip()

    # buscar usuario
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s;", (id_usuario,))
    usuario = cursor.fetchone()

    if not usuario:
        print("No existe un usuario con ese ID.")
        cursor.close()
        return

    print(f"\nActualizando a: {usuario['nombre']} {usuario['apellido']}")


  
 

    nuevo_nombre = input(f"Nuevo nombre ({usuario['nombre']}): ").strip() or usuario['nombre']
    nuevo_apellido = input(f"Nuevo apellido ({usuario['apellido']}): ").strip() or usuario['apellido']
    nuevo_email = input(f"Nuevo email ({usuario['email']}): ").strip() or usuario['email']
    nuevo_tel = input(f"Nuevo teléfono ({usuario['telefono']}): ").strip() or usuario['telefono']

    
     

    nuevo_dni = input(f"Nuevo DNI ({usuario['dni']}): ").strip()

    if nuevo_dni == "":
        nuevo_dni = usuario['dni']
    else:
        # verificar que no exista en otro usuario
        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE dni = %s AND id_usuario != %s;",
            (nuevo_dni, id_usuario)
        )
        dni_existente = cursor.fetchone()

        if dni_existente:
            print("\n Error: ese DNI ya está registrado en otro usuario.")
            cursor.close()
            return


    
    

    consulta = """
        UPDATE usuarios
        SET nombre = %s,
            apellido = %s,
            email = %s,
            telefono = %s,
            dni = %s
        WHERE id_usuario = %s;
    """

    cursor2 = conexion.cursor()
    cursor2.execute(
        consulta,
        (nuevo_nombre, nuevo_apellido, nuevo_email, nuevo_tel, nuevo_dni, id_usuario)
    )
    conexion.commit()

    print("\nUsuario actualizado correctamente.")

    cursor2.close()
    cursor.close()



def eliminar_usuario(conexion):
    cursor = conexion.cursor(dictionary=True)

    print("\n=== ELIMINAR (BAJA LÓGICA) ===")
    id_usuario = input("Ingrese el ID del usuario: ").strip()

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s;", (id_usuario,))
    usuario = cursor.fetchone()

    if not usuario:
        print("No existe ese usuario.")
        cursor.close()
        return

    confirmar = input(f"¿Dar de baja al usuario {usuario['nombre']} {usuario['apellido']}? (s/n): ").strip().lower()

    if confirmar != "s":
        print("Operación cancelada.")
        cursor.close()
        return

    cursor2 = conexion.cursor()
    cursor2.execute("UPDATE usuarios SET activo = 0 WHERE id_usuario = %s;", (id_usuario,))
    conexion.commit()

    print("\nUsuario dado de baja correctamente.")

    cursor.close()
    cursor2.close()


#   2) gestion de libros 


def submenu_libros(conexion):
    while True:
        print("""
----- GESTIÓN DE LIBROS -----
1. Registrar libro
2. Ver libros
3. Actualizar libro
4. Eliminar libro
0. Volver al menú principal
""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_libro(conexion)
        elif opcion == "2":
            ver_libros(conexion)
        elif opcion == "3":
            actualizar_libro(conexion)
        elif opcion == "4":
            eliminar_libro(conexion)
        elif opcion == "0":
            return
        else:
            print("Opción inválida.")


def registrar_libro(conexion):
    cursor = conexion.cursor()

    print("\n=== REGISTRO DE NUEVO LIBRO ===")

    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    anio = input("Año de publicación: ").strip()
    isbn = input("ISBN: ").strip()
    editorial = input("Editorial: ").strip()
    categoria = input("Categoría: ").strip()

    consulta = """
        INSERT INTO libros (titulo, autor, anio_publicacion, isbn, editorial, categoria)
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    try:
        cursor.execute(consulta, (titulo, autor, anio, isbn, editorial, categoria))
        conexion.commit()
        print("\nLibro registrado correctamente.")
    except Exception as e:
        print(f"Error al registrar libro: {e}")

    cursor.close()


def ver_libros(conexion):
    cursor = conexion.cursor(dictionary=True)

    print("\n=== LISTA DE LIBROS ===")

    consulta = """
        SELECT id_libro, titulo, autor, anio_publicacion, editorial, categoria
        FROM libros
        ORDER BY id_libro;
    """

    cursor.execute(consulta)
    libros = cursor.fetchall()

    if not libros:
        print("No hay libros cargados.")
    else:
        for l in libros:
            print(
                f"ID: {l['id_libro']:2d} | "
                f"{l['titulo']} | "
                f"{l['autor']} | "
                f"Año: {l['anio_publicacion']} | "
                f"Editorial: {l['editorial']} | "
                f"Categoría: {l['categoria']}"
            )

    cursor.close()


def actualizar_libro(conexion):
    cursor = conexion.cursor(dictionary=True)

    print("\n=== ACTUALIZAR LIBRO ===")
    id_libro = input("Ingrese el ID del libro: ").strip()

    cursor.execute("SELECT * FROM libros WHERE id_libro = %s;", (id_libro,))
    libro = cursor.fetchone()

    if not libro:
        print("No existe un libro con ese ID.")
        cursor.close()
        return

    print(f"Actualizando: {libro['titulo']}")

    nuevo_titulo = input(f"Nuevo título ({libro['titulo']}): ").strip() or libro['titulo']
    nuevo_autor = input(f"Nuevo autor   ({libro['autor']}): ").strip() or libro['autor']
    nuevo_anio = input(f"Nuevo año     ({libro['anio_publicacion']}): ").strip() or libro['anio_publicacion']
    nuevo_editorial = input(f"Nuevo editorial ({libro['editorial']}): ").strip() or libro['editorial']
    nueva_categoria = input(f"Nueva categoría ({libro['categoria']}): ").strip() or libro['categoria']

    consulta = """
        UPDATE libros
        SET titulo = %s, autor = %s, anio_publicacion = %s,
            editorial = %s, categoria = %s
        WHERE id_libro = %s;
    """

    cursor2 = conexion.cursor()
    cursor2.execute(
        consulta,
        (nuevo_titulo, nuevo_autor, nuevo_anio, nuevo_editorial, nueva_categoria, id_libro)
    )
    conexion.commit()

    print("\nLibro actualizado correctamente.")

    cursor.close()
    cursor2.close()


def eliminar_libro(conexion):
    cursor = conexion.cursor(dictionary=True)

    print("\n=== ELIMINAR LIBRO ===")
    id_libro = input("Ingrese el ID: ").strip()

    cursor.execute("SELECT * FROM libros WHERE id_libro = %s;", (id_libro,))
    libro = cursor.fetchone()

    if not libro:
        print("No existe ese libro.")
        cursor.close()
        return

    confirmar = input(f"¿Eliminar el libro '{libro['titulo']}'? (s/n): ").lower().strip()

    if confirmar != "s":
        print("Operación cancelada.")
        cursor.close()
        return

    cursor2 = conexion.cursor()
    cursor2.execute("DELETE FROM libros WHERE id_libro = %s;", (id_libro,))
    conexion.commit()

    print("\nLibro eliminado correctamente.")

    cursor.close()
    cursor2.close()



# 3) manejo de prestamos con transaccion

def manejo_prestamos(conexion):
    cursor = conexion.cursor(dictionary=True)

    print("\n=== CÁLCULO DE MULTA POR ATRASO ===")

    try:
        id_usuario = int(input("Ingrese el ID del usuario: ").strip())
        id_libro = int(input("Ingrese el ID del libro: ").strip())
    except ValueError:
        print("Error: debe ingresar números enteros.")
        cursor.close()
        return

    
    consulta = """
        SELECT 
            pr.id_prestamo,
            pr.fecha_prestamo,
            pr.fecha_vencimiento,
            pr.fecha_devolucion,
            pr.estado,
            u.nombre AS usuario,
            l.titulo AS libro
        FROM prestamos pr
        JOIN usuarios u ON pr.id_usuario = u.id_usuario
        JOIN libros l ON pr.id_libro = l.id_libro
        WHERE pr.id_usuario = %s AND pr.id_libro = %s;
    """

    cursor.execute(consulta, (id_usuario, id_libro))
    prestamo = cursor.fetchone()

    if not prestamo:
        print("\nNo existe un préstamo registrado para ese usuario y libro.")
        cursor.close()
        return

    print(f"\nPréstamo encontrado:")
    print(f"- Usuario: {prestamo['usuario']}")
    print(f"- Libro: {prestamo['libro']}")
    print(f"- Fecha préstamo: {prestamo['fecha_prestamo']}")
    print(f"- Fecha vencimiento: {prestamo['fecha_vencimiento']}")
    print(f"- Estado actual: {prestamo['estado']}")

    # calculo de dias de atraso
    hoy = datetime.now().date()
    fecha_venc = prestamo["fecha_vencimiento"]

    dias_atraso = (hoy - fecha_venc).days
    if dias_atraso < 0:
        dias_atraso = 0

    print(f"\nDías de atraso: {dias_atraso}")

    # ultima cuota del usuario
    cursor.execute("""
        SELECT monto 
        FROM pagos 
        WHERE id_usuario = %s 
        ORDER BY anio DESC, mes DESC 
        LIMIT 1;
    """, (id_usuario,))
    pago = cursor.fetchone()

    if not pago:
        print("\nNo se encontró cuota mensual para el usuario.")
        cursor.close()
        return

    monto_cuota = float(pago["monto"])
    multa = dias_atraso * (monto_cuota * 0.03)

    print(f"Multa calculada: ${multa:.2f}")

    # transaccion
    try:
        
        conexion.rollback()

        print("\nIniciando transacción...")
        conexion.start_transaction()

        marcar = input("¿Desea marcar este préstamo como devuelto? (s/n): ").strip().lower()

        if marcar == "s":
            update = """
                UPDATE prestamos
                SET 
                    estado = 'DEVUELTO',
                    fecha_devolucion = CURDATE()
                WHERE id_prestamo = %s;
            """
            cursor.execute(update, (prestamo["id_prestamo"],))
            print("✔ El préstamo fue marcado como DEVUELTO.")

        confirmar = input("¿Confirmar y guardar los cambios? (s/n): ").strip().lower()

        if confirmar == "s":
            conexion.commit()
            print("\n✔ Transacción completada con éxito. Cambios guardados.")
        else:
            conexion.rollback()
            print("\n✖ Transacción cancelada. No se guardaron cambios.")

    except Exception as e:
        conexion.rollback()
        print("\n ERROR: La transacción falló. Cambios revertidos.")
        print("Detalle:", e)

    cursor.close()




#   4) busqueda y filtrado


def submenu_busqueda(conexion):
    while True:
        print("""
----- BÚSQUEDA Y FILTRADO -----
1. Buscar libros por título o autor
2. Buscar usuario por ID
3. Buscar usuarios por texto (nombre, apellido, DNI o email)
0. Volver al menú principal
""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            buscar_libros_por_texto(conexion)
        elif opcion == "2":
            buscar_usuario_por_id(conexion)
        elif opcion == "3":
            buscar_usuarios_por_texto(conexion)
        elif opcion == "0":
            return
        else:
            print("Opción inválida.")


def buscar_libros_por_texto(conexion):
    cursor = conexion.cursor(dictionary=True)

    print("\n=== BÚSQUEDA DE LIBROS ===")
    termino = input("Ingrese parte del título o autor: ").strip()

    if not termino:
        print("No se ingresó texto de búsqueda.")
        cursor.close()
        return

    like = f"%{termino}%"

    consulta = """
        SELECT id_libro, titulo, autor, anio_publicacion, editorial, categoria
        FROM libros
        WHERE titulo LIKE %s
           OR autor  LIKE %s
        ORDER BY titulo;
    """
    cursor.execute(consulta, (like, like))
    libros = cursor.fetchall()
    cursor.close()

    if not libros:
        print("No se encontraron libros que coincidan.")
    else:
        print("\nResultados:")
        for l in libros:
            print(
                f"ID: {l['id_libro']:2d} | "
                f"{l['titulo']} | "
                f"{l['autor']} | "
                f"Año: {l['anio_publicacion']} | "
                f"Editorial: {l['editorial']} | "
                f"Categoría: {l['categoria']}"
            )


def buscar_usuario_por_id(conexion):
    cursor = conexion.cursor(dictionary=True)

    print("\n=== BÚSQUEDA DE USUARIO POR ID ===")
    id_usuario = input("Ingrese el ID del usuario: ").strip()

    consulta = """
        SELECT id_usuario, nombre, apellido, dni, email, telefono, fecha_alta, activo
        FROM usuarios
        WHERE id_usuario = %s;
    """
    cursor.execute(consulta, (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()

    if not usuario:
        print("No se encontró un usuario con ese ID.")
    else:
        estado = "Activo" if usuario["activo"] == 1 else "Inactivo"
        print("\nUsuario encontrado:")
        print(f"ID       : {usuario['id_usuario']}")
        print(f"Nombre   : {usuario['nombre']} {usuario['apellido']}")
        print(f"DNI      : {usuario['dni']}")
        print(f"Email    : {usuario['email']}")
        print(f"Teléfono : {usuario['telefono']}")
        print(f"Fecha alta: {usuario['fecha_alta']}")
        print(f"Estado   : {estado}")


def buscar_usuarios_por_texto(conexion):
    cursor = conexion.cursor(dictionary=True)

    print("\n=== BÚSQUEDA DE USUARIOS ===")
    termino = input("Ingrese parte del nombre, apellido, DNI o email: ").strip()

    if not termino:
        print("No se ingresó texto de búsqueda.")
        cursor.close()
        return

    like = f"%{termino}%"

    consulta = """
        SELECT id_usuario, nombre, apellido, dni, email, telefono, fecha_alta, activo
        FROM usuarios
        WHERE nombre   LIKE %s
           OR apellido LIKE %s
           OR dni      LIKE %s
           OR email    LIKE %s
        ORDER BY apellido, nombre;
    """
    cursor.execute(consulta, (like, like, like, like))
    usuarios = cursor.fetchall()
    cursor.close()

    if not usuarios:
        print("No se encontraron usuarios que coincidan.")
    else:
        print("\nResultados:")
        for u in usuarios:
            estado = "Activo" if u["activo"] == 1 else "Inactivo"
            print(
                f"ID: {u['id_usuario']:2d} | "
                f"{u['nombre']} {u['apellido']} | "
                f"DNI: {u['dni']} | "
                f"Email: {u['email']} | "
                f"Tel: {u['telefono']} | "
                f"Estado: {estado}"
            )


#  5) reporte de morosos

def reporte_morosos(conexion):
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT 
            u.id_usuario,
            u.nombre,
            u.apellido,
            COUNT(*) AS meses_adeudados
        FROM usuarios u
        JOIN pagos p ON u.id_usuario = p.id_usuario
        WHERE p.pagado = 0
          AND p.fecha_vencimiento < CURDATE()
        GROUP BY u.id_usuario, u.nombre, u.apellido
        ORDER BY meses_adeudados DESC;
    """

    cursor.execute(consulta)
    resultados = cursor.fetchall()

    if not resultados:
        print("\nNo hay usuarios morosos (todos están al día).")
        cursor.close()
        return

    print("\n=== REPORTE DE MOROSOS ===")
    total_meses = 0

    for fila in resultados:
        total_meses += fila["meses_adeudados"]
        print(
            f"ID: {fila['id_usuario']:2d} | "
            f"{fila['nombre']} {fila['apellido']} | "
            f"Meses adeudados: {fila['meses_adeudados']}"
        )

    promedio = total_meses / len(resultados)
    print(f"\nPromedio de meses adeudados entre los morosos: {promedio:.2f}")

    cursor.close()



#  6) modificacion de la cuota

def modificar_cuota_mes(conexion):
    cursor = conexion.cursor(dictionary=True)

    #  años disponibles
    cursor.execute("SELECT DISTINCT anio FROM pagos ORDER BY anio;")
    filas_anios = cursor.fetchall()

    if not filas_anios:
        print("\nNo hay cuotas cargadas en la base de datos.")
        cursor.close()
        return

    anios_disponibles = [fila["anio"] for fila in filas_anios]

    print("\nAños disponibles en pagos:")
    for anio in anios_disponibles:
        print(f"- {anio}")

    # seleccion de año valido
    while True:
        try:
            anio = int(input("Ingrese el año (YYYY): ").strip())
            if anio in anios_disponibles:
                break
            print("Error: ese año no tiene cuotas registradas.")
        except ValueError:
            print("Error: ingrese un número entero válido.")

    # meses disponibles
    cursor.execute(
        "SELECT DISTINCT mes FROM pagos WHERE anio = %s ORDER BY mes;",
        (anio,)
    )
    filas_meses = cursor.fetchall()
    meses_disponibles = [fila["mes"] for fila in filas_meses]

    print(f"\nMeses disponibles para el año {anio}:")
    for mes in meses_disponibles:
        print(f"- {mes}")

    # seleccion de mes valido
    while True:
        try:
            mes = int(input("Ingrese el mes (1-12): ").strip())
            if mes in meses_disponibles:
                break
            print("Error: ese mes no tiene cuotas registradas.")
        except ValueError:
            print("Error: ingrese un número entero válido.")

    # nuevo monto
    while True:
        try:
            nuevo_monto = float(input("Ingrese el nuevo monto: ").strip())
            if nuevo_monto > 0:
                break
            print("Error: el monto debe ser mayor a cero.")
        except ValueError:
            print("Error: ingrese un número válido.")

    
    cursor.execute(
        "SELECT id_pago, id_usuario, monto FROM pagos WHERE anio = %s AND mes = %s;",
        (anio, mes)
    )
    cuotas = cursor.fetchall()

    print(f"\nCuotas que se actualizarán ({anio}-{mes}):")
    for c in cuotas:
        print(f"ID pago: {c['id_pago']} | Usuario {c['id_usuario']} | Monto: {c['monto']}")

    # confirmar
    confirmar = input(
        f"¿Aplicar nuevo monto ({nuevo_monto})? (s/n): "
    ).strip().lower()

    if confirmar != "s":
        print("Operación cancelada.")
        cursor.close()
        return

    # update
    cursor_update = conexion.cursor()
    cursor_update.execute(
        "UPDATE pagos SET monto = %s WHERE anio = %s AND mes = %s;",
        (nuevo_monto, anio, mes)
    )
    conexion.commit()

    print(f"\nCuotas actualizadas correctamente. Filas afectadas: {cursor_update.rowcount}")

    cursor_update.close()
    cursor.close()



#          MENÚ

def mostrar_menu(conexion):

    while True:
        print("""
========= MENÚ BIBLIOTECA =========
1. Gestión de usuarios        
2. Gestión de libros          
3. Manejo de préstamos        
4. Búsqueda y filtrado        
5. Reporte de morosos
6. Modificación de la cuota
0. Salir
""")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
                submenu_usuarios(conexion)
        elif opcion == "2":
                submenu_libros(conexion)
        elif opcion == "3":
                manejo_prestamos(conexion)
        elif opcion == "4":
                submenu_busqueda(conexion)
        elif opcion == "5":
                reporte_morosos(conexion)
        elif opcion == "6":
                modificar_cuota_mes(conexion)
        elif opcion == "0":
                print("Saliendo del sistema...")
                break
        else:
                print("Opción no implementada o inválida.")


      
        while True:
            volver = input("\n¿Desea volver al menú principal? (s/n): ").strip().lower()
            if volver == "s":
                break       # vuelve al menu
            elif volver == "n":
                print("Saliendo del sistema...")
                return      # termina toda la funcion
            else:
                print("Opción inválida. Responda 's' o 'n'.")



#   MAIN

def main():
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        mostrar_menu(conexion)
    finally:
        conexion.close()
        print("Conexión cerrada correctamente.")

if __name__ == "__main__":
    main()
