#!/usr/bin/env python3
"""
Script de prueba para verificar que las metric cards se renderizan correctamente
sin mostrar HTML crudo.
"""

import streamlit as st
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.components.metric_card import render_metric_card, render_metric_grid

st.set_page_config(page_title="Test Metric Cards", layout="wide")

st.title("🧪 Test de Metric Cards - Nuevo Diseño")
st.markdown("---")

st.header("✅ Test 1: Métrica Simple")
st.markdown("**Esperado:** Debe verse una card bonita con gradiente verde, NO código HTML crudo")

render_metric_card(
    title="Líquido Disponible",
    value=1234.56,
    icon="💧",
    color="info",
    format_type="currency",
    help_text="Balance acumulado de todas tus transacciones"
)

st.markdown("---")

st.header("✅ Test 2: Grid de Métricas (Resumen Mensual)")
st.markdown("**Esperado:** 4 cards en una fila, cada una con su color y gradiente")

metrics_data = [
    {
        "title": "Total Ingresos Mes",
        "value": 2500.00,
        "icon": "💵",
        "color": "success",
        "format_type": "currency",
        "help_text": "Suma de todos los ingresos del mes"
    },
    {
        "title": "Gastos del Mes",
        "value": 1800.50,
        "icon": "💸",
        "color": "danger",
        "format_type": "currency",
        "help_text": "Gastos netos del período"
    },
    {
        "title": "Balance del Mes",
        "value": 699.50,
        "delta": 699.50,
        "icon": "⚖️",
        "color": "info",
        "trend": "up",
        "format_type": "currency",
        "help_text": "Diferencia entre ingresos y gastos"
    },
    {
        "title": "Tasa Ahorro",
        "value": 27.98,
        "delta": "699 €",
        "icon": "💾",
        "color": "success",
        "format_type": "percent",
        "help_text": "Porcentaje de ahorro sobre ingresos"
    }
]

render_metric_grid(metrics_data, columns_desktop=4)

st.markdown("---")

st.header("✅ Test 3: Hover Effect")
st.markdown("**Esperado:** Al pasar el mouse, la card se eleva suavemente (hover funciona)")

render_metric_card(
    title="Hover Test",
    value=999.99,
    delta=10.5,
    icon="🎯",
    color="warning",
    trend="up",
    format_type="currency",
    help_text="Pasa el mouse sobre esta card"
)

st.markdown("---")

st.success("✅ Si ves las cards con diseño premium (gradientes, sombras, hover effect) y NO ves código HTML crudo, ¡el problema está resuelto!")
st.error("❌ Si ves código HTML en texto plano como `<div style='...'> ...`, el problema persiste")
