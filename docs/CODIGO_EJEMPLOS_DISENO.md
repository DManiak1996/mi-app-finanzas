# Código de Ejemplos - Componentes de Diseño

**Complemento de**: ANALISIS_DISENO_UX.md
**Fecha**: 2025-12-04

Este documento contiene código listo para copiar y pegar para implementar las mejoras propuestas.

---

## 1. QUICK WIN #1: Tema Plotly Unificado

### Archivo: `/Users/daniel/mi_app_finanzas/utils/plotly_theme.py` (NUEVO)

```python
"""
Tema Plotly unificado con design tokens.
Importar y aplicar a TODOS los gráficos de la app.
"""

from utils.design_tokens import Colors, Typography
import plotly.graph_objects as go

# === CONFIGURACIÓN GLOBAL DE PLOTLY ===
PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'finanzasflow_chart',
        'height': 600,
        'width': 1000,
        'scale': 2
    }
}

# === PALETA DE COLORES PARA GRÁFICOS ===
CHART_COLORS = {
    'income': Colors.SUCCESS,
    'expense': Colors.ERROR,
    'balance': Colors.PRIMARY,
    'categories': [
        Colors.CATEGORIA_FIJOS,
        Colors.CATEGORIA_DISFRUTE,
        Colors.CATEGORIA_EXTRAORDINARIOS,
        Colors.CATEGORIA_COCHE,
        Colors.SUCCESS,
        Colors.WARNING,
        Colors.PREMIUM_TEAL_START,
        Colors.PREMIUM_CORAL_START
    ]
}

# === LAYOUT BASE ===
def get_base_layout(title: str = None, height: int = 400) -> dict:
    """
    Layout base para todos los gráficos.

    Args:
        title: Título del gráfico (opcional)
        height: Altura en px (default 400)

    Returns:
        Dict con configuración de layout
    """

    return {
        'title': {
            'text': title,
            'font': {
                'family': Typography.FONT_PRIMARY,
                'size': 20,
                'weight': Typography.WEIGHT_BOLD,
                'color': Colors.GRAY_900
            },
            'x': 0.05,
            'xanchor': 'left'
        } if title else None,
        'font': {
            'family': Typography.FONT_PRIMARY,
            'size': 14,
            'color': Colors.GRAY_900
        },
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'margin': dict(l=60, r=40, t=60 if title else 40, b=60),
        'height': height,
        'hovermode': 'closest',
        'hoverlabel': {
            'bgcolor': 'white',
            'bordercolor': Colors.GRAY_300,
            'font': {
                'family': Typography.FONT_PRIMARY,
                'size': 14,
                'color': Colors.GRAY_900
            }
        },
        'colorway': CHART_COLORS['categories'],
        'xaxis': {
            'showgrid': True,
            'gridwidth': 1,
            'gridcolor': Colors.GRAY_200,
            'showline': True,
            'linewidth': 2,
            'linecolor': Colors.GRAY_300,
            'tickfont': {
                'size': 12,
                'color': Colors.GRAY_700
            }
        },
        'yaxis': {
            'showgrid': True,
            'gridwidth': 1,
            'gridcolor': Colors.GRAY_200,
            'showline': True,
            'linewidth': 2,
            'linecolor': Colors.GRAY_300,
            'zeroline': True,
            'zerolinewidth': 2,
            'zerolinecolor': Colors.GRAY_400,
            'tickfont': {
                'size': 12,
                'color': Colors.GRAY_700
            }
        }
    }


def apply_premium_theme(fig: go.Figure, title: str = None, height: int = 400) -> go.Figure:
    """
    Aplica tema premium a una figura existente.

    Args:
        fig: Figura de Plotly
        title: Título (opcional)
        height: Altura en px

    Returns:
        Figura con tema aplicado
    """

    fig.update_layout(**get_base_layout(title=title, height=height))

    return fig


# === EJEMPLO: Gráfico de Barras ===
def create_bar_chart(
    x_data: list,
    y_data: list,
    title: str = None,
    color: str = None,
    orientation: str = 'v'
) -> go.Figure:
    """
    Crea un gráfico de barras con tema premium.

    Args:
        x_data: Datos eje X
        y_data: Datos eje Y
        title: Título del gráfico
        color: Color de las barras (opcional, usa colorway si None)
        orientation: 'v' (vertical) o 'h' (horizontal)

    Returns:
        Figura de Plotly lista para mostrar
    """

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=x_data if orientation == 'v' else y_data,
        y=y_data if orientation == 'v' else x_data,
        orientation=orientation,
        marker=dict(
            color=color or CHART_COLORS['categories'][0],
            line=dict(color='white', width=2)
        ),
        text=y_data if orientation == 'v' else x_data,
        texttemplate='%{text:.2f}€',
        textposition='outside' if orientation == 'v' else 'auto',
        hovertemplate='<b>%{x}</b><br>%{y:.2f}€<extra></extra>' if orientation == 'v' else '<b>%{y}</b><br>%{x:.2f}€<extra></extra>'
    ))

    apply_premium_theme(fig, title=title)

    return fig


# === EJEMPLO: Gráfico Circular (Pie) ===
def create_pie_chart(
    labels: list,
    values: list,
    title: str = None,
    hole: float = 0.4
) -> go.Figure:
    """
    Crea un gráfico circular (donut) con tema premium.

    Args:
        labels: Etiquetas de las porciones
        values: Valores numéricos
        title: Título del gráfico
        hole: Tamaño del agujero (0 = pie completo, 0.4 = donut)

    Returns:
        Figura de Plotly
    """

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=hole,
        marker=dict(
            colors=CHART_COLORS['categories'],
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>%{value:.2f}€<br>%{percent}<extra></extra>'
    ))

    layout = get_base_layout(title=title, height=400)
    # Pie charts no necesitan ejes
    layout.pop('xaxis', None)
    layout.pop('yaxis', None)

    fig.update_layout(**layout)

    return fig


# === EJEMPLO: Gráfico de Línea ===
def create_line_chart(
    x_data: list,
    y_data: list,
    title: str = None,
    fill: bool = False,
    color: str = None
) -> go.Figure:
    """
    Crea un gráfico de línea con tema premium.

    Args:
        x_data: Datos eje X (fechas, categorías)
        y_data: Datos eje Y (valores)
        title: Título del gráfico
        fill: Si True, rellena área bajo la línea
        color: Color de la línea (opcional)

    Returns:
        Figura de Plotly
    """

    fig = go.Figure()

    line_color = color or Colors.PRIMARY

    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines+markers',
        line=dict(color=line_color, width=3),
        marker=dict(
            size=8,
            color=line_color,
            line=dict(width=2, color='white')
        ),
        fill='tozeroy' if fill else None,
        fillcolor=f'rgba({int(line_color[1:3], 16)}, {int(line_color[3:5], 16)}, {int(line_color[5:7], 16)}, 0.1)' if fill else None,
        hovertemplate='<b>%{x}</b><br>%{y:.2f}€<extra></extra>'
    ))

    apply_premium_theme(fig, title=title)

    return fig
```

