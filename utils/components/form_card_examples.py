"""
Ejemplos de uso del componente FormCard

Este archivo contiene ejemplos prácticos de cómo usar el componente FormCard
en diferentes escenarios de la aplicación.
"""

import streamlit as st
import datetime
from .form_card import (
    render_form_card,
    form_section,
    form_field_group,
    form_actions,
    show_form_feedback,
    validate_required_fields,
    show_validation_error,
)


# ============================================================================
# EJEMPLO 1: Formulario básico de nueva transacción
# ============================================================================

def ejemplo_nueva_transaccion():
    """
    Ejemplo de formulario para añadir una nueva transacción
    con validación y feedback
    """

    def contenido_formulario():
        # Sección de datos básicos
        form_section("Datos de la Transacción", "Información básica del movimiento")

        col1, col2 = st.columns(2)

        with col1:
            form_field_group("Fecha", help_text="Fecha del movimiento", required=True)
            fecha = st.date_input(
                "",
                value=datetime.date.today(),
                key="fecha_transaccion",
                label_visibility="collapsed",
            )

            form_field_group("Concepto", help_text="Descripción del movimiento", required=True)
            concepto = st.text_input(
                "",
                key="concepto_transaccion",
                placeholder="Ej: Compra supermercado",
                label_visibility="collapsed",
            )

        with col2:
            form_field_group("Importe (€)", help_text="Cantidad en euros", required=True)
            importe = st.number_input(
                "",
                min_value=0.01,
                step=0.01,
                format="%.2f",
                key="importe_transaccion",
                label_visibility="collapsed",
            )

            form_field_group("Categoría", required=True)
            categoria = st.selectbox(
                "",
                options=["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "INGRESO"],
                key="categoria_transaccion",
                label_visibility="collapsed",
            )

        # Sección de detalles adicionales
        form_section("Detalles Adicionales", "Información complementaria (opcional)")

        form_field_group("Notas", help_text="Comentarios o anotaciones adicionales")
        notas = st.text_area(
            "",
            key="notas_transaccion",
            placeholder="Añade cualquier detalle relevante...",
            height=100,
            label_visibility="collapsed",
        )

    def botones_formulario():
        form_actions(
            primary_btn={"label": "💾 Guardar Transacción", "key": "guardar_transaccion"},
            secondary_btn={"label": "🔄 Limpiar", "key": "limpiar_transaccion"},
        )

    # Renderizar el formulario
    with st.form("form_nueva_transaccion"):
        render_form_card(
            title="Nueva Transacción",
            content_fn=contenido_formulario,
            footer=botones_formulario,
            icon="💸",
            description="Registra un nuevo movimiento en tu cuenta",
        )


# ============================================================================
# EJEMPLO 2: Formulario con validación en tiempo real
# ============================================================================

def ejemplo_formulario_validacion():
    """
    Ejemplo de formulario con validación de campos y mensajes de error
    """

    def contenido_formulario():
        form_field_group("Nombre de usuario", required=True)
        username = st.text_input(
            "",
            key="username",
            placeholder="Ej: john_doe",
            label_visibility="collapsed",
        )

        # Validación inline
        if username and len(username) < 3:
            show_validation_error("Nombre de usuario", "Debe tener al menos 3 caracteres")

        form_field_group("Email", help_text="Tu dirección de correo electrónico", required=True)
        email = st.text_input(
            "",
            key="email",
            placeholder="ejemplo@correo.com",
            label_visibility="collapsed",
        )

        # Validación de email
        if email and "@" not in email:
            show_validation_error("Email", "El email debe contener @")

        form_field_group("Contraseña", required=True)
        password = st.text_input(
            "",
            type="password",
            key="password",
            label_visibility="collapsed",
        )

        if password and len(password) < 8:
            show_validation_error("Contraseña", "Debe tener al menos 8 caracteres")

    def botones():
        clicked = form_actions(
            primary_btn={"label": "Registrarse", "key": "submit_registro"},
        )

    with st.form("form_registro"):
        render_form_card(
            title="Crear Cuenta",
            content_fn=contenido_formulario,
            footer=botones,
            icon="👤",
        )


# ============================================================================
# EJEMPLO 3: Formulario con estados (loading, success, error)
# ============================================================================

def ejemplo_formulario_estados():
    """
    Ejemplo de formulario que muestra diferentes estados visuales
    """
    # Estado del formulario (normalmente estaría en session_state)
    if "form_state" not in st.session_state:
        st.session_state.form_state = "default"

    def contenido_formulario():
        # Mostrar feedback según el estado
        if st.session_state.form_state == "success":
            show_form_feedback("¡Regla guardada correctamente!", type="success")
        elif st.session_state.form_state == "error":
            show_form_feedback("Error al guardar la regla. Intenta de nuevo.", type="error")
        elif st.session_state.form_state == "loading":
            show_form_feedback("Guardando regla...", type="info", icon="⏳")

        form_field_group("Patrón de texto", required=True)
        patron = st.text_input(
            "",
            key="patron",
            placeholder="NETFLIX|HBO|SPOTIFY",
            label_visibility="collapsed",
        )

        col1, col2 = st.columns(2)

        with col1:
            form_field_group("Categoría", required=True)
            categoria = st.selectbox(
                "",
                options=["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "INGRESO"],
                key="categoria_regla",
                label_visibility="collapsed",
            )

        with col2:
            form_field_group("Tipo", required=True)
            tipo = st.selectbox(
                "",
                options=["GASTO", "INGRESO"],
                key="tipo_regla",
                label_visibility="collapsed",
            )

    def botones():
        form_actions(
            primary_btn={"label": "✨ Añadir Regla", "key": "guardar_regla"},
            danger_btn={"label": "🗑️ Eliminar", "key": "eliminar_regla"},
        )

    # Renderizar con estado
    with st.form("form_regla"):
        render_form_card(
            title="Nueva Regla de Clasificación",
            content_fn=contenido_formulario,
            footer=botones,
            icon="🏷️",
            state=st.session_state.form_state,  # 'default', 'loading', 'success', 'error'
            description="Define un patrón para clasificar transacciones automáticamente",
        )


# ============================================================================
# EJEMPLO 4: Formulario complejo con múltiples secciones
# ============================================================================

def ejemplo_formulario_complejo():
    """
    Ejemplo de formulario largo con múltiples secciones organizadas
    """

    def contenido_formulario():
        # Sección 1: Información Personal
        form_section(
            "Información Personal",
            "Datos básicos de identificación"
        )

        col1, col2 = st.columns(2)

        with col1:
            form_field_group("Nombre", required=True)
            nombre = st.text_input("", key="nombre", label_visibility="collapsed")

            form_field_group("Apellidos", required=True)
            apellidos = st.text_input("", key="apellidos", label_visibility="collapsed")

        with col2:
            form_field_group("DNI/NIE", required=True)
            dni = st.text_input("", key="dni", label_visibility="collapsed")

            form_field_group("Fecha de Nacimiento", required=True)
            fecha_nac = st.date_input("", key="fecha_nac", label_visibility="collapsed")

        # Sección 2: Datos de Contacto
        form_section(
            "Datos de Contacto",
            "Información para comunicarnos contigo"
        )

        col1, col2 = st.columns(2)

        with col1:
            form_field_group("Email", help_text="Tu correo electrónico principal", required=True)
            email = st.text_input("", key="email_contacto", label_visibility="collapsed")

        with col2:
            form_field_group("Teléfono", help_text="Número de contacto", required=True)
            telefono = st.text_input("", key="telefono", label_visibility="collapsed")

        form_field_group("Dirección", required=True)
        direccion = st.text_input("", key="direccion", label_visibility="collapsed")

        col1, col2, col3 = st.columns(3)

        with col1:
            form_field_group("Código Postal", required=True)
            cp = st.text_input("", key="cp", label_visibility="collapsed")

        with col2:
            form_field_group("Ciudad", required=True)
            ciudad = st.text_input("", key="ciudad", label_visibility="collapsed")

        with col3:
            form_field_group("Provincia", required=True)
            provincia = st.text_input("", key="provincia", label_visibility="collapsed")

        # Sección 3: Configuración de Cuenta
        form_section(
            "Configuración de Cuenta",
            "Preferencias y ajustes iniciales"
        )

        form_field_group("Saldo Inicial (€)", help_text="Saldo de tu cuenta al registrarte")
        saldo_inicial = st.number_input(
            "",
            min_value=0.0,
            step=0.01,
            format="%.2f",
            key="saldo_inicial",
            label_visibility="collapsed",
        )

        form_field_group("Recibir notificaciones por email")
        notificaciones = st.checkbox(
            "Sí, quiero recibir notificaciones",
            key="notificaciones",
        )

    def botones():
        clicked = form_actions(
            primary_btn={"label": "💾 Guardar Perfil", "key": "guardar_perfil"},
            secondary_btn={"label": "↩️ Volver", "key": "volver"},
            align="right",
        )

    with st.form("form_perfil"):
        render_form_card(
            title="Configuración de Perfil",
            content_fn=contenido_formulario,
            footer=botones,
            icon="⚙️",
            description="Completa tu perfil para empezar a usar la aplicación",
        )


# ============================================================================
# EJEMPLO 5: Validación completa de formulario
# ============================================================================

def ejemplo_validacion_completa():
    """
    Ejemplo completo de validación de formulario con todos los helpers
    """

    def contenido_formulario():
        # Estado de validación
        if "validation_errors" not in st.session_state:
            st.session_state.validation_errors = []

        # Mostrar errores generales
        if st.session_state.validation_errors:
            show_form_feedback(
                f"Se encontraron {len(st.session_state.validation_errors)} errores. Revisa los campos marcados.",
                type="error"
            )

        form_field_group("Concepto del Gasto", required=True)
        concepto = st.text_input(
            "",
            key="concepto_validacion",
            label_visibility="collapsed",
        )

        form_field_group("Importe (€)", required=True)
        importe = st.number_input(
            "",
            min_value=0.0,
            step=0.01,
            key="importe_validacion",
            label_visibility="collapsed",
        )

        form_field_group("Categoría", required=True)
        categoria = st.selectbox(
            "",
            options=["Seleccionar...", "FIJOS", "DISFRUTE", "EXTRAORDINARIOS"],
            key="categoria_validacion",
            label_visibility="collapsed",
        )

    def botones():
        submitted = form_actions(
            primary_btn={"label": "Validar y Guardar", "key": "submit_validacion"},
        )

        # Procesar validación al enviar
        if submitted:
            # Obtener valores del formulario
            fields = {
                "Concepto": st.session_state.get("concepto_validacion", ""),
                "Importe": st.session_state.get("importe_validacion", 0.0),
            }

            # Validar
            is_valid, errors = validate_required_fields(fields)

            # Validar categoría
            if st.session_state.get("categoria_validacion") == "Seleccionar...":
                errors.append("Debes seleccionar una categoría")
                is_valid = False

            if is_valid:
                st.session_state.validation_errors = []
                show_form_feedback("¡Formulario validado correctamente! Guardando...", type="success")
                # Aquí iría la lógica para guardar
            else:
                st.session_state.validation_errors = errors
                for error in errors:
                    st.error(error)

    with st.form("form_validacion"):
        render_form_card(
            title="Formulario con Validación",
            content_fn=contenido_formulario,
            footer=botones,
            icon="✅",
            description="Todos los campos son obligatorios",
        )


# ============================================================================
# FUNCIÓN PRINCIPAL PARA DEMO
# ============================================================================

def demo_form_card():
    """
    Función principal para mostrar todos los ejemplos
    """
    st.title("FormCard Component - Ejemplos de Uso")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Básico",
        "Validación",
        "Estados",
        "Complejo",
        "Validación Completa"
    ])

    with tab1:
        st.header("Ejemplo 1: Formulario Básico")
        ejemplo_nueva_transaccion()

    with tab2:
        st.header("Ejemplo 2: Validación en Tiempo Real")
        ejemplo_formulario_validacion()

    with tab3:
        st.header("Ejemplo 3: Estados del Formulario")
        ejemplo_formulario_estados()

        # Controles para cambiar el estado (demo)
        st.markdown("---")
        st.subheader("Controles de Demo")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Default"):
                st.session_state.form_state = "default"
        with col2:
            if st.button("Loading"):
                st.session_state.form_state = "loading"
        with col3:
            if st.button("Success"):
                st.session_state.form_state = "success"
        with col4:
            if st.button("Error"):
                st.session_state.form_state = "error"

    with tab4:
        st.header("Ejemplo 4: Formulario Complejo")
        ejemplo_formulario_complejo()

    with tab5:
        st.header("Ejemplo 5: Validación Completa")
        ejemplo_validacion_completa()


if __name__ == "__main__":
    demo_form_card()
