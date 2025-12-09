# PageLayout System - Quick Start Guide

## 🚀 Inicio Rápido en 5 Minutos

### 1. Instalación

El sistema PageLayout ya está disponible. No requiere instalación adicional.

```python
from utils.components.page_layout import render_dashboard_layout
```

---

## 📋 4 Layouts Predefinidos

### 1️⃣ Dashboard Layout

**Uso:** Páginas con métricas y gráficas

```python
from utils.components.page_layout import render_dashboard_layout

def mi_dashboard():
    st.metric("Balance", "700€")
    st.line_chart(data)

render_dashboard_layout(
    content_fn=mi_dashboard,
    title="Dashboard Financiero"
)
```

---

### 2️⃣ Form Layout

**Uso:** Páginas de formularios

```python
from utils.components.page_layout import render_form_layout

def mi_formulario():
    with st.form("mi_form"):
        st.text_input("Nombre")
        st.form_submit_button("Guardar")

render_form_layout(
    content_fn=mi_formulario,
    title="Nueva Transacción"
)
```

---

### 3️⃣ Table Layout

**Uso:** Páginas con tablas/listados

```python
from utils.components.page_layout import render_table_layout

def mi_tabla():
    st.dataframe(df, use_container_width=True)

render_table_layout(
    content_fn=mi_tabla,
    title="Transacciones"
)
```

---

### 4️⃣ Detail Layout

**Uso:** Páginas de detalle de un ítem

```python
from utils.components.page_layout import render_detail_layout

def detalle():
    st.write("**Fecha:** 2025-01-15")
    st.write("**Importe:** 50€")

render_detail_layout(
    content_fn=detalle,
    title="Transacción #1234"
)
```

---

## 🧩 5 Helpers Principales

### 1. Page Header

```python
from utils.components.page_layout import page_header

page_header(
    title="Mi Página",
    description="Descripción breve",
    icon="📊"
)
```

---

### 2. Breadcrumbs

```python
from utils.components.page_layout import page_breadcrumbs

page_breadcrumbs([
    {"label": "Inicio", "url": "/"},
    {"label": "Actual", "url": None}
])
```

---

### 3. Page Section

```python
from utils.components.page_layout import page_section

with page_section(title="Métricas", icon="📊"):
    st.metric("Balance", "700€")
```

---

### 4. Page Divider

```python
from utils.components.page_layout import page_divider

st.write("Sección 1")
page_divider()
st.write("Sección 2")
```

---

### 5. Page Footer

```python
from utils.components.page_layout import page_footer

page_footer(
    content="Mi App © 2025",
    links=[{"label": "Ayuda", "url": "/help"}]
)
```

---

## 💡 Ejemplo Completo: Dashboard

```python
import streamlit as st
from utils.components.page_layout import (
    render_dashboard_layout,
    page_section,
    page_divider
)
from utils.components.metric_card import render_metric_row

def mi_dashboard():
    # Métricas
    with page_section(title="Resumen del Mes", icon="📊"):
        render_metric_row([
            {"title": "Ingresos", "value": 2500, "color": "success"},
            {"title": "Gastos", "value": 1800, "color": "danger"},
            {"title": "Balance", "value": 700, "color": "info"}
        ])

    page_divider()

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

## 🎯 Configuraciones Comunes

### Dashboard con Selector de Período

```python
render_dashboard_layout(
    content_fn=mi_contenido,
    title="Dashboard",
    show_period_selector=True  # ← Activa selector mes/año
)
```

---

### Formulario con Ayuda Lateral

```python
help_text = """
### Ayuda
- Completa todos los campos
- El importe debe ser positivo
"""

render_form_layout(
    content_fn=mi_formulario,
    title="Nuevo Item",
    show_help_sidebar=True,  # ← Activa sidebar de ayuda
    help_content=help_text
)
```

---

### Tabla con Filtros y Exportar

```python
render_table_layout(
    content_fn=mi_tabla,
    title="Datos",
    show_filters=True,  # ← Activa sidebar de filtros
    filters_fn=mis_filtros,
    show_export_button=True  # ← Botón exportar en header
)
```

---

### Detalle con Breadcrumbs y Acciones

```python
render_detail_layout(
    content_fn=detalle,
    title="Item #1234",
    breadcrumbs=[  # ← Navegación jerárquica
        {"label": "Lista", "url": "/lista"},
        {"label": "#1234", "url": None}
    ],
    actions=[  # ← Acciones del item
        {"label": "Editar", "icon": "✏️", "callback": editar}
    ]
)
```

---

## 🧪 Probar el Sistema

Ejecuta el demo completo:

```bash
streamlit run utils/components/page_layout_demo.py
```

El demo incluye 7 ejemplos interactivos:
1. Overview de layouts predefinidos
2. Dashboard layout completo
3. Form layout con ayuda
4. Table layout con filtros
5. Detail layout con acciones
6. Componentes individuales
7. Layout personalizado

---

## 📚 Documentación Completa

Para documentación detallada, API reference y troubleshooting:

👉 **Ver: `README_PAGE_LAYOUT.md`**

---

## ✅ Checklist de Implementación

Al migrar una página existente a PageLayout:

- [ ] Identificar el tipo de página (Dashboard/Form/Table/Detail)
- [ ] Mover contenido a función separada
- [ ] Usar layout predefinido correspondiente
- [ ] Agregar breadcrumbs si es necesario
- [ ] Organizar contenido en `page_section()`
- [ ] Agregar `page_divider()` entre secciones principales
- [ ] Probar en diferentes resoluciones

---

## 🎨 Mejores Prácticas

### ✅ Correcto

```python
# Usar layout predefinido
render_dashboard_layout(
    content_fn=mi_dashboard,
    title="Dashboard"
)

# Organizar en secciones
with page_section(title="Métricas", icon="📊"):
    render_metrics()
```

### ❌ Incorrecto

```python
# Reimplementar todo
st.title("Dashboard")
st.write("Contenido...")  # Sin estructura

# Sin separación
render_metrics()
render_charts()  # Sin secciones ni divisores
```

---

## 🔗 Componentes Relacionados

- **Metric Card:** `render_metric_card()` - Tarjetas de métricas
- **Chart Container:** `render_chart_container()` - Contenedores de gráficos
- **Form Card:** `render_form_card()` - Tarjetas de formularios
- **Data Table:** `render_data_table()` - Tablas de datos

---

**¿Listo para empezar?** Elige un layout predefinido y comienza a crear páginas consistentes. 🚀
