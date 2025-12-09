# FormCard Component

Componente reutilizable para formularios estilizados en Streamlit.

## Características

- **Estilos consistentes**: Usa design tokens centralizados
- **Estados visuales**: default, loading, success, error
- **Validación integrada**: Helpers para validar campos
- **Feedback visual**: Mensajes de éxito/error/warning
- **Secciones organizadas**: Divide formularios largos
- **Accesibilidad**: ARIA labels, contraste WCAG AA, navegación por teclado
- **Responsive**: Adaptado a móviles (min-height 44px, font-size 16px)

## Instalación

El componente ya está disponible en `utils/components/form_card.py`.

```python
from utils.components import (
    render_form_card,
    form_section,
    form_field_group,
    form_actions,
    show_form_feedback,
    validate_required_fields,
    show_validation_error,
)
```

## Uso Básico

### 1. Formulario Simple

```python
import streamlit as st
from utils.components import render_form_card, form_actions

def mi_formulario():
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")

def mis_botones():
    form_actions(
        primary_btn={"label": "Guardar", "key": "save"}
    )

with st.form("mi_form"):
    render_form_card(
        title="Registro",
        content_fn=mi_formulario,
        footer=mis_botones,
        icon="👤"
    )
```

### 2. Formulario con Validación

```python
from utils.components import (
    render_form_card,
    form_field_group,
    show_validation_error,
    validate_required_fields,
)

def formulario_con_validacion():
    form_field_group("Concepto", required=True)
    concepto = st.text_input("", key="concepto", label_visibility="collapsed")

    if not concepto:
        show_validation_error("Concepto", "El concepto es obligatorio")

    form_field_group("Importe (€)", required=True)
    importe = st.number_input("", key="importe", label_visibility="collapsed")

def botones():
    submitted = form_actions(
        primary_btn={"label": "Guardar", "key": "submit"}
    )

    if submitted:
        fields = {
            "Concepto": st.session_state.concepto,
            "Importe": st.session_state.importe,
        }

        is_valid, errors = validate_required_fields(fields)

        if is_valid:
            show_form_feedback("¡Guardado correctamente!", type="success")
        else:
            for error in errors:
                st.error(error)

with st.form("form_validacion"):
    render_form_card(
        title="Nueva Transacción",
        content_fn=formulario_con_validacion,
        footer=botones,
        icon="💸"
    )
```

### 3. Formulario con Secciones

```python
from utils.components import form_section

def formulario_largo():
    # Sección 1
    form_section("Datos Personales", "Información básica")
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")

    # Sección 2
    form_section("Contacto")
    email = st.text_input("Email")
    telefono = st.text_input("Teléfono")
```

### 4. Formulario con Estados

```python
# Estado en session_state
if "form_state" not in st.session_state:
    st.session_state.form_state = "default"

def formulario():
    if st.session_state.form_state == "success":
        show_form_feedback("¡Operación exitosa!", type="success")
    elif st.session_state.form_state == "error":
        show_form_feedback("Hubo un error", type="error")

    # Campos del formulario...

with st.form("form"):
    render_form_card(
        title="Mi Formulario",
        content_fn=formulario,
        state=st.session_state.form_state  # 'default', 'loading', 'success', 'error'
    )
```

## API Reference

### `render_form_card()`

Función principal para renderizar un formulario estilizado.

**Parámetros:**

- `title` (str): Título del formulario
- `content_fn` (Callable): Función que renderiza el contenido
- `footer` (Callable, opcional): Función que renderiza botones
- `icon` (str, opcional): Emoji o icono para el header
- `state` (str, opcional): Estado visual ('default', 'loading', 'success', 'error')
- `description` (str, opcional): Descripción bajo el título

**Ejemplo:**

```python
render_form_card(
    title="Nuevo Gasto",
    content_fn=lambda: st.text_input("Concepto"),
    footer=lambda: form_actions(primary_btn={"label": "Guardar", "key": "save"}),
    icon="💸",
    state="default",
    description="Registra un nuevo gasto"
)
```

