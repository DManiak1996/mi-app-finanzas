"""
MetricCard - Ejemplo de Uso Rápido (Quickstart)
================================================

Este script muestra los usos más comunes del componente MetricCard
de forma simple y directa.

Ejecutar con:
    streamlit run examples/metric_card_quickstart.py
"""

import streamlit as st
import sys
sys.path.insert(0, '.')

from utils.components.metric_card import (
    render_metric_card,
    metric_card_success,
    metric_card_danger,
    metric_card_info,
    render_metric_row
)

st.set_page_config(page_title="MetricCard Quickstart", layout="wide")

st.title("🚀 MetricCard - Quickstart")
st.markdown("Los usos más comunes en 5 minutos")
st.markdown("---")

# =============================================================================
# 1. USO MÁS BÁSICO
# =============================================================================
st.header("1. Uso Básico")
st.code("""
from utils.components.metric_card import render_metric_card

render_metric_card(
    title="Balance del Mes",
    value=700.50,
    icon="⚖️"
)
""", language="python")

render_metric_card(
    title="Balance del Mes",
    value=700.50,
    icon="⚖️"
)

st.markdown("---")

# =============================================================================
# 2. CON DELTA Y TENDENCIA
# =============================================================================
st.header("2. Con Delta y Tendencia")
st.code("""
render_metric_card(
    title="Ingresos",
    value=2500.00,
    delta=8.5,
    icon="💰",
    color="success",
    trend="up"
)
""", language="python")

render_metric_card(
    title="Ingresos",
    value=2500.00,
    delta=8.5,
    icon="💰",
    color="success",
    trend="up"
)

st.markdown("---")

# =============================================================================
# 3. FUNCIONES HELPER
# =============================================================================
st.header("3. Funciones Helper (Más Rápido)")
st.code("""
metric_card_success("Ingresos", 2500.00, delta=8.5, icon="💰")
metric_card_danger("Gastos", 1800.50, delta=-5.2, icon="💸")
metric_card_info("Balance", 700.25, icon="⚖️")
""", language="python")

col1, col2, col3 = st.columns(3)
with col1:
    metric_card_success("Ingresos", 2500.00, delta=8.5, icon="💰")
with col2:
    metric_card_danger("Gastos", 1800.50, delta=-5.2, icon="💸")
with col3:
    metric_card_info("Balance", 700.25, icon="⚖️")

st.markdown("---")

# =============================================================================
# 4. FILA COMPLETA (LAYOUT AUTOMÁTICO)
# =============================================================================
st.header("4. Fila Completa (Recomendado)")
st.code("""
render_metric_row([
    {"title": "Ingresos", "value": 2500, "color": "success", "icon": "💰"},
    {"title": "Gastos", "value": 1800, "color": "danger", "icon": "💸"},
    {"title": "Balance", "value": 700, "color": "info", "icon": "⚖️"}
])
""", language="python")

render_metric_row([
    {"title": "Ingresos", "value": 2500, "color": "success", "icon": "💰"},
    {"title": "Gastos", "value": 1800, "color": "danger", "icon": "💸"},
    {"title": "Balance", "value": 700, "color": "info", "icon": "⚖️"}
])

st.markdown("---")

# =============================================================================
# 5. DIFERENTES FORMATOS
# =============================================================================
st.header("5. Diferentes Formatos")
st.code("""
render_metric_row([
    {"title": "Moneda", "value": 1234.56, "format_type": "currency"},
    {"title": "Porcentaje", "value": 28.5, "format_type": "percent"},
    {"title": "Número", "value": 12345, "format_type": "number"},
    {"title": "Texto", "value": "En proceso", "format_type": "text"}
])
""", language="python")

render_metric_row([
    {"title": "Moneda", "value": 1234.56, "format_type": "currency", "color": "success", "icon": "💵"},
    {"title": "Porcentaje", "value": 28.5, "format_type": "percent", "color": "info", "icon": "📊"},
    {"title": "Número", "value": 12345, "format_type": "number", "color": "warning", "icon": "🔢"},
    {"title": "Texto", "value": "En proceso", "format_type": "text", "color": "neutral", "icon": "📝"}
])

st.markdown("---")

# =============================================================================
# 6. DASHBOARD COMPLETO (EJEMPLO REAL)
# =============================================================================
st.header("6. Dashboard Completo (Ejemplo Real)")

st.subheader("Resumen Mensual")
render_metric_row([
    {
        "title": "Total Ingresos",
        "value": 2500.00,
        "delta": 5.2,
        "icon": "💰",
        "color": "success",
        "trend": "up"
    },
    {
        "title": "Total Gastos",
        "value": 1850.50,
        "delta": -3.1,
        "icon": "💸",
        "color": "danger",
        "trend": "down"
    },
    {
        "title": "Balance",
        "value": 649.50,
        "delta": 12.8,
        "icon": "⚖️",
        "color": "info",
        "trend": "up"
    }
])

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Métricas Avanzadas")
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card_info("Tasa Ahorro", 26.0, format_type="percent", icon="🎯")

with col2:
    render_metric_card("Gasto/Día", 61.68, icon="📅", color="neutral")

with col3:
    metric_card_info("Transacciones", 87, format_type="number", icon="📋")

with col4:
    render_metric_card("Health Score", 85, format_type="number", icon="💯", color="success")

st.markdown("---")

# =============================================================================
# 7. CHEATSHEET
# =============================================================================
st.header("7. Cheatsheet Rápido")

with st.expander("Ver Cheatsheet Completo"):
    st.markdown("""
    ### Colores Disponibles
    ```python
    color="success"   # Verde (ingresos, positivo)
    color="danger"    # Rojo (gastos, negativo)
    color="info"      # Azul (información)
    color="warning"   # Naranja (advertencia)
    color="neutral"   # Gris (neutral)
    ```

    ### Formatos Disponibles
    ```python
    format_type="currency"  # 1.234,56 €
    format_type="percent"   # 28.5%
    format_type="number"    # 1.234
    format_type="text"      # Sin formato
    ```

    ### Tendencias
    ```python
    trend="up"       # Flecha hacia arriba ↗
    trend="down"     # Flecha hacia abajo ↘
    trend="neutral"  # Flecha horizontal →
    ```

    ### Iconos Recomendados
    ```python
    "💰" # Ingresos
    "💸" # Gastos
    "⚖️" # Balance
    "📊" # Porcentajes/Estadísticas
    "📈" # Tendencia positiva
    "📉" # Tendencia negativa
    "🎯" # Objetivos
    "⚡" # Alertas
    "📅" # Tiempo/Días
    "📋" # Listas/Transacciones
    "💯" # Puntuaciones
    ```

    ### Funciones Helper
    ```python
    metric_card_success()  # Verde
    metric_card_danger()   # Rojo
    metric_card_info()     # Azul
    metric_card_warning()  # Naranja
    metric_card_neutral()  # Gris
    ```

    ### Layout
    ```python
    render_metric_row([...])   # Fila horizontal
    render_metric_grid([...])  # Grid responsive
    ```

    ### Opciones Especiales
    ```python
    glassmorphism=True   # Efecto vidrio
    show_border=False    # Sin barra superior
    help_text="..."      # Tooltip explicativo
    ```
    """)

st.markdown("---")
st.caption("📚 Documentación completa: docs/METRIC_CARD_USAGE.md")
st.caption("🎨 Demo completa: demo_metric_card.py")
