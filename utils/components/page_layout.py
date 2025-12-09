"""
PageLayout System - Sistema de layouts consistentes para páginas
==================================================================

Este módulo proporciona un sistema completo de layouts predefinidos y componentes
estructurales para mantener consistencia visual en todas las páginas de la aplicación.

Características:
- Función principal render_page_layout() con callback de contenido
- Layouts predefinidos: dashboard, form, table, detail
- Page headers con título, descripción y acciones
- Sistema de breadcrumbs para navegación
- Secciones de contenido con spacing consistente
- Sidebar opcional para filtros
- Footer opcional con información/links
- Container con max-width y padding responsive
- Compatible con design_tokens y feature_flags

Uso básico:
    from utils.components.page_layout import render_dashboard_layout, page_header

    def mi_contenido():
        st.write("Contenido de la página")

    render_dashboard_layout(
        content_fn=mi_contenido,
        title="Mi Dashboard",
        description="Análisis financiero completo"
    )

Autor: Claude Code
Fecha: 2025-12-04
Versión: 1.0.0
Basado en: ESTRATEGIA_OVERHAUL_DISEÑO.md - Sección 4.3
"""

import streamlit as st
from typing import Optional, Callable, List, Dict, Any, Literal
from contextlib import contextmanager
from utils.design_tokens import (
    Colors,
    Typography,
    Spacing,
    BorderRadius,
    Transitions,
    Config,
    rgba_from_hex
)
from utils.feature_flags import is_enabled


# ============================================================================
# FUNCIÓN PRINCIPAL - RENDER PAGE LAYOUT
# ============================================================================

def render_page_layout(
    content_fn: Callable,
    title: Optional[str] = None,
    header: Optional[Dict[str, Any]] = None,
    sidebar: Optional[Dict[str, Any]] = None,
    footer: Optional[Dict[str, Any]] = None,
    max_width: str = Config.MAX_CONTAINER_WIDTH,
    padding: str = Spacing.XL,
    background: str = Colors.BG_PRIMARY
) -> None:
    """
    Renderiza una página completa con layout consistente.

    Esta es la función principal del sistema PageLayout. Acepta un callback
    de contenido y opciones de configuración para header, sidebar y footer.

    Args:
        content_fn: Función que renderiza el contenido de la página
        title: Título de la página (usado si header no se provee)
        header: Configuración del header (dict con keys: title, description, actions, icon, breadcrumbs)
        sidebar: Configuración del sidebar (dict con keys: content_fn, width, position)
        footer: Configuración del footer (dict con keys: content, links, copyright)
        max_width: Ancho máximo del container principal
        padding: Padding del container principal
        background: Color de fondo del container

    Returns:
        None: Renderiza directamente en Streamlit

    Example:
        >>> def mi_contenido():
        ...     st.write("Hola mundo")
        ...
        >>> render_page_layout(
        ...     content_fn=mi_contenido,
        ...     header={
        ...         "title": "Dashboard",
        ...         "description": "Resumen financiero",
        ...         "icon": "📊",
        ...         "breadcrumbs": [
        ...             {"label": "Inicio", "url": "/"},
        ...             {"label": "Dashboard", "url": None}
        ...         ]
        ...     },
        ...     sidebar={"content_fn": render_filtros, "width": "300px"}
        ... )
    """
    # Aplicar estilos globales del container
    _inject_page_container_styles(max_width, padding, background)

    # Renderizar header si se provee
    if header:
        page_header(**header)
    elif title:
        page_header(title=title)

    # Layout con o sin sidebar
    if sidebar:
        _render_with_sidebar(
            content_fn=content_fn,
            sidebar_fn=sidebar.get("content_fn"),
            sidebar_width=sidebar.get("width", "300px"),
            sidebar_position=sidebar.get("position", "left")
        )
    else:
        # Contenido sin sidebar
        content_fn()

    # Renderizar footer si se provee
    if footer:
        page_footer(**footer)


# ============================================================================
# LAYOUTS PREDEFINIDOS
# ============================================================================