---

### `form_section()`

Renderiza un separador de sección dentro del formulario.

**Parámetros:**

- `title` (str): Título de la sección
- `description` (str, opcional): Descripción de la sección

**Ejemplo:**

```python
form_section("Datos Personales", "Información básica del usuario")
```

---

### `form_field_group()`

Agrupa un campo con su label y texto de ayuda.

**Parámetros:**

- `label` (str): Texto del label
- `help_text` (str, opcional): Texto de ayuda (tooltip)
- `required` (bool): Si el campo es requerido (muestra *)

**Ejemplo:**

```python
form_field_group("Email", help_text="Tu dirección de correo", required=True)
email = st.text_input("", key="email", label_visibility="collapsed")
```

---

### `form_actions()`

Renderiza botones de acción del formulario.

**Parámetros:**

- `primary_btn` (dict): Config del botón primario (`{"label": "...", "key": "..."}`)
- `secondary_btn` (dict, opcional): Config del botón secundario
- `danger_btn` (dict, opcional): Config del botón de peligro
- `align` (str): Alineación ('left', 'center', 'right')

**Ejemplo:**

```python
form_actions(
    primary_btn={"label": "Guardar", "key": "save"},
    secondary_btn={"label": "Cancelar", "key": "cancel"},
    danger_btn={"label": "Eliminar", "key": "delete"},
    align="right"
)
```

---

### `show_form_feedback()`

Muestra un mensaje de feedback.

**Parámetros:**

- `message` (str): Mensaje a mostrar
- `type` (str): Tipo ('success', 'error', 'warning', 'info')
- `icon` (str, opcional): Icono personalizado

**Ejemplo:**

```python
show_form_feedback("Guardado correctamente", type="success")
show_form_feedback("Error al guardar", type="error")
show_form_feedback("Revisa los campos", type="warning")
```

---

### `validate_required_fields()`

Valida que los campos requeridos no estén vacíos.

**Parámetros:**

- `fields` (dict): Diccionario `{nombre_campo: valor}`

**Retorna:**

- `tuple[bool, list[str]]`: (es_válido, lista_de_errores)

**Ejemplo:**

```python
fields = {
    "Nombre": nombre,
    "Email": email,
}

is_valid, errors = validate_required_fields(fields)

if not is_valid:
    for error in errors:
        st.error(error)
```

---

### `show_validation_error()`

Muestra un error de validación para un campo específico.

**Parámetros:**

- `field_name` (str): Nombre del campo
- `message` (str): Mensaje de error

**Ejemplo:**

```python
if not email or "@" not in email:
    show_validation_error("Email", "El email debe contener @")
```

## Estilos CSS

El componente inyecta estilos CSS automáticamente para:

- **Inputs**: Border radius, padding, estados hover/focus/error
- **Botones**: Gradientes, sombras, transiciones
- **Labels**: Tipografía consistente
- **Accesibilidad**: Outline en focus, área táctil mínima (44px)

### Estados de Input

- **Default**: Borde gris claro
- **Hover**: Borde gris oscuro
- **Focus**: Borde azul + sombra azul
- **Error**: Borde rojo + fondo rosa claro

### Tipos de Botón

- **Primary**: Gradiente verde oscuro a lima
- **Secondary**: Fondo blanco, borde gris
- **Danger**: Fondo rojo, texto blanco

## Accesibilidad

El componente sigue las mejores prácticas de accesibilidad:

- ✅ **ARIA labels**: `role="region"`, `role="alert"`, `aria-label`, `aria-live`
- ✅ **Navegación por teclado**: Todos los campos son accesibles con Tab
- ✅ **Contraste de color**: WCAG AA (4.5:1 mínimo)
- ✅ **Área táctil**: Mínimo 44x44px (WCAG AAA)
- ✅ **Font size**: 16px mínimo (previene zoom en iOS)
- ✅ **Focus visible**: Outline de 2px en elementos activos

