#!/usr/bin/env python3
"""
Ejemplos de uso del tema unificado de Plotly
Ejecutar desde el root del proyecto: python -m docs.PLOTLY_THEME_EXAMPLES
"""

import sys
import os

# Añadir el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import plotly.graph_objects as go
from utils.plotly_theme import (
    create_themed_line_chart,
    create_themed_bar_chart,
    create_themed_pie_chart,
    create_themed_scatter_chart,
    create_themed_area_chart,
    apply_theme_to_fig,
    add_reference_line,
    CHART_COLORS_FINANCE
)

# ========== DATOS DE EJEMPLO ==========

# Datos mensuales
df_mensual = pd.DataFrame({
    'mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
    'ingresos': [2500, 2600, 2550, 2700, 2650, 2800],
    'gastos': [1800, 1900, 1750, 2000, 1850, 1950],
    'balance': [700, 700, 800, 700, 800, 850]
})

# Datos de categorías
df_categorias = pd.DataFrame({
    'categoria': ['DISFRUTE', 'FIJOS', 'EXTRAORDINARIOS', 'COCHE_ELECTRICO'],
    'total': [450, 800, 200, 350]
})

# Datos de evolución
df_evolucion = pd.DataFrame({
    'fecha': pd.date_range('2024-01-01', periods=30, freq='D'),
    'saldo': [1000 + i*10 + (-1)**i * 50 for i in range(30)]
})

# Datos scatter
df_km = pd.DataFrame({
    'km': [100, 150, 200, 250, 300, 350, 400],
    'coste': [8, 11, 15, 18, 22, 25, 29],
    'kwh': [16, 24, 32, 40, 48, 56, 64]
})


# ========== EJEMPLO 1: GRÁFICO DE LÍNEAS ==========

def ejemplo_lineas():
    """Gráfico de líneas con evolución del saldo"""
    print("\n1. GRÁFICO DE LÍNEAS")
    print("-" * 50)

    fig = create_themed_line_chart(
        df_evolucion,
        x='fecha',
        y='saldo',
        title='Evolución del Saldo Diario',
        labels={'fecha': 'Fecha', 'saldo': 'Saldo (€)'},
        markers=True,
        fill=True
    )

    # Añadir línea de referencia
    add_reference_line(
        fig,
        value=1000,
        annotation='Saldo Inicial',
        annotation_position='left'
    )

    print("✓ Gráfico de líneas creado")
    print(f"  - Puntos: {len(df_evolucion)}")
    print(f"  - Rango: {df_evolucion['saldo'].min():.0f}€ - {df_evolucion['saldo'].max():.0f}€")

    # Para guardar: fig.write_html('evolucion_saldo.html')
    return fig


# ========== EJEMPLO 2: GRÁFICO DE BARRAS ==========

def ejemplo_barras():
    """Gráfico de barras con ingresos y gastos"""
    print("\n2. GRÁFICO DE BARRAS")
    print("-" * 50)

    # Preparar datos para barras agrupadas
    df_melted = df_mensual.melt(
        id_vars='mes',
        value_vars=['ingresos', 'gastos'],
        var_name='tipo',
        value_name='importe'
    )

    fig = create_themed_bar_chart(
        df_melted,
        x='mes',
        y='importe',
        color='tipo',
        title='Ingresos vs Gastos Mensuales',
        barmode='group',
        text_auto=True
    )

    print("✓ Gráfico de barras creado")
    print(f"  - Meses: {len(df_mensual)}")
    print(f"  - Total ingresos: {df_mensual['ingresos'].sum():.0f}€")
    print(f"  - Total gastos: {df_mensual['gastos'].sum():.0f}€")

    return fig


# ========== EJEMPLO 3: GRÁFICO DE PIE/DONUT ==========

def ejemplo_pie():
    """Gráfico de pie/donut con distribución de gastos"""
    print("\n3. GRÁFICO DE PIE/DONUT")
    print("-" * 50)

    fig = create_themed_pie_chart(
        df_categorias,
        names='categoria',
        values='total',
        title='Distribución de Gastos por Categoría',
        hole=0.4,
        pull_first=True
    )

    print("✓ Gráfico de pie creado")
    print(f"  - Categorías: {len(df_categorias)}")
    print(f"  - Total: {df_categorias['total'].sum():.0f}€")

    for _, row in df_categorias.iterrows():
        pct = (row['total'] / df_categorias['total'].sum()) * 100
        print(f"  - {row['categoria']}: {row['total']}€ ({pct:.1f}%)")

    return fig


