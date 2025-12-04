"""
FormCard Component - Componente para formularios estilizados

Proporciona un wrapper para formularios con estilo consistente, validación visual,
y feedback de usuario siguiendo los design tokens de la aplicación.

Características:
- Card container con estilo premium
- Header con título e icono opcional
- Secciones organizadas con dividers
- Validación visual de campos
- Estados: default, loading, success, error
- Feedback con mensajes de éxito/error
- Botones estilizados (primario, secundario, peligro)
- Totalmente accesible (ARIA labels)

Ejemplo básico:
    >>> def formulario_contenido():
    ...     nombre = st.text_input("Nombre", key="nombre")
    ...     email = st.text_input("Email", key="email")
    ...
    >>> render_form_card(
    ...     title="Registro de Usuario",
    ...     content_fn=formulario_contenido,
    ...     icon="👤"
    ... )

Ejemplo con validación:
    >>> def contenido():
    ...     concepto = st.text_input("Concepto", key="concepto")
    ...     importe = st.number_input("Importe", key="importe")
    ...
    >>> render_form_card(
    ...     title="Nueva Transacción",
    ...     content_fn=contenido,
    ...     footer=lambda: form_actions(
    ...         primary_btn={"label": "Guardar", "key": "save"},
    ...         secondary_btn={"label": "Cancelar", "key": "cancel"}
    ...     ),
    ...     icon="💸"
    ... )
"""

import streamlit as st
from typing import Callable, Optional, Dict, List, Any, Literal
from utils.design_tokens import (
    Colors,
    Typography,
    Spacing,
    BorderRadius,
    Transitions,
)


def render_form_card(
    title: str,
    content_fn: Callable[[], None],
    footer: Optional[Callable[[], None]] = None,
    icon: Optional[str] = None,
    state: Literal["default", "loading", "success", "error"] = "default",
    description: Optional[str] = None,
) -> None:
    """
    Renderiza un formulario estilizado dentro de un card premium.

    Args:
        title: Título del formulario
        content_fn: Función que renderiza el contenido del formulario
        footer: Función opcional que renderiza el footer (botones de acción)
        icon: Emoji o icono opcional para el header
        state: Estado visual del card ('default', 'loading', 'success', 'error')
        description: Descripción opcional bajo el título

    Example:
        >>> def mi_formulario():
        ...     nombre = st.text_input("Nombre completo")
        ...     edad = st.number_input("Edad", min_value=0)
        ...
        >>> def mis_botones():
        ...     form_actions(
        ...         primary_btn={"label": "Guardar", "key": "save"},
        ...         secondary_btn={"label": "Cancelar", "key": "cancel"}
        ...     )
        ...
        >>> render_form_card(
        ...     title="Datos Personales",
        ...     content_fn=mi_formulario,
        ...     footer=mis_botones,
        ...     icon="👤"
        ... )
    """
    # Determinar colores según el estado
    state_colors = {
        "default": Colors.PREMIUM_GRADIENT_PRIMARY,
        "loading": Colors.PREMIUM_GRADIENT_SKY,
        "success": Colors.PREMIUM_GRADIENT_TEAL,
        "error": Colors.PREMIUM_GRADIENT_CORAL,
    }

    border_gradient = state_colors.get(state, state_colors["default"])

    # Inyectar CSS para estilos de formulario
    _inject_form_styles()

    # Container principal del card
    st.markdown(
        f"""
        <div class="form-card" role="region" aria-label="{title}">
            <!-- Borde superior con gradiente -->
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: {border_gradient};
                border-radius: {BorderRadius.LG} {BorderRadius.LG} 0 0;
            "></div>
        """,
        unsafe_allow_html=True,
    )

    # Header con título e icono
    _render_form_header(title, icon, description, state)

    # Contenido del formulario
    st.markdown('<div class="form-content">', unsafe_allow_html=True)
    content_fn()
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer con botones (opcional)
    if footer:
        st.markdown(
            f"""
            <div style="
                margin-top: {Spacing.LG};
                padding-top: {Spacing.LG};
                border-top: 1px solid {Colors.GRAY_200};
            ">
            """,
            unsafe_allow_html=True,
        )
        footer()
        st.markdown('</div>', unsafe_allow_html=True)

    # Cerrar container
    st.markdown('</div>', unsafe_allow_html=True)


