# Grid System - Sistema de Grillas Responsive

Sistema moderno de grillas basado en CSS Grid con fallback a flexbox para crear layouts flexibles y responsive.

## Características

- **CSS Grid nativo** con auto-fill y auto-fit
- **Responsive por defecto** con breakpoints automáticos
- **Gaps configurables** usando design_tokens
- **Variantes especializadas** para diferentes tipos de contenido
- **Helpers avanzados** para configuración personalizada

## Instalación

```python
from utils.components.grid_system import (
    render_grid,
    render_card_grid,
    render_metric_grid,
    render_image_grid,
    render_masonry_grid,
    auto_grid,
    grid_item,
    responsive_columns
)
```

## Breakpoints Responsive

Por defecto, el sistema usa los siguientes breakpoints:

| Dispositivo | Breakpoint | Columnas |
|------------|------------|----------|
| Desktop | > 1024px | n configuradas |
| Tablet | 768px - 1024px | min(n, 2) |
| Mobile | < 768px | 1 |

## API Principal

### 1. `render_grid()` - Grid Básico

Grid configurable con número fijo de columnas.

```python
def render_grid(
    items: List[any],
    cols: int = 3,
    gap: GapSize = 'md',
    responsive: bool = True,
    item_renderer: Optional[Callable] = None
) -> None
```

**Parámetros:**
- `items`: Lista de contenidos a renderizar
- `cols`: Número de columnas (1-12)
- `gap`: Tamaño del gap ('xs', 'sm', 'md', 'lg', 'xl')
- `responsive`: Si debe aplicar breakpoints automáticos
- `item_renderer`: Función personalizada para renderizar items

**Ejemplo básico:**

```python
items = ["Card 1", "Card 2", "Card 3", "Card 4", "Card 5", "Card 6"]
render_grid(items, cols=3, gap='lg')
```

**Ejemplo con renderer personalizado:**

```python
def render_custom_item(item, index):
    st.markdown(f"### Item {index + 1}")
    st.write(item)

data = ["Contenido A", "Contenido B", "Contenido C"]
render_grid(data, cols=3, item_renderer=render_custom_item)
```

### 2. `render_card_grid()` - Grid de Cards

Grid especializado para renderizar cards con estilo consistente.

```python
def render_card_grid(
    items: List[dict],
    cols: int = 3,
    gap: GapSize = 'md',
    responsive: bool = True
) -> None
```

**Estructura de item:**

```python
{
    "title": "Título de la card",
    "content": "Contenido principal",
    "footer": "Información adicional (opcional)",
    "color": Colors.PRIMARY  # Color de acento (opcional)
}
```

**Ejemplo:**

```python
cards = [
    {
        "title": "Ingresos",
        "content": "2,500€",
        "footer": "+15% vs mes anterior",
        "color": Colors.SUCCESS
    },
    {
        "title": "Gastos",
        "content": "1,800€",
        "footer": "-5% vs mes anterior",
        "color": Colors.ERROR
    },
    {
        "title": "Balance",
        "content": "700€",
        "footer": "Ahorro positivo",
        "color": Colors.PRIMARY
    }
]

render_card_grid(cards, cols=3, gap='lg')
```

### 3. `render_metric_grid()` - Grid de Métricas

Grid optimizado para métricas financieras usando `st.metric()`.

```python
def render_metric_grid(
    metrics: List[dict],
    cols: int = 4,
    gap: GapSize = 'md',
    responsive: bool = True
) -> None
```

**Estructura de métrica:**

```python
{
    "label": "Etiqueta",
    "value": "Valor principal",
    "delta": "Cambio (opcional)",
    "delta_color": "normal|inverse|off (opcional)",
    "help": "Texto de ayuda (opcional)"
}
```

**Ejemplo:**

```python
metrics = [
    {
        "label": "Total Ingresos",
        "value": "2,500€",
        "delta": "+15%",
        "help": "Ingresos del mes actual"
    },
    {
        "label": "Total Gastos",
        "value": "1,800€",
        "delta": "-5%",
        "delta_color": "inverse"
    },
    {
        "label": "Balance",
        "value": "700€",
        "delta": "+10%"
    },
    {
        "label": "Tasa Ahorro",
        "value": "28%",
        "delta": "+3%",
        "help": "Porcentaje de ingresos ahorrados"
    }
]

render_metric_grid(metrics, cols=4, gap='md')
```

### 4. `render_image_grid()` - Grid de Imágenes

Grid optimizado para mostrar imágenes/media con aspect ratio consistente.

```python
def render_image_grid(
    images: List[dict],
    cols: int = 3,
    gap: GapSize = 'sm',
    responsive: bool = True,
    aspect_ratio: str = "1/1"
) -> None
```

**Estructura de imagen:**

```python
{
    "url": "path/to/image.jpg",
    "caption": "Caption de la imagen (opcional)",
    "alt": "Texto alternativo (opcional)"
}
```

**Ejemplo:**

