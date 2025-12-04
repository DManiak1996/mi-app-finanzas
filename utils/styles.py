"""
🎨 MÓDULO CENTRALIZADO DE ESTILOS CSS
========================================

Sistema de diseño premium para la aplicación de finanzas.
Basado en design tokens y CSS moderno con glassmorphism.

Uso:
    from utils.styles import inject_global_styles

    # Al inicio de app.py (después de set_page_config)
    inject_global_styles()

Arquitectura:
    - Importa design tokens (colors, typography, spacing, etc.)
    - Organizado por secciones semánticas
    - CSS variables nativas para theming
    - Transiciones y animaciones suaves
    - Mobile-first responsive design
"""

import streamlit as st
from utils.design_tokens import (
    Colors,
    Typography,
    Spacing,
    BorderRadius,
    Transitions,
    Config
)


def inject_global_styles():
    """
    Inyecta todos los estilos globales de la aplicación.

    Esta función debe llamarse UNA SOLA VEZ al inicio de la aplicación,
    preferiblemente después de st.set_page_config().

    Características:
        - Glassmorphism y efectos premium
        - Sistema tipográfico consistente
        - Componentes estilizados (buttons, cards, metrics)
        - Animaciones y micro-interacciones
        - Totalmente responsive (mobile-first)
    """

    css = f"""
    <style>
    /* ========== 🎨 FINTECH PREMIUM CSS ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ==========================================
       SECCIÓN 1: RESET Y BASE STYLES
       ========================================== */

    /* Prevenir scroll horizontal */
    html, body {{
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }}

    /* Fondo global con gradiente premium */
    .stApp {{
        background: {Colors.PREMIUM_BG_GRADIENT} !important;
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }}

    /* Container principal */
    .main .block-container {{
        max-width: {Config.MAX_CONTAINER_WIDTH} !important;
        padding-top: {Spacing.XXL} !important;
        overflow-x: hidden !important;
    }}

    /* Scroll suave */
    html {{
        scroll-behavior: smooth !important;
    }}


    /* ==========================================
       SECCIÓN 2: TYPOGRAPHY SYSTEM
       ========================================== */

    /* Font family global con antialiasing */
    html, body, [class*="css"] {{
        font-family: {Typography.FONT_PRIMARY} !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }}

    /* Headings con gradient text */
    h1 {{
        font-size: {Typography.TEXT_4XL} !important;
        font-weight: {Typography.WEIGHT_EXTRABOLD} !important;
        line-height: {Typography.LEADING_TIGHT} !important;
        letter-spacing: {Typography.TRACKING_TIGHT} !important;
        color: {Colors.GRAY_900} !important;
        margin-bottom: {Spacing.LG} !important;
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }}

    h2 {{
        font-size: {Typography.TEXT_3XL} !important;
        font-weight: {Typography.WEIGHT_BOLD} !important;
        line-height: {Typography.LEADING_SNUG} !important;
        color: {Colors.GRAY_900} !important;
        margin-bottom: {Spacing.BASE} !important;
    }}

    h3 {{
        font-size: {Typography.TEXT_2XL} !important;
        font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
        line-height: {Typography.LEADING_NORMAL} !important;
        color: {Colors.GRAY_900} !important;
        margin-bottom: {Spacing.MD} !important;
    }}


    /* ==========================================
       SECCIÓN 3: COMPONENTS - CARDS
       ========================================== */

    /* Cards premium con glassmorphism */
    div[data-testid="column"] > div {{
        background: {Colors.PREMIUM_CARD_GRADIENT} !important;
        border-radius: {BorderRadius.LG} !important;
        padding: {Spacing.LG} !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        border: 1px solid rgba(10, 76, 62, 0.08) !important;
        backdrop-filter: blur(10px) !important;
        transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
    }}

    /* Card hover effect */
    div[data-testid="column"] > div:hover {{
        transform: translateY(-4px) !important;
        box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
        border-color: rgba(10, 76, 62, 0.15) !important;
    }}


    /* ==========================================
       SECCIÓN 4: COMPONENTS - METRICS
       ========================================== */

    /* Métricas premium */
    .stMetric {{
        background: {Colors.PREMIUM_CARD_GRADIENT} !important;
        padding: {Spacing.XL} !important;
        border-radius: {BorderRadius.LG} !important;
        border: 1px solid rgba(10, 76, 62, 0.1) !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        backdrop-filter: blur(10px) !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
    }}

    /* Metric hover effect */
    .stMetric:hover {{
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
        border-color: rgba(10, 76, 62, 0.2) !important;
    }}

    /* Metric top accent bar */
    .stMetric::before {{
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
    }}

    /* Metric label */
    .stMetric label {{
        font-size: {Typography.TEXT_SM} !important;
        font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
        text-transform: uppercase !important;
        letter-spacing: {Typography.TRACKING_WIDER} !important;
        color: {Colors.GRAY_700} !important;
        margin-bottom: {Spacing.SM} !important;
    }}

    /* Metric value con gradient */
    .stMetric [data-testid="stMetricValue"] {{
        font-size: {Typography.TEXT_5XL} !important;
        font-weight: {Typography.WEIGHT_EXTRABOLD} !important;
        line-height: {Typography.LEADING_NONE} !important;
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-feature-settings: 'tnum' 1 !important;
        margin-bottom: {Spacing.SM} !important;
    }}

    /* Metric delta */
    .stMetric [data-testid="stMetricDelta"] {{
        font-size: {Typography.TEXT_SM} !important;
        font-weight: {Typography.WEIGHT_MEDIUM} !important;
        padding: {Spacing.XS} {Spacing.MD} !important;
        border-radius: {BorderRadius.FULL} !important;
        background: rgba(10, 76, 62, 0.08) !important;
        display: inline-block !important;
    }}


    /* ==========================================
       SECCIÓN 5: COMPONENTS - BUTTONS
       ========================================== */

    /* Botones base */
    .stButton button,
    .stFormSubmitButton button {{
        min-height: 48px !important;
        padding: {Spacing.MD} {Spacing.XL} !important;
        font-size: {Typography.TEXT_BASE} !important;
        font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
        border-radius: {BorderRadius.MD} !important;
        border: none !important;
        box-shadow: {Colors.SHADOW_PREMIUM_SM} !important;
        transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
        position: relative !important;
        overflow: hidden !important;
    }}

    /* Botones primary con gradient */
    .stButton button[kind="primary"],
    .stFormSubmitButton button[kind="primary"],
    button[data-testid="stFormSubmitButton"][kind="primary"] {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        color: white !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
    }}

    /* Hover state primary buttons */
    .stButton button[kind="primary"]:hover,
    .stFormSubmitButton button[kind="primary"]:hover,
    button[data-testid="stFormSubmitButton"][kind="primary"]:hover {{
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: {Colors.SHADOW_PREMIUM_LG}, {Colors.SHADOW_GLOW_PRIMARY} !important;
    }}

    /* Active state primary buttons */
    .stButton button[kind="primary"]:active,
    .stFormSubmitButton button[kind="primary"]:active,
    button[data-testid="stFormSubmitButton"][kind="primary"]:active {{
        transform: translateY(0) scale(0.98) !important;
    }}

    /* Efecto ripple en botones */
    .stButton button::after {{
        content: '' !important;
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        width: 0 !important;
        height: 0 !important;
        border-radius: 50% !important;
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translate(-50%, -50%) !important;
        transition: width 0.6s, height 0.6s !important;
    }}

    .stButton button:active::after {{
        width: 300px !important;
        height: 300px !important;
    }}

    /* Secondary buttons */
    .stButton button[kind="secondary"] {{
        background: white !important;
        border: 2px solid rgba(10, 76, 62, 0.2) !important;
        color: {Colors.PREMIUM_PRIMARY_START} !important;
    }}

    .stButton button[kind="secondary"]:hover {{
        background: rgba(10, 76, 62, 0.05) !important;
        border-color: rgba(10, 76, 62, 0.4) !important;
        transform: translateY(-2px) !important;
    }}


    /* ==========================================
       SECCIÓN 6: COMPONENTS - FORMS & INPUTS
       ========================================== */

    /* Inputs premium */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox select,
    .stDateInput input {{
        min-height: 48px !important;
        font-size: {Typography.TEXT_BASE} !important;
        border-radius: {BorderRadius.MD} !important;
        border: 2px solid rgba(10, 76, 62, 0.15) !important;
        background: white !important;
        box-shadow: {Colors.SHADOW_PREMIUM_XS} !important;
        transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
        padding: {Spacing.MD} {Spacing.LG} !important;
    }}

    /* Input focus state */
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stSelectbox select:focus {{
        border-color: {Colors.PREMIUM_PRIMARY_START} !important;
        box-shadow: 0 0 0 3px rgba(10, 76, 62, 0.1), {Colors.SHADOW_PREMIUM_SM} !important;
        outline: none !important;
    }}


    /* ==========================================
       SECCIÓN 7: COMPONENTS - TABS
       ========================================== */

    /* Tab list container */
    .stTabs [data-baseweb="tab-list"] {{
        background: white !important;
        border-radius: {BorderRadius.LG} !important;
        padding: {Spacing.SM} !important;
        box-shadow: {Colors.SHADOW_PREMIUM_SM} !important;
        gap: {Spacing.SM} !important;
    }}

    /* Individual tabs */
    .stTabs [data-baseweb="tab"] {{
        padding: {Spacing.MD} {Spacing.XL} !important;
        font-size: {Typography.TEXT_BASE} !important;
        font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
        border-radius: {BorderRadius.BASE} !important;
        transition: all {Transitions.FAST} {Transitions.EASING_DEFAULT} !important;
        color: {Colors.GRAY_700} !important;
    }}

    /* Tab hover state */
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(10, 76, 62, 0.08) !important;
        color: {Colors.PREMIUM_PRIMARY_START} !important;
    }}

    /* Active tab */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        color: white !important;
        box-shadow: {Colors.SHADOW_PREMIUM_SM} !important;
    }}


    /* ==========================================
       SECCIÓN 8: COMPONENTS - TABLES
       ========================================== */

    /* DataFrame container */
    .stDataFrame {{
        border-radius: {BorderRadius.LG} !important;
        overflow: hidden !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        border: 1px solid rgba(10, 76, 62, 0.08) !important;
    }}

    /* Table header */
    .stDataFrame thead tr th {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        color: white !important;
        font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
        text-transform: uppercase !important;
        font-size: {Typography.TEXT_SM} !important;
        letter-spacing: {Typography.TRACKING_WIDER} !important;
        padding: {Spacing.LG} !important;
    }}

    /* Table rows */
    .stDataFrame tbody tr {{
        transition: all {Transitions.FAST} {Transitions.EASING_DEFAULT} !important;
    }}

    /* Table row hover */
    .stDataFrame tbody tr:hover {{
        background: rgba(10, 76, 62, 0.05) !important;
        transform: scale(1.01) !important;
    }}

    /* Table cells */
    .stDataFrame tbody tr td {{
        padding: {Spacing.LG} !important;
        font-size: {Typography.TEXT_BASE} !important;
    }}


    /* ==========================================
       SECCIÓN 9: COMPONENTS - CHARTS
       ========================================== */

    /* Plotly charts */
    .js-plotly-plot {{
        border-radius: {BorderRadius.LG} !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        background: {Colors.PREMIUM_CARD_GRADIENT} !important;
        padding: {Spacing.LG} !important;
        border: 1px solid rgba(10, 76, 62, 0.08) !important;
        backdrop-filter: blur(10px) !important;
        transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
    }}

    .js-plotly-plot:hover {{
        box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
        transform: translateY(-2px) !important;
    }}


    /* ==========================================
       SECCIÓN 10: COMPONENTS - ALERTS
       ========================================== */

    /* Base alert styles */
    .stAlert {{
        border-radius: {BorderRadius.LG} !important;
        border: none !important;
        box-shadow: {Colors.SHADOW_PREMIUM_SM} !important;
        padding: {Spacing.LG} {Spacing.XL} !important;
        backdrop-filter: blur(10px) !important;
    }}

    /* Success alert */
    .stSuccess {{
        background: linear-gradient(135deg, rgba(17, 153, 142, 0.1) 0%, rgba(56, 239, 125, 0.05) 100%) !important;
        border-left: 4px solid {Colors.PREMIUM_TEAL_START} !important;
    }}

    /* Error alert */
    .stError {{
        background: linear-gradient(135deg, rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.05) 100%) !important;
        border-left: 4px solid {Colors.PREMIUM_CORAL_START} !important;
    }}

    /* Info alert */
    .stInfo {{
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.05) 100%) !important;
        border-left: 4px solid {Colors.PREMIUM_SKY_START} !important;
    }}

    /* Warning alert */
    .stWarning {{
        background: linear-gradient(135deg, rgba(246, 211, 101, 0.1) 0%, rgba(253, 160, 133, 0.05) 100%) !important;
        border-left: 4px solid {Colors.PREMIUM_GOLD_START} !important;
    }}


    /* ==========================================
       SECCIÓN 11: COMPONENTS - MODALS
       ========================================== */

    /* Modal/Dialog glassmorphism */
    div[data-testid="stModal"] > div {{
        background: {Colors.GLASS_BG} !important;
        backdrop-filter: blur(20px) !important;
        border-radius: {BorderRadius.XL} !important;
        border: 1px solid {Colors.GLASS_BORDER} !important;
        box-shadow: {Colors.SHADOW_PREMIUM_2XL} !important;
    }}


    /* ==========================================
       SECCIÓN 12: LAYOUT - SIDEBAR
       ========================================== */

    /* Sidebar premium */
    section[data-testid="stSidebar"] {{
        background: {Colors.PREMIUM_CARD_GRADIENT} !important;
        border-right: 1px solid rgba(10, 76, 62, 0.1) !important;
        box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
    }}

    /* Radio button container */
    section[data-testid="stSidebar"] .stRadio > div {{
        gap: {Spacing.SM} !important;
    }}

    /* Radio button labels */
    section[data-testid="stSidebar"] .stRadio label {{
        padding: {Spacing.MD} {Spacing.LG} !important;
        border-radius: {BorderRadius.BASE} !important;
        transition: all {Transitions.FAST} {Transitions.EASING_DEFAULT} !important;
        font-weight: {Typography.WEIGHT_MEDIUM} !important;
        position: relative !important;
    }}

    /* Radio button hover */
    section[data-testid="stSidebar"] .stRadio label:hover {{
        background: rgba(10, 76, 62, 0.08) !important;
        transform: translateX(4px) !important;
    }}

    /* Active radio button */
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        color: white !important;
        box-shadow: {Colors.SHADOW_PREMIUM_SM} !important;
    }}

    /* Ocultar círculo de radio button nativo */
    section[data-testid="stSidebar"] .stRadio input[type="radio"] {{
        display: none !important;
    }}

    section[data-testid="stSidebar"] div[role="radio"] {{
        width: 0 !important;
        height: 0 !important;
        min-width: 0 !important;
        min-height: 0 !important;
        opacity: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Indicador visual de selección */
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"]::before {{
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 4px !important;
        height: 70% !important;
        background: {Colors.PREMIUM_PRIMARY_END} !important;
        border-radius: 0 4px 4px 0 !important;
        z-index: 999 !important;
    }}


    /* ==========================================
       SECCIÓN 13: ANIMATIONS
       ========================================== */

    /* Fade in up animation */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    /* Pulse animation */
    @keyframes pulse {{
        0%, 100% {{
            opacity: 1;
        }}
        50% {{
            opacity: 0.5;
        }}
    }}

    /* Shimmer animation */
    @keyframes shimmer {{
        0% {{
            background-position: -1000px 0;
        }}
        100% {{
            background-position: 1000px 0;
        }}
    }}

    /* Aplicar animación a componentes */
    .stMetric,
    div[data-testid="column"] > div,
    .js-plotly-plot {{
        animation: fadeInUp 0.6s {Transitions.EASING_DEFAULT} !important;
    }}

    /* Loading spinner animation */
    .stSpinner > div {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        animation: pulse 1.5s ease-in-out infinite !important;
    }}


    /* ==========================================
       SECCIÓN 14: SPECIAL EFFECTS
       ========================================== */

    /* Custom text selection */
    ::selection {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        color: white !important;
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 10px !important;
        height: 10px !important;
    }}

    ::-webkit-scrollbar-track {{
        background: rgba(10, 76, 62, 0.05) !important;
        border-radius: {BorderRadius.FULL} !important;
    }}

    ::-webkit-scrollbar-thumb {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        border-radius: {BorderRadius.FULL} !important;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        box-shadow: {Colors.SHADOW_GLOW_PRIMARY} !important;
    }}


    /* ==========================================
       SECCIÓN 15: UTILITY CLASSES
       ========================================== */

    /* Glassmorphism utility */
    .premium-glass {{
        background: {Colors.GLASS_BG} !important;
        backdrop-filter: {Colors.GLASS_BACKDROP} !important;
        border: 1px solid {Colors.GLASS_BORDER} !important;
        box-shadow: {Colors.GLASS_SHADOW} !important;
    }}

    /* Gradient utility */
    .premium-gradient {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        color: white !important;
    }}

    /* Shadow utility */
    .premium-shadow {{
        box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
    }}

    /* Card utility */
    .premium-card {{
        background: {Colors.PREMIUM_CARD_GRADIENT} !important;
        border-radius: {BorderRadius.LG} !important;
        padding: {Spacing.XL} !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        border: 1px solid rgba(10, 76, 62, 0.1) !important;
    }}


    /* ==========================================
       SECCIÓN 16: RESPONSIVE DESIGN
       ========================================== */

    /* Tablet breakpoint */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding-left: {Spacing.BASE} !important;
            padding-right: {Spacing.BASE} !important;
        }}

        h1 {{ font-size: {Typography.TEXT_3XL} !important; }}
        h2 {{ font-size: {Typography.TEXT_2XL} !important; }}
        h3 {{ font-size: {Typography.TEXT_XL} !important; }}

        .stMetric {{
            padding: {Spacing.LG} !important;
        }}

        .stMetric [data-testid="stMetricValue"] {{
            font-size: {Typography.TEXT_3XL} !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            padding: {Spacing.SM} {Spacing.MD} !important;
            font-size: {Typography.TEXT_SM} !important;
        }}

        /* Deshabilitar hover effects en tablet */
        div[data-testid="column"] > div:hover {{
            transform: none !important;
        }}
    }}

    /* Mobile breakpoint */
    @media (max-width: 480px) {{
        h1 {{ font-size: {Typography.TEXT_2XL} !important; }}

        .stButton button {{
            width: 100% !important;
        }}

        .stMetric {{
            min-width: 100% !important;
        }}

        .stMetric [data-testid="stMetricValue"] {{
            font-size: {Typography.TEXT_2XL} !important;
        }}
    }}

    </style>
    """

    st.markdown(css, unsafe_allow_html=True)


