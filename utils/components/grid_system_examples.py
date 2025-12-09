"""
Grid System Examples - Ejemplos interactivos del sistema de grillas

Ejecutar con: streamlit run utils/components/grid_system_examples.py

Este archivo contiene ejemplos prácticos y casos de uso reales del Grid System.
Perfecto para entender cómo usar cada función y ver el resultado en vivo.

Autor: Claude Code
Fecha: 2025-12-04
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Imports del proyecto
from utils.components.grid_system import (
    render_grid,
    render_card_grid,
    render_metric_grid,
    render_image_grid,
    render_masonry_grid,
    auto_grid,
    grid_item,
    responsive_columns
)
from utils.design_tokens import Colors, Spacing


# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Grid System - Ejemplos Interactivos",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# FUNCIONES HELPER PARA EJEMPLOS
# ============================================================================

def generate_sample_data():
    """Genera datos de ejemplo para los grids"""
    return {
        "metrics": [
            {"label": "Ingresos Totales", "value": "2,500€", "delta": "+15%", "help": "Ingresos del mes actual"},
            {"label": "Gastos Totales", "value": "1,800€", "delta": "-5%", "delta_color": "inverse", "help": "Gastos del mes actual"},
            {"label": "Balance Neto", "value": "700€", "delta": "+10%", "help": "Diferencia entre ingresos y gastos"},
            {"label": "Tasa de Ahorro", "value": "28%", "delta": "+3%", "help": "Porcentaje de ingresos ahorrados"},
        ],
        "cards": [
            {
                "title": "FIJOS",
                "content": "850€",
                "footer": "35% del total gastado",
                "color": Colors.PRIMARY
            },
            {
                "title": "DISFRUTE",
                "content": "720€",
                "footer": "30% del total gastado",
                "color": Colors.SUCCESS
            },
            {
                "title": "EXTRAORDINARIOS",
                "content": "230€",
                "footer": "10% del total gastado",
                "color": Colors.WARNING
            },
            {
                "title": "AHORRADO",
                "content": "700€",
                "footer": "28% de los ingresos",
                "color": Colors.ACCENT_TEAL
            }
        ],
        "posts": [
            "Resumen mensual de octubre: Este mes hemos conseguido ahorrar un 28% de nuestros ingresos.",
            "Tips de ahorro: Reducir gastos variables en un 10% puede suponer 200€ extra al mes para ahorro.",
            "Análisis de gastos fijos: Los gastos fijos representan el 35% del total, dentro del rango saludable.",
            "Planificación financiera: Establecer objetivos de ahorro claros mejora la disciplina financiera en un 40%.",
            "Inversión inteligente: Diversificar el ahorro entre diferentes productos financieros reduce el riesgo.",
            "Presupuesto 2025: Planificar con antelación permite identificar oportunidades de ahorro.",
        ]
    }


def create_sample_chart():
    """Crea un gráfico de ejemplo para demostrar integración"""
    months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
    ingresos = [2300, 2400, 2500, 2450, 2600, 2500]
    gastos = [1900, 1850, 1800, 1950, 1750, 1800]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Ingresos',
        x=months,
        y=ingresos,
        marker_color=Colors.SUCCESS
    ))
    fig.add_trace(go.Bar(
        name='Gastos',
        x=months,
        y=gastos,
        marker_color=Colors.ERROR
    ))

    fig.update_layout(
        barmode='group',
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )

    return fig


# ============================================================================
# EJEMPLOS INDIVIDUALES
# ============================================================================

def example_1_basic_grid():
    """Ejemplo 1: Grid básico de 3 columnas"""
    st.header("1. Grid Básico")
    st.markdown("Grid simple con número fijo de columnas.")

    with st.expander("Ver código", expanded=False):
        st.code("""
from utils.components.grid_system import render_grid

items = [
    "Card 1",
    "Card 2",
    "Card 3",
    "Card 4",
    "Card 5",
    "Card 6"
]

