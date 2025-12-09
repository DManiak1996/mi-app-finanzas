# PageLayout System - Documentación Completa

## 📐 Descripción

**PageLayout** es un sistema completo de layouts consistentes para páginas de la aplicación. Proporciona layouts predefinidos, componentes estructurales y helpers para mantener consistencia visual en toda la aplicación.

### Características Principales

- ✅ **Función principal `render_page_layout()`** con callback de contenido
- ✅ **4 Layouts predefinidos:** Dashboard, Form, Table, Detail
- ✅ **Page headers** con título, descripción, icono y acciones
- ✅ **Sistema de breadcrumbs** para navegación jerárquica
- ✅ **Secciones de contenido** con spacing consistente
- ✅ **Sidebar opcional** para filtros y navegación secundaria
- ✅ **Footer opcional** con links y copyright
- ✅ **Container responsive** con max-width y padding
- ✅ **Compatible** con `design_tokens.py` y `feature_flags.py`
- ✅ **Documentación exhaustiva** con ejemplos de uso

---

## 🚀 Quick Start

### Instalación

El módulo ya está disponible en `utils/components/page_layout.py`. No requiere instalación adicional.

### Uso Básico

```python
from utils.components.page_layout import render_dashboard_layout

def mi_contenido():
    st.write("Contenido de mi dashboard")
    st.metric("Balance", "700€")

render_dashboard_layout(
    content_fn=mi_contenido,
    title="Mi Dashboard",
    description="Resumen financiero completo"
)
```

### Ejemplo Completo

```python
import streamlit as st
from utils.components.page_layout import render_dashboard_layout, page_section
from utils.components.metric_card import render_metric_row

def mi_dashboard():
    # Métricas
    with page_section(title="Resumen del Mes", icon="📊"):
        render_metric_row([
            {"title": "Ingresos", "value": 2500, "color": "success"},
            {"title": "Gastos", "value": 1800, "color": "danger"},
            {"title": "Balance", "value": 700, "color": "info"}
        ])

    # Gráficos
    with page_section(title="Evolución", icon="📈"):
        st.line_chart(data)

def mis_filtros():
    st.selectbox("Categoría", ["Todas", "FIJOS", "DISFRUTE"])
    st.button("Aplicar", use_container_width=True)

# Renderizar
render_dashboard_layout(
    content_fn=mi_dashboard,
    title="Dashboard Financiero",
    description="Análisis completo de tus finanzas",
    show_period_selector=True,
    show_filters=True,
    filters_fn=mis_filtros
)
```

---

## 📚 API Reference

### Función Principal

#### `render_page_layout()`

Renderiza una página completa con layout consistente.

**Firma:**
```python
def render_page_layout(
    content_fn: Callable,
    title: Optional[str] = None,
    header: Optional[Dict[str, Any]] = None,
    sidebar: Optional[Dict[str, Any]] = None,
    footer: Optional[Dict[str, Any]] = None,
    max_width: str = Config.MAX_CONTAINER_WIDTH,
    padding: str = Spacing.XL,
    background: str = Colors.BG_PRIMARY
) -> None
```

**Parámetros:**
- `content_fn`: Función que renderiza el contenido de la página
- `title`: Título de la página (usado si `header` no se provee)
- `header`: Configuración del header (dict)
  - `title`: Título
  - `description`: Descripción
  - `icon`: Emoji/icono
  - `breadcrumbs`: Lista de breadcrumbs
  - `actions`: Lista de acciones
- `sidebar`: Configuración del sidebar (dict)
  - `content_fn`: Función de contenido
  - `width`: Ancho (ej: "300px")
  - `position`: Posición ("left" o "right")
- `footer`: Configuración del footer (dict)
  - `content`: Contenido principal
  - `links`: Lista de links
  - `copyright`: Texto de copyright
- `max_width`: Ancho máximo del container
- `padding`: Padding del container
- `background`: Color de fondo

