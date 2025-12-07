"""
Script de prueba rápida para verificar componentes nativos
==========================================================

Este script verifica que render_metric_card() y render_metric_grid()
funcionen correctamente con componentes nativos de Streamlit.
"""

import streamlit as st
from utils.components.metric_card import render_metric_card, render_metric_grid

st.set_page_config(page_title="Test Native Metrics", layout="wide")

st.title("Prueba de Componentes Nativos")
st.markdown("---")

# Test 1: Métrica individual
st.header("1. Métrica Individual")
render_metric_card(
    title="Total Ingresos",
    value=2500.50,
    delta=150.25,
    icon="💰",
    color="success",
    trend="up",
    format_type="currency",
    help_text="Esto es una métrica de prueba"
)

st.markdown("---")

# Test 2: Grid de métricas
st.header("2. Grid de Métricas")
metrics_data = [
    {
        "title": "Ingresos",
        "value": 2500.00,
        "delta": 8.5,
        "icon": "💵",
        "color": "success",
        "format_type": "currency"
    },
    {
        "title": "Gastos",
        "value": 1800.50,
        "delta": -5.2,
        "icon": "💸",
        "color": "danger",
        "format_type": "currency"
    },
    {
        "title": "Balance",
        "value": 700.50,
        "delta": 15.5,
        "icon": "⚖️",
        "color": "info",
        "trend": "up",
        "format_type": "currency"
    },
    {
        "title": "Tasa Ahorro",
        "value": 28.5,
        "icon": "💾",
        "color": "success",
        "format_type": "percent"
    }
]

render_metric_grid(metrics_data, columns_desktop=4)

st.markdown("---")

# Test 3: Grid con 3 columnas
st.header("3. Grid con 3 Columnas")
metrics_3col = [
    {"title": "Métrica 1", "value": 100, "icon": "1️⃣", "color": "success", "format_type": "number"},
    {"title": "Métrica 2", "value": 200, "icon": "2️⃣", "color": "info", "format_type": "number"},
    {"title": "Métrica 3", "value": 300, "icon": "3️⃣", "color": "warning", "format_type": "number"},
    {"title": "Métrica 4", "value": 400, "icon": "4️⃣", "color": "danger", "format_type": "number"},
    {"title": "Métrica 5", "value": 500, "icon": "5️⃣", "color": "neutral", "format_type": "number"}
]

render_metric_grid(metrics_3col, columns_desktop=3)

st.success("✅ Todas las pruebas completadas. Si ves métricas con st.metric() nativo arriba, el componente funciona correctamente.")