### Uso en visualizer.py:

```python
# utils/visualizer.py - MODIFICAR
from utils.plotly_theme import (
    create_bar_chart,
    create_pie_chart,
    create_line_chart,
    apply_premium_theme,
    PLOTLY_CONFIG
)

def grafico_distribucion_gastos(gastos_por_categoria):
    """Gráfico de distribución de gastos (ACTUALIZADO)"""

    if not gastos_por_categoria:
        return None

    categorias = list(gastos_por_categoria.keys())
    importes = [abs(v) for v in gastos_por_categoria.values()]

    # ANTES: fig = go.Figure(go.Pie(...))
    # AHORA: Usar template
    fig = create_pie_chart(
        labels=categorias,
        values=importes,
        title="Distribución de Gastos por Categoría",
        hole=0.4
    )

    return fig
```

---

## 2. QUICK WIN #2: Empty States

### Archivo: `/Users/daniel/mi_app_finanzas/utils/empty_states.py` (NUEVO)

```python
"""
Empty states ilustrados para cuando no hay datos.
"""

from utils.design_tokens import Colors, Typography, Spacing

# === SVG: Sin Transacciones ===
EMPTY_TRANSACTIONS = f"""
<div style="text-align: center; padding: 3rem 1rem;">
    <svg width="180" height="180" viewBox="0 0 180 180" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="emptyGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{Colors.PREMIUM_PRIMARY_START};stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:{Colors.PREMIUM_PRIMARY_END};stop-opacity:0.1" />
            </linearGradient>
        </defs>
        <!-- Billetera vacía -->
        <rect x="40" y="60" width="100" height="70" rx="8" fill="url(#emptyGrad1)" stroke="{Colors.GRAY_300}" stroke-width="2"/>
        <rect x="50" y="70" width="80" height="10" rx="2" fill="{Colors.GRAY_200}"/>
        <rect x="50" y="90" width="60" height="8" rx="2" fill="{Colors.GRAY_200}"/>
        <circle cx="90" cy="95" r="35" fill="none" stroke="{Colors.GRAY_300}" stroke-width="2" stroke-dasharray="4 4"/>
        <text x="90" y="100" text-anchor="middle" font-size="14" fill="{Colors.GRAY_400}">0€</text>
    </svg>
    <h3 style="color: {Colors.GRAY_700}; font-family: {Typography.FONT_PRIMARY}; margin-top: {Spacing.LG};">
        No hay transacciones
    </h3>
    <p style="color: {Colors.GRAY_500}; font-family: {Typography.FONT_PRIMARY}; margin-top: {Spacing.SM};">
        Comienza importando tu archivo de Excel o añade tu primera transacción manualmente
    </p>
</div>
"""

# === SVG: Sin Presupuestos ===
EMPTY_BUDGETS = f"""
<div style="text-align: center; padding: 3rem 1rem;">
    <svg width="180" height="180" viewBox="0 0 180 180" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="emptyGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{Colors.PREMIUM_PRIMARY_START};stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:{Colors.PREMIUM_PRIMARY_END};stop-opacity:0.1" />
            </linearGradient>
        </defs>
        <!-- Diana con objetivo -->
        <circle cx="90" cy="90" r="60" fill="url(#emptyGrad2)"/>
        <circle cx="90" cy="90" r="45" fill="white"/>
        <circle cx="90" cy="90" r="30" fill="url(#emptyGrad2)"/>
        <circle cx="90" cy="90" r="15" fill="{Colors.PREMIUM_PRIMARY_END}"/>
        <path d="M 90 30 L 95 80 L 90 90 L 85 80 Z" fill="{Colors.ERROR}" stroke="white" stroke-width="2"/>
    </svg>
    <h3 style="color: {Colors.GRAY_700}; font-family: {Typography.FONT_PRIMARY}; margin-top: {Spacing.LG};">
        Sin presupuestos configurados
    </h3>
    <p style="color: {Colors.GRAY_500}; font-family: {Typography.FONT_PRIMARY}; margin-top: {Spacing.SM};">
        Define tus objetivos de gasto por categoría para mantener el control
    </p>
</div>
"""

# === SVG: Sin Datos de Gráfico ===
EMPTY_CHART = f"""
<div style="text-align: center; padding: 3rem 1rem;">
    <svg width="180" height="180" viewBox="0 0 180 180" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="emptyGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{Colors.PREMIUM_PRIMARY_START};stop-opacity:0.2" />
                <stop offset="100%" style="stop-color:{Colors.PREMIUM_PRIMARY_END};stop-opacity:0.1" />
            </linearGradient>
        </defs>
        <!-- Gráfico de barras vacío -->
        <rect x="30" y="120" width="20" height="40" rx="4" fill="{Colors.GRAY_200}"/>
        <rect x="65" y="90" width="20" height="70" rx="4" fill="{Colors.GRAY_200}"/>
        <rect x="100" y="110" width="20" height="50" rx="4" fill="{Colors.GRAY_200}"/>
        <rect x="135" y="80" width="20" height="80" rx="4" fill="{Colors.GRAY_200}"/>
        <line x1="20" y1="165" x2="165" y2="165" stroke="{Colors.GRAY_300}" stroke-width="2"/>
        <line x1="20" y1="75" x2="20" y2="165" stroke="{Colors.GRAY_300}" stroke-width="2"/>
    </svg>
    <h3 style="color: {Colors.GRAY_700}; font-family: {Typography.FONT_PRIMARY}; margin-top: {Spacing.LG};">
        Sin datos para mostrar
    </h3>
    <p style="color: {Colors.GRAY_500}; font-family: {Typography.FONT_PRIMARY}; margin-top: {Spacing.SM};">
        Los gráficos aparecerán cuando registres transacciones en este período
    </p>
</div>
"""

# === Función Helper ===
def show_empty_state(state_type: str) -> str:
    """
    Retorna el HTML del empty state solicitado.

    Args:
        state_type: 'transactions', 'budgets', 'chart'

    Returns:
        HTML string para usar con st.markdown(..., unsafe_allow_html=True)
    """

    states = {
        'transactions': EMPTY_TRANSACTIONS,
        'budgets': EMPTY_BUDGETS,
        'chart': EMPTY_CHART
    }

    return states.get(state_type, EMPTY_CHART)
```

