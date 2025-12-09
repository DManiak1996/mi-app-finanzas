"""
Demo simple del componente FormCard

Ejecutar con:
    streamlit run utils/components/demo_form_card.py
"""

import streamlit as st
import datetime
from form_card import (
    render_form_card,
    form_section,
    form_field_group,
    form_actions,
    show_form_feedback,
    validate_required_fields,
    show_validation_error,
)

# Configuración de página
st.set_page_config(
    page_title="FormCard Demo",
    page_icon="📝",
    layout="wide"
)

st.title("FormCard Component - Demo")
st.markdown("Demostración del componente FormCard con todos sus features")

# Inicializar estado
if "demo_state" not in st.session_state:
    st.session_state.demo_state = "default"

st.markdown("---")

# ============================================================================
# DEMO 1: Formulario básico
# ============================================================================

st.header("1. Formulario Básico")

def formulario_basico():
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre", key="nombre_basico")

    with col2:
        email = st.text_input("Email", key="email_basico")

    mensaje = st.text_area("Mensaje", key="mensaje_basico")

def botones_basico():
    submitted = form_actions(
        primary_btn={"label": "Enviar", "key": "submit_basico"},
        secondary_btn={"label": "Cancelar", "key": "cancel_basico"},
    )

    if submitted:
        st.success("Formulario enviado correctamente")

with st.form("form_basico"):
    render_form_card(
        title="Contacto",
        content_fn=formulario_basico,
        footer=botones_basico,
        icon="📧",
        description="Envíanos un mensaje"
    )

st.markdown("---")

# ============================================================================
# DEMO 2: Formulario con validación
# ============================================================================

st.header("2. Formulario con Validación")

def formulario_validacion():
    form_field_group("Concepto", help_text="Descripción del gasto", required=True)
    concepto = st.text_input(
        "",
        key="concepto_val",
        placeholder="Ej: Compra supermercado",
        label_visibility="collapsed"
    )

    if concepto and len(concepto) < 3:
        show_validation_error("Concepto", "Debe tener al menos 3 caracteres")

    form_field_group("Importe (€)", required=True)
    importe = st.number_input(
        "",
        min_value=0.01,
        step=0.01,
        format="%.2f",
        key="importe_val",
        label_visibility="collapsed"
    )

    form_field_group("Categoría", required=True)
    categoria = st.selectbox(
        "",
        options=["FIJOS", "DISFRUTE", "EXTRAORDINARIOS"],
        key="categoria_val",
        label_visibility="collapsed"
    )

def botones_validacion():
    submitted = form_actions(
        primary_btn={"label": "💾 Guardar", "key": "submit_val"}
    )

    if submitted:
        fields = {
            "Concepto": st.session_state.concepto_val,
            "Importe": st.session_state.importe_val,
        }

        is_valid, errors = validate_required_fields(fields)

        if is_valid and len(st.session_state.concepto_val) >= 3:
            show_form_feedback("¡Transacción guardada correctamente!", type="success")
        else:
            if not is_valid:
                for error in errors:
                    show_form_feedback(error, type="error")

with st.form("form_validacion"):
    render_form_card(
        title="Nueva Transacción",
        content_fn=formulario_validacion,
        footer=botones_validacion,
        icon="💸"
    )

st.markdown("---")

# ============================================================================
# DEMO 3: Formulario con secciones
# ============================================================================

st.header("3. Formulario con Secciones")

def formulario_secciones():
    # Sección 1
    form_section("Datos Personales", "Información básica del usuario")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nombre", key="nombre_sec")
    with col2:
        st.text_input("Apellidos", key="apellidos_sec")

    # Sección 2
    form_section("Contacto", "Información de contacto")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Email", key="email_sec")
    with col2:
        st.text_input("Teléfono", key="telefono_sec")

    # Sección 3
    form_section("Configuración")

    st.checkbox("Recibir notificaciones", key="notif_sec")

def botones_secciones():
    form_actions(
        primary_btn={"label": "Guardar", "key": "submit_sec"}
    )

with st.form("form_secciones"):
    render_form_card(
        title="Configuración de Perfil",
        content_fn=formulario_secciones,
        footer=botones_secciones,
        icon="⚙️"
    )

st.markdown("---")

# ============================================================================
# DEMO 4: Estados del formulario
# ============================================================================

st.header("4. Estados del Formulario")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Default", use_container_width=True):
        st.session_state.demo_state = "default"

with col2:
    if st.button("Loading", use_container_width=True):
        st.session_state.demo_state = "loading"

with col3:
    if st.button("Success", use_container_width=True):
        st.session_state.demo_state = "success"

with col4:
    if st.button("Error", use_container_width=True):
        st.session_state.demo_state = "error"

st.markdown("")

def formulario_estados():
    if st.session_state.demo_state == "loading":
        show_form_feedback("Procesando...", type="info", icon="⏳")
    elif st.session_state.demo_state == "success":
        show_form_feedback("¡Operación completada con éxito!", type="success")
    elif st.session_state.demo_state == "error":
        show_form_feedback("Hubo un error al procesar la solicitud", type="error")

    st.text_input("Campo de prueba", key="campo_estados")

def botones_estados():
    form_actions(
        primary_btn={"label": "Procesar", "key": "submit_estados"}
    )

with st.form("form_estados"):
    render_form_card(
        title="Formulario con Estados",
        content_fn=formulario_estados,
        footer=botones_estados,
        icon="🎭",
        state=st.session_state.demo_state,
        description=f"Estado actual: {st.session_state.demo_state}"
    )

st.markdown("---")

# ============================================================================
# DEMO 5: Todos los tipos de feedback
# ============================================================================

st.header("5. Tipos de Feedback")

st.subheader("Success")
show_form_feedback("¡Operación completada correctamente!", type="success")

st.subheader("Error")
show_form_feedback("Se produjo un error al procesar la solicitud", type="error")

st.subheader("Warning")
show_form_feedback("Advertencia: Revisa los datos antes de continuar", type="warning")

st.subheader("Info")
show_form_feedback("Información: Todos los campos son opcionales", type="info")

st.markdown("---")

# ============================================================================
# DEMO 6: Validación de errores
# ============================================================================

st.header("6. Mensajes de Validación")

st.subheader("Errores inline por campo")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Email", value="invalid-email", key="email_error")
    show_validation_error("Email", "El email debe contener @")

with col2:
    st.text_input("Contraseña", type="password", value="123", key="pass_error")
    show_validation_error("Contraseña", "Debe tener al menos 8 caracteres")

st.markdown("---")

# Footer
st.markdown("""
---
### Componente FormCard

**Features:**
- ✅ Estilos consistentes con design tokens
- ✅ Estados visuales (default, loading, success, error)
- ✅ Validación integrada
- ✅ Feedback visual
- ✅ Secciones organizadas
- ✅ Accesibilidad (ARIA, WCAG AA)
- ✅ Responsive

**Archivos:**
- `form_card.py` - Componente principal
- `form_card_examples.py` - Ejemplos completos
- `form_card_test.py` - Tests unitarios
- `README_FORM_CARD.md` - Documentación completa
""")
