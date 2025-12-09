# utils/visualizer.py
"""
Generador de visualizaciones con Plotly
Todos los gráficos usan el design system centralizado y el tema unificado
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.design_tokens import Colors, Typography
from utils.plotly_theme import (
    apply_theme_to_fig,
    create_themed_pie_chart,
    create_themed_line_chart,
    create_themed_bar_chart,
    CHART_COLORS_PREMIUM,
    CHART_COLORS_FINANCE
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

    # Usar función temática
    fig = create_themed_pie_chart(
        df,
        names='categoria',
        values='total',
        title="Distribución de Gastos por Categoría",
        hole=0.4,
        pull_first=True
    )

    # Personalizar leyenda
    fig.update_layout(
        legend_title_text='Categorías',
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

    # Línea de Ingresos (verde - éxito)
    fig.add_trace(go.Scatter(
        x=df_evolucion['periodo_str'],
        y=df_evolucion['ingresos'],
        mode='lines+markers',
        name='Ingresos',
        line=dict(color=CHART_COLORS_FINANCE['income'], width=3),
        marker=dict(
            size=10,
            color=Colors.SUCCESS_LIGHT,
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>Ingresos</b><br>%{x}<br>%{y:.2f} €<extra></extra>'
    ))

    # Línea de Gastos Netos (rojo - error)
    fig.add_trace(go.Scatter(
        x=df_evolucion['periodo_str'],
        y=df_evolucion['gastos_netos'].abs(),  # Valores absolutos
        mode='lines+markers',
        name='Gastos Netos',
        line=dict(color=CHART_COLORS_FINANCE['expense'], width=3),
        marker=dict(
            size=10,
            color=Colors.ERROR_LIGHT,
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>Gastos</b><br>%{x}<br>%{y:.2f} €<extra></extra>'
    ))

    # Línea de Balance (azul - primario, punteada)
    fig.add_trace(go.Scatter(
        x=df_evolucion['periodo_str'],
        y=df_evolucion['balance'],
        mode='lines+markers',
        name='Balance',
        line=dict(color=CHART_COLORS_FINANCE['balance'], width=3, dash='dot'),
        marker=dict(
            size=10,
            color=Colors.PRIMARY_LIGHT,
            line=dict(width=2, color='white')
        ),
        hovertemplate='<b>Balance</b><br>%{x}<br>%{y:.2f} €<extra></extra>'
    ))

    # Aplicar tema unificado
    apply_theme_to_fig(
        fig,
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
        marker_color=CHART_COLORS_FINANCE['income'],
        marker_line=dict(width=0),
        hovertemplate='<b>Ingresos</b><br>%{x}<br>%{y:.2f} €<extra></extra>'
    ))

    # Barras de Gastos Netos (rojo)
    fig.add_trace(go.Bar(
        x=df_evolucion['mes_nombre'],
        y=df_evolucion['gastos_netos'].abs(),  # Valores absolutos
        name='Gastos Netos',
        marker_color=CHART_COLORS_FINANCE['expense'],
        marker_line=dict(width=0),
        hovertemplate='<b>Gastos</b><br>%{x}<br>%{y:.2f} €<extra></extra>'
    ))

    # Aplicar tema unificado
    apply_theme_to_fig(
        fig,
        barmode='group',
        title="Resumen Mensual del Año",
        xaxis_title="Mes",
        yaxis_title="Importe (€)",
        height=500,
        bargap=0.15,
        bargroupgap=0.1
    )

    return fig
