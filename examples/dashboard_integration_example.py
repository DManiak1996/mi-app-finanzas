"""
Ejemplo de Integración del MetricCard en el Dashboard
======================================================

Este archivo muestra cómo reemplazar st.metric() con render_metric_card()
en el dashboard existente de FinanzasFlow.

NO ejecutar directamente. Este es un ejemplo de código para copiar/adaptar.
"""

# =============================================================================
# ANTES: Usando st.metric() nativo
# =============================================================================

def mostrar_dashboard_OLD():
    """Dashboard con st.metric() nativo"""
    import streamlit as st

    # Sección de métricas
    st.subheader("Resumen del Mes")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Ingresos",
            value="2,500.00 €",
            delta="+5.2%"
        )

    with col2:
        st.metric(
            label="Total Gastos",
            value="1,850.50 €",
            delta="-3.1%"
        )

    with col3:
        st.metric(
            label="Balance",
            value="649.50 €",
            delta="+12.8%"
        )


# =============================================================================
# DESPUÉS: Usando render_metric_card()
# =============================================================================

def mostrar_dashboard_NEW():
    """Dashboard con MetricCard premium"""
    import streamlit as st
    from utils.components.metric_card import render_metric_row

    # Sección de métricas
    st.subheader("Resumen del Mes")

    # Opción 1: Usando render_metric_row (RECOMENDADO)
    render_metric_row([
        {
            "title": "Total Ingresos",
            "value": 2500.00,
            "delta": 5.2,
            "icon": "💰",
            "color": "success",
            "trend": "up",
            "help_text": "Ingresos totales del mes actual"
        },
        {
            "title": "Total Gastos",
            "value": 1850.50,
            "delta": -3.1,
            "icon": "💸",
            "color": "danger",
            "trend": "down",
            "help_text": "Gastos totales del mes actual"
        },
        {
            "title": "Balance",
            "value": 649.50,
            "delta": 12.8,
            "icon": "⚖️",
            "color": "info",
            "trend": "up",
            "help_text": "Diferencia entre ingresos y gastos"
        }
    ])

    # Opción 2: Usando helpers individuales
    # col1, col2, col3 = st.columns(3)
    #
    # with col1:
    #     metric_card_success(
    #         "Total Ingresos",
    #         2500.00,
    #         delta=5.2,
    #         icon="💰"
    #     )
    #
    # with col2:
    #     metric_card_danger(
    #         "Total Gastos",
    #         1850.50,
    #         delta=-3.1,
    #         icon="💸"
    #     )
    #
    # with col3:
    #     metric_card_info(
    #         "Balance",
    #         649.50,
    #         delta=12.8,
    #         icon="⚖️"
    #     )


# =============================================================================
# MIGRACIÓN GRADUAL CON FEATURE FLAGS
# =============================================================================

def mostrar_dashboard_MIGRATED():
    """Dashboard con migración gradual usando feature flags"""
    import streamlit as st
    from utils.feature_flags import FeatureFlags
    from utils.components.metric_card import render_metric_row

    st.subheader("Resumen del Mes")

    # Obtener datos (lógica existente)
    total_ingresos = 2500.00
    total_gastos = 1850.50
    balance = 649.50
    delta_ingresos = 5.2
    delta_gastos = -3.1
    delta_balance = 12.8

    # Usar nuevo componente si el feature flag está activado
    if FeatureFlags.USE_NEW_METRIC_CARDS:
        render_metric_row([
            {
                "title": "Total Ingresos",
                "value": total_ingresos,
                "delta": delta_ingresos,
                "icon": "💰",
                "color": "success",
                "trend": "up"
            },
            {
                "title": "Total Gastos",
                "value": total_gastos,
                "delta": delta_gastos,
                "icon": "💸",
                "color": "danger",
                "trend": "down"
            },
            {
                "title": "Balance",
                "value": balance,
                "delta": delta_balance,
                "icon": "⚖️",
                "color": "info",
                "trend": "up"
            }
        ])
    else:
        # Mantener código viejo
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Ingresos", f"{total_ingresos:,.2f} €", f"+{delta_ingresos}%")
        with col2:
            st.metric("Total Gastos", f"{total_gastos:,.2f} €", f"{delta_gastos}%")
        with col3:
            st.metric("Balance", f"{balance:,.2f} €", f"+{delta_balance}%")