def _render_form_header(
    title: str,
    icon: Optional[str],
    description: Optional[str],
    state: str,
) -> None:
    """Renderiza el header del FormCard"""
    # Icono de estado
    state_icons = {
        "loading": "⏳",
        "success": "✅",
        "error": "❌",
    }
    state_icon = state_icons.get(state, "")

    header_html = f"""
    <div class="form-header" style="margin-bottom: {Spacing.LG};">
        <div style="display: flex; align-items: center; gap: {Spacing.SM};">
            {f'<span style="font-size: {Typography.TEXT_2XL};">{icon}</span>' if icon else ''}
            <h2 style="
                margin: 0;
                font-size: {Typography.TEXT_2XL};
                font-weight: {Typography.WEIGHT_BOLD};
                color: {Colors.GRAY_900};
            ">{title}</h2>
            {f'<span style="margin-left: auto; font-size: {Typography.TEXT_XL};">{state_icon}</span>' if state_icon else ''}
        </div>
    """

    if description:
        header_html += f"""
        <p style="
            margin: {Spacing.SM} 0 0 0;
            font-size: {Typography.TEXT_SM};
            color: {Colors.GRAY_600};
            line-height: {Typography.LEADING_NORMAL};
        ">{description}</p>
        """

    header_html += "</div>"

    st.markdown(header_html, unsafe_allow_html=True)


