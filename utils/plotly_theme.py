# utils/plotly_theme.py
"""
Sistema unificado de temas para gráficas Plotly
Integrado con el design system (design_tokens.py)

Este módulo proporciona:
- Tema global consistente para todas las gráficas
- Funciones helper para crear gráficas temáticas
- Configuración centralizada de colores, fuentes, ejes, etc.

Uso:
    from utils.plotly_theme import apply_theme_to_fig, create_themed_line_chart

    # Aplicar tema a figura existente
    fig = px.bar(df, x='mes', y='total')
    apply_theme_to_fig(fig)

    # O crear gráfica con tema desde cero
    fig = create_themed_bar_chart(df, x='mes', y='total', title='Ventas Mensuales')
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, Dict, Any, List
from utils.design_tokens import Colors, Typography, Spacing, BorderRadius, Transitions


# ========== PALETA DE COLORES PARA GRÁFICAS ==========

CHART_COLORS_PREMIUM = [
    Colors.PREMIUM_TEAL_START,      # Verde oscuro (principal)
    Colors.PREMIUM_CORAL_START,     # Rosa coral (secundario)
    Colors.PREMIUM_PRIMARY_START,   # Verde bosque (terciario)
    Colors.PREMIUM_GOLD_START,      # Dorado (acento)
    Colors.PREMIUM_SKY_START,       # Azul cielo (acento)
    Colors.PREMIUM_TEAL_END,        # Lima brillante
    Colors.PREMIUM_CORAL_END,       # Amarillo suave
]

# Colores semánticos para finanzas
CHART_COLORS_FINANCE = {
    'income': Colors.SUCCESS,           # Verde para ingresos
    'expense': Colors.ERROR,            # Rojo para gastos
    'balance': Colors.PRIMARY,          # Azul para balance
    'positive': Colors.SUCCESS,         # Positivo
    'negative': Colors.ERROR,           # Negativo
    'neutral': Colors.GRAY_500,         # Neutral
    'warning': Colors.WARNING,          # Advertencia
}


# ========== TEMA BASE DE PLOTLY ==========

def get_unified_plotly_theme() -> Dict[str, Any]:
    """
    Retorna el tema unificado de Plotly como diccionario de configuración.

    Este tema se aplica a todas las gráficas de la aplicación para mantener
    consistencia visual con el design system.

    Returns:
        Dict con la configuración completa del tema

    Example:
        >>> theme = get_unified_plotly_theme()
        >>> fig.update_layout(**theme)
    """
    return {
        # === FUENTES ===
        'font': {
            'family': Typography.FONT_PRIMARY,
            'size': 14,
            'color': Colors.GRAY_900
        },

        # === FONDOS ===
        'plot_bgcolor': Colors.BG_PRIMARY,      # Fondo del área de gráfica
        'paper_bgcolor': Colors.BG_PRIMARY,     # Fondo del papel (todo el chart)

        # === PALETA DE COLORES ===
        'colorway': CHART_COLORS_PREMIUM,

        # === TÍTULO ===
        'title': {
            'font': {
                'size': 20,
                'color': Colors.GRAY_900,
                'family': Typography.FONT_PRIMARY
            },
            'x': 0.5,           # Centrado horizontal
            'xanchor': 'center',
            'y': 0.95,          # Posición superior
            'yanchor': 'top',
            'pad': {'b': 15, 't': 10}
        },

        # === EJE X ===
        'xaxis': {
            'gridcolor': Colors.GRAY_200,
            'gridwidth': 1,
            'linecolor': Colors.GRAY_300,
            'linewidth': 1.5,
            'zerolinecolor': Colors.GRAY_400,
            'zerolinewidth': 2,
            'title': {
                'font': {
                    'size': 14,
                    'color': Colors.GRAY_700,
                    'family': Typography.FONT_PRIMARY
                },
                'standoff': 10
            },
            'tickfont': {
                'size': 12,
                'color': Colors.GRAY_600
            },
            'showgrid': True,
            'showline': True,
            'zeroline': True,
        },

        # === EJE Y ===
        'yaxis': {
            'gridcolor': Colors.GRAY_200,
            'gridwidth': 1,
            'linecolor': Colors.GRAY_300,
            'linewidth': 1.5,
            'zerolinecolor': Colors.GRAY_400,
            'zerolinewidth': 2,
            'title': {
                'font': {
                    'size': 14,
                    'color': Colors.GRAY_700,
                    'family': Typography.FONT_PRIMARY
                },
                'standoff': 10
            },
            'tickfont': {
                'size': 12,
                'color': Colors.GRAY_600
            },
            'showgrid': True,
            'showline': True,
            'zeroline': True,
        },

        # === LEYENDA ===
        'legend': {
            'bgcolor': Colors.BG_SECONDARY,
            'bordercolor': Colors.GRAY_300,
            'borderwidth': 1,
            'font': {
                'size': 12,
                'color': Colors.GRAY_700,
                'family': Typography.FONT_PRIMARY
            },
            'orientation': 'v',
            'yanchor': 'top',
            'y': 0.99,
            'xanchor': 'left',
            'x': 1.02
        },

        # === TOOLTIPS (Hover) ===
        'hoverlabel': {
            'bgcolor': Colors.GRAY_900,
            'bordercolor': Colors.GRAY_700,
            'font': {
                'size': 13,
                'family': Typography.FONT_PRIMARY,
                'color': 'white'
            },
            'align': 'left'
        },

        # === MÁRGENES ===
        'margin': {
            'l': 60,    # izquierda
            'r': 40,    # derecha
            't': 80,    # arriba (espacio para título)
            'b': 60     # abajo
        },

        # === ANIMACIONES ===
        'transition': {
            'duration': 250,
            'easing': 'cubic-in-out'
        },

        # === INTERACTIVIDAD ===
        'hovermode': 'closest',
        'dragmode': 'zoom',

        # === OTROS ===
        'showlegend': True,
        'height': 450,  # Altura por defecto
    }


# ========== PLANTILLA REUTILIZABLE ==========

PLOTLY_TEMPLATE = go.layout.Template(
    layout=get_unified_plotly_theme()
)


# ========== FUNCIÓN PRINCIPAL: APLICAR TEMA ==========

def apply_theme_to_fig(fig: go.Figure, **custom_layout) -> go.Figure:
    """
    Aplica el tema unificado a una figura de Plotly existente.

    Args:
        fig: Figura de Plotly (go.Figure o resultado de px.*)
        **custom_layout: Parámetros adicionales para personalizar el layout

    Returns:
        Figura con el tema aplicado (modifica in-place y retorna)

    Example:
        >>> fig = px.bar(df, x='mes', y='total')
        >>> apply_theme_to_fig(fig, title='Ventas por Mes', height=500)
        >>> st.plotly_chart(fig)
    """
    theme = get_unified_plotly_theme()

    # Merge custom layout con el tema
    theme.update(custom_layout)

    # Aplicar tema
    fig.update_layout(**theme)

    return fig


# ========== FUNCIONES HELPER: CREAR GRÁFICAS TEMÁTICAS ==========

def create_themed_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str | List[str],
    title: Optional[str] = None,
    labels: Optional[Dict[str, str]] = None,
    color: Optional[str] = None,
    line_shape: str = 'linear',
    markers: bool = True,
    fill: bool = False,
    **kwargs
) -> go.Figure:
    """
    Crea un gráfico de líneas con el tema unificado.

    Args:
        df: DataFrame con los datos
        x: Nombre de la columna para el eje X
        y: Nombre de la columna (o lista de columnas) para el eje Y
        title: Título del gráfico
        labels: Dict para renombrar ejes/leyendas
        color: Columna para colorear líneas diferentes
        line_shape: 'linear', 'spline', 'hv', 'vh', 'hvh', 'vhv'
        markers: Mostrar marcadores en los puntos
        fill: Rellenar área bajo la línea
        **kwargs: Argumentos adicionales para px.line()

    Returns:
        Figura de Plotly con tema aplicado

    Example:
        >>> fig = create_themed_line_chart(
        ...     df, x='fecha', y='saldo',
        ...     title='Evolución del Saldo',
        ...     markers=True, fill=True
        ... )
    """
    # Configurar modo
    mode = 'lines+markers' if markers else 'lines'

    # Crear gráfica base
    fig = px.line(
        df, x=x, y=y,
        labels=labels,
        color=color,
        **kwargs
    )

    # Personalizar líneas
    fig.update_traces(
        mode=mode,
        line_shape=line_shape,
        line=dict(width=3),
        marker=dict(
            size=8,
            line=dict(width=2, color='white')
        )
    )

    # Rellenar área si se solicita
    if fill and not color:  # Solo si hay una sola línea
        fig.update_traces(
            fill='tozeroy',
            fillcolor=f'rgba(10, 76, 62, 0.1)'  # Verde teal con alpha
        )

    # Aplicar tema
    apply_theme_to_fig(fig, title=title)

    return fig


def create_themed_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str | List[str],
    title: Optional[str] = None,
    labels: Optional[Dict[str, str]] = None,
    color: Optional[str] = None,
    orientation: str = 'v',
    barmode: str = 'group',
    text_auto: bool = False,
    **kwargs
) -> go.Figure:
    """
    Crea un gráfico de barras con el tema unificado.

    Args:
        df: DataFrame con los datos
        x: Nombre de la columna para el eje X
        y: Nombre de la columna (o lista de columnas) para el eje Y
        title: Título del gráfico
        labels: Dict para renombrar ejes/leyendas
        color: Columna para colorear barras diferentes
        orientation: 'v' (vertical) o 'h' (horizontal)
        barmode: 'group' (agrupadas), 'stack' (apiladas), 'relative'
        text_auto: Mostrar valores en las barras automáticamente
        **kwargs: Argumentos adicionales para px.bar()

    Returns:
        Figura de Plotly con tema aplicado

    Example:
        >>> fig = create_themed_bar_chart(
        ...     df, x='categoria', y='total',
        ...     title='Gastos por Categoría',
        ...     text_auto=True
        ... )
    """
    # Crear gráfica base
    fig = px.bar(
        df, x=x, y=y,
        labels=labels,
        color=color,
        orientation=orientation,
        barmode=barmode,
        text_auto=text_auto,
        **kwargs
    )

    # Personalizar barras
    fig.update_traces(
        marker_line=dict(width=0),  # Sin borde
        textposition='auto'
    )

    # Espaciado entre barras
    gap = 0.15 if barmode == 'group' else 0.1

    # Aplicar tema
    apply_theme_to_fig(
        fig,
        title=title,
        bargap=gap,
        bargroupgap=0.1
    )

    return fig


def create_themed_pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: Optional[str] = None,
    hole: float = 0.4,
    pull_first: bool = True,
    **kwargs
) -> go.Figure:
    """
    Crea un gráfico de torta/donut con el tema unificado.

    Args:
        df: DataFrame con los datos
        names: Columna con los nombres de las categorías
        values: Columna con los valores
        title: Título del gráfico
        hole: Tamaño del agujero central (0 = pie, 0.4 = donut)
        pull_first: Destacar el primer sector ligeramente
        **kwargs: Argumentos adicionales para px.pie()

    Returns:
        Figura de Plotly con tema aplicado

    Example:
        >>> fig = create_themed_pie_chart(
        ...     df, names='categoria', values='total',
        ...     title='Distribución de Gastos',
        ...     hole=0.4
        ... )
    """
    # Crear gráfica base
    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=hole,
        color_discrete_sequence=CHART_COLORS_PREMIUM,
        **kwargs
    )

    # Personalizar sectores
    pull = [0.05] + [0] * (len(df) - 1) if pull_first else None

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=13,
        textfont_color='white',
        marker=dict(
            line=dict(color=Colors.BG_PRIMARY, width=3)  # Separación entre sectores
        ),
        hovertemplate='<b>%{label}</b><br>Importe: %{value:.2f} €<br>Porcentaje: %{percent}<extra></extra>',
        pull=pull
    )

    # Aplicar tema
    apply_theme_to_fig(fig, title=title, height=450)

    return fig


def create_themed_scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: Optional[str] = None,
    labels: Optional[Dict[str, str]] = None,
    color: Optional[str] = None,
    size: Optional[str] = None,
    trendline: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """
    Crea un gráfico de dispersión (scatter) con el tema unificado.

    Args:
        df: DataFrame con los datos
        x: Nombre de la columna para el eje X
        y: Nombre de la columna para el eje Y
        title: Título del gráfico
        labels: Dict para renombrar ejes/leyendas
        color: Columna para colorear puntos
        size: Columna para tamaño de puntos
        trendline: 'ols' (regresión lineal), 'lowess', etc.
        **kwargs: Argumentos adicionales para px.scatter()

    Returns:
        Figura de Plotly con tema aplicado

    Example:
        >>> fig = create_themed_scatter_chart(
        ...     df, x='km', y='coste',
        ...     title='Coste vs Kilómetros',
        ...     trendline='ols'
        ... )
    """
    # Crear gráfica base
    fig = px.scatter(
        df, x=x, y=y,
        labels=labels,
        color=color,
        size=size,
        trendline=trendline,
        **kwargs
    )

    # Personalizar puntos
    fig.update_traces(
        marker=dict(
            size=10,
            line=dict(width=1.5, color='white'),
            opacity=0.8
        )
    )

    # Aplicar tema
    apply_theme_to_fig(fig, title=title)

    return fig


def create_themed_area_chart(
    df: pd.DataFrame,
    x: str,
    y: str | List[str],
    title: Optional[str] = None,
    labels: Optional[Dict[str, str]] = None,
    color: Optional[str] = None,
    groupnorm: Optional[str] = None,
    **kwargs
) -> go.Figure:
    """
    Crea un gráfico de área con el tema unificado.

    Args:
        df: DataFrame con los datos
        x: Nombre de la columna para el eje X
        y: Nombre de la columna (o lista de columnas) para el eje Y
        title: Título del gráfico
        labels: Dict para renombrar ejes/leyendas
        color: Columna para colorear áreas diferentes
        groupnorm: 'percent' para normalizar a 100%, None para valores absolutos
        **kwargs: Argumentos adicionales para px.area()

    Returns:
        Figura de Plotly con tema aplicado

    Example:
        >>> fig = create_themed_area_chart(
        ...     df, x='mes', y=['ingresos', 'gastos'],
        ...     title='Evolución Ingresos vs Gastos'
        ... )
    """
    # Crear gráfica base
    fig = px.area(
        df, x=x, y=y,
        labels=labels,
        color=color,
        groupnorm=groupnorm,
        **kwargs
    )

    # Personalizar áreas
    fig.update_traces(
        line=dict(width=2),
        opacity=0.6
    )

    # Aplicar tema
    apply_theme_to_fig(fig, title=title)

    return fig


# ========== FUNCIONES AUXILIARES ==========

def add_reference_line(
    fig: go.Figure,
    value: float,
    orientation: str = 'h',
    line_dash: str = 'dash',
    line_color: str = None,
    annotation: Optional[str] = None,
    annotation_position: str = 'right'
) -> go.Figure:
    """
    Añade una línea de referencia horizontal o vertical a la figura.

    Args:
        fig: Figura de Plotly
        value: Valor donde dibujar la línea
        orientation: 'h' (horizontal) o 'v' (vertical)
        line_dash: 'solid', 'dash', 'dot', 'dashdot'
        line_color: Color de la línea (usa Colors.GRAY_500 por defecto)
        annotation: Texto de anotación
        annotation_position: 'left', 'right', 'top', 'bottom'

    Returns:
        Figura modificada

    Example:
        >>> fig = create_themed_line_chart(df, x='mes', y='balance')
        >>> add_reference_line(fig, value=0, annotation='Break Even')
    """
    if line_color is None:
        line_color = Colors.GRAY_500

    if orientation == 'h':
        fig.add_hline(
            y=value,
            line_dash=line_dash,
            line_color=line_color,
            opacity=0.6,
            annotation_text=annotation,
            annotation_position=annotation_position
        )
    else:  # vertical
        fig.add_vline(
            x=value,
            line_dash=line_dash,
            line_color=line_color,
            opacity=0.6,
            annotation_text=annotation,
            annotation_position=annotation_position
        )

    return fig


def set_finance_colors(fig: go.Figure, trace_names: Dict[str, str]) -> go.Figure:
    """
    Aplica colores semánticos de finanzas a trazas específicas.

    Args:
        fig: Figura de Plotly
        trace_names: Dict mapeando nombre de traza -> tipo financiero
                    Tipos: 'income', 'expense', 'balance', 'positive', 'negative'

    Returns:
        Figura modificada

    Example:
        >>> fig = create_themed_bar_chart(df, x='mes', y=['ingresos', 'gastos'])
        >>> set_finance_colors(fig, {'ingresos': 'income', 'gastos': 'expense'})
    """
    for trace in fig.data:
        trace_name = trace.name
        if trace_name in trace_names:
            finance_type = trace_names[trace_name]
            color = CHART_COLORS_FINANCE.get(finance_type, Colors.PRIMARY)

            # Aplicar color según el tipo de traza
            if hasattr(trace, 'marker'):
                trace.marker.color = color
            if hasattr(trace, 'line'):
                trace.line.color = color

    return fig


def enable_responsive_layout(fig: go.Figure) -> go.Figure:
    """
    Habilita layout responsivo para móviles.

    Args:
        fig: Figura de Plotly

    Returns:
        Figura modificada con configuración responsiva

    Example:
        >>> fig = create_themed_bar_chart(df, x='mes', y='total')
        >>> enable_responsive_layout(fig)
    """
    fig.update_layout(
        autosize=True,
        margin=dict(l=40, r=20, t=60, b=40),
        # Ajustar fuentes en móvil
        font=dict(size=12),
        title=dict(font=dict(size=16)),
        # Leyenda más compacta
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        )
    )

    return fig