**Ejemplo:**
```python
def mi_contenido():
    st.write("Hola mundo")

render_page_layout(
    content_fn=mi_contenido,
    header={
        "title": "Mi Página",
        "description": "Descripción",
        "icon": "📄",
        "breadcrumbs": [{"label": "Inicio", "url": "/"}]
    },
    sidebar={
        "content_fn": mis_filtros,
        "width": "300px",
        "position": "left"
    },
    footer={
        "content": "Mi App © 2025",
        "links": [{"label": "Ayuda", "url": "/help"}]
    }
)
```

---

## 🎨 Layouts Predefinidos

### 1. Dashboard Layout

**Uso:** Páginas con métricas y gráficas

**Características:**
- Container ancho (1600px)
- Selector de período opcional
- Sidebar de filtros opcional
- Background con gradiente premium

**Función:**
```python
def render_dashboard_layout(
    content_fn: Callable,
    title: str = "Dashboard",
    description: Optional[str] = None,
    icon: str = "📊",
    show_period_selector: bool = True,
    show_filters: bool = False,
    filters_fn: Optional[Callable] = None,
    breadcrumbs: Optional[List[Dict[str, str]]] = None
) -> None
```

**Ejemplo:**
```python
from utils.components.page_layout import render_dashboard_layout

def mi_dashboard():
    st.metric("Balance", "700€")
    st.line_chart(data)

def mis_filtros():
    st.selectbox("Mes", ["Enero", "Febrero", "Marzo"])

render_dashboard_layout(
    content_fn=mi_dashboard,
    title="Dashboard Financiero",
    description="Resumen de ingresos y gastos",
    show_period_selector=True,
    show_filters=True,
    filters_fn=mis_filtros
)
```

---

### 2. Form Layout

**Uso:** Páginas de formularios

**Características:**
- Container estrecho (800px) para mejor legibilidad
- Sidebar opcional con ayuda
- Padding adicional para formularios

**Función:**
```python
def render_form_layout(
    content_fn: Callable,
    title: str = "Formulario",
    description: Optional[str] = None,
    icon: str = "📝",
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    show_help_sidebar: bool = False,
    help_content: Optional[str] = None
) -> None
```

**Ejemplo:**
```python
from utils.components.page_layout import render_form_layout

def mi_formulario():
    with st.form("mi_form"):
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        st.form_submit_button("Enviar")

help_text = """
### Ayuda
Completa todos los campos marcados como obligatorios.
"""

render_form_layout(
    content_fn=mi_formulario,
    title="Nueva Transacción",
    description="Completa los campos",
    show_help_sidebar=True,
    help_content=help_text
)
```

---

### 3. Table Layout

**Uso:** Páginas con tablas/listados

**Características:**
- Container ancho (1400px)
- Sidebar de filtros opcional
- Botón de exportar en header

**Función:**
```python
def render_table_layout(
    content_fn: Callable,
    title: str = "Datos",
    description: Optional[str] = None,
    icon: str = "📋",
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    show_filters: bool = True,
    filters_fn: Optional[Callable] = None,
    show_export_button: bool = True
) -> None
```

**Ejemplo:**
```python
from utils.components.page_layout import render_table_layout

def mi_tabla():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    st.dataframe(df, use_container_width=True)

def mis_filtros():
    st.date_input("Desde")
    st.date_input("Hasta")

render_table_layout(
    content_fn=mi_tabla,
    title="Transacciones",
    description="Listado completo",
    filters_fn=mis_filtros,
    show_export_button=True
)
```

---

### 4. Detail Layout

**Uso:** Páginas de detalle de un ítem

**Características:**
- Container medio (1000px)
- Botón "Volver" en header
- Acciones opcionales (editar, eliminar)

**Función:**
```python
def render_detail_layout(
    content_fn: Callable,
    title: str,
    subtitle: Optional[str] = None,
    icon: str = "📄",
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    show_back_button: bool = True,
    actions: Optional[List[Dict[str, Any]]] = None
) -> None
```

