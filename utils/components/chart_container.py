# utils/components/chart_container.py
"""
ChartContainer - Componente para gráficas Plotly consistentes

Este módulo proporciona contenedores estilizados para gráficas Plotly,
asegurando consistencia visual en toda la aplicación.

Características:
- Container responsive con estilos premium
- Header opcional con título y descripción
- Área de acciones (botones, filtros, etc)
- Loading states y empty states
- Error boundaries para gráficas que fallan
- Integración con el tema Plotly unificado

Uso:
    from utils.components.chart_container import render_chart_container

    fig = create_themed_line_chart(df, x='fecha', y='saldo')
    render_chart_container(
        fig,
        title="Evolución del Saldo",
        description="Saldo después de cada transacción"
    )
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Optional, Dict, List, Callable
from utils.design_tokens import Colors, BorderRadius, Spacing, Typography, Transitions
from utils.plotly_theme import apply_theme_to_fig
from utils.feature_flags import is_enabled


# ========== COMPONENTE PRINCIPAL ==========

def render_chart_container(
    fig: Optional[go.Figure] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    actions: Optional[List[Dict]] = None,
    height: int = 450,
    show_fullscreen: bool = True,
    loading: bool = False,
    error: Optional[str] = None,
    empty_message: Optional[str] = None,
    config: Optional[Dict] = None,
    variant: str = "default"
) -> None:
    """
    Renderiza un contenedor estilizado para gráficas Plotly.

    Args:
        fig: Figura de Plotly (None si loading o error)
        title: Título de la gráfica
        description: Descripción breve debajo del título
        actions: Lista de acciones (botones, filtros) a mostrar en el header
        height: Altura de la gráfica en píxeles
        show_fullscreen: Mostrar botón de pantalla completa
        loading: Mostrar skeleton loader
        error: Mensaje de error a mostrar
        empty_message: Mensaje cuando no hay datos
        config: Configuración adicional para st.plotly_chart
        variant: Variante de estilo ('default', 'premium', 'minimal')

    Example:
        >>> fig = create_themed_line_chart(df, x='fecha', y='saldo')
        >>> render_chart_container(
        ...     fig,
        ...     title="Evolución del Saldo",
        ...     description="Últimos 30 días",
        ...     actions=[
        ...         {"type": "button", "label": "Exportar", "icon": "📥"},
        ...         {"type": "selectbox", "label": "Período", "options": ["Mes", "Año"]}
        ...     ]
        ... )
    """

    # Verificar feature flag (opcional, para rollout progresivo)
    try:
        if not is_enabled("enable_chart_containers"):
            # Fallback: renderizar gráfica sin container
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            return
    except:
        # Si el flag no existe, continuar normalmente (default=True)
        pass

    # Seleccionar estilos según variante
    container_styles = _get_container_styles(variant)

    # Abrir contenedor
    st.markdown(f"""
    <div style="
        background: {container_styles['background']};
        border-radius: {container_styles['border_radius']};
        border: {container_styles['border']};
        padding: {container_styles['padding']};
        box-shadow: {container_styles['shadow']};
        transition: all {Transitions.BASE};
        margin-bottom: {Spacing.LG};
    ">
    """, unsafe_allow_html=True)

    # Renderizar header si hay título o acciones
    if title or actions:
        _render_header(title, description, actions)

    # Renderizar contenido según estado
    if loading:
        show_chart_loading()
    elif error:
        _render_error_state(error)
    elif empty_message:
        show_chart_empty(empty_message)
    elif fig:
        try:
            # Aplicar tema unificado si no está aplicado
            apply_theme_to_fig(fig, height=height)

            # Configuración por defecto para Plotly
            default_config = {
                'displayModeBar': show_fullscreen,
                'displaylogo': False,
                'modeBarButtonsToRemove': [
                    'pan2d',
                    'lasso2d',
                    'select2d',
                    'autoScale2d'
                ],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': title.replace(' ', '_').lower() if title else 'chart',
                    'height': height,
                    'width': 1200,
                    'scale': 2
                }
            }

            # Merge con config personalizada
            if config:
                default_config.update(config)

            # Renderizar gráfica
            st.plotly_chart(
                fig,
                use_container_width=True,
                config=default_config
            )
        except Exception as e:
            _render_error_state(f"Error al renderizar gráfica: {str(e)}")
    else:
        show_chart_empty("No se proporcionó ninguna gráfica")

    # Cerrar contenedor
    st.markdown("</div>", unsafe_allow_html=True)


# ========== VARIANTES ==========

def render_chart_full(
    fig: Optional[go.Figure] = None,
    title: Optional[str] = None,
    **kwargs
) -> None:
    """
    Renderiza gráfica de ancho completo (variante explícita).

    Args:
        fig: Figura de Plotly
        title: Título de la gráfica
        **kwargs: Argumentos adicionales para render_chart_container

    Example:
        >>> render_chart_full(fig, title="Dashboard Anual")
    """
    render_chart_container(fig, title, **kwargs)


def render_chart_half(
    figures: List[Dict],
    gap: str = Spacing.LG
) -> None:
    """
    Renderiza dos gráficas en mitad de ancho (columnas).

    Args:
        figures: Lista de diccionarios con configuración de gráficas
                 [{"fig": fig1, "title": "...", ...}, {"fig": fig2, ...}]
        gap: Espacio entre columnas

    Example:
        >>> render_chart_half([
        ...     {"fig": fig1, "title": "Ingresos"},
        ...     {"fig": fig2, "title": "Gastos"}
        ... ])
    """
    if len(figures) != 2:
        st.error("render_chart_half requiere exactamente 2 gráficas")
        return

    cols = st.columns(2, gap=gap)

    for col, chart_config in zip(cols, figures):
        with col:
            render_chart_container(**chart_config)


def render_chart_compact(
    fig: Optional[go.Figure] = None,
    title: Optional[str] = None,
    **kwargs
) -> None:
    """
    Renderiza gráfica en versión compacta (menor altura y padding).

    Args:
        fig: Figura de Plotly
        title: Título de la gráfica
        **kwargs: Argumentos adicionales

    Example:
        >>> render_chart_compact(fig, title="Mini Dashboard", height=300)
    """
    # Override con estilos compactos
    kwargs['height'] = kwargs.get('height', 300)
    kwargs['variant'] = 'minimal'

    render_chart_container(fig, title, **kwargs)


# ========== HELPERS PARA ACCIONES ==========

def add_chart_actions(
    export: bool = True,
    filter: bool = True,
    refresh: bool = False,
    custom_actions: Optional[List[Dict]] = None
) -> List[Dict]:
    """
    Genera lista de acciones comunes para gráficas.

    Args:
        export: Incluir botón de exportar
        filter: Incluir selector de filtros
        refresh: Incluir botón de refrescar
        custom_actions: Acciones personalizadas adicionales

    Returns:
        Lista de diccionarios de configuración de acciones

    Example:
        >>> actions = add_chart_actions(export=True, filter=True)
        >>> render_chart_container(fig, actions=actions)
    """
    actions = []

    if filter:
        actions.append({
            "type": "selectbox",
            "label": "Período",
            "key": "chart_filter_period",
            "options": ["Mes Actual", "Año Actual", "Últimos 12 meses", "Todo"],
            "index": 0
        })

    if export:
        actions.append({
            "type": "button",
            "label": "Exportar",
            "icon": "📥",
            "key": "chart_export_btn",
            "help": "Exportar gráfica como imagen PNG"
        })

    if refresh:
        actions.append({
            "type": "button",
            "label": "Refrescar",
            "icon": "🔄",
            "key": "chart_refresh_btn",
            "help": "Actualizar datos de la gráfica"
        })

    if custom_actions:
        actions.extend(custom_actions)

    return actions


# ========== ESTADOS ESPECIALES ==========

def show_chart_loading(message: str = "Cargando gráfica...") -> None:
    """
    Muestra skeleton loader mientras carga la gráfica.

    Args:
        message: Mensaje de carga

    Example:
        >>> show_chart_loading("Procesando datos...")
    """
    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 400px;
        gap: {Spacing.LG};
    ">
        <div style="
            width: 100%;
            height: 300px;
            background: linear-gradient(
                90deg,
                {Colors.GRAY_100} 0%,
                {Colors.GRAY_200} 50%,
                {Colors.GRAY_100} 100%
            );
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            border-radius: {BorderRadius.BASE};
        "></div>

        <p style="
            font-size: {Typography.TEXT_SM};
            color: {Colors.GRAY_600};
            font-weight: {Typography.WEIGHT_MEDIUM};
        ">{message}</p>
    </div>

    <style>
        @keyframes shimmer {{
            0% {{ background-position: 200% 0; }}
            100% {{ background-position: -200% 0; }}
        }}
    </style>
    """, unsafe_allow_html=True)


