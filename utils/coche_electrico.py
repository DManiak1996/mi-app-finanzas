# utils/coche_electrico.py
# Módulo para cálculos y análisis del coche eléctrico

import datetime
from typing import Dict, List, Tuple, Optional

# ========== CONSTANTES ==========

# Especificaciones VW ID.3 Pro S 2025
CAPACIDAD_BATERIA = 77.0  # kWh

# Tarifas electricidad (€/kWh) - de tu factura Iberdrola
TARIFAS = {
    'punta': 0.184576,
    'llano': 0.131892,
    'valle': 0.099904
}

# Costes fijos mensuales (€) - de tu factura
COSTES_FIJOS_MES = {
    'potencia': 13.71,
    'alquiler_contador': 0.80,
    'bono_social': 0.38,
    'servicios': 4.69
}

# Impuestos
IMPUESTO_ELECTRICIDAD = 0.0511269632  # 5,11269632%
IVA = 0.21  # 21%

# Comparativa gasolina
CONSUMO_GASOLINA_100KM = 7.0  # Litros/100km (coche equivalente)
PRECIO_GASOLINA_LITRO = 1.55  # €/litro (precio medio)

# Días en un mes (para cálculos proporcionales)
DIAS_MES = 30
HORAS_DIA = 24


# ========== FUNCIONES DE CÁLCULO DE RECARGA ==========

def calcular_kwh_cargados(bateria_inicial: float, bateria_final: float) -> float:
    """
    Calcula los kWh cargados según % de batería.

    Args:
        bateria_inicial: % de batería al inicio (0-100)
        bateria_final: % de batería al final (0-100)

    Returns:
        kWh cargados
    """
    porcentaje_cargado = bateria_final - bateria_inicial
    return CAPACIDAD_BATERIA * (porcentaje_cargado / 100)


def calcular_tiempo_recarga(kwh_cargados: float, potencia_recarga: float) -> float:
    """
    Calcula el tiempo estimado de recarga en horas.

    Args:
        kwh_cargados: kWh a cargar
        potencia_recarga: Potencia del cargador en kW (ej: 4.6, 7.4, 11)

    Returns:
        Horas de recarga
    """
    if potencia_recarga <= 0:
        return 0
    return kwh_cargados / potencia_recarga


def calcular_coste_recarga(
    kwh_cargados: float,
    franja_horaria: str,
    horas_recarga: float
) -> Dict[str, float]:
    """
    Calcula el coste completo de una recarga incluyendo todos los conceptos.

    Args:
        kwh_cargados: kWh cargados
        franja_horaria: 'punta', 'llano' o 'valle'
        horas_recarga: Duración de la recarga en horas

    Returns:
        Dict con desglose completo de costes
    """
    # 1. Coste energía según franja
    tarifa_kwh = TARIFAS.get(franja_horaria, TARIFAS['valle'])
    coste_energia = kwh_cargados * tarifa_kwh

    # 2. Proporción de tiempo que ocupa la recarga en el mes
    proporcion_tiempo = horas_recarga / (DIAS_MES * HORAS_DIA)

    # 3. Costes fijos proporcionales
    coste_potencia = COSTES_FIJOS_MES['potencia'] * proporcion_tiempo
    coste_alquiler = COSTES_FIJOS_MES['alquiler_contador'] * proporcion_tiempo
    coste_bono = COSTES_FIJOS_MES['bono_social'] * proporcion_tiempo
    coste_servicios = COSTES_FIJOS_MES['servicios'] * proporcion_tiempo

    # 4. Subtotal antes de impuestos
    subtotal = (coste_energia + coste_potencia + coste_alquiler +
                coste_bono + coste_servicios)

    # 5. Impuesto sobre electricidad
    impuesto_electricidad = subtotal * IMPUESTO_ELECTRICIDAD

    # 6. Total antes de IVA
    total_sin_iva = subtotal + impuesto_electricidad

    # 7. IVA
    iva = total_sin_iva * IVA

    # 8. Total final
    coste_total = total_sin_iva + iva

    return {
        'coste_energia': round(coste_energia, 2),
        'coste_potencia': round(coste_potencia, 2),
        'coste_alquiler': round(coste_alquiler, 2),
        'coste_bono': round(coste_bono, 2),
        'coste_servicios': round(coste_servicios, 2),
        'subtotal': round(subtotal, 2),
        'impuesto_electricidad': round(impuesto_electricidad, 2),
        'total_sin_iva': round(total_sin_iva, 2),
        'iva': round(iva, 2),
        'coste_total': round(coste_total, 2),
        'tarifa_kwh': tarifa_kwh
    }


# ========== FUNCIONES DE ANÁLISIS ==========