### Uso en app.py:

```python
# app.py - Reemplazar st.info() con empty states
from utils.empty_states import show_empty_state

# ANTES:
# if not datos_mes['gastos_por_categoria']:
#     st.info("Sin datos de gastos")

# AHORA:
if not datos_mes['gastos_por_categoria']:
    st.markdown(show_empty_state('chart'), unsafe_allow_html=True)
```

---

## 3. QUICK WIN #3: Iconos SVG de Categorías

### Archivo: `/Users/daniel/mi_app_finanzas/utils/category_icons.py` (NUEVO)

```python
"""
Iconos SVG para categorías de gastos/ingresos.
Reemplazan emojis para consistencia cross-platform.
"""

from utils.design_tokens import Colors

# === CATEGORÍAS DE GASTO ===

ICON_FIJOS = f"""
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="gradFijos" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#5c6bc0"/>
            <stop offset="100%" style="stop-color:#7986cb"/>
        </linearGradient>
    </defs>
    <!-- Escudo (gastos fijos = protección/estabilidad) -->
    <path d="M12 2L4 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-8-3z"
          fill="url(#gradFijos)" opacity="0.2"/>
    <path d="M12 2L4 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-8-3z"
          stroke="url(#gradFijos)" stroke-width="2" fill="none"/>
</svg>
"""

ICON_DISFRUTE = f"""
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="gradDisfrute" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#f48fb1"/>
            <stop offset="100%" style="stop-color:#ce93d8"/>
        </linearGradient>
    </defs>
    <!-- Copa de cóctel (disfrute = ocio) -->
    <path d="M3 10h18L12 2 3 10z" fill="url(#gradDisfrute)" opacity="0.2"/>
    <path d="M3 10h18L12 2 3 10z" stroke="url(#gradDisfrute)" stroke-width="2" fill="none"/>
    <line x1="12" y1="10" x2="12" y2="20" stroke="url(#gradDisfrute)" stroke-width="2"/>
    <line x1="8" y1="20" x2="16" y2="20" stroke="url(#gradDisfrute)" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

ICON_EXTRAORDINARIOS = f"""
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="gradExtra" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#ffa726"/>
            <stop offset="100%" style="stop-color:#ffb74d"/>
        </linearGradient>
    </defs>
    <!-- Rayo (extraordinarios = imprevisto) -->
    <path d="M13 2L3 14h8l-1 8 10-12h-8l1-8z" fill="url(#gradExtra)" opacity="0.2"/>
    <path d="M13 2L3 14h8l-1 8 10-12h-8l1-8z" stroke="url(#gradExtra)" stroke-width="2" fill="none" stroke-linejoin="round"/>
</svg>
"""

ICON_COCHE = f"""
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="gradCoche" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#0a4c3e"/>
            <stop offset="100%" style="stop-color:#84cc16"/>
        </linearGradient>
    </defs>
    <!-- Coche eléctrico con rayo -->
    <path d="M5 11h14l-1.5-4H6.5L5 11z" fill="url(#gradCoche)" opacity="0.2"/>
    <rect x="3" y="11" width="18" height="6" rx="2" stroke="url(#gradCoche)" stroke-width="2" fill="none"/>
    <circle cx="7" cy="17" r="1.5" fill="url(#gradCoche)"/>
    <circle cx="17" cy="17" r="1.5" fill="url(#gradCoche)"/>
    <!-- Rayo eléctrico -->
    <path d="M12 5L10 9h2l-1 3" stroke="{Colors.PREMIUM_PRIMARY_END}" stroke-width="1.5" fill="none"/>
</svg>
"""

# === CATEGORÍAS DE INGRESO ===

ICON_NOMINA = f"""
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="gradNomina" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{Colors.SUCCESS_DARK}"/>
            <stop offset="100%" style="stop-color:{Colors.SUCCESS_LIGHT}"/>
        </linearGradient>
    </defs>
    <!-- Dinero/billete -->
    <rect x="2" y="8" width="20" height="10" rx="2" stroke="url(#gradNomina)" stroke-width="2" fill="none"/>
    <circle cx="12" cy="13" r="3" stroke="url(#gradNomina)" stroke-width="2" fill="url(#gradNomina)" opacity="0.2"/>
    <line x1="5" y1="11" x2="7" y2="11" stroke="url(#gradNomina)" stroke-width="2" stroke-linecap="round"/>
    <line x1="17" y1="15" x2="19" y2="15" stroke="url(#gradNomina)" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

ICON_REEMBOLSO = f"""
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="gradReembolso" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{Colors.INFO}"/>
            <stop offset="100%" style="stop-color:{Colors.INFO_LIGHT}"/>
        </linearGradient>
    </defs>
    <!-- Flecha circular (devolución) -->
    <path d="M12 2a10 10 0 0 1 8.66 5" stroke="url(#gradReembolso)" stroke-width="2" stroke-linecap="round" fill="none"/>
    <path d="M20.66 7a10 10 0 0 1-8.66 15" stroke="url(#gradReembolso)" stroke-width="2" stroke-linecap="round" fill="none"/>
    <path d="M12 22A10 10 0 0 1 3.34 17" stroke="url(#gradReembolso)" stroke-width="2" stroke-linecap="round" fill="none"/>
    <path d="M3.34 17L6 19l-2 3" stroke="url(#gradReembolso)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>
"""

# === ESTADOS / ACCIONES ===

ICON_SUCCESS = f"""
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="10" fill="{Colors.SUCCESS}" opacity="0.2"/>
    <circle cx="12" cy="12" r="10" stroke="{Colors.SUCCESS}" stroke-width="2" fill="none"/>
    <path d="M8 12l3 3 6-6" stroke="{Colors.SUCCESS}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>
"""

ICON_WARNING = f"""
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L2 20h20L12 2z" fill="{Colors.WARNING}" opacity="0.2"/>
    <path d="M12 2L2 20h20L12 2z" stroke="{Colors.WARNING}" stroke-width="2" fill="none"/>
    <line x1="12" y1="9" x2="12" y2="14" stroke="{Colors.WARNING}" stroke-width="2.5" stroke-linecap="round"/>
    <circle cx="12" cy="17" r="1" fill="{Colors.WARNING}"/>
</svg>
"""

ICON_ERROR = f"""
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="10" fill="{Colors.ERROR}" opacity="0.2"/>
    <circle cx="12" cy="12" r="10" stroke="{Colors.ERROR}" stroke-width="2" fill="none"/>
    <path d="M8 8l8 8M16 8l-8 8" stroke="{Colors.ERROR}" stroke-width="2.5" stroke-linecap="round"/>
</svg>
"""

# === FUNCIÓN HELPER ===

def get_category_icon(categoria: str, size: int = 24) -> str:
    """
    Obtiene el icono SVG de una categoría.

    Args:
        categoria: Nombre de la categoría
        size: Tamaño del icono en px (default 24)

    Returns:
        HTML string con SVG
    """

    icons = {
        'FIJOS': ICON_FIJOS,
        'DISFRUTE': ICON_DISFRUTE,
        'EXTRAORDINARIOS': ICON_EXTRAORDINARIOS,
        'COCHE_ELECTRICO': ICON_COCHE,
        'NOMINA': ICON_NOMINA,
        'INGRESO': ICON_NOMINA,
        'REEMBOLSO': ICON_REEMBOLSO,
        'SUCCESS': ICON_SUCCESS,
        'WARNING': ICON_WARNING,
        'ERROR': ICON_ERROR
    }

    svg = icons.get(categoria.upper(), ICON_FIJOS)

    # Ajustar tamaño si no es 24px
    if size != 24:
        svg = svg.replace('width="24"', f'width="{size}"')
        svg = svg.replace('height="24"', f'height="{size}"')

    return svg


def get_icon_inline(categoria: str, size: int = 20) -> str:
    """
    Icono inline (para usar dentro de texto).

    Args:
        categoria: Nombre categoría
        size: Tamaño en px

    Returns:
        HTML con SVG inline
    """

    icon = get_category_icon(categoria, size)

    return f'<span style="display: inline-block; vertical-align: middle;">{icon}</span>'
```