render_grid(items, cols=3, gap='lg', responsive=True)
        """, language="python")

    # Configuración interactiva
    col1, col2, col3 = st.columns(3)
    with col1:
        cols = st.slider("Columnas", 1, 6, 3, key="ex1_cols")
    with col2:
        gap = st.selectbox("Gap", ['xs', 'sm', 'md', 'lg', 'xl'], index=2, key="ex1_gap")
    with col3:
        responsive = st.checkbox("Responsive", value=True, key="ex1_resp")

    # Render
    items = [f"Card {i+1}" for i in range(12)]
    render_grid(items, cols=cols, gap=gap, responsive=responsive)


def example_2_card_grid():
    """Ejemplo 2: Grid de cards con estilo"""
    st.header("2. Card Grid")
    st.markdown("Grid especializado para cards con título, contenido y footer.")

    with st.expander("Ver código", expanded=False):
        st.code("""
from utils.components.grid_system import render_card_grid
from utils.design_tokens import Colors

cards = [
    {
        "title": "FIJOS",
        "content": "850€",
        "footer": "35% del total",
        "color": Colors.PRIMARY
    },
    {
        "title": "DISFRUTE",
        "content": "720€",
        "footer": "30% del total",
        "color": Colors.SUCCESS
    },
    # ... más cards
]

render_card_grid(cards, cols=4, gap='lg')
        """, language="python")

    # Configuración
    col1, col2 = st.columns(2)
    with col1:
        cols = st.slider("Columnas", 1, 4, 4, key="ex2_cols")
    with col2:
        gap = st.selectbox("Gap", ['xs', 'sm', 'md', 'lg', 'xl'], index=3, key="ex2_gap")

    # Data
    data = generate_sample_data()

    # Render
    render_card_grid(data["cards"], cols=cols, gap=gap)


def example_3_metric_grid():
    """Ejemplo 3: Grid de métricas"""
    st.header("3. Metric Grid")
    st.markdown("Grid optimizado para métricas usando `st.metric()` nativo.")

    with st.expander("Ver código", expanded=False):
        st.code("""
from utils.components.grid_system import render_metric_grid

metrics = [
    {
        "label": "Ingresos Totales",
        "value": "2,500€",
        "delta": "+15%",
        "help": "Ingresos del mes"
    },
    {
        "label": "Gastos Totales",
        "value": "1,800€",
        "delta": "-5%",
        "delta_color": "inverse"
    },
    # ... más métricas
]

render_metric_grid(metrics, cols=4, gap='md')
        """, language="python")

    # Configuración
    cols = st.slider("Columnas", 1, 4, 4, key="ex3_cols")

    # Data
    data = generate_sample_data()

    # Render
    render_metric_grid(data["metrics"], cols=cols, gap='md')


def example_4_auto_grid():
    """Ejemplo 4: Auto Grid"""
    st.header("4. Auto Grid")
    st.markdown("Grid que ajusta automáticamente las columnas según ancho mínimo.")

    with st.expander("Ver código", expanded=False):
        st.code("""
from utils.components.grid_system import auto_grid

items = [f"Item {i+1}" for i in range(12)]

# Se ajusta automáticamente según espacio disponible
auto_grid(items, min_width='250px', gap='md')
        """, language="python")

    # Configuración
    col1, col2 = st.columns(2)
    with col1:
        min_width = st.slider("Ancho mínimo (px)", 150, 500, 250, step=50, key="ex4_width")
    with col2:
        gap = st.selectbox("Gap", ['xs', 'sm', 'md', 'lg', 'xl'], index=2, key="ex4_gap")

    # Data
    items = [f"Item {i+1}" for i in range(15)]

    # Render
    auto_grid(items, min_width=f'{min_width}px', gap=gap)


def example_5_masonry_grid():
    """Ejemplo 5: Masonry Grid"""
    st.header("5. Masonry Grid")
    st.markdown("Grid tipo Pinterest con alturas variables.")

    with st.expander("Ver código", expanded=False):
        st.code("""
from utils.components.grid_system import render_masonry_grid

posts = [
    "Post corto",
    "Post con mucho contenido...",
    "Post medio",
    # ... más posts
]

render_masonry_grid(posts, cols=3, gap='md')
        """, language="python")

    # Configuración
    col1, col2 = st.columns(2)
    with col1:
        cols = st.slider("Columnas", 1, 4, 3, key="ex5_cols")
    with col2:
        gap = st.selectbox("Gap", ['xs', 'sm', 'md', 'lg', 'xl'], index=2, key="ex5_gap")

    # Data
    data = generate_sample_data()

    # Render
    render_masonry_grid(data["posts"], cols=cols, gap=gap)


def example_6_custom_renderer():
    """Ejemplo 6: Renderer personalizado"""
    st.header("6. Custom Renderer")
    st.markdown("Usar una función personalizada para renderizar items.")

    with st.expander("Ver código", expanded=False):
        st.code("""
