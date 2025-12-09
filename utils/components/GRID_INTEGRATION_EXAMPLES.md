# Grid System - Ejemplos de Integración

Guía práctica de cómo integrar el Grid System con los componentes existentes de la aplicación.

## Tabla de Contenidos
1. [Grid + MetricCard](#1-grid--metriccard)
2. [Grid + ChartContainer](#2-grid--chartcontainer)
3. [Grid + FormCard](#3-grid--formcard)
4. [Grid + DataTable](#4-grid--datatable)
5. [Layouts Completos](#5-layouts-completos)

---

## 1. Grid + MetricCard

### Dashboard de Métricas Financieras

```python
import streamlit as st
from utils.components import render_grid, render_metric_card
from utils.metrics import calcular_totales_mes

# Obtener datos
datos = calcular_totales_mes(mes=10, año=2024)

# Crear función renderer personalizada
def render_financial_metric(data, idx):
    render_metric_card(
        label=data["label"],
        value=data["value"],
        change=data.get("change"),
        change_label=data.get("change_label"),
        trend=data.get("trend", "neutral"),
        icon=data.get("icon"),
        help_text=data.get("help")
    )

# Preparar métricas
metrics = [
    {
        "label": "Ingresos Totales",
        "value": f"{datos['total_ingresos']:,.2f}€",
        "change": "+15%",
        "change_label": "vs mes anterior",
        "trend": "up",
        "icon": "💰",
        "help": "Total de ingresos del mes actual"
    },
    {
        "label": "Gastos Totales",
        "value": f"{abs(datos['total_gastos']):,.2f}€",
        "change": "-5%",
        "change_label": "vs mes anterior",
        "trend": "down",
        "icon": "💸",
        "help": "Total de gastos del mes actual"
    },
    {
        "label": "Balance Neto",
        "value": f"{datos['balance_mes']:,.2f}€",
        "change": "+10%",
        "change_label": "vs mes anterior",
        "trend": "up" if datos['balance_mes'] > 0 else "down",
        "icon": "💵",
        "help": "Diferencia entre ingresos y gastos"
    },
    {
        "label": "Tasa de Ahorro",
        "value": f"{datos['tasa_ahorro']:.1f}%",
        "change": "+3%",
        "change_label": "vs mes anterior",
        "trend": "up",
        "icon": "🎯",
        "help": "Porcentaje de ingresos ahorrados"
    }
]

# Renderizar grid de métricas
st.subheader("📊 Resumen Financiero")
render_grid(metrics, cols=4, gap='lg', item_renderer=render_financial_metric)
```

### Grid de Métricas por Categoría

```python
from utils.components import render_card_grid
from utils.design_tokens import Colors
from database.db_manager import obtener_totales_por_categoria

# Obtener datos por categoría
categorias = obtener_totales_por_categoria(mes=10, año=2024)

# Mapear a cards
cards = []
color_map = {
    "FIJOS": Colors.PRIMARY,
    "DISFRUTE": Colors.SUCCESS,
    "EXTRAORDINARIOS": Colors.WARNING,
    "INGRESO": Colors.ACCENT_TEAL
}

for cat in categorias:
    cards.append({
        "title": cat["categoria"],
        "content": f"{abs(cat['total']):,.2f}€",
        "footer": f"{cat['porcentaje']:.1f}% del total",
        "color": color_map.get(cat["categoria"], Colors.GRAY_500)
    })

# Renderizar
st.subheader("📂 Distribución por Categoría")
render_card_grid(cards, cols=4, gap='md')
```

---

## 2. Grid + ChartContainer

### Dashboard con Múltiples Gráficos

```python
import streamlit as st
from utils.components import render_grid, render_chart_container
from utils.visualizer import (
    grafico_distribucion_gastos,
    grafico_evolucion_anual
)
from utils.metrics import calcular_totales_mes, calcular_totales_anual

# Función renderer de gráficos
def render_chart_item(chart_data, idx):
    render_chart_container(
        title=chart_data["title"],
        chart=chart_data["fig"],
        description=chart_data.get("description"),
        height=chart_data.get("height", 400),
        actions=chart_data.get("actions", [])
    )

# Preparar gráficos
datos_mes = calcular_totales_mes(mes=10, año=2024)
datos_anual = calcular_totales_anual(año=2024)

charts = [
    {
        "title": "Distribución de Gastos (Octubre)",
        "fig": grafico_distribucion_gastos(datos_mes["por_categoria"]),
        "description": "Desglose de gastos por categoría del mes actual",
        "height": 350
    },
    {
        "title": "Evolución Anual 2024",
        "fig": grafico_evolucion_anual(datos_anual["evolucion_mensual"]),
        "description": "Tendencia de ingresos y gastos a lo largo del año",
        "height": 350
    }
]

# Renderizar en 2 columnas
st.subheader("📈 Análisis Visual")
render_grid(charts, cols=2, gap='xl', item_renderer=render_chart_item)
```

### Grid de Gráficos Compactos

```python
from utils.components import auto_grid, render_chart_compact

def render_compact_chart(data, idx):
    render_chart_compact(
        title=data["title"],
        chart=data["fig"],
        height=250
    )

# Múltiples gráficos pequeños
mini_charts = [
    {"title": "Gastos FIJOS", "fig": create_mini_chart("FIJOS")},
    {"title": "Gastos DISFRUTE", "fig": create_mini_chart("DISFRUTE")},
    {"title": "Gastos EXTRAORDINARIOS", "fig": create_mini_chart("EXTRAORDINARIOS")},
    {"title": "Evolución Semanal", "fig": create_weekly_chart()},
]

# Auto grid - se ajusta automáticamente
auto_grid(mini_charts, min_width='300px', gap='md', item_renderer=render_compact_chart)
```

---

## 3. Grid + FormCard

### Configuración Multi-Sección

```python
from utils.components import render_grid, render_form_card

def render_config_form(form_data, idx):
    with render_form_card(
        title=form_data["title"],
        description=form_data["description"],
        icon=form_data.get("icon")
    ):
        # Renderizar campos del formulario
        for field in form_data["fields"]:
            if field["type"] == "text":
                st.text_input(field["label"], key=field["key"])
            elif field["type"] == "number":
                st.number_input(field["label"], key=field["key"])
            elif field["type"] == "select":
                st.selectbox(field["label"], field["options"], key=field["key"])

        # Botón de guardar
        if st.button("Guardar", key=f"save_{idx}"):
            st.success("Configuración guardada")

# Definir secciones de configuración
config_sections = [
    {
        "title": "Perfil de Usuario",
        "description": "Información personal",
        "icon": "👤",
        "fields": [
            {"type": "text", "label": "Nombre", "key": "nombre"},
            {"type": "text", "label": "Email", "key": "email"}
        ]
    },
    {
        "title": "Preferencias",
        "description": "Configuración de la aplicación",
        "icon": "⚙️",
        "fields": [
            {"type": "select", "label": "Moneda", "options": ["EUR", "USD"], "key": "moneda"},
            {"type": "select", "label": "Idioma", "options": ["ES", "EN"], "key": "idioma"}
        ]
    },
    {
        "title": "Notificaciones",
        "description": "Gestionar alertas y avisos",
        "icon": "🔔",
        "fields": [
            {"type": "select", "label": "Frecuencia", "options": ["Diaria", "Semanal"], "key": "freq"}
        ]
    }
]

# Renderizar en grid
st.title("⚙️ Configuración")
render_grid(config_sections, cols=3, gap='lg', item_renderer=render_config_form)
```

---

## 4. Grid + DataTable

### Tablas Comparativas

```python
from utils.components import render_grid, render_transaction_table
from database.db_manager import obtener_transacciones

def render_month_table(month_data, idx):
    st.subheader(month_data["title"])

    # Obtener transacciones del mes
    transacciones = obtener_transacciones(
        mes=month_data["mes"],
        año=month_data["año"]
    )

    # Renderizar tabla
    render_transaction_table(
        data=transacciones,
        show_filters=False,
        compact=True,
        max_rows=10
    )

    # Métricas del mes
    total = sum(t['importe'] for t in transacciones)
    st.metric("Total", f"{total:,.2f}€")

# Comparar 3 meses
months = [
    {"title": "Agosto 2024", "mes": 8, "año": 2024},
    {"title": "Septiembre 2024", "mes": 9, "año": 2024},
    {"title": "Octubre 2024", "mes": 10, "año": 2024}
]

st.title("📊 Comparativa Trimestral")
render_grid(months, cols=3, gap='lg', item_renderer=render_month_table)
```

---

## 5. Layouts Completos

### Dashboard Completo con Grid System

```python
import streamlit as st
from utils.components import (
    render_grid,
    render_card_grid,
    render_metric_card,
    render_chart_container,
    page_header
)
from utils.design_tokens import Colors

def build_financial_dashboard():
    """Dashboard financiero completo usando Grid System"""

    # Header
    page_header(
        title="Dashboard Financiero",
        subtitle="Resumen completo de tu situación financiera",
        icon="📊"
    )

    # Sección 1: Métricas principales (4 columnas)
    st.subheader("💰 Métricas Principales")

    def render_main_metric(data, idx):
        render_metric_card(
            label=data["label"],
            value=data["value"],
            change=data["change"],
            trend=data["trend"],
            icon=data["icon"]
        )

    main_metrics = [
        {"label": "Líquido", "value": "15,320€", "change": "+8%", "trend": "up", "icon": "💵"},
        {"label": "Ingresos", "value": "2,500€", "change": "+15%", "trend": "up", "icon": "💰"},
        {"label": "Gastos", "value": "1,800€", "change": "-5%", "trend": "down", "icon": "💸"},
        {"label": "Ahorro", "value": "28%", "change": "+3%", "trend": "up", "icon": "🎯"}
    ]

    render_grid(main_metrics, cols=4, gap='lg', item_renderer=render_main_metric)

    st.markdown("---")

    # Sección 2: Categorías (4 cards)
    st.subheader("📂 Distribución por Categoría")

    categories = [
        {"title": "FIJOS", "content": "850€", "footer": "35%", "color": Colors.PRIMARY},
        {"title": "DISFRUTE", "content": "720€", "footer": "30%", "color": Colors.SUCCESS},
        {"title": "EXTRAORDINARIOS", "content": "230€", "footer": "10%", "color": Colors.WARNING},
        {"title": "AHORRADO", "content": "700€", "footer": "28%", "color": Colors.ACCENT_TEAL}
    ]

    render_card_grid(categories, cols=4, gap='md')

    st.markdown("---")

    # Sección 3: Gráficos (2 columnas)
    st.subheader("📈 Análisis Visual")

    def render_analysis_chart(chart, idx):
        render_chart_container(
            title=chart["title"],
            chart=chart["fig"],
            description=chart["description"],
            height=400
        )

    charts = [
        {
            "title": "Distribución de Gastos",
            "fig": create_pie_chart(),
            "description": "Desglose por categoría"
        },
        {
            "title": "Evolución Mensual",
            "fig": create_line_chart(),
            "description": "Últimos 6 meses"
        }
    ]

    render_grid(charts, cols=2, gap='xl', item_renderer=render_analysis_chart)

    st.markdown("---")

    # Sección 4: Top transacciones (auto grid)
    st.subheader("🔝 Top 10 Gastos del Mes")

    def render_transaction_item(tx, idx):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.markdown(f"**{tx['concepto']}**")
        with col2:
            st.markdown(tx['fecha'])
        with col3:
            st.markdown(f"**{tx['importe']}€**")

    top_transactions = get_top_transactions(limit=10)
    auto_grid(top_transactions, min_width='300px', gap='sm', item_renderer=render_transaction_item)

# Ejecutar dashboard
build_financial_dashboard()
```

### Layout Responsive Multi-Dispositivo

```python
from utils.components import responsive_columns
from utils.design_tokens import Breakpoints

# CSS responsive personalizado
css = responsive_columns(desktop=6, tablet=3, mobile=1, gap='md')
st.markdown(css, unsafe_allow_html=True)

# Contenido que se adapta perfectamente
st.markdown('<div class="responsive-grid">', unsafe_allow_html=True)

items = [
    "Dashboard", "Transacciones", "Importar",
    "Categorías", "Presupuestos", "Reportes",
    "Configuración", "Ayuda", "Perfil"
]

for item in items:
    st.markdown(f'''
    <div style="
        padding: 2rem;
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    ">
        {item}
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
```

---

## Tips de Integración

### 1. Naming Conflicts
Si hay conflictos de nombres entre componentes:

```python
# ❌ Problema
from utils.components import render_metric_grid  # De metric_card
from utils.components.grid_system import render_metric_grid  # Del grid system

# ✅ Solución 1: Usar alias
from utils.components import render_metric_grid as metric_card_grid
from utils.components.grid_system import render_metric_grid

# ✅ Solución 2: Import explícito
from utils.components.grid_system import render_metric_grid
```

### 2. Performance
Para grids grandes, considera lazy loading:

```python
# Para >50 items, paginar
items_per_page = 20
page = st.number_input("Página", min_value=1, value=1)
start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page

paginated_items = all_items[start_idx:end_idx]
render_grid(paginated_items, cols=4)
```

### 3. Estado y Callbacks
Mantén estado entre renders:

```python
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

def render_selectable_item(item, idx):
    is_selected = st.session_state.selected_item == idx

    if st.button(item["title"], key=f"item_{idx}"):
        st.session_state.selected_item = idx
        st.rerun()

    if is_selected:
        st.info("Seleccionado")

render_grid(items, cols=3, item_renderer=render_selectable_item)
```

---

## Recursos Adicionales

- [Grid System README](README_GRID_SYSTEM.md)
- [Quick Start Guide](QUICK_START_GRID_SYSTEM.md)
- [Ejemplos Interactivos](grid_system_examples.py)
- [Design Tokens](../design_tokens.py)

---

Última actualización: 2025-12-04