### Uso en app.py:

```python
# app.py
from utils.category_icons import get_category_icon, get_icon_inline

# Mostrar categoría con icono:
st.markdown(
    f"{get_icon_inline('FIJOS')} **Gastos Fijos**: {total_fijos:.2f} €",
    unsafe_allow_html=True
)

# En tarjetas de transacción:
icon = get_category_icon(transaccion['categoria'], size=32)
st.markdown(f"""
<div style="display: flex; align-items: center; gap: 1rem;">
    {icon}
    <div>{transaccion['concepto']}</div>
</div>
""", unsafe_allow_html=True)
```

---

## 4. QUICK WIN #4: Skeleton Screens

### CSS a añadir en app.py:

```python
# app.py - Añadir al bloque de st.markdown con CSS

SKELETON_CSS = """
<style>
/* === SKELETON LOADERS === */
@keyframes shimmer {
    0% {
        background-position: -1000px 0;
    }
    100% {
        background-position: 1000px 0;
    }
}

.skeleton {
    background: linear-gradient(
        90deg,
        #f0f2f6 0px,
        #e0e0e0 40px,
        #f0f2f6 80px
    );
    background-size: 1000px 100%;
    animation: shimmer 2s infinite linear;
}

.skeleton-card {
    border-radius: 1rem;
    height: 140px;
    margin-bottom: 1.5rem;
}

.skeleton-text {
    border-radius: 4px;
    height: 16px;
    margin: 12px 0;
}

.skeleton-text.large {
    height: 32px;
    width: 60%;
}

.skeleton-text.medium {
    height: 20px;
    width: 80%;
}

.skeleton-text.small {
    height: 14px;
    width: 40%;
}

.skeleton-metric {
    border-radius: 1rem;
    height: 120px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.skeleton-chart {
    border-radius: 1rem;
    height: 400px;
}
</style>
"""

st.markdown(SKELETON_CSS, unsafe_allow_html=True)
```

