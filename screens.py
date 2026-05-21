"""
screens.py - Pantallas de InnovaX
Login, Inicio, Panel Empleado, Panel Administrador
"""
import flet as ft
from typing import Callable
from ui_components import (
    Colores, Badge, TarjetaMetrica, CampoTexto, Boton,
    PestanaUI, Notificacion, Tipografia, GraficaBarras
)
from services import ServicioInventario, ServicioUsuarios, ServicioPrediccion
from models import Categoria, EstadoStock


# ============================================================
#  PANTALLA DE INICIO (landing)
# ============================================================

class PantallaInicio:
    def __init__(self, page: ft.Page, on_ir_login: Callable):
        self.page = page
        self.on_ir_login = on_ir_login

    def construir(self) -> ft.Column:
        return ft.Column(
            spacing=0,
            controls=[
                self._navbar(),
                self._hero(),
                self._caracteristicas(),
                self._footer(),
            ]
        )

    def _navbar(self) -> ft.Container:
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=40, vertical=16),
            bgcolor=Colores.AZUL_OSCURO,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(spacing=12, controls=[
                        ft.Icon(ft.Icons.INVENTORY_2, size=36, color=Colores.BLANCO),
                        ft.Text("InnovaX", size=22, weight=ft.FontWeight.BOLD, color=Colores.BLANCO),
                    ]),
                    ft.ElevatedButton(
                        "Iniciar sesion",
                        bgcolor=Colores.AZUL_PRIMARIO,
                        color=Colores.BLANCO,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                        on_click=self.on_ir_login,
                    ),
                ]
            )
        )

    def _hero(self) -> ft.Container:
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=60, vertical=80),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[Colores.AZUL_OSCURO, Colores.AZUL_PRIMARIO],
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Icon(ft.Icons.INVENTORY_2, size=80, color=Colores.BLANCO),
                    ft.Text(
                        "Gestion Inteligente de Inventario",
                        size=36, weight=ft.FontWeight.BOLD,
                        color=Colores.BLANCO,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Control en tiempo real, prediccion de demanda y analisis de stock\npara micro y pequeñas empresas.",
                        size=16, color="rgba(255,255,255,0.8)",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=10),
                    Boton.primario("Comenzar ahora", self.on_ir_login, ancho=220),
                ]
            )
        )

    def _caracteristicas(self) -> ft.Container:
        items = [
            (ft.Icons.SPEED, "Control en tiempo real",
             "Visualiza el estado de tu inventario en cualquier momento."),
            (ft.Icons.AUTO_GRAPH, "Prediccion de demanda",
             "Estima cuanto y cuando reponer cada producto automaticamente."),
            (ft.Icons.PEOPLE, "Gestion de usuarios",
             "Roles de empleado y administrador con acceso diferenciado."),
            (ft.Icons.ANALYTICS, "Analisis ABC",
             "Identifica cuales productos generan mas valor para tu negocio."),
        ]

        tarjetas = []
        for icono, titulo, desc in items:
            tarjetas.append(
                ft.Container(
                    width=260, padding=24,
                    border_radius=16, bgcolor=Colores.BLANCO,
                    shadow=ft.BoxShadow(blur_radius=12, color="rgba(0,0,0,0.08)"),
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Container(
                                width=50, height=50, border_radius=25,
                                bgcolor=Colores.AZUL_CLARO,
                                alignment=ft.alignment.center,
                                content=ft.Icon(icono, size=26, color=Colores.AZUL_PRIMARIO)
                            ),
                            ft.Text(titulo, size=15, weight=ft.FontWeight.BOLD, color=Colores.NEGRO),
                            ft.Text(desc, size=12, color=Colores.GRIS),
                        ]
                    )
                )
            )

        return ft.Container(
            padding=ft.padding.symmetric(horizontal=40, vertical=60),
            bgcolor=Colores.GRIS_MUY_CLARO,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
                controls=[
                    Tipografia.titulo_seccion("Por que usar InnovaX"),
                    Tipografia.subtitulo("Herramientas diseñadas para hacer crecer tu negocio"),
                    ft.Row(wrap=True, spacing=20, alignment=ft.MainAxisAlignment.CENTER, controls=tarjetas),
                ]
            )
        )

    def _footer(self) -> ft.Container:
        return ft.Container(
            padding=20, bgcolor=Colores.NEGRO,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
                controls=[
                    ft.Text("InnovaX", size=16, weight=ft.FontWeight.BOLD, color=Colores.BLANCO),
                    ft.Text("Sistema de inventario predictivo - 2026", size=12, color=Colores.GRIS),
                ]
            )
        )


# ============================================================
#  PANTALLA DE LOGIN
# ============================================================