def render_dashboard_layout(
    content_fn: Callable,
    title: str = "Dashboard",
    description: Optional[str] = None,
    icon: str = "📊",
    show_period_selector: bool = True,
    show_filters: bool = False,
    filters_fn: Optional[Callable] = None,
    breadcrumbs: Optional[List[Dict[str, str]]] = None
) -> None:
    """
    Layout predefinido para páginas tipo dashboard con métricas y gráficas.

    Incluye:
    - Header con título, descripción e icono
    - Breadcrumbs opcionales
    - Selector de período (mes/año) opcional
    - Sidebar de filtros opcional
    - Area de contenido optimizada para métricas y charts

    Args:
        content_fn: Función que renderiza el contenido del dashboard
        title: Título del dashboard
        description: Descripción breve del dashboard
        icon: Emoji/icono decorativo
        show_period_selector: Mostrar selector de mes/año en el header
        show_filters: Mostrar sidebar de filtros
        filters_fn: Función que renderiza los filtros (si show_filters=True)
        breadcrumbs: Lista de breadcrumbs [{"label": "Inicio", "url": "/"}]

    Returns:
        None: Renderiza directamente en Streamlit

    Example:
        >>> def mi_dashboard():
        ...     col1, col2, col3 = st.columns(3)
        ...     with col1:
        ...         st.metric("Ingresos", "2,500€")
        ...     # ... más contenido
        ...
        >>> def mis_filtros():
        ...     st.selectbox("Categoría", ["Todas", "FIJOS", "DISFRUTE"])
        ...
        >>> render_dashboard_layout(
        ...     content_fn=mi_dashboard,
        ...     title="Dashboard Financiero",
        ...     description="Análisis de ingresos y gastos",
        ...     show_period_selector=True,
        ...     show_filters=True,
        ...     filters_fn=mis_filtros
        ... )
    """
    header_config = {
        "title": title,
        "description": description,
        "icon": icon,
        "breadcrumbs": breadcrumbs
    }

    # Agregar selector de período si se requiere
    actions = []
    if show_period_selector:
        actions.append({"type": "period_selector"})

    if actions:
        header_config["actions"] = actions

    sidebar_config = None
    if show_filters and filters_fn:
        sidebar_config = {
            "content_fn": filters_fn,
            "width": "280px",
            "position": "left"
        }

    render_page_layout(
        content_fn=content_fn,
        header=header_config,
        sidebar=sidebar_config,
        max_width="1600px",  # Dashboards suelen ser más anchos
        background=Colors.PREMIUM_BG_GRADIENT
    )


def render_form_layout(
    content_fn: Callable,
    title: str = "Formulario",
    description: Optional[str] = None,
    icon: str = "📝",
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    show_help_sidebar: bool = False,
    help_content: Optional[str] = None
) -> None:
    """
    Layout predefinido para páginas de formularios.

    Incluye:
    - Header con título y descripción
    - Container estrecho para mejor legibilidad (max 800px)
    - Sidebar opcional para ayuda/instrucciones
    - Padding adicional para formularios

    Args:
        content_fn: Función que renderiza el formulario
        title: Título del formulario
        description: Descripción/instrucciones del formulario
        icon: Emoji/icono decorativo
        breadcrumbs: Lista de breadcrumbs
        show_help_sidebar: Mostrar sidebar con ayuda
        help_content: Contenido de ayuda (markdown) para el sidebar

    Returns:
        None: Renderiza directamente en Streamlit

    Example:
        >>> def mi_formulario():
        ...     with st.form("mi_form"):
        ...         nombre = st.text_input("Nombre")
        ...         email = st.text_input("Email")
        ...         st.form_submit_button("Enviar")
        ...
        >>> render_form_layout(
        ...     content_fn=mi_formulario,
        ...     title="Nueva Transacción",
        ...     description="Completa los campos para agregar una transacción",
        ...     show_help_sidebar=True,
        ...     help_content="### Ayuda\\nIngresa la fecha en formato DD/MM/YYYY"
        ... )
    """
    header_config = {
        "title": title,
        "description": description,
        "icon": icon,
        "breadcrumbs": breadcrumbs
    }

    sidebar_config = None
    if show_help_sidebar and help_content:
        def render_help():
            st.markdown("### 💡 Ayuda")
            st.markdown("---")
            st.markdown(help_content)

        sidebar_config = {
            "content_fn": render_help,
            "width": "300px",
            "position": "right"
        }

    render_page_layout(
        content_fn=content_fn,
        header=header_config,
        sidebar=sidebar_config,
        max_width="800px",  # Formularios más estrechos para legibilidad
        padding=Spacing.XXL
    )