from utils.components.grid_system import render_grid
import plotly.graph_objects as go

def render_chart_item(data, idx):
    st.subheader(data["title"])
    fig = create_chart(data)
    st.plotly_chart(fig, use_container_width=True)

charts_data = [
    {"title": "Chart 1", "data": [...]},
    {"title": "Chart 2", "data": [...]},
]

render_grid(
    charts_data,
    cols=2,
    gap='xl',
    item_renderer=render_chart_item
)
        """, language="python")

    # Función renderer personalizada
    def render_chart(data, idx):
        st.markdown(f"### {data['title']}")
        fig = create_sample_chart()
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Gráfico {idx + 1}")

    # Data
    charts = [
        {"title": "Evolución Ingresos vs Gastos"},
        {"title": "Comparativa Mensual"},
    ]

    # Render
    render_grid(charts, cols=2, gap='xl', item_renderer=render_chart)


def example_7_responsive_config():
    """Ejemplo 7: Configuración responsive explícita"""
    st.header("7. Responsive Config")
    st.markdown("Control exacto de columnas por breakpoint.")

    with st.expander("Ver código", expanded=False):
        st.code("""
from utils.components.grid_system import responsive_columns

# 5 columnas desktop, 3 tablet, 1 mobile
css = responsive_columns(desktop=5, tablet=3, mobile=1, gap='lg')
st.markdown(css, unsafe_allow_html=True)

st.markdown('<div class="responsive-grid">', unsafe_allow_html=True)
for item in items:
    st.markdown(f'<div>{item}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
        """, language="python")

    # Configuración
    col1, col2, col3 = st.columns(3)
    with col1:
        desktop = st.slider("Desktop", 1, 6, 5, key="ex7_desktop")
    with col2:
        tablet = st.slider("Tablet", 1, 4, 3, key="ex7_tablet")
    with col3:
        mobile = st.slider("Mobile", 1, 2, 1, key="ex7_mobile")

    st.info(f"📱 Desktop: {desktop} cols | Tablet: {tablet} cols | Mobile: {mobile} col")

    # Data
    items = [f"Item {i+1}" for i in range(10)]

    # Render usando configuración responsive
    css = responsive_columns(desktop=desktop, tablet=tablet, mobile=mobile, gap='md')
    st.markdown(css, unsafe_allow_html=True)

    st.markdown('<div class="responsive-grid">', unsafe_allow_html=True)
    for item in items:
        st.markdown(f'''
        <div style="
            background: {Colors.BG_PRIMARY};
            border: 2px solid {Colors.GRAY_300};
            border-radius: 8px;
            padding: {Spacing.LG};
            text-align: center;
            font-weight: 600;
        ">{item}</div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================================
# CASOS DE USO REALES
# ============================================================================

def use_case_dashboard():
    """Caso de uso: Dashboard financiero"""
    st.header("🎯 Caso de Uso: Dashboard Financiero")
    st.markdown("Ejemplo completo de dashboard usando Grid System.")

    # Métricas principales
    st.subheader("Métricas Principales")
    data = generate_sample_data()
    render_metric_grid(data["metrics"], cols=4, gap='lg')

    st.markdown("---")

    # Categorías de gasto
    st.subheader("Distribución de Gastos")
    render_card_grid(data["cards"], cols=4, gap='md')

    st.markdown("---")

    # Gráficos
    st.subheader("Análisis Visual")

    def render_chart_section(chart_data, idx):
        st.markdown(f"### {chart_data['title']}")
        fig = create_sample_chart()
        st.plotly_chart(fig, use_container_width=True)

    charts = [
        {"title": "Evolución Mensual"},
        {"title": "Comparativa Anual"}
    ]

    render_grid(charts, cols=2, gap='xl', item_renderer=render_chart_section)


def use_case_gallery():
    """Caso de uso: Galería de categorías"""
    st.header("🎯 Caso de Uso: Galería de Categorías")
    st.markdown("Grid adaptativo para mostrar categorías de gastos.")

    categories = [
        {"title": "Supermercado", "count": 24, "total": "450€", "color": Colors.SUCCESS},
        {"title": "Gasolina", "count": 8, "total": "280€", "color": Colors.WARNING},
        {"title": "Restaurantes", "count": 12, "total": "320€", "color": Colors.PRIMARY},
        {"title": "Entretenimiento", "count": 6, "total": "180€", "color": Colors.ACCENT_CORAL},
        {"title": "Deportes", "count": 4, "total": "120€", "color": Colors.ACCENT_TEAL},
        {"title": "Otros", "count": 15, "total": "250€", "color": Colors.GRAY_500},
    ]

    def render_category(cat, idx):
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {cat['color']}15 0%, {cat['color']}05 100%);
            border: 2px solid {cat['color']};
            border-radius: 12px;
            padding: {Spacing.LG};
            text-align: center;
            transition: transform 0.2s;
        ">
            <h3 style="margin: 0; color: {Colors.GRAY_900};">{cat['title']}</h3>
            <p style="font-size: 2rem; font-weight: 700; margin: {Spacing.SM} 0; color: {cat['color']};">{cat['total']}</p>
            <p style="color: {Colors.GRAY_600}; margin: 0;">{cat['count']} transacciones</p>
        </div>
        """, unsafe_allow_html=True)

    auto_grid(categories, min_width='220px', gap='md', item_renderer=render_category)