class PantallaLogin:
    def __init__(self, page: ft.Page, on_login: Callable, on_ir_inicio: Callable):
        self.page = page
        self.on_login = on_login
        self.on_ir_inicio = on_ir_inicio
        self.svc_usuarios = ServicioUsuarios()

    def construir(self) -> ft.Container:
        campo_correo = CampoTexto.crear("Correo electronico", icon=ft.Icons.EMAIL_OUTLINED)
        campo_clave  = CampoTexto.crear("Contrasena", icon=ft.Icons.LOCK_OUTLINE, password=True)
        msg_error    = ft.Text("", color=Colores.ROJO, size=13)

        def hacer_login(e):
            correo = campo_correo.value.strip()
            clave  = campo_clave.value.strip()
            if not correo or not clave:
                msg_error.value = "Completa todos los campos"
                self.page.update()
                return
            ok, usuario = self.svc_usuarios.db.autenticar_usuario(correo, clave)
            if ok:
                self.on_login(usuario)
            else:
                msg_error.value = "Correo o contrasena incorrectos"
                self.page.update()

        return ft.Container(
            expand=True,
            bgcolor=Colores.GRIS_MUY_CLARO,
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=450, border_radius=16, bgcolor=Colores.BLANCO, padding=40,
                        shadow=ft.BoxShadow(blur_radius=24, color="rgba(0,0,0,0.12)", offset=ft.Offset(0, 8)),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                ft.Icon(ft.Icons.INVENTORY_2, size=70, color=Colores.AZUL_PRIMARIO),
                                Tipografia.titulo_seccion("InnovaX"),
                                Tipografia.subtitulo("Gestion inteligente de inventario"),
                                ft.Divider(color=Colores.AZUL_CLARO),
                                campo_correo,
                                campo_clave,
                                msg_error,
                                Boton.primario("Iniciar sesion", hacer_login, ancho=370),
                                ft.TextButton(
                                    "Volver al inicio",
                                    style=ft.ButtonStyle(color=Colores.GRIS),
                                    on_click=self.on_ir_inicio
                                ),
                            ]
                        )
                    )
                ]
            )
        )


# ============================================================
#  HELPER: navbar reutilizable
# ============================================================

def crear_navbar(page, nombre_usuario: str, rol: str, on_cerrar_sesion: Callable) -> ft.Container:
    """Barra superior comun para empleado y admin"""
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=30, vertical=14),
        bgcolor=Colores.AZUL_OSCURO,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(spacing=12, controls=[
                    ft.Icon(ft.Icons.INVENTORY_2, size=36, color=Colores.BLANCO),
                    ft.Text("InnovaX", size=20, weight=ft.FontWeight.BOLD, color=Colores.BLANCO),
                    ft.Container(
                        bgcolor="rgba(255,255,255,0.2)", border_radius=16,
                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        content=ft.Text(rol, size=11, color=Colores.BLANCO)
                    ),
                ]),
                ft.Row(spacing=12, controls=[
                    ft.Text(f"Hola, {nombre_usuario.split()[0]}", color=Colores.BLANCO, size=14),
                    Boton.peligro("Cerrar sesion", on_cerrar_sesion),
                ]),
            ]
        )
    )


# ============================================================
#  PANEL EMPLEADO
# ============================================================

