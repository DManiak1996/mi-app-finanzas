# auth_simple.py - Autenticación básica SIN cookies (temporal)

import streamlit as st
import time

def check_authentication():
    """
    Sistema de autenticación simple solo con session_state.
    Sin cookies persistentes.
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

    # 2. Mostrar login compacto
    show_compact_login(authorized_email, correct_password)

    return False

def show_compact_login(authorized_email, correct_password):
    """Formulario de login centrado en formato vertical"""

    # Espaciado superior
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Centrar con columnas
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("💰 Finanzas")
        st.subheader("Gestión Personal")

        st.markdown("---")

        # Formulario simple
        email_input = st.text_input("Email", placeholder="tu-email@gmail.com")
        password_input = st.text_input("Contraseña", type="password", placeholder="Tu contraseña")

        if st.button("Entrar", type="primary", use_container_width=True):
            if email_input == authorized_email and password_input == correct_password:
                st.session_state["authenticated"] = True
                st.session_state["user_email"] = email_input
                st.session_state["login_time"] = time.time()
                st.success("✅ Acceso concedido")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas")

def show_user_info():
    """Muestra información del usuario autenticado en el sidebar"""
    if "user_email" in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"👤 **{st.session_state['user_email'].split('@')[0].title()}**")

        if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
            # Limpiar session state
            st.session_state["authenticated"] = False
            st.session_state.pop("user_email", None)
            st.session_state.pop("login_time", None)

            st.rerun()