# =============================================================================
# EJEMPLO COMPLETO: Desglose por Categorías
# =============================================================================

def mostrar_desglose_categorias():
    """Ejemplo de desglose de gastos por categoría con MetricCard"""
    import streamlit as st
    from utils.components.metric_card import render_metric_grid

    st.subheader("Gastos por Categoría")

    # Datos de ejemplo (en producción vendrían de la BD)
    gastos = {
        "FIJOS": {"total": 850.00, "porcentaje": 45.9},
        "DISFRUTE": {"total": 450.50, "porcentaje": 24.3},
        "EXTRAORDINARIOS": {"total": 550.00, "porcentaje": 29.8}
    }

    # Crear métricas
    metrics = []
    for categoria, data in gastos.items():
        metrics.append({
            "title": categoria,
            "value": data["total"],
            "delta": f"{data['porcentaje']}% del total",
            "icon": get_icon_for_category(categoria),
            "color": get_color_for_category(categoria),
            "format_type": "currency"
        })

    # Renderizar en grid de 3 columnas
    render_metric_grid(metrics, columns_desktop=3)


def get_icon_for_category(categoria: str) -> str:
    """Helper para obtener icono según categoría"""
    icons = {
        "FIJOS": "🏠",
        "DISFRUTE": "🎉",
        "EXTRAORDINARIOS": "⚡",
        "INGRESO": "💰"
    }
    return icons.get(categoria, "📊")


def get_color_for_category(categoria: str) -> str:
    """Helper para obtener color según categoría"""
    colors = {
        "FIJOS": "danger",
        "DISFRUTE": "warning",
        "EXTRAORDINARIOS": "info",
        "INGRESO": "success"
    }
    return colors.get(categoria, "neutral")


# =============================================================================
# EJEMPLO: Métricas Avanzadas (Financial Health Score, etc.)
# =============================================================================

def mostrar_metricas_avanzadas():
    """Ejemplo de métricas avanzadas del dashboard"""
    import streamlit as st
    from utils.components.metric_card import (
        metric_card_info,
        metric_card_neutral,
        metric_card_success
    )

    st.subheader("Métricas Avanzadas")

    # Calcular métricas (lógica simplificada)
    tasa_ahorro = 26.0
    gasto_promedio_dia = 61.68
    num_transacciones = 87
    health_score = 85

    # Renderizar en 4 columnas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card_info(
            "Tasa de Ahorro",
            tasa_ahorro,
            format_type="percent",
            icon="🎯",
            help_text="Porcentaje de ingresos ahorrados (ideal >20%)"
        )

    with col2:
        metric_card_neutral(
            "Gasto Promedio/Día",
            gasto_promedio_dia,
            icon="📅",
            help_text="Promedio de gasto diario este mes"
        )

    with col3:
        metric_card_info(
            "Transacciones",
            num_transacciones,
            format_type="number",
            icon="📋",
            help_text="Número total de transacciones"
        )

    with col4:
        metric_card_success(
            "Health Score",
            health_score,
            format_type="number",
            icon="💯",
            help_text="Puntuación de salud financiera (0-100)"
        )


# =============================================================================
# PASOS PARA MIGRAR TU DASHBOARD:
# =============================================================================

"""
1. ACTIVAR FEATURE FLAG (en utils/feature_flags.py):
   FeatureFlags.USE_NEW_METRIC_CARDS = True

2. IMPORTAR COMPONENTE (al inicio de app.py):
   from utils.components.metric_card import render_metric_row, metric_card_success

3. IDENTIFICAR MÉTRICAS (buscar en tu código):
   Busca: st.metric(
   Reemplaza con: render_metric_card() o helpers

4. ADAPTAR CÓDIGO:
   - Extraer datos a variables
   - Crear diccionarios de configuración
   - Usar render_metric_row() para layouts

5. TESTEAR:
   - Verificar que los valores son correctos
   - Probar en diferentes resoluciones
   - Verificar hover effects

6. ROLLBACK SI ES NECESARIO:
   - Simplemente cambia el feature flag a False
   - El código viejo seguirá funcionando

EJEMPLO DE CAMBIO MÍNIMO:
   # Antes
   st.metric("Balance", "700.50 €")

   # Después
   render_metric_card("Balance", 700.50, icon="⚖️")

EJEMPLO DE CAMBIO CON MEJORAS:
   # Antes
   st.metric("Balance", "700.50 €", "+12.8%")

   # Después
   render_metric_card(
       title="Balance",
       value=700.50,
       delta=12.8,
       icon="⚖️",
       color="info",
       trend="up",
       help_text="Diferencia entre ingresos y gastos"
   )
"""