## Responsive

El componente es responsive y funciona correctamente en:

- **Desktop**: Layout completo
- **Tablet**: Columnas adaptativas
- **Mobile**: Layout vertical, inputs táctiles

### Optimizaciones Móviles

- `min-height: 44px` en todos los inputs y botones
- `font-size: 16px` para prevenir zoom automático en iOS
- Padding adecuado para dedos (no mouse)

## Testing

### Ejecutar Tests Unitarios

```bash
pytest utils/components/form_card_test.py -v
```

### Tests Manuales

1. Ejecutar ejemplos:
   ```bash
   streamlit run utils/components/form_card_examples.py
   ```

2. Verificar:
   - Renderizado correcto de todos los componentes
   - Validación de campos funciona
   - Estados visuales se aplican correctamente
   - Botones disparan acciones correctas
   - Accesibilidad (Tab, screen readers)

## Ejemplos Completos

Ver archivo `form_card_examples.py` para ejemplos completos de:

1. ✅ Formulario básico de transacción
2. ✅ Validación en tiempo real
3. ✅ Estados del formulario (loading, success, error)
4. ✅ Formulario complejo con múltiples secciones
5. ✅ Validación completa con feedback

## Integración con la App

### Migración de Formularios Existentes

#### Antes (código viejo):

```python
st.subheader("💸 Nuevo Gasto")
with st.form("form_gasto"):
    concepto = st.text_input("Concepto")
    importe = st.number_input("Importe")
    submitted = st.form_submit_button("Guardar")
```

#### Después (con FormCard):

```python
def formulario():
    form_field_group("Concepto", required=True)
    concepto = st.text_input("", key="concepto", label_visibility="collapsed")

    form_field_group("Importe (€)", required=True)
    importe = st.number_input("", key="importe", label_visibility="collapsed")

def botones():
    form_actions(primary_btn={"label": "💾 Guardar", "key": "submit"})

with st.form("form_gasto"):
    render_form_card(
        title="Nuevo Gasto",
        content_fn=formulario,
        footer=botones,
        icon="💸"
    )
```

### Feature Flag

Para migrar gradualmente, usa feature flags:

```python
from utils.feature_flags import FeatureFlags

if FeatureFlags.USE_FORM_CARDS:
    # Versión nueva con FormCard
    with st.form("form"):
        render_form_card(...)
else:
    # Versión vieja
    st.subheader("Título")
    with st.form("form"):
        # Formulario viejo
```

## Troubleshooting

### Los estilos no se aplican

**Problema**: Los inputs no tienen los estilos personalizados.

**Solución**: Asegúrate de llamar a `render_form_card()` que inyecta los estilos CSS automáticamente.

---

### Los botones no funcionan

**Problema**: Los botones no disparan acciones.

**Solución**: Asegúrate de que `form_actions()` está dentro de un `st.form()`.

---

### Validación no funciona

**Problema**: `validate_required_fields()` no detecta errores.

**Solución**: Verifica que los valores de los campos estén en `st.session_state` y que las keys coincidan.

---

### Error de import

**Problema**: `ModuleNotFoundError: No module named 'utils.components'`

**Solución**: Asegúrate de que el archivo `__init__.py` existe en `utils/components/`.

## Roadmap

Funcionalidades futuras:

- [ ] Soporte para dark mode
- [ ] Animaciones de transición entre estados
- [ ] Validación async (con spinners)
- [ ] Auto-save de formularios
- [ ] Campo de búsqueda con autocomplete
- [ ] Upload de archivos estilizado
- [ ] Multi-step forms (wizard)

## Contribuir

Para añadir nuevas funcionalidades al componente:

1. Añade la función en `form_card.py`
2. Exporta en `__init__.py`
3. Añade ejemplo en `form_card_examples.py`
4. Añade test en `form_card_test.py`
5. Documenta en este README

## Licencia

Este componente es parte del proyecto Mi App Finanzas.

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0.0
**Autor:** Claude Code