def show_chart_empty(message: str = "No hay datos para mostrar") -> None:
    """
    Muestra estado vacío cuando no hay datos.

    Args:
        message: Mensaje de estado vacío

    Example:
        >>> show_chart_empty("No hay transacciones este mes")
    """
    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 400px;
        gap: {Spacing.MD};
        text-align: center;
    ">
        <div style="
            font-size: 4rem;
            opacity: 0.3;
        ">📊</div>

        <p style="
            font-size: {Typography.TEXT_LG};
            color: {Colors.GRAY_600};
            font-weight: {Typography.WEIGHT_MEDIUM};
            margin: 0;
        ">{message}</p>

        <p style="
            font-size: {Typography.TEXT_SM};
            color: {Colors.GRAY_500};
            margin: 0;
        ">Intenta cambiar los filtros o importar más datos</p>
    </div>
    """, unsafe_allow_html=True)


# ========== FUNCIONES PRIVADAS (HELPERS INTERNOS) ==========

def _get_container_styles(variant: str) -> Dict[str, str]:
    """Retorna estilos del contenedor según variante."""

    styles = {
        "default": {
            "background": Colors.PREMIUM_CARD_GRADIENT,
            "border_radius": BorderRadius.LG,
            "border": f"1px solid rgba(10, 76, 62, 0.08)",
            "padding": Spacing.LG,
            "shadow": Colors.SHADOW_PREMIUM_MD
        },
        "premium": {
            "background": Colors.PREMIUM_CARD_GRADIENT,
            "border_radius": BorderRadius.XL,
            "border": f"1px solid rgba(10, 76, 62, 0.12)",
            "padding": Spacing.XL,
            "shadow": Colors.SHADOW_PREMIUM_LG
        },
        "minimal": {
            "background": Colors.BG_PRIMARY,
            "border_radius": BorderRadius.BASE,
            "border": f"1px solid {Colors.GRAY_200}",
            "padding": Spacing.MD,
            "shadow": Colors.SHADOW_PREMIUM_SM
        },
        "glass": {
            "background": Colors.GLASS_BG,
            "border_radius": BorderRadius.LG,
            "border": f"1px solid {Colors.GLASS_BORDER}",
            "padding": Spacing.LG,
            "shadow": Colors.GLASS_SHADOW
        }
    }

    return styles.get(variant, styles["default"])


def _render_header(
    title: Optional[str],
    description: Optional[str],
    actions: Optional[List[Dict]]
) -> None:
    """Renderiza el header del container con título y acciones."""

    # Contenedor flex para título y acciones
    if title or actions:
        header_col1, header_col2 = st.columns([3, 1])

        with header_col1:
            if title:
                st.markdown(f"""
                <h3 style="
                    margin: 0 0 {Spacing.XS if description else Spacing.MD} 0;
                    font-size: {Typography.TEXT_XL};
                    font-weight: {Typography.WEIGHT_BOLD};
                    color: {Colors.GRAY_900};
                ">{title}</h3>
                """, unsafe_allow_html=True)

            if description:
                st.markdown(f"""
                <p style="
                    margin: 0 0 {Spacing.MD} 0;
                    font-size: {Typography.TEXT_SM};
                    color: {Colors.GRAY_600};
                ">{description}</p>
                """, unsafe_allow_html=True)

        with header_col2:
            if actions:
                _render_actions(actions)


def _render_actions(actions: List[Dict]) -> None:
    """Renderiza botones y controles de acción."""

    for action in actions:
        action_type = action.get("type", "button")

        if action_type == "button":
            label = action.get("label", "Action")
            icon = action.get("icon", "")
            key = action.get("key", f"action_{label}")
            help_text = action.get("help")

            button_label = f"{icon} {label}" if icon else label

            if st.button(button_label, key=key, help=help_text):
                # Callback si existe
                if "callback" in action:
                    action["callback"]()

        elif action_type == "selectbox":
            label = action.get("label", "Select")
            options = action.get("options", [])
            key = action.get("key", f"select_{label}")
            index = action.get("index", 0)

            st.selectbox(label, options, index=index, key=key)

        elif action_type == "checkbox":
            label = action.get("label", "Option")
            key = action.get("key", f"check_{label}")
            value = action.get("value", False)

            st.checkbox(label, value=value, key=key)


def _render_error_state(error_message: str) -> None:
    """Renderiza estado de error."""

    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 400px;
        gap: {Spacing.MD};
        text-align: center;
        background: {Colors.ERROR_ULTRA_LIGHT};
        border-radius: {BorderRadius.BASE};
        padding: {Spacing.XL};
    ">
        <div style="
            font-size: 3rem;
        ">⚠️</div>

        <p style="
            font-size: {Typography.TEXT_LG};
            color: {Colors.ERROR_DARK};
            font-weight: {Typography.WEIGHT_SEMIBOLD};
            margin: 0;
        ">Error al cargar la gráfica</p>

        <p style="
            font-size: {Typography.TEXT_SM};
            color: {Colors.GRAY_600};
            margin: 0;
            font-family: {Typography.FONT_MONO};
        ">{error_message}</p>
    </div>
    """, unsafe_allow_html=True)


