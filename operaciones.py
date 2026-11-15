# Función: ordenar_productos_seleccion
# Propósito: Ordena la lista de productos de menor a mayor precio usando el algoritmo de Selección manual.
# Cómo funciona: Busca el producto más barato de toda la lista y lo pone primero; luego busca el segundo
# más barato y lo pone segundo, y así sucesivamente.
# Dato clave: p[3] es la posición donde se guarda el precio. Si quisieras ordenar por stock, cambiarías [3] por [4].
def ordenar_productos_seleccion(productos):
    n = len(productos)
    for i in range(n):
        min_idx = i  # Asumimos que el elemento actual es el más barato
        for j in range(i + 1, n):
            # Comparamos los precios (índice 3)
            if productos[j][3] < productos[min_idx][3]:
                min_idx = j  # Encontramos uno más barato, guardamos su posición
        
        # Intercambiamos de lugar el producto actual con el más barato encontrado
        temp = productos[i]
        productos[i] = productos[min_idx]
        productos[min_idx] = temp


# Función: buscar_producto
# Propósito: Busca coincidencias en el inventario ya sea por código exacto o por parte del nombre.
# Parámetros: Recibe la lista completa de productos y el texto que escribió el usuario.
# Retorno: Devuelve una nueva lista llamada "encontrados" solo con los productos que coinciden.
def buscar_producto(productos, texto):
    criterio = texto.strip().lower()  # Pasamos todo a minúsculas para que "Leche" y "leche" coincidan igual
    encontrados = []
    for p in productos:
        # p[0] es el código (búsqueda exacta) | p[1] es la descripción (búsqueda parcial con 'in')
        if criterio == p[0].lower() or criterio in p[1].lower():
            encontrados.append(p)
    return encontrados