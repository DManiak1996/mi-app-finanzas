# Guía de Integración - FormCard Component

Guía práctica para integrar el componente FormCard en los formularios existentes de la aplicación.

## Tabla de Contenidos

1. [Preparación](#preparación)
2. [Migración Paso a Paso](#migración-paso-a-paso)
3. [Ejemplos de Migración Real](#ejemplos-de-migración-real)
4. [Feature Flags](#feature-flags)
5. [Testing](#testing)
6. [Troubleshooting](#troubleshooting)

---

## Preparación

### 1. Verificar que el componente está disponible

```python
from utils.components import render_form_card
print("FormCard está disponible!")
```

### 2. Revisar design tokens

```python
from utils.design_tokens import Colors, Typography, Spacing
# El componente usa estos tokens automáticamente
```

---

## Migración Paso a Paso

### Paso 1: Identificar formularios existentes

Busca en tu código todos los formularios que usan `st.form()`:

```bash
grep -r "st.form(" app.py pages_*.py
```

### Paso 2: Extraer lógica de negocio

Separa la lógica del formulario de la UI:

**Antes:**
```python
with st.form("mi_form"):
    st.subheader("Título")
    campo1 = st.text_input("Campo 1")
    campo2 = st.number_input("Campo 2")
    submitted = st.form_submit_button("Guardar")

    if submitted:
        # Lógica de guardado
        guardar_datos(campo1, campo2)
```

**Después:**
```python
def contenido_formulario():
    campo1 = st.text_input("Campo 1", key="campo1")
    campo2 = st.number_input("Campo 2", key="campo2")

def botones_formulario():
    submitted = form_actions(
        primary_btn={"label": "Guardar", "key": "guardar"}
    )

    if submitted:
        guardar_datos(
            st.session_state.campo1,
            st.session_state.campo2
        )

with st.form("mi_form"):
    render_form_card(
        title="Título",
        content_fn=contenido_formulario,
        footer=botones_formulario
    )
```

### Paso 3: Añadir validación (opcional)

```python
def contenido_formulario():
    form_field_group("Campo 1", required=True)
    campo1 = st.text_input("", key="campo1", label_visibility="collapsed")

    if not campo1:
        show_validation_error("Campo 1", "Este campo es obligatorio")

def botones_formulario():
    submitted = form_actions(primary_btn={"label": "Guardar", "key": "guardar"})

    if submitted:
        fields = {"Campo 1": st.session_state.campo1}
        is_valid, errors = validate_required_fields(fields)

        if is_valid:
            show_form_feedback("Guardado correctamente", type="success")
        else:
            for error in errors:
                show_form_feedback(error, type="error")
```

---

## Ejemplos de Migración Real

### Ejemplo 1: Formulario "Añadir Gasto" (app.py)

**ANTES (líneas 1045-1100 de app.py):**

```python
def mostrar_añadir_gasto():
    st.title("➕ Añadir Nuevo Gasto")
    st.markdown("Registra gastos individuales...")

    with st.form("form_nuevo_gasto", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            fecha_gasto = st.date_input("📅 Fecha", value=datetime.date.today())
            concepto = st.text_input("💬 Concepto", placeholder="Ej: Compra supermercado")

        with col2:
            importe = st.number_input("💰 Importe (€)", min_value=0.01, step=0.01)
            categoria = st.selectbox("🏷️ Categoría", ["FIJOS", "DISFRUTE", "EXTRAORDINARIOS"])

        notas = st.text_area("📝 Notas (opcional)")

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("💾 Guardar Gasto", type="primary")

        if submitted:
            # Lógica de guardado...
            db_manager.insertar_transaccion(...)
            st.success("¡Gasto guardado correctamente!")
```

**DESPUÉS (con FormCard):**

```python
from utils.components import (
    render_form_card,
    form_section,
    form_field_group,
    form_actions,
    show_form_feedback,
    validate_required_fields,
)

def mostrar_añadir_gasto():
    st.title("➕ Añadir Nuevo Gasto")
    st.markdown("Registra gastos individuales...")

    def contenido_formulario():
        # Sección principal
        form_section("Datos del Gasto", "Información básica de la transacción")

        col1, col2 = st.columns(2)

        with col1:
            form_field_group("Fecha", help_text="Fecha del movimiento", required=True)
            fecha_gasto = st.date_input(
                "",
                value=datetime.date.today(),
                key="fecha_gasto",
                label_visibility="collapsed"
            )

            form_field_group("Concepto", help_text="Descripción del gasto", required=True)
            concepto = st.text_input(
                "",
                placeholder="Ej: Compra supermercado",
                key="concepto_gasto",
                label_visibility="collapsed"
            )

        with col2:
            form_field_group("Importe (€)", required=True)
            importe = st.number_input(
                "",
                min_value=0.01,
                step=0.01,
                format="%.2f",
                key="importe_gasto",
                label_visibility="collapsed"
            )

            form_field_group("Categoría", required=True)
            categoria = st.selectbox(
                "",
                ["FIJOS", "DISFRUTE", "EXTRAORDINARIOS"],
                key="categoria_gasto",
                label_visibility="collapsed"
            )

        # Sección de detalles adicionales
        form_section("Detalles Adicionales", "Información complementaria (opcional)")

        form_field_group("Notas")
        notas = st.text_area(
            "",
            placeholder="Añade cualquier detalle relevante...",
            key="notas_gasto",
            label_visibility="collapsed"
        )

    def botones_formulario():
        submitted = form_actions(
            primary_btn={"label": "💾 Guardar Gasto", "key": "guardar_gasto"},
            secondary_btn={"label": "🔄 Limpiar", "key": "limpiar_gasto"}
        )

        if submitted:
            # Validar campos requeridos
            fields = {
                "Concepto": st.session_state.concepto_gasto,
                "Importe": st.session_state.importe_gasto,
            }

            is_valid, errors = validate_required_fields(fields)

            if is_valid:
                try:
                    # Guardar en base de datos
                    db_manager.insertar_transaccion(
                        fecha=st.session_state.fecha_gasto,
                        concepto=st.session_state.concepto_gasto,
                        importe=-st.session_state.importe_gasto,
                        categoria=st.session_state.categoria_gasto,
                        tipo="GASTO",
                        notas=st.session_state.notas_gasto
                    )

                    show_form_feedback(
                        "¡Gasto guardado correctamente! Ya puedes verlo en tus transacciones.",
                        type="success"
                    )
                except Exception as e:
                    show_form_feedback(
                        f"Error al guardar el gasto: {str(e)}",
                        type="error"
                    )
            else:
                for error in errors:
                    show_form_feedback(error, type="error")

    # Renderizar formulario con FormCard
    with st.form("form_nuevo_gasto", clear_on_submit=True):
        render_form_card(
            title="Nuevo Gasto",
            content_fn=contenido_formulario,
            footer=botones_formulario,
            icon="💸",
            description="Registra un gasto que no aparece en tu extracto bancario"
        )
```

**Beneficios:**
- ✅ Estilos consistentes con el resto de la app
- ✅ Validación visual integrada
- ✅ Feedback de usuario mejorado
- ✅ Mejor organización del código
- ✅ Accesibilidad mejorada
- ✅ Responsive por defecto

---

### Ejemplo 2: Formulario "Añadir Regla" (app.py)

**ANTES (líneas 1482-1520 de app.py):**

```python
st.subheader("Añadir Nueva Regla")
with st.form(key="nueva_regla_form", clear_on_submit=True):
    nuevo_patron = st.text_input("Patrón de texto (puede ser una expresión regular)")
    importes_str = st.text_input("Importes exactos (opcional, separados por coma, ej: 500, 275)")
    nueva_categoria = st.selectbox("Categoría a asignar", ["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "INGRESO"])
    nuevo_tipo = st.selectbox("Tipo de transacción", ["GASTO", "INGRESO"])

    submit_button = st.form_submit_button(label="✨ Añadir Regla")

    if submit_button:
        if nuevo_patron or importes_str:
            # Lógica de guardado...
            categorizer.guardar_regla(...)
            st.success("Regla añadida correctamente")
```

**DESPUÉS (con FormCard):**

```python
from utils.components import render_form_card, form_field_group, form_actions, show_form_feedback

st.subheader("Añadir Nueva Regla")

def contenido_regla():
    form_field_group(
        "Patrón de texto",
        help_text="Puede ser una expresión regular (ej: NETFLIX|HBO|SPOTIFY)",
        required=True
    )
    patron = st.text_input(
        "",
        placeholder="NETFLIX|HBO",
        key="patron_regla",
        label_visibility="collapsed"
    )

    form_field_group(
        "Importes exactos",
        help_text="Opcional: Separados por coma (ej: 9.99, 14.99)"
    )
    importes_str = st.text_input(
        "",
        placeholder="9.99, 14.99",
        key="importes_regla",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)

    with col1:
        form_field_group("Categoría", required=True)
        categoria = st.selectbox(
            "",
            ["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "INGRESO"],
            key="categoria_regla",
            label_visibility="collapsed"
        )

    with col2:
        form_field_group("Tipo de transacción", required=True)
        tipo = st.selectbox(
            "",
            ["GASTO", "INGRESO"],
            key="tipo_regla",
            label_visibility="collapsed"
        )

def botones_regla():
    submitted = form_actions(
        primary_btn={"label": "✨ Añadir Regla", "key": "guardar_regla"}
    )

    if submitted:
        patron = st.session_state.patron_regla
        importes_str = st.session_state.importes_regla

        if patron or importes_str:
            try:
                # Procesar importes
                importes_exactos = []
                if importes_str:
                    importes_exactos = [
                        float(x.strip())
                        for x in importes_str.split(',')
                        if x.strip()
                    ]

                # Guardar regla
                categorizer.guardar_regla(
                    patron=patron,
                    categoria=st.session_state.categoria_regla,
                    tipo=st.session_state.tipo_regla,
                    importes_exactos=importes_exactos
                )

                show_form_feedback(
                    "¡Regla añadida correctamente! Ya se aplicará a futuras importaciones.",
                    type="success"
                )
            except ValueError:
                show_form_feedback(
                    "Error: Los importes deben ser números válidos",
                    type="error"
                )
            except Exception as e:
                show_form_feedback(
                    f"Error al guardar la regla: {str(e)}",
                    type="error"
                )
        else:
            show_form_feedback(
                "Debes especificar al menos un patrón o importes exactos",
                type="warning"
            )

with st.form(key="nueva_regla_form", clear_on_submit=True):
    render_form_card(
        title="Nueva Regla de Clasificación",
        content_fn=contenido_regla,
        footer=botones_regla,
        icon="🏷️",
        description="Define patrones para clasificar transacciones automáticamente"
    )
```

---

## Feature Flags

Para migrar gradualmente, usa feature flags en `utils/feature_flags.py`:

```python
# utils/feature_flags.py

class FeatureFlags:
    # ... otros flags ...

    # FormCard components
    USE_FORM_CARDS = True  # Activar/desactivar globalmente
    USE_FORM_CARDS_GASTOS = True  # Específico para formulario de gastos
    USE_FORM_CARDS_REGLAS = True  # Específico para formulario de reglas
```

**Uso en app.py:**

```python
from utils.feature_flags import FeatureFlags

def mostrar_añadir_gasto():
    if FeatureFlags.USE_FORM_CARDS_GASTOS:
        # Versión nueva con FormCard
        mostrar_formulario_gasto_v2()
    else:
        # Versión vieja
        mostrar_formulario_gasto_viejo()
```

---

## Testing

### 1. Testing Visual

Ejecuta la app y verifica:

```bash
streamlit run app.py
```

- [ ] Los formularios se renderizan correctamente
- [ ] Los estilos se aplican (bordes, colores, sombras)
- [ ] La validación funciona
- [ ] Los botones disparan acciones correctas
- [ ] Los mensajes de feedback se muestran

### 2. Testing Funcional

Verifica cada formulario:

- [ ] Enviar con campos vacíos → Muestra errores
- [ ] Enviar con datos válidos → Guarda correctamente
- [ ] Botón secundario funciona (Cancelar, Limpiar)
- [ ] Estados visuales cambian (loading, success, error)

### 3. Testing de Accesibilidad

- [ ] Navegar con Tab entre campos
- [ ] Todos los campos son accesibles
- [ ] Los mensajes de error son legibles
- [ ] Contraste de colores adecuado

### 4. Testing Responsive

Prueba en diferentes tamaños de pantalla:

- [ ] Desktop (>1024px)
- [ ] Tablet (768px-1024px)
- [ ] Mobile (<768px)

---

## Troubleshooting

### Problema: Los estilos no se aplican

**Síntoma:** Los inputs tienen el estilo por defecto de Streamlit.

**Solución:**
1. Verifica que `render_form_card()` se está llamando (inyecta CSS automáticamente)
2. Verifica que no hay CSS conflictivo en `app.py`
3. Recarga la página con Ctrl+F5 (hard reload)

### Problema: Los botones no funcionan

**Síntoma:** Click en botón no dispara acción.

**Solución:**
1. Asegúrate de que `form_actions()` está dentro de `st.form()`
2. Verifica que los valores están en `st.session_state` con las keys correctas
3. Usa `st.write(st.session_state)` para debuggear

### Problema: Validación no detecta errores

**Síntoma:** `validate_required_fields()` no devuelve errores.

**Solución:**
1. Verifica que los campos están en el diccionario que pasas
2. Verifica que las keys de `session_state` coinciden
3. Usa `st.write(fields)` antes de validar para ver los valores

### Problema: Import error

**Síntoma:** `ModuleNotFoundError: No module named 'utils.components'`

**Solución:**
1. Verifica que existe `utils/components/__init__.py`
2. Verifica que el import está correcto
3. Reinicia Streamlit

### Problema: Estados visuales no cambian

**Síntoma:** El borde superior no cambia de color.

**Solución:**
1. Verifica que pasas el parámetro `state` a `render_form_card()`
2. Los valores válidos son: 'default', 'loading', 'success', 'error'
3. El estado debe estar en `st.session_state`

---

## Checklist de Migración

Usa este checklist para cada formulario que migres:

- [ ] Extraer contenido a función `contenido_formulario()`
- [ ] Extraer botones a función `botones_formulario()`
- [ ] Añadir `form_field_group()` a campos requeridos
- [ ] Implementar validación con `validate_required_fields()`
- [ ] Añadir `show_form_feedback()` para success/error
- [ ] Usar `form_section()` para separar secciones largas
- [ ] Configurar `form_actions()` con botones apropiados
- [ ] Testing visual (renderizado correcto)
- [ ] Testing funcional (guardado funciona)
- [ ] Testing de validación (errores se muestran)
- [ ] Testing responsive (funciona en móvil)
- [ ] Documentar cambios en commit

---

## Próximos Pasos

Una vez migrados todos los formularios:

1. **Activar globalmente**: `FeatureFlags.USE_FORM_CARDS = True`
2. **Eliminar código viejo**: Remover versiones antiguas de formularios
3. **Añadir más features**:
   - Auto-save de formularios
   - Validación async
   - Multi-step forms
4. **Optimizar performance**: Cachear componentes si es necesario

---

**Última actualización:** Diciembre 2025
**Mantenedor:** Claude Code
