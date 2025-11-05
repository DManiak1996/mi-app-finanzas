# utils/visualizer.py
"""
Generador de visualizaciones con Plotly
Todos los gráficos usan el design system centralizado
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.design_tokens import Colors, Typography

# Colores premium para gráficos (gradientes simulados con colores vibrantes)
CHART_COLORS_PREMIUM = [
    Colors.PREMIUM_TEAL_START,      # Verde menta (ingresos)
    Colors.PREMIUM_CORAL_START,     # Coral (gastos)
    Colors.PREMIUM_PRIMARY_START,   # Violeta (balance)
    Colors.PREMIUM_GOLD_START,      # Dorado (extras)
    Colors.PREMIUM_SKY_START,       # Azul cielo
    Colors.PREMIUM_TEAL_END,
    Colors.PREMIUM_CORAL_END,
]


# === CONFIGURACIÓN GLOBAL DE PLOTLY ===
PLOTLY_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
            size=14,
            color=Colors.GRAY_900
        ),
        plot_bgcolor=Colors.BG_PRIMARY,
        paper_bgcolor=Colors.BG_PRIMARY,
        colorway=CHART_COLORS_PREMIUM,
        title=dict(
            font=dict(size=18, color=Colors.GRAY_900),
            x=0.5,  # Centrado
            xanchor='center',
            pad=dict(b=20)
        ),
        xaxis=dict(
            gridcolor=Colors.GRAY_200,
            linecolor=Colors.GRAY_300,
            zerolinecolor=Colors.GRAY_300,
            title_font=dict(size=14, color=Colors.GRAY_700),
            tickfont=dict(size=12, color=Colors.GRAY_600)
        ),
        yaxis=dict(
            gridcolor=Colors.GRAY_200,
            linecolor=Colors.GRAY_300,
            zerolinecolor=Colors.GRAY_300,
            title_font=dict(size=14, color=Colors.GRAY_700),
            tickfont=dict(size=12, color=Colors.GRAY_600)
        ),
        legend=dict(
            bgcolor=Colors.BG_SECONDARY,
            bordercolor=Colors.GRAY_300,
            borderwidth=1,
            font=dict(size=12, color=Colors.GRAY_700)
        ),
        hoverlabel=dict(
            bgcolor=Colors.GRAY_900,
            font_size=13,
            font_family="Inter, -apple-system, sans-serif",
            font_color="white"
        ),
        margin=dict(l=60, r=40, t=60, b=60)
    )
)


def grafico_distribucion_gastos(gastos_por_categoria):
    """
    Gráfico de torta (donut) con distribución de gastos por categoría

    Args:
        gastos_por_categoria: Dict con {categoria: importe}

    Returns:
        Figura de Plotly o None si no hay datos
    """
    if not gastos_por_categoria:
        return None

    # Convertir a valores absolutos para el gráfico
    data = {
        "categoria": list(gastos_por_categoria.keys()),
        "total": [abs(v) for v in gastos_por_categoria.values()]  # Valores absolutos
    }
    df = pd.DataFrame(data)

    fig = px.pie(
        df,
        names='categoria',
        values='total',
        title="Distribución de Gastos por Categoría",
        hole=0.4,  # Donut más pronunciado
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=[
            Colors.PREMIUM_CORAL_START,    # DISFRUTE / Primer sector
            Colors.PREMIUM_PRIMARY_START,  # FIJOS
            Colors.PREMIUM_GOLD_START,     # EXTRAORDINARIOS
            Colors.PREMIUM_SKY_START,      # COCHE_ELECTRICO
            Colors.PRIMARY_LIGHT,
            Colors.ERROR_LIGHT,
        ]
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        textfont_size=14,
        textfont_color='white',
        marker=dict(
            line=dict(color=Colors.BG_PRIMARY, width=3)  # Separación entre sectores
        ),
        hovertemplate='<b>%{label}</b><br>Importe: %{value:.2f} €<br>Porcentaje: %{percent}<extra></extra>',
        pull=[0.05, 0, 0, 0, 0, 0]  # Destacar primer sector ligeramente
    )

    fig.update_layout(
        showlegend=True,
        legend_title_text='Categorías',
        height=450,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        )
    )

    return fig


def grafico_evolucion_mensual(df_evolucion):
    """
    Gráfico de líneas con evolución de ingresos, gastos y balance

    Args:
        df_evolucion: DataFrame con columnas [periodo, ingresos, gastos_netos, balance]

    Returns:
        Figura de Plotly o None si no hay datos
    """
    if df_evolucion.empty:
        return None

    fig = go.Figure()

    # Formatear el período para el eje X
    df_evolucion['periodo_str'] = df_evolucion['periodo'].dt.strftime('%Y-%m')

    # Línea de Ingresos (verde menta premium)
    fig.add_trace(go.Scatter(
        x=df_evolucion['periodo_str'],
        y=df_evolucion['ingresos'],
        mode='lines+markers',
        name='Ingresos',
        line=dict(color=Colors.PREMIUM_TEAL_START, width=3),
        marker=dict(
            size=10,
            color=Colors.PREMIUM_TEAL_END,
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>Ingresos</b><br>%{x}<br>%{y:.2f} €<extra></extra>'
    ))

    # Línea de Gastos Netos (coral premium)
    fig.add_trace(go.Scatter(
        x=df_evolucion['periodo_str'],
        y=df_evolucion['gastos_netos'].abs(),  # Valores absolutos
        mode='lines+markers',
        name='Gastos Netos',
        line=dict(color=Colors.PREMIUM_CORAL_START, width=3),
        marker=dict(
            size=10,
            color=Colors.PREMIUM_CORAL_END,
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>Gastos</b><br>%{x}<br>%{y:.2f} €<extra></extra>'
    ))

    # Línea de Balance (violeta premium, punteada)
    fig.add_trace(go.Scatter(
        x=df_evolucion['periodo_str'],
        y=df_evolucion['balance'],
        mode='lines+markers',
        name='Balance',
        line=dict(color=Colors.PREMIUM_PRIMARY_START, width=3, dash='dot'),
        marker=dict(
            size=10,
            color=Colors.PREMIUM_PRIMARY_END,
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>Balance</b><br>%{x}<br>%{y:.2f} €<extra></extra>'
    ))

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title="Evolución Mensual (Ingresos, Gastos, Balance)",
        xaxis_title="Mes",
        yaxis_title="Importe (€)",
        legend_title="Métrica",
        hovermode='x unified',
        height=500
    )

    return fig


def grafico_evolucion_anual(df_evolucion, nombres_meses):
    """
    Gráfico de barras agrupadas con evolución anual

    Args:
        df_evolucion: DataFrame con índice mes (1-12) y columnas [ingresos, gastos_netos]
        nombres_meses: Dict para mapear número de mes a nombre

    Returns:
        Figura de Plotly o None si no hay datos
    """
    if df_evolucion.empty:
        return None

    df_evolucion['mes_nombre'] = df_evolucion.index.map(nombres_meses)

    fig = go.Figure()

    # Barras de Ingresos (verde)
    fig.add_trace(go.Bar(
        x=df_evolucion['mes_nombre'],
        y=df_evolucion['ingresos'],
        name='Ingresos',
        marker_color=Colors.CHART_INCOME,
        marker_line=dict(width=0),
        hovertemplate='<b>Ingresos</b><br>%{x}<br>%{y:.2f} €<extra></extra>'
    ))

    # Barras de Gastos Netos (rojo)
    fig.add_trace(go.Bar(
        x=df_evolucion['mes_nombre'],
        y=df_evolucion['gastos_netos'].abs(),  # Valores absolutos
        name='Gastos Netos',
        marker_color=Colors.CHART_EXPENSE,
        marker_line=dict(width=0),
        hovertemplate='<b>Gastos</b><br>%{x}<br>%{y:.2f} €<extra></extra>'
    ))

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        barmode='group',
        title="Resumen Mensual del Año",
        xaxis_title="Mes",
        yaxis_title="Importe (€)",
        height=500,
        bargap=0.15,  # Espacio entre grupos
        bargroupgap=0.1  # Espacio dentro de grupos
    )

    return fig
