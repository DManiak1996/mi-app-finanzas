# utils/design_tokens.py
"""
Design Tokens - Sistema de diseño centralizado
Basado en Material Design 3 adaptado para finanzas personales

Este módulo centraliza TODOS los valores de diseño visual:
- Colores semánticos
- Tipografía
- Spacing
- Border radius
- Sombras y transiciones

Uso:
    from utils.design_tokens import Colors, Typography, Spacing

    # En lugar de:
    color = "#26a69a"  # ❌ Hardcoded

    # Usar:
    color = Colors.SUCCESS  # ✅ Semántico
"""


class Colors:
    """
    Paleta de colores semánticos

    Nomenclatura:
    - PRIMARY: Color principal de la marca
    - SUCCESS: Operaciones exitosas, ingresos, positivo
    - WARNING: Advertencias, estados intermedios
    - ERROR: Errores, gastos, negativo
    - GRAY_XXX: Escala de grises para textos y backgrounds
    """

    # === COLORES PRIMARIOS ===
    PRIMARY = "#1f77b4"          # Azul corporativo (del theme)
    PRIMARY_LIGHT = "#6fa8dc"    # Azul claro (hover, secondary)
    PRIMARY_DARK = "#0c5aa6"     # Azul oscuro (active, emphasis)
    PRIMARY_ULTRA_LIGHT = "#e3f2fd"  # Backgrounds sutiles

    # === COLORES SEMÁNTICOS FINANCIEROS ===
    SUCCESS = "#26a69a"          # Verde (ingresos, positivo, OK)
    SUCCESS_LIGHT = "#4db6ac"
    SUCCESS_DARK = "#00897b"
    SUCCESS_ULTRA_LIGHT = "#e0f2f1"

    WARNING = "#ff9800"          # Naranja (advertencia, medio)
    WARNING_LIGHT = "#ffb74d"
    WARNING_DARK = "#f57c00"
    WARNING_ULTRA_LIGHT = "#fff3e0"

    ERROR = "#ef5350"            # Rojo (gastos, negativo, alerta)
    ERROR_LIGHT = "#e57373"
    ERROR_DARK = "#c62828"
    ERROR_ULTRA_LIGHT = "#ffebee"

    # === GRISES (Neutrales) ===
    GRAY_900 = "#262730"         # Texto principal (del theme)
    GRAY_800 = "#2d2e38"
    GRAY_700 = "#31333F"         # Texto secundario
    GRAY_600 = "#4a4c5a"
    GRAY_500 = "#757575"         # Texto deshabilitado
    GRAY_400 = "#9e9e9e"
    GRAY_300 = "#bdbdbd"         # Bordes
    GRAY_200 = "#e0e0e0"
    GRAY_100 = "#f0f2f6"         # Backgrounds secundarios (del theme)
    GRAY_50 = "#fafafa"          # Backgrounds hover

    # === BACKGROUNDS ===
    BG_PRIMARY = "#ffffff"       # Fondo principal (del theme)
    BG_SECONDARY = "#f8f9fa"     # Fondo secundario (más claro)
    BG_TERTIARY = "#fafafa"      # Fondo terciario
    BG_DARK = "#1a1a1a"          # Para dark mode (futuro)

    # === COLORES ESPECÍFICOS DE LA APP ===
    CHART_INCOME = SUCCESS       # Ingresos en gráficos
    CHART_EXPENSE = ERROR        # Gastos en gráficos
    CHART_BALANCE = PRIMARY      # Balance en gráficos
    CHART_NEUTRAL = GRAY_500     # Líneas auxiliares

    # === PRESUPUESTOS ===
    BUDGET_OK = SUCCESS          # <70% usado
    BUDGET_WARNING = WARNING     # 70-90% usado
    BUDGET_OVER = ERROR          # >90% usado

    # === OVERLAYS Y SOMBRAS ===
    OVERLAY_LIGHT = "rgba(0, 0, 0, 0.05)"
    OVERLAY_MEDIUM = "rgba(0, 0, 0, 0.12)"
    OVERLAY_DARK = "rgba(0, 0, 0, 0.24)"

    SHADOW_SM = "0 1px 2px rgba(0,0,0,0.05)"
    SHADOW_MD = "0 4px 6px rgba(0,0,0,0.07)"
    SHADOW_LG = "0 10px 15px rgba(0,0,0,0.1)"
    SHADOW_XL = "0 20px 25px rgba(0,0,0,0.15)"

    # === GRADIENTES ===
    GRADIENT_PRIMARY = f"linear-gradient(135deg, {BG_PRIMARY} 0%, {BG_SECONDARY} 100%)"
    GRADIENT_SUCCESS = f"linear-gradient(135deg, {SUCCESS_ULTRA_LIGHT} 0%, {SUCCESS_LIGHT}30 100%)"
    GRADIENT_ERROR = f"linear-gradient(135deg, {ERROR_ULTRA_LIGHT} 0%, {ERROR_LIGHT}30 100%)"

    # === 🎨 FINTECH PREMIUM PALETTE ===
    # Gradientes vibrantes para UI premium - Tema Verde Oscuro a Lima
    PREMIUM_PRIMARY_START = "#0a4c3e"      # Verde oscuro profundo (90%)
    PREMIUM_PRIMARY_END = "#84cc16"        # Verde lima brillante (10%)
    PREMIUM_GRADIENT_PRIMARY = f"linear-gradient(135deg, {PREMIUM_PRIMARY_START} 0%, {PREMIUM_PRIMARY_END} 100%)"

    # Gradientes de acento
    PREMIUM_GOLD_START = "#f6d365"         # Dorado suave
    PREMIUM_GOLD_END = "#fda085"           # Coral-naranja
    PREMIUM_GRADIENT_GOLD = f"linear-gradient(135deg, {PREMIUM_GOLD_START} 0%, {PREMIUM_GOLD_END} 100%)"

    PREMIUM_TEAL_START = "#0d5f4e"         # Verde bosque profundo
    PREMIUM_TEAL_END = "#a3e635"           # Lima vibrante
    PREMIUM_GRADIENT_TEAL = f"linear-gradient(135deg, {PREMIUM_TEAL_START} 0%, {PREMIUM_TEAL_END} 100%)"

    PREMIUM_CORAL_START = "#fa709a"        # Rosa coral
    PREMIUM_CORAL_END = "#fee140"          # Amarillo suave
    PREMIUM_GRADIENT_CORAL = f"linear-gradient(135deg, {PREMIUM_CORAL_START} 0%, {PREMIUM_CORAL_END} 100%)"

    PREMIUM_SKY_START = "#4facfe"          # Azul cielo
    PREMIUM_SKY_END = "#00f2fe"            # Cyan brillante
    PREMIUM_GRADIENT_SKY = f"linear-gradient(135deg, {PREMIUM_SKY_START} 0%, {PREMIUM_SKY_END} 100%)"

    # Gradiente de fondo sutil - tema verde
    PREMIUM_BG_GRADIENT = "linear-gradient(180deg, #ffffff 0%, #f0fdf4 100%)"
    PREMIUM_CARD_GRADIENT = "linear-gradient(135deg, #ffffff 0%, #f7fee7 100%)"

    # === 💎 GLASSMORPHISM ===
    GLASS_BG = "rgba(255, 255, 255, 0.7)"
    GLASS_BG_DARK = "rgba(255, 255, 255, 0.1)"
    GLASS_BORDER = "rgba(255, 255, 255, 0.3)"
    GLASS_BACKDROP = "blur(10px)"
    GLASS_SHADOW = "0 8px 32px rgba(31, 38, 135, 0.15)"

    # === 🌈 SOMBRAS MULTICAPA (Profundidad realista) ===
    SHADOW_PREMIUM_XS = "0 1px 2px rgba(0,0,0,0.05)"
    SHADOW_PREMIUM_SM = """0 2px 4px rgba(0,0,0,0.06),
                           0 1px 2px rgba(0,0,0,0.04)"""
    SHADOW_PREMIUM_MD = """0 4px 6px rgba(0,0,0,0.07),
                           0 2px 4px rgba(0,0,0,0.05),
                           0 1px 2px rgba(0,0,0,0.04)"""
    SHADOW_PREMIUM_LG = """0 10px 15px rgba(0,0,0,0.08),
                           0 4px 6px rgba(0,0,0,0.06),
                           0 2px 4px rgba(0,0,0,0.04)"""
    SHADOW_PREMIUM_XL = """0 20px 25px rgba(0,0,0,0.10),
                           0 10px 10px rgba(0,0,0,0.04),
                           0 0 0 1px rgba(0,0,0,0.02)"""
    SHADOW_PREMIUM_2XL = """0 25px 50px rgba(0,0,0,0.15),
                            0 12px 25px rgba(0,0,0,0.08)"""

    # Sombras con color (glow effects) - tema verde
    SHADOW_GLOW_PRIMARY = "0 0 20px rgba(10, 76, 62, 0.4)"      # Verde oscuro con alpha
    SHADOW_GLOW_SUCCESS = "0 0 20px rgba(13, 95, 78, 0.4)"      # Verde bosque con alpha
    SHADOW_GLOW_ERROR = "0 0 20px rgba(250, 112, 154, 0.4)"     # #fa709a con alpha

    # === 🎯 ACENTOS PREMIUM ===
    ACCENT_GOLD = PREMIUM_GOLD_START       # Para highlights especiales
    ACCENT_CORAL = PREMIUM_CORAL_START     # Para CTAs importantes
    ACCENT_TEAL = PREMIUM_TEAL_START       # Para info y success
    ACCENT_SKY = PREMIUM_SKY_START         # Para links y acciones secundarias