def render_table_layout(
    content_fn: Callable,
    title: str = "Datos",
    description: Optional[str] = None,
    icon: str = "📋",
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    show_filters: bool = True,
    filters_fn: Optional[Callable] = None,
    show_export_button: bool = True
) -> None:
    """
    Layout predefinido para páginas con tablas/listados de datos.

    Incluye:
    - Header con título y descripción
    - Botón de exportar opcional
    - Sidebar de filtros opcional
    - Container ancho para tablas

    Args:
        content_fn: Función que renderiza la tabla
        title: Título de la página
        description: Descripción de los datos
        icon: Emoji/icono decorativo
        breadcrumbs: Lista de breadcrumbs
        show_filters: Mostrar sidebar de filtros
        filters_fn: Función que renderiza los filtros
        show_export_button: Mostrar botón de exportar en header

    Returns:
        None: Renderiza directamente en Streamlit

    Example:
        >>> def mi_tabla():
        ...     df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        ...     st.dataframe(df, use_container_width=True)
        ...
        >>> def mis_filtros():
        ...     st.date_input("Fecha desde")
        ...     st.date_input("Fecha hasta")
        ...
        >>> render_table_layout(
        ...     content_fn=mi_tabla,
        ...     title="Transacciones",
        ...     description="Listado de todas las transacciones",
        ...     filters_fn=mis_filtros,
        ...     show_export_button=True
        ... )
    """
    header_config = {
        "title": title,
        "description": description,
        "icon": icon,
        "breadcrumbs": breadcrumbs
    }

    # Agregar botón de exportar si se requiere
    if show_export_button:
        header_config["actions"] = [{"type": "export_button"}]

    sidebar_config = None
    if show_filters and filters_fn:
        sidebar_config = {
            "content_fn": filters_fn,
            "width": "280px",
            "position": "left"
        }

    render_page_layout(
        content_fn=content_fn,
        header=header_config,
        sidebar=sidebar_config,
        max_width="1400px"  # Tablas suelen necesitar más ancho
    )


def render_detail_layout(
    content_fn: Callable,
    title: str,
    subtitle: Optional[str] = None,
    icon: str = "📄",
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    show_back_button: bool = True,
    actions: Optional[List[Dict[str, Any]]] = None
) -> None:
    """
    Layout predefinido para páginas de detalle de un ítem específico.

    Incluye:
    - Header con título, subtítulo y botón volver
    - Breadcrumbs para navegación
    - Acciones opcionales (editar, eliminar, etc.)
    - Container medio para detalle

    Args:
        content_fn: Función que renderiza el detalle
        title: Título (nombre del ítem)
        subtitle: Subtítulo (descripción o ID)
        icon: Emoji/icono decorativo
        breadcrumbs: Lista de breadcrumbs
        show_back_button: Mostrar botón volver en header
        actions: Lista de acciones disponibles [{"label": "Editar", "icon": "✏️", "callback": fn}]

    Returns:
        None: Renderiza directamente en Streamlit

    Example:
        >>> def detalle_transaccion():
        ...     st.write("**Fecha:** 2025-01-15")
        ...     st.write("**Importe:** 50.00€")
        ...     st.write("**Categoría:** DISFRUTE")
        ...
        >>> render_detail_layout(
        ...     content_fn=detalle_transaccion,
        ...     title="Transacción #1234",
        ...     subtitle="Compra en MERCADONA",
        ...     breadcrumbs=[
        ...         {"label": "Transacciones", "url": "/transacciones"},
        ...         {"label": "#1234", "url": None}
        ...     ],
        ...     actions=[
        ...         {"label": "Editar", "icon": "✏️", "callback": editar_transaccion},
        ...         {"label": "Eliminar", "icon": "🗑️", "callback": eliminar_transaccion}
        ...     ]
        ... )
    """
    header_config = {
        "title": title,
        "description": subtitle,
        "icon": icon,
        "breadcrumbs": breadcrumbs
    }

    # Agregar acciones al header
    header_actions = []

    if show_back_button:
        header_actions.append({"type": "back_button"})

    if actions:
        header_actions.extend(actions)

    if header_actions:
        header_config["actions"] = header_actions

    render_page_layout(
        content_fn=content_fn,
        header=header_config,
        max_width="1000px"  # Detalle con ancho medio
    )


