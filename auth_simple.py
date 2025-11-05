# auth_simple.py - Autenticación PREMIUM con branding FinanzasFlow

import streamlit as st
import time
from streamlit.components.v1 import html as render_html
from utils import brand_assets
from utils.design_tokens import Colors, Typography, Spacing, BorderRadius, Transitions

def check_authentication():
    """
    Sistema de autenticación simple solo con session_state.
    Con diseño PREMIUM FinanzasFlow.
    """

    # Obtener credenciales de secrets
    try:
        authorized_email = st.secrets["auth"]["authorized_email"]
        correct_password = st.secrets["auth"]["password"]
    except Exception:
        st.error("⚠️ Configuración de autenticación pendiente")
        st.info("""
        Para configurar la autenticación, añade en `.streamlit/secrets.toml`:
        ```toml
        [auth]
        authorized_email = "tu-email@gmail.com"
        password = "tu-contraseña"
        ```
        """)
        st.stop()

    # 1. Verificar si ya está autenticado en session_state
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        return True

    # 2. Mostrar login PREMIUM
    show_premium_login(authorized_email, correct_password)

    return False

def show_premium_login(authorized_email, correct_password):
    """Formulario de login PREMIUM con branding FinanzasFlow"""

    # === CSS PREMIUM PARA LOGIN ===
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Fondo con gradiente premium */
    .stApp {{
        background: {Colors.PREMIUM_BG_GRADIENT} !important;
    }}

    /* Tipografía premium */
    html, body, [class*="css"] {{
        font-family: {Typography.FONT_PRIMARY} !important;
    }}

    /* Input fields premium */
    .stTextInput input {{
        min-height: 52px !important;
        font-size: {Typography.TEXT_BASE} !important;
        border-radius: {BorderRadius.MD} !important;
        border: 2px solid rgba(102, 126, 234, 0.15) !important;
        background: white !important;
        padding: {Spacing.MD} {Spacing.LG} !important;
        transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
    }}

    .stTextInput input:focus {{
        border-color: {Colors.PREMIUM_PRIMARY_START} !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
        outline: none !important;
    }}

    /* Botón premium */
    .stButton button {{
        min-height: 52px !important;
        font-size: {Typography.TEXT_BASE} !important;
        font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
        border-radius: {BorderRadius.MD} !important;
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.05) !important;
        transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
        color: white !important;
    }}

    .stButton button:hover {{
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 10px 15px rgba(0,0,0,0.1), 0 0 20px rgba(102, 126, 234, 0.4) !important;
    }}

    .stButton button:active {{
        transform: translateY(0) scale(0.98) !important;
    }}

    /* Animación fadeIn */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .login-container {{
        animation: fadeInUp 0.8s {Transitions.EASING_DEFAULT};
    }}
    </style>
    """, unsafe_allow_html=True)

    # Espaciado superior
    st.markdown("<br>", unsafe_allow_html=True)

    # Centrar con columnas
    col1, col2, col3 = st.columns([1, 2.5, 1])

    with col2:
        # === LOGO PREMIUM CON COMPONENTE HTML (bypasea el sanitizer) ===
        st.markdown(f"""
<div class="login-container" style="background: {Colors.PREMIUM_CARD_GRADIENT}; padding: {Spacing.XXL}; border-radius: {BorderRadius.XL}; box-shadow: 0 20px 25px rgba(0,0,0,0.10), 0 10px 10px rgba(0,0,0,0.04); border: 1px solid rgba(102, 126, 234, 0.1); backdrop-filter: blur(10px); text-align: center;">
    <div id="logo-container" style="margin-bottom: {Spacing.XL}; display: flex; justify-content: center;"></div>
    <h1 style="font-size: {Typography.TEXT_4XL}; font-weight: {Typography.WEIGHT_EXTRABOLD}; margin-bottom: {Spacing.SM}; background: {Colors.PREMIUM_GRADIENT_PRIMARY}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        Bienvenido
    </h1>
    <p style="font-size: {Typography.TEXT_BASE}; color: {Colors.GRAY_600}; margin-bottom: {Spacing.XL}; font-weight: {Typography.WEIGHT_MEDIUM};">
        Accede a tu control financiero premium
    </p>