### Función helper para mostrar skeleton:

```python
# utils/loading.py - NUEVO ARCHIVO

from utils.design_tokens import Spacing

def show_skeleton_metrics(num_metrics: int = 4) -> str:
    """
    Skeleton para métricas mientras cargan.

    Args:
        num_metrics: Número de skeletons a mostrar

    Returns:
        HTML string
    """

    html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">'

    for _ in range(num_metrics):
        html += '''
        <div class="skeleton skeleton-metric">
            <div class="skeleton skeleton-text small" style="width: 40%; margin-bottom: 1rem;"></div>
            <div class="skeleton skeleton-text large" style="width: 60%;"></div>
        </div>
        '''

    html += '</div>'

    return html


def show_skeleton_chart() -> str:
    """Skeleton para gráfico mientras carga"""

    return '<div class="skeleton skeleton-chart"></div>'


def show_skeleton_table(rows: int = 5) -> str:
    """
    Skeleton para tabla.

    Args:
        rows: Número de filas skeleton

    Returns:
        HTML string
    """

    html = '<div style="margin: 1rem 0;">'

    # Header
    html += '<div class="skeleton skeleton-text" style="height: 40px; margin-bottom: 1rem;"></div>'

    # Rows
    for _ in range(rows):
        html += '<div class="skeleton skeleton-text" style="height: 24px; margin-bottom: 0.5rem;"></div>'

    html += '</div>'

    return html
```

