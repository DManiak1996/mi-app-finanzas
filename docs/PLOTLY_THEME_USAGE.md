# Guía de Uso del Tema Unificado de Plotly

## Introducción

Este documento describe cómo usar el nuevo sistema de temas unificado para todas las gráficas Plotly de la aplicación.

El tema está definido en `/utils/plotly_theme.py` e integrado con el sistema de design tokens (`/utils/design_tokens.py`).

---

## Características Principales

✅ **Tema Consistente**: Todas las gráficas usan los mismos colores, fuentes y estilos
✅ **Colores Semánticos**: Verde para ingresos, rojo para gastos, azul para balance
✅ **Tooltips Mejorados**: Información clara y bien formateada
✅ **Animaciones Suaves**: Transiciones fluidas de 250ms
✅ **Responsive**: Adaptado para móviles
✅ **Accesibilidad**: Alto contraste y legibilidad

---

## Importar el Tema

```python
from utils.plotly_theme import (
    apply_theme_to_fig,           # Aplicar tema a figura existente
    create_themed_line_chart,     # Crear gráfica de líneas temática
    create_themed_bar_chart,      # Crear gráfica de barras temática
    create_themed_pie_chart,      # Crear gráfica de pie/donut temática
    create_themed_scatter_chart,  # Crear scatter plot temático
    create_themed_area_chart,     # Crear gráfica de área temática
    add_reference_line,           # Añadir línea de referencia
    CHART_COLORS_FINANCE          # Colores semánticos financieros
)
```

---

## Uso Básico

### Opción 1: Aplicar tema a una figura existente

```python
import plotly.express as px
from utils.plotly_theme import apply_theme_to_fig

# Crear gráfica como siempre
fig = px.bar(df, x='mes', y='total')

# Aplicar tema unificado
apply_theme_to_fig(fig, title='Ventas Mensuales', height=500)

# Mostrar
st.plotly_chart(fig, use_container_width=True)
```

### Opción 2: Crear gráfica temática desde cero

```python
from utils.plotly_theme import create_themed_bar_chart

# Crear y aplicar tema en un solo paso
fig = create_themed_bar_chart(
    df,
    x='mes',
    y='total',
    title='Ventas Mensuales',
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)
```

---

## Ejemplos por Tipo de Gráfica

### 1. Gráfico de Líneas

```python
from utils.plotly_theme import create_themed_line_chart

fig = create_themed_line_chart(
    df,
    x='fecha',
    y='saldo',
    title='Evolución del Saldo',
    labels={'fecha': 'Fecha', 'saldo': 'Saldo (€)'},
    markers=True,     # Mostrar puntos
    fill=True,        # Rellenar área bajo la línea
    line_shape='linear'  # 'linear', 'spline', 'hv', etc.
)
```

**Múltiples líneas:**

```python
# Preparar datos
df_melted = df.melt(id_vars='fecha', value_vars=['ingresos', 'gastos'])

fig = create_themed_line_chart(
    df_melted,
    x='fecha',
    y='value',
    color='variable',  # Colorear por columna
    title='Ingresos vs Gastos'
)
```

### 2. Gráfico de Barras

```python
from utils.plotly_theme import create_themed_bar_chart

# Barras simples
fig = create_themed_bar_chart(
    df,
    x='categoria',
    y='total',
    title='Gastos por Categoría',
    text_auto=True,          # Mostrar valores en barras
    orientation='v'          # 'v' vertical, 'h' horizontal
)

# Barras agrupadas
fig = create_themed_bar_chart(
    df,
    x='mes',
    y='total',
    color='categoria',       # Agrupar por categoría
    barmode='group',         # 'group', 'stack', 'relative'
    title='Comparativa Mensual'
)
```

### 3. Gráfico de Pie/Donut

```python
from utils.plotly_theme import create_themed_pie_chart

fig = create_themed_pie_chart(
    df,
    names='categoria',
    values='total',
    title='Distribución de Gastos',
    hole=0.4,              # 0 = pie completo, 0.4 = donut
    pull_first=True        # Destacar primer sector
)
```

### 4. Scatter Plot

