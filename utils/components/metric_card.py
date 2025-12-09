"""
Componente MetricCard - Tarjetas de métricas usando componentes nativos de Streamlit
===================================================================================

Este módulo proporciona componentes para mostrar métricas financieras
usando SOLO componentes nativos de Streamlit (st.metric):
- Formateo automático (currency, percent, number, text)
- Indicadores de tendencia (delta con colores)
- Iconos personalizables en el título
- Integración con design_tokens.py para formateo

NOTA: Esta versión usa st.metric() nativo en lugar de HTML custom.
Los parámetros 'color', 'show_border' y 'glassmorphism' se mantienen
para compatibilidad con código existente pero se ignoran en el render.

Uso básico:
    from utils.components.metric_card import render_metric_card

    render_metric_card(
        title="Balance del Mes",
        value=700.50,
        delta=15.5,
        icon="⚖️",
        trend="up",
        color="success"
    )

Author: Daniel
Version: 2.0 (Native Components)
Date: 2025-12-07
"""

import streamlit as st
from typing import Optional, Literal, Union
from utils.design_tokens import (
    Colors,
    Typography,
    Spacing,
    BorderRadius,
    Transitions,
    rgba_from_hex
)


def render_metric_card(
    title: str,
    value: Union[float, str],
    delta: Optional[Union[float, str]] = None,
    icon: Optional[str] = None,
    color: Literal["success", "danger", "info", "warning", "neutral"] = "neutral",
    trend: Optional[Literal["up", "down", "neutral"]] = None,
    format_type: Literal["currency", "percent", "number", "text"] = "currency",
    help_text: Optional[str] = None,
    show_border: bool = True,
    glassmorphism: bool = False
) -> None:
    """
    Renderiza una tarjeta de métrica usando componentes nativos de Streamlit.

    Args:
        title: Título de la métrica (ej: "Balance del Mes")
        value: Valor principal. Si es número, se formatea automáticamente
        delta: Cambio respecto período anterior (número o texto)
        icon: Emoji o icono decorativo (ej: "⚖️", "💰", "📈")
        color: Variante de color ("success", "danger", "info", "warning", "neutral")
        trend: Indicador de tendencia visual ("up", "down", "neutral")
        format_type: Tipo de formato automático ("currency", "percent", "number", "text")
        help_text: Texto de ayuda mostrado como caption
        show_border: Mostrar borde decorativo superior (ignorado en versión nativa)
        glassmorphism: Aplicar efecto glassmorphism (ignorado en versión nativa)

    Returns:
        None: Renderiza directamente en Streamlit

    Example:
        >>> # Métrica de ingresos con tendencia positiva
        >>> render_metric_card(
        ...     title="Ingresos del Mes",
        ...     value=2500.00,
        ...     delta=8.5,
        ...     icon="💰",
        ...     color="success",
        ...     trend="up",
        ...     help_text="Total de ingresos recibidos este mes"
        ... )

        >>> # Métrica de gastos con valor personalizado
        >>> render_metric_card(
        ...     title="Gastos Totales",
        ...     value=1800.50,
        ...     delta=-5.2,
        ...     icon="💸",
        ...     color="danger",
        ...     trend="down",
        ...     format_type="currency"
        ... )

        >>> # Métrica de porcentaje
        >>> render_metric_card(
        ...     title="Tasa de Ahorro",
        ...     value=28.5,
        ...     icon="📊",
        ...     color="info",
        ...     format_type="percent"
        ... )
    """

    # Formatear valor según tipo
    formatted_value = _format_value(value, format_type)

    # Formatear delta si existe
    formatted_delta = None
    delta_color = "normal"  # Streamlit usa "normal", "inverse", "off"

    if delta is not None:
        formatted_delta, delta_icon, delta_color_text = _format_delta(
            delta, format_type, trend
        )

        # Determinar delta_color para st.metric
        # Si trend está especificado, usarlo; si no, basarse en el signo
        if trend == "up" or (trend is None and isinstance(delta, (int, float)) and delta > 0):
            delta_color = "normal"  # Verde para positivo
        elif trend == "down" or (trend is None and isinstance(delta, (int, float)) and delta < 0):
            delta_color = "inverse"  # Rojo para negativo
        else:
            delta_color = "off"  # Sin color para neutral

    # Agregar icono al título si existe
    label_with_icon = f"{icon} {title}" if icon else title

    # Usar st.metric nativo de Streamlit
    st.metric(
        label=label_with_icon,
        value=formatted_value,
        delta=formatted_delta if delta is not None else None,
        delta_color=delta_color,
        help=help_text
    )


