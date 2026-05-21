# InnovaX - Sistema de Inventario Predictivo

Sistema de gestion de inventario para micro y pequeñas empresas, con prediccion de demanda, analisis ABC y control de stock en tiempo real.

## Instalacion

```bash
pip install -r requirements.txt
```

## Ejecucion

```bash
# Crear datos de prueba (solo la primera vez)
python seed.py

# Iniciar la aplicacion
python main.py
```

## Credenciales de prueba

| Rol           | Correo              | Contrasena  |
|---------------|---------------------|-------------|
| Administrador | juan@email.com      | password123 |
| Empleado      | maria@email.com     | password123 |

## Funcionalidades

### Empleado
- Ver inventario con estado visual de stock (barras de progreso)
- Registrar entradas y salidas con validacion en tiempo real
- Ver su propio historial de movimientos

### Administrador
- **Resumen**: dashboard con metricas, alertas criticas, grafica de actividad 7 dias, top consumo por producto y por categoria
- **Productos**: CRUD completo con visualizacion de valor total por producto
- **Movimientos**: historial completo con opcion de reversion
- **Prediccion**: analisis de consumo diario/mensual, dias restantes de stock, punto de reorden y recomendacion de compra con costo estimado
- **Analisis ABC**: clasificacion Pareto (A/B/C) por valor de movimiento mensual
- **Usuarios**: gestion de usuarios con roles

## Estructura del proyecto

```
innovax/
├── main.py          # Punto de entrada y navegacion
├── models.py        # Clases de datos (Usuario, Producto, Movimiento)
├── database.py      # Operaciones SQLite (CRUD)
├── services.py      # Logica de negocio y prediccion
├── screens.py       # Pantallas de la aplicacion
├── ui_components.py # Componentes reutilizables y graficas
├── seed.py          # Datos de prueba
└── requirements.txt
```
