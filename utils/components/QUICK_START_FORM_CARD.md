# FormCard - Quick Start Guide

Guía rápida para empezar a usar el componente FormCard en 5 minutos.

## 1. Importar el Componente

```python
from utils.components import (
    render_form_card,
    form_actions,
)
```

## 2. Ejemplo Mínimo

```python
import streamlit as st
from utils.components import render_form_card, form_actions

def mi_formulario():
    nombre = st.text_input("Nombre", key="nombre")
    email = st.text_input("Email", key="email")

def mis_botones():
    form_actions(
        primary_btn={"label": "Guardar", "key": "guardar"}
    )

# Renderizar
with st.form("mi_form"):
    render_form_card(
        title="Formulario de Contacto",
        content_fn=mi_formulario,
        footer=mis_botones,
        icon="📧"
    )
```

## 3. Ejecutar Demo

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar demo
streamlit run utils/components/demo_form_card.py
```

## 4. Ver Ejemplos Completos

Abre el archivo `form_card_examples.py` para ver:
- Formulario con validación
- Formulario con secciones
- Formulario con estados (loading, success, error)
- Formulario complejo

## 5. Documentación Completa

- **API Reference**: `README_FORM_CARD.md`
- **Guía de Integración**: `INTEGRATION_GUIDE.md`
- **Resumen**: `FORM_CARD_SUMMARY.md`

## 6. Testing

```bash
# Tests unitarios
python -m pytest utils/components/form_card_test.py -v

# Tests manuales de validación
python -c "
from utils.components.form_card import validate_required_fields
fields = {'nombre': 'Juan', 'email': 'juan@email.com'}
is_valid, errors = validate_required_fields(fields)
print('Válido:', is_valid, 'Errores:', errors)
"
```

## Funciones Principales

| Función | Descripción |
|---------|-------------|
| `render_form_card()` | Renderiza formulario en card estilizado |
| `form_section()` | Separador de secciones |
| `form_field_group()` | Label + campo con validación |
| `form_actions()` | Botones estilizados |
| `show_form_feedback()` | Mensajes success/error/warning |
| `validate_required_fields()` | Valida campos requeridos |
| `show_validation_error()` | Error por campo |

## Estados Disponibles

- `default` - Estado normal (verde)
- `loading` - Cargando (azul)
- `success` - Éxito (verde oscuro)
- `error` - Error (rojo/coral)

## Próximos Pasos

1. Ejecutar demo: `streamlit run utils/components/demo_form_card.py`
2. Revisar ejemplos: `form_card_examples.py`
3. Leer guía de integración: `INTEGRATION_GUIDE.md`
4. Migrar primer formulario de tu app

---

**¿Necesitas ayuda?** Revisa `README_FORM_CARD.md` para documentación completa.
