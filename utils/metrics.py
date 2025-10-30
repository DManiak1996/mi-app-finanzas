
# utils/metrics.py

from database import db_manager
import pandas as pd
from datetime import datetime, timedelta

def calcular_totales_mes(mes, año):
    """
    Calcula los totales de ingresos, gastos y el balance para un mes y año específicos.
    """
    transacciones = db_manager.obtener_transacciones(mes=mes, año=año)
    
    total_ingresos = sum(t['importe'] for t in transacciones if t['tipo'] == 'INGRESO')
    total_gastos = sum(t['importe'] for t in transacciones if t['tipo'] == 'GASTO')
    balance_neto = total_ingresos + total_gastos # Gastos ya son negativos
    
    # Obtener gastos por categoría
    gastos_por_categoria = db_manager.obtener_totales_por_categoria(mes, año)

    return {
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "balance_neto": balance_neto,
        "gastos_por_categoria": gastos_por_categoria
    }

def calcular_totales_anual(año):
    """
    Calcula los totales de ingresos, gastos y el balance para un año específico.
    También devuelve datos mensuales para gráficos de evolución.
    """
    transacciones = db_manager.obtener_transacciones(año=año)
    if not transacciones:
        return None

    df = pd.DataFrame(transacciones)
    df['fecha'] = pd.to_datetime(df['fecha'])

    total_ingresos = df[df['tipo'] == 'INGRESO']['importe'].sum()
    total_gastos = df[df['tipo'] == 'GASTO']['importe'].sum()
    balance_neto = total_ingresos + total_gastos

    gastos_por_categoria = df[df['tipo'] == 'GASTO'].groupby('categoria')['importe'].sum().to_dict()

    evolucion_mensual = df.groupby(df['fecha'].dt.month).agg(
        ingresos=('importe', lambda x: x[x > 0].sum()),
        gastos=('importe', lambda x: x[x < 0].sum())
    ).reindex(range(1, 13), fill_value=0)
    evolucion_mensual['balance'] = evolucion_mensual['ingresos'] + evolucion_mensual['gastos']

    return {
        "total_ingresos": total_ingresos, "total_gastos": total_gastos, "balance_neto": balance_neto,
        "gastos_por_categoria": gastos_por_categoria, "evolucion_mensual": evolucion_mensual
    }

def calcular_evolucion_mensual():
    """
    Calcula la evolución de ingresos, gastos y balance de los últimos 12 meses.
    """
    # Obtener todas las transacciones de la base de datos
    transacciones = db_manager.obtener_transacciones()
    if not transacciones:
        return pd.DataFrame()

    df = pd.DataFrame(transacciones)
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Asegurarse de que solo se consideran los últimos 12 meses desde la última transacción
    fecha_max = df['fecha'].max()
    fecha_min = fecha_max - timedelta(days=365)
    
    df_filtrado = df[df['fecha'] >= fecha_min]
    
    if df_filtrado.empty:
        return pd.DataFrame()

    # Agrupar por año y mes
    df_agrupado = df_filtrado.groupby([df_filtrado['fecha'].dt.year.rename('año'), df_filtrado['fecha'].dt.month.rename('mes')]).apply(lambda x: pd.Series({
        'ingresos': x[x['tipo'] == 'INGRESO']['importe'].sum(),
        'gastos': x[x['tipo'] == 'GASTO']['importe'].sum()
    })).reset_index()

    df_agrupado['balance'] = df_agrupado['ingresos'] + df_agrupado['gastos']
    
    # Crear una columna de período para ordenar
    df_agrupado['periodo'] = pd.to_datetime(df_agrupado['año'].astype(str) + '-' + df_agrupado['mes'].astype(str) + '-01')
    df_agrupado = df_agrupado.sort_values('periodo').reset_index(drop=True)

    return df_agrupado

def calcular_liquido_disponible():
    """
    Obtiene el balance total acumulado de la base de datos.
    """
    return db_manager.obtener_ultimo_saldo()
