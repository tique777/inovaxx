"""
seed.py - Datos de prueba para InnovaX
Ejecutar: python seed.py
"""
import os
from database import BaseDatos
from models import Categoria, Movimiento
from datetime import datetime


def sembrar():
    db = BaseDatos()
    print("Creando datos de ejemplo...")

    # Usuarios
    usuarios = [
        ("Juan Garcia", "juan@email.com", "password123", "administrador"),
        ("Maria Lopez", "maria@email.com", "password123", "empleado"),
        ("Carlos Ruiz", "carlos@email.com", "password123", "empleado"),
    ]
    for nombre, correo, clave, rol in usuarios:
        ok, msg = db.crear_usuario(nombre, correo, clave, rol)
        print(f"  Usuario '{nombre}': {'OK' if ok else msg}")

    # Productos
    productos = [
        ("Arroz Blanco",       "P001", Categoria.ALIMENTOS.value,   150, 30, 300, 2.50,   "kg"),
        ("Frijoles Negros",    "P002", Categoria.ALIMENTOS.value,    80, 20, 200, 3.00,   "kg"),
        ("Aceite Vegetal",     "P003", Categoria.ALIMENTOS.value,    45, 10, 100, 5.50,   "botella"),
        ("Harina de Trigo",    "P004", Categoria.ALIMENTOS.value,   200, 50, 400, 1.80,   "kg"),
        ("Azucar",             "P005", Categoria.ALIMENTOS.value,    18, 30, 250, 2.20,   "kg"),
        ("Agua Mineral",       "P006", Categoria.BEBIDAS.value,     300, 50, 600, 0.50,   "botella"),
        ("Refresco Cola",      "P007", Categoria.BEBIDAS.value,     100, 20, 200, 1.20,   "botella"),
        ("Jugo Natural",       "P008", Categoria.BEBIDAS.value,      80, 15, 150, 1.80,   "botella"),
        ("Detergente Liquido", "P009", Categoria.LIMPIEZA.value,     60, 10, 100, 3.50,   "botella"),
        ("Desinfectante",      "P010", Categoria.LIMPIEZA.value,     40,  8,  80, 4.20,   "botella"),
        ("Papel Higienico",    "P011", Categoria.LIMPIEZA.value,    500,100,1000, 0.80,   "paquete"),
        ("Cuaderno A4",        "P012", Categoria.PAPELERIA.value,   200, 30, 400, 1.50,   "unidad"),
        ("Boligrafo Azul",     "P013", Categoria.PAPELERIA.value,   500,100,1000, 0.30,   "unidad"),
        ("Laptop",             "P014", Categoria.ELECTRONICO.value,  15,  3,  30,600.00,  "unidad"),
        ("Mouse Inalambrico",  "P015", Categoria.ELECTRONICO.value,  25,  5,  50, 15.00,  "unidad"),
    ]
    for nombre, codigo, cat, stock, smin, smax, precio, unidad in productos:
        ok, msg = db.crear_producto(nombre, codigo, cat, stock, smin, smax, precio, unidad)
        print(f"  Producto '{nombre}': {'OK' if ok else msg}")

    # Movimientos de ejemplo para que funcione la prediccion
    movimientos = [
        (1, "Entrada", 100, 2, "Compra inicial"),
        (1, "Salida",   30, 3, "Venta"),
        (1, "Salida",   20, 2, "Venta mayorista"),
        (2, "Entrada",  60, 2, "Reabastecimiento"),
        (2, "Salida",   15, 3, "Venta"),
        (3, "Entrada",  80, 2, "Compra proveedor"),
        (3, "Salida",   20, 3, "Venta"),
        (3, "Salida",   15, 2, "Uso interno"),
        (6, "Entrada", 200, 2, "Compra en volumen"),
        (6, "Salida",   50, 3, "Venta supermercado"),
        (6, "Salida",   30, 2, "Venta evento"),
        (9, "Entrada",  40, 2, "Stock inicial"),
        (9, "Salida",    5, 3, "Uso interno"),
        (11,"Salida",   50, 3, "Distribucion"),
        (12,"Salida",   40, 2, "Venta papeleria"),
        (14,"Entrada",  10, 2, "Compra especial"),
        (14,"Salida",    2, 3, "Venta corporativa"),
    ]
    for pid, tipo, cantidad, uid, notas in movimientos:
        mov = Movimiento(
            producto_id=pid, tipo=tipo, cantidad=cantidad,
            usuario_id=uid, fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            notas=notas
        )
        ok, msg = db.crear_movimiento(mov)
        print(f"  Movimiento {tipo} x{cantidad}: {'OK' if ok else msg}")

    print("\nListo. Credenciales de prueba:")
    print("  Admin:    juan@email.com    / password123")
    print("  Empleado: maria@email.com   / password123")


if __name__ == "__main__":
    if os.path.exists("innovax.db"):
        resp = input("Limpiar base de datos existente? (s/n): ")
        if resp.lower() == 's':
            os.remove("innovax.db")
            print("Base de datos limpiada.")
    sembrar()
