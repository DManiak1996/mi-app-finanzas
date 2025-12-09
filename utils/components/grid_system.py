"""
Grid System - Sistema de grillas responsive para layouts flexibles

Sistema moderno de grillas basado en CSS Grid con fallback a flexbox.
Proporciona layouts responsive automáticos con configuración simple.

Características:
- CSS Grid nativo con auto-fill y auto-fit
- Responsive por defecto (desktop/tablet/mobile)
- Gaps configurables usando design_tokens
- Variantes especializadas (cards, metrics, images, masonry)
- Helpers para configuración avanzada

Uso básico:
    from utils.components.grid_system import render_grid, grid_item

    # Grid simple de 3 columnas
    items = [content1, content2, content3]
    render_grid(items, cols=3)

    # Grid responsive automático
    render_grid(items, cols=4, gap='lg', responsive=True)

Autor: Claude Code
Fecha: 2025-12-04
Referencia: ESTRATEGIA_OVERHAUL_DISEÑO.md - Sección 4.3
"""

import streamlit as st
from typing import List, Union, Literal, Optional, Callable
from utils.design_tokens import Spacing, Colors, BorderRadius, Breakpoints


# Tipos para type hints
GapSize = Literal['xs', 'sm', 'md', 'lg', 'xl']
GridColumns = Union[int, str]


def _get_spacing_value(gap: GapSize) -> str:
    """
    Convierte tamaño de gap a valor CSS usando design_tokens.

    Args:
        gap: Tamaño del gap ('xs', 'sm', 'md', 'lg', 'xl')

    Returns:
        Valor CSS del spacing (ej: '1rem')
    """
    spacing_map = {
        'xs': Spacing.XS,
        'sm': Spacing.SM,
        'md': Spacing.MD,
        'lg': Spacing.LG,
        'xl': Spacing.XL,
    }
    return spacing_map.get(gap, Spacing.MD)


def _generate_grid_css(
    cols: int,
    gap: str,
    responsive: bool,
    min_width: Optional[str] = None,
    auto_fit: bool = False,
    item_height: Optional[str] = None
) -> str:
    """
    Genera el CSS para el grid con todas las configuraciones.

    Args:
        cols: Número de columnas
        gap: Valor CSS del gap
        responsive: Si debe ser responsive
        min_width: Ancho mínimo para auto-grid (ej: '300px')
        auto_fit: Si usa auto-fit en lugar de auto-fill
        item_height: Altura fija de items (ej: '200px')

    Returns:
        String con el CSS del grid
    """

    # Determinar el valor de grid-template-columns
    if min_width:
        # Auto-grid basado en ancho mínimo
        repeat_mode = 'auto-fit' if auto_fit else 'auto-fill'
        grid_cols = f"repeat({repeat_mode}, minmax({min_width}, 1fr))"
    else:
        # Grid con columnas fijas
        grid_cols = f"repeat({cols}, 1fr)"

    # CSS base del grid
    css = f"""
    <style>
    .grid-container {{
        display: grid;
        grid-template-columns: {grid_cols};
        gap: {gap};
        width: 100%;
        margin: 0;
        padding: 0;
    }}

    .grid-item {{
        min-width: 0; /* Previene overflow en grid items */
        min-height: 0;
        {f'height: {item_height};' if item_height else ''}
    }}
    """

    # Agregar reglas responsive si está activado
    if responsive and not min_width:  # min_width ya es responsive por naturaleza
        # Calcular columnas para tablet y mobile
        tablet_cols = min(cols, 2)

        css += f"""
    /* Tablet: {Breakpoints.MD} - {Breakpoints.LG} */
    @media (max-width: {Breakpoints.LG}) and (min-width: {Breakpoints.MD}) {{
        .grid-container {{
            grid-template-columns: repeat({tablet_cols}, 1fr);
        }}
    }}

    /* Mobile: < {Breakpoints.MD} */
    @media (max-width: {Breakpoints.MD}) {{
        .grid-container {{
            grid-template-columns: 1fr;
            gap: {Spacing.MD}; /* Gap más pequeño en móvil */
        }}
    }}
    """

    css += """
    </style>
    """

    return css


