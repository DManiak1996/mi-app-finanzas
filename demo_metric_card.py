"""
Demo del componente MetricCard
===============================

Script de demostración para probar el componente MetricCard
sin las dependencias problemáticas de otros módulos.

Ejecutar con:
    streamlit run demo_metric_card.py
"""

import streamlit as st
import sys
sys.path.insert(0, '.')

# Importar directamente desde el archivo (evitando __init__.py problemático)
from utils.components.metric_card import (
    render_metric_card,
    metric_card_success,
    metric_card_danger,
    metric_card_info,
    metric_card_warning,
    metric_card_neutral,
    render_metric_row,
    render_metric_grid
)

# Configuración de la página
st.set_page_config(
    page_title="MetricCard Demo",
    page_icon="🎨",
    layout="wide"
)

# Título principal
st.title("🎨 MetricCard Component Demo")
st.markdown("Componente reutilizable para métricas premium con diseño glassmorphism")
st.markdown("---")

# Sección 1: Variantes básicas
st.header("1. Variantes de Color")
st.markdown("Cinco variantes de color para diferentes tipos de métricas:")

render_metric_row([
    {
        "title": "Success",
        "value": 2500.50,
        "delta": 8.5,
        "icon": "💰",
        "color": "success",
        "trend": "up",
        "help_text": "Variante verde para ingresos/positivo"
    },
    {
        "title": "Danger",
        "value": 1800.25,
        "delta": -5.2,
        "icon": "💸",
        "color": "danger",
        "trend": "down",
        "help_text": "Variante roja para gastos/negativo"
    },
    {
        "title": "Info",
        "value": 700.25,
        "delta": 3.3,
        "icon": "⚖️",
        "color": "info",
        "trend": "up",
        "help_text": "Variante azul para información"
    }
])

st.markdown("<br>", unsafe_allow_html=True)

render_metric_row([
    {
        "title": "Warning",
        "value": 850.00,
        "delta": 15.0,
        "icon": "⚡",
        "color": "warning",
        "trend": "up",
        "help_text": "Variante naranja para alertas"
    },
    {
        "title": "Neutral",
        "value": 60.15,
        "icon": "📊",
        "color": "neutral",
        "help_text": "Variante gris para datos generales"
    }
])

st.markdown("---")

# Sección 2: Formatos
st.header("2. Tipos de Formato")
st.markdown("Formato automático de números: currency, percent, number, text")

render_metric_row([
    {
        "title": "Currency",
        "value": 1234.56,
        "icon": "💵",
        "format_type": "currency",
        "color": "success"
    },
    {
        "title": "Percent",
        "value": 28.5,
        "icon": "📊",
        "format_type": "percent",
        "color": "info"
    },
    {
        "title": "Number",
        "value": 12345,
        "icon": "🔢",
        "format_type": "number",
        "color": "neutral"
    },
    {
        "title": "Text",
        "value": "Custom Value",
        "icon": "📝",
        "format_type": "text",
        "color": "warning"
    }
])

st.markdown("---")

# Sección 3: Funciones helper
st.header("3. Funciones Helper")
st.markdown("Atajos para variantes comunes:")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Success & Danger")
    metric_card_success("Ingresos Totales", 2500.00, delta=8.5, icon="💰")
    st.markdown("<br>", unsafe_allow_html=True)
    metric_card_danger("Gastos Totales", 1800.50, delta=-5.2, icon="💸")

with col2:
    st.subheader("Info, Warning & Neutral")
    metric_card_info("Transacciones", 45, format_type="number", icon="📋")
    st.markdown("<br>", unsafe_allow_html=True)
    metric_card_warning("Presupuesto", "85%", icon="⚠️")
    st.markdown("<br>", unsafe_allow_html=True)
    metric_card_neutral("Promedio Diario", 60.15, icon="📈")

st.markdown("---")