# ========== FUNCIONES DE UTILIDAD ==========

def create_chart_grid(
    charts: List[Dict],
    columns: int = 2,
    gap: str = Spacing.LG
) -> None:
    """
    Crea una cuadrícula de gráficas.

    Args:
        charts: Lista de diccionarios con configuración de gráficas
        columns: Número de columnas
        gap: Espacio entre gráficas

    Example:
        >>> create_chart_grid([
        ...     {"fig": fig1, "title": "Chart 1"},
        ...     {"fig": fig2, "title": "Chart 2"},
        ...     {"fig": fig3, "title": "Chart 3"},
        ...     {"fig": fig4, "title": "Chart 4"}
        ... ], columns=2)
    """
    cols = st.columns(columns, gap=gap)

    for i, chart_config in enumerate(charts):
        col_idx = i % columns
        with cols[col_idx]:
            render_chart_container(**chart_config)


def render_chart_with_tabs(
    tabs_config: Dict[str, Dict]
) -> None:
    """
    Renderiza múltiples gráficas en tabs.

    Args:
        tabs_config: Dict donde key=nombre_tab, value=config_chart

    Example:
        >>> render_chart_with_tabs({
        ...     "Mensual": {"fig": fig_monthly, "title": "Vista Mensual"},
        ...     "Anual": {"fig": fig_yearly, "title": "Vista Anual"}
        ... })
    """
    tabs = st.tabs(list(tabs_config.keys()))

    for tab, (tab_name, chart_config) in zip(tabs, tabs_config.items()):
        with tab:
            render_chart_container(**chart_config)