**Ejemplo:**
```python
from utils.components.page_layout import render_detail_layout

def detalle():
    st.write("**Fecha:** 2025-01-15")
    st.write("**Importe:** 50€")

def editar():
    st.info("Editar transacción")

render_detail_layout(
    content_fn=detalle,
    title="Transacción #1234",
    subtitle="Compra en MERCADONA",
    breadcrumbs=[
        {"label": "Transacciones", "url": "/transacciones"},
        {"label": "#1234", "url": None}
    ],
    actions=[
        {"label": "Editar", "icon": "✏️", "callback": editar}
    ]
)
```

---

## 🧩 Componentes Helper

### `page_header()`

Renderiza un header de página consistente.

**Firma:**
```python
def page_header(
    title: str,
    description: Optional[str] = None,
    icon: Optional[str] = None,
    actions: Optional[List[Dict[str, Any]]] = None,
    breadcrumbs: Optional[List[Dict[str, str]]] = None,
    background: str = Colors.PREMIUM_BG_GRADIENT,
    show_divider: bool = True
) -> None
```

**Ejemplo:**
```python
from utils.components.page_layout import page_header

page_header(
    title="Dashboard Financiero",
    description="Resumen de tus finanzas",
    icon="📊",
    breadcrumbs=[
        {"label": "Inicio", "url": "/"},
        {"label": "Dashboard", "url": None}
    ]
)
```

---

### `page_breadcrumbs()`

Renderiza breadcrumbs de navegación.

**Firma:**
```python
def page_breadcrumbs(
    items: List[Dict[str, str]]
) -> None
```

**Ejemplo:**
```python
from utils.components.page_layout import page_breadcrumbs

page_breadcrumbs([
    {"label": "Inicio", "url": "/"},
    {"label": "Transacciones", "url": "/transacciones"},
    {"label": "Detalle", "url": None}
])
```

---

### `page_section()`

Context manager para crear secciones de contenido.

**Firma:**
```python
@contextmanager
def page_section(
    title: Optional[str] = None,
    description: Optional[str] = None,
    icon: Optional[str] = None,
    collapsible: bool = False,
    expanded: bool = True,
    background: str = "transparent",
    padding: str = Spacing.LG,
    margin_top: str = Spacing.XL,
    margin_bottom: str = Spacing.XL
)
```

**Ejemplo:**
```python
from utils.components.page_layout import page_section

with page_section(title="Métricas Principales", icon="📊"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Balance", "700€")

with page_section(title="Configuración", collapsible=True):
    st.checkbox("Opción 1")
    st.checkbox("Opción 2")
```

---

### `page_divider()`

Renderiza un divisor visual horizontal.

**Firma:**
```python
def page_divider(
    margin: str = Spacing.XL,
    color: str = Colors.GRAY_200,
    thickness: str = "1px",
    style: Literal["solid", "dashed", "dotted"] = "solid"
) -> None
```

**Ejemplo:**
```python
from utils.components.page_layout import page_divider

st.write("Sección 1")
page_divider()
st.write("Sección 2")
page_divider(style="dashed")
st.write("Sección 3")
```

---

### `page_footer()`

Renderiza un footer de página consistente.

**Firma:**
```python
def page_footer(
    content: Optional[str] = None,
    links: Optional[List[Dict[str, str]]] = None,
    copyright: Optional[str] = None,
    background: str = Colors.GRAY_100,
    show_divider: bool = True
) -> None
```

**Ejemplo:**
```python
from utils.components.page_layout import page_footer

page_footer(
    content="Mi App Finanzas",
    links=[
        {"label": "Ayuda", "url": "/help"},
        {"label": "Privacidad", "url": "/privacy"}
    ],
    copyright="© 2025 Mi App Finanzas"
)
```

---

## 💡 Casos de Uso Comunes

### Caso 1: Dashboard con Métricas y Gráficos

