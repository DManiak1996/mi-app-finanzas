# app.py

import streamlit as st
from database import db_manager
from utils import metrics, visualizer, excel_reader, categorizer, sync, coche_electrico, config_manager
from utils.design_tokens import Colors, Typography, Spacing, BorderRadius, Transitions, Config, get_budget_color, spacer_html
from utils import brand_assets
import datetime
import pandas as pd
import json
import sqlite3
import plotly.graph_objects as go
import auth_simple as auth  # Sistema de autenticación (sin cookies temporalmente)

# --- Configuración de la página ---
st.set_page_config(
    page_title="Mi App de Finanzas",
    page_icon="💰",
    layout="wide"
)

# --- Autenticación ---
if not auth.check_authentication():
    st.stop()  # Detiene la ejecución si no está autenticado

# --- Inicialización ---
def inicializar_app():
    """Inicializa la base de datos creando las tablas si es necesario."""
    # NO usar cache para asegurar que siempre se crean las tablas nuevas
    db_manager.crear_tablas()

    # Inicializar session_state para persistencia de mes/año entre pestañas
    año_actual = datetime.date.today().year
    mes_actual = datetime.date.today().month

    # Detectar cambio de año automáticamente
    # Si ya había un año seleccionado pero ahora es un nuevo año, actualizarlo
    if 'año_seleccionado' not in st.session_state:
        st.session_state.año_seleccionado = año_actual
        st.session_state.ultimo_año_real = año_actual  # Guardar año real para detectar cambios
    elif 'ultimo_año_real' not in st.session_state:
        # Primera vez que añadimos esta lógica, guardar el año real actual
        st.session_state.ultimo_año_real = año_actual
    elif st.session_state.ultimo_año_real != año_actual:
        # ¡Ha cambiado el año real! Actualizar automáticamente al nuevo año
        st.session_state.año_seleccionado = año_actual
        st.session_state.ultimo_año_real = año_actual

    if 'mes_seleccionado' not in st.session_state:
        st.session_state.mes_seleccionado = mes_actual

    # Migración automática: añadir campos 'pagado' y 'fecha_pago' si no existen
    try:
        conn = db_manager.get_db_connection()
        cursor = conn.cursor()

        # Verificar si los campos existen
        cursor.execute("PRAGMA table_info(recargas_coche)")
        columnas = [col[1] for col in cursor.fetchall()]

        # Añadir campo 'pagado' si no existe
        if 'pagado' not in columnas:
            cursor.execute("ALTER TABLE recargas_coche ADD COLUMN pagado BOOLEAN DEFAULT 0")
            print("✅ Campo 'pagado' añadido a recargas_coche")

        # Añadir campo 'fecha_pago' si no existe
        if 'fecha_pago' not in columnas:
            cursor.execute("ALTER TABLE recargas_coche ADD COLUMN fecha_pago TIMESTAMP")
            print("✅ Campo 'fecha_pago' añadido a recargas_coche")

        # Asegurar que recargas existentes estén marcadas como no pagadas
        cursor.execute("UPDATE recargas_coche SET pagado = 0 WHERE pagado IS NULL")

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Migración: {e}")

inicializar_app()

# --- Funciones de Dialog (Popups) ---

@st.dialog("💵 Desglose de Ingresos del Mes", width="large")
def mostrar_desglose_ingresos(ingreso_base_data, ingresos_extra, total_ingresos_mes):
    """Dialog popup para mostrar el desglose detallado de ingresos"""
    st.info("Aquí puedes ver el detalle de todos los ingresos del mes actual.")

    col1, col2, col3 = st.columns(3)

    # Mostrar nómina con fecha si existe
    if ingreso_base_data['fecha']:
        from datetime import datetime
        fecha_obj = datetime.strptime(ingreso_base_data['fecha'], '%Y-%m-%d')
        fecha_str = fecha_obj.strftime('%d/%m/%Y')
        col1.metric(
            "💼 Ingreso Base (Nómina)",
            f"{ingreso_base_data['importe']:.2f} €",
            delta=f"Recibida el {fecha_str}",
            help="Nómina regular identificada para este mes"
        )
    else:
        col1.metric(
            "💼 Ingreso Base (Nómina)",
            f"{ingreso_base_data['importe']:.2f} €",
            delta="Sin nómina registrada",
            delta_color="off",
            help="No se encontró nómina para este mes"
        )

    col2.metric(
        "✨ Ingresos Extraordinarios",
        f"{ingresos_extra['total']:.2f} €",
        delta=f"{ingresos_extra['cantidad']} transacciones",
        help="Pagas extras, devoluciones IRPF, ventas, bonificaciones, etc."
    )

    col3.metric(
        "💵 Total Ingresos",
        f"{total_ingresos_mes:.2f} €",
        help="Ingreso base + extraordinarios"
    )

    # Mostrar desglose detallado si hay ingresos extraordinarios
    if ingresos_extra['total'] > 0:
        st.markdown("---")
        st.markdown("**📋 Detalle de Ingresos Extraordinarios:**")

        desglose = ingresos_extra['desglose']

        if desglose['pagas_extras'] > 0:
            st.caption(f"💼 Pagas extras / Nóminas adicionales: **{desglose['pagas_extras']:.2f} €**")

        if desglose['irpf_bonificaciones'] > 0:
            st.caption(f"🏦 Devoluciones IRPF / Bonificaciones: **{desglose['irpf_bonificaciones']:.2f} €**")

        if desglose['otros'] > 0:
            st.caption(f"🔄 Otros ingresos: **{desglose['otros']:.2f} €**")

        if desglose['sin_clasificar'] > 0:
            st.caption(f"❓ Sin clasificar: **{desglose['sin_clasificar']:.2f} €**")

        # Mostrar lista de transacciones
        st.markdown("---")
        st.markdown("**📝 Lista de Transacciones:**")
        for t in ingresos_extra['transacciones']:
            categoria_icon = {
                'FIJOS': '💼',
                'EXTRAORDINARIOS': '🏦',
                'INGRESO': '💰',
                'SIN_CLASIFICAR': '❓'
            }.get(t.get('categoria'), '📌')

            concepto_corto = t['concepto'][:50] + "..." if len(t['concepto']) > 50 else t['concepto']
            st.caption(f"{categoria_icon} {t['fecha']} - {concepto_corto}: **{t['importe']:.2f} €**")
    else:
        st.info("ℹ️ No hay ingresos extraordinarios en este mes (solo nómina regular)")