# ========== EJEMPLO 4: SCATTER PLOT ==========

def ejemplo_scatter():
    """Scatter plot con coste vs kilómetros"""
    print("\n4. SCATTER PLOT")
    print("-" * 50)

    fig = create_themed_scatter_chart(
        df_km,
        x='km',
        y='coste',
        size='kwh',
        title='Coste vs Kilómetros (Coche Eléctrico)',
        labels={'km': 'Kilómetros', 'coste': 'Coste (€)', 'kwh': 'kWh'},
        trendline='ols'
    )

    print("✓ Scatter plot creado")
    print(f"  - Puntos: {len(df_km)}")
    print(f"  - Coste por km promedio: {(df_km['coste'].sum() / df_km['km'].sum()):.3f}€/km")

    return fig


# ========== EJEMPLO 5: GRÁFICO DE ÁREA ==========

def ejemplo_area():
    """Gráfico de área con evolución"""
    print("\n5. GRÁFICO DE ÁREA")
    print("-" * 50)

    # Preparar datos
    df_area = df_mensual[['mes', 'ingresos', 'gastos']].copy()

    fig = create_themed_area_chart(
        df_area,
        x='mes',
        y=['ingresos', 'gastos'],
        title='Evolución de Ingresos y Gastos (Área)'
    )

    print("✓ Gráfico de área creado")
    print(f"  - Meses: {len(df_area)}")

    return fig


# ========== EJEMPLO 6: GRÁFICO MANUAL CON TEMA ==========

def ejemplo_manual():
    """Gráfico creado manualmente con tema aplicado"""
    print("\n6. GRÁFICO MANUAL CON TEMA")
    print("-" * 50)

    fig = go.Figure()

    # Añadir trazas manualmente
    fig.add_trace(go.Scatter(
        x=df_mensual['mes'],
        y=df_mensual['ingresos'],
        mode='lines+markers',
        name='Ingresos',
        line=dict(color=CHART_COLORS_FINANCE['income'], width=3),
        marker=dict(size=10)
    ))

    fig.add_trace(go.Scatter(
        x=df_mensual['mes'],
        y=df_mensual['gastos'],
        mode='lines+markers',
        name='Gastos',
        line=dict(color=CHART_COLORS_FINANCE['expense'], width=3),
        marker=dict(size=10)
    ))

    fig.add_trace(go.Scatter(
        x=df_mensual['mes'],
        y=df_mensual['balance'],
        mode='lines+markers',
        name='Balance',
        line=dict(color=CHART_COLORS_FINANCE['balance'], width=3, dash='dot'),
        marker=dict(size=10)
    ))

    # Aplicar tema
    apply_theme_to_fig(
        fig,
        title='Comparativa Financiera (Manual)',
        xaxis_title='Mes',
        yaxis_title='Importe (€)',
        height=500
    )

    print("✓ Gráfico manual creado y tema aplicado")
    print(f"  - Trazas: 3 (Ingresos, Gastos, Balance)")

    return fig


# ========== EJECUTAR TODOS LOS EJEMPLOS ==========

def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "="*50)
    print("EJEMPLOS DE USO - TEMA UNIFICADO DE PLOTLY")
    print("="*50)

    ejemplos = [
        ejemplo_lineas,
        ejemplo_barras,
        ejemplo_pie,
        ejemplo_scatter,
        ejemplo_area,
        ejemplo_manual
    ]

    figuras = []

    for ejemplo in ejemplos:
        try:
            fig = ejemplo()
            figuras.append(fig)
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\n" + "="*50)
    print(f"RESUMEN: {len(figuras)}/{len(ejemplos)} ejemplos ejecutados correctamente")
    print("="*50)

    # Opción: guardar todos los ejemplos
    guardar = input("\n¿Guardar ejemplos como HTML? (s/n): ").lower() == 's'

    if guardar:
        nombres = [
            'ejemplo_lineas.html',
            'ejemplo_barras.html',
            'ejemplo_pie.html',
            'ejemplo_scatter.html',
            'ejemplo_area.html',
            'ejemplo_manual.html'
        ]

        for i, fig in enumerate(figuras):
            if i < len(nombres):
                filename = f'docs/{nombres[i]}'
                fig.write_html(filename)
                print(f"✓ Guardado: {filename}")

        print(f"\n✓ {len(figuras)} archivos HTML guardados en /docs/")

    return figuras


if __name__ == '__main__':
    main()