def form_section(title: str, description: Optional[str] = None) -> None:
    """
    Renderiza un separador de sección dentro del formulario.

    Útil para organizar formularios largos en secciones lógicas.

    Args:
        title: Título de la sección
        description: Descripción opcional de la sección

    Example:
        >>> form_section("Datos Personales", "Información básica del usuario")
        >>> nombre = st.text_input("Nombre")
        >>> apellido = st.text_input("Apellido")
        >>>
        >>> form_section("Contacto")
        >>> email = st.text_input("Email")
        >>> telefono = st.text_input("Teléfono")
    """
    st.markdown(
        f"""
        <div style="
            margin-top: {Spacing.XL};
            margin-bottom: {Spacing.LG};
            padding-bottom: {Spacing.MD};
            border-bottom: 2px solid {Colors.GRAY_200};
        ">
            <h3 style="
                margin: 0;
                font-size: {Typography.TEXT_LG};
                font-weight: {Typography.WEIGHT_SEMIBOLD};
                color: {Colors.GRAY_800};
                text-transform: uppercase;
                letter-spacing: {Typography.TRACKING_WIDE};
            ">{title}</h3>
            {f'''
            <p style="
                margin: {Spacing.XS} 0 0 0;
                font-size: {Typography.TEXT_SM};
                color: {Colors.GRAY_600};
            ">{description}</p>
            ''' if description else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def form_field_group(
    label: str,
    help_text: Optional[str] = None,
    required: bool = False,
) -> None:
    """
    Agrupa un campo de formulario con su label y texto de ayuda.

    Renderiza un label estilizado que debe preceder al campo de entrada.

    Args:
        label: Texto del label
        help_text: Texto de ayuda opcional (se muestra como tooltip)
        required: Si el campo es requerido (muestra asterisco)

    Example:
        >>> form_field_group("Dirección de email", help_text="Usaremos este email para contactarte", required=True)
        >>> email = st.text_input("", key="email", label_visibility="collapsed")
    """
    label_html = f"""
    <label style="
        display: block;
        margin-bottom: {Spacing.XS};
        font-size: {Typography.TEXT_SM};
        font-weight: {Typography.WEIGHT_MEDIUM};
        color: {Colors.GRAY_700};
    ">
        {label}
        {f'<span style="color: {Colors.ERROR};">*</span>' if required else ''}
        {f'''
        <span style="
            margin-left: {Spacing.XS};
            font-size: {Typography.TEXT_XS};
            color: {Colors.GRAY_500};
            font-weight: {Typography.WEIGHT_NORMAL};
        " title="{help_text}">ⓘ</span>
        ''' if help_text else ''}
    </label>
    """

    st.markdown(label_html, unsafe_allow_html=True)


def form_actions(
    primary_btn: Dict[str, Any],
    secondary_btn: Optional[Dict[str, Any]] = None,
    danger_btn: Optional[Dict[str, Any]] = None,
    align: Literal["left", "center", "right"] = "right",
) -> None:
    """
    Renderiza un grupo de botones de acción del formulario.

    Los botones se estilizan automáticamente según su tipo (primario, secundario, peligro).

    Args:
        primary_btn: Configuración del botón primario (dict con 'label', 'key', 'disabled', 'type')
        secondary_btn: Configuración opcional del botón secundario
        danger_btn: Configuración opcional del botón de peligro
        align: Alineación de los botones ('left', 'center', 'right')

    Example:
        >>> form_actions(
        ...     primary_btn={"label": "Guardar", "key": "save", "type": "primary"},
        ...     secondary_btn={"label": "Cancelar", "key": "cancel"},
        ...     danger_btn={"label": "Eliminar", "key": "delete"},
        ...     align="right"
        ... )

    Note:
        Los botones deben usarse dentro de un st.form() para funcionar correctamente.
    """
    justify_map = {
        "left": "flex-start",
        "center": "center",
        "right": "flex-end",
    }

    st.markdown(
        f"""
        <div style="
            display: flex;
            gap: {Spacing.SM};
            justify-content: {justify_map[align]};
            flex-wrap: wrap;
        ">
        """,
        unsafe_allow_html=True,
    )

    # Usar columnas para los botones
    buttons = []
    if danger_btn:
        buttons.append(("danger", danger_btn))
    if secondary_btn:
        buttons.append(("secondary", secondary_btn))
    if primary_btn:
        buttons.append(("primary", primary_btn))

    if buttons:
        cols = st.columns(len(buttons))

        for col, (btn_type, btn_config) in zip(cols, buttons):
            with col:
                _render_styled_button(btn_type, btn_config)

    st.markdown('</div>', unsafe_allow_html=True)


def _render_styled_button(btn_type: str, config: Dict[str, Any]) -> Any:
    """Renderiza un botón estilizado según su tipo"""
    label = config.get("label", "Button")
    key = config.get("key", "btn")
    disabled = config.get("disabled", False)
    form_button = config.get("use_form_button", True)

    # Determinar tipo de botón de Streamlit
    if btn_type == "primary":
        st_type = "primary"
    elif btn_type == "danger":
        st_type = "secondary"  # Streamlit no tiene tipo 'danger', usamos CSS
    else:
        st_type = "secondary"

    # Renderizar botón
    if form_button:
        clicked = st.form_submit_button(
            label,
            type=st_type,
            disabled=disabled,
            use_container_width=True,
        )
    else:
        clicked = st.button(
            label,
            key=key,
            type=st_type,
            disabled=disabled,
            use_container_width=True,
        )

    # Aplicar estilo de peligro si es necesario
    if btn_type == "danger":
        st.markdown(
            f"""
            <style>
            button[kind="secondary"]:has-text("{label}") {{
                background-color: {Colors.ERROR} !important;
                color: white !important;
                border-color: {Colors.ERROR_DARK} !important;
            }}
            button[kind="secondary"]:has-text("{label}"):hover {{
                background-color: {Colors.ERROR_DARK} !important;
                border-color: {Colors.ERROR_DARK} !important;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    return clicked


def show_form_feedback(
    message: str,
    type: Literal["success", "error", "warning", "info"] = "success",
    icon: Optional[str] = None,
) -> None:
    """
    Muestra un mensaje de feedback del formulario.

    Args:
        message: Mensaje a mostrar
        type: Tipo de feedback ('success', 'error', 'warning', 'info')
        icon: Icono opcional (si no se especifica, se usa uno por defecto)

    Example:
        >>> show_form_feedback("Transacción guardada correctamente", type="success")
        >>> show_form_feedback("Error al guardar la transacción", type="error")
        >>> show_form_feedback("Revisa los campos marcados", type="warning")
    """
    # Configuración por tipo
    feedback_config = {
        "success": {
            "icon": "✅",
            "bg_color": Colors.SUCCESS_ULTRA_LIGHT,
            "border_color": Colors.SUCCESS,
            "text_color": Colors.SUCCESS_DARK,
        },
        "error": {
            "icon": "❌",
            "bg_color": Colors.ERROR_ULTRA_LIGHT,
            "border_color": Colors.ERROR,
            "text_color": Colors.ERROR_DARK,
        },
        "warning": {
            "icon": "⚠️",
            "bg_color": Colors.WARNING_ULTRA_LIGHT,
            "border_color": Colors.WARNING,
            "text_color": Colors.WARNING_DARK,
        },
        "info": {
            "icon": "ℹ️",
            "bg_color": Colors.PRIMARY_ULTRA_LIGHT,
            "border_color": Colors.PRIMARY,
            "text_color": Colors.PRIMARY_DARK,
        },
    }

    config = feedback_config.get(type, feedback_config["info"])
    display_icon = icon or config["icon"]

    st.markdown(
        f"""
        <div role="alert" aria-live="polite" style="
            display: flex;
            align-items: center;
            gap: {Spacing.SM};
            padding: {Spacing.MD} {Spacing.LG};
            margin: {Spacing.MD} 0;
            background-color: {config['bg_color']};
            border-left: 4px solid {config['border_color']};
            border-radius: {BorderRadius.BASE};
            font-size: {Typography.TEXT_SM};
            color: {config['text_color']};
            font-weight: {Typography.WEIGHT_MEDIUM};
        ">
            <span style="font-size: {Typography.TEXT_LG};">{display_icon}</span>
            <span>{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def validate_required_fields(fields: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Valida que los campos requeridos no estén vacíos.

    Args:
        fields: Diccionario con pares {nombre_campo: valor}

    Returns:
        Tupla de (es_valido, lista_de_errores)

    Example:
        >>> fields = {
        ...     "nombre": nombre,
        ...     "email": email,
        ...     "telefono": telefono,
        ... }
        >>> is_valid, errors = validate_required_fields(fields)
        >>> if not is_valid:
        ...     for error in errors:
        ...         st.error(error)
    """
    errors = []

    for field_name, field_value in fields.items():
        # Validar según el tipo de dato
        if field_value is None:
            errors.append(f"El campo '{field_name}' es requerido")
        elif isinstance(field_value, str) and not field_value.strip():
            errors.append(f"El campo '{field_name}' no puede estar vacío")
        elif isinstance(field_value, (int, float)) and field_value == 0:
            # Opcional: solo marcar error si es exactamente 0
            # Comentar esta línea si 0 es un valor válido
            pass

    is_valid = len(errors) == 0
    return is_valid, errors


def show_validation_error(field_name: str, message: str) -> None:
    """
    Muestra un error de validación para un campo específico.

    Renderiza un mensaje de error con estilo inline debajo del campo.

    Args:
        field_name: Nombre del campo con error
        message: Mensaje de error a mostrar

    Example:
        >>> concepto = st.text_input("Concepto", key="concepto")
        >>> if not concepto:
        ...     show_validation_error("Concepto", "El concepto es obligatorio")
    """
    st.markdown(
        f"""
        <div role="alert" class="field-error" style="
            display: flex;
            align-items: center;
            gap: {Spacing.XS};
            margin-top: -{Spacing.XS};
            margin-bottom: {Spacing.SM};
            padding: {Spacing.XS} {Spacing.SM};
            background-color: {Colors.ERROR_ULTRA_LIGHT};
            border-left: 3px solid {Colors.ERROR};
            border-radius: {BorderRadius.SM};
            font-size: {Typography.TEXT_XS};
            color: {Colors.ERROR_DARK};
        ">
            <span>⚠️</span>
            <span><strong>{field_name}:</strong> {message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _inject_form_styles() -> None:
    """Inyecta estilos CSS globales para formularios"""
    st.markdown(
        f"""
        <style>
        /* === FORM CARD STYLES === */
        .form-card {{
            position: relative;
            background: {Colors.PREMIUM_CARD_GRADIENT};
            border-radius: {BorderRadius.LG};
            padding: {Spacing.XL};
            border: 1px solid rgba(10, 76, 62, 0.1);
            box-shadow: {Colors.SHADOW_PREMIUM_MD};
            margin-bottom: {Spacing.LG};
        }}

        .form-content {{
            margin-top: {Spacing.MD};
        }}

        /* === INPUT STYLES === */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {{
            border-radius: {BorderRadius.BASE} !important;
            border: 1px solid {Colors.GRAY_300} !important;
            padding: {Spacing.SM} {Spacing.MD} !important;
            font-size: {Typography.TEXT_BASE} !important;
            transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
            min-height: 44px !important;
            font-size: 16px !important; /* Previene zoom en iOS */
        }}

        /* Focus state */
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {{
            border-color: {Colors.PRIMARY} !important;
            box-shadow: 0 0 0 3px {Colors.PRIMARY_ULTRA_LIGHT} !important;
            outline: none !important;
        }}

        /* Hover state */
        .stTextInput > div > div > input:hover,
        .stNumberInput > div > div > input:hover,
        .stTextArea > div > div > textarea:hover,
        .stSelectbox > div > div > select:hover {{
            border-color: {Colors.GRAY_400} !important;
        }}

        /* Error state */
        .stTextInput.has-error > div > div > input,
        .stNumberInput.has-error > div > div > input {{
            border-color: {Colors.ERROR} !important;
            background-color: {Colors.ERROR_ULTRA_LIGHT} !important;
        }}

        .stTextInput.has-error > div > div > input:focus,
        .stNumberInput.has-error > div > div > input:focus {{
            box-shadow: 0 0 0 3px rgba(239, 83, 80, 0.1) !important;
        }}

        /* === BUTTON STYLES === */
        button[kind="primary"] {{
            background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
            color: white !important;
            border: none !important;
            border-radius: {BorderRadius.BASE} !important;
            padding: {Spacing.SM} {Spacing.LG} !important;
            font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
            transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
            min-height: 44px !important;
        }}

        button[kind="primary"]:hover {{
            transform: translateY(-1px);
            box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        }}

        button[kind="primary"]:active {{
            transform: translateY(0);
        }}

        button[kind="secondary"] {{
            background: white !important;
            color: {Colors.GRAY_700} !important;
            border: 1px solid {Colors.GRAY_300} !important;
            border-radius: {BorderRadius.BASE} !important;
            padding: {Spacing.SM} {Spacing.LG} !important;
            font-weight: {Typography.WEIGHT_MEDIUM} !important;
            transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
            min-height: 44px !important;
        }}

        button[kind="secondary"]:hover {{
            background: {Colors.GRAY_50} !important;
            border-color: {Colors.GRAY_400} !important;
        }}

        /* === LABEL STYLES === */
        .stTextInput > label,
        .stNumberInput > label,
        .stTextArea > label,
        .stSelectbox > label {{
            font-size: {Typography.TEXT_SM} !important;
            font-weight: {Typography.WEIGHT_MEDIUM} !important;
            color: {Colors.GRAY_700} !important;
            margin-bottom: {Spacing.XS} !important;
        }}

        /* === DATE INPUT === */
        .stDateInput > div > div > input {{
            min-height: 44px !important;
            font-size: 16px !important;
        }}

        /* === ACCESSIBILITY === */
        *:focus-visible {{
            outline: 2px solid {Colors.PRIMARY} !important;
            outline-offset: 2px !important;
        }}

        /* Aumentar área táctil mínima (WCAG AAA) */
        button, input, select, textarea {{
            min-height: 44px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