# ============================================================================
# HELPERS - PAGE COMPONENTS
# ============================================================================

def page_header(
    title: str,
    description: Optional[str] = None,
    icon: Optional[str] = None,
    actions: Optional[List[Dict[str, Any]]] = None,
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    background: str = Colors.PREMIUM_BG_GRADIENT,
    show_divider: bool = True
) -> None:
    """
    Renderiza un header de página consistente.

    Args:
        title: Título principal de la página
        description: Descripción o subtítulo
        icon: Emoji/icono decorativo (opcional)
        actions: Lista de acciones/botones [{"type": "period_selector"|"export_button"|"back_button"}]
        breadcrumbs: Lista de breadcrumbs [{"label": "Home", "url": "/"}]
        background: Gradiente de fondo
        show_divider: Mostrar línea divisoria debajo del header

    Returns:
        None: Renderiza directamente en Streamlit

    Example:
        >>> page_header(
        ...     title="Dashboard Financiero",
        ...     description="Resumen de tus finanzas personales",
        ...     icon="📊",
        ...     breadcrumbs=[
        ...         {"label": "Inicio", "url": "/"},
        ...         {"label": "Dashboard", "url": None}
        ...     ],
        ...     actions=[{"type": "period_selector"}]
        ... )
    """
    # Renderizar breadcrumbs si existen
    if breadcrumbs:
        page_breadcrumbs(breadcrumbs)
        st.markdown(f'<div style="height: {Spacing.MD};"></div>', unsafe_allow_html=True)

    # Container del header
    st.markdown(f"""
    <div style="
        background: {background};
        padding: {Spacing.XL} 0 {Spacing.LG} 0;
        margin-bottom: {Spacing.XXL};
        {f'border-bottom: 2px solid {rgba_from_hex(Colors.PREMIUM_PRIMARY_START, 0.1)};' if show_divider else ''}
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: {Spacing.MD};
            margin-bottom: {Spacing.SM};
        ">
            {f'<span style="font-size: {Typography.TEXT_4XL}; line-height: 1;">{icon}</span>' if icon else ''}
            <h1 style="
                margin: 0;
                font-size: {Typography.TEXT_4XL};
                font-weight: {Typography.WEIGHT_EXTRABOLD};
                color: {Colors.GRAY_900};
                font-family: {Typography.FONT_PRIMARY};
                line-height: {Typography.LEADING_TIGHT};
            ">{title}</h1>
        </div>
        {f'''<p style="
            margin: 0;
            font-size: {Typography.TEXT_LG};
            color: {Colors.GRAY_600};
            line-height: {Typography.LEADING_NORMAL};
            max-width: {Config.MAX_TEXT_WIDTH};
        ">{description}</p>''' if description else ''}
    </div>
    """, unsafe_allow_html=True)

    # Renderizar acciones si existen
    if actions:
        _render_header_actions(actions)