# Sección 4: Glassmorphism
st.header("4. Efecto Glassmorphism")
st.markdown("Efecto de vidrio translúcido con backdrop-filter:")

render_metric_row([
    {
        "title": "Balance Premium",
        "value": 700.50,
        "delta": 15.5,
        "icon": "✨",
        "color": "info",
        "trend": "up",
        "glassmorphism": True,
        "help_text": "Con efecto glassmorphism activado"
    },
    {
        "title": "Ahorro Mensual",
        "value": 500.00,
        "delta": 20.0,
        "icon": "💎",
        "color": "success",
        "trend": "up",
        "glassmorphism": True
    },
    {
        "title": "Inversiones",
        "value": 3500.00,
        "icon": "📈",
        "color": "warning",
        "glassmorphism": True
    }
])

st.markdown("---")

# Sección 5: Grid layout
st.header("5. Grid Layout")
st.markdown("Organización automática en grid responsive:")

metrics_data = [
    {"title": "Métrica 1", "value": 100.50, "icon": "1️⃣", "color": "success", "format_type": "currency"},
    {"title": "Métrica 2", "value": 200.75, "icon": "2️⃣", "color": "info", "format_type": "currency"},
    {"title": "Métrica 3", "value": 300.25, "icon": "3️⃣", "color": "warning", "format_type": "currency"},
    {"title": "Métrica 4", "value": 400.00, "icon": "4️⃣", "color": "danger", "format_type": "currency"},
    {"title": "Métrica 5", "value": 500.99, "icon": "5️⃣", "color": "neutral", "format_type": "currency"},
    {"title": "Métrica 6", "value": 600.33, "icon": "6️⃣", "color": "success", "format_type": "currency"},
]

render_metric_grid(metrics_data, columns_desktop=3)

st.markdown("---")

# Sección 6: Ejemplo real de dashboard financiero
st.header("6. Ejemplo Real: Dashboard Financiero")
st.markdown("Simulación de métricas de un dashboard de finanzas:")

st.subheader("Resumen del Mes")
render_metric_row([
    {
        "title": "Total Ingresos",
        "value": 2500.00,
        "delta": 5.2,
        "icon": "💰",
        "color": "success",
        "trend": "up",
        "help_text": "Ingresos totales del mes actual"
    },
    {
        "title": "Total Gastos",
        "value": 1850.50,
        "delta": -3.1,
        "icon": "💸",
        "color": "danger",
        "trend": "down",
        "help_text": "Gastos totales del mes actual"
    },
    {
        "title": "Balance",
        "value": 649.50,
        "delta": 12.8,
        "icon": "⚖️",
        "color": "info",
        "trend": "up",
        "help_text": "Diferencia entre ingresos y gastos"
    }
])

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Métricas Avanzadas")
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card_info("Tasa de Ahorro", 26.0, format_type="percent", icon="🎯")

with col2:
    metric_card_neutral("Gasto Promedio/Día", 61.68, icon="📅")

with col3:
    metric_card_warning("Transacciones", 87, format_type="number", icon="📋")

with col4:
    metric_card_success("Health Score", 85, format_type="number", icon="💯")

st.markdown("---")

# Sección 7: Sin borde decorativo
st.header("7. Variante sin Borde")
st.markdown("Métricas sin la barra decorativa superior:")

render_metric_row([
    {
        "title": "Sin Borde 1",
        "value": 1500.00,
        "icon": "📊",
        "color": "success",
        "show_border": False
    },
    {
        "title": "Sin Borde 2",
        "value": 2500.00,
        "icon": "📈",
        "color": "info",
        "show_border": False
    },
    {
        "title": "Sin Borde 3",
        "value": 3500.00,
        "icon": "💹",
        "color": "warning",
        "show_border": False
    }
])

st.markdown("---")

# Footer
st.markdown("---")
st.caption("🎨 MetricCard Component v1.0 | Desarrollado para FinanzasFlow")
st.caption("Integrado con design_tokens.py para consistencia visual")
