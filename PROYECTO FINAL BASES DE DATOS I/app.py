from conexion import conectar

# =========================
#   OPCIÓN 5: REPORTE DE MOROSOS
# =========================
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


# =========================
#   OPCIÓN 6: MODIFICACIÓN DE LA CUOTA
# =========================
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
1. Gestión de usuarios        (no implementado)
2. Gestión de libros          (no implementado)
3. Manejo de préstamos        (no implementado)
4. Búsqueda y filtrado        (no implementado)
5. Reporte de morosos
6. Modificación de la cuota
0. Salir
""")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "5":
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

