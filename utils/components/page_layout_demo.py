"""
PageLayout Demo - Ejemplos de uso del sistema PageLayout
=========================================================

Este archivo contiene ejemplos completos de cómo usar el sistema PageLayout
en diferentes escenarios. Ejecuta con:

    streamlit run utils/components/page_layout_demo.py

Autor: Claude Code
Fecha: 2025-12-04
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.components.page_layout import (
    render_page_layout,
    render_dashboard_layout,
    render_form_layout,
    render_table_layout,
    render_detail_layout,
    page_header,
    page_breadcrumbs,
    page_section,
    page_divider,
    page_footer
)
from utils.components.metric_card import render_metric_row


# ============================================================================
# PÁGINA PRINCIPAL - SELECTOR DE EJEMPLOS
# ============================================================================

def main():
    st.set_page_config(
        page_title="PageLayout Demo",
        page_icon="📐",
        layout="wide"
    )

    st.sidebar.title("📐 PageLayout Demo")
    st.sidebar.markdown("---")

    ejemplo = st.sidebar.radio(
        "Selecciona un ejemplo:",
        [
            "1. Layouts Predefinidos",
            "2. Dashboard Layout",
            "3. Form Layout",
            "4. Table Layout",
            "5. Detail Layout",
            "6. Componentes Individuales",
            "7. Layout Personalizado"
        ]
    )

    # Renderizar el ejemplo seleccionado
    if ejemplo == "1. Layouts Predefinidos":
        ejemplo_layouts_predefinidos()
    elif ejemplo == "2. Dashboard Layout":
        ejemplo_dashboard_layout()
    elif ejemplo == "3. Form Layout":
        ejemplo_form_layout()
    elif ejemplo == "4. Table Layout":
        ejemplo_table_layout()
    elif ejemplo == "5. Detail Layout":
        ejemplo_detail_layout()
    elif ejemplo == "6. Componentes Individuales":
        ejemplo_componentes_individuales()
    elif ejemplo == "7. Layout Personalizado":
        ejemplo_layout_personalizado()


# ============================================================================
# EJEMPLO 1: OVERVIEW DE LAYOUTS PREDEFINIDOS
# ============================================================================

def ejemplo_layouts_predefinidos():
    """Muestra un overview de todos los layouts disponibles."""

    page_header(
        title="Layouts Predefinidos",
        description="Sistema completo de layouts para páginas consistentes",
        icon="📐"
    )

    st.markdown("""
    El sistema **PageLayout** proporciona 4 layouts predefinidos optimizados
    para casos de uso comunes en la aplicación:
    """)

    page_divider()

    # Layout 1: Dashboard
    with page_section(title="1. Dashboard Layout", icon="📊", collapsible=True, expanded=True):
        st.markdown("""
        **Uso:** Páginas con métricas y gráficas

        **Características:**
        - Header con título, descripción e icono
        - Selector de período opcional (mes/año)
        - Sidebar de filtros opcional
        - Container ancho (1600px)
        - Background con gradiente premium

        **Ejemplo de código:**
        ```python
        render_dashboard_layout(
            content_fn=mi_dashboard,
            title="Dashboard Financiero",
            description="Análisis de ingresos y gastos",
            show_period_selector=True,
            show_filters=True,
            filters_fn=mis_filtros
        )
        ```
        """)

        if st.button("Ver Ejemplo Dashboard", key="btn_dashboard"):
            st.info("Selecciona '2. Dashboard Layout' en el sidebar")

    page_divider()

    # Layout 2: Form
    with page_section(title="2. Form Layout", icon="📝", collapsible=True, expanded=True):
        st.markdown("""
        **Uso:** Páginas de formularios y entrada de datos

        **Características:**
        - Container estrecho (800px) para mejor legibilidad
        - Sidebar opcional con ayuda/instrucciones
        - Padding adicional para formularios
        - Optimizado para focus en el formulario

        **Ejemplo de código:**
        ```python
        render_form_layout(
            content_fn=mi_formulario,
            title="Nueva Transacción",
            description="Completa los campos",
            show_help_sidebar=True,
            help_content="### Ayuda\\nInstrucciones..."
        )
        ```
        """)

        if st.button("Ver Ejemplo Form", key="btn_form"):
            st.info("Selecciona '3. Form Layout' en el sidebar")

    page_divider()

    # Layout 3: Table
    with page_section(title="3. Table Layout", icon="📋", collapsible=True, expanded=True):
        st.markdown("""
        **Uso:** Páginas con tablas y listados de datos

        **Características:**
        - Container ancho (1400px) para tablas
        - Sidebar de filtros opcional
        - Botón de exportar en header
        - Optimizado para visualización de datos tabulares

        **Ejemplo de código:**
        ```python
        render_table_layout(
            content_fn=mi_tabla,
            title="Transacciones",
            description="Listado completo",
            filters_fn=mis_filtros,
            show_export_button=True
        )
        ```
        """)

        if st.button("Ver Ejemplo Table", key="btn_table"):
            st.info("Selecciona '4. Table Layout' en el sidebar")

    page_divider()

    # Layout 4: Detail
    with page_section(title="4. Detail Layout", icon="📄", collapsible=True, expanded=True):
        st.markdown("""
        **Uso:** Páginas de detalle de un ítem específico

        **Características:**
        - Container medio (1000px)
        - Botón "Volver" en header
        - Breadcrumbs para navegación
        - Acciones opcionales (editar, eliminar)
        - Optimizado para lectura de detalles

        **Ejemplo de código:**
        ```python
        render_detail_layout(
            content_fn=detalle_transaccion,
            title="Transacción #1234",
            subtitle="Compra en MERCADONA",
            breadcrumbs=[...],
            actions=[{"label": "Editar", "icon": "✏️"}]
        )
        ```
        """)

        if st.button("Ver Ejemplo Detail", key="btn_detail"):
            st.info("Selecciona '5. Detail Layout' en el sidebar")


# ============================================================================
# EJEMPLO 2: DASHBOARD LAYOUT
# ============================================================================

def ejemplo_dashboard_layout():
    """Ejemplo completo de dashboard layout."""

    def mi_dashboard():
        """Contenido del dashboard."""

        # Métricas principales
        with page_section(title="Resumen del Mes", icon="📊"):
            render_metric_row([
                {
                    "title": "Ingresos",
                    "value": 2500.00,
                    "delta": 8.5,
                    "icon": "💰",
                    "color": "success",
                    "trend": "up"
                },
                {
                    "title": "Gastos",
                    "value": 1800.50,
                    "delta": -5.2,
                    "icon": "💸",
                    "color": "danger",
                    "trend": "down"
                },
                {
                    "title": "Balance",
                    "value": 699.50,
                    "delta": 15.3,
                    "icon": "⚖️",
                    "color": "info",
                    "trend": "up"
                }
            ])

        page_divider()

        # Gráficos
        with page_section(title="Evolución Mensual", icon="📈"):
            # Crear gráfico de ejemplo
            df = pd.DataFrame({
                "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
                "Ingresos": [2400, 2500, 2600, 2450, 2550, 2500],
                "Gastos": [1900, 1850, 1800, 1950, 1750, 1800]
            })

            st.line_chart(df.set_index("Mes"))

        page_divider()

        # Tabla resumen
        with page_section(title="Categorías", icon="🏷️"):
            df_categorias = pd.DataFrame({
                "Categoría": ["FIJOS", "DISFRUTE", "EXTRAORDINARIOS"],
                "Total": [800.00, 600.50, 400.00],
                "% del Total": ["44%", "33%", "22%"]
            })

            st.dataframe(df_categorias, use_container_width=True, hide_index=True)

    def mis_filtros():
        """Sidebar de filtros."""
        st.markdown("### 🔍 Filtros")
        st.markdown("---")

        st.selectbox("Categoría", ["Todas", "FIJOS", "DISFRUTE", "EXTRAORDINARIOS"])
        st.date_input("Fecha desde")
        st.date_input("Fecha hasta")

        st.markdown("---")
        st.button("Aplicar Filtros", use_container_width=True)

    # Renderizar con dashboard layout
    render_dashboard_layout(
        content_fn=mi_dashboard,
        title="Dashboard Financiero",
        description="Resumen completo de tus finanzas personales",
        icon="📊",
        show_period_selector=True,
        show_filters=True,
        filters_fn=mis_filtros,
        breadcrumbs=[
            {"label": "Inicio", "url": "/"},
            {"label": "Dashboard", "url": None}
        ]
    )


# ============================================================================
# EJEMPLO 3: FORM LAYOUT
# ============================================================================

def ejemplo_form_layout():
    """Ejemplo completo de form layout."""

    def mi_formulario():
        """Contenido del formulario."""

        with st.form("nueva_transaccion"):
            st.markdown("### Información Básica")

            col1, col2 = st.columns(2)

            with col1:
                fecha = st.date_input(
                    "Fecha",
                    value=datetime.now(),
                    help="Fecha de la transacción"
                )

            with col2:
                importe = st.number_input(
                    "Importe (€)",
                    min_value=0.0,
                    step=0.01,
                    help="Importe de la transacción"
                )

            concepto = st.text_input(
                "Concepto",
                placeholder="Ej: Compra en supermercado",
                help="Descripción de la transacción"
            )

            page_divider()

            st.markdown("### Clasificación")

            col1, col2 = st.columns(2)

            with col1:
                categoria = st.selectbox(
                    "Categoría",
                    ["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "INGRESO"]
                )

            with col2:
                tipo = st.selectbox(
                    "Tipo",
                    ["GASTO", "INGRESO"]
                )

            notas = st.text_area(
                "Notas (opcional)",
                placeholder="Información adicional...",
                help="Notas adicionales sobre la transacción"
            )

            page_divider()

            # Botones
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                submitted = st.form_submit_button(
                    "💾 Guardar",
                    use_container_width=True
                )

            with col2:
                st.form_submit_button(
                    "🔄 Limpiar",
                    use_container_width=True
                )

            with col3:
                st.form_submit_button(
                    "❌ Cancelar",
                    use_container_width=True
                )

            if submitted:
                st.success("✅ Transacción guardada correctamente")

    help_content = """