class Typography:
    """Sistema tipográfico basado en mejores prácticas de legibilidad"""

    # === FONT FAMILIES ===
    FONT_PRIMARY = "'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    FONT_MONO = "'Fira Code', 'SF Mono', 'Roboto Mono', 'Consolas', monospace"

    # === FONT SIZES (Mobile First - Base 16px) ===
    TEXT_XS = "0.75rem"     # 12px - Captions, footnotes
    TEXT_SM = "0.875rem"    # 14px - Secondary text, labels
    TEXT_BASE = "1rem"      # 16px - Body text, inputs
    TEXT_LG = "1.125rem"    # 18px - Emphasized text
    TEXT_XL = "1.25rem"     # 20px - Small headings
    TEXT_2XL = "1.5rem"     # 24px - Headings h3
    TEXT_3XL = "1.875rem"   # 30px - Headings h2
    TEXT_4XL = "2.25rem"    # 36px - Headings h1
    TEXT_5XL = "3rem"       # 48px - Display text, scores
    TEXT_6XL = "3.75rem"    # 60px - Hero text

    # === FONT WEIGHTS ===
    WEIGHT_LIGHT = "300"
    WEIGHT_NORMAL = "400"
    WEIGHT_MEDIUM = "500"
    WEIGHT_SEMIBOLD = "600"
    WEIGHT_BOLD = "700"
    WEIGHT_EXTRABOLD = "800"

    # === LINE HEIGHTS ===
    LEADING_NONE = "1"
    LEADING_TIGHT = "1.25"
    LEADING_SNUG = "1.375"
    LEADING_NORMAL = "1.5"
    LEADING_RELAXED = "1.75"
    LEADING_LOOSE = "2"

    # === LETTER SPACING ===
    TRACKING_TIGHTER = "-0.05em"
    TRACKING_TIGHT = "-0.025em"
    TRACKING_NORMAL = "0"
    TRACKING_WIDE = "0.025em"
    TRACKING_WIDER = "0.05em"
    TRACKING_WIDEST = "0.1em"