# =============================================================================
# EJEMPLO: Migración de una página completa
# =============================================================================

def ejemplo_migracion_completa():
    """Ejemplo de cómo migrar una página completa del dashboard"""
    import streamlit as st
    from utils.components.metric_card import render_metric_row, metric_card_info

    # Título
    st.title("Dashboard Financiero")

    # === SECCIÓN 1: RESUMEN MENSUAL ===
    st.header("Resumen del Mes")

    # Obtener datos (tu lógica existente)
    from utils.metrics import calcular_totales_mes
    mes_actual = 12
    año_actual = 2025
    datos = calcular_totales_mes(mes_actual, año_actual)

    # Renderizar métricas principales
    render_metric_row([
        {
            "title": "Total Ingresos",
            "value": datos['total_ingresos'],
            "delta": datos.get('delta_ingresos', 0),
            "icon": "💰",
            "color": "success",
            "trend": "up" if datos.get('delta_ingresos', 0) > 0 else "down"
        },
        {
            "title": "Total Gastos",
            "value": abs(datos['total_gastos']),
            "delta": datos.get('delta_gastos', 0),
            "icon": "💸",
            "color": "danger",
            "trend": "down" if datos.get('delta_gastos', 0) < 0 else "up"
        },
        {
            "title": "Balance",
            "value": datos['balance_mes'],
            "delta": datos.get('delta_balance', 0),
            "icon": "⚖️",
            "color": "info",
            "trend": "up" if datos['balance_mes'] > 0 else "down"
        }
    ])

    st.markdown("---")

    # === SECCIÓN 2: DESGLOSE POR CATEGORÍA ===
    st.header("Gastos por Categoría")

    # Tu lógica para obtener gastos por categoría
    # gastos_categoria = obtener_gastos_categoria(mes_actual, año_actual)

    # Renderizar con grid
    from utils.components.metric_card import render_metric_grid

    gastos_categoria = [
        {
            "title": "Fijos",
            "value": 850.00,
            "icon": "🏠",
            "color": "danger",
            "delta": "45.9% del total"
        },
        {
            "title": "Disfrute",
            "value": 450.50,
            "icon": "🎉",
            "color": "warning",
            "delta": "24.3% del total"
        },
        {
            "title": "Extraordinarios",
            "value": 550.00,
            "icon": "⚡",
            "color": "info",
            "delta": "29.8% del total"
        }
    ]

    render_metric_grid(gastos_categoria, columns_desktop=3)

    st.markdown("---")

    # === SECCIÓN 3: MÉTRICAS AVANZADAS ===
    st.header("Métricas Avanzadas")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card_info(
            "Tasa de Ahorro",
            26.0,
            format_type="percent",
            icon="🎯"
        )

    with col2:
        metric_card_info(
            "Gasto/Día",
            61.68,
            icon="📅"
        )

    with col3:
        metric_card_info(
            "Transacciones",
            87,
            format_type="number",
            icon="📋"
        )

    with col4:
        metric_card_info(
            "Health Score",
            85,
            format_type="number",
            icon="💯"
        )


# =============================================================================
# NOTAS FINALES
# =============================================================================

"""
VENTAJAS DE LA MIGRACIÓN:
- ✅ Diseño más premium y profesional
- ✅ Consistencia visual en toda la app
- ✅ Menos código duplicado
- ✅ Fácil de mantener y modificar
- ✅ Animaciones y efectos mejorados
- ✅ Integración con design tokens
- ✅ Rollback instantáneo si hay problemas

COMPATIBILIDAD:
- ✅ Compatible con todos los navegadores modernos
- ✅ Funciona en móvil y desktop
- ✅ No rompe funcionalidad existente
- ✅ Puede coexistir con st.metric() nativo

PRÓXIMOS PASOS:
1. Activar feature flag en un entorno de prueba
2. Migrar una sección a la vez
3. Testear exhaustivamente
4. Desplegar gradualmente
5. Monitorear feedback de usuarios
"""