def metric_card_success(
    title: str,
    value: Union[float, str],
    delta: Optional[Union[float, str]] = None,
    icon: str = "✅",
    **kwargs
) -> None:
    """
    Tarjeta de métrica con variante SUCCESS (verde, para ingresos/positivo).

    Args:
        title: Título de la métrica
        value: Valor principal
        delta: Cambio respecto período anterior
        icon: Icono (default: ✅)
        **kwargs: Argumentos adicionales para render_metric_card

    Example:
        >>> metric_card_success("Ingresos", 2500.00, delta=8.5, icon="💰")
    """
    render_metric_card(
        title=title,
        value=value,
        delta=delta,
        icon=icon,
        color="success",
        **kwargs
    )


def metric_card_danger(
    title: str,
    value: Union[float, str],
    delta: Optional[Union[float, str]] = None,
    icon: str = "⚠️",
    **kwargs
) -> None:
    """
    Tarjeta de métrica con variante DANGER (rojo, para gastos/negativo).

    Args:
        title: Título de la métrica
        value: Valor principal
        delta: Cambio respecto período anterior
        icon: Icono (default: ⚠️)
        **kwargs: Argumentos adicionales para render_metric_card

    Example:
        >>> metric_card_danger("Gastos Totales", 1800.50, delta=-5.2, icon="💸")
    """
    render_metric_card(
        title=title,
        value=value,
        delta=delta,
        icon=icon,
        color="danger",
        **kwargs
    )


def metric_card_info(
    title: str,
    value: Union[float, str],
    delta: Optional[Union[float, str]] = None,
    icon: str = "ℹ️",
    **kwargs
) -> None:
    """
    Tarjeta de métrica con variante INFO (azul, para información).

    Args:
        title: Título de la métrica
        value: Valor principal
        delta: Cambio respecto período anterior
        icon: Icono (default: ℹ️)
        **kwargs: Argumentos adicionales para render_metric_card

    Example:
        >>> metric_card_info("Transacciones", 45, format_type="number", icon="📋")
    """
    render_metric_card(
        title=title,
        value=value,
        delta=delta,
        icon=icon,
        color="info",
        **kwargs
    )


def metric_card_warning(
    title: str,
    value: Union[float, str],
    delta: Optional[Union[float, str]] = None,
    icon: str = "⚡",
    **kwargs
) -> None:
    """
    Tarjeta de métrica con variante WARNING (amarillo/naranja, para alertas).

    Args:
        title: Título de la métrica
        value: Valor principal
        delta: Cambio respecto período anterior
        icon: Icono (default: ⚡)
        **kwargs: Argumentos adicionales para render_metric_card

    Example:
        >>> metric_card_warning("Presupuesto al 85%", "850€", icon="⚠️")
    """
    render_metric_card(
        title=title,
        value=value,
        delta=delta,
        icon=icon,
        color="warning",
        **kwargs
    )


def metric_card_neutral(
    title: str,
    value: Union[float, str],
    delta: Optional[Union[float, str]] = None,
    icon: str = "📊",
    **kwargs
) -> None:
    """
    Tarjeta de métrica con variante NEUTRAL (gris, para datos generales).

    Args:
        title: Título de la métrica
        value: Valor principal
        delta: Cambio respecto período anterior
        icon: Icono (default: 📊)
        **kwargs: Argumentos adicionales para render_metric_card

    Example:
        >>> metric_card_neutral("Promedio Diario", 60.15, icon="📈")
    """
    render_metric_card(
        title=title,
        value=value,
        delta=delta,
        icon=icon,
        color="neutral",
        **kwargs
    )


