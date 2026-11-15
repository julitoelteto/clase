import archivos as arc

# Función: Registrar producto pide los datos de un producto nuevo, valida que no se repita el código ni haya
# precios negativos, lo añade a la lista y guarda inmediatamente en el archivo .txt.
def registrar_producto(productos, ventas, caja):
    cod = input("Código del producto: ").strip().upper().replace(",", "")
    if cod == "": #si esta vacio genera un error y no permite continuar
        print("Error: El código es obligatorio.")
        return

    # Verificamos que el código no exista ya en el inventario
    for p in productos:
        if p[0] == cod:
            print("Error: Ya existe un producto con ese código.")
            return

    desc = input("Descripción: ").strip().capitalize().replace(",", " ")
    cat = input("Categoría: ").strip().upper().replace(",", " ")
    precio = float(input("Precio unitario (S/): "))
    stock = int(input("Stock inicial: "))

    # Precio y stock no sean negativos
    if precio <= 0 or stock < 0:
        print("Error: El precio debe ser mayor a 0 y el stock no puede ser negativo.")
        return

    # El último valor (0) es el contador histórico de unidades vendidas de este producto
    productos.append([cod, desc, cat, precio, stock, 0])
    
    # Guardamos automáticamente para asegurar persistencia
    arc.guardar_minimarket(productos, ventas, caja)
    print("Producto registrado y guardado en Datos/productos.txt")


# Función: actualizar cambiar el precio o el stock de un producto ya registrado.
def actualizar_producto(productos, ventas, caja):
    cod = input("Código del producto a modificar: ").strip().upper()
    for p in productos:
        if p[0] == cod:
            print("Producto actual:", p[1], "| Precio: S/", p[3], "| Stock:", p[4])
            nuevo_precio = float(input("Nuevo precio (S/): "))
            nuevo_stock = int(input("Nuevo stock total: "))
            
            if nuevo_precio > 0 and nuevo_stock >= 0:
                p[3] = nuevo_precio  # Actualiza precio en memoria
                p[4] = nuevo_stock   # Actualiza stock en memoria
                arc.guardar_minimarket(productos, ventas, caja)  # Guarda cambios
                print("Producto actualizado correctamente.")
            else:
                print("Valores inválidos. No se realizaron cambios.")
            return
    print("Producto no encontrado.")


# Función: registrar dinero para la APERTURA de caja (dinero inicial para dar vuelto) 
def registrar_movimiento_caja(productos, ventas, caja, tipo):
    concepto = input("Concepto del movimiento: ").strip().replace(",", " ")
    monto = float(input("Monto (S/): "))
    if monto <= 0:
        print("Error: El monto debe ser mayor a 0.")
        return
    
    caja.append([tipo, concepto, monto])
    arc.guardar_minimarket(productos, ventas, caja)
    print("Movimiento", tipo, "guardado en Datos/caja.txt")


