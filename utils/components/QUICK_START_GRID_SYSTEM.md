# Quick Start - Grid System

Guía rápida para empezar a usar el Grid System en 5 minutos.

## Instalación

```python
from utils.components.grid_system import (
    render_grid,
    render_card_grid,
    render_metric_grid,
    auto_grid
)
```

## Caso 1: Dashboard con Métricas (2 minutos)

```python
import streamlit as st
from utils.components.grid_system import render_metric_grid

# 1. Preparar datos
metrics = [
    {"label": "Ingresos", "value": "2,500€", "delta": "+15%"},
    {"label": "Gastos", "value": "1,800€", "delta": "-5%", "delta_color": "inverse"},
    {"label": "Balance", "value": "700€", "delta": "+10%"},
    {"label": "Ahorro", "value": "28%", "delta": "+3%"}
]

# 2. Renderizar grid
render_metric_grid(metrics, cols=4, gap='lg')
```

**Resultado:** 4 métricas en una fila responsive que se adapta a mobile.

## Caso 2: Cards de Categorías (3 minutos)

```python
from utils.components.grid_system import render_card_grid
from utils.design_tokens import Colors

# 1. Preparar datos
cards = [
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

# 2. Renderizar grid
render_card_grid(cards, cols=3, gap='lg')
```

**Resultado:** 3 cards con estilo consistente y borde superior coloreado.

## Caso 3: Grid Automático (1 minuto)

```python
from utils.components.grid_system import auto_grid

# 1. Preparar items
items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

# 2. Renderizar grid automático
auto_grid(items, min_width='250px', gap='md')
```

**Resultado:** Grid que ajusta automáticamente las columnas según espacio disponible.

## Caso 4: Renderer Personalizado (4 minutos)

```python
from utils.components.grid_system import render_grid
import plotly.graph_objects as go

# 1. Función para renderizar cada item
def render_chart(data, idx):
    st.subheader(data["title"])
    fig = go.Figure(data=data["fig_data"])
    st.plotly_chart(fig, use_container_width=True)

# 2. Preparar datos
charts = [
    {"title": "Ventas", "fig_data": [...]},
    {"title": "Gastos", "fig_data": [...]},
]

# 3. Renderizar con renderer personalizado
render_grid(charts, cols=2, gap='xl', item_renderer=render_chart)
```

**Resultado:** 2 gráficos en columnas con renderer personalizado.

## Parámetros Comunes

### Gaps Disponibles
- `xs` = 4px - Compacto
- `sm` = 8px - Pequeño
- `md` = 12px - Medio (default)
- `lg` = 24px - Grande
- `xl` = 32px - Extra grande

### Columnas Recomendadas
- **2 columnas**: Comparaciones, before/after
- **3 columnas**: Distribución balanceada
- **4 columnas**: Métricas/KPIs
- **Auto**: Deja que el sistema decida

### Responsive
Por defecto `responsive=True`:
- Desktop (>1024px): n columnas configuradas
- Tablet (768-1024px): max 2 columnas
- Mobile (<768px): 1 columna

## Cheat Sheet

```python
# Grid básico
render_grid(items, cols=3)

# Cards con estilo
render_card_grid(cards, cols=4, gap='lg')

# Métricas
render_metric_grid(metrics, cols=4)

# Auto grid
auto_grid(items, min_width='300px')

# Masonry (alturas variables)
render_masonry_grid(posts, cols=3)

# Imágenes
render_image_grid(images, cols=3, aspect_ratio="16/9")

# Personalizado
render_grid(data, cols=2, item_renderer=custom_func)
```

## Próximos Pasos

1. **Ver ejemplos completos**: `streamlit run utils/components/grid_system_examples.py`
2. **Leer documentación**: `utils/components/README_GRID_SYSTEM.md`
3. **Explorar código**: `utils/components/grid_system.py`

## Solución Rápida de Problemas

**Grid no responsive en mobile?**
→ Asegúrate de usar `responsive=True` (es el default)

**Items muy juntos?**
→ Aumenta el gap: `gap='lg'` o `gap='xl'`

**Muchas columnas en desktop?**
→ Reduce: `cols=3` o `cols=4` en lugar de 6+

**Contenido desborda?**
→ Usa `auto_grid()` con `min_width` apropiado

---

Listo para empezar! 🚀