### Uso en dashboard:

```python
# app.py - Dashboard

from utils.loading import show_skeleton_metrics, show_skeleton_chart

# Crear placeholder
metrics_placeholder = st.empty()
chart_placeholder = st.empty()

# Mostrar skeletons
with metrics_placeholder:
    st.markdown(show_skeleton_metrics(4), unsafe_allow_html=True)

with chart_placeholder:
    st.markdown(show_skeleton_chart(), unsafe_allow_html=True)

# Cargar datos (simular delay)
with st.spinner("Calculando métricas..."):
    datos_mes = metrics.calcular_totales_mes(mes, año)
    # ... cargar datos ...

# Limpiar skeletons
metrics_placeholder.empty()
chart_placeholder.empty()

# Mostrar datos reales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ingresos", f"{datos_mes['total_ingresos']:.2f} €")
# ...
```

---

## 5. QUICK WIN #5: Tablas Responsive

### Función helper:

```python
# utils/responsive.py - NUEVO ARCHIVO

import streamlit as st
import pandas as pd
from utils.design_tokens import Colors, Spacing, BorderRadius
from utils.category_icons import get_category_icon

def detect_device_type() -> str:
    """
    Detecta tipo de dispositivo basado en viewport.

    Returns:
        'mobile', 'tablet', o 'desktop'
    """

    # Inyectar JavaScript para detectar ancho
    js_code = """
    <script>
    const width = window.parent.document.documentElement.clientWidth;
    let device = 'desktop';
    if (width < 768) device = 'mobile';
    else if (width < 1024) device = 'tablet';

    // Guardar en sessionStorage
    window.parent.sessionStorage.setItem('device_type', device);
    </script>
    """

    st.components.v1.html(js_code, height=0)

    # Por ahora, default a desktop (mejorar con session_state)
    return 'desktop'


def mostrar_transacciones_responsive(df: pd.DataFrame):
    """
    Muestra transacciones como tabla en desktop, cards en mobile.

    Args:
        df: DataFrame con columnas: fecha, concepto, categoria, importe
    """

    device = st.session_state.get('device_type', 'desktop')

    if device == 'mobile':
        # MOBILE: Cards individuales
        for _, row in df.iterrows():
            icon = get_category_icon(row['categoria'], size=32)
            color = Colors.SUCCESS if row['importe'] > 0 else Colors.ERROR

            st.markdown(
                f"""
                <div style="
                    background: {Colors.PREMIUM_CARD_GRADIENT};
                    border-radius: {BorderRadius.LG};
                    padding: {Spacing.LG};
                    margin-bottom: {Spacing.MD};
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    border-left: 4px solid {color};
                ">
                    <div style="display: flex; justify-content: space-between; align-items: start; gap: 1rem;">
                        <div style="flex: 1;">
                            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                                {icon}
                                <strong style="font-size: 1rem; color: {Colors.GRAY_900};">
                                    {row['concepto'][:40]}{'...' if len(row['concepto']) > 40 else ''}
                                </strong>
                            </div>
                            <div style="font-size: 0.875rem; color: {Colors.GRAY_500};">
                                {row['fecha']} • {row['categoria']}
                            </div>
                        </div>
                        <div style="
                            font-size: 1.5rem;
                            font-weight: 700;
                            color: {color};
                            white-space: nowrap;
                        ">
                            {'+' if row['importe'] > 0 else ''}{row['importe']:.2f}€
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        # DESKTOP/TABLET: Tabla normal
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
                "concepto": st.column_config.TextColumn("Concepto", width="large"),
                "categoria": st.column_config.TextColumn("Categoría", width="small"),
                "importe": st.column_config.NumberColumn("Importe", format="%.2f €")
            }
        )
```