```python
from utils.plotly_theme import create_themed_scatter_chart

fig = create_themed_scatter_chart(
    df,
    x='km',
    y='coste',
    title='Coste vs Kilómetros',
    size='kwh',            # Tamaño de puntos variable
    color='franja',        # Color por categoría
    trendline='ols'        # Línea de tendencia
)
```

### 5. Gráfico de Área

```python
from utils.plotly_theme import create_themed_area_chart

fig = create_themed_area_chart(
    df,
    x='mes',
    y=['ingresos', 'gastos'],
    title='Evolución de Ingresos y Gastos',
    groupnorm='percent'    # Normalizar a 100%
)
```

---

## Personalización Avanzada

### Añadir Líneas de Referencia

```python
from utils.plotly_theme import add_reference_line

# Crear gráfica
fig = create_themed_line_chart(df, x='mes', y='balance')

# Añadir línea horizontal en y=0 (break even)
add_reference_line(
    fig,
    value=0,
    orientation='h',
    line_dash='dash',
    annotation='Break Even',
    annotation_position='right'
)

# Añadir línea vertical en x=6 (mitad del año)
add_reference_line(
    fig,
    value=6,
    orientation='v',
    line_dash='dot',
    annotation='Mitad del Año'
)
```

### Usar Colores Semánticos Financieros

```python
from utils.plotly_theme import CHART_COLORS_FINANCE

# Colores disponibles:
CHART_COLORS_FINANCE['income']    # Verde para ingresos
CHART_COLORS_FINANCE['expense']   # Rojo para gastos
CHART_COLORS_FINANCE['balance']   # Azul para balance
CHART_COLORS_FINANCE['positive']  # Verde para positivo
CHART_COLORS_FINANCE['negative']  # Rojo para negativo
CHART_COLORS_FINANCE['neutral']   # Gris para neutral
CHART_COLORS_FINANCE['warning']   # Naranja para advertencias

# Usar en una gráfica
fig = go.Figure()
fig.add_trace(go.Bar(
    x=df['mes'],
    y=df['ingresos'],
    marker_color=CHART_COLORS_FINANCE['income'],
    name='Ingresos'
))
fig.add_trace(go.Bar(
    x=df['mes'],
    y=df['gastos'],
    marker_color=CHART_COLORS_FINANCE['expense'],
    name='Gastos'
))

apply_theme_to_fig(fig, title='Ingresos vs Gastos')
```

### Configuración Manual del Tema

Si necesitas personalizar completamente:

```python
from utils.plotly_theme import get_unified_plotly_theme

# Obtener tema base
theme = get_unified_plotly_theme()

# Modificar según necesites
theme['height'] = 600
theme['title']['text'] = 'Mi Título Personalizado'
theme['xaxis']['title'] = 'Eje X'

# Aplicar a figura
fig.update_layout(**theme)
```

---

## Configuración del Tema

El tema se define en `get_unified_plotly_theme()` con estos parámetros:

### Fuentes
- **Familia**: Inter, SF Pro Display, system fonts
- **Tamaño**: 14px (texto), 20px (título)
- **Color**: Gray 900 (#262730)

### Colores
- **Fondo**: Blanco (#ffffff)
- **Grids**: Gray 200 (#e0e0e0)
- **Líneas de ejes**: Gray 300 (#bdbdbd)
- **Paleta**: 7 colores premium (verde teal, coral, dorado, etc.)

### Ejes
- **Grids**: Líneas sutiles de 1px
- **Zero line**: Línea de 2px para y=0
- **Tick fonts**: 12px

### Tooltips (Hover)
- **Fondo**: Gray 900 (casi negro)
- **Texto**: Blanco
- **Tamaño**: 13px
- **Alineación**: Izquierda

### Animaciones
- **Duración**: 250ms
- **Easing**: cubic-in-out

### Márgenes
- **Izquierda**: 60px
- **Derecha**: 40px
- **Arriba**: 80px (para título)
- **Abajo**: 60px

---

## Mejores Prácticas

### ✅ DO

1. **Usar funciones temáticas** cuando sea posible:
   ```python
   fig = create_themed_bar_chart(df, x='mes', y='total')  # ✅ BIEN
   ```

2. **Aplicar tema a figuras manuales**:
   ```python
   fig = go.Figure()
   fig.add_trace(...)
   apply_theme_to_fig(fig)  # ✅ BIEN
   ```

3. **Usar colores semánticos**:
   ```python
   marker_color=CHART_COLORS_FINANCE['income']  # ✅ BIEN
   ```

4. **Especificar hovertemplates personalizados**:
   ```python
   hovertemplate='<b>%{x}</b><br>Total: %{y:.2f} €<extra></extra>'  # ✅ BIEN
   ```

### ❌ DON'T

1. **No hardcodear colores**:
   ```python
   marker_color='#26a69a'  # ❌ MAL
   ```

2. **No ignorar el tema**:
   ```python
   fig = px.bar(df, x='mes', y='total')
   st.plotly_chart(fig)  # ❌ MAL - falta apply_theme_to_fig()
   ```

3. **No usar templates obsoletos**:
   ```python
   fig = px.line(df, template='plotly_dark')  # ❌ MAL
   ```

---

## Migración de Código Existente

### Antes (sin tema)
```python
fig = px.pie(df, names='categoria', values='total', hole=0.3)
fig.update_traces(textinfo='percent', marker=dict(line=dict(width=2)))
fig.update_layout(title='Distribución', height=400)
st.plotly_chart(fig)
```

### Después (con tema)
```python
fig = create_themed_pie_chart(
    df,
    names='categoria',
    values='total',
    title='Distribución',
    hole=0.4
)
st.plotly_chart(fig, use_container_width=True)
```

**Beneficios**: 50% menos código, estilo consistente, mejor UX.

---

## Troubleshooting

### Problema: "Gráfica no se ve bien en móvil"
**Solución**: Usar `use_container_width=True` en `st.plotly_chart()`:
```python
st.plotly_chart(fig, use_container_width=True)
```

### Problema: "Colores no coinciden con el diseño"
**Solución**: Revisar que estés usando `CHART_COLORS_FINANCE` o `CHART_COLORS_PREMIUM`:
```python
from utils.plotly_theme import CHART_COLORS_FINANCE
marker_color=CHART_COLORS_FINANCE['income']
```

### Problema: "El tema no se aplica"
**Solución**: Asegurarte de llamar `apply_theme_to_fig()` DESPUÉS de añadir todas las trazas:
```python
fig = go.Figure()
fig.add_trace(...)  # Añadir trazas primero
apply_theme_to_fig(fig)  # Aplicar tema al final
```

---

## Referencia Rápida

| Función | Uso | Ejemplo |
|---------|-----|---------|
| `apply_theme_to_fig(fig)` | Aplicar tema a figura existente | `apply_theme_to_fig(fig, title='Mi Título')` |
| `create_themed_line_chart()` | Gráfico de líneas | `create_themed_line_chart(df, x='fecha', y='saldo')` |
| `create_themed_bar_chart()` | Gráfico de barras | `create_themed_bar_chart(df, x='mes', y='total')` |
| `create_themed_pie_chart()` | Pie/Donut | `create_themed_pie_chart(df, names='cat', values='val')` |
| `create_themed_scatter_chart()` | Scatter plot | `create_themed_scatter_chart(df, x='km', y='coste')` |
| `create_themed_area_chart()` | Gráfico de área | `create_themed_area_chart(df, x='mes', y='total')` |
| `add_reference_line()` | Línea de referencia | `add_reference_line(fig, value=0, orientation='h')` |

---

## Archivos Modificados

1. **`/utils/plotly_theme.py`** (NUEVO): Tema unificado y funciones helper
2. **`/utils/visualizer.py`**: Actualizado para usar el nuevo tema
3. **`/app.py`**: Gráfico de evolución del saldo actualizado
4. **`/pages_coche_electrico.py`**: Todas las gráficas actualizadas

---

## Recursos

- **Design Tokens**: `/utils/design_tokens.py`
- **Estrategia de Diseño**: `/docs/ESTRATEGIA_OVERHAUL_DISEÑO.md` (Sección 3.2)
- **Documentación Plotly**: https://plotly.com/python/

---

## Conclusión

El tema unificado de Plotly proporciona:
- ✅ Consistencia visual en toda la aplicación
- ✅ Colores semánticos para finanzas
- ✅ Tooltips informativos y claros
- ✅ Animaciones suaves
- ✅ Responsive y accesible
- ✅ Menos código, más legible

**Usa las funciones temáticas siempre que puedas para mantener la consistencia.**