def page_breadcrumbs(items: List[Dict[str, str]]) -> None:
    """
    Renderiza breadcrumbs de navegación.

    Args:
        items: Lista de items [{"label": "Home", "url": "/"}]
               El último item (sin url) se renderiza como texto actual

    Returns:
        None: Renderiza directamente en Streamlit

    Example:
        >>> page_breadcrumbs([
        ...     {"label": "Inicio", "url": "/"},
        ...     {"label": "Transacciones", "url": "/transacciones"},
        ...     {"label": "Detalle", "url": None}
        ... ])
    """
    if not items:
        return

    breadcrumb_html = f"""
    <div style="
        display: flex;
        align-items: center;
        gap: {Spacing.SM};
        font-size: {Typography.TEXT_SM};
        color: {Colors.GRAY_600};
        margin-top: {Spacing.MD};
        flex-wrap: wrap;
    ">
    """

    for idx, item in enumerate(items):
        label = item.get("label", "")
        url = item.get("url")

        # Separador (excepto para el primero)
        if idx > 0:
            breadcrumb_html += f"""
            <span style="color: {Colors.GRAY_400};">›</span>
            """

        # Item (link o texto)
        if url:
            breadcrumb_html += f"""
            <style>
                .breadcrumb-link-{i}:hover {{
                    color: {Colors.PRIMARY_LIGHT} !important;
                }}
            </style>
            <a href="{url}" class="breadcrumb-link-{i}" style="
                color: {Colors.PRIMARY};
                text-decoration: none;
                transition: color {Transitions.FAST} {Transitions.EASING_DEFAULT};
            ">
                {label}
            </a>
            """
        else:
            # Último item (actual) sin link
            breadcrumb_html += f"""
            <span style="
                color: {Colors.GRAY_900};
                font-weight: {Typography.WEIGHT_SEMIBOLD};
            ">{label}</span>
            """

    breadcrumb_html += "</div>"
    st.markdown(breadcrumb_html, unsafe_allow_html=True)


@contextmanager
def page_section(
    title: Optional[str] = None,
    description: Optional[str] = None,
    icon: Optional[str] = None,
    collapsible: bool = False,
    expanded: bool = True,
    background: str = "transparent",
    padding: str = Spacing.LG,
    margin_top: str = Spacing.XL,
    margin_bottom: str = Spacing.XL
):
    """
    Context manager para crear una sección de contenido con título y spacing consistente.

    Args:
        title: Título de la sección
        description: Descripción breve
        icon: Emoji/icono decorativo
        collapsible: Si la sección es colapsable (expander)
        expanded: Si está expandida por defecto (solo si collapsible=True)
        background: Color de fondo de la sección
        padding: Padding interno de la sección
        margin_top: Margen superior
        margin_bottom: Margen inferior

    Yields:
        None: Context manager para usar con 'with'

    Example:
        >>> with page_section(title="Métricas Principales", icon="📊"):
        ...     col1, col2, col3 = st.columns(3)
        ...     with col1:
        ...         st.metric("Balance", "700€")
        ...
        >>> with page_section(title="Configuración", collapsible=True):
        ...     st.checkbox("Opción 1")
        ...     st.checkbox("Opción 2")
    """
    # Si es colapsible, usar st.expander
    if collapsible:
        section_title = f"{icon} {title}" if icon else title
        with st.expander(section_title, expanded=expanded):
            if description:
                st.caption(description)
                st.markdown(f'<div style="height: {Spacing.MD};"></div>', unsafe_allow_html=True)
            yield
    else:
        # Sección no colapsable con estilos
        if title or description:
            title_html = f"""
            <div style="margin-top: {margin_top}; margin-bottom: {Spacing.LG};">
                {f'''<h3 style="
                    display: flex;
                    align-items: center;
                    gap: {Spacing.SM};
                    font-size: {Typography.TEXT_2XL};
                    font-weight: {Typography.WEIGHT_BOLD};
                    color: {Colors.GRAY_900};
                    margin: 0 0 {Spacing.XS} 0;
                ">
                    {f'<span style="font-size: {Typography.TEXT_2XL};">{icon}</span>' if icon else ''}
                    {title}
                </h3>''' if title else ''}
                {f'<p style="color: {Colors.GRAY_600}; margin: 0; font-size: {Typography.TEXT_BASE};">{description}</p>' if description else ''}
            </div>
            """
            st.markdown(title_html, unsafe_allow_html=True)

        # Container de la sección
        st.markdown(f"""
        <div style="
            background: {background};
            padding: {padding};
            margin-bottom: {margin_bottom};
            border-radius: {BorderRadius.BASE if background != "transparent" else "0"};
        ">
        """, unsafe_allow_html=True)

        yield

        st.markdown("</div>", unsafe_allow_html=True)