```python
images = [
    {
        "url": "https://example.com/image1.jpg",
        "caption": "Imagen 1",
        "alt": "Descripción de imagen 1"
    },
    {
        "url": "https://example.com/image2.jpg",
        "caption": "Imagen 2"
    },
    {
        "url": "https://example.com/image3.jpg",
        "caption": "Imagen 3"
    }
]

render_image_grid(images, cols=3, aspect_ratio="16/9")
```

**Aspect ratios comunes:**
- `"1/1"` - Cuadrado
- `"16/9"` - Widescreen
- `"4/3"` - Clásico
- `"3/2"` - Fotografía

### 5. `render_masonry_grid()` - Grid Masonry

Grid tipo Pinterest con alturas variables.

```python
def render_masonry_grid(
    items: List[any],
    cols: int = 3,
    gap: GapSize = 'md',
    responsive: bool = True,
    item_renderer: Optional[Callable] = None
) -> None
```

**Ejemplo:**

```python
items = [
    "Contenido corto",
    "Contenido más largo que ocupa más espacio vertical porque tiene más texto...",
    "Contenido medio con algo de información",
    "Otro contenido corto",
    "Contenido extenso con múltiples párrafos..."
]

render_masonry_grid(items, cols=3, gap='md')
```

### 6. `auto_grid()` - Grid Automático

Grid que ajusta automáticamente el número de columnas según el ancho mínimo especificado.

```python
def auto_grid(
    items: List[any],
    min_width: str = '300px',
    gap: GapSize = 'md',
    responsive: bool = True,
    item_renderer: Optional[Callable] = None
) -> None
```

**Ejemplo:**

```python
items = [f"Item {i+1}" for i in range(12)]

# Creará automáticamente tantas columnas como quepan
# con un mínimo de 280px por item
auto_grid(items, min_width='280px', gap='md')
```

**Ventajas:**
- No necesitas especificar número de columnas
- Se adapta automáticamente al tamaño de pantalla
- Ideal para contenido de tamaño variable

### 7. `grid_item()` - Item con Colspan/Rowspan

Crea un item con configuración de span personalizada.

```python
def grid_item(
    content: any,
    span: int = 1,
    row_span: int = 1
) -> dict
```

**Ejemplo:**

```python
items = [
    grid_item("Normal", span=1),
    grid_item("Ancho", span=2),
    grid_item("Normal", span=1),
    grid_item("Muy ancho", span=3),
    grid_item("Alto", span=1, row_span=2)
]
```

**Nota:** Para usar spans personalizados efectivamente, necesitas renderizar manualmente con HTML/CSS o usar `st.columns()` con proporciones.

### 8. `responsive_columns()` - Configuración Responsive Explícita

Genera CSS para control exacto de columnas por breakpoint.

```python
def responsive_columns(
    desktop: int = 4,
    tablet: int = 2,
    mobile: int = 1,
    gap: GapSize = 'md'
) -> str
```

**Ejemplo:**

```python
# Configuración personalizada: 5 cols desktop, 3 tablet, 1 mobile
css = responsive_columns(desktop=5, tablet=3, mobile=1, gap='xl')
st.markdown(css, unsafe_allow_html=True)

st.markdown('<div class="responsive-grid">', unsafe_allow_html=True)
for item in items:
    st.markdown('<div class="grid-item">...</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
```

## Configuración de Gaps

Tamaños de gap disponibles (basados en `design_tokens.py`):

| Gap | Valor CSS | Pixels |
|-----|-----------|--------|
| `xs` | 0.25rem | 4px |
| `sm` | 0.5rem | 8px |
| `md` | 0.75rem | 12px |
| `lg` | 1.5rem | 24px |
| `xl` | 2rem | 32px |

## Casos de Uso

### Dashboard con Métricas

```python
# Métricas principales en 4 columnas
metrics = [
    {"label": "Ingresos", "value": "2,500€", "delta": "+15%"},
    {"label": "Gastos", "value": "1,800€", "delta": "-5%", "delta_color": "inverse"},
    {"label": "Balance", "value": "700€", "delta": "+10%"},
    {"label": "Ahorro", "value": "28%", "delta": "+3%"}
]
render_metric_grid(metrics, cols=4, gap='lg')
```

### Galería de Imágenes

```python
images = [
    {"url": f"image{i}.jpg", "caption": f"Imagen {i}"}
    for i in range(1, 10)
]
render_image_grid(images, cols=3, aspect_ratio="4/3", gap='sm')
```

### Cards de Categorías

```python
categories = [
    {
        "title": "FIJOS",
        "content": "850€",
        "footer": "35% del total",
        "color": Colors.PRIMARY
    },
    {
        "title": "DISFRUTE",
        "content": "720€",
        "footer": "30% del total",
        "color": Colors.SUCCESS
    },
    {
        "title": "EXTRAORDINARIOS",
        "content": "230€",
        "footer": "10% del total",
        "color": Colors.WARNING
    }
]
render_card_grid(categories, cols=3, gap='lg')
```

### Sección de Noticias/Blog