class PanelEmpleado:
    def __init__(self, page: ft.Page, usuario: dict, on_cerrar_sesion: Callable):
        self.page = page
        self.usuario = usuario
        self.on_cerrar_sesion = on_cerrar_sesion
        self.svc = ServicioInventario()
        self.pestanas = PestanaUI(["Inventario", "Registrar Movimiento", "Mis Movimientos"])
        self.cuerpo = ft.Container(expand=True)
        self.contenidos = []

    def construir(self) -> ft.Column:
        navbar = crear_navbar(self.page, self.usuario['nombre'],
                              "Empleado", self.on_cerrar_sesion)
        botones = self.pestanas.crear_botones(self._cambiar_pestana)

        self.contenidos = [
            ft.Container(self._tab_inventario(), padding=30),
            ft.Container(self._tab_registrar(), padding=30),
            ft.Container(self._tab_mis_movimientos(), padding=30),
        ]
        self.cuerpo.content = self.contenidos[0]

        return ft.Column(spacing=0, expand=True, controls=[
            navbar,
            self.pestanas.crear_barra(),
            self.cuerpo,
        ])

    def _cambiar_pestana(self, indice: int):
        self.pestanas.actualizar_activa(indice)
        # Reconstruir tab de movimientos para reflejar cambios recientes
        if indice == 2:
            self.contenidos[2] = ft.Container(self._tab_mis_movimientos(), padding=30)
        self.cuerpo.content = self.contenidos[indice]
        self.page.update()

    def _tab_inventario(self) -> ft.Column:
        """Tabla de todos los productos con estado y barra de stock"""
        productos = self.svc.obtener_todos_productos()

        filas_tabla = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(p.nombre, size=13)),
                ft.DataCell(ft.Text(p.categoria, size=12, color=Colores.GRIS)),
                ft.DataCell(ft.Text(f"{p.stock_actual} {p.unidad}",
                                    size=13, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(f"Min: {p.stock_minimo}", size=12, color=Colores.GRIS)),
                ft.DataCell(Badge.estado_stock(p.calcular_estado())),
            ])
            for p in productos
        ]

        tabla = ft.DataTable(
            border=ft.border.all(1, Colores.AZUL_CLARO),
            border_radius=10,
            heading_row_color=Colores.AZUL_CLARO,
            columns=[
                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD, size=13)),
                ft.DataColumn(ft.Text("Categoria", weight=ft.FontWeight.BOLD, size=13)),
                ft.DataColumn(ft.Text("Stock", weight=ft.FontWeight.BOLD, size=13)),
                ft.DataColumn(ft.Text("Minimo", weight=ft.FontWeight.BOLD, size=13)),
                ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD, size=13)),
            ],
            rows=filas_tabla,
        )

        # Barras de stock visuales para los primeros 8 productos
        barras = [
            GraficaBarras.stock_producto(
                p.nombre, p.stock_actual, p.stock_minimo, p.stock_maximo, p.unidad
            )
            for p in productos[:8]
        ]

        return ft.Column(
            spacing=16, scroll=ft.ScrollMode.AUTO,
            controls=[
                Tipografia.titulo_seccion("Inventario Actual"),
                Tipografia.subtitulo(f"{len(productos)} productos registrados"),
                ft.Divider(color=Colores.AZUL_CLARO),
                ft.Text("Estado visual del stock", size=14,
                        weight=ft.FontWeight.BOLD, color=Colores.NEGRO),
                ft.Column(spacing=8, controls=barras),
                ft.Divider(color=Colores.AZUL_CLARO),
                ft.Text("Tabla completa", size=14,
                        weight=ft.FontWeight.BOLD, color=Colores.NEGRO),
                tabla,
            ]
        )

    def _tab_registrar(self) -> ft.Column:
        """Formulario para registrar entradas y salidas"""
        productos = self.svc.obtener_todos_productos()
        opciones = [
            ft.dropdown.Option(key=str(p.id), text=f"{p.nombre} ({p.stock_actual} {p.unidad})")
            for p in productos
        ]

        dd_producto = ft.Dropdown(label="Producto", width=380, options=opciones, border_radius=10)
        dd_tipo = ft.Dropdown(
            label="Tipo",
            width=380,
            options=[ft.dropdown.Option("Entrada"), ft.dropdown.Option("Salida")],
            border_radius=10
        )
        tf_cantidad = ft.TextField(label="Cantidad", width=380, border_radius=10,
                                   keyboard_type=ft.KeyboardType.NUMBER)
        tf_notas = ft.TextField(label="Notas (opcional)", width=380, border_radius=10,
                                multiline=True, max_lines=3)
        msg = ft.Text("", size=13)

        # Panel de informacion del producto seleccionado
        info_producto = ft.Container(visible=False)

        def actualizar_info(e):
            """Muestra info del producto elegido"""
            if not dd_producto.value:
                return
            pid = int(dd_producto.value)
            p = self.svc.obtener_producto(pid)
            if p:
                info_producto.content = ft.Container(
                    padding=12, border_radius=10, bgcolor=Colores.AZUL_CLARO,
                    content=ft.Row(
                        spacing=20,
                        controls=[
                            ft.Column(controls=[
                                ft.Text("Stock actual", size=11, color=Colores.GRIS),
                                ft.Text(f"{p.stock_actual} {p.unidad}", size=18,
                                        weight=ft.FontWeight.BOLD, color=Colores.AZUL_OSCURO),
                            ]),
                            ft.Column(controls=[
                                ft.Text("Minimo", size=11, color=Colores.GRIS),
                                ft.Text(str(p.stock_minimo), size=18,
                                        weight=ft.FontWeight.BOLD, color=Colores.AMARILLO),
                            ]),
                            ft.Column(controls=[
                                ft.Text("Maximo", size=11, color=Colores.GRIS),
                                ft.Text(str(p.stock_maximo), size=18,
                                        weight=ft.FontWeight.BOLD, color=Colores.VERDE),
                            ]),
                            Badge.estado_stock(p.calcular_estado()),
                        ]
                    )
                )
                info_producto.visible = True
                self.page.update()

        dd_producto.on_change = actualizar_info

        def registrar(e):
            if not dd_producto.value or not dd_tipo.value or not tf_cantidad.value:
                msg.value = "Completa todos los campos obligatorios"
                msg.color = Colores.ROJO
                self.page.update()
                return
            try:
                cantidad = int(tf_cantidad.value)
                if cantidad <= 0:
                    raise ValueError()
            except ValueError:
                msg.value = "La cantidad debe ser un numero positivo"
                msg.color = Colores.ROJO
                self.page.update()
                return

            pid = int(dd_producto.value)
            notas = tf_notas.value.strip()
            uid   = self.usuario['id']

            if dd_tipo.value == "Entrada":
                ok, texto = self.svc.registrar_entrada(pid, cantidad, uid, notas)
            else:
                ok, texto = self.svc.registrar_salida(pid, cantidad, uid, notas)

            msg.value = texto
            msg.color = Colores.VERDE if ok else Colores.ROJO

            if ok:
                dd_producto.value = None
                dd_tipo.value = None
                tf_cantidad.value = ""
                tf_notas.value = ""
                info_producto.visible = False

            self.page.update()

        return ft.Column(
            spacing=16, scroll=ft.ScrollMode.AUTO,
            controls=[
                Tipografia.titulo_seccion("Registrar Movimiento"),
                Tipografia.subtitulo("Registra una entrada o salida de producto"),
                ft.Divider(color=Colores.AZUL_CLARO),
                dd_producto,
                info_producto,
                dd_tipo,
                tf_cantidad,
                tf_notas,
                msg,
                Boton.primario("Registrar", registrar, ancho=380),
            ]
        )

    def _tab_mis_movimientos(self) -> ft.Column:
        """Historial de movimientos registrados por este empleado"""
        todos = self.svc.obtener_movimientos(200)
        # Filtrar solo los del usuario actual
        movs = [m for m in todos if m['usuario_id'] == self.usuario['id']]

        if not movs:
            return ft.Column(controls=[
                Tipografia.titulo_seccion("Mis Movimientos"),
                ft.Text("Aun no has registrado movimientos", color=Colores.GRIS, size=13),
            ])

        filas = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(m['fecha'][:16], size=11, color=Colores.GRIS)),
                ft.DataCell(ft.Text(m['producto_nombre'], size=12)),
                ft.DataCell(ft.Container(
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    border_radius=16,
                    bgcolor=Colores.VERDE_CLARO if m['tipo'] == 'Entrada' else Colores.ROJO_CLARO,
                    content=ft.Text(
                        m['tipo'], size=11, weight=ft.FontWeight.BOLD,
                        color=Colores.VERDE if m['tipo'] == 'Entrada' else Colores.ROJO
                    )
                )),
                ft.DataCell(ft.Text(str(m['cantidad']), size=12, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(m['notas'] or "-", size=11, color=Colores.GRIS)),
            ])
            for m in movs
        ]

        tabla = ft.DataTable(
            border=ft.border.all(1, Colores.AZUL_CLARO),
            border_radius=10,
            heading_row_color=Colores.AZUL_CLARO,
            columns=[
                ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Notas", weight=ft.FontWeight.BOLD, size=12)),
            ],
            rows=filas
        )

        return ft.Column(
            spacing=16, scroll=ft.ScrollMode.AUTO,
            controls=[
                Tipografia.titulo_seccion("Mis Movimientos"),
                Tipografia.subtitulo(f"{len(movs)} movimientos registrados por ti"),
                ft.Divider(color=Colores.AZUL_CLARO),
                tabla,
            ]
        )


