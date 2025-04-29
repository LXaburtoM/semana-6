import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('inventario_calzado.db')
c = conn.cursor()

# Crear tabla de productos
c.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL
    )
''')
conn.commit()

def agregar_producto(nombre, cantidad, precio):
    c.execute('INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)', (nombre, cantidad, precio))
    conn.commit()
    print(f'Producto {nombre} agregado con éxito.')

def mostrar_inventario():
    c.execute('SELECT * FROM productos')
    productos = c.fetchall()
    print("Inventario de Calzado:")
    for producto in productos:
        print(f'ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[2]}, Precio: {producto[3]}')

def vender_producto(producto_id, cantidad_vendida):
    c.execute('SELECT cantidad FROM productos WHERE id = ?', (producto_id,))
    producto = c.fetchone()
    if producto and producto[0] >= cantidad_vendida:
        nueva_cantidad = producto[0] - cantidad_vendida
        c.execute('UPDATE productos SET cantidad = ? WHERE id = ?', (nueva_cantidad, producto_id))
        conn.commit()
        print(f'Venta realizada. {cantidad_vendida} unidades de ID {producto_id} vendidas.')
    else:
        print('No hay suficiente stock para realizar la venta.')

def main():
    while True:
        print("\nSistema de Gestión de Inventario de Calzado")
        print("1. Agregar Producto")
        print("2. Mostrar Inventario")
        print("3. Vender Producto")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Ingrese el nombre del producto: ")
            cantidad = int(input("Ingrese la cantidad: "))
            precio = float(input("Ingrese el precio: "))
            agregar_producto(nombre, cantidad, precio)
        elif opcion == '2':
            mostrar_inventario()
        elif opcion == '3':
            producto_id = int(input("Ingrese el ID del producto a vender: "))
            cantidad_vendida = int(input("Ingrese la cantidad a vender: "))
            vender_producto(producto_id, cantidad_vendida)
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

    # Cerrar la conexión a la base de datos
    conn.close()

if __name__ == "__main__":
    main()