# ChartContainer Component

Componente reutilizable para gráficas Plotly con estilos consistentes y características avanzadas.

## Índice

- [Características](#características)
- [Instalación](#instalación)
- [Uso Básico](#uso-básico)
- [Variantes](#variantes)
- [Estados Especiales](#estados-especiales)
- [Acciones](#acciones)
- [Layouts Avanzados](#layouts-avanzados)
- [Presets](#presets)
- [API Completa](#api-completa)

---

## Características

- **Estilos Premium Consistentes**: Gradientes, sombras y bordes redondeados del design system
- **Responsive**: Se adapta automáticamente al ancho del contenedor
- **Múltiples Variantes**: default, premium, minimal, glass
- **Estados Especiales**: Loading, empty, error
- **Acciones Integradas**: Botones, filtros, checkboxes
- **Layouts Flexibles**: Full width, half, compact, grid, tabs
- **Configuraciones Preset**: Preconfigurados para casos comunes
- **Integración con Feature Flags**: Rollout progresivo opcional
- **Error Boundaries**: Manejo robusto de errores

---

## Instalación

El componente ya está incluido en el proyecto. Solo necesitas importarlo:

```python
from utils.components.chart_container import render_chart_container
```

O importar desde el paquete:

```python
from utils.components import render_chart_container
```

---

## Uso Básico

### Ejemplo Mínimo

```python
import streamlit as st
from utils.components import render_chart_container
from utils.plotly_theme import create_themed_line_chart

# Crear gráfica
fig = create_themed_line_chart(df, x='fecha', y='saldo')

# Renderizar con container
render_chart_container(fig)
```

### Con Título y Descripción

```python
render_chart_container(
    fig,
    title="Evolución del Saldo",
    description="Saldo después de cada transacción en los últimos 30 días"
)
```

### Con Altura Personalizada

```python
render_chart_container(
    fig,
    title="Dashboard Anual",
    height=600  # píxeles
)
```

---

## Variantes

El componente ofrece 4 variantes de estilo:

### 1. Default (Predeterminada)

```python
render_chart_container(
    fig,
    title="Gráfica Default",
    variant="default"  # opcional, es el default
)
```

- Gradiente premium
- Sombras medianas
- Border radius grande
- Padding estándar

### 2. Premium

```python
render_chart_container(
    fig,
    title="Gráfica Premium",
    variant="premium"
)
```

- Mayor padding y altura
- Sombras más pronunciadas
- Border radius XL
- Máxima calidad visual

### 3. Minimal

```python
render_chart_container(
    fig,
    title="Gráfica Minimal",
    variant="minimal"
)
```

- Sin gradientes
- Sombras mínimas
- Border radius pequeño
- Padding reducido
- Ideal para dashboards densos

### 4. Glass (Glassmorphism)

```python
render_chart_container(
    fig,
    title="Gráfica Glass",
    variant="glass"
)
```

- Fondo translúcido
- Efecto blur
- Bordes sutiles
- Estilo moderno

---

## Estados Especiales

### Loading State

Muestra un skeleton loader mientras se cargan los datos:

```python
render_chart_container(
    loading=True,
    title="Cargando datos..."
)
```

### Empty State

Muestra mensaje cuando no hay datos:

```python
render_chart_container(
    empty_message="No hay transacciones este mes",
    title="Sin Datos"
)
```

### Error State

Muestra error cuando falla la gráfica:

```python
render_chart_container(
    error="Error al conectar con la base de datos",
    title="Error de Conexión"
)
```

### Ejemplo Dinámico

```python
if is_loading:
    render_chart_container(loading=True)
elif has_error:
    render_chart_container(error=error_message)
elif not has_data:
    render_chart_container(empty_message="No hay datos")
else:
    render_chart_container(fig)
```

---

## Acciones

### Acciones Predefinidas

```python
from utils.components import add_chart_actions

actions = add_chart_actions(
    export=True,   # Botón de exportar
    filter=True,   # Selector de período
    refresh=True   # Botón de refrescar
)

render_chart_container(fig, actions=actions)
```

### Acciones Personalizadas

```python
custom_actions = [
    {
        "type": "button",
        "label": "Compartir",
        "icon": "🔗",
        "key": "share_btn",
        "help": "Compartir gráfica"
    },
    {
        "type": "selectbox",
        "label": "Vista",
        "key": "view_select",
        "options": ["Diaria", "Semanal", "Mensual"],
        "index": 0
    },
    {
        "type": "checkbox",
        "label": "Mostrar tendencia",
        "key": "trend_check",
        "value": True
    }
]

render_chart_container(fig, actions=custom_actions)
```

---

## Layouts Avanzados

### Full Width

```python
from utils.components import render_chart_full

render_chart_full(fig, title="Gráfica de Ancho Completo")
```

### Half Width (2 Columnas)

```python
from utils.components import render_chart_half

render_chart_half([
    {"fig": fig1, "title": "Ingresos"},
    {"fig": fig2, "title": "Gastos"}
])
```

### Compact

```python
from utils.components import render_chart_compact

render_chart_compact(fig, title="Mini Dashboard", height=300)
```

### Grid (2x2, 3x3, etc)

```python
from utils.components import create_chart_grid

charts = [
    {"fig": fig1, "title": "Chart 1"},
    {"fig": fig2, "title": "Chart 2"},
    {"fig": fig3, "title": "Chart 3"},
    {"fig": fig4, "title": "Chart 4"}
]

create_chart_grid(charts, columns=2)
```

### Tabs

```python
from utils.components import render_chart_with_tabs

render_chart_with_tabs({
    "Mensual": {"fig": fig_monthly, "title": "Vista Mensual"},
    "Anual": {"fig": fig_yearly, "title": "Vista Anual"},
    "Histórico": {"fig": fig_history, "title": "Histórico"}
})
```

---

## Presets

Configuraciones predefinidas para casos comunes.

### Presets Disponibles

```python
from utils.components import PRESET_CONFIGS

# Ver todos los presets
print(PRESET_CONFIGS)

# Resultado:
# {
#     "finance_dashboard": {
#         "variant": "premium",
#         "height": 500,
#         "show_fullscreen": True,
#         "actions": [...]
#     },
#     "compact_widget": {
#         "variant": "minimal",
#         "height": 250,
#         "show_fullscreen": False,
#     },
#     "fullscreen_analysis": {
#         "variant": "default",
#         "height": 600,
#         "show_fullscreen": True,
#     }
# }
```

### Usar Preset

```python
from utils.components import render_chart_preset

render_chart_preset(
    "finance_dashboard",
    fig,
    title="Dashboard Financiero"
)
```

### Preset con Overrides

```python
render_chart_preset(
    "finance_dashboard",
    fig,
    title="Dashboard Personalizado",
    variant="glass",  # Override
    height=700        # Override
)
```

---

## API Completa

### `render_chart_container()`

```python
render_chart_container(
    fig: Optional[go.Figure] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    actions: Optional[List[Dict]] = None,
    height: int = 450,
    show_fullscreen: bool = True,
    loading: bool = False,
    error: Optional[str] = None,
    empty_message: Optional[str] = None,
    config: Optional[Dict] = None,
    variant: str = "default"
) -> None
```

**Parámetros:**

- `fig`: Figura de Plotly (None si loading o error)
- `title`: Título de la gráfica
- `description`: Descripción breve debajo del título
- `actions`: Lista de acciones (botones, filtros) a mostrar en el header
- `height`: Altura de la gráfica en píxeles (default: 450)
- `show_fullscreen`: Mostrar botón de pantalla completa (default: True)
- `loading`: Mostrar skeleton loader (default: False)
- `error`: Mensaje de error a mostrar (default: None)
- `empty_message`: Mensaje cuando no hay datos (default: None)
- `config`: Configuración adicional para st.plotly_chart (default: None)
- `variant`: Variante de estilo ('default', 'premium', 'minimal', 'glass')

### `add_chart_actions()`

```python
add_chart_actions(
    export: bool = True,
    filter: bool = True,
    refresh: bool = False,
    custom_actions: Optional[List[Dict]] = None
) -> List[Dict]
```

Genera lista de acciones comunes para gráficas.

### `show_chart_loading()`

```python
show_chart_loading(message: str = "Cargando gráfica...") -> None
```

Muestra skeleton loader.

### `show_chart_empty()`

```python
show_chart_empty(message: str = "No hay datos para mostrar") -> None
```

Muestra estado vacío.

---

## Ejemplos Completos

### Ejemplo 1: Dashboard de Finanzas

```python
import streamlit as st
from utils.components import render_chart_container, add_chart_actions
from utils.plotly_theme import create_themed_line_chart
from database.db_manager import obtener_transacciones
import pandas as pd

# Obtener datos
transacciones = obtener_transacciones(mes=11, año=2024)
df = pd.DataFrame(transacciones)

# Verificar si hay datos
if df.empty:
    render_chart_container(
        empty_message="No hay transacciones para este período",
        title="Balance Mensual"
    )
else:
    # Crear gráfica
    fig = create_themed_line_chart(
        df,
        x='fecha',
        y='saldo',
        markers=True
    )

    # Añadir acciones
    actions = add_chart_actions(
        export=True,
        filter=True,
        refresh=True
    )

    # Renderizar
    render_chart_container(
        fig,
        title="Evolución del Balance",
        description=f"Balance diario de {df['fecha'].min()} a {df['fecha'].max()}",
        actions=actions,
        variant="premium",
        height=500
    )
```

### Ejemplo 2: Comparativa Mensual vs Anual

```python
from utils.components import render_chart_with_tabs
from utils.plotly_theme import create_themed_bar_chart

# Crear gráficas
fig_monthly = create_themed_bar_chart(
    df_mensual,
    x='categoria',
    y='importe'
)

fig_yearly = create_themed_bar_chart(
    df_anual,
    x='mes',
    y='total'
)

# Renderizar en tabs
render_chart_with_tabs({
    "Mes Actual": {
        "fig": fig_monthly,
        "title": "Gastos por Categoría - Noviembre",
        "description": "Distribución mensual de gastos"
    },
    "Año Completo": {
        "fig": fig_yearly,
        "title": "Evolución Anual - 2024",
        "description": "Total de gastos por mes"
    }
})
```

### Ejemplo 3: Grid de KPIs

```python
from utils.components import create_chart_grid
from utils.plotly_theme import (
    create_themed_pie_chart,
    create_themed_bar_chart,
    create_themed_line_chart
)

charts = [
    {
        "fig": create_themed_pie_chart(df1, names='categoria', values='total'),
        "title": "Distribución de Gastos",
        "variant": "minimal"
    },
    {
        "fig": create_themed_bar_chart(df2, x='mes', y='balance'),
        "title": "Balance Mensual",
        "variant": "minimal"
    },
    {
        "fig": create_themed_line_chart(df3, x='fecha', y='saldo'),
        "title": "Evolución del Saldo",
        "variant": "minimal"
    },
    {
        "fig": create_themed_bar_chart(df4, x='tipo', y='cantidad'),
        "title": "Transacciones por Tipo",
        "variant": "minimal"
    }
]

create_chart_grid(charts, columns=2)
```

---

## Integración con Otros Componentes

### Con Plotly Theme

```python
from utils.plotly_theme import (
    create_themed_line_chart,
    apply_theme_to_fig
)

# El tema se aplica automáticamente en render_chart_container
fig = create_themed_line_chart(df, x='fecha', y='saldo')
render_chart_container(fig)

# O aplicar manualmente antes
fig = px.line(df, x='fecha', y='saldo')
apply_theme_to_fig(fig)
render_chart_container(fig)
```

### Con Feature Flags

```python
from utils.feature_flags import get_feature_flag

# Habilitar/deshabilitar globalmente
if get_feature_flag("enable_chart_containers", True):
    render_chart_container(fig)
else:
    # Fallback sin container
    st.plotly_chart(fig, use_container_width=True)
```

---

## Mejores Prácticas

### 1. Usa Variantes Apropiadas

- **Premium**: Gráficas hero, dashboards principales
- **Default**: Uso general en páginas
- **Minimal**: Widgets, dashboards densos
- **Glass**: Landing pages, secciones destacadas

### 2. Maneja Estados

Siempre considera loading, empty y error:

```python
try:
    df = obtener_datos()
    if df.empty:
        render_chart_container(empty_message="...")
    else:
        fig = crear_grafica(df)
        render_chart_container(fig)
except Exception as e:
    render_chart_container(error=str(e))
```

### 3. Acciones Consistentes

Usa `add_chart_actions()` para consistencia:

```python
actions = add_chart_actions(export=True, filter=True)
```

### 4. Títulos Descriptivos

```python
# ❌ Mal
render_chart_container(fig, title="Gráfica")

# ✅ Bien
render_chart_container(
    fig,
    title="Evolución del Saldo Mensual",
    description="Balance después de cada transacción"
)
```

### 5. Usa Presets

Para casos comunes, usa presets:

```python
# En lugar de repetir configuración
render_chart_preset("finance_dashboard", fig, title="...")
```

---

## Troubleshooting

### La gráfica no se muestra

1. Verifica que `fig` no es None
2. Verifica que no estás pasando `loading=True` o `error`
3. Revisa la consola de Streamlit para errores

### Los estilos no se aplican

1. Verifica que `variant` es válido: 'default', 'premium', 'minimal', 'glass'
2. Asegúrate de importar correctamente desde `utils.components`
3. Verifica que design_tokens.py está disponible

### Las acciones no funcionan

1. Asegúrate de que cada acción tiene un `key` único
2. Verifica el formato de las acciones (ver ejemplos)
3. Usa `st.session_state[key]` para acceder a valores

---

## Demo Interactiva

Ejecuta la demo para ver todos los ejemplos:

```bash
streamlit run utils/components/chart_container_demo.py
```

---

## Changelog

### v1.0.0 (2024-12-04)

- Lanzamiento inicial
- 4 variantes de estilo
- Estados especiales (loading, empty, error)
- Sistema de acciones
- Layouts avanzados (grid, tabs, half)
- Presets configurables
- Integración con plotly_theme.py y design_tokens.py

---

## Licencia

Parte del proyecto Mi App Finanzas.

---

## Soporte

Para reportar bugs o solicitar features, contacta al equipo de desarrollo.