def use_case_comparison():
    """Caso de uso: Comparación de periodos"""
    st.header("🎯 Caso de Uso: Comparación de Periodos")
    st.markdown("Grid de 2 columnas para comparar meses.")

    periods = [
        {
            "title": "Octubre 2024",
            "metrics": [
                {"label": "Ingresos", "value": "2,500€"},
                {"label": "Gastos", "value": "1,800€"},
                {"label": "Balance", "value": "700€"},
                {"label": "Ahorro", "value": "28%"}
            ]
        },
        {
            "title": "Septiembre 2024",
            "metrics": [
                {"label": "Ingresos", "value": "2,400€"},
                {"label": "Gastos", "value": "1,900€"},
                {"label": "Balance", "value": "500€"},
                {"label": "Ahorro", "value": "21%"}
            ]
        }
    ]

    def render_period(period, idx):
        st.subheader(period["title"])
        render_metric_grid(period["metrics"], cols=2, gap='sm', responsive=False)

    render_grid(periods, cols=2, gap='xl', item_renderer=render_period)


# ============================================================================
# SIDEBAR Y NAVEGACIÓN
# ============================================================================

def render_sidebar():
    """Renderiza el sidebar con navegación"""
    st.sidebar.title("📐 Grid System Examples")
    st.sidebar.markdown("---")

    st.sidebar.markdown("### 📚 Ejemplos Básicos")
    examples = {
        "1. Grid Básico": example_1_basic_grid,
        "2. Card Grid": example_2_card_grid,
        "3. Metric Grid": example_3_metric_grid,
        "4. Auto Grid": example_4_auto_grid,
        "5. Masonry Grid": example_5_masonry_grid,
        "6. Custom Renderer": example_6_custom_renderer,
        "7. Responsive Config": example_7_responsive_config,
    }

    st.sidebar.markdown("### 🎯 Casos de Uso")
    use_cases = {
        "Dashboard Financiero": use_case_dashboard,
        "Galería de Categorías": use_case_gallery,
        "Comparación de Periodos": use_case_comparison,
    }

    # Combinar todos los ejemplos
    all_examples = {**examples, **use_cases}

    # Selector
    selected = st.sidebar.radio(
        "Selecciona un ejemplo:",
        list(all_examples.keys()),
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📖 Documentación")
    st.sidebar.markdown("""
    - [README completo](README_GRID_SYSTEM.md)
    - [Design Tokens](../design_tokens.py)
    - [Código fuente](grid_system.py)
    """)

    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Tip:** Cambia el tamaño de la ventana del navegador para ver cómo responden los grids en diferentes tamaños de pantalla.
    """)

    return all_examples[selected]


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""

    # Header
    st.title("📐 Grid System - Ejemplos Interactivos")
    st.markdown("""
    Sistema de grillas responsive para crear layouts flexibles y profesionales.
    Explora los ejemplos y casos de uso para ver todas las posibilidades.
    """)
    st.markdown("---")

    # Render selected example
    selected_example = render_sidebar()
    selected_example()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>Desarrollado con ❤️ usando <strong>Streamlit</strong> y <strong>CSS Grid</strong></p>
        <p>Grid System v1.0.0 | 2025-12-04</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