### 💡 Ayuda

**Categorías:**
- **FIJOS:** Gastos recurrentes mensuales (alquiler, gimnasio, suscripciones)
- **DISFRUTE:** Gastos variables de ocio (restaurantes, compras, etc.)
- **EXTRAORDINARIOS:** Gastos puntuales grandes (viajes, reparaciones, etc.)

**Consejos:**
- Usa un concepto descriptivo para identificar fácilmente la transacción
- Los importes se ingresan siempre en positivo
- El tipo (GASTO/INGRESO) determina si suma o resta del balance

**Clasificación automática:**
El sistema puede clasificar automáticamente transacciones basándose en reglas.
Puedes revisar y ajustar la clasificación antes de guardar.
"""

    # Renderizar con form layout
    render_form_layout(
        content_fn=mi_formulario,
        title="Nueva Transacción",
        description="Completa los campos para agregar una nueva transacción",
        icon="📝",
        show_help_sidebar=True,
        help_content=help_content,
        breadcrumbs=[
            {"label": "Transacciones", "url": "/transacciones"},
            {"label": "Nueva", "url": None}
        ]
    )


# ============================================================================
# EJEMPLO 4: TABLE LAYOUT
# ============================================================================

def ejemplo_table_layout():
    """Ejemplo completo de table layout."""

    def mi_tabla():
        """Contenido de la tabla."""

        # Crear datos de ejemplo
        df = pd.DataFrame({
            "Fecha": pd.date_range(start="2025-01-01", periods=20, freq="D"),
            "Concepto": [
                "Compra MERCADONA", "Gasolina REPSOL", "Netflix", "Restaurante",
                "Gimnasio", "Farmacia", "Amazon", "Bar", "Supermercado",
                "Parking", "Kebab", "Ropa", "Cine", "Peluquería",
                "Cafetería", "Tabaco", "Compra online", "Gasolina",
                "Supermercado", "Bar"
            ],
            "Categoría": [
                "DISFRUTE", "DISFRUTE", "FIJOS", "DISFRUTE", "FIJOS",
                "EXTRAORDINARIOS", "DISFRUTE", "DISFRUTE", "DISFRUTE",
                "DISFRUTE", "DISFRUTE", "DISFRUTE", "DISFRUTE", "DISFRUTE",
                "DISFRUTE", "DISFRUTE", "DISFRUTE", "DISFRUTE", "DISFRUTE",
                "DISFRUTE"
            ],
            "Importe": [
                -45.50, -55.00, -9.99, -38.50, -40.00,
                -15.50, -29.99, -12.00, -52.30, -2.50,
                -8.50, -45.00, -15.00, -25.00, -3.50,
                -6.50, -32.00, -60.00, -48.20, -10.00
            ]
        })

        # Formatear para mostrar
        df["Fecha"] = df["Fecha"].dt.strftime("%d/%m/%Y")
        df["Importe"] = df["Importe"].apply(lambda x: f"{x:.2f} €")

        # Estadísticas
        with page_section(title="Resumen", icon="📊"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Transacciones", "20")

            with col2:
                st.metric("Gasto Total", "-614.48 €")

            with col3:
                st.metric("Promedio por Transacción", "-30.72 €")

        page_divider()

        # Tabla
        with page_section(title="Listado de Transacciones", icon="📋"):
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                height=500
            )

    def mis_filtros():
        """Sidebar de filtros."""
        st.markdown("### 🔍 Filtros")
        st.markdown("---")

        st.selectbox("Categoría", ["Todas", "FIJOS", "DISFRUTE", "EXTRAORDINARIOS"])

        st.markdown("---")

        st.date_input("Desde")
        st.date_input("Hasta")

        st.markdown("---")

        st.number_input("Importe mínimo (€)", min_value=0.0, step=1.0)
        st.number_input("Importe máximo (€)", min_value=0.0, step=1.0)

        st.markdown("---")

        st.text_input("Buscar en concepto", placeholder="Ej: mercadona")

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.button("Aplicar", use_container_width=True)
        with col2:
            st.button("Limpiar", use_container_width=True)

    # Renderizar con table layout
    render_table_layout(
        content_fn=mi_tabla,
        title="Transacciones",
        description="Listado completo de todas tus transacciones",
        icon="💸",
        show_filters=True,
        filters_fn=mis_filtros,
        show_export_button=True,
        breadcrumbs=[
            {"label": "Inicio", "url": "/"},
            {"label": "Transacciones", "url": None}
        ]
    )


# ============================================================================
# EJEMPLO 5: DETAIL LAYOUT
# ============================================================================

def ejemplo_detail_layout():
    """Ejemplo completo de detail layout."""

    def detalle_transaccion():
        """Contenido del detalle."""

        # Información principal
        with page_section(title="Información Básica", icon="📝"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Fecha:**")
                st.markdown("15/01/2025")
                st.markdown("")

                st.markdown("**Concepto:**")
                st.markdown("Compra en MERCADONA")
                st.markdown("")

                st.markdown("**Categoría:**")
                st.markdown("🏷️ DISFRUTE")

            with col2:
                st.markdown("**Importe:**")
                st.markdown("-45.50 €")
                st.markdown("")

                st.markdown("**Tipo:**")
                st.markdown("GASTO")
                st.markdown("")

                st.markdown("**Saldo Posterior:**")
                st.markdown("1.254,50 €")

        page_divider()

        # Notas
        with page_section(title="Notas", icon="📌", collapsible=True):
            st.markdown("""
            Compra semanal de supermercado. Incluye:
            - Productos frescos
            - Productos básicos
            - Productos de limpieza
            """)

        page_divider()

        # Histórico
        with page_section(title="Histórico de Cambios", icon="🕒", collapsible=True):
            st.markdown("""
            | Fecha | Usuario | Acción | Detalles |
            |-------|---------|--------|----------|
            | 15/01/2025 10:30 | Sistema | Creación | Transacción creada |
            | 15/01/2025 10:35 | Usuario | Edición | Categoría cambiada |
            """)

    def editar_transaccion():
        st.info("Funcionalidad de edición próximamente...")

    def eliminar_transaccion():
        st.warning("¿Estás seguro de eliminar esta transacción?")

    # Renderizar con detail layout
    render_detail_layout(
        content_fn=detalle_transaccion,
        title="Transacción #1234",
        subtitle="Compra en MERCADONA - 45.50€",
        icon="📄",
        show_back_button=True,
        breadcrumbs=[
            {"label": "Inicio", "url": "/"},
            {"label": "Transacciones", "url": "/transacciones"},
            {"label": "#1234", "url": None}
        ],
        actions=[
            {"label": "Editar", "icon": "✏️", "callback": editar_transaccion},
            {"label": "Eliminar", "icon": "🗑️", "callback": eliminar_transaccion}
        ]
    )


# ============================================================================
# EJEMPLO 6: COMPONENTES INDIVIDUALES
# ============================================================================

def ejemplo_componentes_individuales():
    """Ejemplos de componentes individuales del sistema."""

    page_header(
        title="Componentes Individuales",
        description="Helpers y utilidades del sistema PageLayout",
        icon="🧩"
    )

    # Breadcrumbs
    with page_section(title="1. Breadcrumbs", icon="🔗", collapsible=True, expanded=True):
        st.markdown("**Código:**")
        st.code("""