def render_grid(
    items: List[any],
    cols: int = 3,
    gap: GapSize = 'md',
    responsive: bool = True,
    item_renderer: Optional[Callable] = None
) -> None:
    """
    Renderiza un grid responsive con los items proporcionados.

    Sistema de columnas configurable con breakpoints responsive automáticos:
    - Desktop (>1024px): n columnas configuradas
    - Tablet (768-1024px): min(n, 2) columnas
    - Mobile (<768px): 1 columna

    Args:
        items: Lista de contenidos a renderizar en el grid
        cols: Número de columnas (1-12)
        gap: Tamaño del gap ('xs', 'sm', 'md', 'lg', 'xl')
        responsive: Si debe aplicar breakpoints responsive automáticos
        item_renderer: Función opcional para renderizar cada item.
                       Si no se proporciona, se renderiza el item directamente.
                       Firma: item_renderer(item, index) -> None

    Ejemplo:
        >>> items = ["Card 1", "Card 2", "Card 3", "Card 4"]
        >>> render_grid(items, cols=2, gap='lg')

        >>> # Con renderer personalizado
        >>> def render_metric(item, idx):
        ...     st.metric(f"Métrica {idx}", item)
        >>> render_grid([100, 200, 300], cols=3, item_renderer=render_metric)
    """

    # Validación
    if not items:
        st.warning("No hay items para mostrar en el grid")
        return

    if cols < 1 or cols > 12:
        st.error("El número de columnas debe estar entre 1 y 12")
        return

    # Obtener valor del spacing
    gap_value = _get_spacing_value(gap)

    # Generar CSS
    css = _generate_grid_css(cols, gap_value, responsive)
    st.markdown(css, unsafe_allow_html=True)

    # Renderizar grid container
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)

    # Renderizar cada item
    for idx, item in enumerate(items):
        st.markdown('<div class="grid-item">', unsafe_allow_html=True)

        if item_renderer:
            item_renderer(item, idx)
        else:
            # Renderizar directamente
            if isinstance(item, str):
                st.markdown(item, unsafe_allow_html=True)
            else:
                st.write(item)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_card_grid(
    items: List[dict],
    cols: int = 3,
    gap: GapSize = 'md',
    responsive: bool = True
) -> None:
    """
    Renderiza un grid de cards con estilo consistente.

    Cada item debe ser un diccionario con las siguientes claves:
    - title: Título de la card
    - content: Contenido principal
    - footer: (opcional) Contenido del footer
    - color: (opcional) Color de acento

    Args:
        items: Lista de diccionarios con datos de las cards
        cols: Número de columnas
        gap: Tamaño del gap
        responsive: Si debe ser responsive

    Ejemplo:
        >>> cards = [
        ...     {"title": "Ingresos", "content": "2500€", "footer": "+15%"},
        ...     {"title": "Gastos", "content": "1800€", "footer": "-5%"},
        ...     {"title": "Balance", "content": "700€", "footer": "Positivo"}
        ... ]
        >>> render_card_grid(cards, cols=3)
    """

    def render_card(item: dict, idx: int) -> None:
        """Renderiza una card individual"""
        title = item.get('title', f'Card {idx + 1}')
        content = item.get('content', '')
        footer = item.get('footer', '')
        color = item.get('color', Colors.PRIMARY)

        card_html = f"""
        <div style="
            background: {Colors.BG_PRIMARY};
            border: 1px solid {Colors.GRAY_200};
            border-radius: {BorderRadius.BASE};
            padding: {Spacing.LG};
            height: 100%;
            box-shadow: {Colors.SHADOW_SM};
            transition: all 0.2s ease;
            border-top: 3px solid {color};
        ">
            <h3 style="
                margin: 0 0 {Spacing.MD} 0;
                color: {Colors.GRAY_700};
                font-size: 0.875rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">{title}</h3>
            <div style="
                margin: {Spacing.MD} 0;
                color: {Colors.GRAY_900};
                font-size: 1.5rem;
                font-weight: 700;
            ">{content}</div>
            {f'<div style="margin-top: {Spacing.SM}; color: {Colors.GRAY_600}; font-size: 0.875rem;">{footer}</div>' if footer else ''}
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    render_grid(items, cols, gap, responsive, item_renderer=render_card)


def render_metric_grid(
    metrics: List[dict],
    cols: int = 4,
    gap: GapSize = 'md',
    responsive: bool = True
) -> None:
    """
    Renderiza un grid optimizado para métricas financieras.

    Cada métrica debe ser un diccionario con:
    - label: Etiqueta de la métrica
    - value: Valor principal
    - delta: (opcional) Cambio/delta
    - delta_color: (opcional) Color del delta
    - help: (opcional) Texto de ayuda

    Args:
        metrics: Lista de diccionarios con datos de métricas
        cols: Número de columnas
        gap: Tamaño del gap
        responsive: Si debe ser responsive

    Ejemplo:
        >>> metrics = [
        ...     {"label": "Ingresos", "value": "2500€", "delta": "+15%"},
        ...     {"label": "Gastos", "value": "1800€", "delta": "-5%"},
        ...     {"label": "Balance", "value": "700€", "delta": "+10%"}
        ... ]
        >>> render_metric_grid(metrics, cols=3)
    """

    def render_metric(metric: dict, idx: int) -> None:
        """Renderiza una métrica individual usando st.metric"""
        label = metric.get('label', f'Métrica {idx + 1}')
        value = metric.get('value', '—')
        delta = metric.get('delta', None)
        delta_color = metric.get('delta_color', 'normal')
        help_text = metric.get('help', None)

        st.metric(
            label=label,
            value=value,
            delta=delta,
            delta_color=delta_color,
            help=help_text
        )

    render_grid(metrics, cols, gap, responsive, item_renderer=render_metric)


def render_image_grid(
    images: List[dict],
    cols: int = 3,
    gap: GapSize = 'sm',
    responsive: bool = True,
    aspect_ratio: str = "1/1"
) -> None:
    """
    Renderiza un grid optimizado para imágenes/media.

    Cada imagen debe ser un diccionario con:
    - url: URL o path de la imagen
    - caption: (opcional) Caption de la imagen
    - alt: (opcional) Texto alternativo

    Args:
        images: Lista de diccionarios con datos de imágenes
        cols: Número de columnas
        gap: Tamaño del gap
        responsive: Si debe ser responsive
        aspect_ratio: Aspect ratio de las imágenes (ej: "16/9", "4/3", "1/1")

    Ejemplo:
        >>> images = [
        ...     {"url": "image1.jpg", "caption": "Imagen 1"},
        ...     {"url": "image2.jpg", "caption": "Imagen 2"},
        ... ]
        >>> render_image_grid(images, cols=3, aspect_ratio="16/9")
    """

    def render_image(image: dict, idx: int) -> None:
        """Renderiza una imagen individual"""
        url = image.get('url', '')
        caption = image.get('caption', '')
        alt = image.get('alt', caption or f'Image {idx + 1}')

        image_html = f"""
        <div style="
            position: relative;
            width: 100%;
            aspect-ratio: {aspect_ratio};
            overflow: hidden;
            border-radius: {BorderRadius.BASE};
            background: {Colors.GRAY_100};
        ">
            <img
                src="{url}"
                alt="{alt}"
                style="
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    display: block;
                "
            />
        </div>
        {f'<p style="margin-top: {Spacing.SM}; color: {Colors.GRAY_600}; font-size: 0.875rem; text-align: center;">{caption}</p>' if caption else ''}
        """
        st.markdown(image_html, unsafe_allow_html=True)

    render_grid(images, cols, gap, responsive, item_renderer=render_image)


def render_masonry_grid(
    items: List[any],
    cols: int = 3,
    gap: GapSize = 'md',
    responsive: bool = True,
    item_renderer: Optional[Callable] = None
) -> None:
    """
    Renderiza un grid tipo masonry (Pinterest-style) con heights variables.

    Nota: Esta es una implementación simple usando CSS columns.
    Para masonry real con mejor control, considerar usar una librería JS.

    Args:
        items: Lista de contenidos a renderizar
        cols: Número de columnas
        gap: Tamaño del gap
        responsive: Si debe ser responsive
        item_renderer: Función para renderizar cada item

    Ejemplo:
        >>> items = [
        ...     "Contenido corto",
        ...     "Contenido más largo que ocupa más espacio vertical...",
        ...     "Contenido medio"
        ... ]
        >>> render_masonry_grid(items, cols=3)
    """

    gap_value = _get_spacing_value(gap)

    # CSS para masonry usando columns
    masonry_css = f"""
    <style>
    .masonry-container {{
        column-count: {cols};
        column-gap: {gap_value};
        width: 100%;
    }}

    .masonry-item {{
        break-inside: avoid;
        margin-bottom: {gap_value};
        background: {Colors.BG_PRIMARY};
        border: 1px solid {Colors.GRAY_200};
        border-radius: {BorderRadius.BASE};
        padding: {Spacing.LG};
    }}
    """

    if responsive:
        tablet_cols = min(cols, 2)

        masonry_css += f"""
    @media (max-width: {Breakpoints.LG}) and (min-width: {Breakpoints.MD}) {{
        .masonry-container {{
            column-count: {tablet_cols};
        }}
    }}

    @media (max-width: {Breakpoints.MD}) {{
        .masonry-container {{
            column-count: 1;
            column-gap: {Spacing.MD};
        }}
    }}
    """

    masonry_css += """
    </style>
    """

    st.markdown(masonry_css, unsafe_allow_html=True)

    # Renderizar masonry container
    st.markdown('<div class="masonry-container">', unsafe_allow_html=True)

    for idx, item in enumerate(items):
        st.markdown('<div class="masonry-item">', unsafe_allow_html=True)

        if item_renderer:
            item_renderer(item, idx)
        else:
            if isinstance(item, str):
                st.markdown(item, unsafe_allow_html=True)
            else:
                st.write(item)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def grid_item(
    content: any,
    span: int = 1,
    row_span: int = 1
) -> dict:
    """
    Crea un item de grid con colspan/rowspan personalizado.

    Args:
        content: Contenido del item
        span: Número de columnas que ocupa (colspan)
        row_span: Número de filas que ocupa (rowspan)

    Returns:
        Diccionario con la configuración del item

    Nota: Para usar spans personalizados, necesitas renderizar manualmente
          con HTML/CSS personalizado o usar st.columns con proporciones.

    Ejemplo:
        >>> item1 = grid_item("Contenido normal", span=1)
        >>> item2 = grid_item("Contenido ancho", span=2)
        >>> item3 = grid_item("Contenido alto", span=1, row_span=2)
    """
    return {
        'content': content,
        'span': span,
        'row_span': row_span
    }


def auto_grid(
    items: List[any],
    min_width: str = '300px',
    gap: GapSize = 'md',
    responsive: bool = True,
    item_renderer: Optional[Callable] = None
) -> None:
    """
    Renderiza un grid automático basado en ancho mínimo de items.

    Usa CSS Grid auto-fill para crear automáticamente tantas columnas
    como quepan respetando el ancho mínimo especificado.

    Args:
        items: Lista de contenidos a renderizar
        min_width: Ancho mínimo de cada item (ej: '300px', '250px', '20rem')
        gap: Tamaño del gap
        responsive: Si debe ajustar el min_width en móvil
        item_renderer: Función para renderizar cada item

    Ejemplo:
        >>> items = [card1, card2, card3, card4, card5]
        >>> auto_grid(items, min_width='280px')
        >>> # Creará automáticamente 3 columnas en pantallas grandes,
        >>> # 2 en medianas, 1 en pequeñas
    """

    gap_value = _get_spacing_value(gap)

    # Ajustar min_width para móvil si responsive está activado
    mobile_min_width = '100%' if responsive else min_width

    # Generar CSS con auto-fill
    css = f"""
    <style>
    .auto-grid-container {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax({min_width}, 1fr));
        gap: {gap_value};
        width: 100%;
    }}

    .auto-grid-item {{
        min-width: 0;
        min-height: 0;
    }}
    """

    if responsive:
        css += f"""
    @media (max-width: {Breakpoints.MD}) {{
        .auto-grid-container {{
            grid-template-columns: repeat(auto-fill, minmax({mobile_min_width}, 1fr));
            gap: {Spacing.MD};
        }}
    }}
    """

    css += """
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

    # Renderizar grid
    st.markdown('<div class="auto-grid-container">', unsafe_allow_html=True)

    for idx, item in enumerate(items):
        st.markdown('<div class="auto-grid-item">', unsafe_allow_html=True)

        if item_renderer:
            item_renderer(item, idx)
        else:
            if isinstance(item, str):
                st.markdown(item, unsafe_allow_html=True)
            else:
                st.write(item)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def responsive_columns(
    desktop: int = 4,
    tablet: int = 2,
    mobile: int = 1,
    gap: GapSize = 'md'
) -> str:
    """
    Genera CSS personalizado para configuración responsive explícita.

    Útil cuando necesitas control exacto sobre el número de columnas
    en cada breakpoint.

    Args:
        desktop: Columnas en desktop (>1024px)
        tablet: Columnas en tablet (768-1024px)
        mobile: Columnas en móvil (<768px)
        gap: Tamaño del gap

    Returns:
        String con el CSS para incluir con st.markdown(..., unsafe_allow_html=True)

    Ejemplo:
        >>> css = responsive_columns(desktop=4, tablet=2, mobile=1, gap='lg')
        >>> st.markdown(css, unsafe_allow_html=True)
        >>> st.markdown('<div class="responsive-grid">...items...</div>', unsafe_allow_html=True)
    """

    gap_value = _get_spacing_value(gap)

    css = f"""
    <style>
    .responsive-grid {{
        display: grid;
        grid-template-columns: repeat({desktop}, 1fr);
        gap: {gap_value};
        width: 100%;
    }}

    @media (max-width: {Breakpoints.LG}) and (min-width: {Breakpoints.MD}) {{
        .responsive-grid {{
            grid-template-columns: repeat({tablet}, 1fr);
        }}
    }}

    @media (max-width: {Breakpoints.MD}) {{
        .responsive-grid {{
            grid-template-columns: repeat({mobile}, 1fr);
            gap: {Spacing.MD};
        }}
    }}
    </style>
    """

    return css


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def _example_basic_grid():
    """Ejemplo: Grid básico de 3 columnas"""
    st.subheader("Grid Básico (3 columnas)")

    items = [
        "Contenido 1",
        "Contenido 2",
        "Contenido 3",
        "Contenido 4",
        "Contenido 5",
        "Contenido 6"
    ]

    render_grid(items, cols=3, gap='md')