def get_chart_export_button(
    fig: go.Figure,
    filename: str = "chart",
    label: str = "Exportar PNG"
) -> bool:
    """
    Retorna botón de exportación de gráfica.

    Args:
        fig: Figura de Plotly
        filename: Nombre del archivo sin extensión
        label: Texto del botón

    Returns:
        True si se hizo clic en el botón

    Example:
        >>> if get_chart_export_button(fig, "balance_mensual"):
        ...     st.success("Gráfica exportada")
    """
    if st.button(label):
        try:
            # Plotly ya maneja la exportación con el botón de la modebar
            # Este botón es para triggers adicionales si se necesitan
            st.info("Usa el botón 📷 en la esquina de la gráfica para exportar")
            return True
        except Exception as e:
            st.error(f"Error al exportar: {e}")
            return False

    return False


# ========== PRESETS DE CONFIGURACIÓN ==========

PRESET_CONFIGS = {
    "finance_dashboard": {
        "variant": "premium",
        "height": 500,
        "show_fullscreen": True,
        "actions": add_chart_actions(export=True, filter=True, refresh=True)
    },
    "compact_widget": {
        "variant": "minimal",
        "height": 250,
        "show_fullscreen": False,
    },
    "fullscreen_analysis": {
        "variant": "default",
        "height": 600,
        "show_fullscreen": True,
    }
}


def render_chart_preset(
    preset: str,
    fig: Optional[go.Figure] = None,
    title: Optional[str] = None,
    **override_kwargs
) -> None:
    """
    Renderiza gráfica con configuración preset.

    Args:
        preset: Nombre del preset ('finance_dashboard', 'compact_widget', etc)
        fig: Figura de Plotly
        title: Título
        **override_kwargs: Argumentos para sobrescribir el preset

    Example:
        >>> render_chart_preset("finance_dashboard", fig, title="Balance")
    """
    config = PRESET_CONFIGS.get(preset, {}).copy()
    config.update(override_kwargs)

    render_chart_container(fig, title, **config)