# ============================================================================
# FUNCIONES HELPER PRIVADAS
# ============================================================================

def _format_value(value: Union[float, str], format_type: str) -> str:
    """
    Formatea el valor según el tipo especificado.

    Args:
        value: Valor a formatear
        format_type: Tipo de formato ("currency", "percent", "number", "text")

    Returns:
        Valor formateado como string
    """
    if format_type == "text" or isinstance(value, str):
        return str(value)

    # Convertir a float si es posible
    try:
        numeric_value = float(value)
    except (ValueError, TypeError):
        return str(value)

    if format_type == "currency":
        # Formato: 1.234,56 €
        return f"{numeric_value:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

    elif format_type == "percent":
        # Formato: 28.5%
        return f"{numeric_value:.1f}%"

    elif format_type == "number":
        # Formato: 1.234
        if numeric_value >= 1000:
            return f"{numeric_value:,.0f}".replace(",", ".")
        elif numeric_value >= 10:
            return f"{numeric_value:.1f}"
        else:
            return f"{numeric_value:.2f}"

    return str(value)


def _format_delta(
    delta: Union[float, str],
    format_type: str,
    trend: Optional[str]
) -> tuple[str, str, str]:
    """
    Formatea el delta y determina el icono y color.

    Args:
        delta: Valor del delta
        format_type: Tipo de formato
        trend: Tendencia especificada

    Returns:
        Tupla de (delta_formateado, icono, color)
    """
    # Si delta es string, retornar tal cual
    if isinstance(delta, str):
        icon = _get_trend_arrow(trend) if trend else ""
        color = _get_delta_color(0, trend)  # Neutral por defecto
        return delta, icon, color

    # Convertir a float
    try:
        numeric_delta = float(delta)
    except (ValueError, TypeError):
        return str(delta), "", Colors.GRAY_700

    # Determinar signo y valor absoluto
    sign = "+" if numeric_delta >= 0 else ""

    # Formatear según tipo
    if format_type == "currency":
        formatted = f"{sign}{numeric_delta:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
    elif format_type == "percent":
        formatted = f"{sign}{numeric_delta:.1f}%"
    else:
        formatted = f"{sign}{numeric_delta:.1f}"

    # Determinar icono y color
    icon = _get_trend_arrow(trend) if trend else _get_delta_arrow(numeric_delta)
    color = _get_delta_color(numeric_delta, trend)

    return formatted, icon, color


def _get_trend_arrow(trend: Optional[str]) -> str:
    """
    Obtiene el emoji de flecha según la tendencia.

    Args:
        trend: "up", "down" o "neutral"

    Returns:
        Emoji de flecha
    """
    if trend == "up":
        return "↗"
    elif trend == "down":
        return "↘"
    elif trend == "neutral":
        return "→"
    return ""


def _get_delta_arrow(delta: float) -> str:
    """
    Obtiene el emoji de flecha según el valor del delta.

    Args:
        delta: Valor numérico del delta

    Returns:
        Emoji de flecha
    """
    if delta > 0:
        return "↗"
    elif delta < 0:
        return "↘"
    return "→"


def _get_delta_color(delta: float, trend: Optional[str]) -> str:
    """
    Determina el color del delta según su valor y tendencia.

    Args:
        delta: Valor numérico del delta
        trend: Tendencia especificada

    Returns:
        Color hexadecimal
    """
    # Si hay tendencia especificada, usarla
    if trend == "up":
        return Colors.SUCCESS
    elif trend == "down":
        return Colors.ERROR
    elif trend == "neutral":
        return Colors.GRAY_700

    # Si no hay tendencia, usar el signo del delta
    if delta > 0:
        return Colors.SUCCESS
    elif delta < 0:
        return Colors.ERROR

    return Colors.GRAY_700


