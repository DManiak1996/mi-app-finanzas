
# utils/metrics.py

from database import db_manager
import pandas as pd
from datetime import datetime, timedelta

def calcular_totales_mes(mes, año):
    """
    Calcula los totales de ingresos, gastos y el balance para un mes y año específicos.
    Incluye cálculo de gastos netos (restando reembolsos).
    """
    transacciones = db_manager.obtener_transacciones(mes=mes, año=año)

    total_ingresos = sum(t['importe'] for t in transacciones if t['tipo'] == 'INGRESO' and t.get('categoria') != 'REEMBOLSO')
    total_gastos = sum(t['importe'] for t in transacciones if t['tipo'] == 'GASTO')
    total_reembolsos = sum(t['importe'] for t in transacciones if t.get('categoria') == 'REEMBOLSO' and t['tipo'] == 'INGRESO')

    # Gastos netos = gastos - reembolsos (total_gastos es negativo, total_reembolsos es positivo)
    gastos_netos = total_gastos + total_reembolsos

    balance_neto = total_ingresos + gastos_netos # Gastos netos ya son negativos

    # Obtener gastos NETOS por categoría (restando reembolsos asignados)
    gastos_por_categoria = db_manager.obtener_gastos_netos_por_categoria(mes, año)

    return {
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "total_reembolsos": total_reembolsos,
        "gastos_netos": gastos_netos,
        "balance_neto": balance_neto,
        "gastos_por_categoria": gastos_por_categoria
    }

def calcular_totales_anual(año):
    """
    Calcula los totales de ingresos, gastos y el balance para un año específico.
    También devuelve datos mensuales para gráficos de evolución.
    Incluye cálculo de gastos netos (restando reembolsos).
    """
    transacciones = db_manager.obtener_transacciones(año=año)
    if not transacciones:
        return None

    df = pd.DataFrame(transacciones)
    df['fecha'] = pd.to_datetime(df['fecha'])

    # Separar ingresos regulares de reembolsos
    total_ingresos = df[(df['tipo'] == 'INGRESO') & (df['categoria'] != 'REEMBOLSO')]['importe'].sum()
    total_gastos = df[df['tipo'] == 'GASTO']['importe'].sum()
    total_reembolsos = df[(df['categoria'] == 'REEMBOLSO') & (df['tipo'] == 'INGRESO')]['importe'].sum()

    # Gastos netos = gastos - reembolsos (total_gastos es negativo, total_reembolsos es positivo)
    gastos_netos = total_gastos + total_reembolsos
    balance_neto = total_ingresos + gastos_netos

    # Calcular gastos NETOS por categoría para el año (gastos brutos - reembolsos asignados)
    gastos_brutos_categoria = df[df['tipo'] == 'GASTO'].groupby('categoria')['importe'].sum()

    # Reembolsos asignados por categoría
    reembolsos_df = df[(df['categoria'] == 'REEMBOLSO') & (df['tipo'] == 'INGRESO') & (df['notas'].str.startswith('REEMBOLSO_DE:', na=False))].copy()
    if not reembolsos_df.empty:
        reembolsos_df['categoria_original'] = reembolsos_df['notas'].str.replace('REEMBOLSO_DE:', '')
        reembolsos_por_categoria = reembolsos_df.groupby('categoria_original')['importe'].sum()
    else:
        reembolsos_por_categoria = pd.Series(dtype=float)

    # Calcular netos: gastos_brutos + reembolsos (reembolsos son positivos, gastos son negativos)
    gastos_por_categoria = {}
    for cat in gastos_brutos_categoria.index:
        bruto = gastos_brutos_categoria[cat]
        reembolso = reembolsos_por_categoria.get(cat, 0)
        gastos_por_categoria[cat] = bruto + reembolso  # Resultado es más cercano a 0

    # Evolución mensual con gastos netos
    evolucion_mensual = df.groupby(df['fecha'].dt.month).agg(
        ingresos=('importe', lambda x: x[(x > 0) & (df.loc[x.index, 'categoria'] != 'REEMBOLSO')].sum()),
        gastos=('importe', lambda x: x[x < 0].sum()),
        reembolsos=('importe', lambda x: x[(df.loc[x.index, 'categoria'] == 'REEMBOLSO') & (df.loc[x.index, 'tipo'] == 'INGRESO')].sum())
    ).reindex(range(1, 13), fill_value=0)
    evolucion_mensual['gastos_netos'] = evolucion_mensual['gastos'] + evolucion_mensual['reembolsos']
    evolucion_mensual['balance'] = evolucion_mensual['ingresos'] + evolucion_mensual['gastos_netos']

    return {
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "total_reembolsos": total_reembolsos,
        "gastos_netos": gastos_netos,
        "balance_neto": balance_neto,
        "gastos_por_categoria": gastos_por_categoria,
        "evolucion_mensual": evolucion_mensual
    }