```python
from utils.components.page_layout import render_dashboard_layout, page_section
from utils.components.metric_card import render_metric_row

def mi_dashboard():
    # Métricas
    with page_section(title="Resumen del Mes", icon="📊"):
        render_metric_row([
            {"title": "Ingresos", "value": 2500, "color": "success"},
            {"title": "Gastos", "value": 1800, "color": "danger"},
            {"title": "Balance", "value": 700, "color": "info"}
        ])

    # Gráficos
    with page_section(title="Evolución", icon="📈"):
        st.line_chart(data)

render_dashboard_layout(
    content_fn=mi_dashboard,
    title="Dashboard Financiero",
    show_period_selector=True
)
```

---

### Caso 2: Formulario con Ayuda Lateral

```python
from utils.components.page_layout import render_form_layout

def mi_formulario():
    with st.form("nueva_transaccion"):
        fecha = st.date_input("Fecha")
        importe = st.number_input("Importe")
        concepto = st.text_input("Concepto")
        st.form_submit_button("Guardar")

help_content = """
### Ayuda
- **Fecha:** Fecha de la transacción
- **Importe:** Cantidad en euros
- **Concepto:** Descripción breve
"""

render_form_layout(
    content_fn=mi_formulario,
    title="Nueva Transacción",
    show_help_sidebar=True,
    help_content=help_content
)
```

---

### Caso 3: Tabla con Filtros

```python
from utils.components.page_layout import render_table_layout

def mi_tabla():
    df = obtener_transacciones()
    st.dataframe(df, use_container_width=True)

def mis_filtros():
    st.selectbox("Categoría", ["Todas", "FIJOS", "DISFRUTE"])
    st.date_input("Desde")
    st.date_input("Hasta")
    st.button("Aplicar", use_container_width=True)

render_table_layout(
    content_fn=mi_tabla,
    title="Transacciones",
    filters_fn=mis_filtros,
    show_export_button=True
)
```

---

### Caso 4: Detalle con Acciones

```python
from utils.components.page_layout import render_detail_layout, page_section

def detalle_transaccion():
    with page_section(title="Información", icon="📝"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Fecha:** 15/01/2025")
            st.write("**Importe:** -45.50€")
        with col2:
            st.write("**Categoría:** DISFRUTE")
            st.write("**Concepto:** MERCADONA")

def editar():
    st.info("Editar transacción")

def eliminar():
    st.warning("¿Eliminar transacción?")

render_detail_layout(
    content_fn=detalle_transaccion,
    title="Transacción #1234",
    subtitle="Compra en MERCADONA",
    actions=[
        {"label": "Editar", "icon": "✏️", "callback": editar},
        {"label": "Eliminar", "icon": "🗑️", "callback": eliminar}
    ]
)
```

---

## 🎯 Mejores Prácticas

### 1. Usa Layouts Predefinidos

✅ **Correcto:**
```python
render_dashboard_layout(
    content_fn=mi_dashboard,
    title="Mi Dashboard"
)
```

❌ **Incorrecto:**
```python
# Reimplementar todo desde cero
st.title("Mi Dashboard")
col1, col2 = st.columns([3, 1])
# ... código duplicado
```

---

### 2. Organiza Contenido en Secciones

✅ **Correcto:**
```python
def mi_contenido():
    with page_section(title="Métricas", icon="📊"):
        render_metrics()

    with page_section(title="Gráficos", icon="📈"):
        render_charts()
```

❌ **Incorrecto:**
```python
def mi_contenido():
    render_metrics()
    render_charts()  # Sin separación visual
```

---

### 3. Usa Breadcrumbs para Navegación

✅ **Correcto:**
```python
render_detail_layout(
    content_fn=detalle,
    title="Transacción #1234",
    breadcrumbs=[
        {"label": "Inicio", "url": "/"},
        {"label": "Transacciones", "url": "/transacciones"},
        {"label": "#1234", "url": None}
    ]
)
```

❌ **Incorrecto:**
```python
render_detail_layout(
    content_fn=detalle,
    title="Transacción #1234"
    # Sin breadcrumbs - usuario no sabe dónde está
)
```

---

### 4. Separa Lógica de Presentación