def calcular_autonomia_restante(bateria_actual: float, consumo_medio: float) -> float:
    """
    Calcula la autonomía estimada restante en km.

    Args:
        bateria_actual: % de batería actual (0-100)
        consumo_medio: Consumo en kWh/100km

    Returns:
        Kilómetros de autonomía restante
    """
    if consumo_medio <= 0:
        return 0

    kwh_disponibles = CAPACIDAD_BATERIA * (bateria_actual / 100)
    autonomia = (kwh_disponibles / consumo_medio) * 100
    return round(autonomia, 1)


def calcular_dias_desde_ultima_recarga(
    fecha_actual: datetime.date,
    fecha_ultima: datetime.date
) -> int:
    """
    Calcula los días transcurridos desde la última recarga.
    """
    delta = fecha_actual - fecha_ultima
    return delta.days


def calcular_km_diarios(km_recorridos: float, dias: int) -> float:
    """
    Calcula el promedio de km recorridos por día.
    """
    if dias <= 0:
        return 0
    return round(km_recorridos / dias, 1)


def calcular_kwh_diarios(kwh_cargados: float, dias: int) -> float:
    """
    Calcula el promedio de kWh consumidos por día.
    """
    if dias <= 0:
        return 0
    return round(kwh_cargados / dias, 2)


def calcular_coste_por_km(coste_total: float, km_recorridos: float) -> float:
    """
    Calcula el coste por kilómetro.
    """
    if km_recorridos <= 0:
        return 0
    return round(coste_total / km_recorridos, 4)


def calcular_ahorro_vs_gasolina(km_recorridos: float, coste_electrico: float) -> Dict[str, float]:
    """
    Calcula el ahorro comparado con un coche de gasolina equivalente.

    Args:
        km_recorridos: Kilómetros recorridos
        coste_electrico: Coste de electricidad en €

    Returns:
        Dict con coste gasolina, ahorro y porcentaje
    """
    # Coste si fuera gasolina
    litros_necesarios = (km_recorridos / 100) * CONSUMO_GASOLINA_100KM
    coste_gasolina = litros_necesarios * PRECIO_GASOLINA_LITRO

    # Ahorro
    ahorro = coste_gasolina - coste_electrico
    porcentaje_ahorro = (ahorro / coste_gasolina * 100) if coste_gasolina > 0 else 0

    return {
        'coste_gasolina': round(coste_gasolina, 2),
        'ahorro': round(ahorro, 2),
        'porcentaje_ahorro': round(porcentaje_ahorro, 1)
    }


def calcular_consumo_medio(kwh_totales: float, km_totales: float) -> float:
    """
    Calcula el consumo medio en kWh/100km.
    """
    if km_totales <= 0:
        return 0
    return round((kwh_totales / km_totales) * 100, 2)


# ========== FUNCIONES DE ESTADÍSTICAS MENSUALES ==========