### Uso:

```python
# app.py - Sección de transacciones

from utils.responsive import mostrar_transacciones_responsive

# Obtener transacciones
transacciones = db_manager.obtener_transacciones(mes=mes, año=año, limit=20)
df = pd.DataFrame(transacciones)

# Mostrar responsive
mostrar_transacciones_responsive(df)
```

---

## 6. Template de Componente Completo

### Ejemplo: BudgetCard Premium

```python
# utils/components.py

from utils.design_tokens import Colors, Typography, Spacing, BorderRadius, get_budget_color
from utils.category_icons import get_category_icon

def budget_card_premium(
    categoria: str,
    limite: float,
    gastado: float,
    reembolsos: float = 0,
    clickable: bool = False,
    onclick_key: str = None
) -> None:
    """
    Card premium para presupuesto con progress bar animada.

    Args:
        categoria: Nombre de la categoría
        limite: Límite del presupuesto
        gastado: Cantidad gastada (bruto)
        reembolsos: Reembolsos aplicados
        clickable: Si True, convierte en botón clickeable
        onclick_key: Key único para el botón (si clickable=True)
    """

    import streamlit as st

    # Calcular métricas
    gastado_neto = gastado - reembolsos
    restante = limite - gastado_neto
    porcentaje = (gastado_neto / limite * 100) if limite > 0 else 0

    # Obtener colores según porcentaje
    emoji, color, bg_color = get_budget_color(porcentaje)
    icon = get_category_icon(categoria, size=32)

    # HTML del card
    html = f"""
    <div style="
        background: {Colors.PREMIUM_CARD_GRADIENT};
        border-radius: {BorderRadius.LG};
        padding: {Spacing.XL};
        margin-bottom: {Spacing.LG};
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border-left: 4px solid {color};
        transition: all 0.25s ease;
        {f'cursor: pointer;' if clickable else ''}
    " {'onmouseover="this.style.transform=\'translateY(-4px)\'; this.style.boxShadow=\'0 8px 12px rgba(0,0,0,0.12)\';" onmouseout="this.style.transform=\'translateY(0)\'; this.style.boxShadow=\'0 4px 6px rgba(0,0,0,0.07)\';"' if clickable else ''}>

        <!-- Header con icono y categoría -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: {Spacing.LG};">
            <div style="display: flex; align-items: center; gap: {Spacing.MD};">
                {icon}
                <div>
                    <h3 style="
                        font-size: {Typography.TEXT_LG};
                        font-weight: {Typography.WEIGHT_SEMIBOLD};
                        color: {Colors.GRAY_900};
                        margin: 0;
                    ">{emoji} {categoria}</h3>
                    {f'<small style="color: {Colors.GRAY_500}; font-size: {Typography.TEXT_SM};">Bruto: {gastado:.0f}€ - Reembolsos: {reembolsos:.0f}€</small>' if reembolsos > 0 else ''}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="
                    font-size: {Typography.TEXT_2XL};
                    font-weight: {Typography.WEIGHT_BOLD};
                    color: {color};
                ">{gastado_neto:.0f}€</div>
                <small style="color: {Colors.GRAY_500};">de {limite:.0f}€</small>
            </div>
        </div>

        <!-- Progress bar -->
        <div style="
            background: {Colors.GRAY_200};
            border-radius: {BorderRadius.FULL};
            height: 12px;
            overflow: hidden;
            margin-bottom: {Spacing.MD};
        ">
            <div style="
                width: {min(porcentaje, 100):.1f}%;
                background: linear-gradient(90deg, {color} 0%, {color}dd 100%);
                height: 100%;
                border-radius: {BorderRadius.FULL};
                transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
                animation: slideIn 0.8s ease-out;
            "></div>
        </div>

        <!-- Métricas inferiores -->
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: {Typography.TEXT_SM}; color: {Colors.GRAY_600};">
                    Restante:
                </span>
                <strong style="font-size: {Typography.TEXT_BASE}; color: {Colors.SUCCESS if restante > 0 else Colors.ERROR};">
                    {restante:.0f}€
                </strong>
            </div>
            <div>
                <span style="
                    font-size: {Typography.TEXT_BASE};
                    font-weight: {Typography.WEIGHT_BOLD};
                    color: {color};
                ">{porcentaje:.1f}%</span>
                <span style="font-size: {Typography.TEXT_SM}; color: {Colors.GRAY_500};"> usado</span>
            </div>
        </div>
    </div>

    <style>
    @keyframes slideIn {{
        from {{ width: 0%; }}
        to {{ width: {min(porcentaje, 100):.1f}%; }}
    }}
    </style>
    """

    if clickable and onclick_key:
        # Envolver en contenedor clickeable
        clicked = st.button(
            label="Ver detalle",
            key=onclick_key,
            help=f"Ver detalles de {categoria}",
            use_container_width=True
        )

        st.markdown(html, unsafe_allow_html=True)

        return clicked
    else:
        st.markdown(html, unsafe_allow_html=True)
        return None
```