class Spacing:
    """
    Sistema de spacing consistente (múltiplos de 4px)
    Basado en escala de 8pt grid system
    """

    NONE = "0"
    XXS = "0.125rem"  # 2px
    XS = "0.25rem"    # 4px
    SM = "0.5rem"     # 8px
    MD = "0.75rem"    # 12px
    BASE = "1rem"     # 16px
    LG = "1.5rem"     # 24px
    XL = "2rem"       # 32px
    XXL = "3rem"      # 48px
    XXXL = "4rem"     # 64px
    XXXXL = "6rem"    # 96px


class BorderRadius:
    """Radios de borde consistentes"""

    NONE = "0"
    SM = "0.25rem"    # 4px - Inputs, small buttons
    BASE = "0.5rem"   # 8px - Cards, containers
    MD = "0.75rem"    # 12px - Large cards
    LG = "1rem"       # 16px - Modals, special elements
    XL = "1.5rem"     # 24px - Hero sections
    FULL = "9999px"   # Circular/pill


class Transitions:
    """Tiempos de transición estándar para animaciones suaves"""

    FASTEST = "100ms"
    FAST = "150ms"
    BASE = "250ms"
    SLOW = "350ms"
    SLOWEST = "500ms"

    # Easing functions (cubic-bezier)
    EASING_DEFAULT = "cubic-bezier(0.4, 0, 0.2, 1)"  # ease-in-out
    EASING_IN = "cubic-bezier(0.4, 0, 1, 1)"         # ease-in
    EASING_OUT = "cubic-bezier(0, 0, 0.2, 1)"        # ease-out
    EASING_SHARP = "cubic-bezier(0.4, 0, 0.6, 1)"    # sharp
    EASING_BOUNCE = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"  # bounce