def _get_color_config(color: str) -> dict:
    """
    Obtiene la configuración de colores para cada variante.

    Args:
        color: Variante de color

    Returns:
        Diccionario con gradient, border_color y base_color
    """
    configs = {
        "success": {
            "gradient": Colors.PREMIUM_GRADIENT_TEAL,
            "border_color": rgba_from_hex(Colors.PREMIUM_TEAL_START, 0.2),
            "base_color": Colors.SUCCESS
        },
        "danger": {
            "gradient": Colors.PREMIUM_GRADIENT_CORAL,
            "border_color": rgba_from_hex(Colors.PREMIUM_CORAL_START, 0.2),
            "base_color": Colors.ERROR
        },
        "info": {
            "gradient": Colors.PREMIUM_GRADIENT_SKY,
            "border_color": rgba_from_hex(Colors.PREMIUM_SKY_START, 0.2),
            "base_color": Colors.PRIMARY
        },
        "warning": {
            "gradient": Colors.PREMIUM_GRADIENT_GOLD,
            "border_color": rgba_from_hex(Colors.PREMIUM_GOLD_START, 0.2),
            "base_color": Colors.WARNING
        },
        "neutral": {
            "gradient": Colors.PREMIUM_GRADIENT_PRIMARY,
            "border_color": rgba_from_hex(Colors.PREMIUM_PRIMARY_START, 0.15),
            "base_color": Colors.GRAY_700
        }
    }

    return configs.get(color, configs["neutral"])


# ============================================================================
# COMPONENTES DE UTILIDAD
# ============================================================================

def render_metric_row(metrics: list[dict], columns: Optional[int] = None) -> None:
    """
    Renderiza múltiples métricas en una fila responsive.

    Args:
        metrics: Lista de diccionarios con parámetros para render_metric_card
        columns: Número de columnas (None = automático según número de métricas)

    Example:
        >>> render_metric_row([
        ...     {"title": "Ingresos", "value": 2500, "color": "success", "icon": "💰"},
        ...     {"title": "Gastos", "value": 1800, "color": "danger", "icon": "💸"},
        ...     {"title": "Balance", "value": 700, "color": "info", "icon": "⚖️"}
        ... ])
    """
    if not metrics:
        return

    # Determinar número de columnas
    num_cols = columns if columns else len(metrics)
    cols = st.columns(num_cols)

    # Renderizar cada métrica en su columna
    for idx, metric_config in enumerate(metrics):
        col_idx = idx % num_cols
        with cols[col_idx]:
            render_metric_card(**metric_config)