def calcular_estadisticas_mes(
    recargas: List[Dict],
    incluir_proyeccion: bool = False,
    detectar_anomalias: bool = False
) -> Dict:
    """
    Calcula estadísticas completas de un mes basándose en todas las recargas.

    Args:
        recargas: Lista de diccionarios con datos de recargas del mes
        incluir_proyeccion: Si True, calcula proyecciones a fin de mes
        detectar_anomalias: Si True, busca recargas con km/día atípicos

    Returns:
        Dict con todas las estadísticas del mes
    """
    if not recargas:
        return {
            'total_recargas': 0,
            'kwh_totales': 0,
            'km_totales': 0,
            'coste_total': 0,
            'consumo_medio': 0,
            'coste_por_km': 0,
            'dias_promedio_entre_recargas': 0,
            'km_promedio_por_recarga': 0
        }

    total_recargas = len(recargas)
    kwh_totales = sum(r.get('kwh_cargados', 0) for r in recargas)
    km_totales = sum(r.get('km_recorridos', 0) for r in recargas)
    coste_total = sum(r.get('coste_total', 0) for r in recargas)

    # Consumo medio: Si hay km registrados, calcular como kWh/km
    # Si no hay km, usar el promedio de los consumos de cada recarga
    if km_totales > 0:
        consumo_medio = calcular_consumo_medio(kwh_totales, km_totales)
        coste_por_km = calcular_coste_por_km(coste_total, km_totales)
    else:
        # Sin km registrados: usar promedio del campo consumo_medio de cada recarga
        consumos_registrados = [r.get('consumo_medio', 0) for r in recargas if r.get('consumo_medio', 0) > 0]
        consumo_medio = sum(consumos_registrados) / len(consumos_registrados) if consumos_registrados else 0
        coste_por_km = 0  # No se puede calcular sin km

    # Calcular días promedio entre recargas
    dias_entre_recargas = []
    recargas_ordenadas = sorted(recargas, key=lambda x: x.get('fecha_recarga', datetime.datetime.now()))

    for i in range(1, len(recargas_ordenadas)):
        fecha_anterior = recargas_ordenadas[i-1].get('fecha_recarga')
        fecha_actual = recargas_ordenadas[i].get('fecha_recarga')
        if fecha_anterior and fecha_actual:
            if isinstance(fecha_anterior, str):
                fecha_anterior = datetime.datetime.fromisoformat(fecha_anterior)
            if isinstance(fecha_actual, str):
                fecha_actual = datetime.datetime.fromisoformat(fecha_actual)
            dias = (fecha_actual - fecha_anterior).days
            dias_entre_recargas.append(dias)

    dias_promedio = sum(dias_entre_recargas) / len(dias_entre_recargas) if dias_entre_recargas else 0
    km_promedio_recarga = km_totales / total_recargas if total_recargas > 0 else 0

    # Distribución por franja horaria
    recargas_por_franja = {
        'punta': sum(1 for r in recargas if r.get('franja_horaria') == 'punta'),
        'llano': sum(1 for r in recargas if r.get('franja_horaria') == 'llano'),
        'valle': sum(1 for r in recargas if r.get('franja_horaria') == 'valle')
    }

    porcentajes_franja = {
        franja: round((count / total_recargas * 100), 1) if total_recargas > 0 else 0
        for franja, count in recargas_por_franja.items()
    }

    # Proyecciones y Anomalías
    proyeccion = {}
    anomalias = []
    
    if incluir_proyeccion:
        proyeccion = calcular_proyeccion_mes(recargas)
        
    if detectar_anomalias:
        anomalias = detectar_anomalias_km(recargas)

    return {
        'total_recargas': total_recargas,
        'kwh_totales': round(kwh_totales, 2),
        'km_totales': round(km_totales, 1),
        'coste_total': round(coste_total, 2),
        'consumo_medio': consumo_medio,
        'coste_por_km': coste_por_km,
        'dias_promedio_entre_recargas': round(dias_promedio, 1),
        'km_promedio_por_recarga': round(km_promedio_recarga, 1),
        'distribucion_franjas': porcentajes_franja,
        'proyeccion': proyeccion,
        'anomalias': anomalias
    }


# ========== FUNCIONES DE PREDICCIÓN ==========

def predecir_proxima_recarga(
    fecha_ultima_recarga: datetime.date,
    dias_promedio: float,
    bateria_actual: float,
    autonomia_restante: float,
    km_diarios_promedio: float
) -> Dict:
    """
    Predice cuándo será necesaria la próxima recarga.

    Returns:
        Dict con fecha estimada y días restantes
    """
    # Método 1: Basado en días promedio entre recargas
    dias_hasta_proxima_por_patron = dias_promedio

    # Método 2: Basado en autonomía y km diarios
    dias_hasta_proxima_por_autonomia = autonomia_restante / km_diarios_promedio if km_diarios_promedio > 0 else dias_promedio

    # Usamos el promedio de ambos métodos
    dias_hasta_proxima = (dias_hasta_proxima_por_patron + dias_hasta_proxima_por_autonomia) / 2

    fecha_proxima = fecha_ultima_recarga + datetime.timedelta(days=int(dias_hasta_proxima))

    return {
        'fecha_estimada': fecha_proxima,
        'dias_restantes': int(dias_hasta_proxima),
        'metodo_patron': round(dias_hasta_proxima_por_patron, 1),
        'metodo_autonomia': round(dias_hasta_proxima_por_autonomia, 1)
    }


# ========== FUNCIONES DE VALIDACIÓN ==========

def validar_porcentaje_bateria(porcentaje: float) -> bool:
    """Valida que el porcentaje de batería esté entre 0 y 100."""
    return 0 <= porcentaje <= 100


def validar_franja_horaria(franja: str) -> bool:
    """Valida que la franja horaria sea válida."""
    return franja in TARIFAS.keys()


def validar_potencia_recarga(potencia: float) -> bool:
    """Valida que la potencia de recarga sea razonable (entre 1 y 350 kW)."""
    return 1 <= potencia <= 350

# ========== FUNCIONES DE PROYECCIÓN Y ANOMALÍAS ==========