### Uso del BudgetCard:

```python
# app.py - Mostrar presupuestos

from utils.components import budget_card_premium

resumen_presupuestos = db_manager.obtener_resumen_presupuestos(mes, año)

st.subheader("📊 Presupuestos del Mes")

for idx, presupuesto in enumerate(resumen_presupuestos):
    clicked = budget_card_premium(
        categoria=presupuesto['categoria'],
        limite=presupuesto['presupuesto'],
        gastado=presupuesto.get('gastado_bruto', presupuesto['gastado']),
        reembolsos=presupuesto.get('reembolsos_asignados', 0),
        clickable=True,
        onclick_key=f"budget_card_{idx}"
    )

    if clicked:
        st.info(f"Detalles de {presupuesto['categoria']}")
        # Mostrar dialog con transacciones de la categoría
```

---

## 7. Checklist de Implementación

### Preparación
- [ ] Leer ANALISIS_DISENO_UX.md completo
- [ ] Hacer backup de archivos antes de modificar
- [ ] Crear rama git: `git checkout -b feature/design-improvements`

### Quick Wins (Semana 1)
- [ ] QW#1: Crear `utils/plotly_theme.py`
- [ ] QW#1: Migrar `utils/visualizer.py` al nuevo tema
- [ ] QW#2: Crear `utils/empty_states.py`
- [ ] QW#2: Reemplazar `st.info()` con empty states en app.py
- [ ] QW#3: Crear `utils/category_icons.py`
- [ ] QW#3: Usar iconos en lugar de emojis
- [ ] QW#4: Añadir skeleton CSS a app.py
- [ ] QW#4: Crear `utils/loading.py`
- [ ] QW#4: Implementar skeletons en dashboard
- [ ] QW#5: Crear `utils/responsive.py`
- [ ] QW#5: Migrar tablas a función responsive

### Componentes (Semana 2-3)
- [ ] Crear `utils/components.py`
- [ ] Implementar `budget_card_premium()`
- [ ] Implementar `metric_card_premium()`
- [ ] Implementar `transaction_card_mobile()`
- [ ] Implementar `progress_bar_premium()`
- [ ] Migrar código existente a componentes

### Testing
- [ ] Probar en desktop (Chrome, Firefox, Safari)
- [ ] Probar en mobile (iOS Safari, Chrome Android)
- [ ] Probar en tablet
- [ ] Verificar accesibilidad (contraste, focus states)
- [ ] Performance check (tiempo de carga < 3s)

---

**Fin de ejemplos de código**
