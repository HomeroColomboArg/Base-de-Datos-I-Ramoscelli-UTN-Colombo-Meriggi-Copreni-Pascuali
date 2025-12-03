from PROYECTO_SQL import conectar
from datetime import date, datetime


#   1) GESTIÓN DE USUARIOS 


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

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s;", (id_usuario,))
    usuario = cursor.fetchone()

    if not usuario:
        print("No existe un usuario con ese ID.")
        cursor.close()
        return

    print(f"Actualizando a: {usuario['nombre']} {usuario['apellido']}")

    nuevo_nombre = input(f"Nuevo nombre ({usuario['nombre']}): ").strip() or usuario['nombre']
    nuevo_apellido = input(f"Nuevo apellido ({usuario['apellido']}): ").strip() or usuario['apellido']
    nuevo_email = input(f"Nuevo email ({usuario['email']}): ").strip() or usuario['email']
    nuevo_tel = input(f"Nuevo teléfono ({usuario['telefono']}): ").strip() or usuario['telefono']

    consulta = """
        UPDATE usuarios
        SET nombre = %s, apellido = %s, email = %s, telefono = %s
        WHERE id_usuario = %s;
    """

    cursor2 = conexion.cursor()
    cursor2.execute(consulta, (nuevo_nombre, nuevo_apellido, nuevo_email, nuevo_tel, id_usuario))
    conexion.commit()

    print("\nUsuario actualizado correctamente.")

    cursor.close()
    cursor2.close()


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


#   2) GESTIÓN DE LIBROS 


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


#   3) MANEJO DE PRÉSTAMOS  (cálculo de multa)


def submenu_prestamos(conexion):
        while True:
            print("""
     ----- MANEJO DE PRÉSTAMOS -----
     1. Calcular multa por retraso para un socio
     0. Volver al menú principal
     """)
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                calcular_multa_socio(conexion)
            elif opcion == "0":
                return
            else:
                print("Opción inválida.")


def calcular_multa_socio(conexion):
    cursor = conexion.cursor(dictionary=True)

    print("\n=== CÁLCULO DE MULTA POR RETRASO ===")
    id_usuario = input("Ingrese el ID del usuario: ").strip()

    
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s;", (id_usuario,))
    usuario = cursor.fetchone()

    if not usuario:
        print("No existe un usuario con ese ID.")
        cursor.close()
        return

    
    consulta = """
        SELECT 
            pr.id_prestamo,
            pr.fecha_prestamo,
            pr.fecha_vencimiento,
            pr.fecha_devolucion,
            pr.estado,
            pa.monto AS cuota_mensual
        FROM prestamos pr
        LEFT JOIN pagos pa
            ON pa.id_usuario = pr.id_usuario
           AND pa.anio = YEAR(pr.fecha_vencimiento)
           AND pa.mes  = MONTH(pr.fecha_vencimiento)
        WHERE pr.id_usuario = %s
        ORDER BY pr.fecha_prestamo;
    """
    cursor.execute(consulta, (id_usuario,))
    prestamos = cursor.fetchall()
    cursor.close()

    if not prestamos:
        print("\nEse usuario no tiene préstamos registrados.")
        return

    
    texto_fecha = input(
        "Ingrese la fecha actual para el cálculo (YYYY-MM-DD) o deje vacío para usar la fecha de hoy: "
    ).strip()

    if texto_fecha:
        try:
            fecha_hoy = datetime.strptime(texto_fecha, "%Y-%m-%d").date()
        except ValueError:
            print("Formato inválido, se usa la fecha de hoy del sistema.")
            fecha_hoy = date.today()
    else:
        fecha_hoy = date.today()

    total_multa = 0  

    print(f"\nPréstamos del usuario {usuario['nombre']} {usuario['apellido']}:\n")

    for p in prestamos:
        fecha_venc = p["fecha_vencimiento"]
        fecha_dev = p["fecha_devolucion"]
        cuota = p["cuota_mensual"]

        
        if fecha_dev is None:
            fecha_dev_str = "Todavía no devolvió"
        else:
            fecha_dev_str = str(fecha_dev)

        
        if cuota is None:
            dias_atraso = 0
            multa = 0.0
        else:
            if fecha_dev is not None:
                fecha_fin = fecha_dev
            else:
                fecha_fin = fecha_hoy

            if fecha_fin > fecha_venc:
                dias_atraso = (fecha_fin - fecha_venc).days
                multa = dias_atraso * 0.03 * float(cuota)
            else:
                dias_atraso = 0
                multa = 0.0

        total_multa += multa

        print(
            f"Préstamo ID: {p['id_prestamo']} | "
            f"Estado: {p['estado']} | "
            f"Vence: {fecha_venc} | "
            f"Devolución: {fecha_dev_str} | "
            f"Días atraso: {dias_atraso} | "
            f"Cuota: {cuota if cuota is not None else 'N/A'} | "
            f"Multa: ${multa:.2f}"
        )

    print(f"\n>>> Multa TOTAL para el usuario {usuario['nombre']} {usuario['apellido']}: ${total_multa:.2f}")



#   4) BÚSQUEDA Y FILTRADO


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


#  5) REPORTE DE MOROSOS

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



#  6) MODIFICACIÓN DE LA CUOTA

def modificar_cuota_mes(conexion):
    cursor = conexion.cursor(dictionary=True)

    # 1) Años disponibles
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

    # Selección de año válido
    while True:
        try:
            anio = int(input("Ingrese el año (YYYY): ").strip())
            if anio in anios_disponibles:
                break
            print("Error: ese año no tiene cuotas registradas.")
        except ValueError:
            print("Error: ingrese un número entero válido.")

    # 2) Meses disponibles
    cursor.execute(
        "SELECT DISTINCT mes FROM pagos WHERE anio = %s ORDER BY mes;",
        (anio,)
    )
    filas_meses = cursor.fetchall()
    meses_disponibles = [fila["mes"] for fila in filas_meses]

    print(f"\nMeses disponibles para el año {anio}:")
    for mes in meses_disponibles:
        print(f"- {mes}")

    # Selección de mes válido
    while True:
        try:
            mes = int(input("Ingrese el mes (1-12): ").strip())
            if mes in meses_disponibles:
                break
            print("Error: ese mes no tiene cuotas registradas.")
        except ValueError:
            print("Error: ingrese un número entero válido.")

    # 3) Nuevo monto
    while True:
        try:
            nuevo_monto = float(input("Ingrese el nuevo monto: ").strip())
            if nuevo_monto > 0:
                break
            print("Error: el monto debe ser mayor a cero.")
        except ValueError:
            print("Error: ingrese un número válido.")

    # Preview
    cursor.execute(
        "SELECT id_pago, id_usuario, monto FROM pagos WHERE anio = %s AND mes = %s;",
        (anio, mes)
    )
    cuotas = cursor.fetchall()

    print(f"\nCuotas que se actualizarán ({anio}-{mes}):")
    for c in cuotas:
        print(f"ID pago: {c['id_pago']} | Usuario {c['id_usuario']} | Monto: {c['monto']}")

    # Confirmación
    confirmar = input(
        f"¿Aplicar nuevo monto ({nuevo_monto})? (s/n): "
    ).strip().lower()

    if confirmar != "s":
        print("Operación cancelada.")
        cursor.close()
        return

    # UPDATE
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
                submenu_prestamos(conexion)
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
                break       # vuelve al menú
            elif volver == "n":
                print("Saliendo del sistema...")
                return      # termina toda la función, se cierra conexión en main()
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
