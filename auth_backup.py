# auth.py - Sistema de autenticación con cookies persistentes

import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import hashlib
import secrets
import time
from datetime import datetime, timedelta

# Inicializar cookie manager
def get_cookie_manager():
    """Obtiene el gestor de cookies encriptadas (se inicializa una vez por sesión)"""
    if 'cookies' not in st.session_state:
        st.session_state.cookies = EncryptedCookieManager(
            prefix="finanzas_app_",
            password=st.secrets.get("auth", {}).get("cookie_password", "default_secret_key_change_in_production")
        )
    return st.session_state.cookies

def generate_auth_token(email):
    """Genera un token único de autenticación"""
    timestamp = str(time.time())
    random_salt = secrets.token_hex(16)
    token_data = f"{email}:{timestamp}:{random_salt}"
    return hashlib.sha256(token_data.encode()).hexdigest()

def verify_token(token, email):
    """Verifica si un token es válido (simplificado - en producción usar BD)"""
    # Por ahora solo verificamos que exista
    # En una implementación real, guardarías tokens en BD con expiración
    return token and len(token) == 64  # SHA256 produce 64 caracteres hex

def check_authentication():
    """
    Sistema de autenticación con cookies persistentes.
    - Verifica token en cookies primero
    - Si no hay token válido, muestra login compacto
    - Al hacer login exitoso, guarda token en cookies (30 días)
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

        cookie_password = "clave-secreta-para-encriptar-cookies"
        ```
        """)
        st.stop()

    # 1. Verificar si ya está autenticado en session_state
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        return True

    # Obtener cookie manager
    cookies = get_cookie_manager()

    # Esperar a que las cookies estén listas
    if not cookies.ready():
        st.warning("🔄 Inicializando...")
        st.stop()

    # 2. Verificar si hay un token válido en cookies
    saved_token = cookies.get('auth_token')
    saved_email = cookies.get('user_email')

    if saved_token and saved_email == authorized_email:
        if verify_token(saved_token, saved_email):
            # Token válido - auto-login
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = saved_email
            st.session_state["login_time"] = time.time()
            st.session_state["auto_login"] = True
            return True

    # 3. Mostrar login compacto y elegante
    show_compact_login(authorized_email, correct_password, cookies)

    return False

def show_compact_login(authorized_email, correct_password, cookies):
    """Muestra un formulario de login compacto y centrado"""

    # CSS personalizado para el login
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        margin-top: 5vh;
    }
    .login-title {
        color: white;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .login-subtitle {
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Espaciado superior
    st.markdown("<br>", unsafe_allow_html=True)

    # Contenedor centrado con columnas
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Card de login
        st.markdown('<div class="login-container">', unsafe_allow_html=True)

        st.markdown('<div class="login-title">💰 Finanzas</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Gestión Personal</div>', unsafe_allow_html=True)

        # Formulario
        with st.form("login_form", clear_on_submit=False):
            email_input = st.text_input(
                "📧 Email",
                placeholder="tu-email@gmail.com",
                key="email_input",
                label_visibility="collapsed"
            )

            password_input = st.text_input(
                "🔒 Contraseña",
                type="password",
                placeholder="Tu contraseña",
                key="password_input",
                label_visibility="collapsed"
            )

            remember_me = st.checkbox(
                "🔐 Recordar en este dispositivo (30 días)",
                value=True,
                help="Mantiene tu sesión activa durante 30 días en este navegador"
            )

            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                submit_button = st.form_submit_button(
                    "🚀 Entrar",
                    use_container_width=True,
                    type="primary"
                )

            if submit_button:
                # Verificar credenciales
                if email_input == authorized_email and password_input == correct_password:
                    # Login exitoso
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email_input
                    st.session_state["login_time"] = time.time()

                    # Guardar token en cookies si "recordar" está activado
                    if remember_me:
                        auth_token = generate_auth_token(email_input)
                        cookies['auth_token'] = auth_token
                        cookies['user_email'] = email_input
                        # Expiración: 30 días
                        expires = datetime.now() + timedelta(days=30)
                        cookies['token_expires'] = expires.isoformat()
                        cookies.save()

                    st.success("✅ ¡Bienvenido!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
                    time.sleep(1.5)

        st.markdown('</div>', unsafe_allow_html=True)

        # Información adicional
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center; color: #888; font-size: 0.85rem;'>🔒 Acceso seguro y privado</p>",
            unsafe_allow_html=True
        )

def show_user_info():
    """Muestra información del usuario autenticado en el sidebar"""
    if "user_email" in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"👤 **{st.session_state['user_email'].split('@')[0].title()}**")

        # Mostrar si fue auto-login
        if st.session_state.get("auto_login"):
            st.sidebar.caption("🔐 Sesión recordada")

        if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
            # Limpiar session state
            st.session_state["authenticated"] = False
            st.session_state.pop("user_email", None)
            st.session_state.pop("login_time", None)
            st.session_state.pop("auto_login", None)

            # Limpiar cookies
            cookies = get_cookie_manager()
            cookies['auth_token'] = ''
            cookies['user_email'] = ''
            cookies['token_expires'] = ''
            cookies.save()

            st.rerun()
