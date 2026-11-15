import archivos as arc
import operaciones as op
import funciones as fn

# Funcion: menu carga los datos al iniciar bucle infinito (while True) hasta que el usuario elija salir
def menu():
    # Carga la información guardada en sesiones anteriores
    productos, ventas, caja = arc.cargar_minimarket()
    
    # Mostramos menu principal
    while True:
        print("\n=== SISTEMA DE CAJA Y VENTAS - MINIMARKET ===")
        print("1. Registrar producto")
        print("2. Actualizar precio o stock de producto")
        print("3. Registrar apertura de caja")
        print("4. Realizar venta")
        print("5. Registrar egreso de caja")
        print("6. Buscar producto (código o nombre)")
        print("7. Listar productos ordenados por precio (Selección)")
        print("8. Reportes y cierre diario de caja")
        print("9. Guardar y Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            fn.registrar_producto(productos, ventas, caja)
        elif opcion == "2":
            fn.actualizar_producto(productos, ventas, caja)
        elif opcion == "3":
            fn.registrar_movimiento_caja(productos, ventas, caja, "APERTURA")
        elif opcion == "4":
            fn.realizar_venta(productos, ventas, caja)
        elif opcion == "5":
            fn.registrar_movimiento_caja(productos, ventas, caja, "EGRESO")
        elif opcion == "6":
            crit = input("Ingrese código o nombre a buscar: ")
            encontrados = op.buscar_producto(productos, crit)
            if len(encontrados) == 0:
                print("Sin coincidencias.")
            else:
                for p in encontrados:
                    print("Cód:", p[0], "| Desc:", p[1], "| Cat:", p[2], "| Precio: S/", p[3], "| Stock:", p[4])
        elif opcion == "7":
            op.ordenar_productos_seleccion(productos)
            for p in productos:
                print("Cód:", p[0], "| Desc:", p[1], "| Cat:", p[2], "| Precio: S/", p[3], "| Stock:", p[4])
        elif opcion == "8":
            fn.reportes_minimarket(productos, ventas, caja)
        elif opcion == "9":
            arc.guardar_minimarket(productos, ventas, caja)
            print("Todos los datos guardados en Datos/. Saliendo...")
            break  # Rompe el bucle while y termina el programa
        else:
            print("Opción inválida. Intente nuevamente.")

# Punto de arranque estándar en Python: asegura que el menú solo se ejecute si corremos este archivo directamente
if __name__ == "__main__":
    menu()