def render_metric_grid(
    metrics: list[dict],
    columns_desktop: int = 3,
    columns_tablet: int = 2,
    columns_mobile: int = 1
) -> None:
    """
    Renderiza métricas en un grid usando st.columns nativo.

    Args:
        metrics: Lista de diccionarios con parámetros para render_metric_card
        columns_desktop: Número de columnas en desktop (usado por defecto)
        columns_tablet: Número de columnas en tablet (ignorado en versión nativa)
        columns_mobile: Número de columnas en móvil (ignorado en versión nativa)

    Note:
        Esta versión usa componentes nativos de Streamlit.
        Los parámetros columns_tablet y columns_mobile se ignoran ya que
        Streamlit no soporta media queries CSS directamente.

    Example:
        >>> render_metric_grid([
        ...     {"title": "Métrica 1", "value": 100, "color": "success"},
        ...     {"title": "Métrica 2", "value": 200, "color": "info"},
        ...     {"title": "Métrica 3", "value": 300, "color": "warning"},
        ...     {"title": "Métrica 4", "value": 400, "color": "danger"},
        ...     {"title": "Métrica 5", "value": 500, "color": "neutral"}
        ... ], columns_desktop=3)
    """
    if not metrics:
        return

    # Dividir métricas en filas
    num_cols = columns_desktop
    rows = [metrics[i:i + num_cols] for i in range(0, len(metrics), num_cols)]

    # Renderizar cada fila
    for row in rows:
        # Crear columnas para esta fila (usar len(row) para manejar última fila incompleta)
        cols = st.columns(len(row))
        for idx, metric_config in enumerate(row):
            with cols[idx]:
                render_metric_card(**metric_config)


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    st.set_page_config(page_title="MetricCard Demo", layout="wide")

    st.title("🎨 MetricCard Component Demo")
    st.markdown("---")

    # Sección 1: Variantes básicas
    st.header("1. Variantes de Color")
    render_metric_row([
        {
            "title": "Success",
            "value": 2500.50,
            "delta": 8.5,
            "icon": "💰",
            "color": "success",
            "trend": "up",
            "help_text": "Variante verde para ingresos/positivo"
        },
        {
            "title": "Danger",
            "value": 1800.25,
            "delta": -5.2,
            "icon": "💸",
            "color": "danger",
            "trend": "down",
            "help_text": "Variante roja para gastos/negativo"
        },
        {
            "title": "Info",
            "value": 700.25,
            "delta": 3.3,
            "icon": "⚖️",
            "color": "info",
            "trend": "up",
            "help_text": "Variante azul para información"
        }
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    render_metric_row([
        {
            "title": "Warning",
            "value": 850.00,
            "delta": 15.0,
            "icon": "⚡",
            "color": "warning",
            "trend": "up",
            "help_text": "Variante naranja para alertas"
        },
        {
            "title": "Neutral",
            "value": 60.15,
            "icon": "📊",
            "color": "neutral",
            "help_text": "Variante gris para datos generales"
        }
    ])

    st.markdown("---")

    # Sección 2: Formatos
    st.header("2. Tipos de Formato")
    render_metric_row([
        {
            "title": "Currency",
            "value": 1234.56,
            "icon": "💵",
            "format_type": "currency",
            "color": "success"
        },
        {
            "title": "Percent",
            "value": 28.5,
            "icon": "📊",
            "format_type": "percent",
            "color": "info"
        },
        {
            "title": "Number",
            "value": 12345,
            "icon": "🔢",
            "format_type": "number",
            "color": "neutral"
        },
        {
            "title": "Text",
            "value": "Custom Value",
            "icon": "📝",
            "format_type": "text",
            "color": "warning"
        }
    ])

    st.markdown("---")

    # Sección 3: Funciones helper
    st.header("3. Funciones Helper")
    col1, col2 = st.columns(2)

    with col1:
        metric_card_success("Ingresos Totales", 2500.00, delta=8.5, icon="💰")

    with col2:
        metric_card_danger("Gastos Totales", 1800.50, delta=-5.2, icon="💸")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card_info("Transacciones", 45, format_type="number", icon="📋")

    with col2:
        metric_card_warning("Presupuesto", "85%", icon="⚠️")

    with col3:
        metric_card_neutral("Promedio Diario", 60.15, icon="📈")

    st.markdown("---")

    # Sección 4: Glassmorphism
    st.header("4. Efecto Glassmorphism")
    render_metric_row([
        {
            "title": "Balance Premium",
            "value": 700.50,
            "delta": 15.5,
            "icon": "✨",
            "color": "info",
            "trend": "up",
            "glassmorphism": True,
            "help_text": "Con efecto glassmorphism activado"
        },
        {
            "title": "Ahorro Mensual",
            "value": 500.00,
            "delta": 20.0,
            "icon": "💎",
            "color": "success",
            "trend": "up",
            "glassmorphism": True
        }
    ])

    st.markdown("---")

    # Sección 5: Grid layout
    st.header("5. Grid Layout")
    metrics_data = [
        {"title": "Métrica 1", "value": 100, "icon": "1️⃣", "color": "success"},
        {"title": "Métrica 2", "value": 200, "icon": "2️⃣", "color": "info"},
        {"title": "Métrica 3", "value": 300, "icon": "3️⃣", "color": "warning"},
        {"title": "Métrica 4", "value": 400, "icon": "4️⃣", "color": "danger"},
        {"title": "Métrica 5", "value": 500, "icon": "5️⃣", "color": "neutral"},
    ]

    render_metric_grid(metrics_data, columns_desktop=3)
