import os

# Función: guardar_minimarket
# Propósito: Toma las listas que están en la memoria del programa y las escribe 
# línea por línea en archivos .txt separados por comas dentro de la carpeta "Datos".
# Si quieres agregar una nueva columna a tus datos en el futuro, aquí es donde debes añadirla.
def guardar_minimarket(productos, ventas, caja):
    # Verifica si la carpeta "Datos" existe; si alguien la borró, la vuelve a crear automáticamente
    if not os.path.exists("Datos"):
        os.makedirs("Datos")

    # 1. Guardamos el inventario de productos
    # Estructura de cada fila: [código, descripción, categoría, precio, stock, unidades_vendidas]
    f1 = open("Datos/productos.txt", "w", encoding="utf-8")
    for p in productos:
        linea = p[0] + "," + p[1] + "," + p[2] + "," + str(p[3]) + "," + str(p[4]) + "," + str(p[5]) + "\n"
        f1.write(linea)
    f1.close()  # Siempre cerramos el archivo para que los cambios se guarden en disco

    # 2. Guardamos el historial detallado de cada venta realizada
    # Estructura de cada fila: [id_venta, dni_cliente, cod_producto, cantidad, subtotal_linea, descuento, total_boleta]
    f2 = open("Datos/ventas.txt", "w", encoding="utf-8")
    for v in ventas:
        linea = v[0] + "," + v[1] + "," + v[2] + "," + str(v[3]) + "," + str(v[4]) + "," + str(v[5]) + "," + str(v[6]) + "\n"
        f2.write(linea)
    f2.close()

    # 3. Guardamos los movimientos de dinero en la caja registradora
    # Estructura de cada fila: [tipo_movimiento, concepto, monto]
    f3 = open("Datos/caja.txt", "w", encoding="utf-8")
    for c in caja:
        linea = c[0] + "," + c[1] + "," + str(c[2]) + "\n"
        f3.write(linea)
    f3.close()


# Función: cargar_minimarket
# Propósito: Se ejecuta apenas arranca el programa. Busca los archivos .txt en la carpeta "Datos",
# lee cada línea, la corta donde haya comas (split) y reconstruye las listas en memoria.
# Nota: Convierte los textos a números (float o int) según corresponda para poder hacer cálculos después.
def cargar_minimarket():
    productos = []
    ventas = []
    caja = []

    # Recuperar productos guardados anteriormente
    try:
        f1 = open("Datos/productos.txt", "r", encoding="utf-8")
        for linea in f1:
            d = linea.strip().split(",")  # strip() quita el salto de línea y split(",") separa por comas
            if len(d) == 6:  # Verificamos que la línea tenga exactamente los 6 datos esperados
                productos.append([d[0], d[1], d[2], float(d[3]), int(d[4]), int(d[5])])
        f1.close()
    except FileNotFoundError:
        # Si es la primera vez que abres el programa y aún no existe el archivo, no hace nada y empieza vacío
        pass

    # Recuperar historial de ventas
    try:
        f2 = open("Datos/ventas.txt", "r", encoding="utf-8")
        for linea in f2:
            d = linea.strip().split(",")
            if len(d) == 7:
                ventas.append([d[0], d[1], d[2], int(d[3]), float(d[4]), float(d[5]), float(d[6])])
        f2.close()
    except FileNotFoundError:
        pass

    # Recuperar movimientos de caja
    try:
        f3 = open("Datos/caja.txt", "r", encoding="utf-8")
        for linea in f3:
            d = linea.strip().split(",")
            if len(d) == 3:
                caja.append([d[0], d[1], float(d[2])])
        f3.close()
    except FileNotFoundError:
        pass

    # Devuelve las 3 listas cargadas hacia el archivo main.py
    return productos, ventas, caja