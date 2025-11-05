# utils/brand_assets.py
"""
Brand Assets - Logo y elementos visuales de la marca
Incluye SVGs inline para logo, iconos y patterns
"""

# === LOGO PRINCIPAL ===
LOGO_SVG = """
<svg width="180" height="48" viewBox="0 0 180 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    
    <defs>
        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#f6d365;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#fda085;stop-opacity:1" />
        </linearGradient>
    </defs>

    <g transform="translate(4, 4)">
        
        <circle cx="20" cy="20" r="18" fill="url(#logoGradient)" opacity="0.1"/>
        <circle cx="20" cy="20" r="18" stroke="url(#logoGradient)" stroke-width="2.5" fill="none"/>

        <path d="M 10 25 L 15 20 L 20 18 L 25 12 L 30 10"
              stroke="url(#logoGradient)"
              stroke-width="2.5"
              stroke-linecap="round"
              stroke-linejoin="round"
              fill="none"/>

        <circle cx="15" cy="20" r="2.5" fill="url(#accentGradient)"/>
        <circle cx="20" cy="18" r="2.5" fill="url(#accentGradient)"/>
        <circle cx="25" cy="12" r="2.5" fill="url(#accentGradient)"/>
        <circle cx="30" cy="10" r="3" fill="url(#accentGradient)"/>
    </g>

    <text x="54" y="20"
          font-family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
          font-size="18"
          font-weight="700"
          fill="#262730">
        FinanzasFlow
    </text>
    <text x="54" y="36"
          font-family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
          font-size="9"
          font-weight="500"
          fill="#757575"
          letter-spacing="0.5">
        CONTROL FINANCIERO PREMIUM
    </text>
</svg>
"""

LOGO_ICON_ONLY = """
<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="iconGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="iconAccent" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#f6d365;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#fda085;stop-opacity:1" />
        </linearGradient>
    </defs>

    <g transform="translate(4, 4)">
        <circle cx="20" cy="20" r="18" fill="url(#iconGradient)" opacity="0.1"/>
        <circle cx="20" cy="20" r="18" stroke="url(#iconGradient)" stroke-width="2.5" fill="none"/>

        <path d="M 10 25 L 15 20 L 20 18 L 25 12 L 30 10"
              stroke="url(#iconGradient)"
              stroke-width="2.5"
              stroke-linecap="round"
              stroke-linejoin="round"
              fill="none"/>

        <circle cx="15" cy="20" r="2.5" fill="url(#iconAccent)"/>
        <circle cx="20" cy="18" r="2.5" fill="url(#iconAccent)"/>
        <circle cx="25" cy="12" r="2.5" fill="url(#iconAccent)"/>
        <circle cx="30" cy="10" r="3" fill="url(#iconAccent)"/>
    </g>
</svg>
"""

# === PATTERN BACKGROUNDS ===
PATTERN_DOTS = """
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <pattern id="dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="1" fill="#667eea" opacity="0.05"/>
        </pattern>
    </defs>
    <rect width="100" height="100" fill="url(#dots)"/>
</svg>
"""

PATTERN_GRID = """
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <pattern id="grid" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#667eea" stroke-width="0.5" opacity="0.08"/>
        </pattern>
    </defs>
    <rect width="100" height="100" fill="url(#grid)"/>
</svg>
"""

# === ICONOS PREMIUM ===
ICON_INCOME = """
<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="incomeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#11998e"/>
            <stop offset="100%" style="stop-color:#38ef7d"/>
        </linearGradient>
    </defs>
    <circle cx="16" cy="16" r="14" fill="url(#incomeGrad)" opacity="0.2"/>
    <path d="M16 8 L16 24 M16 8 L12 12 M16 8 L20 12" stroke="url(#incomeGrad)" stroke-width="2.5" stroke-linecap="round"/>
</svg>
"""