def _example_card_grid():
    """Ejemplo: Grid de cards"""
    st.subheader("Card Grid")

    cards = [
        {
            "title": "Ingresos",
            "content": "2,500€",
            "footer": "+15% vs mes anterior",
            "color": Colors.SUCCESS
        },
        {
            "title": "Gastos",
            "content": "1,800€",
            "footer": "-5% vs mes anterior",
            "color": Colors.ERROR
        },
        {
            "title": "Balance",
            "content": "700€",
            "footer": "Ahorro positivo",
            "color": Colors.PRIMARY
        },
        {
            "title": "Tasa Ahorro",
            "content": "28%",
            "footer": "Objetivo: 20%",
            "color": Colors.SUCCESS
        }
    ]

    render_card_grid(cards, cols=4, gap='lg')


def _example_metric_grid():
    """Ejemplo: Grid de métricas"""
    st.subheader("Metric Grid")

    metrics = [
        {"label": "Total Ingresos", "value": "2,500€", "delta": "+15%"},
        {"label": "Total Gastos", "value": "1,800€", "delta": "-5%", "delta_color": "inverse"},
        {"label": "Balance", "value": "700€", "delta": "+10%"},
        {"label": "Tasa Ahorro", "value": "28%", "delta": "+3%"}
    ]

    render_metric_grid(metrics, cols=4, gap='md')


def _example_auto_grid():
    """Ejemplo: Auto grid"""
    st.subheader("Auto Grid (min-width: 250px)")

    items = [f"Item {i+1}" for i in range(8)]

    auto_grid(items, min_width='250px', gap='md')


if __name__ == "__main__":
    # Demo completo del sistema Grid
    st.set_page_config(page_title="Grid System Demo", layout="wide")

    st.title("Grid System - Sistema de Grillas Responsive")
    st.markdown("---")

    # Ejemplos
    _example_basic_grid()
    st.markdown("---")

    _example_card_grid()
    st.markdown("---")

    _example_metric_grid()
    st.markdown("---")

    _example_auto_grid()
