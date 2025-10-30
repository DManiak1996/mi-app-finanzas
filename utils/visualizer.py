
# utils/visualizer.py

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def grafico_distribucion_gastos(gastos_por_categoria):
    """
    Genera un gráfico de torta (pie chart) con la distribución de gastos por categoría.
    """
    if not gastos_por_categoria:
        return None

    # Convertir los gastos a valores positivos para el gráfico
    data = {
        "categoria": list(gastos_por_categoria.keys()),
        "total": [-v for v in gastos_por_categoria.values()] 
    }
    df = pd.DataFrame(data)

    fig = px.pie(
        df,
        names='categoria',
        values='total',
        title="Distribución de Gastos por Categoría",
        hole=0.3 # Para un efecto donut
    )
    
    fig.update_traces(textinfo='percent', textposition='inside')
    fig.update_layout(showlegend=True, legend_title_text='Categorías')
    
    return fig

def grafico_evolucion_mensual(df_evolucion):
    """
    Genera un gráfico de líneas con la evolución de ingresos, gastos y balance.
    """
    if df_evolucion.empty:
        return None

    fig = go.Figure()

    # Formatear el período para el eje X
    df_evolucion['periodo_str'] = df_evolucion['periodo'].dt.strftime('%Y-%m')

    fig.add_trace(go.Scatter(
        x=df_evolucion['periodo_str'],
        y=df_evolucion['ingresos'],
        mode='lines+markers',
        name='Ingresos',
        marker=dict(color='green')
    ))

    # Usar valores absolutos para el gráfico de gastos
    fig.add_trace(go.Scatter(
        x=df_evolucion['periodo_str'],
        y=df_evolucion['gastos'].abs(),
        mode='lines+markers',
        name='Gastos',
        marker=dict(color='red')
    ))

    fig.add_trace(go.Scatter(
        x=df_evolucion['periodo_str'],
        y=df_evolucion['balance'],
        mode='lines+markers',
        name='Balance',
        marker=dict(color='blue')
    ))

    fig.update_layout(
        title="Evolución Mensual (Ingresos, Gastos, Balance)",
        xaxis_title="Mes",
        yaxis_title="Importe (€)",
        legend_title="Métrica"
    )

    return fig

def grafico_evolucion_anual(df_evolucion, nombres_meses):
    """
    Genera un gráfico de barras con la evolución mensual de ingresos y gastos para un año.
    """
    if df_evolucion.empty:
        return None

    df_evolucion['mes_nombre'] = df_evolucion.index.map(nombres_meses)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_evolucion['mes_nombre'],
        y=df_evolucion['ingresos'],
        name='Ingresos',
        marker_color='green'
    ))

    fig.add_trace(go.Bar(
        x=df_evolucion['mes_nombre'],
        y=df_evolucion['gastos'].abs(),
        name='Gastos',
        marker_color='red'
    ))

    fig.update_layout(
        barmode='group',
        title="Resumen Mensual del Año",
        xaxis_title="Mes",
        yaxis_title="Importe (€)"
    )
    return fig