def calcular_evolucion_mensual():
    """
    Calcula la evolución de ingresos, gastos y balance de los últimos 12 meses.
    Incluye cálculo de gastos netos (restando reembolsos).
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
        'ingresos': x[(x['tipo'] == 'INGRESO') & (x['categoria'] != 'REEMBOLSO')]['importe'].sum(),
        'gastos': x[x['tipo'] == 'GASTO']['importe'].sum(),
        'reembolsos': x[(x['categoria'] == 'REEMBOLSO') & (x['tipo'] == 'INGRESO')]['importe'].sum()
    })).reset_index()

    df_agrupado['gastos_netos'] = df_agrupado['gastos'] + df_agrupado['reembolsos']
    df_agrupado['balance'] = df_agrupado['ingresos'] + df_agrupado['gastos_netos']

    # Crear una columna de período para ordenar
    df_agrupado['periodo'] = pd.to_datetime(df_agrupado['año'].astype(str) + '-' + df_agrupado['mes'].astype(str) + '-01')
    df_agrupado = df_agrupado.sort_values('periodo').reset_index(drop=True)

    return df_agrupado

def calcular_liquido_disponible():
    """
    Calcula el líquido disponible total.

    Returns:
        Saldo inicial + suma de todas las transacciones
    """
    from utils import config_manager

    saldo_inicial = config_manager.obtener_saldo_inicial()
    suma_transacciones = db_manager.obtener_ultimo_saldo()

    return saldo_inicial + suma_transacciones


# ========== MÉTRICAS FINANCIERAS AVANZADAS ==========

def calcular_tasa_ahorro(mes, año):
    """
    Calcula el porcentaje de ingresos que se está ahorrando.
    Usa el total de ingresos del mes (nómina + extraordinarios).

    Returns:
        Dict con tasa_ahorro (%), total_ingresos, gastos_netos, ahorro_absoluto
    """
    datos = calcular_totales_mes(mes, año)

    # Calcular total de ingresos del mes (nómina + extraordinarios)
    ingreso_base = obtener_ingreso_base_mes(mes, año)
    ingresos_extra = obtener_ingresos_extraordinarios_mes(mes, año)
    total_ingresos = ingreso_base + ingresos_extra['total']

    gastos_netos = abs(datos['gastos_netos'])  # Usar gastos netos (después de reembolsos)
    ahorro = total_ingresos - gastos_netos

    if total_ingresos == 0:
        tasa = 0
    else:
        tasa = (ahorro / total_ingresos) * 100

    return {
        'tasa_ahorro': round(tasa, 2),
        'ahorro_absoluto': round(ahorro, 2),
        'total_ingresos': round(total_ingresos, 2),
        'ingreso_base': round(ingreso_base, 2),
        'gastos': round(gastos_netos, 2)
    }


def calcular_gasto_promedio_diario(mes, año):
    """
    Calcula el gasto promedio por día del mes.

    Returns:
        Dict con promedio_diario, proyeccion_mes, dias_transcurridos
    """
    transacciones = db_manager.obtener_transacciones(mes=mes, año=año)
    gastos = [t for t in transacciones if t['tipo'] == 'GASTO']

    if not gastos:
        return {
            'promedio_diario': 0,
            'proyeccion_mes': 0,
            'dias_transcurridos': 0,
            'total_gastado': 0
        }

    # Calcular días transcurridos
    df = pd.DataFrame(gastos)
    df['fecha'] = pd.to_datetime(df['fecha'])

    dias_unicos = df['fecha'].dt.day.nunique()
    total_gastado = abs(df['importe'].sum())

    promedio_diario = total_gastado / dias_unicos if dias_unicos > 0 else 0

    # Proyección a fin de mes (asumiendo 30 días)
    proyeccion_mes = promedio_diario * 30

    return {
        'promedio_diario': round(promedio_diario, 2),
        'proyeccion_mes': round(proyeccion_mes, 2),
        'dias_transcurridos': dias_unicos,
        'total_gastado': round(total_gastado, 2)
    }


def calcular_variacion_mensual(mes, año):
    """
    Calcula la variación porcentual respecto al mes anterior.

    Returns:
        Dict con variaciones por categoría y total
    """
    # Mes actual
    datos_actual = calcular_totales_mes(mes, año)

    # Mes anterior
    mes_anterior = mes - 1 if mes > 1 else 12
    año_anterior = año if mes > 1 else año - 1
    datos_anterior = calcular_totales_mes(mes_anterior, año_anterior)

    # Variación total - usar gastos netos (después de reembolsos)
    gastos_actual = abs(datos_actual['gastos_netos'])
    gastos_anterior = abs(datos_anterior['gastos_netos'])

    if gastos_anterior == 0:
        variacion_total = 0
    else:
        variacion_total = ((gastos_actual - gastos_anterior) / gastos_anterior) * 100

    # Variaciones por categoría
    variaciones_categoria = {}
    for cat in datos_actual['gastos_por_categoria']:
        actual = abs(datos_actual['gastos_por_categoria'].get(cat, 0))
        anterior = abs(datos_anterior['gastos_por_categoria'].get(cat, 0))

        if anterior == 0:
            var = 0 if actual == 0 else 100
        else:
            var = ((actual - anterior) / anterior) * 100

        variaciones_categoria[cat] = {
            'actual': round(actual, 2),
            'anterior': round(anterior, 2),
            'variacion': round(var, 2)
        }

    return {
        'variacion_total': round(variacion_total, 2),
        'gastos_actual': round(gastos_actual, 2),
        'gastos_anterior': round(gastos_anterior, 2),
        'por_categoria': variaciones_categoria
    }


def calcular_top_gastos(mes, año, limite=10):
    """
    Obtiene los N gastos más grandes del mes.

    Returns:
        List de transacciones ordenadas por importe (mayor a menor)
    """
    transacciones = db_manager.obtener_transacciones(mes=mes, año=año)
    gastos = [t for t in transacciones if t['tipo'] == 'GASTO']

    # Ordenar por importe (de más negativo a menos negativo = mayor gasto primero)
    gastos_ordenados = sorted(gastos, key=lambda x: x['importe'])

    return gastos_ordenados[:limite]


def calcular_proyeccion_balance(meses_futuro=3):
    """
    Proyecta el balance futuro basándose en el promedio de los últimos 3 meses.

    Args:
        meses_futuro: Número de meses a proyectar

    Returns:
        Dict con balance_proyectado, promedio_mensual, fecha_proyeccion
    """
    # Obtener últimos 3 meses
    transacciones = db_manager.obtener_transacciones()
    if not transacciones:
        return {
            'balance_proyectado': 0,
            'promedio_mensual': 0,
            'confianza': 'baja'
        }

    df = pd.DataFrame(transacciones)
    df['fecha'] = pd.to_datetime(df['fecha'])

    # Últimos 3 meses
    fecha_max = df['fecha'].max()
    fecha_min = fecha_max - timedelta(days=90)
    df_reciente = df[df['fecha'] >= fecha_min]

    if df_reciente.empty:
        return {'balance_proyectado': 0, 'promedio_mensual': 0, 'confianza': 'baja'}

    # Agrupar por mes
    df_mensual = df_reciente.groupby([
        df_reciente['fecha'].dt.year,
        df_reciente['fecha'].dt.month
    ])['importe'].sum()

    promedio_mensual = df_mensual.mean()

    # Balance actual
    balance_actual = calcular_liquido_disponible()

    # Proyección
    balance_proyectado = balance_actual + (promedio_mensual * meses_futuro)

    # Confianza basada en volatilidad
    std = df_mensual.std()
    if std < abs(promedio_mensual) * 0.2:
        confianza = 'alta'
    elif std < abs(promedio_mensual) * 0.5:
        confianza = 'media'
    else:
        confianza = 'baja'

    return {
        'balance_proyectado': round(balance_proyectado, 2),
        'balance_actual': round(balance_actual, 2),
        'promedio_mensual': round(promedio_mensual, 2),
        'meses_proyectados': meses_futuro,
        'confianza': confianza
    }


def calcular_efficiency_ratios(mes, año):
    """
    Calcula ratios de eficiencia financiera.
    Usa el total de ingresos del mes (nómina + extraordinarios).

    Returns:
        Dict con ratios de cada categoría sobre total de ingresos
    """
    datos = calcular_totales_mes(mes, año)

    # Calcular total de ingresos del mes
    ingreso_base = obtener_ingreso_base_mes(mes, año)
    ingresos_extra = obtener_ingresos_extraordinarios_mes(mes, año)
    total_ingresos = ingreso_base + ingresos_extra['total']

    if total_ingresos == 0:
        return {
            'ratio_fijos': 0,
            'ratio_disfrute': 0,
            'ratio_extraordinarios': 0,
            'evaluacion': 'Sin ingresos registrados',
            'total_ingresos': 0
        }

    # Ratios por categoría
    ratios = {}
    for cat, gasto in datos['gastos_por_categoria'].items():
        ratio = (abs(gasto) / total_ingresos) * 100
        ratios[f'ratio_{cat.lower()}'] = round(ratio, 2)

    # Evaluación
    ratio_fijos = ratios.get('ratio_fijos', 0)
    ratio_disfrute = ratios.get('ratio_disfrute', 0)

    if ratio_fijos < 30 and ratio_disfrute < 30:
        evaluacion = '✅ Excelente control financiero'
    elif ratio_fijos < 50 and ratio_disfrute < 40:
        evaluacion = '👍 Buen equilibrio'
    elif ratio_fijos < 70:
        evaluacion = '⚠️ Gastos altos, considera optimizar'
    else:
        evaluacion = '❌ Gastos excesivos, acción necesaria'

    ratios['evaluacion'] = evaluacion
    ratios['total_ingresos'] = round(total_ingresos, 2)

    return ratios


def calcular_financial_health_score(mes, año):
    """
    Calcula un score de salud financiera (0-100).

    Considera:
    - Tasa de ahorro (30%)
    - Ratio fijos/ingresos (25%)
    - Estabilidad (25%)
    - Tendencia (20%)

    Returns:
        Dict con score y desglose
    """
    # 1. Tasa de ahorro (30 puntos)
    tasa_ahorro_data = calcular_tasa_ahorro(mes, año)
    tasa_ahorro = tasa_ahorro_data['tasa_ahorro']

    if tasa_ahorro >= 20:
        puntos_ahorro = 30
    elif tasa_ahorro >= 10:
        puntos_ahorro = 20
    elif tasa_ahorro >= 0:
        puntos_ahorro = 10
    else:
        puntos_ahorro = 0

    # 2. Ratio fijos/ingresos (25 puntos)
    ratios = calcular_efficiency_ratios(mes, año)
    ratio_fijos = ratios.get('ratio_fijos', 100)

    if ratio_fijos < 30:
        puntos_fijos = 25
    elif ratio_fijos < 50:
        puntos_fijos = 15
    elif ratio_fijos < 70:
        puntos_fijos = 5
    else:
        puntos_fijos = 0

    # 3. Estabilidad (25 puntos) - Basado en variación
    variacion = calcular_variacion_mensual(mes, año)
    var_total = abs(variacion['variacion_total'])

    if var_total < 10:
        puntos_estabilidad = 25
    elif var_total < 25:
        puntos_estabilidad = 15
    elif var_total < 50:
        puntos_estabilidad = 5
    else:
        puntos_estabilidad = 0

    # 4. Tendencia (20 puntos)
    # Si la variación es negativa (gastas menos), es positivo
    if variacion['variacion_total'] < -5:
        puntos_tendencia = 20  # Mejorando
    elif variacion['variacion_total'] < 5:
        puntos_tendencia = 10  # Estable
    else:
        puntos_tendencia = 0   # Empeorando

    # Score total
    score = puntos_ahorro + puntos_fijos + puntos_estabilidad + puntos_tendencia

    # Evaluación
    if score >= 80:
        evaluacion = '🌟 Excelente'
        color = 'verde'
    elif score >= 60:
        evaluacion = '👍 Bueno'
        color = 'azul'
    elif score >= 40:
        evaluacion = '⚠️ Regular'
        color = 'amarillo'
    else:
        evaluacion = '❌ Necesita Mejora'
        color = 'rojo'

    return {
        'score': score,
        'evaluacion': evaluacion,
        'color': color,
        'desglose': {
            'ahorro': puntos_ahorro,
            'eficiencia_fijos': puntos_fijos,
            'estabilidad': puntos_estabilidad,
            'tendencia': puntos_tendencia
        },
        'metricas': {
            'tasa_ahorro': tasa_ahorro,
            'ratio_fijos': ratio_fijos,
            'variacion': variacion['variacion_total']
        }
    }

def obtener_ingreso_base_mes(mes, año):
    """
    Obtiene el ingreso base (nómina regular) del mes.

    Estrategia mejorada con prioridad en el mes ACTUAL primero:
    1. Busca nómina en días 20-31 del mes ACTUAL (caso más común: nómina del 29)
    2. Busca nómina en últimos 7 días del mes ANTERIOR (para nóminas adelantadas)
    3. Busca nómina en primeros 10 días del mes ACTUAL (para nóminas tardías)
    4. Busca múltiples FIJOS y elige el más frecuente
    5. Busca cualquier ingreso alto (>500€) bien clasificado

    Returns:
        float: Importe de la nómina regular del mes
    """
    from database import db_manager
    import calendar

    conn = db_manager.get_db_connection()
    cursor = conn.cursor()

    # Calcular mes anterior
    if mes == 1:
        mes_anterior = 12
        año_anterior = año - 1
    else:
        mes_anterior = mes - 1
        año_anterior = año

    # ESTRATEGIA 1 (PRIORITARIA): Buscar nómina en días 20-31 del mes ACTUAL
    # Esto cubre el caso típico donde la nómina se paga el día 29-30 del mes correspondiente
    cursor.execute("""
        SELECT importe, fecha
        FROM transacciones
        WHERE tipo = 'INGRESO'
        AND categoria = 'FIJOS'
        AND mes = ?
        AND año = ?
        AND CAST(strftime('%d', fecha) AS INTEGER) >= 20
        ORDER BY importe DESC
        LIMIT 1
    """, (mes, año))

    resultado = cursor.fetchone()
    if resultado and resultado['importe']:
        conn.close()
        return resultado['importe']

    # ESTRATEGIA 2: Buscar nómina en últimos 7 días del mes ANTERIOR
    # Fallback para casos donde la nómina se adelanta (ej: pagada 28-31 del mes anterior)
    ultimo_dia_mes_anterior = calendar.monthrange(año_anterior, mes_anterior)[1]

    cursor.execute("""
        SELECT importe, fecha
        FROM transacciones
        WHERE tipo = 'INGRESO'
        AND categoria = 'FIJOS'
        AND mes = ?
        AND año = ?
        AND CAST(strftime('%d', fecha) AS INTEGER) >= ?
        ORDER BY importe DESC
        LIMIT 1
    """, (mes_anterior, año_anterior, max(1, ultimo_dia_mes_anterior - 6)))

    resultado = cursor.fetchone()
    if resultado and resultado['importe']:
        conn.close()
        return resultado['importe']

    # ESTRATEGIA 3: Buscar nómina en primeros 10 días del mes ACTUAL
    # Para nóminas tardías (ej: febrero pagada el 5 de marzo)
    cursor.execute("""
        SELECT importe, fecha
        FROM transacciones
        WHERE tipo = 'INGRESO'
        AND categoria = 'FIJOS'
        AND mes = ?
        AND año = ?
        AND CAST(strftime('%d', fecha) AS INTEGER) <= 10
        ORDER BY importe DESC
        LIMIT 1
    """, (mes, año))

    resultado = cursor.fetchone()
    if resultado and resultado['importe']:
        conn.close()
        return resultado['importe']

    # ESTRATEGIA 4: Si hay múltiples FIJOS en el mes (pagas extras),
    # tomar el más frecuente o el primero cronológicamente
    cursor.execute("""
        SELECT importe, COUNT(*) as frecuencia, MIN(fecha) as primera_fecha
        FROM transacciones
        WHERE tipo = 'INGRESO'
        AND categoria = 'FIJOS'
        AND mes = ?
        AND año = ?
        GROUP BY importe
        ORDER BY frecuencia DESC, primera_fecha ASC
        LIMIT 1
    """, (mes, año))

    resultado = cursor.fetchone()
    if resultado and resultado['importe']:
        conn.close()
        return resultado['importe']

    # ESTRATEGIA 5: Buscar cualquier ingreso alto (>500€) que no sea EXTRAORDINARIOS
    # Para casos donde la nómina no está bien clasificada
    cursor.execute("""
        SELECT MAX(importe) as max_ingreso
        FROM transacciones
        WHERE tipo = 'INGRESO'
        AND categoria != 'EXTRAORDINARIOS'
        AND categoria != 'REEMBOLSO'
        AND importe > 500
        AND mes = ?
        AND año = ?
    """, (mes, año))

    resultado = cursor.fetchone()
    if resultado and resultado['max_ingreso']:
        conn.close()
        return resultado['max_ingreso']

    # FALLBACK: Devolver 0 si no se encuentra nada
    conn.close()
    return 0.0

def obtener_ingresos_extraordinarios_mes(mes, año):
    """
    Obtiene los ingresos extraordinarios del mes (excluyendo nómina regular y reembolsos):
    - Pagas extras
    - Devoluciones IRPF
    - Ventas segunda mano
    - Bonificaciones
    - Otros ingresos no regulares

    Returns:
        Dict con total, lista de transacciones y desglose por tipo
    """
    from database import db_manager

    transacciones = db_manager.obtener_transacciones(mes=mes, año=año)

    # Obtener la nómina regular para excluirla
    ingreso_base = obtener_ingreso_base_mes(mes, año)

    ingresos_extraordinarios = []

    for t in transacciones:
        # Solo ingresos, no reembolsos
        if t['tipo'] != 'INGRESO' or t.get('categoria') == 'REEMBOLSO':
            continue

        # Excluir la nómina regular (con tolerancia de 1€ por si hay variaciones)
        if ingreso_base > 0 and abs(t['importe'] - ingreso_base) < 1.0:
            continue

        ingresos_extraordinarios.append(t)

    # Calcular totales y desglose
    total = sum(t['importe'] for t in ingresos_extraordinarios)

    desglose = {
        'pagas_extras': sum(t['importe'] for t in ingresos_extraordinarios if t.get('categoria') == 'FIJOS'),
        'irpf_bonificaciones': sum(t['importe'] for t in ingresos_extraordinarios if t.get('categoria') == 'EXTRAORDINARIOS'),
        'otros': sum(t['importe'] for t in ingresos_extraordinarios if t.get('categoria') not in ['FIJOS', 'EXTRAORDINARIOS', 'INGRESO'] and t.get('categoria') is not None),
        'sin_clasificar': sum(t['importe'] for t in ingresos_extraordinarios if t.get('categoria') == 'INGRESO' or t.get('categoria') is None or t.get('categoria') == 'SIN_CLASIFICAR')
    }

    return {
        'total': round(total, 2),
        'cantidad': len(ingresos_extraordinarios),
        'transacciones': ingresos_extraordinarios,
        'desglose': desglose
    }