page_breadcrumbs([
    {"label": "Inicio", "url": "/"},
    {"label": "Transacciones", "url": "/transacciones"},
    {"label": "Detalle", "url": None}
])
        """)

        st.markdown("**Resultado:**")
        page_breadcrumbs([
            {"label": "Inicio", "url": "/"},
            {"label": "Transacciones", "url": "/transacciones"},
            {"label": "Detalle", "url": None}
        ])

    page_divider()

    # Secciones
    with page_section(title="2. Page Section", icon="📦", collapsible=True, expanded=True):
        st.markdown("**Código:**")
        st.code("""
with page_section(title="Mi Sección", icon="⭐", description="Descripción"):
    st.write("Contenido de la sección")
        """)

        st.markdown("**Resultado:**")
        with page_section(title="Mi Sección", icon="⭐", description="Esta es una sección de ejemplo"):
            st.write("Contenido de la sección con spacing consistente")

    page_divider()

    # Divisores
    with page_section(title="3. Page Divider", icon="➖", collapsible=True, expanded=True):
        st.markdown("**Código:**")
        st.code("""
page_divider()  # Sólido por defecto
page_divider(style="dashed")
page_divider(style="dotted")
        """)

        st.markdown("**Resultado:**")
        st.write("Línea sólida:")
        page_divider()

        st.write("Línea discontinua:")
        page_divider(style="dashed")

        st.write("Línea punteada:")
        page_divider(style="dotted")

    page_divider()

    # Footer
    with page_section(title="4. Page Footer", icon="👣", collapsible=True, expanded=True):
        st.markdown("**Código:**")
        st.code("""