✅ **Correcto:**
```python
def mi_contenido():
    """Lógica de presentación separada."""
    data = obtener_datos()
    with page_section(title="Resultados"):
        st.dataframe(data)

render_dashboard_layout(content_fn=mi_contenido)
```

❌ **Incorrecto:**
```python
# Todo mezclado en una función
def render_todo():
    data = obtener_datos()
    st.title("Dashboard")
    st.dataframe(data)
```

---

## 🔧 Troubleshooting

### Problema: "El contenido se sale del container"

**Solución:** Verifica que estés usando `use_container_width=True` en los componentes de Streamlit:

```python
st.dataframe(df, use_container_width=True)
st.plotly_chart(fig, use_container_width=True)
```

---

### Problema: "El sidebar no aparece"

**Solución:** Asegúrate de pasar tanto `show_filters=True` como `filters_fn`:

```python
render_dashboard_layout(
    content_fn=mi_dashboard,
    show_filters=True,  # ← Importante
    filters_fn=mis_filtros  # ← Importante
)
```

---

### Problema: "Los breadcrumbs no se muestran"

**Solución:** Los breadcrumbs deben ser una lista de diccionarios con `label` y `url`:

```python
breadcrumbs=[
    {"label": "Inicio", "url": "/"},  # Con URL
    {"label": "Actual", "url": None}  # Sin URL = actual
]
```

---

### Problema: "El footer aparece a mitad de página"

**Solución:** Asegúrate de llamar `page_footer()` al final del contenido:

```python
def mi_contenido():
    # ... contenido
    page_footer(...)  # ← Al final
```

---

## 📊 Ejemplos Avanzados

### Ejemplo 1: Dashboard Completo

Ver archivo: `utils/components/page_layout_demo.py` - Función `ejemplo_dashboard_layout()`

### Ejemplo 2: Formulario Multi-Paso

Ver archivo: `utils/components/page_layout_demo.py` - Función `ejemplo_form_layout()`

### Ejemplo 3: Tabla con Paginación

Ver archivo: `utils/components/page_layout_demo.py` - Función `ejemplo_table_layout()`

### Ejemplo 4: Detalle con Tabs

Ver archivo: `utils/components/page_layout_demo.py` - Función `ejemplo_detail_layout()`

---

## 🧪 Testing

Para probar todos los layouts y componentes, ejecuta el demo:

```bash
streamlit run utils/components/page_layout_demo.py
```

El demo incluye:
- Overview de todos los layouts
- Ejemplo de cada layout predefinido
- Ejemplos de componentes individuales
- Ejemplo de layout personalizado

---

## 🔗 Enlaces Relacionados

- **Design Tokens:** `utils/design_tokens.py` - Sistema de diseño centralizado
- **Feature Flags:** `utils/feature_flags.py` - Control de características
- **Metric Card:** `utils/components/metric_card.py` - Tarjetas de métricas
- **Chart Container:** `utils/components/chart_container.py` - Contenedores de gráficos
- **Form Card:** `utils/components/form_card.py` - Tarjetas de formularios
- **Data Table:** `utils/components/data_table.py` - Tablas de datos

---

## 📝 Changelog

### v1.0.0 (2025-12-04)
- ✅ Implementación inicial del sistema PageLayout
- ✅ 4 layouts predefinidos (Dashboard, Form, Table, Detail)
- ✅ Función principal `render_page_layout()`
- ✅ 5 helpers (header, breadcrumbs, section, divider, footer)
- ✅ Demo completo con ejemplos
- ✅ Documentación exhaustiva

---

## 👨‍💻 Autor

**Claude Code**
Fecha: 2025-12-04
Versión: 1.0.0

Basado en: **ESTRATEGIA_OVERHAUL_DISEÑO.md - Sección 4.3**

---

## 📄 Licencia

Este componente es parte de **Mi App Finanzas** y sigue la misma licencia del proyecto principal.

---

**¿Preguntas o sugerencias?** Consulta el archivo `page_layout_demo.py` para más ejemplos o revisa la sección de troubleshooting arriba.