def calcular_proyeccion_mes(recargas: List[Dict], fecha_actual: datetime.date = None) -> Dict:
    """
    Calcula proyecciones para fin de mes basadas en el ritmo actual.
    
    Args:
        recargas: Lista de recargas del mes
        fecha_actual: Fecha de referencia (por defecto hoy)
        
    Returns:
        Dict con valores proyectados
    """
    if not fecha_actual:
        fecha_actual = datetime.date.today()
        
    # Datos básicos del mes
    dias_totales_mes = (fecha_actual.replace(month=fecha_actual.month % 12 + 1, day=1) - datetime.timedelta(days=1)).day
    dias_transcurridos = fecha_actual.day
    dias_restantes = dias_totales_mes - dias_transcurridos
    
    # Totales actuales
    kwh_actuales = sum(r.get('kwh_cargados', 0) for r in recargas)
    coste_actual = sum(r.get('coste_total', 0) for r in recargas)
    km_actuales = sum(r.get('km_recorridos', 0) for r in recargas)
    
    # Calcular promedio km/día (solo de recargas con km > 0)
    recargas_con_km = [r for r in recargas if r.get('km_recorridos', 0) > 0]
    
    # Necesitamos saber cuántos días cubren esas recargas
    # Simplificación: usamos días transcurridos si hay al menos una recarga con km
    if recargas_con_km and dias_transcurridos > 0:
        km_promedio_dia = km_actuales / dias_transcurridos
    else:
        km_promedio_dia = 0
        
    # Proyecciones
    km_proyectados = km_actuales + (km_promedio_dia * dias_restantes)
    
    # Proyección proporcional para kWh y Coste (asumiendo consumo constante)
    if dias_transcurridos > 0:
        factor_proyeccion = dias_totales_mes / dias_transcurridos
        kwh_proyectados = kwh_actuales * factor_proyeccion
        coste_proyectado = coste_actual * factor_proyeccion
    else:
        kwh_proyectados = 0
        coste_proyectado = 0
        
    return {
        'dias_transcurridos': dias_transcurridos,
        'dias_totales': dias_totales_mes,
        'km_promedio_dia': round(km_promedio_dia, 1),
        'km_proyectados': round(km_proyectados, 0),
        'kwh_proyectados': round(kwh_proyectados, 1),
        'coste_proyectado': round(coste_proyectado, 2)
    }

def detectar_anomalias_km(recargas: List[Dict], umbral_desviacion: float = 0.5) -> List[Dict]:
    """
    Detecta recargas con km/día que se desvían significativamente del promedio.
    
    Args:
        recargas: Lista de recargas
        umbral_desviacion: Porcentaje de desviación para considerar anomalía (0.5 = 50%)
        
    Returns:
        Lista de anomalías detectadas
    """
    recargas_con_km = [r for r in recargas if r.get('km_recorridos', 0) > 0]
    if not recargas_con_km:
        return []
        
    # Calcular km/día para cada recarga
    # Necesitamos la fecha de la recarga anterior para saber los días
    recargas_ordenadas = sorted(recargas_con_km, key=lambda x: x.get('fecha_recarga'))
    datos_analisis = []
    
    # Obtener todas las recargas (incluso sin km) para calcular días correctamente
    todas_recargas = sorted(recargas, key=lambda x: x.get('fecha_recarga'))
    
    for i, recarga in enumerate(todas_recargas):
        if recarga.get('km_recorridos', 0) <= 0:
            continue
            
        # Buscar fecha anterior
        if i > 0:
            fecha_anterior = todas_recargas[i-1].get('fecha_recarga')
            if isinstance(fecha_anterior, str):
                fecha_anterior = datetime.datetime.fromisoformat(fecha_anterior)
        else:
            # Si es la primera del mes, no podemos calcular días exactos sin consultar mes anterior
            # Omitimos esta para el análisis de anomalías intra-mes
            continue
            
        fecha_actual = recarga.get('fecha_recarga')
        if isinstance(fecha_actual, str):
            fecha_actual = datetime.datetime.fromisoformat(fecha_actual)
            
        dias = (fecha_actual - fecha_anterior).days
        if dias > 0:
            km_dia = recarga['km_recorridos'] / dias
            datos_analisis.append({
                'recarga': recarga,
                'km_dia': km_dia,
                'dias': dias,
                'fecha': fecha_actual.strftime('%d/%m')
            })
            
    if not datos_analisis:
        return []
        
    # Calcular promedio y desviación
    promedio_km_dia = sum(d['km_dia'] for d in datos_analisis) / len(datos_analisis)
    
    anomalias = []
    for dato in datos_analisis:
        desviacion = (dato['km_dia'] - promedio_km_dia) / promedio_km_dia if promedio_km_dia > 0 else 0
        
        if abs(desviacion) > umbral_desviacion:
            anomalias.append({
                'recarga_id': dato['recarga'].get('id'),
                'fecha': dato['fecha'],
                'km_dia': round(dato['km_dia'], 1),
                'promedio': round(promedio_km_dia, 1),
                'desviacion_pct': round(desviacion * 100, 0),
                'tipo': 'alto' if desviacion > 0 else 'bajo'
            })
            
    return anomalias