def page_divider(
    margin: str = Spacing.XL,
    color: str = Colors.GRAY_200,
    thickness: str = "1px",
    style: Literal["solid", "dashed", "dotted"] = "solid"
) -> None:
    """
    Renderiza un divisor visual horizontal.

    Args:
        margin: Margen vertical (arriba y abajo)
        color: Color de la línea
        thickness: Grosor de la línea
        style: Estilo de la línea ("solid", "dashed", "dotted")

    Returns:
        None: Renderiza directamente en Streamlit

    Example:
        >>> st.write("Sección 1")
        >>> page_divider()
        >>> st.write("Sección 2")
        >>> page_divider(style="dashed", color=Colors.PRIMARY)
        >>> st.write("Sección 3")
    """
    st.markdown(f"""
    <div style="
        margin: {margin} 0;
        border-bottom: {thickness} {style} {color};
    "></div>
    """, unsafe_allow_html=True)


def page_footer(
    content: Optional[str] = None,
    links: Optional[List[Dict[str, str]]] = None,
    copyright: Optional[str] = None,
    background: str = Colors.GRAY_100,
    show_divider: bool = True
) -> None:
    """
    Renderiza un footer de página consistente.

    Args:
        content: Contenido principal del footer (markdown)
        links: Lista de links [{"label": "Ayuda", "url": "/help"}]
        copyright: Texto de copyright
        background: Color de fondo del footer
        show_divider: Mostrar línea divisoria arriba del footer

    Returns:
        None: Renderiza directamente en Streamlit

    Example:
        >>> page_footer(
        ...     content="Mi App Finanzas - Gestiona tus finanzas personales",
        ...     links=[
        ...         {"label": "Ayuda", "url": "/help"},
        ...         {"label": "Privacidad", "url": "/privacy"}
        ...     ],
        ...     copyright="© 2025 Mi App Finanzas"
        ... )
    """
    if show_divider:
        page_divider(margin=Spacing.XXL, color=Colors.GRAY_300)

    footer_html = f"""
    <div style="
        background: {background};
        padding: {Spacing.XXL} {Spacing.XL};
        margin-top: {Spacing.XXXL};
        border-radius: {BorderRadius.LG};
        text-align: center;
    ">
    """

    # Contenido principal
    if content:
        footer_html += f"""
        <p style="
            font-size: {Typography.TEXT_BASE};
            color: {Colors.GRAY_700};
            margin-bottom: {Spacing.LG};
        ">{content}</p>
        """

    # Links
    if links:
        footer_html += f"""
        <div style="
            display: flex;
            justify-content: center;
            gap: {Spacing.XL};
            margin-bottom: {Spacing.LG};
            flex-wrap: wrap;
        ">
        """
        for idx, link in enumerate(links):
            label = link.get("label", "")
            url = link.get("url", "#")
            footer_html += f"""
            <style>
                .footer-link-{idx}:hover {{
                    color: {Colors.PRIMARY_LIGHT} !important;
                }}
            </style>
            <a href="{url}" class="footer-link-{idx}" style="
                color: {Colors.PRIMARY};
                text-decoration: none;
                font-size: {Typography.TEXT_SM};
                font-weight: {Typography.WEIGHT_MEDIUM};
                transition: color {Transitions.FAST} {Transitions.EASING_DEFAULT};
            ">
                {label}
            </a>
            """
        footer_html += "</div>"

    # Copyright
    if copyright:
        footer_html += f"""
        <p style="
            font-size: {Typography.TEXT_XS};
            color: {Colors.GRAY_500};
            margin: 0;
        ">{copyright}</p>
        """

    footer_html += "</div>"
    st.markdown(footer_html, unsafe_allow_html=True)


# ============================================================================
# FUNCIONES PRIVADAS - INTERNAL HELPERS
# ============================================================================

def _inject_page_container_styles(
    max_width: str,
    padding: str,
    background: str
) -> None:
    """
    Inyecta estilos CSS globales para el container de la página.

    Args:
        max_width: Ancho máximo del container
        padding: Padding del container
        background: Color de fondo
    """
    st.markdown(f"""
    <style>
    /* PageLayout Container Styles */
    .main .block-container {{
        max-width: {max_width};
        padding: {padding};
        background: {background};
    }}

    /* Responsive padding */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: {Spacing.LG} {Spacing.MD};
        }}
    }}

    /* Smooth scrolling */
    html {{
        scroll-behavior: smooth;
    }}

    /* Hide Streamlit branding if feature flag enabled */
    {'#MainMenu {visibility: hidden;} footer {visibility: hidden;}' if is_enabled('RESPONSIVE_MOBILE') else ''}
    </style>
    """, unsafe_allow_html=True)


