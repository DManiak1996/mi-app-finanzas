#!/usr/bin/env python3
# utils/components/EJEMPLO_CHART_CONTAINER.py
"""
Ejemplo rápido de uso del ChartContainer

Este archivo muestra los casos de uso más comunes del componente.
Cópialo y pégalo en tu página para comenzar.

Para ejecutar este ejemplo standalone:
    streamlit run utils/components/EJEMPLO_CHART_CONTAINER.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# === IMPORTACIONES DEL COMPONENTE ===
from utils.components import (
    render_chart_container,
    render_chart_half,
    render_chart_preset,
    add_chart_actions
)

# === IMPORTACIONES DE TEMAS PLOTLY ===
from utils.plotly_theme import (
    create_themed_line_chart,
    create_themed_bar_chart,
    create_themed_pie_chart
)


# === DATOS DE EJEMPLO ===

@st.cache_data
def obtener_datos_ejemplo():
    """Genera datos de ejemplo para el demo."""

    # Datos temporales para línea
    fechas = pd.date_range(start='2024-11-01', end='2024-11-30', freq='D')
    df_balance = pd.DataFrame({
        'fecha': fechas,
        'saldo': 1000 + (fechas.day * 10) + pd.np.random.randint(-50, 50, len(fechas))
    })

    # Datos para barra
    df_categorias = pd.DataFrame({
        'categoria': ['FIJOS', 'DISFRUTE', 'EXTRAORDINARIOS'],
        'total': [1200, 800, 300]
    })

    # Datos para pie
    df_distribucion = pd.DataFrame({
        'tipo': ['Alquiler', 'Comida', 'Transporte', 'Ocio', 'Otros'],
        'valor': [600, 350, 200, 150, 100]
    })

    return df_balance, df_categorias, df_distribucion


# === EJEMPLO 1: USO BÁSICO ===

def ejemplo_basico():
    st.header("Ejemplo 1: Uso Básico")

    df_balance, _, _ = obtener_datos_ejemplo()

    # Crear gráfica
    fig = create_themed_line_chart(
        df_balance,
        x='fecha',
        y='saldo',
        markers=True
    )

    # Renderizar con container
    render_chart_container(
        fig,
        title="Evolución del Saldo",
        description="Balance diario durante noviembre 2024"
    )

    # Mostrar código
    with st.expander("Ver código"):
        st.code('''
from utils.components import render_chart_container
from utils.plotly_theme import create_themed_line_chart

fig = create_themed_line_chart(df, x='fecha', y='saldo', markers=True)

render_chart_container(
    fig,
    title="Evolución del Saldo",
    description="Balance diario durante noviembre 2024"
)
        ''', language='python')


# === EJEMPLO 2: CON ACCIONES ===

def ejemplo_con_acciones():
    st.header("Ejemplo 2: Con Acciones")

    _, df_categorias, _ = obtener_datos_ejemplo()

    # Crear gráfica
    fig = create_themed_bar_chart(
        df_categorias,
        x='categoria',
        y='total',
        text_auto=True
    )

    # Añadir acciones
    actions = add_chart_actions(
        export=True,
        filter=True,
        refresh=True
    )

    # Renderizar
    render_chart_container(
        fig,
        title="Gastos por Categoría",
        description="Distribución mensual con botones de acción",
        actions=actions,
        variant="premium"
    )

    # Mostrar código
    with st.expander("Ver código"):
        st.code('''
from utils.components import render_chart_container, add_chart_actions

actions = add_chart_actions(export=True, filter=True, refresh=True)

render_chart_container(
    fig,
    title="Gastos por Categoría",
    actions=actions,
    variant="premium"
)
        ''', language='python')


# === EJEMPLO 3: LAYOUT DE DOS COLUMNAS ===

def ejemplo_dos_columnas():
    st.header("Ejemplo 3: Layout de Dos Columnas")

    _, df_categorias, df_distribucion = obtener_datos_ejemplo()

    # Crear gráficas
    fig1 = create_themed_bar_chart(
        df_categorias,
        x='categoria',
        y='total'
    )

    fig2 = create_themed_pie_chart(
        df_distribucion,
        names='tipo',
        values='valor',
        hole=0.4
    )

    # Renderizar en dos columnas
    render_chart_half([
        {
            "fig": fig1,
            "title": "Totales por Categoría",
            "variant": "minimal"
        },
        {
            "fig": fig2,
            "title": "Distribución Detallada",
            "variant": "minimal"
        }
    ])

    # Mostrar código
    with st.expander("Ver código"):
        st.code('''
from utils.components import render_chart_half

render_chart_half([
    {"fig": fig1, "title": "Totales por Categoría"},
    {"fig": fig2, "title": "Distribución Detallada"}
])
        ''', language='python')


# === EJEMPLO 4: ESTADOS ESPECIALES ===

def ejemplo_estados():
    st.header("Ejemplo 4: Estados Especiales")

    estado = st.radio(
        "Selecciona un estado:",
        ["Normal", "Loading", "Empty", "Error"],
        horizontal=True
    )

    df_balance, _, _ = obtener_datos_ejemplo()
    fig = create_themed_line_chart(df_balance, x='fecha', y='saldo')

    if estado == "Loading":
        render_chart_container(
            loading=True,
            title="Cargando datos..."
        )
    elif estado == "Empty":
        render_chart_container(
            empty_message="No hay transacciones este mes",
            title="Sin Datos"
        )
    elif estado == "Error":
        render_chart_container(
            error="Error al conectar con la base de datos",
            title="Error de Conexión"
        )
    else:
        render_chart_container(fig, title="Gráfica Normal")

    # Mostrar código
    with st.expander("Ver código"):
        st.code('''
# Loading
render_chart_container(loading=True, title="Cargando...")

# Empty
render_chart_container(
    empty_message="No hay datos",
    title="Sin Datos"
)

# Error
render_chart_container(
    error="Error al conectar",
    title="Error"
)
        ''', language='python')


# === EJEMPLO 5: USANDO PRESETS ===

def ejemplo_presets():
    st.header("Ejemplo 5: Usando Presets")

    df_balance, _, _ = obtener_datos_ejemplo()
    fig = create_themed_line_chart(df_balance, x='fecha', y='saldo')

    preset = st.selectbox(
        "Selecciona un preset:",
        ["finance_dashboard", "compact_widget", "fullscreen_analysis"]
    )

    # Renderizar con preset
    render_chart_preset(
        preset,
        fig,
        title=f"Gráfica con preset '{preset}'"
    )

    # Mostrar código
    with st.expander("Ver código"):
        st.code('''
from utils.components import render_chart_preset

render_chart_preset(
    "finance_dashboard",
    fig,
    title="Dashboard Financiero"
)
        ''', language='python')


# === PÁGINA PRINCIPAL ===

def main():
    st.set_page_config(
        page_title="Ejemplo ChartContainer",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 Ejemplos de Uso - ChartContainer")
    st.markdown("""
    Este documento muestra los casos de uso más comunes del componente `ChartContainer`.
    Cada ejemplo incluye el código para que puedas copiarlo directamente.
    """)

    st.divider()

    # Ejecutar ejemplos
    ejemplo_basico()
    st.divider()

    ejemplo_con_acciones()
    st.divider()

    ejemplo_dos_columnas()
    st.divider()

    ejemplo_estados()
    st.divider()

    ejemplo_presets()

    # Footer
    st.divider()
    st.info("""
    **Documentación completa:** `utils/components/README_CHART_CONTAINER.md`

    **Demo interactiva:** `streamlit run utils/components/chart_container_demo.py`

    **Tests:** `python tests/test_chart_container.py`
    """)


if __name__ == "__main__":
    main()