</div>
        """, unsafe_allow_html=True)

        # Renderizar SVG usando componente HTML (bypasea sanitizer)
        render_html(f"""
        <script>
        const logoContainer = window.parent.document.querySelector('#logo-container');
        if (logoContainer) {{
            logoContainer.innerHTML = `{brand_assets.LOGO_SVG}`;
        }}
        </script>
        """, height=0)

        st.markdown("<br>", unsafe_allow_html=True)

        # === INPUTS PREMIUM ===
        email_input = st.text_input(
            "📧 Email",
            placeholder="tu-email@ejemplo.com",
            label_visibility="collapsed",
            help="Introduce tu email autorizado"
        )

        password_input = st.text_input(
            "🔒 Contraseña",
            type="password",
            placeholder="Tu contraseña segura",
            label_visibility="collapsed",
            help="Introduce tu contraseña"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Botón de login
        if st.button("🚀 Acceder a FinanzasFlow", type="primary", use_container_width=True):
            if email_input == authorized_email and password_input == correct_password:
                # Animación de éxito
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(17, 153, 142, 0.1) 0%, rgba(56, 239, 125, 0.05) 100%);
                    padding: {Spacing.LG};
                    border-radius: {BorderRadius.MD};
                    border-left: 4px solid {Colors.PREMIUM_TEAL_START};
                    margin: {Spacing.LG} 0;
                    animation: fadeInUp 0.5s ease;
                ">
                    <div style="display: flex; align-items: center; gap: {Spacing.MD};">
                        {brand_assets.get_icon('success')}
                        <div>
                            <h3 style="margin: 0; color: {Colors.PREMIUM_TEAL_START}; font-size: {Typography.TEXT_LG};">
                                ✅ Acceso Concedido
                            </h3>
                            <p style="margin: 0; color: {Colors.GRAY_600}; font-size: {Typography.TEXT_SM};">
                                Bienvenido de vuelta, preparando tu dashboard...
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.session_state["authenticated"] = True
                st.session_state["user_email"] = email_input
                st.session_state["login_time"] = time.time()

                time.sleep(1.5)  # Mostrar animación
                st.rerun()
            else:
                # Animación de error
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.05) 100%);
                    padding: {Spacing.LG};
                    border-radius: {BorderRadius.MD};
                    border-left: 4px solid {Colors.PREMIUM_CORAL_START};
                    margin: {Spacing.LG} 0;
                    animation: fadeInUp 0.5s ease;
                ">
                    <div style="display: flex; align-items: center; gap: {Spacing.MD};">
                        <div>
                            <h3 style="margin: 0; color: {Colors.PREMIUM_CORAL_START}; font-size: {Typography.TEXT_LG};">
                                ❌ Credenciales Incorrectas
                            </h3>
                            <p style="margin: 0; color: {Colors.GRAY_600}; font-size: {Typography.TEXT_SM};">
                                Verifica tu email y contraseña e intenta nuevamente
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Footer premium
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; color: {Colors.GRAY_500}; font-size: {Typography.TEXT_SM};">
            <p style="margin: 0;">
                🔒 Conexión segura •
                <span style="background: {Colors.PREMIUM_GRADIENT_PRIMARY}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: {Typography.WEIGHT_SEMIBOLD};">
                    FinanzasFlow Premium
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)

def show_user_info():
    """Muestra información del usuario autenticado en el sidebar PREMIUM"""
    if "user_email" in st.session_state:
        st.sidebar.markdown("---")

        # Usuario con estilo premium
        username = st.session_state['user_email'].split('@')[0].title()

        st.sidebar.markdown(f"""
        <div style="
            background: {Colors.PREMIUM_CARD_GRADIENT};
            padding: {Spacing.LG};
            border-radius: {BorderRadius.MD};
            margin-bottom: {Spacing.LG};
            border: 1px solid rgba(102, 126, 234, 0.1);
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        ">
            <div style="display: flex; align-items: center; gap: {Spacing.MD};">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: {Colors.PREMIUM_GRADIENT_PRIMARY};
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: {Typography.WEIGHT_BOLD};
                    color: white;
                    font-size: {Typography.TEXT_LG};
                ">
                    {username[0]}
                </div>
                <div>
                    <div style="font-weight: {Typography.WEIGHT_SEMIBOLD}; color: {Colors.GRAY_900};">
                        {username}
                    </div>
                    <div style="font-size: {Typography.TEXT_XS}; color: {Colors.GRAY_600};">
                        Premium User
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Botón de cerrar sesión premium
        if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
            # Limpiar session state
            st.session_state["authenticated"] = False
            st.session_state.pop("user_email", None)
            st.session_state.pop("login_time", None)
            st.rerun()