def inject_custom_css(css_string: str):
    """
    Inyecta CSS personalizado adicional.

    Args:
        css_string: String con CSS personalizado

    Uso:
        inject_custom_css('''
            .my-custom-class {
                color: red;
            }
        ''')
    """
    st.markdown(f"<style>{css_string}</style>", unsafe_allow_html=True)


# Estilos específicos para componentes reutilizables
class ComponentStyles:
    """
    Clases CSS predefinidas para componentes comunes.
    Usar con st.markdown() para aplicar estilos inline.
    """

    @staticmethod
    def metric_card(title: str, value: str, delta: str = None, icon: str = None) -> str:
        """
        HTML para una métrica con estilo premium.

        Args:
            title: Título de la métrica
            value: Valor principal
            delta: Valor delta opcional
            icon: Emoji opcional

        Returns:
            String HTML listo para st.markdown()
        """
        delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ''
        icon_html = f'<span class="metric-icon">{icon}</span>' if icon else ''

        return f"""
        <div class="premium-card" style="text-align: center;">
            {icon_html}
            <div style="font-size: 0.875rem; font-weight: 600; text-transform: uppercase;
                        letter-spacing: 0.05em; color: {Colors.GRAY_700}; margin-bottom: {Spacing.SM};">
                {title}
            </div>
            <div style="font-size: 2.5rem; font-weight: 800;
                        background: {Colors.PREMIUM_GRADIENT_PRIMARY};
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {value}
            </div>
            {delta_html}
        </div>
        """

    @staticmethod
    def info_box(content: str, style: str = "info") -> str:
        """
        HTML para una caja informativa con estilo premium.

        Args:
            content: Contenido de la caja
            style: Tipo de caja (info, success, warning, error)

        Returns:
            String HTML listo para st.markdown()
        """
        colors = {
            "info": Colors.PREMIUM_SKY_START,
            "success": Colors.PREMIUM_TEAL_START,
            "warning": Colors.PREMIUM_GOLD_START,
            "error": Colors.PREMIUM_CORAL_START
        }

        border_color = colors.get(style, colors["info"])

        return f"""
        <div style="padding: {Spacing.LG}; border-radius: {BorderRadius.LG};
                    border-left: 4px solid {border_color};
                    background: rgba(255, 255, 255, 0.6);
                    backdrop-filter: blur(10px);
                    box-shadow: {Colors.SHADOW_PREMIUM_SM};">
            {content}
        </div>
        """