ICON_EXPENSE = """
<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="expenseGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#fa709a"/>
            <stop offset="100%" style="stop-color:#fee140"/>
        </linearGradient>
    </defs>
    <circle cx="16" cy="16" r="14" fill="url(#expenseGrad)" opacity="0.2"/>
    <path d="M16 24 L16 8 M16 24 L12 20 M16 24 L20 20" stroke="url(#expenseGrad)" stroke-width="2.5" stroke-linecap="round"/>
</svg>
"""

ICON_BALANCE = """
<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="balanceGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#4facfe"/>
            <stop offset="100%" style="stop-color:#00f2fe"/>
        </linearGradient>
    </defs>
    <circle cx="16" cy="16" r="14" fill="url(#balanceGrad)" opacity="0.2"/>
    <path d="M10 16 L22 16 M16 10 L16 22" stroke="url(#balanceGrad)" stroke-width="2.5" stroke-linecap="round"/>
</svg>
"""

# === LOADING SPINNER ===
LOADING_SPINNER = """
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="spinnerGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#667eea"/>
            <stop offset="100%" style="stop-color:#764ba2"/>
        </linearGradient>
    </defs>
    <g>
        <circle cx="24" cy="24" r="18" stroke="url(#spinnerGrad)" stroke-width="4" fill="none" opacity="0.2"/>
        <path d="M 24 6 A 18 18 0 0 1 42 24" stroke="url(#spinnerGrad)" stroke-width="4" fill="none" stroke-linecap="round">
            <animateTransform
                attributeName="transform"
                type="rotate"
                from="0 24 24"
                to="360 24 24"
                dur="1s"
                repeatCount="indefinite"/>
        </path>
    </g>
</svg>
"""

# === ILUSTRACIONES DECORATIVAS ===
DECORATION_SUCCESS = """
<svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="successGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#11998e"/>
            <stop offset="100%" style="stop-color:#38ef7d"/>
        </linearGradient>
    </defs>
    <circle cx="60" cy="60" r="50" fill="url(#successGrad)" opacity="0.1"/>
    <circle cx="60" cy="60" r="40" stroke="url(#successGrad)" stroke-width="3" fill="none"/>
    <path d="M 40 60 L 55 75 L 80 45" stroke="url(#successGrad)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>
"""

DECORATION_ERROR = """
<svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="errorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#fa709a"/>
            <stop offset="100%" style="stop-color:#fee140"/>
        </linearGradient>
    </defs>
    <circle cx="60" cy="60" r="50" fill="url(#errorGrad)" opacity="0.1"/>
    <circle cx="60" cy="60" r="40" stroke="url(#errorGrad)" stroke-width="3" fill="none"/>
    <path d="M 45 45 L 75 75 M 75 45 L 45 75" stroke="url(#errorGrad)" stroke-width="5" stroke-linecap="round"/>
</svg>
"""

# === FUNCIONES HELPER ===
def get_logo(size="full"):
    """
    Obtiene el logo de la app.

    Args:
        size: "full" (con texto) o "icon" (solo icono)

    Returns:
        str: SVG del logo
    """
    return LOGO_SVG if size == "full" else LOGO_ICON_ONLY

def get_pattern(pattern_type="dots"):
    """
    Obtiene un pattern de fondo.

    Args:
        pattern_type: "dots" o "grid"

    Returns:
        str: SVG del pattern
    """
    patterns = {
        "dots": PATTERN_DOTS,
        "grid": PATTERN_GRID
    }
    return patterns.get(pattern_type, PATTERN_DOTS)

def get_icon(icon_type):
    """
    Obtiene un icono premium.

    Args:
        icon_type: "income", "expense", "balance", "success", "error"

    Returns:
        str: SVG del icono
    """
    icons = {
        "income": ICON_INCOME,
        "expense": ICON_EXPENSE,
        "balance": ICON_BALANCE,
        "success": DECORATION_SUCCESS,
        "error": DECORATION_ERROR
    }
    return icons.get(icon_type, "")

def get_loading_spinner():
    """Obtiene el spinner de carga animado."""
    return LOADING_SPINNER