# Función: venta arma un carrito temporal con varios productos, valida que alcance el stock, aplica descuentos, calcula el vuelto y actualiza inventario y caja.
def realizar_venta(productos, ventas, caja):
    dni = input("DNI Cliente (Enter para 'PUBLICO GENERAL'): ").strip().replace(",", "")
    if dni == "":
        dni = "PUBLICO GENERAL"

    carrito = []     # Lista temporal solo para esta venta
    subtotal = 0.0

    # Bucle para agregar todos los productos que el cliente lleva
    while True:
        cod = input("Código de producto (o escriba 'FIN' para cobrar): ").strip().upper()
        if cod == "FIN":
            break

        # Buscamos el producto en el inventario
        prod_encontrado = None
        for p in productos:
            if p[0] == cod:
                prod_encontrado = p
                break

        if prod_encontrado is None:
            print("Producto no encontrado.")
            continue

        print("Seleccionado:", prod_encontrado[1], "| Precio: S/", prod_encontrado[3], "| Stock:", prod_encontrado[4])
        cant = int(input("Cantidad a llevar: "))
        
        # Impedimos vender más de lo que hay en tienda
        if cant <= 0 or cant > prod_encontrado[4]:
            print("Error: Stock insuficiente o cantidad inválida.")
            continue

        importe_linea = cant * prod_encontrado[3]
        subtotal += importe_linea
        # Guardamos en el carrito: 
        carrito.append([prod_encontrado, cant, importe_linea])

    # Si el cajero escribió FIN sin agregar nada, cancelamos
    if len(carrito) == 0:
        print("Venta cancelada.")
        return

    # Cálculo de descuentos y total final
    porc_desc = float(input("Porcentaje de descuento (0 si no aplica): "))
    descuento = subtotal * (porc_desc / 100.0)
    total = subtotal - descuento

    print("\n--- RESUMEN DE PAGO ---")
    print("Subtotal: S/", round(subtotal, 2))
    print("Descuento: S/", round(descuento, 2))
    print("TOTAL A PAGAR: S/", round(total, 2))

    # Validación de pago y cálculo de vuelto
    recibido = float(input("Monto recibido del cliente (S/): "))
    if recibido < total:
        print("Error: Monto recibido insuficiente. Venta anulada.")
        return

    vuelto = recibido - total
    print("Vuelto a entregar: S/", round(vuelto, 2))

    # Confirmamos la venta: descontamos stock, registramos detalle y sumamos el dinero a la caja
    id_venta = "V-" + str(len(ventas) + 101)
    for item in carrito:
        prod = item[0]
        cant = item[1]
        prod[4] -= cant  # Resta al stock disponible
        prod[5] += cant  # Suma al historial de vendidos
        ventas.append([id_venta, dni, prod[0], cant, item[2], round(descuento, 2), round(total, 2)])

    # Registramos el ingreso de dinero en la caja
    caja.append(["INGRESO", "Venta " + id_venta, round(total, 2)])
    
    # Guardamos todo en los 3 archivos .txt
    arc.guardar_minimarket(productos, ventas, caja)
    print("Venta", id_venta, "completada y guardada en Datos/.")


# Función: reportes_minimarket
# Propósito: Procesa las matrices de datos para mostrar los 3 reportes obligatorios que exige la guía:
# 1. Cierre de caja, 2. Productos más vendidos, 3. Ingresos agrupados por categoría.
def reportes_minimarket(productos, ventas, caja):
    saldo_caja = 0.0
    ingresos = 0.0
    egresos = 0.0
    
    # Recorremos los movimientos de caja sumando entradas y restando salidas
    for m in caja:
        if m[0] == "APERTURA" or m[0] == "INGRESO":
            saldo_caja += m[2]
            ingresos += m[2]
        elif m[0] == "EGRESO":
            saldo_caja -= m[2]
            egresos += m[2]

    print("\n--- 1. CIERRE DIARIO DE CAJA ---")
    print("Total Ingresos (inc. apertura): S/", round(ingresos, 2))
    print("Total Egresos: S/", round(egresos, 2))
    print("Saldo Neto en Caja: S/", round(saldo_caja, 2))

    print("\n--- 2. PRODUCTOS MÁS VENDIDOS ---")
    for p in productos:
        if p[5] > 0:  # Solo muestra los que han tenido al menos 1 venta
            print(p[0], "-", p[1], "| Vendidos:", p[5], "unidades")

    print("\n--- 3. INGRESOS POR CATEGORÍA ---")
    # Usamos dos listas paralelas: una guarda los nombres de categorías y otra sus montos acumulados
    categorias = []
    totales_cat = []
    
    for v in ventas:
        cod_p = v[2]
        monto_linea = v[4]
        cat_p = "OTROS"
        
        # Buscamos a qué categoría pertenece el producto vendido
        for p in productos:
            if p[0] == cod_p:
                cat_p = p[2]
                break
                
        # Si la categoría ya está en nuestra lista, le sumamos el dinero; si no, la agregamos
        if cat_p in categorias:
            idx = categorias.index(cat_p)
            totales_cat[idx] += monto_linea
        else:
            categorias.append(cat_p)
            totales_cat.append(monto_linea)

    for i in range(len(categorias)):
        print("Categoría:", categorias[i], "-> S/", round(totales_cat[i], 2))