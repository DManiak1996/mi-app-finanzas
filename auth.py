# auth.py - Sistema de autenticación para la app

import streamlit as st
import hashlib
import time

def check_authentication():
    """
    Sistema de autenticación robusto con email y contraseña.
    Usa Streamlit secrets para almacenar credenciales.
    """

    # Verificar si ya está autenticado
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        return True

    # Obtener credenciales de secrets
    try:
        authorized_email = st.secrets["auth"]["authorized_email"]
        correct_password = st.secrets["auth"]["password"]
    except Exception:
        # Si no hay secrets configurados, mostrar instrucciones
        st.error("⚠️ Configuración de autenticación pendiente")
        st.info("""
        Para configurar la autenticación:
        1. Ve a Streamlit Cloud > Settings > Secrets
        2. Añade:
        ```toml
        [auth]
        authorized_email = "tu-email@gmail.com"
        password = "tu-contraseña-segura"
        ```
        3. Guarda y reinicia la app
        """)
        st.stop()

    # Página de login
    st.title("🔐 Mi App de Finanzas")
    st.markdown("---")

    st.markdown("### Acceso Privado")
    st.info("Esta aplicación es de uso personal. Introduce tus credenciales para acceder.")

    # Formulario de login
    with st.form("login_form"):
        email_input = st.text_input(
            "Email:",
            placeholder="tu-email@gmail.com",
            key="email_input"
        )
        password_input = st.text_input(
            "Contraseña:",
            type="password",
            placeholder="Tu contraseña",
            key="password_input"
        )

        submit_button = st.form_submit_button("🔑 Iniciar Sesión")

        if submit_button:
            # Verificar credenciales
            if email_input == authorized_email and password_input == correct_password:
                st.session_state["authenticated"] = True
                st.session_state["user_email"] = email_input
                st.session_state["login_time"] = time.time()
                st.success("✅ Acceso concedido. Redirigiendo...")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Email o contraseña incorrectos")
                time.sleep(1)

    st.markdown("---")
    st.caption("🔒 Aplicación protegida • Solo acceso autorizado")
    st.caption("💡 Tip: Guarda esta página en favoritos o añádela a tu pantalla de inicio")

    return False

def show_user_info():
    """Muestra información del usuario autenticado en el sidebar"""
    if "user_email" in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"👤 **Usuario:** {st.session_state['user_email']}")
        if st.sidebar.button("🚪 Cerrar Sesión"):
            st.session_state["authenticated"] = False
            st.session_state.pop("user_email", None)
            st.rerun()
