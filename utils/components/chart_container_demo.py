# utils/components/chart_container_demo.py
"""
Demo de uso del ChartContainer

Este archivo muestra ejemplos de uso del componente ChartContainer
con todas sus variantes y características.

Para ejecutar esta demo:
    streamlit run utils/components/chart_container_demo.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Importar componentes
from chart_container import (
    render_chart_container,
    render_chart_full,
    render_chart_half,
    render_chart_compact,
    add_chart_actions,
    show_chart_loading,
    show_chart_empty,
    create_chart_grid,
    render_chart_with_tabs,
    render_chart_preset,
    PRESET_CONFIGS
)

# Importar temas
from utils.plotly_theme import (
    create_themed_line_chart,
    create_themed_bar_chart,
    create_themed_pie_chart
)


# ========== DATOS DE EJEMPLO ==========

def generate_sample_data():
    """Genera datos de ejemplo para las demos."""

    # Datos temporales para líneas
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    df_temporal = pd.DataFrame({
        'fecha': dates,
        'saldo': (1000 + pd.np.cumsum(pd.np.random.randn(len(dates)) * 50)).round(2),
        'ingresos': pd.np.abs(pd.np.random.randn(len(dates)) * 200).round(2),
        'gastos': pd.np.abs(pd.np.random.randn(len(dates)) * 150).round(2)
    })

    # Datos categóricos para barras
    df_categorias = pd.DataFrame({
        'categoria': ['FIJOS', 'DISFRUTE', 'EXTRAORDINARIOS', 'AHORRO'],
        'importe': [1200, 800, 300, 500]
    })

    # Datos para pie chart
    df_distribucion = pd.DataFrame({
        'tipo': ['Alquiler', 'Comida', 'Transporte', 'Ocio', 'Otros'],
        'valor': [600, 350, 200, 150, 100]
    })

    return df_temporal, df_categorias, df_distribucion


# ========== PÁGINA PRINCIPAL ==========

def main():
    st.set_page_config(
        page_title="ChartContainer Demo",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 ChartContainer Component Demo")
    st.markdown("Ejemplos de uso del componente ChartContainer con todas sus variantes")

    # Generar datos
    df_temporal, df_categorias, df_distribucion = generate_sample_data()

    # Tabs principales
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Básico",
        "Variantes",
        "Estados",
        "Acciones",
        "Layouts",
        "Presets"
    ])

    # === TAB 1: USO BÁSICO ===
    with tab1:
        st.header("Uso Básico")

        st.subheader("1. Gráfica simple sin container")
        fig1 = create_themed_line_chart(
            df_temporal,
            x='fecha',
            y='saldo',
            title='Evolución del Saldo (Sin Container)'
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("---")

        st.subheader("2. Gráfica con ChartContainer básico")
        fig2 = create_themed_line_chart(
            df_temporal,
            x='fecha',
            y='saldo'
        )
        render_chart_container(
            fig2,
            title="Evolución del Saldo",
            description="Con ChartContainer - Estilos premium consistentes"
        )

        st.markdown("---")

        st.subheader("3. Container con título y descripción")
        fig3 = create_themed_bar_chart(
            df_categorias,
            x='categoria',
            y='importe'
        )
        render_chart_container(
            fig3,
            title="Gastos por Categoría",
            description="Distribución mensual de gastos según categoría"
        )

    # === TAB 2: VARIANTES ===
    with tab2:
        st.header("Variantes de Estilo")

        st.subheader("1. Variante Default")
        fig = create_themed_pie_chart(
            df_distribucion,
            names='tipo',
            values='valor'
        )
        render_chart_container(
            fig,
            title="Default Variant",
            description="Estilo por defecto con gradiente premium",
            variant="default"
        )

        st.markdown("---")

        st.subheader("2. Variante Premium")
        fig = create_themed_line_chart(
            df_temporal.tail(30),
            x='fecha',
            y='saldo'
        )
        render_chart_container(
            fig,
            title="Premium Variant",
            description="Mayor padding y sombras más pronunciadas",
            variant="premium"
        )

        st.markdown("---")

        st.subheader("3. Variante Minimal")
        fig = create_themed_bar_chart(
            df_categorias,
            x='categoria',
            y='importe'
        )
        render_chart_container(
            fig,
            title="Minimal Variant",
            description="Estilo minimalista sin efectos",
            variant="minimal"
        )

        st.markdown("---")

        st.subheader("4. Variante Glass (Glassmorphism)")
        fig = create_themed_line_chart(
            df_temporal.tail(60),
            x='fecha',
            y='ingresos'
        )
        render_chart_container(
            fig,
            title="Glass Variant",
            description="Efecto de cristal translúcido",
            variant="glass"
        )

    # === TAB 3: ESTADOS ===
    with tab3:
        st.header("Estados Especiales")

        st.subheader("1. Loading State")
        render_chart_container(
            loading=True,
            title="Cargando datos...",
            description="Skeleton loader mientras se cargan los datos"
        )

        st.markdown("---")

        st.subheader("2. Empty State")
        render_chart_container(
            empty_message="No hay transacciones este mes",
            title="Sin Datos",
            description="Estado cuando no hay datos para mostrar"
        )

        st.markdown("---")

        st.subheader("3. Error State")
        render_chart_container(
            error="Error al conectar con la base de datos: Connection timeout",
            title="Error de Conexión",
            description="Estado de error con detalles técnicos"
        )

        st.markdown("---")

        st.subheader("4. Simulador de Estados")
        estado = st.radio(
            "Selecciona un estado:",
            ["Normal", "Loading", "Empty", "Error"],
            horizontal=True
        )

        if estado == "Loading":
            render_chart_container(loading=True, title="Procesando...")
        elif estado == "Empty":
            render_chart_container(empty_message="No hay datos", title="Vacío")
        elif estado == "Error":
            render_chart_container(error="Error de prueba", title="Error")
        else:
            fig = create_themed_line_chart(df_temporal.tail(30), x='fecha', y='saldo')
            render_chart_container(fig, title="Gráfica Normal")

    # === TAB 4: ACCIONES ===
    with tab4:
        st.header("Acciones y Controles")

        st.subheader("1. Container con acciones básicas")
        fig = create_themed_bar_chart(df_categorias, x='categoria', y='importe')
        actions = add_chart_actions(export=True, filter=True, refresh=True)
        render_chart_container(
            fig,
            title="Gráfica con Acciones",
            description="Incluye filtros y botones de exportar/refrescar",
            actions=actions
        )

        st.markdown("---")

        st.subheader("2. Container con acciones personalizadas")
        custom_actions = [
            {
                "type": "selectbox",
                "label": "Vista",
                "key": "demo_vista",
                "options": ["Diaria", "Semanal", "Mensual"],
                "index": 2
            },
            {
                "type": "button",
                "label": "Compartir",
                "icon": "🔗",
                "key": "demo_share",
                "help": "Compartir gráfica"
            },
            {
                "type": "checkbox",
                "label": "Mostrar tendencia",
                "key": "demo_trend",
                "value": True
            }
        ]

        fig = create_themed_line_chart(df_temporal.tail(60), x='fecha', y='saldo')
        render_chart_container(
            fig,
            title="Acciones Personalizadas",
            actions=custom_actions
        )

    # === TAB 5: LAYOUTS ===
    with tab5:
        st.header("Layouts y Disposiciones")

        st.subheader("1. Full Width (render_chart_full)")
        fig = create_themed_line_chart(
            df_temporal,
            x='fecha',
            y='saldo'
        )
        render_chart_full(fig, title="Gráfica de Ancho Completo")

        st.markdown("---")

        st.subheader("2. Half Width (render_chart_half)")
        fig1 = create_themed_bar_chart(df_categorias, x='categoria', y='importe')
        fig2 = create_themed_pie_chart(df_distribucion, names='tipo', values='valor')

        render_chart_half([
            {"fig": fig1, "title": "Gastos por Categoría"},
            {"fig": fig2, "title": "Distribución Detallada"}
        ])

        st.markdown("---")

        st.subheader("3. Compact (render_chart_compact)")
        fig = create_themed_line_chart(df_temporal.tail(30), x='fecha', y='saldo')
        render_chart_compact(fig, title="Gráfica Compacta")

        st.markdown("---")

        st.subheader("4. Grid Layout (create_chart_grid)")
        charts = [
            {
                "fig": create_themed_bar_chart(df_categorias, x='categoria', y='importe'),
                "title": "Chart 1",
                "variant": "minimal"
            },
            {
                "fig": create_themed_pie_chart(df_distribucion, names='tipo', values='valor'),
                "title": "Chart 2",
                "variant": "minimal"
            },
            {
                "fig": create_themed_line_chart(df_temporal.tail(30), x='fecha', y='saldo'),
                "title": "Chart 3",
                "variant": "minimal"
            },
            {
                "fig": create_themed_line_chart(df_temporal.tail(30), x='fecha', y='ingresos'),
                "title": "Chart 4",
                "variant": "minimal"
            }
        ]
        create_chart_grid(charts, columns=2)

        st.markdown("---")

        st.subheader("5. Tabs Layout (render_chart_with_tabs)")
        render_chart_with_tabs({
            "Saldo": {
                "fig": create_themed_line_chart(df_temporal, x='fecha', y='saldo'),
                "title": "Evolución del Saldo"
            },
            "Ingresos": {
                "fig": create_themed_line_chart(df_temporal, x='fecha', y='ingresos'),
                "title": "Evolución de Ingresos"
            },
            "Gastos": {
                "fig": create_themed_line_chart(df_temporal, x='fecha', y='gastos'),
                "title": "Evolución de Gastos"
            }
        })

    # === TAB 6: PRESETS ===
    with tab6:
        st.header("Configuraciones Preset")

        st.subheader("Presets disponibles:")
        for preset_name, config in PRESET_CONFIGS.items():
            st.code(f"{preset_name}: {config}")

        st.markdown("---")

        st.subheader("1. Preset: finance_dashboard")
        fig = create_themed_line_chart(df_temporal, x='fecha', y='saldo')
        render_chart_preset("finance_dashboard", fig, title="Finance Dashboard Preset")

        st.markdown("---")

        st.subheader("2. Preset: compact_widget")
        fig = create_themed_bar_chart(df_categorias, x='categoria', y='importe')
        render_chart_preset("compact_widget", fig, title="Compact Widget Preset")

        st.markdown("---")

        st.subheader("3. Preset: fullscreen_analysis")
        fig = create_themed_line_chart(df_temporal, x='fecha', y='saldo')
        render_chart_preset("fullscreen_analysis", fig, title="Fullscreen Analysis Preset")

        st.markdown("---")

        st.subheader("4. Preset personalizado (con overrides)")
        fig = create_themed_pie_chart(df_distribucion, names='tipo', values='valor')
        render_chart_preset(
            "finance_dashboard",
            fig,
            title="Preset con Overrides",
            variant="glass",  # Override
            height=400        # Override
        )


# ========== SIDEBAR ==========

with st.sidebar:
    st.header("Configuración de Demo")

    st.markdown("### Información del Componente")
    st.info("""
    **ChartContainer** es un componente reutilizable
    para gráficas Plotly con estilos consistentes.

    **Características:**
    - ✅ Estilos premium
    - ✅ Variantes múltiples
    - ✅ Estados especiales
    - ✅ Acciones integradas
    - ✅ Layouts flexibles
    - ✅ Presets configurables
    """)

    st.markdown("### Navegación Rápida")
    st.markdown("""
    1. **Básico**: Uso fundamental
    2. **Variantes**: Estilos diferentes
    3. **Estados**: Loading/Empty/Error
    4. **Acciones**: Botones y controles
    5. **Layouts**: Disposiciones
    6. **Presets**: Configuraciones predefinidas
    """)

    st.markdown("### Enlaces")
    st.markdown("""
    - [Documentación Plotly](https://plotly.com/python/)
    - [Streamlit Docs](https://docs.streamlit.io/)
    - [Design Tokens](/utils/design_tokens.py)
    - [Plotly Theme](/utils/plotly_theme.py)
    """)


# ========== EJECUTAR ==========

if __name__ == "__main__":
    main()