def _render_with_sidebar(
    content_fn: Callable,
    sidebar_fn: Optional[Callable],
    sidebar_width: str,
    sidebar_position: Literal["left", "right"]
) -> None:
    """
    Renderiza contenido con sidebar lateral.

    Args:
        content_fn: Función de contenido principal
        sidebar_fn: Función de contenido del sidebar
        sidebar_width: Ancho del sidebar (ej: "300px")
        sidebar_position: Posición del sidebar ("left" o "right")
    """
    # Calcular proporción de columnas
    # sidebar_width como porcentaje aprox
    sidebar_proportion = 1
    content_proportion = 3

    if sidebar_position == "left":
        col_sidebar, col_content = st.columns([sidebar_proportion, content_proportion], gap="large")
    else:
        col_content, col_sidebar = st.columns([content_proportion, sidebar_proportion], gap="large")

    # Renderizar sidebar
    with col_sidebar:
        st.markdown(f"""
        <div style="
            background: {Colors.BG_SECONDARY};
            padding: {Spacing.LG};
            border-radius: {BorderRadius.LG};
            border: 1px solid {Colors.GRAY_200};
            position: sticky;
            top: {Spacing.LG};
        ">
        """, unsafe_allow_html=True)

        if sidebar_fn:
            sidebar_fn()

        st.markdown("</div>", unsafe_allow_html=True)

    # Renderizar contenido principal
    with col_content:
        content_fn()


def _render_header_actions(actions: List[Dict[str, Any]]) -> None:
    """
    Renderiza acciones en el header (botones, selectores, etc).

    Args:
        actions: Lista de acciones [{"type": "period_selector"|"export_button"|"back_button"}]
    """
    # Container para acciones
    st.markdown(f'<div style="margin-bottom: {Spacing.LG};"></div>', unsafe_allow_html=True)

    for action in actions:
        action_type = action.get("type")

        if action_type == "period_selector":
            _render_period_selector_action()

        elif action_type == "export_button":
            _render_export_button_action()

        elif action_type == "back_button":
            _render_back_button_action()

        # Custom action con callback
        elif action_type == "custom" and "label" in action:
            label = action.get("label")
            icon = action.get("icon", "")
            callback = action.get("callback")

            if st.button(f"{icon} {label}" if icon else label):
                if callback:
                    callback()


def _render_period_selector_action() -> None:
    """Renderiza selector de período (mes/año)."""
    from datetime import datetime

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        current_year = datetime.now().year
        years = list(range(current_year - 5, current_year + 2))
        selected_year = st.selectbox(
            "Año",
            years,
            index=years.index(current_year) if current_year in years else 0,
            key="page_layout_year"
        )

    with col2:
        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        current_month = datetime.now().month
        selected_month = st.selectbox(
            "Mes",
            months,
            index=current_month - 1,
            key="page_layout_month"
        )

    with col3:
        st.info(f"📅 Mostrando datos de **{selected_month} {selected_year}**")

    # Guardar selección en session_state para que otras partes de la app la usen
    st.session_state["selected_year"] = selected_year
    st.session_state["selected_month"] = months.index(selected_month) + 1


def _render_export_button_action() -> None:
    """Renderiza botón de exportar."""
    col1, col2, col3 = st.columns([3, 1, 1])

    with col2:
        if st.button("📥 Exportar", use_container_width=True):
            st.info("Funcionalidad de exportación próximamente...")


def _render_back_button_action() -> None:
    """Renderiza botón de volver."""
    if st.button("← Volver", use_container_width=False):
        # En Streamlit no hay navegación directa, pero podemos usar session_state
        st.info("Usa el sidebar para navegar")


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Función principal
    "render_page_layout",

    # Layouts predefinidos
    "render_dashboard_layout",
    "render_form_layout",
    "render_table_layout",
    "render_detail_layout",

    # Helpers
    "page_header",
    "page_breadcrumbs",
    "page_section",
    "page_divider",
    "page_footer",
]