class Breakpoints:
    """Breakpoints responsivos estándar"""

    XS = "320px"   # Mobile small
    SM = "480px"   # Mobile
    MD = "768px"   # Tablet
    LG = "1024px"  # Desktop
    XL = "1280px"  # Desktop large
    XXL = "1536px" # Desktop XL


# === FUNCIONES HELPER ===

def rgba_from_hex(hex_color: str, alpha: float) -> str:
    """
    Convierte un color hexadecimal a rgba con opacidad

    Args:
        hex_color: Color en formato hex (#RRGGBB)
        alpha: Opacidad (0.0 - 1.0)

    Returns:
        Color en formato rgba(r, g, b, alpha)

    Ejemplo:
        >>> rgba_from_hex("#1f77b4", 0.5)
        'rgba(31, 119, 180, 0.5)'
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def get_contrast_text(bg_color: str) -> str:
    """
    Devuelve color de texto con contraste adecuado (blanco o negro)
    basado en el color de fondo

    Args:
        bg_color: Color de fondo en formato hex

    Returns:
        Color de texto recomendado (#ffffff o #262730)

    Ejemplo:
        >>> get_contrast_text("#1f77b4")  # Fondo azul oscuro
        '#ffffff'  # Texto blanco
    """
    # Lista de colores oscuros que necesitan texto blanco
    dark_backgrounds = [
        Colors.PRIMARY_DARK,
        Colors.SUCCESS_DARK,
        Colors.ERROR_DARK,
        Colors.WARNING_DARK,
        Colors.GRAY_900,
        Colors.GRAY_800,
        Colors.GRAY_700,
        Colors.BG_DARK
    ]

    return "#ffffff" if bg_color in dark_backgrounds else Colors.GRAY_900


def get_budget_color(percentage_used: float) -> tuple[str, str, str]:
    """
    Devuelve colores apropiados para presupuestos según porcentaje usado

    Args:
        percentage_used: Porcentaje del presupuesto utilizado (0-100+)

    Returns:
        Tupla de (emoji, color, color_fondo)

    Ejemplo:
        >>> get_budget_color(50)
        ('🟢', '#26a69a', '#e0f2f1')
    """
    if percentage_used < 70:
        return ("🟢", Colors.BUDGET_OK, Colors.SUCCESS_ULTRA_LIGHT)
    elif percentage_used < 90:
        return ("🟡", Colors.BUDGET_WARNING, Colors.WARNING_ULTRA_LIGHT)
    else:
        return ("🔴", Colors.BUDGET_OVER, Colors.ERROR_ULTRA_LIGHT)


def spacer_html(size: str = "BASE") -> str:
    """
    Genera HTML para un espaciador vertical

    Args:
        size: Tamaño del espaciador (XS, SM, MD, BASE, LG, XL, etc.)

    Returns:
        HTML string para insertar con st.markdown(..., unsafe_allow_html=True)

    Ejemplo:
        >>> st.markdown(spacer_html("LG"), unsafe_allow_html=True)
    """
    spacing_value = getattr(Spacing, size, Spacing.BASE)
    return f"<div style='height: {spacing_value}'></div>"


# === CONSTANTES DE CONFIGURACIÓN ===

class Config:
    """Configuración general de la aplicación"""

    # Tamaños mínimos táctiles (WCAG AAA)
    MIN_TOUCH_TARGET = "44px"

    # Altura mínima de inputs (previene zoom iOS)
    MIN_INPUT_HEIGHT = "44px"
    MIN_INPUT_FONT_SIZE = "16px"

    # Anchos máximos para legibilidad
    MAX_TEXT_WIDTH = "65ch"  # Máximo ~65 caracteres por línea
    MAX_CONTAINER_WIDTH = "1400px"

    # Z-index layers
    Z_BASE = 1
    Z_DROPDOWN = 10
    Z_STICKY = 100
    Z_OVERLAY = 1000
    Z_MODAL = 1100
    Z_TOOLTIP = 1200
    Z_TOAST = 1300
