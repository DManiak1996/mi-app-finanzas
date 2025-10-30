# auth.py - Sistema de autenticación para la app

import streamlit as st

def check_authentication():
    """
    Sistema de autenticación simple con Google.
    Usa Streamlit secrets para almacenar emails autorizados.
    """

    # Verificar si ya está autenticado
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        return True

    # Obtener email autorizado de secrets
    try:
        authorized_email = st.secrets["auth"]["authorized_email"]
    except Exception:
        # Si no hay secrets configurados, mostrar instrucciones
        st.error("⚠️ Configuración de autenticación pendiente")
        st.info("""
        Para configurar la autenticación:
        1. Ve a Streamlit Cloud
        2. Settings > Secrets
        3. Añade:
        ```
        [auth]
        authorized_email = "tu-email@gmail.com"
        ```
        """)
        st.stop()

    # Página de login
    st.title("🔐 Mi App de Finanzas")
    st.markdown("---")

    # Usar el authenticator de Streamlit (simple)
    st.markdown("### Acceso Privado")
    st.info("Esta aplicación requiere autenticación.")

    # Input de email simple
    email_input = st.text_input("Introduce tu email:", key="email_input")
    password_input = st.text_input("Introduce la contraseña:", type="password", key="password_input")

    if st.button("🔑 Acceder"):
        # Verificar email y password
        try:
            correct_password = st.secrets["auth"]["password"]
        except Exception:
            correct_password = "finanzas2024"  # Default para desarrollo local

        if email_input == authorized_email and password_input == correct_password:
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = email_input
            st.success("✅ Acceso concedido")
            st.rerun()
        else:
            st.error("❌ Email o contraseña incorrectos")

    st.markdown("---")
    st.caption("🔒 Aplicación protegida con autenticación")

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