# ============================================================
#  PANEL ADMINISTRADOR
# ============================================================

class PanelAdministrador:
    def __init__(self, page: ft.Page, usuario: dict, on_cerrar_sesion: Callable):
        self.page = page
        self.usuario = usuario
        self.on_cerrar_sesion = on_cerrar_sesion
        self.svc = ServicioInventario()
        self.svc_usuarios = ServicioUsuarios()
        self.svc_pred = ServicioPrediccion()
        self.pestanas = PestanaUI([
            "Resumen", "Productos", "Movimientos",
            "Prediccion", "Analisis ABC", "Usuarios"
        ])
        self.cuerpo = ft.Container(expand=True)
        self.contenidos = []

    def construir(self) -> ft.Column:
        navbar = crear_navbar(self.page, self.usuario['nombre'],
                              "Administrador", self.on_cerrar_sesion)
        self.pestanas.crear_botones(self._cambiar_pestana)

        self.contenidos = [
            ft.Container(self._tab_resumen(), padding=30),
            ft.Container(self._tab_productos(), padding=30),
            ft.Container(self._tab_movimientos(), padding=30),
            ft.Container(self._tab_prediccion(), padding=30),
            ft.Container(self._tab_abc(), padding=30),
            ft.Container(self._tab_usuarios(), padding=30),
        ]
        self.cuerpo.content = self.contenidos[0]

        return ft.Column(spacing=0, expand=True, controls=[
            navbar,
            self.pestanas.crear_barra(),
            self.cuerpo,
        ])

    def _cambiar_pestana(self, indice: int):
        # Reconstruir al cambiar para datos actualizados
        constructores = [
            self._tab_resumen, self._tab_productos, self._tab_movimientos,
            self._tab_prediccion, self._tab_abc, self._tab_usuarios,
        ]
        self.pestanas.actualizar_activa(indice)
        self.contenidos[indice] = ft.Container(constructores[indice](), padding=30)
        self.cuerpo.content = self.contenidos[indice]
        self.page.update()

    # ── RESUMEN ──

    def _tab_resumen(self) -> ft.Column:
        resumen = self.svc.obtener_resumen()
        criticos = self.svc.obtener_productos_criticos()
        actividad = self.svc.obtener_movimientos_por_dia(7)
        top_consumo = self.svc.obtener_top_productos_consumo(5)
        consumo_cat = self.svc.obtener_consumo_por_categoria()

        # Tarjetas de metricas
        metricas = ft.Row(
            wrap=True, spacing=16,
            controls=[
                TarjetaMetrica.crear("Total Productos",
                                     str(resumen['total_productos']),
                                     ft.Icons.INVENTORY_2, Colores.AZUL_PRIMARIO),
                TarjetaMetrica.crear("Stock Critico",
                                     str(resumen['productos_criticos']),
                                     ft.Icons.WARNING, Colores.ROJO),
                TarjetaMetrica.crear("Stock Normal",
                                     str(resumen['productos_normales']),
                                     ft.Icons.CHECK_CIRCLE, Colores.VERDE),
                TarjetaMetrica.crear("Valor Total",
                                     f"${resumen['valor_inventario']:,.0f}",
                                     ft.Icons.ATTACH_MONEY, Colores.AMARILLO),
            ]
        )

        # Productos criticos destacados
        items_criticos = []
        if criticos:
            for p in criticos[:5]:
                items_criticos.append(ft.Container(
                    padding=12, border_radius=10, bgcolor=Colores.ROJO_CLARO,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(spacing=2, controls=[
                                ft.Text(p.nombre, size=13, weight=ft.FontWeight.BOLD),
                                ft.Text(f"{p.stock_actual} {p.unidad} | Min: {p.stock_minimo}",
                                        size=11, color=Colores.ROJO),
                            ]),
                            ft.Row(spacing=8, controls=[
                                Badge.estado_stock(p.calcular_estado()),
                                ft.Text(f"${p.valor_total():,.0f}", size=11, color=Colores.GRIS),
                            ])
                        ]
                    )
                ))
        else:
            items_criticos.append(
                ft.Text("No hay productos criticos", color=Colores.VERDE, size=13)
            )

        # Top consumo simple
        maximo_consumo = max((d['total'] for d in top_consumo), default=1)
        top_controls = []
        for d in top_consumo:
            top_controls.append(
                GraficaBarras.barra_horizontal(
                    f"{d['nombre']} ({d['unidad']})",
                    d['total'], maximo_consumo,
                    Colores.AZUL_PRIMARIO, ancho_total=400
                )
            )

        grafica_top = ft.Container(
            padding=16, border_radius=12, bgcolor=Colores.BLANCO,
            shadow=ft.BoxShadow(blur_radius=10, color="rgba(0,0,0,0.08)"),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text("Top 5 Productos mas Consumidos", size=15,
                            weight=ft.FontWeight.BOLD, color=Colores.NEGRO),
                    ft.Text("Unidades de salida totales", size=12, color=Colores.GRIS),
                    ft.Divider(color=Colores.GRIS_CLARO),
                ] + (top_controls if top_controls else [
                    ft.Text("Registra movimientos para ver estadisticas", color=Colores.GRIS, size=13)
                ])
            )
        )

        return ft.Column(
            spacing=20, scroll=ft.ScrollMode.AUTO,
            controls=[
                Tipografia.titulo_seccion("Resumen General"),
                Tipografia.subtitulo("Estado actual del inventario"),
                ft.Divider(color=Colores.AZUL_CLARO),
                metricas,
                ft.Divider(color=Colores.AZUL_CLARO),
                ft.Row(
                    wrap=True, spacing=20, alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Column(spacing=10, width=500, controls=[
                            ft.Text("Alertas de Stock Critico", size=15,
                                    weight=ft.FontWeight.BOLD, color=Colores.NEGRO),
                        ] + items_criticos),
                        ft.Column(spacing=10, controls=[
                            grafica_top,
                            GraficaBarras.grafica_actividad_reciente(actividad),
                            GraficaBarras.grafica_categorias(consumo_cat),
                        ]),
                    ]
                )
            ]
        )

    # ── PRODUCTOS ──

    def _tab_productos(self) -> ft.Column:
        # Formulario nuevo producto
        tf_codigo    = CampoTexto.crear("Codigo", width=220)
        tf_nombre    = CampoTexto.crear("Nombre del Producto", width=280)
        dd_categoria = ft.Dropdown(
            label="Categoria", width=220, border_radius=10,
            options=[ft.dropdown.Option(c.value) for c in Categoria]
        )
        tf_stock_ini = CampoTexto.crear("Stock Inicial", width=160)
        tf_stock_min = CampoTexto.crear("Stock Minimo", width=160)
        tf_stock_max = CampoTexto.crear("Stock Maximo", width=160)
        tf_precio    = CampoTexto.crear("Precio Unitario", width=160)
        tf_unidad    = CampoTexto.crear("Unidad (kg, bote...)", width=200)
        msg_prod     = ft.Text("", size=13)

        lista_ref = ft.Ref[ft.Column]()

        def refrescar():
            productos = self.svc.obtener_todos_productos()
            filas = []
            for p in productos:
                filas.append(ft.Container(
                    padding=12, border_radius=10, bgcolor=Colores.BLANCO,
                    shadow=ft.BoxShadow(blur_radius=8, color="rgba(0,0,0,0.07)"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(spacing=3, controls=[
                                ft.Row(spacing=8, controls=[
                                    ft.Text(p.nombre, size=13, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"[{p.codigo}]", size=11, color=Colores.GRIS),
                                ]),
                                ft.Text(f"{p.categoria} | {p.stock_actual} {p.unidad} | ${p.precio}",
                                        size=11, color=Colores.GRIS),
                            ]),
                            ft.Row(spacing=8, controls=[
                                Badge.estado_stock(p.calcular_estado()),
                                ft.Text(f"${p.valor_total():,.0f}", size=12,
                                        color=Colores.AZUL_PRIMARIO, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    ft.Icons.DELETE, icon_color=Colores.ROJO,
                                    tooltip="Eliminar",
                                    on_click=lambda e, pid=p.id: eliminar(pid)
                                ),
                            ])
                        ]
                    )
                ))
            lista_ref.current.controls = filas
            self.page.update()

        def crear(e):
            try:
                ok, msg = self.svc.crear_producto(
                    nombre=tf_nombre.value, codigo=tf_codigo.value,
                    categoria=dd_categoria.value or "Otro",
                    stock_actual=int(tf_stock_ini.value or 0),
                    stock_minimo=int(tf_stock_min.value or 5),
                    stock_maximo=int(tf_stock_max.value or 100),
                    precio=float(tf_precio.value or 0),
                    unidad=tf_unidad.value or "unidad",
                )
                msg_prod.value = msg
                msg_prod.color = Colores.VERDE if ok else Colores.ROJO
                if ok:
                    for f in [tf_codigo, tf_nombre, tf_stock_ini, tf_stock_min,
                               tf_stock_max, tf_precio, tf_unidad]:
                        f.value = ""
                    dd_categoria.value = None
                    refrescar()
            except Exception as ex:
                msg_prod.value = f"Error: {ex}"
                msg_prod.color = Colores.ROJO
            self.page.update()

        def eliminar(pid):
            self.svc.eliminar_producto(pid)
            Notificacion.mostrar(self.page, "Producto eliminado")
            refrescar()

        lista_productos = ft.Column(ref=lista_ref, spacing=10)
        refrescar()

        return ft.Column(
            spacing=16, scroll=ft.ScrollMode.AUTO,
            controls=[
                Tipografia.titulo_seccion("Gestion de Productos"),
                ft.Divider(color=Colores.AZUL_CLARO),
                Tipografia.subtitulo("Agregar nuevo producto"),
                ft.Row(wrap=True, spacing=10, controls=[tf_codigo, tf_nombre, dd_categoria]),
                ft.Row(wrap=True, spacing=10, controls=[
                    tf_stock_ini, tf_stock_min, tf_stock_max, tf_precio, tf_unidad
                ]),
                msg_prod,
                Boton.primario("Agregar Producto", crear, ancho=280),
                ft.Divider(color=Colores.AZUL_CLARO),
                Tipografia.subtitulo("Productos registrados"),
                lista_productos,
            ]
        )

    # ── MOVIMIENTOS ──

    def _tab_movimientos(self) -> ft.Column:
        movimientos = self.svc.obtener_movimientos(150)

        lista_ref = ft.Ref[ft.Column]()

        def refrescar():
            movs = self.svc.obtener_movimientos(150)
            filas = [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(m['fecha'][:16], size=11, color=Colores.GRIS)),
                    ft.DataCell(ft.Text(m['producto_nombre'], size=12)),
                    ft.DataCell(ft.Container(
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=12,
                        bgcolor=Colores.VERDE_CLARO if m['tipo'] == 'Entrada' else Colores.ROJO_CLARO,
                        content=ft.Text(
                            m['tipo'], size=11, weight=ft.FontWeight.BOLD,
                            color=Colores.VERDE if m['tipo'] == 'Entrada' else Colores.ROJO
                        )
                    )),
                    ft.DataCell(ft.Text(str(m['cantidad']), size=12,
                                        weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(m['usuario_nombre'], size=12)),
                    ft.DataCell(ft.Text(m['notas'] or "-", size=11, color=Colores.GRIS)),
                    ft.DataCell(ft.IconButton(
                        ft.Icons.UNDO, icon_color=Colores.AMARILLO,
                        tooltip="Revertir movimiento",
                        on_click=lambda e, mid=m['id']: revertir(mid)
                    )),
                ])
                for m in movs
            ]
            lista_ref.current.controls = [
                ft.DataTable(
                    border=ft.border.all(1, Colores.AZUL_CLARO),
                    border_radius=10,
                    heading_row_color=Colores.AZUL_CLARO,
                    columns=[
                        ft.DataColumn(ft.Text("Fecha", weight=ft.FontWeight.BOLD, size=12)),
                        ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD, size=12)),
                        ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD, size=12)),
                        ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD, size=12)),
                        ft.DataColumn(ft.Text("Usuario", weight=ft.FontWeight.BOLD, size=12)),
                        ft.DataColumn(ft.Text("Notas", weight=ft.FontWeight.BOLD, size=12)),
                        ft.DataColumn(ft.Text("Accion", weight=ft.FontWeight.BOLD, size=12)),
                    ],
                    rows=filas
                )
            ] if filas else [ft.Text("Sin movimientos registrados", color=Colores.GRIS)]
            self.page.update()

        def revertir(mid):
            ok, msg = self.svc.eliminar_movimiento(mid)
            Notificacion.mostrar(self.page, msg, es_error=not ok)
            refrescar()

        contenedor_tabla = ft.Column(ref=lista_ref, spacing=0)
        refrescar()

        return ft.Column(
            spacing=16, scroll=ft.ScrollMode.AUTO,
            controls=[
                Tipografia.titulo_seccion("Historial de Movimientos"),
                Tipografia.subtitulo("Ultimas 150 operaciones. Puedes revertir cualquiera."),
                ft.Divider(color=Colores.AZUL_CLARO),
                contenedor_tabla,
            ]
        )

    # ── PREDICCION ──

    def _tab_prediccion(self) -> ft.Column:
        """
        Prediccion de demanda por producto:
        consumo diario, dias restantes, urgencia, recomendacion de compra y punto de reorden
        """
        predicciones = self.svc_pred.predecir_todos()

        if not predicciones:
            return ft.Column(controls=[
                Tipografia.titulo_seccion("Prediccion de Consumo"),
                ft.Text("Registra movimientos para activar las predicciones", color=Colores.GRIS, size=13),
            ])

        # Resumen de urgencias
        urgentes = sum(1 for p in predicciones if p['urgencia'] == 'Urgente')
        prontos  = sum(1 for p in predicciones if p['urgencia'] == 'Pronto')
        normales = sum(1 for p in predicciones if p['urgencia'] == 'Normal')

        resumen_urgencias = ft.Row(
            spacing=12,
            controls=[
                TarjetaMetrica.crear("Urgentes", str(urgentes), ft.Icons.ERROR, Colores.ROJO),
                TarjetaMetrica.crear("Reorden pronto", str(prontos), ft.Icons.WARNING, Colores.AMARILLO),
                TarjetaMetrica.crear("Stock normal", str(normales), ft.Icons.CHECK_CIRCLE, Colores.VERDE),
            ]
        )

        # Tarjetas de prediccion por producto
        tarjetas = []
        for p in predicciones:
            punto_reorden = self.svc_pred.calcular_punto_reorden(p['producto_id'])

            # Color del borde segun urgencia
            color_borde = {
                "Urgente": Colores.ROJO,
                "Pronto":  Colores.AMARILLO,
                "Normal":  Colores.VERDE,
            }.get(p['urgencia'], Colores.GRIS)

            tarjetas.append(ft.Container(
                padding=16, border_radius=12, bgcolor=Colores.BLANCO,
                border=ft.border.all(2, color_borde),
                shadow=ft.BoxShadow(blur_radius=8, color="rgba(0,0,0,0.06)"),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(spacing=2, controls=[
                                    ft.Text(p['producto'], size=15,
                                            weight=ft.FontWeight.BOLD, color=Colores.NEGRO),
                                    ft.Text(f"{p['categoria']} | [{p['codigo']}]",
                                            size=11, color=Colores.GRIS),
                                ]),
                                Badge.urgencia(p['urgencia']),
                            ]
                        ),

                        # Barra de stock visual
                        ft.Stack(controls=[
                            ft.Container(width=500, height=10, border_radius=5,
                                         bgcolor=Colores.GRIS_CLARO),
                            ft.Container(
                                width=max(4, int(p['porcentaje_stock'] / 100 * 500)),
                                height=10, border_radius=5, bgcolor=color_borde
                            ),
                        ]),
                        ft.Text(f"Stock: {p['stock_actual']} {p['unidad']} ({p['porcentaje_stock']:.0f}% del maximo)",
                                size=11, color=Colores.GRIS),

                        # Metricas en fila
                        ft.Row(
                            spacing=20,
                            controls=[
                                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                                    ft.Text(str(p['consumo_diario']), size=20,
                                            weight=ft.FontWeight.BOLD, color=Colores.AZUL_PRIMARIO),
                                    ft.Text("Consumo/dia", size=10, color=Colores.GRIS),
                                ]),
                                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                                    ft.Text(str(p['consumo_mensual']), size=20,
                                            weight=ft.FontWeight.BOLD, color=Colores.AMARILLO),
                                    ft.Text("Consumo/mes", size=10, color=Colores.GRIS),
                                ]),
                                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                                    ft.Text(
                                        f"{p['dias_restantes']}d" if p['dias_restantes'] < 999 else "Indefinido",
                                        size=20, weight=ft.FontWeight.BOLD, color=color_borde
                                    ),
                                    ft.Text("Dias restantes", size=10, color=Colores.GRIS),
                                ]),
                                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                                    ft.Text(str(punto_reorden), size=20,
                                            weight=ft.FontWeight.BOLD, color=Colores.MORADO),
                                    ft.Text("Punto reorden", size=10, color=Colores.GRIS),
                                ]),
                            ]
                        ),

                        # Recomendacion de compra
                        ft.Container(
                            padding=10, border_radius=8, bgcolor=Colores.AZUL_CLARO,
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        f"Recomendacion: pedir {p['cantidad_recomendada']} {p['unidad']}",
                                        size=12, color=Colores.AZUL_OSCURO,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        f"Costo estimado: ${p['costo_recomendado']:,.2f}",
                                        size=12, color=Colores.AZUL_OSCURO
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            ))

        return ft.Column(
            spacing=16, scroll=ft.ScrollMode.AUTO,
            controls=[
                Tipografia.titulo_seccion("Prediccion de Consumo"),
                Tipografia.subtitulo("Analisis basado en historial de movimientos"),
                ft.Divider(color=Colores.AZUL_CLARO),
                resumen_urgencias,
                ft.Divider(color=Colores.AZUL_CLARO),
            ] + tarjetas
        )

    # ── ANALISIS ABC ──

    def _tab_abc(self) -> ft.Column:
        """
        Clasificacion ABC (Pareto):
        A = 20% de productos con 80% del valor de movimiento
        B = siguiente 15%
        C = restante 5%
        """
        datos = self.svc_pred.analisis_abc()

        if not datos:
            return ft.Column(controls=[
                Tipografia.titulo_seccion("Analisis ABC"),
                ft.Text("Registra movimientos para activar el analisis", color=Colores.GRIS, size=13),
            ])

        # Conteo por clase
        conteo = {'A': 0, 'B': 0, 'C': 0}
        valor_clase = {'A': 0.0, 'B': 0.0, 'C': 0.0}
        for d in datos:
            conteo[d['clase']] += 1
            valor_clase[d['clase']] += d['valor_mensual']

        resumen_abc = ft.Row(
            spacing=12,
            controls=[
                TarjetaMetrica.crear(
                    f"Clase A ({conteo['A']} prod.)",
                    f"${valor_clase['A']:,.0f}/mes",
                    ft.Icons.STAR, Colores.ROJO
                ),
                TarjetaMetrica.crear(
                    f"Clase B ({conteo['B']} prod.)",
                    f"${valor_clase['B']:,.0f}/mes",
                    ft.Icons.STAR_HALF, Colores.AMARILLO
                ),
                TarjetaMetrica.crear(
                    f"Clase C ({conteo['C']} prod.)",
                    f"${valor_clase['C']:,.0f}/mes",
                    ft.Icons.STAR_BORDER, Colores.VERDE
                ),
            ]
        )

        # Tabla de productos con su clase
        filas_tabla = []
        for d in datos:
            filas_tabla.append(ft.DataRow(cells=[
                ft.DataCell(Badge.clase_abc(d['clase'])),
                ft.DataCell(ft.Text(d['producto'], size=12, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(f"{d['consumo_mensual']:.1f}", size=12)),
                ft.DataCell(ft.Text(f"${d['valor_mensual']:,.2f}", size=12,
                                    weight=ft.FontWeight.BOLD)),
            ]))

        tabla = ft.DataTable(
            border=ft.border.all(1, Colores.AZUL_CLARO),
            border_radius=10,
            heading_row_color=Colores.AZUL_CLARO,
            columns=[
                ft.DataColumn(ft.Text("Clase", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Consumo/mes", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Valor mensual", weight=ft.FontWeight.BOLD, size=12)),
            ],
            rows=filas_tabla
        )

        # Explicacion rapida
        explicacion = ft.Container(
            padding=16, border_radius=10, bgcolor=Colores.AZUL_CLARO,
            content=ft.Column(spacing=6, controls=[
                ft.Text("Que significa cada clase:", size=13,
                        weight=ft.FontWeight.BOLD, color=Colores.AZUL_OSCURO),
                ft.Text("A: Productos de alto valor. Monitoreo frecuente y control estricto.",
                        size=12, color=Colores.AZUL_OSCURO),
                ft.Text("B: Importancia media. Revision periodica.",
                        size=12, color=Colores.AZUL_OSCURO),
                ft.Text("C: Bajo valor de movimiento. Control simple.",
                        size=12, color=Colores.AZUL_OSCURO),
            ])
        )

        return ft.Column(
            spacing=16, scroll=ft.ScrollMode.AUTO,
            controls=[
                Tipografia.titulo_seccion("Analisis ABC"),
                Tipografia.subtitulo("Clasificacion por valor de movimiento mensual (Pareto 80/20)"),
                ft.Divider(color=Colores.AZUL_CLARO),
                resumen_abc,
                explicacion,
                ft.Divider(color=Colores.AZUL_CLARO),
                tabla,
            ]
        )

    # ── USUARIOS ──

    def _tab_usuarios(self) -> ft.Column:
        tf_nombre = CampoTexto.crear("Nombre Completo", width=280)
        tf_correo = CampoTexto.crear("Correo", width=280)
        tf_clave  = CampoTexto.crear("Contrasena", password=True, width=280)
        dd_rol    = ft.Dropdown(
            label="Rol", width=280, border_radius=10,
            options=[
                ft.dropdown.Option("empleado"),
                ft.dropdown.Option("administrador"),
            ]
        )
        msg_u = ft.Text("", size=13)
        lista_ref = ft.Ref[ft.Column]()

        def refrescar():
            usuarios = self.svc_usuarios.obtener_todos_usuarios()
            filas = []
            for u in usuarios:
                color_rol = Colores.ROJO_CLARO if u.es_admin() else Colores.AZUL_CLARO
                txt_rol = ft.Text(
                    u.rol.capitalize(), size=11,
                    color=Colores.ROJO if u.es_admin() else Colores.AZUL_PRIMARIO,
                    weight=ft.FontWeight.BOLD
                )
                filas.append(ft.Container(
                    padding=12, border_radius=10, bgcolor=Colores.BLANCO,
                    shadow=ft.BoxShadow(blur_radius=8, color="rgba(0,0,0,0.07)"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(spacing=3, controls=[
                                ft.Text(u.nombre, size=13, weight=ft.FontWeight.BOLD),
                                ft.Text(u.correo, size=11, color=Colores.GRIS),
                            ]),
                            ft.Row(spacing=8, controls=[
                                ft.Container(
                                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                    border_radius=20, bgcolor=color_rol,
                                    content=txt_rol
                                ),
                                ft.IconButton(
                                    ft.Icons.DELETE, icon_color=Colores.ROJO,
                                    tooltip="Eliminar",
                                    disabled=u.es_admin(),
                                    on_click=lambda e, uid=u.id: eliminar_u(uid)
                                ),
                            ])
                        ]
                    )
                ))
            lista_ref.current.controls = filas
            self.page.update()

        def crear_u(e):
            ok, msg = self.svc_usuarios.crear_usuario(
                tf_nombre.value, tf_correo.value,
                tf_clave.value, dd_rol.value or "empleado"
            )
            msg_u.value = msg
            msg_u.color = Colores.VERDE if ok else Colores.ROJO
            if ok:
                tf_nombre.value = tf_correo.value = tf_clave.value = ""
                dd_rol.value = None
                refrescar()
            self.page.update()

        def eliminar_u(uid):
            self.svc_usuarios.eliminar_usuario(uid)
            Notificacion.mostrar(self.page, "Usuario eliminado")
            refrescar()

        lista_usuarios = ft.Column(ref=lista_ref, spacing=10)
        refrescar()

        return ft.Column(
            spacing=16, scroll=ft.ScrollMode.AUTO,
            controls=[
                Tipografia.titulo_seccion("Gestion de Usuarios"),
                ft.Divider(color=Colores.AZUL_CLARO),
                Tipografia.subtitulo("Crear nuevo usuario"),
                ft.Row(wrap=True, spacing=10, controls=[tf_nombre, tf_correo]),
                ft.Row(wrap=True, spacing=10, controls=[tf_clave, dd_rol]),
                msg_u,
                Boton.primario("Crear Usuario", crear_u, ancho=280),
                ft.Divider(color=Colores.AZUL_CLARO),
                Tipografia.subtitulo("Usuarios registrados"),
                lista_usuarios,
            ]
        )