@st.dialog("💰 Gestionar Reembolsos", width="large")
def mostrar_modal_reembolsos(mes, año, ingreso_base):
    """Dialog popup para gestionar y clasificar reembolsos"""
    st.info("Selecciona los ingresos (bizums, devoluciones) que son reembolsos de gastos y márcalos como REEMBOLSO.")

    # Obtener todos los ingresos del mes que NO sean ya reembolsos ni nómina
    ingresos_sin_clasificar = [
        t for t in db_manager.obtener_transacciones(mes=mes, año=año)
        if t['tipo'] == 'INGRESO'
        and t.get('categoria') not in ['REEMBOLSO', 'INGRESO']
        and t['importe'] < ingreso_base * 0.5  # Filtrar nómina (menos de 50% del ingreso base)
    ]

    if ingresos_sin_clasificar:
        st.write(f"**{len(ingresos_sin_clasificar)} ingresos pendientes de revisar:**")
        st.info("💡 **Tip**: Asigna la categoría de gasto que este reembolso compensa (ej: si te devolvieron dinero de un restaurante, selecciona DISFRUTE)")

        for ingreso in ingresos_sin_clasificar:
            col1, col2, col3, col4, col5 = st.columns([1.5, 0.8, 2, 1.5, 0.8])

            with col1:
                st.text(ingreso['fecha'])
            with col2:
                st.text(f"{ingreso['importe']:.2f} €")
            with col3:
                # Mostrar concepto truncado
                concepto = ingreso['concepto'][:30] + "..." if len(ingreso['concepto']) > 30 else ingreso['concepto']
                st.text(concepto)
            with col4:
                # Dropdown de categorías de GASTO (para asignar el reembolso)
                categoria_gasto = st.selectbox(
                    "Categoría",
                    options=["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "SIN_ASIGNAR"],
                    key=f"cat_reembolso_{ingreso['id']}",
                    label_visibility="collapsed"
                )
            with col5:
                if st.button("✅", key=f"marcar_reembolso_{ingreso['id']}", help="Marcar como REEMBOLSO"):
                    # Actualizar categoría a REEMBOLSO y guardar categoría de gasto asociada en notas
                    notas_reembolso = f"REEMBOLSO_DE:{categoria_gasto}" if categoria_gasto != "SIN_ASIGNAR" else "REEMBOLSO_DE:SIN_ASIGNAR"

                    db_manager.actualizar_transaccion(ingreso['id'], {
                        'categoria': 'REEMBOLSO',
                        'notas': notas_reembolso
                    })
                    st.toast(f"✅ Reembolso de {categoria_gasto}: {ingreso['importe']:.2f}€ procesado correctamente", icon="✅")
                    st.rerun()
    else:
        st.success("✅ No hay ingresos pendientes de clasificar como reembolsos")

# --- CSS FINTECH PREMIUM COMPLETO ---
st.markdown(f"""
<!-- Logo Premium en Header -->
<div style="padding: {Spacing.LG} 0; margin-bottom: {Spacing.XL}; background: {Colors.PREMIUM_BG_GRADIENT}; border-bottom: 1px solid rgba(102, 126, 234, 0.1);">
    <div style="max-width: {Config.MAX_CONTAINER_WIDTH}; margin: 0 auto; padding: 0 {Spacing.LG};">
        {brand_assets.LOGO_SVG}
    </div>
</div>

<style>
/* ========== 🎨 FINTECH PREMIUM CSS ========== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* === FONDO GLOBAL CON GRADIENTE === */
.stApp {{
    background: {Colors.PREMIUM_BG_GRADIENT} !important;
}}

.main .block-container {{
    max-width: {Config.MAX_CONTAINER_WIDTH} !important;
    padding-top: {Spacing.XXL} !important;
}}

/* === SISTEMA TIPOGRÁFICO === */
html, body, [class*="css"] {{
    font-family: {Typography.FONT_PRIMARY} !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
}}

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

/* === 💎 CARDS PREMIUM CON GLASSMORPHISM === */
div[data-testid="column"] > div {{
    background: {Colors.PREMIUM_CARD_GRADIENT} !important;
    border-radius: {BorderRadius.LG} !important;
    padding: {Spacing.LG} !important;
    box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
    border: 1px solid rgba(102, 126, 234, 0.08) !important;
    backdrop-filter: blur(10px) !important;
    transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
}}

div[data-testid="column"] > div:hover {{
    transform: translateY(-4px) !important;
    box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
    border-color: rgba(102, 126, 234, 0.15) !important;
}}

/* === 🎯 MÉTRICAS PREMIUM === */
.stMetric {{
    background: {Colors.PREMIUM_CARD_GRADIENT} !important;
    padding: {Spacing.XL} !important;
    border-radius: {BorderRadius.LG} !important;
    border: 1px solid rgba(102, 126, 234, 0.1) !important;
    box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
    backdrop-filter: blur(10px) !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
}}

.stMetric:hover {{
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
    border-color: rgba(102, 126, 234, 0.2) !important;
}}

.stMetric::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 4px !important;
    background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
}}

.stMetric label {{
    font-size: {Typography.TEXT_SM} !important;
    font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
    text-transform: uppercase !important;
    letter-spacing: {Typography.TRACKING_WIDER} !important;
    color: {Colors.GRAY_700} !important;
    margin-bottom: {Spacing.SM} !important;
}}

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

.stMetric [data-testid="stMetricDelta"] {{
    font-size: {Typography.TEXT_SM} !important;
    font-weight: {Typography.WEIGHT_MEDIUM} !important;
    padding: {Spacing.XS} {Spacing.MD} !important;
    border-radius: {BorderRadius.FULL} !important;
    background: rgba(102, 126, 234, 0.08) !important;
    display: inline-block !important;
}}

/* === 🔘 BOTONES PREMIUM CON GRADIENTES === */
.stButton button {{
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

.stButton button[kind="primary"] {{
    background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
    color: white !important;
    box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
}}

.stButton button[kind="primary"]:hover {{
    transform: translateY(-2px) scale(1.05) !important;
    box-shadow: {Colors.SHADOW_PREMIUM_LG}, {Colors.SHADOW_GLOW_PRIMARY} !important;
}}

.stButton button[kind="primary"]:active {{
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

.stButton button[kind="secondary"] {{
    background: white !important;
    border: 2px solid rgba(102, 126, 234, 0.2) !important;
    color: {Colors.PREMIUM_PRIMARY_START} !important;
}}

.stButton button[kind="secondary"]:hover {{
    background: rgba(102, 126, 234, 0.05) !important;
    border-color: rgba(102, 126, 234, 0.4) !important;
    transform: translateY(-2px) !important;
}}

/* === 📊 GRÁFICOS PREMIUM === */
.js-plotly-plot {{
    border-radius: {BorderRadius.LG} !important;
    box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
    background: {Colors.PREMIUM_CARD_GRADIENT} !important;
    padding: {Spacing.LG} !important;
    border: 1px solid rgba(102, 126, 234, 0.08) !important;
    backdrop-filter: blur(10px) !important;
    transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
}}

.js-plotly-plot:hover {{
    box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
    transform: translateY(-2px) !important;
}}

/* === 📝 INPUTS PREMIUM === */
.stTextInput input, .stNumberInput input, .stSelectbox select, .stDateInput input {{
    min-height: 48px !important;
    font-size: {Typography.TEXT_BASE} !important;
    border-radius: {BorderRadius.MD} !important;
    border: 2px solid rgba(102, 126, 234, 0.15) !important;
    background: white !important;
    box-shadow: {Colors.SHADOW_PREMIUM_XS} !important;
    transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
    padding: {Spacing.MD} {Spacing.LG} !important;
}}

.stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {{
    border-color: {Colors.PREMIUM_PRIMARY_START} !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), {Colors.SHADOW_PREMIUM_SM} !important;
    outline: none !important;
}}

/* === 🔖 TABS PREMIUM === */
.stTabs [data-baseweb="tab-list"] {{
    background: white !important;
    border-radius: {BorderRadius.LG} !important;
    padding: {Spacing.SM} !important;
    box-shadow: {Colors.SHADOW_PREMIUM_SM} !important;
    gap: {Spacing.SM} !important;
}}

.stTabs [data-baseweb="tab"] {{
    padding: {Spacing.MD} {Spacing.XL} !important;
    font-size: {Typography.TEXT_BASE} !important;
    font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
    border-radius: {BorderRadius.BASE} !important;
    transition: all {Transitions.FAST} {Transitions.EASING_DEFAULT} !important;
    color: {Colors.GRAY_700} !important;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: rgba(102, 126, 234, 0.08) !important;
    color: {Colors.PREMIUM_PRIMARY_START} !important;
}}

.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
    color: white !important;
    box-shadow: {Colors.SHADOW_PREMIUM_SM} !important;
}}

/* === 📋 TABLAS PREMIUM === */
.stDataFrame {{
    border-radius: {BorderRadius.LG} !important;
    overflow: hidden !important;
    box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
    border: 1px solid rgba(102, 126, 234, 0.08) !important;
}}

.stDataFrame thead tr th {{
    background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
    color: white !important;
    font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
    text-transform: uppercase !important;
    font-size: {Typography.TEXT_SM} !important;
    letter-spacing: {Typography.TRACKING_WIDER} !important;
    padding: {Spacing.LG} !important;
}}

.stDataFrame tbody tr {{
    transition: all {Transitions.FAST} {Transitions.EASING_DEFAULT} !important;
}}

.stDataFrame tbody tr:hover {{
    background: rgba(102, 126, 234, 0.05) !important;
    transform: scale(1.01) !important;
}}

.stDataFrame tbody tr td {{
    padding: {Spacing.LG} !important;
    font-size: {Typography.TEXT_BASE} !important;
}}

/* === 📢 ALERTAS Y MENSAJES PREMIUM === */
.stAlert {{
    border-radius: {BorderRadius.LG} !important;
    border: none !important;
    box-shadow: {Colors.SHADOW_PREMIUM_SM} !important;
    padding: {Spacing.LG} {Spacing.XL} !important;
    backdrop-filter: blur(10px) !important;
}}

.stSuccess {{
    background: linear-gradient(135deg, rgba(17, 153, 142, 0.1) 0%, rgba(56, 239, 125, 0.05) 100%) !important;
    border-left: 4px solid {Colors.PREMIUM_TEAL_START} !important;
}}

.stError {{
    background: linear-gradient(135deg, rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.05) 100%) !important;
    border-left: 4px solid {Colors.PREMIUM_CORAL_START} !important;
}}

.stInfo {{
    background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.05) 100%) !important;
    border-left: 4px solid {Colors.PREMIUM_SKY_START} !important;
}}

.stWarning {{
    background: linear-gradient(135deg, rgba(246, 211, 101, 0.1) 0%, rgba(253, 160, 133, 0.05) 100%) !important;
    border-left: 4px solid {Colors.PREMIUM_GOLD_START} !important;
}}

/* === 🎭 MODALS/DIALOGS GLASSMORPHISM === */
div[data-testid="stModal"] > div {{
    background: {Colors.GLASS_BG} !important;
    backdrop-filter: blur(20px) !important;
    border-radius: {BorderRadius.XL} !important;
    border: 1px solid {Colors.GLASS_BORDER} !important;
    box-shadow: {Colors.SHADOW_PREMIUM_2XL} !important;
}}

/* === 🎪 SIDEBAR PREMIUM === */
section[data-testid="stSidebar"] {{
    background: {Colors.PREMIUM_CARD_GRADIENT} !important;
    border-right: 1px solid rgba(102, 126, 234, 0.1) !important;
    box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
}}

section[data-testid="stSidebar"] .stRadio > div {{
    gap: {Spacing.SM} !important;
}}

section[data-testid="stSidebar"] .stRadio label {{
    padding: {Spacing.MD} {Spacing.LG} !important;
    border-radius: {BorderRadius.BASE} !important;
    transition: all {Transitions.FAST} {Transitions.EASING_DEFAULT} !important;
    font-weight: {Typography.WEIGHT_MEDIUM} !important;
}}

section[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(102, 126, 234, 0.08) !important;
    transform: translateX(4px) !important;
}}

section[data-testid="stSidebar"] .stRadio label[data-checked="true"] {{
    background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
    color: white !important;
    box-shadow: {Colors.SHADOW_PREMIUM_SM} !important;
}}

/* === ⚡ ANIMACIONES Y MICRO-INTERACCIONES === */
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

@keyframes pulse {{
    0%, 100% {{
        opacity: 1;
    }}
    50% {{
        opacity: 0.5;
    }}
}}

@keyframes shimmer {{
    0% {{
        background-position: -1000px 0;
    }}
    100% {{
        background-position: 1000px 0;
    }}
}}

.stMetric, div[data-testid="column"] > div, .js-plotly-plot {{
    animation: fadeInUp 0.6s {Transitions.EASING_DEFAULT} !important;
}}

/* Loading state shimmer effect */
.stSpinner > div {{
    background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
    animation: pulse 1.5s ease-in-out infinite !important;
}}

/* === 📱 RESPONSIVE MÓVIL === */
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

    div[data-testid="column"] > div:hover {{
        transform: none !important;
    }}
}}

@media (max-width: 480px) {{
    h1 {{ font-size: {Typography.TEXT_2XL} !important; }}
    .stButton button {{ width: 100% !important; }}
    .stMetric {{ min-width: 100% !important; }}

    .stMetric [data-testid="stMetricValue"] {{
        font-size: {Typography.TEXT_2XL} !important;
    }}
}}

/* === 🌟 EFECTOS ESPECIALES === */
/* Scroll suave */
html {{
    scroll-behavior: smooth !important;
}}

/* Selection personalizada */
::selection {{
    background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
    color: white !important;
}}

/* Scrollbar personalizada */
::-webkit-scrollbar {{
    width: 10px !important;
    height: 10px !important;
}}

::-webkit-scrollbar-track {{
    background: rgba(102, 126, 234, 0.05) !important;
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

/* === 🎨 CLASES UTILITY === */
.premium-glass {{
    background: {Colors.GLASS_BG} !important;
    backdrop-filter: {Colors.GLASS_BACKDROP} !important;
    border: 1px solid {Colors.GLASS_BORDER} !important;
    box-shadow: {Colors.GLASS_SHADOW} !important;
}}

.premium-gradient {{
    background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
    color: white !important;
}}

.premium-shadow {{
    box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
}}

.premium-card {{
    background: {Colors.PREMIUM_CARD_GRADIENT} !important;
    border-radius: {BorderRadius.LG} !important;
    padding: {Spacing.XL} !important;
    box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
    border: 1px solid rgba(102, 126, 234, 0.1) !important;
}}
</style>
""", unsafe_allow_html=True)

# --- Barra lateral de navegación ---
st.sidebar.title("Navegación")

# Navegación simple con radio button
PAGINAS = ["Dashboard", "Añadir Gasto", "Transacciones", "Importar", "Categorías", "🔌 Coche Eléctrico", "Sincronización", "Configuración"]

pagina_seleccionada = st.sidebar.radio(
    "Elige una página:",
    PAGINAS,
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("Aplicación de finanzas personales desarrollada con la ayuda de Gemini.")

# Mostrar info de usuario autenticado
auth.show_user_info()

# --- Constantes y utilidades ---
NOMBRES_MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
MESES_INVERTIDO = {v: k for k, v in NOMBRES_MESES.items()}

# --- Contenido principal de la página ---

def mostrar_dashboard():
    st.title("📊 Dashboard Financiero")

    # --- Selectores de período en columnas ---
    col_selector1, col_selector2, col_selector3, col_selector4 = st.columns([1, 1, 2, 1])

    año_actual = datetime.date.today().year

    with col_selector1:
        # Obtener años disponibles desde la BD (años con datos + actual + siguiente)
        años_disponibles = db_manager.obtener_años_disponibles()
        index_año = años_disponibles.index(st.session_state.año_seleccionado) if st.session_state.año_seleccionado in años_disponibles else len(años_disponibles) - 1

        año = st.selectbox("📅 Año", años_disponibles, index=index_año, key="dashboard_año")
        # Actualizar session_state
        st.session_state.año_seleccionado = año

    with col_selector2:
        # Calcular índice del mes en session_state
        meses_disponibles = list(NOMBRES_MESES.values())
        index_mes = st.session_state.mes_seleccionado - 1

        nombre_mes_seleccionado = st.selectbox("📆 Mes", meses_disponibles, index=index_mes, key="dashboard_mes")
        mes = MESES_INVERTIDO[nombre_mes_seleccionado]
        # Actualizar session_state
        st.session_state.mes_seleccionado = mes

    with col_selector3:
        # Métrica Global: Líquido Disponible
        liquido_disponible = metrics.calcular_liquido_disponible()
        st.metric(
            label="💧 Líquido Disponible Total",
            value=f"{liquido_disponible:.2f} €",
            help="Balance acumulado de todas tus transacciones"
        )

    with col_selector4:
        # Selector de vista (Mes / Año) - Reemplaza sub-tabs
        vista_periodo = st.radio(
            "📊 Vista",
            options=["Mes", "Año"],
            horizontal=True,
            help="Alterna entre vista mensual y anual"
        )

    st.markdown("---")

    # Tabs principales reorganizados
    tab_resumen, tab_analisis, tab_historico = st.tabs([
        "📊 Resumen General",
        "📈 Análisis Avanzado",
        "📉 Histórico"
    ])

    # ========== TAB 1: RESUMEN GENERAL ==========
    with tab_resumen:
        # Vista mensual o anual según selector
        if vista_periodo == "Mes":
            with st.spinner("Calculando métricas mensuales..."):
                datos_mes = metrics.calcular_totales_mes(mes, año)

                # Calcular ingresos totales del mes
                ingreso_base_data = metrics.obtener_ingreso_base_mes(mes, año)
                ingresos_extra = metrics.obtener_ingresos_extraordinarios_mes(mes, año)
                total_ingresos_mes = ingreso_base_data['importe'] + ingresos_extra['total']

                # Métricas principales en cards - Layout responsive (2x2)
                col1, col2 = st.columns(2)

                # MÉTRICA PRINCIPAL: Total Ingresos del Mes con botón de desglose
                with col1:
                    st.metric(
                        "💵 Total Ingresos Mes",
                        f"{total_ingresos_mes:.2f} €",
                        help="Suma de todos los ingresos del mes (nómina + extraordinarios)"
                    )
                    # Botón para ver desglose de ingresos (popup) - pegado debajo de la métrica
                    if st.button("ℹ️ Ver desglose", key="btn_desglose_ingresos", help="Ver desglose de ingresos", type="primary"):
                        mostrar_desglose_ingresos(ingreso_base_data, ingresos_extra, total_ingresos_mes)

                with col2:
                    # Mostrar gastos netos (después de reembolsos)
                    gastos_brutos = abs(datos_mes['total_gastos'])
                    reembolsos = datos_mes['total_reembolsos']
                    gastos_netos = abs(datos_mes['gastos_netos'])

                    # Construir texto del help con información de reembolsos
                    help_text = f"Gastos brutos: {gastos_brutos:.2f}€"
                    if reembolsos > 0:
                        help_text += f" - Reembolsos: {reembolsos:.2f}€ = Netos: {gastos_netos:.2f}€"
                    else:
                        help_text += f" = Netos: {gastos_netos:.2f}€ (sin reembolsos este mes)"

                    st.metric(
                        "💸 Gastos del Mes",
                        f"{abs(gastos_netos):.2f} €",  # Valor absoluto para claridad
                        help=help_text
                    )
                    # Botón para gestionar reembolsos (popup) - pegado debajo de la métrica
                    if st.button("💰 Reembolsos", key="btn_reembolsos", help="Gestionar reembolsos", type="primary"):
                        mostrar_modal_reembolsos(mes, año, ingreso_base_data['importe'])

                col3, col4 = st.columns(2)

                # Calcular balance basado en TOTAL INGRESOS usando gastos NETOS
                balance_mes = total_ingresos_mes + datos_mes['gastos_netos']  # gastos_netos ya es negativo
                col3.metric(
                    "⚖️ Balance del Mes",
                    f"{balance_mes:.2f} €",
                    delta=f"{balance_mes:.2f} €",
                    delta_color="normal" if balance_mes > 0 else "inverse",
                    help="Diferencia entre total de ingresos y gastos netos del mes. Positivo = superávit, Negativo = déficit"
                )

                # Tasa de ahorro basada en TOTAL INGRESOS
                if total_ingresos_mes > 0:
                    tasa_ahorro_pct = (balance_mes / total_ingresos_mes) * 100
                else:
                    tasa_ahorro_pct = 0

                col4.metric(
                    "💾 Tasa Ahorro",
                    f"{tasa_ahorro_pct:.1f}%",
                    delta=f"{balance_mes:.0f} €",
                    help="Porcentaje de tus ingresos totales que has logrado ahorrar. Ideal: >20%. Mide tu capacidad de ahorro real"
                )

                st.markdown("---")

                # Mostrar presupuestos del mes (si existen)
                resumen_presupuestos = db_manager.obtener_resumen_presupuestos(mes, año)
                if resumen_presupuestos:
                    st.subheader("📊 Presupuestos del Mes")

                    for presupuesto in resumen_presupuestos:
                        categoria = presupuesto['categoria']
                        limite = presupuesto['presupuesto']
                        gastado = presupuesto['gastado']
                        restante = presupuesto['restante']
                        porcentaje = presupuesto['porcentaje_usado']
                        gastado_bruto = presupuesto.get('gastado_bruto', gastado)
                        reembolsos = presupuesto.get('reembolsos_asignados', 0)

                        # Determinar color según porcentaje usado (usando design system)
                        color, barra_color, _ = get_budget_color(porcentaje)

                        with st.container():
                            col1, col2, col3 = st.columns([3, 1, 1])

                            with col1:
                                st.markdown(f"**{color} {categoria}**")
                                # Mostrar desglose si hay reembolsos asignados
                                if reembolsos > 0:
                                    st.caption(f"💰 Bruto: {gastado_bruto:.2f} € | Reembolsos: {reembolsos:.2f} € | Neto: {gastado:.2f} €")
                                # Barra de progreso visual (asegurar rango [0.0, 1.0])
                                st.progress(max(0.0, min(porcentaje / 100, 1.0)))

                            with col2:
                                st.metric("Gastado", f"{gastado:.2f} €")

                            with col3:
                                st.metric("Restante", f"{restante:.2f} €",
                                         delta=f"{porcentaje:.1f}% usado",
                                         delta_color="inverse" if porcentaje > 100 else "off")

                    st.markdown("---")

                # Gráficos en columnas
                col_grafico, col_detalle = st.columns([2, 1])

                with col_grafico:
                    st.subheader("📊 Distribución de Gastos")
                    fig = visualizer.grafico_distribucion_gastos(datos_mes['gastos_por_categoria'])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True, key=f"plot_gastos_mes_{mes}_{año}")
                    else:
                        st.info("Sin datos de gastos")

                with col_detalle:
                    st.markdown("### 📋 Desglose")
                    if datos_mes['gastos_por_categoria']:
                        df = pd.DataFrame(list(datos_mes['gastos_por_categoria'].items()),
                                        columns=['Categoría', 'Importe'])
                        df['Importe'] = df['Importe'].abs()
                        total = df['Importe'].sum()
                        df['%'] = (df['Importe'] / total * 100).round(1)

                        st.dataframe(
                            df,
                            column_config={
                                "Importe": st.column_config.NumberColumn(format="%.0f €"),
                                "%": st.column_config.NumberColumn(format="%.1f%%"),
                            },
                            hide_index=True,
                            use_container_width=True
                        )

                st.markdown("---")

                # Gráfico de evolución del saldo disponible
                st.subheader("📈 Evolución del Saldo Disponible")
                transacciones = db_manager.obtener_transacciones(mes=mes, año=año)

                if transacciones:
                    df_trans = pd.DataFrame(transacciones)
                    df_trans['fecha'] = pd.to_datetime(df_trans['fecha'])

                    # Calcular el saldo inicial del mes:
                    # Método robusto que maneja ingresos y gastos en el último día del mes anterior
                    conn_temp = db_manager.get_db_connection()
                    cursor_temp = conn_temp.cursor()

                    # 1. Obtener la fecha máxima del mes anterior
                    cursor_temp.execute("""
                        SELECT MAX(fecha) as ultima_fecha
                        FROM transacciones
                        WHERE (año < ? OR (año = ? AND mes < ?))
                    """, (año, año, mes))

                    fecha_max = cursor_temp.fetchone()['ultima_fecha']

                    if fecha_max:
                        # 2. Obtener todas las transacciones del último día
                        cursor_temp.execute("""
                            SELECT saldo_posterior, importe
                            FROM transacciones
                            WHERE fecha = ? AND saldo_posterior IS NOT NULL
                        """, (fecha_max,))

                        trans_ultimo_dia = cursor_temp.fetchall()

                        if trans_ultimo_dia:
                            # 3. Calcular suma neta de importes del último día
                            suma_importes = sum(t['importe'] for t in trans_ultimo_dia)

                            # 4. Elegir saldo según si hubo ingreso o gasto neto
                            saldos = [t['saldo_posterior'] for t in trans_ultimo_dia]
                            if suma_importes >= 0:
                                # Ingreso neto → el saldo más ALTO es el final
                                saldo_inicial = max(saldos)
                            else:
                                # Gasto neto → el saldo más BAJO es el final
                                saldo_inicial = min(saldos)
                        else:
                            saldo_inicial = config_manager.obtener_saldo_inicial()
                    else:
                        saldo_inicial = config_manager.obtener_saldo_inicial()

                    conn_temp.close()

                    # Ahora ordenar para el gráfico por fecha e ID
                    df_trans = df_trans.sort_values(['fecha', 'id'], ascending=[True, True])

                    # SIEMPRE CALCULAR el saldo para evitar inconsistencias del banco
                    # El saldo_posterior del banco puede tener errores de ordenamiento
                    df_trans['saldo_disponible'] = saldo_inicial + df_trans['importe'].cumsum()

                    # Añadir punto inicial del mes (saldo al cierre del mes anterior)
                    fecha_inicial = df_trans['fecha'].min() - pd.Timedelta(days=1)
                    df_inicial = pd.DataFrame([{
                        'fecha': fecha_inicial,
                        'importe': 0,
                        'saldo_disponible': saldo_inicial
                    }])

                    # Combinar con las transacciones del mes
                    df_completo = pd.concat([df_inicial, df_trans[['fecha', 'saldo_disponible']]], ignore_index=True)

                    # Crear gráfico de línea
                    fig = go.Figure()

                    # Preparar etiquetas de fecha para el eje X
                    df_completo['fecha_str'] = df_completo['fecha'].dt.strftime('%d/%m/%Y')

                    # Línea de evolución del saldo (usando índices para equidistancia)
                    fig.add_trace(go.Scatter(
                        x=df_completo['fecha_str'],
                        y=df_completo['saldo_disponible'],
                        mode='lines+markers',
                        name='Saldo',
                        line=dict(color=Colors.PRIMARY, width=2.5),
                        marker=dict(
                            size=8,
                            color=df_completo['saldo_disponible'],
                            colorscale=[[0, Colors.ERROR], [0.5, Colors.WARNING], [1, Colors.SUCCESS]],
                            showscale=False,
                            line=dict(width=1, color='white')
                        ),
                        fill='tonexty',
                        fillcolor=f'rgba(31, 119, 180, 0.1)',
                        hovertemplate='<b>%{x}</b><br>Saldo: %{y:.2f} €<extra></extra>'
                    ))

                    # Línea de referencia en y=0
                    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5,
                                 annotation_text="Break Even", annotation_position="right")

                    # Línea de saldo inicial
                    fig.add_hline(y=saldo_inicial, line_dash="dot", line_color="blue", opacity=0.3,
                                 annotation_text=f"Inicial: {saldo_inicial:.0f}€",
                                 annotation_position="left")

                    fig.update_layout(
                        title=f"Evolución del Saldo - {nombre_mes_seleccionado} {año}",
                        xaxis_title="Fecha",
                        yaxis_title="Saldo Disponible (€)",
                        hovermode='closest',
                        height=450,
                        showlegend=False,
                        xaxis=dict(
                            tickangle=-45,
                            tickmode='auto',
                            nticks=20
                        )
                    )

                    st.plotly_chart(fig, use_container_width=True, key=f"plot_evolucion_saldo_mes_{mes}_{año}")

                    # Estadísticas del mes - Layout responsive (2x2)
                    col1, col2 = st.columns(2)
                    num_transacciones = len(df_trans)
                    col1.metric(
                        "📊 Transacciones",
                        num_transacciones,
                        help="Número total de transacciones registradas en el mes"
                    )
                    col2.metric(
                        "📈 Saldo Inicial",
                        f"{saldo_inicial:.2f} €",
                        help="Saldo disponible al inicio del mes (cierre del mes anterior)"
                    )

                    col3, col4 = st.columns(2)
                    col3.metric(
                        "💰 Saldo Final",
                        f"{df_trans['saldo_disponible'].iloc[-1]:.2f} €",
                        delta=f"{df_trans['saldo_disponible'].iloc[-1] - saldo_inicial:.2f} €",
                        help="Saldo disponible al final del mes con la variación respecto al inicio"
                    )
                    col4.metric(
                        "📊 Variación (Max-Min)",
                        f"{df_trans['saldo_disponible'].max() - df_trans['saldo_disponible'].min():.2f} €",
                        help="Diferencia entre el saldo máximo y mínimo alcanzado durante el mes"
                    )
                else:
                    st.info("No hay transacciones registradas en este mes")

        else:  # Vista anual
            with st.spinner("Calculando métricas anuales..."):
                datos_anuales = metrics.calcular_totales_anual(año)

                if datos_anuales:
                    # Métricas anuales - Layout responsive (2x2)
                    col1, col2 = st.columns(2)
                    col1.metric(
                        "💰 Ingresos Anuales",
                        f"{datos_anuales['total_ingresos']:.2f} €",
                        help="Suma total de ingresos en todos los meses del año (sin reembolsos)"
                    )
                    col2.metric(
                        "💸 Gastos Netos Anuales",
                        f"{abs(datos_anuales['gastos_netos']):.2f} €",
                        delta=f"-{datos_anuales['total_reembolsos']:.2f} € reembolsados" if datos_anuales['total_reembolsos'] > 0 else None,
                        delta_color="normal",
                        help=f"Gastos brutos: {abs(datos_anuales['total_gastos']):.2f}€ - Reembolsos: {datos_anuales['total_reembolsos']:.2f}€"
                    )

                    col3, col4 = st.columns(2)
                    col3.metric(
                        "⚖️ Balance Anual",
                        f"{datos_anuales['balance_neto']:.2f} €",
                        delta_color="normal" if datos_anuales['balance_neto'] > 0 else "inverse",
                        help="Balance neto del año completo (Total Ingresos - Total Gastos)"
                    )

                    # Ahorro anual
                    ahorro_anual = datos_anuales['balance_neto']
                    if datos_anuales['total_ingresos'] > 0:
                        tasa_anual = (ahorro_anual / datos_anuales['total_ingresos']) * 100
                    else:
                        tasa_anual = 0
                    col4.metric(
                        "💾 Tasa Ahorro Anual",
                        f"{tasa_anual:.1f}%",
                        help="Porcentaje de ahorro sobre el total de ingresos del año. Mide tu capacidad de ahorro anual"
                    )

                    st.markdown("---")

                    # Gráficos anuales
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 📈 Evolución Mensual")
                        fig = visualizer.grafico_evolucion_anual(datos_anuales['evolucion_mensual'], NOMBRES_MESES)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True, key=f"plot_evolucion_anual_{año}")

                    with col2:
                        st.markdown("### 📊 Distribución Anual")
                        fig = visualizer.grafico_distribucion_gastos(datos_anuales['gastos_por_categoria'])
                        if fig:
                            st.plotly_chart(fig, use_container_width=True, key=f"plot_distribucion_anual_{año}")
                else:
                    st.info(f"No hay datos para el año {año}")

    # ========== TAB 2: ANÁLISIS AVANZADO ==========
    with tab_analisis:
        # Usar el mismo selector de vista del tab principal
        if vista_periodo == "Mes":
            with st.spinner("Calculando análisis avanzado..."):
                # Financial Health Score destacado
                health = metrics.calcular_financial_health_score(mes, año)

                st.subheader("🏆 Financial Health Score")

                score_cols = st.columns([1, 2, 1])
                with score_cols[1]:
                    # Score grande y centrado
                    score_emoji = {
                        'verde': '🌟',
                        'azul': '👍',
                        'amarillo': '⚠️',
                        'rojo': '❌'
                    }.get(health['color'], '📊')

                    st.markdown(f"""
                    <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
                        <h1 style='font-size: 4em; margin: 0;'>{health['score']}</h1>
                        <p style='font-size: 1.5em; margin: 0;'>{score_emoji} {health['evaluacion']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # Métricas en expanders organizados
                with st.expander("💰 Ahorro y Proyecciones", expanded=True):
                    col1, col2, col3 = st.columns(3)

                    tasa_ahorro = metrics.calcular_tasa_ahorro(mes, año)
                    col1.metric(
                        "Tasa de Ahorro",
                        f"{tasa_ahorro['tasa_ahorro']:.1f}%",
                        delta=f"{tasa_ahorro['ahorro_absoluto']:.0f} €",
                        help="% de tus ingresos que lograste ahorrar. Ideal >20%. Útil para evaluar tu disciplina financiera"
                    )

                    gasto_diario = metrics.calcular_gasto_promedio_diario(mes, año)
                    col2.metric(
                        "Gasto Promedio/Día",
                        f"{gasto_diario['promedio_diario']:.2f} €",
                        delta=f"Proyección mes: {gasto_diario['proyeccion_mes']:.0f} €",
                        help="Cuánto gastas en promedio cada día. Te ayuda a controlar tus gastos diarios y proyectar el total del mes"
                    )

                    proyeccion = metrics.calcular_proyeccion_balance(3)
                    col3.metric(
                        "Balance en 3 Meses",
                        f"{proyeccion['balance_proyectado']:.0f} €",
                        delta=f"Confianza: {proyeccion['confianza']}",
                        help="Proyección de tu balance en 3 meses basado en tu comportamiento histórico. Útil para planificar gastos futuros"
                    )

                with st.expander("📊 Efficiency Ratios"):
                    ratios = metrics.calcular_efficiency_ratios(mes, año)
                    st.info(f"**{ratios['evaluacion']}**")

                    col1, col2, col3 = st.columns(3)
                    col1.metric(
                        "FIJOS/Ingresos",
                        f"{ratios.get('ratio_fijos', 0):.1f}%",
                        delta="Ideal <30%",
                        help="% de gastos fijos sobre tus ingresos. Ideal <30%. Mide qué porción de tus ingresos va a gastos obligatorios (vivienda, servicios, etc.)"
                    )
                    col2.metric(
                        "DISFRUTE/Ingresos",
                        f"{ratios.get('ratio_disfrute', 0):.1f}%",
                        delta="Ideal <30%",
                        help="% de gastos de disfrute sobre tus ingresos. Ideal <30%. Mide cuánto destinas a ocio, entretenimiento y placeres personales"
                    )
                    col3.metric(
                        "EXTRA/Ingresos",
                        f"{ratios.get('ratio_extraordinarios', 0):.1f}%",
                        delta="Ideal <10%",
                        help="% de gastos extraordinarios sobre tus ingresos. Ideal <10%. Gastos imprevistos o no recurrentes que afectan tu presupuesto"
                    )

                with st.expander("📉 Variación vs Mes Anterior"):
                    variacion = metrics.calcular_variacion_mensual(mes, año)

                    if variacion['gastos_anterior'] > 0:
                        delta = variacion['variacion_total']
                        if delta < 0:
                            st.success(f"✅ **{abs(delta):.1f}% menos** que el mes pasado")
                        elif delta > 0:
                            st.warning(f"⚠️ **{delta:.1f}% más** que el mes pasado")
                        else:
                            st.info("➡️ Gastos similares")

                        col1, col2 = st.columns(2)
                        col1.metric("Mes Actual", f"{variacion['gastos_actual']:.2f} €")
                        col2.metric("Mes Anterior", f"{variacion['gastos_anterior']:.2f} €")

                        # Por categoría
                        for cat, datos in variacion['por_categoria'].items():
                            if datos['variacion'] != 0:
                                icono = "📈" if datos['variacion'] > 0 else "📉"
                                st.caption(f"{icono} **{cat}**: {datos['variacion']:+.1f}%")
                    else:
                        st.info("Sin datos del mes anterior")

                with st.expander("🔝 Top 10 Gastos"):
                    top = metrics.calcular_top_gastos(mes, año, 10)
                    if top:
                        df = pd.DataFrame(top)
                        df['importe'] = df['importe'].abs()
                        st.dataframe(
                            df[['fecha', 'concepto', 'importe', 'categoria']],
                            column_config={
                                "fecha": "Fecha",
                                "concepto": "Concepto",
                                "importe": st.column_config.NumberColumn("Importe", format="%.2f €"),
                                "categoria": "Categoría"
                            },
                            hide_index=True,
                            use_container_width=True
                        )

                        total_top = df['importe'].sum()
                        datos_mes_top = metrics.calcular_totales_mes(mes, año)
                        pct = (total_top / abs(datos_mes_top['gastos_netos'])) * 100
                        st.caption(f"💡 Representan el **{pct:.1f}%** del total de gastos netos")

                with st.expander("🔍 Desglose del Health Score"):
                    # Layout responsive (2x2)
                    col1, col2 = st.columns(2)
                    desg = health['desglose']

                    col1.metric(
                        "Ahorro",
                        f"{desg['ahorro']}/30",
                        help="Puntos por tu capacidad de ahorro. Máximo 30pts. Basado en tu tasa de ahorro mensual"
                    )
                    col2.metric(
                        "Eficiencia",
                        f"{desg['eficiencia_fijos']}/25",
                        help="Puntos por eficiencia en gastos fijos. Máximo 25pts. Cuanto menor sea tu ratio de gastos fijos, más puntos"
                    )

                    col3, col4 = st.columns(2)
                    col3.metric(
                        "Estabilidad",
                        f"{desg['estabilidad']}/25",
                        help="Puntos por estabilidad financiera. Máximo 25pts. Basado en tu balance positivo y consistencia"
                    )
                    col4.metric(
                        "Tendencia",
                        f"{desg['tendencia']}/20",
                        help="Puntos por tendencia de mejora. Máximo 20pts. Si gastas menos que el mes anterior, ganas puntos"
                    )

        else:  # Vista anual
            st.subheader("📅 Métricas Anuales Avanzadas")

            datos_anuales = metrics.calcular_totales_anual(año)

            if datos_anuales:
                col1, col2, col3 = st.columns(3)

                # Ahorro anual total
                ahorro_anual = datos_anuales['balance_neto']
                ingresos_anuales = datos_anuales['total_ingresos']
                gastos_anuales_netos = abs(datos_anuales['gastos_netos'])

                tasa_ahorro_anual = (ahorro_anual / ingresos_anuales * 100) if ingresos_anuales > 0 else 0

                col1.metric(
                    "💰 Ahorro Anual Total",
                    f"{ahorro_anual:.2f} €",
                    delta=f"Tasa: {tasa_ahorro_anual:.1f}%",
                    help="Total ahorrado en el año completo. La tasa muestra qué % de tus ingresos anuales has logrado ahorrar"
                )

                # Promedio mensual
                promedio_gasto_mensual = gastos_anuales_netos / 12
                col2.metric(
                    "📊 Promedio Gasto Neto/Mes",
                    f"{promedio_gasto_mensual:.2f} €",
                    help="Gasto neto promedio mensual del año (después de reembolsos). Útil para establecer un presupuesto mensual realista"
                )

                promedio_ingreso_mensual = ingresos_anuales / 12
                col3.metric(
                    "💵 Promedio Ingreso/Mes",
                    f"{promedio_ingreso_mensual:.2f} €",
                    help="Ingreso promedio mensual del año. Te ayuda a entender tu capacidad financiera mensual típica"
                )

                st.markdown("---")

                # Mejor y peor mes
                evol = datos_anuales['evolucion_mensual']
                if not evol.empty and 'balance' in evol.columns:
                    mejor_mes_idx = evol['balance'].idxmax()
                    peor_mes_idx = evol['balance'].idxmin()

                    col1, col2 = st.columns(2)

                    with col1:
                        st.success(f"🌟 **Mejor Mes:** {NOMBRES_MESES.get(mejor_mes_idx + 1, 'N/A')}")
                        st.write(f"Balance: {evol.loc[mejor_mes_idx, 'balance']:.2f} €")

                    with col2:
                        st.error(f"⚠️ **Peor Mes:** {NOMBRES_MESES.get(peor_mes_idx + 1, 'N/A')}")
                        st.write(f"Balance: {evol.loc[peor_mes_idx, 'balance']:.2f} €")

                st.markdown("---")

                # Distribución anual por categoría
                st.markdown("### 📊 Distribución Anual Detallada")

                gastos_cat = datos_anuales['gastos_por_categoria']
                if gastos_cat:
                    df_cat = pd.DataFrame(list(gastos_cat.items()), columns=['Categoría', 'Total'])
                    df_cat['Total'] = df_cat['Total'].abs()
                    df_cat['%'] = (df_cat['Total'] / df_cat['Total'].sum() * 100).round(1)
                    df_cat['Promedio/Mes'] = (df_cat['Total'] / 12).round(2)

                    st.dataframe(
                        df_cat,
                        column_config={
                            "Total": st.column_config.NumberColumn(format="%.2f €"),
                            "%": st.column_config.NumberColumn(format="%.1f%%"),
                            "Promedio/Mes": st.column_config.NumberColumn(format="%.2f €")
                        },
                        hide_index=True,
                        use_container_width=True
                    )
            else:
                st.info(f"No hay datos para el año {año}")

    # ========== TAB 3: HISTÓRICO ==========
    with tab_historico:
        st.subheader("📉 Evolución Últimos 12 Meses")

        df_evol = metrics.calcular_evolucion_mensual()
        fig = visualizer.grafico_evolucion_mensual(df_evol)

        if fig:
            st.plotly_chart(fig, use_container_width=True, key=f"plot_historico_mensual_{año}")

            # Estadísticas del histórico
            if not df_evol.empty:
                with st.expander("📊 Estadísticas del Período"):
                    # Layout responsive (2x2)
                    col1, col2 = st.columns(2)
                    col1.metric("💰 Total Ingresos", f"{df_evol['ingresos'].sum():.2f} €")
                    col2.metric("💸 Total Gastos Netos", f"{abs(df_evol['gastos_netos'].sum()):.2f} €")

                    col3, col4 = st.columns(2)
                    col3.metric("⚖️ Balance Total", f"{df_evol['balance'].sum():.2f} €")
                    col4.metric("📈 Promedio Balance/Mes", f"{df_evol['balance'].mean():.2f} €")
        else:
            st.info("No hay suficientes datos históricos")

def mostrar_añadir_gasto():
    """Página para añadir gastos individuales manualmente"""
    st.title("➕ Añadir Nuevo Gasto")
    st.markdown("Registra gastos individuales que no están en tu extracto bancario o que quieres anotar inmediatamente.")

    # Validación en tiempo real (fuera del formulario)
    validation_errors = []

    # Formulario de añadir gasto
    with st.form("form_nuevo_gasto", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            fecha_gasto = st.date_input(
                "📅 Fecha",
                value=datetime.date.today(),
                help="Fecha del gasto"
            )

            concepto = st.text_input(
                "📝 Concepto",
                placeholder="Ej: Café con amigos, Uber, etc.",
                help="Descripción del gasto"
            )

        with col2:
            importe = st.number_input(
                "💶 Importe (€)",
                min_value=0.01,
                value=10.00,
                step=0.01,
                format="%.2f",
                help="Cantidad gastada (siempre positiva, se guardará como negativa)"
            )

            categoria = st.selectbox(
                "🏷️ Categoría",
                ["DISFRUTE", "FIJOS", "EXTRAORDINARIOS"],
                help="Tipo de gasto"
            )

        notas = st.text_area(
            "📋 Notas (opcional)",
            placeholder="Añade cualquier información adicional...",
            height=80
        )

        # Botones
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            submit = st.form_submit_button("💾 Guardar Gasto", use_container_width=True, type="primary")
        with col_btn2:
            clear = st.form_submit_button("🗑️ Limpiar", use_container_width=True)

        if submit:
            # Validaciones
            if not concepto or concepto.strip() == "":
                st.error("❌ El concepto no puede estar vacío")
            elif importe <= 0:
                st.error("❌ El importe debe ser mayor que 0")
            else:
                # Insertar en base de datos
                try:
                    # Convertir importe a negativo (es un gasto)
                    importe_negativo = -abs(importe)

                    # Generar ID único
                    id_transaccion = db_manager.generar_uuid()

                    # Insertar transacción
                    db_manager.insertar_transaccion(
                        id=id_transaccion,
                        fecha=fecha_gasto,
                        concepto=concepto.strip(),
                        importe=importe_negativo,
                        categoria=categoria,
                        tipo='GASTO',
                        mes=fecha_gasto.month,
                        año=fecha_gasto.year,
                        notas=notas.strip() if notas else None,
                        saldo_posterior=None  # Se calculará al importar Excel
                    )

                    st.success(f"✅ Gasto guardado: {concepto} - {abs(importe_negativo):.2f}€")
                    st.balloons()

                    # Mostrar resumen
                    with st.expander("📊 Ver resumen del gasto", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Fecha", fecha_gasto.strftime("%d/%m/%Y"))
                        col2.metric("Importe", f"{abs(importe_negativo):.2f} €")
                        col3.metric("Categoría", categoria)

                except Exception as e:
                    # Log técnico para debugging (si tienes logger)
                    # logger.error(f"Error al insertar gasto: {e}")
                    st.error("❌ No se pudo guardar el gasto. Por favor, inténtalo de nuevo o verifica los datos.")

    # Separador
    st.markdown("---")

    # Últimos gastos añadidos manualmente
    st.subheader("📝 Últimos gastos registrados")

    try:
        # Obtener últimos 10 gastos
        conn = db_manager.get_db_connection()
        query = """
        SELECT fecha, concepto, importe, categoria
        FROM transacciones
        WHERE tipo = 'GASTO'
        ORDER BY fecha DESC, id DESC
        LIMIT 10
        """
        df_ultimos = pd.read_sql_query(query, conn)
        conn.close()

        if not df_ultimos.empty:
            df_ultimos['importe'] = df_ultimos['importe'].abs()
            df_ultimos.columns = ['Fecha', 'Concepto', 'Importe (€)', 'Categoría']

            st.dataframe(
                df_ultimos,
                column_config={
                    "Fecha": st.column_config.DateColumn(format="DD/MM/YYYY"),
                    "Importe (€)": st.column_config.NumberColumn(format="%.2f €"),
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("Aún no has registrado ningún gasto")

    except Exception as e:
        # logger.error(f"Error al cargar últimos gastos: {e}")
        st.error("❌ No se pudieron cargar los últimos gastos. Intenta recargar la página.")

    # Información sobre duplicados
    with st.expander("ℹ️ ¿Qué pasa cuando importo mi extracto bancario?"):
        st.markdown("""
        **Detección automática de duplicados:**

        Cuando importes tu extracto bancario del mes:
        1. El sistema buscará transacciones duplicadas (misma fecha + importe + concepto)
        2. Si encuentra un duplicado con un gasto que añadiste manualmente:
           - **Prioriza los datos del banco** (son más fiables)
           - Actualiza la transacción con los datos bancarios
           - Mantiene tu categoría si ya la habías clasificado

        **Recomendación:**
        - Usa esta página para gastos que quieres registrar inmediatamente
        - Al final del mes, importa tu extracto bancario normalmente
        - El sistema se encargará de evitar duplicados automáticamente
        """)

def mostrar_transacciones():
    st.title("💸 Transacciones")
    st.markdown("Aquí puedes ver, filtrar y editar tus transacciones.")

    # --- Filtros ---
    col1, col2, col3 = st.columns(3)
    with col1:
        # Usar session_state compartido con Dashboard
        año_actual = datetime.date.today().year
        # Obtener años disponibles desde la BD (años con datos + actual + siguiente)
        años_disponibles = db_manager.obtener_años_disponibles()
        index_año = años_disponibles.index(st.session_state.año_seleccionado) if st.session_state.año_seleccionado in años_disponibles else len(años_disponibles) - 1

        año = st.selectbox("Año", años_disponibles, index=index_año, key="trans_año")
        # Actualizar session_state
        st.session_state.año_seleccionado = año

    with col2:
        # Usar session_state compartido con Dashboard
        meses_disponibles = list(NOMBRES_MESES.values())
        index_mes = st.session_state.mes_seleccionado - 1

        nombre_mes_seleccionado = st.selectbox("Mes", meses_disponibles, index=index_mes, key="trans_mes")
        mes = MESES_INVERTIDO[nombre_mes_seleccionado]
        # Actualizar session_state
        st.session_state.mes_seleccionado = mes
    with col3:
        # Obtener categorías de la base de datos para el filtro
        # Se podría mejorar el rendimiento cacheando esta llamada
        # (Esta es una simplificación, se podría cachear)
        categorias_db = list(db_manager.obtener_totales_por_categoria(mes, año).keys())
        categorias_seleccionadas = st.multiselect("Categorías", ["Todas"] + categorias_db, default="Todas")

    # --- Cargar y mostrar datos ---
    with st.spinner("Cargando transacciones..."):
        transacciones = db_manager.obtener_transacciones(mes=mes, año=año)
        df_original = pd.DataFrame(transacciones)

        if not df_original.empty:
            df_filtrado = df_original.copy()
            if "Todas" not in categorias_seleccionadas and categorias_seleccionadas:
                df_filtrado = df_filtrado[df_filtrado['categoria'].isin(categorias_seleccionadas)]
            
            # Convertir la columna de fecha a objetos de fecha para el editor
            df_filtrado['fecha'] = pd.to_datetime(df_filtrado['fecha'])

            st.info("Puedes editar las celdas directamente. Haz clic en 'Guardar Cambios' para persistir las modificaciones.")
            
            # Configuración del editor de datos
            configuracion_columnas = {
                "id": st.column_config.NumberColumn("ID", disabled=True),
                "fecha": st.column_config.DateColumn("Fecha", format="YYYY-MM-DD"),
                "concepto": st.column_config.TextColumn("Concepto", width="large"), # 'width' aquí se refiere al tamaño de la columna, no al aviso.
                "importe": st.column_config.NumberColumn("Importe", format="%.2f €"),
                "categoria": st.column_config.SelectboxColumn("Categoría", options=["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "REEMBOLSO", "INGRESO", "SIN_CLASIFICAR"], width="medium")
            }
            
            df_editado = st.data_editor(
                df_filtrado,
                column_config=configuracion_columnas,
                num_rows="fixed",
                hide_index=True,
                use_container_width=True
            )

            if st.button("💾 Guardar Cambios"):
                # Asegurarse de que los dataframes originales y editados tengan los mismos tipos y orden de columnas para una comparación justa
                df_original_comp = df_original.set_index('id').sort_index()
                df_editado_comp = df_editado.set_index('id').sort_index()
                
                # Convertir la fecha del df_original a datetime para comparar con el editor
                df_original_comp['fecha'] = pd.to_datetime(df_original_comp['fecha'])
                
                # Encontrar las filas que han cambiado
                try:
                    # `compare` devuelve un DataFrame con las diferencias
                    diferencias = df_original_comp.compare(df_editado_comp)
                except ValueError: # Ocurre si no hay cambios
                    diferencias = pd.DataFrame()
                
                if not diferencias.empty:
                    with st.spinner("Guardando cambios en la base de datos..."):
                        updates_exitosos = 0
                        # Iterar sobre los índices de las filas modificadas
                        for id_transaccion in diferencias.index.unique():
                            # Obtener la fila completa de datos editados
                            fila_editada = df_editado_comp.loc[id_transaccion]
                            campos_a_actualizar = fila_editada.to_dict()
                            # **LA SOLUCIÓN CLAVE**: Convertir Timestamp a objeto date
                            if 'fecha' in campos_a_actualizar and isinstance(campos_a_actualizar['fecha'], pd.Timestamp):
                                campos_a_actualizar['fecha'] = campos_a_actualizar['fecha'].date()
                                
                            if campos_a_actualizar:
                                if db_manager.actualizar_transaccion(id_transaccion, campos_a_actualizar):
                                    updates_exitosos += 1
                    st.success(f"{updates_exitosos} transacciones actualizadas correctamente.")
                    st.rerun()
                else:
                    st.info("No se detectaron cambios para guardar.")
        else:
            st.info("No se encontraron transacciones para el período seleccionado.")

def mostrar_importar():
    st.title("📥 Importar desde Excel")
    st.markdown("Sube aquí tu archivo Excel con los movimientos bancarios para procesarlos e importarlos a la base de datos.")

    uploaded_file = st.file_uploader(
        "Elige un archivo Excel (.xlsx)", 
        type=['xlsx']
    )

    if uploaded_file is not None:
        # Almacenar el estado de la importación en la sesión
        if 'import_data' not in st.session_state or st.session_state.get('uploaded_filename') != uploaded_file.name:
            with st.spinner("Procesando archivo Excel..."):
                transacciones, stats = excel_reader.leer_excel(uploaded_file)
                st.session_state.import_data = transacciones
                st.session_state.import_stats = stats
                st.session_state.uploaded_filename = uploaded_file.name
                # --- Detección de duplicados ---
                st.session_state.nuevas_transacciones = []
                st.session_state.transacciones_duplicadas = []
                for t in transacciones:
                    if db_manager.transaccion_existe(fecha=t['fecha'], importe=t['importe']):
                        st.session_state.transacciones_duplicadas.append(t)
                    else:
                        st.session_state.nuevas_transacciones.append(t)

        stats = st.session_state.import_stats
        transacciones = st.session_state.import_data

        st.subheader("Resumen de la importación")
        if "error" in stats:
            st.error(f"Ocurrió un error al leer el archivo: {stats['error']}")
        else:
            nuevas = st.session_state.get('nuevas_transacciones', [])
            duplicadas = st.session_state.get('transacciones_duplicadas', [])

            col1, col2, col3 = st.columns(3)
            col1.metric("Hojas procesadas", stats.get('total_sheets_processed', 0))
            col2.metric("Transacciones Nuevas", len(nuevas))
            col3.metric("Potenciales Duplicados", len(duplicadas), delta_color="off")

            if transacciones:
                st.subheader("Vista Previa de Transacciones a Importar")
                st.dataframe(pd.DataFrame(nuevas).head(10))

                accion_duplicados = "omitir"
                if duplicadas:
                    st.warning(f"Se han detectado {len(duplicadas)} transacciones que podrían estar ya registradas (misma fecha e importe).")
                    st.write("Transacciones duplicadas detectadas:")
                    st.dataframe(pd.DataFrame(duplicadas))
                    accion_duplicados = st.radio(
                        "¿Qué quieres hacer con estas transacciones duplicadas?",
                        ('Omitir duplicados (Recomendado)', 'Importar todo (creará duplicados)'),
                        key='accion_duplicados'
                    )

                if st.button("✅ Confirmar e Importar"):
                    transacciones_a_importar = []
                    if accion_duplicados == 'Omitir duplicados (Recomendado)':
                        transacciones_a_importar = nuevas
                        st.info(f"Se omitirán {len(duplicadas)} transacciones duplicadas.")
                    else: # Importar todo
                        transacciones_a_importar = transacciones
                        st.warning("Se importarán todas las transacciones, incluyendo posibles duplicados.")

                    if not transacciones_a_importar:
                        st.info("No hay nuevas transacciones para importar.")
                    else:
                        with st.spinner("Importando transacciones..."):
                            count = 0
                            for t in transacciones_a_importar:
                                categoria_final = categorizer.clasificar_transaccion(t['concepto'], t['importe'])
                                db_manager.insertar_transaccion(
                                    fecha=t['fecha'],
                                    concepto=t['concepto'],
                                    importe=t['importe'],
                                    categoria=categoria_final,
                                    tipo=t['tipo'],
                                    mes=t['mes'],
                                    año=t['año'],
                                    notas=t.get('notas', ''),
                                    saldo_posterior=t.get('saldo_posterior')
                                )
                                count += 1
                        
                        st.success(f"¡Éxito! Se importaron {count} nuevas transacciones.")
                        st.balloons()
                        # Limpiar el estado para permitir una nueva subida
                        for key in ['import_data', 'import_stats', 'uploaded_filename', 'nuevas_transacciones', 'transacciones_duplicadas']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.rerun()

def mostrar_categorias():
    st.title("🏷️ Categorías y Reglas de Clasificación")
    st.markdown("Gestiona las reglas que se usan para clasificar automáticamente tus transacciones.")

    # Cargar y mostrar las reglas actuales
    try:
        with open(categorizer.RULES_FILE, 'r', encoding='utf-8') as f:
            reglas_actuales = json.load(f)['reglas']
        st.subheader("Reglas Actuales")

        # Mostrar cada regla en un expander para poder editarla o eliminarla
        for i, regla in enumerate(reglas_actuales):
            patron = regla.get("patron", "")
            importes = regla.get("importes_exactos", [])
            categoria = regla.get("categoria", "N/A")
            
            # Crear un título descriptivo para el expander
            titulo_expander = f"Patrón: `{patron}`" if patron else f"Importes: `{', '.join(map(str, importes))}`"
            titulo_expander += f" -> **{categoria}**"

            with st.expander(titulo_expander):
                st.write(f"**Categoría:** {regla.get('categoria')}")
                st.write(f"**Tipo:** {regla.get('tipo')}")
                if importes:
                    st.write(f"**Importes exactos:** {', '.join(map(str, importes))}")

                col1, col2 = st.columns([1, 0.1])
                
                with col1:
                    # El botón de editar podría abrir un modal o un formulario aquí mismo
                    # Por simplicidad, por ahora solo mostramos la opción
                    if st.button("✏️ Editar", key=f"edit_{i}"):
                        st.info("Funcionalidad de edición en desarrollo. Por ahora, elimina la regla y créala de nuevo.", icon="🚧")

                with col2:
                    if st.button("🗑️ Eliminar", key=f"del_{i}", help="Eliminar esta regla permanentemente"):
                        if categorizer.eliminar_regla(patron):
                            st.success(f"Regla para '{patron}' eliminada.")
                            st.rerun()
                        else:
                            st.error("No se pudo eliminar la regla.")

    except (FileNotFoundError, json.JSONDecodeError):
        st.error("No se pudo cargar el archivo de reglas.")
        reglas_actuales = []
    except KeyError:
        st.info("El archivo de reglas está vacío o no tiene el formato correcto.")
        reglas_actuales = []

    st.markdown("---")

    # Formulario para añadir nueva regla
    st.subheader("Añadir Nueva Regla")
    with st.form(key="nueva_regla_form", clear_on_submit=True):
        nuevo_patron = st.text_input("Patrón de texto (puede ser una expresión regular)")
        importes_str = st.text_input("Importes exactos (opcional, separados por coma, ej: 500, 275)")
        nueva_categoria = st.selectbox("Categoría a asignar", ["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "INGRESO"])
        nuevo_tipo = st.selectbox("Tipo de transacción", ["GASTO", "INGRESO"])
        
        submit_button = st.form_submit_button(label="✨ Añadir Regla")

        if submit_button:
            if nuevo_patron or importes_str:
                importes_exactos = []
                if importes_str:
                    try:
                        # Convertir el string de importes a una lista de floats
                        importes_exactos = [float(i.strip()) for i in importes_str.split(',')]
                    except ValueError:
                        st.error("El formato de los importes no es válido. Usa números separados por comas (ej: 500, 275.5).")
                        return # Detener la ejecución si hay error
                if categorizer.guardar_regla(nuevo_patron, nueva_categoria, nuevo_tipo, importes_exactos):
                    st.success(f"¡Regla '{nuevo_patron}' -> '{nueva_categoria}' guardada!")
                    st.rerun()
                else:
                    st.error("No se pudo guardar la regla. ¿Quizás el patrón ya existe?")
            else:
                st.warning("Debes proporcionar al menos un patrón de texto o uno o más importes exactos.")

def mostrar_sincronizacion():
    st.title("🔄 Sincronización")
    st.markdown("Sincroniza tu base de datos entre diferentes dispositivos (Mac ↔ Cloud)")

    st.markdown("---")

    # Tabs para exportar e importar
    tab_export, tab_import, tab_comparar = st.tabs(["📤 Exportar", "📥 Importar", "🔍 Comparar"])

    with tab_export:
        st.subheader("Exportar Base de Datos")
        st.info("Descarga tu base de datos completa en formato JSON para importarla en otro dispositivo.")

        # Mostrar estadísticas
        transacciones = db_manager.obtener_transacciones()
        col1, col2 = st.columns(2)
        col1.metric("Total de Transacciones", len(transacciones))

        if transacciones:
            importes_totales = sum(t['importe'] for t in transacciones)
            col2.metric("Balance Total", f"{importes_totales:.2f} €")

        st.markdown("---")

        # Detectar si estamos en local (Mac de Daniel) para ofrecer guardado directo
        import os
        RUTA_ICLOUD_BACKUPS = '/Users/daniel/Desktop/DANIEL/GASTOS/Histórico backups'
        es_local = os.path.exists(RUTA_ICLOUD_BACKUPS)

        if es_local:
            st.info("🏠 **Modo Local Detectado** - Puedes guardar directamente en tu carpeta de iCloud")

        # Inicializar session_state para mantener el JSON generado
        if 'json_exportacion' not in st.session_state:
            st.session_state.json_exportacion = None
            st.session_state.filename_exportacion = None

        if st.button("📥 Generar Archivo de Exportación", type="primary"):
            with st.spinner("Generando archivo..."):
                json_export = sync.generar_json_exportacion()
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"finanzas_export_{timestamp}.json"

                # Guardar en session_state para mantenerlo entre reruns
                st.session_state.json_exportacion = json_export
                st.session_state.filename_exportacion = filename

                # Contar transacciones del JSON
                import json as json_module
                data = json_module.loads(json_export)
                num_transacciones = len(data.get('transacciones', []))

                st.success(f"✅ Archivo generado: {num_transacciones} transacciones")
                st.info("👇 Ahora puedes guardar o descargar el archivo usando los botones de abajo")

        # Mostrar botones de guardado/descarga si hay un archivo generado
        if st.session_state.json_exportacion:
            st.markdown("---")

            # Opción 1: Guardado directo en local (solo si está en Mac de Daniel)
            if es_local:
                col_save1, col_save2 = st.columns(2)

                with col_save1:
                    if st.button("💾 Guardar en iCloud Desktop", use_container_width=True, type="primary"):
                        try:
                            ruta_completa = os.path.join(RUTA_ICLOUD_BACKUPS, st.session_state.filename_exportacion)
                            with open(ruta_completa, 'w', encoding='utf-8') as f:
                                f.write(st.session_state.json_exportacion)
                            st.success(f"✅ Guardado exitosamente en:")
                            st.code(ruta_completa, language=None)
                            st.info(f"📱 Accesible desde iPhone en:\niCloud Drive/Desktop/DANIEL/GASTOS/Histórico backups/{st.session_state.filename_exportacion}")
                        except Exception as e:
                            st.error(f"❌ Error al guardar: {e}")
                            import traceback
                            st.code(traceback.format_exc(), language=None)

                with col_save2:
                    st.download_button(
                        label="⬇️ O Descargar (navegador)",
                        data=st.session_state.json_exportacion,
                        file_name=st.session_state.filename_exportacion,
                        mime="application/json",
                        use_container_width=True
                    )
            else:
                # Opción 2: Solo descarga normal (cuando está en Streamlit Cloud)
                st.download_button(
                    label="⬇️ Descargar Archivo JSON",
                    data=st.session_state.json_exportacion,
                    file_name=st.session_state.filename_exportacion,
                    mime="application/json"
                )

            # Botón para limpiar y generar uno nuevo
            if st.button("🔄 Generar Nuevo Archivo", type="secondary"):
                st.session_state.json_exportacion = None
                st.session_state.filename_exportacion = None
                st.rerun()

    with tab_import:
        st.subheader("Importar Base de Datos")
        st.info("Sube un archivo JSON exportado desde otro dispositivo para sincronizar datos.")

        uploaded_file = st.file_uploader(
            "Selecciona archivo JSON de exportación",
            type=['json'],
            key="sync_upload"
        )

        if uploaded_file is not None:
            try:
                # Leer y parsear el JSON
                json_string = uploaded_file.read().decode('utf-8')
                data_importar = sync.parsear_json_importacion(json_string)

                # Mostrar preview
                st.success("✅ Archivo válido cargado")

                metadata = data_importar.get("metadata", {})
                transacciones_importar = data_importar.get("transacciones", [])

                st.write(f"**Exportado en:** {metadata.get('exported_at', 'N/A')}")
                st.write(f"**Total transacciones:** {len(transacciones_importar)}")

                # Comparar con DB actual
                comparacion = sync.comparar_bases_datos(data_importar)

                st.markdown("### 📊 Análisis de Diferencias")

                col1, col2, col3 = st.columns(3)
                col1.metric("En este dispositivo", comparacion['total_local'])
                col2.metric("En el archivo", comparacion['total_remota'])
                col3.metric("En ambos", comparacion['en_ambas'])

                st.markdown("---")

                # Mostrar transacciones nuevas
                if comparacion['solo_en_remota']['count'] > 0:
                    st.success(f"✨ **{comparacion['solo_en_remota']['count']} transacciones nuevas** encontradas en el archivo")

                    with st.expander("Ver transacciones nuevas"):
                        df_nuevas = pd.DataFrame(comparacion['solo_en_remota']['transacciones'])
                        st.dataframe(df_nuevas[['fecha', 'concepto', 'importe', 'categoria']], use_container_width=True)
                else:
                    st.info("No hay transacciones nuevas en el archivo")

                if comparacion['solo_en_local']['count'] > 0:
                    st.warning(f"⚠️ **{comparacion['solo_en_local']['count']} transacciones** existen aquí pero no en el archivo")

                st.markdown("---")

                # Modo de importación
                modo_import = st.radio(
                    "Modo de importación:",
                    ["Fusionar (Añadir solo nuevas)", "Sobrescribir (Reemplazar todo)"],
                    help="Fusionar: Añade solo transacciones nuevas. Sobrescribir: Elimina todo y reemplaza (NO DISPONIBLE por seguridad)"
                )

                modo = "fusionar" if "Fusionar" in modo_import else "sobrescribir"

                if modo == "sobrescribir":
                    st.error("⚠️ Modo sobrescribir desactivado por seguridad. Usa 'Fusionar'.")
                else:
                    if st.button("🔄 Importar y Fusionar", type="primary", disabled=(comparacion['solo_en_remota']['count'] == 0)):
                        with st.spinner("Importando transacciones..."):
                            stats = sync.importar_base_datos(data_importar, modo=modo)

                        st.success("✅ Importación completada")

                        # Estadísticas de transacciones
                        st.markdown("### 📋 Transacciones")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Nuevas", stats['nuevas'], delta=f"+{stats['nuevas']}")
                        col2.metric("Duplicadas (omitidas)", stats['duplicadas'])
                        col3.metric("Errores", stats['errores'], delta_color="inverse")

                        # Estadísticas de recargas (si las hay)
                        if 'total_recargas' in stats and stats['total_recargas'] > 0:
                            st.markdown("### 🔌 Recargas de Coche")
                            col4, col5, col6 = st.columns(3)
                            col4.metric("Nuevas recargas", stats.get('nuevas_recargas', 0), delta=f"+{stats.get('nuevas_recargas', 0)}")
                            col5.metric("Duplicadas", stats.get('duplicadas_recargas', 0))
                            col6.metric("Errores", stats.get('errores_recargas', 0), delta_color="inverse")

                        if stats['nuevas'] > 0 or stats.get('nuevas_recargas', 0) > 0:
                            st.balloons()

                        st.info("💡 Refresca la página para ver los datos actualizados")

            except Exception:
                # logger.error(f"Error al procesar archivo de sincronización")
                st.error("❌ No se pudo procesar el archivo. Asegúrate de que es un archivo JSON válido exportado desde esta aplicación.")

    with tab_comparar:
        st.subheader("Comparar con Archivo")
        st.info("Compara tu base de datos actual con un archivo exportado sin importar nada.")

        uploaded_file_compare = st.file_uploader(
            "Selecciona archivo JSON para comparar",
            type=['json'],
            key="sync_compare"
        )

        if uploaded_file_compare is not None:
            try:
                json_string = uploaded_file_compare.read().decode('utf-8')
                data_comparar = sync.parsear_json_importacion(json_string)

                comparacion = sync.comparar_bases_datos(data_comparar)

                st.markdown("### 📊 Resultados de la Comparación")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Total en este dispositivo", comparacion['total_local'])
                    st.metric("Solo en este dispositivo", comparacion['solo_en_local']['count'])

                    if comparacion['solo_en_local']['count'] > 0:
                        with st.expander(f"Ver {comparacion['solo_en_local']['count']} transacciones"):
                            df = pd.DataFrame(comparacion['solo_en_local']['transacciones'])
                            st.dataframe(df[['fecha', 'concepto', 'importe']], use_container_width=True)

                with col2:
                    st.metric("Total en el archivo", comparacion['total_remota'])
                    st.metric("Solo en el archivo", comparacion['solo_en_remota']['count'])

                    if comparacion['solo_en_remota']['count'] > 0:
                        with st.expander(f"Ver {comparacion['solo_en_remota']['count']} transacciones"):
                            df = pd.DataFrame(comparacion['solo_en_remota']['transacciones'])
                            st.dataframe(df[['fecha', 'concepto', 'importe']], use_container_width=True)

                st.metric("En ambos (sincronizadas)", comparacion['en_ambas'])

                # Recomendación
                if comparacion['solo_en_remota']['count'] > 0 and comparacion['solo_en_local']['count'] > 0:
                    st.warning("⚠️ Ambos dispositivos tienen transacciones únicas. Considera importar en ambas direcciones.")
                elif comparacion['solo_en_remota']['count'] > 0:
                    st.info("💡 El archivo tiene transacciones nuevas. Ve a la pestaña 'Importar' para sincronizar.")
                elif comparacion['solo_en_local']['count'] > 0:
                    st.info("💡 Este dispositivo tiene transacciones nuevas. Ve a 'Exportar' para compartirlas.")
                else:
                    st.success("✅ Ambas bases de datos están completamente sincronizadas")

            except Exception:
                # logger.error(f"Error al comparar archivos")
                st.error("❌ No se pudo comparar el archivo. Verifica que sea un JSON válido exportado desde esta aplicación.")

def mostrar_configuracion():
    st.title("⚙️ Configuración")

    # ========== SECCIÓN: SALDO INICIAL ==========
    st.subheader("💰 Saldo Inicial")
    st.info("El saldo inicial se suma a todas las transacciones para calcular el líquido disponible total. "
            "Úsalo para establecer el saldo de tu cuenta al comenzar a usar la app.")

    config_actual = config_manager.obtener_config()

    with st.form("form_saldo_inicial"):
        col1, col2 = st.columns(2)

        with col1:
            saldo_inicial = st.number_input(
                "Saldo inicial (€)",
                value=config_actual.get('saldo_inicial', 0.0),
                step=0.01,
                format="%.2f",
                help="Saldo de tu cuenta al comenzar a usar la aplicación"
            )

            fecha_inicial = st.date_input(
                "Fecha del saldo inicial",
                value=datetime.datetime.strptime(config_actual.get('fecha_saldo_inicial', '2025-01-01'), '%Y-%m-%d').date()
                      if config_actual.get('fecha_saldo_inicial') else datetime.date.today(),
                help="Fecha a la que corresponde este saldo"
            )

        with col2:
            notas_inicial = st.text_area(
                "Notas (opcional)",
                value=config_actual.get('notas', ''),
                height=100,
                help="Información adicional sobre este saldo inicial"
            )

            st.metric(
                "💧 Líquido Disponible Actual",
                f"{metrics.calcular_liquido_disponible():.2f} €",
                help="Saldo inicial + suma de todas las transacciones"
            )

        submitted = st.form_submit_button("💾 Guardar Saldo Inicial", type="primary", use_container_width=True)

        if submitted:
            if config_manager.actualizar_saldo_inicial(saldo_inicial, fecha_inicial, notas_inicial):
                st.success(f"✅ Saldo inicial actualizado: {saldo_inicial:.2f} €")
                st.rerun()
            else:
                st.error("❌ Error al guardar el saldo inicial")

    st.markdown("---")

    # ========== SECCIÓN: PRESUPUESTOS MENSUALES ==========
    st.subheader("📊 Presupuestos Mensuales por Categoría")
    st.info("Define límites mensuales de gasto por categoría para controlar mejor tus finanzas. "
            "Los presupuestos se reflejarán en el dashboard para ver tu progreso en tiempo real.")

    # Mostrar presupuestos actuales
    presupuestos_actuales = db_manager.obtener_presupuestos()

    if presupuestos_actuales:
        st.markdown("#### 📋 Presupuestos Configurados")

        # Crear DataFrame para mostrar
        df_presupuestos = pd.DataFrame(presupuestos_actuales)
        df_presupuestos = df_presupuestos[['categoria', 'limite_mensual']]
        df_presupuestos.columns = ['Categoría', 'Límite Mensual (€)']

        # Mostrar tabla editable con opción de eliminar
        for idx, presupuesto in enumerate(presupuestos_actuales):
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.text(presupuesto['categoria'])

            with col2:
                st.text(f"{presupuesto['limite_mensual']:.2f} €")

            with col3:
                if st.button("🗑️", key=f"del_presupuesto_{idx}", help="Eliminar presupuesto"):
                    if db_manager.eliminar_presupuesto(presupuesto['categoria']):
                        st.success(f"Presupuesto de {presupuesto['categoria']} eliminado")
                        st.rerun()
                    else:
                        st.error("Error al eliminar presupuesto")

        st.markdown("---")

    # Formulario para añadir/actualizar presupuesto
    st.markdown("#### ➕ Añadir/Actualizar Presupuesto")

    col1, col2 = st.columns(2)

    with col1:
        # Obtener categorías disponibles
        categorias_disponibles = ["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "COCHE_ELECTRICO"]
        categoria_presupuesto = st.selectbox(
            "Categoría",
            categorias_disponibles,
            key="presupuesto_categoria",
            help="Selecciona la categoría para la que quieres establecer un presupuesto"
        )

    with col2:
        limite_mensual = st.number_input(
            "Límite Mensual (€)",
            min_value=0.01,
            value=100.00,
            step=10.00,
            format="%.2f",
            key="presupuesto_limite",
            help="Cantidad máxima que quieres gastar en esta categoría cada mes"
        )

    if st.button("💾 Guardar Presupuesto", type="primary", use_container_width=True, key="btn_guardar_presupuesto"):
        try:
            resultado = db_manager.crear_presupuesto(categoria_presupuesto, limite_mensual)
            if resultado:
                st.success(f"✅ Presupuesto para {categoria_presupuesto} guardado: {limite_mensual:.2f} €/mes")
                st.rerun()
            else:
                st.error("❌ Error al guardar el presupuesto - crear_presupuesto devolvió False")
        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

    st.markdown("---")

    # ========== SECCIÓN: BASE DE DATOS ==========
    st.subheader("🗄️ Gestión de Base de Datos")

    col_info, col_reset = st.columns([2, 1])

    with col_info:
        st.warning(
            "⚠️ **Resetear la base de datos eliminará todas las transacciones**, "
            "pero el saldo inicial se mantendrá guardado y podrás restaurarlo después.",
            icon="⚠️"
        )

    with col_reset:
        if st.button("⚠️ Resetear Base de Datos", type="secondary", use_container_width=True):
            confirmacion = st.warning(
                "¿Estás seguro de que quieres resetear la base de datos? ¡Esta acción borrará todos los datos!",
                icon="⚠️"
            )
            if confirmacion:
                with st.spinner("Reseteando la base de datos..."):
                    db_manager.resetear_base_de_datos()
                st.success("¡Base de datos reseteada con éxito!")
                st.info(f"💡 Tu saldo inicial de {config_actual.get('saldo_inicial', 0):.2f} € se mantiene guardado en la configuración.")
                st.rerun()

# --- Importar módulo de Coche Eléctrico ---
import pages_coche_electrico

# --- Routing principal ---
if pagina_seleccionada == "Dashboard":
    mostrar_dashboard()
elif pagina_seleccionada == "Añadir Gasto":
    mostrar_añadir_gasto()
elif pagina_seleccionada == "Transacciones":
    mostrar_transacciones()
elif pagina_seleccionada == "Importar":
    mostrar_importar()
elif pagina_seleccionada == "Categorías":
    mostrar_categorias()
elif pagina_seleccionada == "🔌 Coche Eléctrico":
    pages_coche_electrico.mostrar_coche_electrico()
elif pagina_seleccionada == "Sincronización":
    mostrar_sincronizacion()
elif pagina_seleccionada == "Configuración":
    mostrar_configuracion()