```python
posts = [
    "Post corto",
    "Post con mucho más contenido y varios párrafos...",
    "Post medio",
    "Otro post extenso..."
]
render_masonry_grid(posts, cols=3, gap='md')
```

### Grid Adaptativo de Productos

```python
products = [product_data for product in get_products()]

# Se ajusta automáticamente según espacio disponible
auto_grid(products, min_width='250px', gap='md')
```

## Integración con Componentes Existentes

### Con MetricCard

```python
from utils.components.metric_card import MetricCard
from utils.components.grid_system import render_grid

def render_metric(data, idx):
    MetricCard(
        label=data["label"],
        value=data["value"],
        change=data.get("change"),
        trend=data.get("trend", "neutral")
    )

metrics_data = [...]
render_grid(metrics_data, cols=4, item_renderer=render_metric)
```

### Con ChartContainer

```python
from utils.components.chart_container import ChartContainer
from utils.components.grid_system import render_grid

def render_chart(chart_data, idx):
    with ChartContainer(title=chart_data["title"]):
        st.plotly_chart(chart_data["fig"], use_container_width=True)

charts = [...]
render_grid(charts, cols=2, gap='xl', item_renderer=render_chart)
```

### Con FormCard

```python
from utils.components.form_card import FormCard
from utils.components.grid_system import auto_grid

forms = [
    {"title": "Configuración 1", "fields": [...]},
    {"title": "Configuración 2", "fields": [...]},
]

def render_form(form_data, idx):
    with FormCard(title=form_data["title"]):
        # Render form fields
        pass

auto_grid(forms, min_width='400px', gap='lg', item_renderer=render_form)
```

## Mejores Prácticas

### 1. Elegir el Tipo Correcto de Grid

- **`render_grid()`**: Contenido uniforme, número fijo de columnas
- **`auto_grid()`**: Contenido variable, adaptación automática
- **`render_masonry_grid()`**: Contenido con alturas muy diferentes
- **`render_card_grid()`**: Cards con estilo consistente
- **`render_metric_grid()`**: Métricas financieras
- **`render_image_grid()`**: Galerías de imágenes

### 2. Gap Apropiado por Contexto

- **`xs/sm`**: Imágenes compactas, galerías densas
- **`md`**: Uso general, default recomendado
- **`lg/xl`**: Dashboards, separación clara entre secciones

### 3. Número de Columnas

- **2 columnas**: Comparaciones, before/after
- **3 columnas**: Tríadas, distribución balanceada
- **4 columnas**: Métricas, KPIs, dashboards
- **5-6 columnas**: Galerías densas, muchos items pequeños

### 4. Responsive

- **Siempre activado** para aplicaciones públicas
- **Desactivado** solo si controlas totalmente el viewport

### 5. Performance

- Para grids muy grandes (>50 items), considera paginación
- Usa `item_renderer` eficiente para evitar re-renders
- Evita cálculos pesados dentro de renderers

## Solución de Problemas

### Grid no se muestra

```python
# ❌ Problema: items vacío
render_grid([], cols=3)

# ✅ Solución: Verificar que items tiene contenido
if items:
    render_grid(items, cols=3)
else:
    st.info("No hay items para mostrar")
```

### Columnas no responsive

```python
# ❌ Problema: responsive=False
render_grid(items, cols=4, responsive=False)

# ✅ Solución: Activar responsive
render_grid(items, cols=4, responsive=True)
```

### Items desbordan

```python
# ❌ Problema: Contenido muy ancho sin wrap
render_grid(very_wide_items, cols=3)

# ✅ Solución: Usar auto_grid con min_width apropiado
auto_grid(very_wide_items, min_width='400px')
```

### Gap demasiado grande/pequeño

```python
# ❌ Problema: Gap incorrecto
render_grid(items, cols=3, gap='xl')  # Muy grande

# ✅ Solución: Ajustar gap
render_grid(items, cols=3, gap='md')  # Balanced
```

## Roadmap / Futuras Mejoras

- [ ] Soporte para colspan/rowspan nativo en CSS Grid
- [ ] Animaciones de transición al cambiar layouts
- [ ] Drag & drop para reordenar items
- [ ] Infinite scroll integrado
- [ ] Virtual scrolling para grids enormes
- [ ] Grid con filtros/búsqueda incorporados
- [ ] Soporte para dark mode
- [ ] Presets por tipo de contenido (productos, posts, etc.)

## Ejemplos Completos

Ver el archivo principal para ejecutar:

```bash
streamlit run utils/components/grid_system.py
```

## Referencias

- [CSS Grid Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)
- [A Complete Guide to Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Responsive Grid System](https://www.w3schools.com/css/css_grid.asp)
- Design Tokens: `/Users/daniel/mi_app_finanzas/utils/design_tokens.py`
- Estrategia de Diseño: `/Users/daniel/mi_app_finanzas/docs/ESTRATEGIA_OVERHAUL_DISEÑO.md`

---

**Última actualización:** 2025-12-04
**Versión:** 1.0.0
**Autor:** Claude Code
**Licencia:** MIT