page_footer(
    content="Mi App Finanzas",
    links=[
        {"label": "Ayuda", "url": "/help"},
        {"label": "Privacidad", "url": "/privacy"}
    ],
    copyright="© 2025"
)
        """)

        st.markdown("**Resultado:**")
        page_footer(
            content="Mi App Finanzas - Gestiona tus finanzas personales",
            links=[
                {"label": "Ayuda", "url": "/help"},
                {"label": "Privacidad", "url": "/privacy"},
                {"label": "Términos", "url": "/terms"}
            ],
            copyright="© 2025 Mi App Finanzas"
        )


# ============================================================================
# EJEMPLO 7: LAYOUT PERSONALIZADO
# ============================================================================

def ejemplo_layout_personalizado():
    """Ejemplo de layout completamente personalizado usando render_page_layout."""

    def mi_contenido_custom():
        """Contenido personalizado."""

        # Sección 1
        with page_section(title="Welcome Section", icon="👋", background=Colors.PREMIUM_CARD_GRADIENT):
            st.markdown("""
            Este es un ejemplo de layout completamente personalizado usando la función
            `render_page_layout()` con configuraciones avanzadas.
            """)

        page_divider()

        # Sección 2
        col1, col2 = st.columns(2)

        with col1:
            with page_section(title="Feature 1", icon="⚡"):
                st.markdown("Descripción de la característica 1")

        with col2:
            with page_section(title="Feature 2", icon="🚀"):
                st.markdown("Descripción de la característica 2")

        page_divider()

        # Sección 3
        with page_section(title="Call to Action", icon="🎯"):
            st.button("Comenzar Ahora", use_container_width=True)

    def mi_sidebar_custom():
        """Sidebar personalizado."""
        st.markdown("### 🎨 Personalización")
        st.markdown("---")

        st.color_picker("Color principal")
        st.slider("Tamaño de fuente", 12, 24, 16)
        st.checkbox("Modo oscuro")

    from utils.design_tokens import Colors

    # Renderizar con configuración personalizada
    render_page_layout(
        content_fn=mi_contenido_custom,
        header={
            "title": "Layout Personalizado",
            "description": "Ejemplo de layout con configuración avanzada",
            "icon": "🎨",
            "breadcrumbs": [
                {"label": "Demo", "url": "/"},
                {"label": "Custom", "url": None}
            ]
        },
        sidebar={
            "content_fn": mi_sidebar_custom,
            "width": "300px",
            "position": "right"
        },
        footer={
            "content": "Layout creado con render_page_layout()",
            "copyright": "© 2025 PageLayout Demo"
        },
        max_width="1200px",
        background=Colors.PREMIUM_BG_GRADIENT
    )


# ============================================================================
# EJECUTAR DEMO
# ============================================================================

if __name__ == "__main__":
    main()
