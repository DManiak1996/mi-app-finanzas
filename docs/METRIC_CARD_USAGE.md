# MetricCard Component - Guía de Uso

## Descripción

El componente `MetricCard` es un componente reutilizable para mostrar métricas financieras con un diseño premium que incluye:

- ✨ Glassmorphism y gradientes premium
- 📊 Indicadores de tendencia visuales
- 💰 Formato automático de números (currency, percent, number)
- 🎨 5 variantes de color (success, danger, info, warning, neutral)
- 🚀 Animaciones hover suaves
- 📱 Responsive design
- 🎯 Integración completa con design_tokens.py

## Instalación

El componente ya está disponible en `utils/components/metric_card.py`.

## Importación

```python
# Opción 1: Importar directamente desde el módulo
from utils.components.metric_card import (
    render_metric_card,
    metric_card_success,
    metric_card_danger,
    metric_card_info,
    metric_card_warning,
    metric_card_neutral,
    render_metric_row,
    render_metric_grid
)

# Opción 2: Importar desde el paquete components (cuando __init__.py esté actualizado)
from utils.components import render_metric_card
```

## Uso Básico

### 1. Métrica Simple

```python
render_metric_card(
    title="Balance del Mes",
    value=700.50,
    icon="⚖️",
    color="info"
)
```

### 2. Métrica con Delta

```python
render_metric_card(
    title="Ingresos",
    value=2500.00,
    delta=8.5,
    icon="💰",
    color="success",
    trend="up"
)
```

### 3. Métrica con Help Text

```python
render_metric_card(
    title="Tasa de Ahorro",
    value=28.5,
    format_type="percent",
    icon="🎯",
    color="info",
    help_text="Porcentaje de ingresos ahorrados este mes"
)
```

## Parámetros

### render_metric_card()

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `title` | `str` | *requerido* | Título de la métrica |
| `value` | `float\|str` | *requerido* | Valor principal |
| `delta` | `float\|str\|None` | `None` | Cambio respecto período anterior |
| `icon` | `str\|None` | `None` | Emoji o icono decorativo |
| `color` | `Literal` | `"neutral"` | Variante: success, danger, info, warning, neutral |
| `trend` | `Literal\|None` | `None` | Tendencia: up, down, neutral |
| `format_type` | `Literal` | `"currency"` | Formato: currency, percent, number, text |
| `help_text` | `str\|None` | `None` | Texto de ayuda mostrado como caption |
| `show_border` | `bool` | `True` | Mostrar barra decorativa superior |
| `glassmorphism` | `bool` | `False` | Aplicar efecto glassmorphism |

## Variantes de Color

### Success (Verde)
Para ingresos, resultados positivos, métricas exitosas.

```python
metric_card_success(
    title="Ingresos del Mes",
    value=2500.00,
    delta=8.5,
    icon="💰"
)
```

### Danger (Rojo)
Para gastos, alertas, métricas negativas.

```python
metric_card_danger(
    title="Gastos Totales",
    value=1800.50,
    delta=-5.2,
    icon="💸"
)
```

### Info (Azul)
Para información general, métricas informativas.

```python
metric_card_info(
    title="Balance",
    value=700.25,
    icon="⚖️"
)
```

### Warning (Naranja)
Para advertencias, estados intermedios, alertas moderadas.

```python
metric_card_warning(
    title="Presupuesto al 85%",
    value="850€",
    icon="⚠️"
)
```

### Neutral (Gris)
Para datos generales, métricas sin clasificación específica.

```python
metric_card_neutral(
    title="Promedio Diario",
    value=60.15,
    icon="📈"
)
```

## Tipos de Formato

### Currency (Moneda)
Formato: `1.234,56 €`

```python
render_metric_card(
    title="Balance",
    value=1234.56,
    format_type="currency"
)
# Output: "1.234,56 €"
```

### Percent (Porcentaje)
Formato: `28.5%`

```python
render_metric_card(
    title="Tasa de Ahorro",
    value=28.5,
    format_type="percent"
)
# Output: "28.5%"
```

### Number (Número)
Formato inteligente según magnitud:
- >= 1000: `1.234` (sin decimales)
- >= 10: `12.3` (1 decimal)
- < 10: `1.23` (2 decimales)

```python
render_metric_card(
    title="Transacciones",
    value=87,
    format_type="number"
)
# Output: "87"
```

### Text (Texto)
Sin formato, valor tal cual.

```python
render_metric_card(
    title="Estado",
    value="En proceso",
    format_type="text"
)
# Output: "En proceso"
```

## Layouts

### Fila de Métricas

Organiza métricas en una fila horizontal:

```python
render_metric_row([
    {"title": "Ingresos", "value": 2500, "color": "success", "icon": "💰"},
    {"title": "Gastos", "value": 1800, "color": "danger", "icon": "💸"},
    {"title": "Balance", "value": 700, "color": "info", "icon": "⚖️"}
])
```

### Grid de Métricas

Organiza métricas en un grid responsive:

```python
metrics = [
    {"title": "Métrica 1", "value": 100, "color": "success"},
    {"title": "Métrica 2", "value": 200, "color": "info"},
    {"title": "Métrica 3", "value": 300, "color": "warning"},
    {"title": "Métrica 4", "value": 400, "color": "danger"},
    {"title": "Métrica 5", "value": 500, "color": "neutral"},
]

render_metric_grid(metrics, columns_desktop=3)
```

## Efectos Especiales

### Glassmorphism

Aplica efecto de vidrio translúcido:

```python
render_metric_card(
    title="Balance Premium",
    value=700.50,
    icon="✨",
    color="info",
    glassmorphism=True
)
```

### Sin Borde Decorativo

Oculta la barra superior decorativa:

```python
render_metric_card(
    title="Métrica Limpia",
    value=1500.00,
    icon="📊",
    color="success",
    show_border=False
)
```

## Ejemplos Reales

### Dashboard Financiero Completo

```python
import streamlit as st
from utils.components.metric_card import render_metric_row, metric_card_info, metric_card_neutral

# Resumen mensual
st.subheader("Resumen del Mes")
render_metric_row([
    {
        "title": "Total Ingresos",
        "value": 2500.00,
        "delta": 5.2,
        "icon": "💰",
        "color": "success",
        "trend": "up",
        "help_text": "Ingresos totales del mes actual"
    },
    {
        "title": "Total Gastos",
        "value": 1850.50,
        "delta": -3.1,
        "icon": "💸",
        "color": "danger",
        "trend": "down",
        "help_text": "Gastos totales del mes actual"
    },
    {
        "title": "Balance",
        "value": 649.50,
        "delta": 12.8,
        "icon": "⚖️",
        "color": "info",
        "trend": "up",
        "help_text": "Diferencia entre ingresos y gastos"
    }
])

# Métricas avanzadas
st.subheader("Métricas Avanzadas")
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card_info("Tasa de Ahorro", 26.0, format_type="percent", icon="🎯")

with col2:
    metric_card_neutral("Gasto/Día", 61.68, icon="📅")

with col3:
    metric_card_info("Transacciones", 87, format_type="number", icon="📋")

with col4:
    metric_card_info("Health Score", 85, format_type="number", icon="💯")
```

### Desglose de Gastos por Categoría

```python
from utils.components.metric_card import render_metric_grid

gastos_categoria = [
    {"title": "Fijos", "value": 850.00, "icon": "🏠", "color": "danger"},
    {"title": "Disfrute", "value": 450.50, "icon": "🎉", "color": "warning"},
    {"title": "Extraordinarios", "value": 550.00, "icon": "⚡", "color": "info"},
]

render_metric_grid(gastos_categoria, columns_desktop=3)
```

### Evolución con Tendencias

```python
render_metric_row([
    {
        "title": "vs Mes Anterior",
        "value": 12.5,
        "format_type": "percent",
        "icon": "📈",
        "color": "success",
        "trend": "up"
    },
    {
        "title": "vs Promedio 3 Meses",
        "value": 8.2,
        "format_type": "percent",
        "icon": "📊",
        "color": "info",
        "trend": "up"
    },
    {
        "title": "vs Año Anterior",
        "value": -3.5,
        "format_type": "percent",
        "icon": "📉",
        "color": "danger",
        "trend": "down"
    }
])
```

## Integración con Feature Flags

```python
from utils.feature_flags import FeatureFlags

if FeatureFlags.USE_NEW_METRIC_CARDS:
    # Usar componente nuevo
    render_metric_card(
        title="Balance",
        value=700.50,
        color="success"
    )
else:
    # Mantener st.metric antiguo
    st.metric("Balance", "700.50 €")
```

## Best Practices

### 1. Consistencia de Iconos
Usa iconos consistentes para el mismo tipo de métrica en toda la app:
- 💰 Ingresos
- 💸 Gastos
- ⚖️ Balance
- 📊 Porcentajes
- 📈 Tendencias positivas
- 📉 Tendencias negativas

### 2. Colores Semánticos
Usa colores según el significado:
- `success`: Ingresos, ahorros, resultados positivos
- `danger`: Gastos, alertas críticas, problemas
- `info`: Información neutral, balances, datos generales
- `warning`: Advertencias, estados intermedios
- `neutral`: Datos sin clasificación específica

### 3. Help Text
Incluye help text para métricas complejas o no obvias:
```python
render_metric_card(
    title="Financial Health Score",
    value=85,
    format_type="number",
    help_text="Puntuación de 0-100 basada en ahorro, eficiencia y estabilidad"
)
```

### 4. Deltas Informativos
Usa deltas para mostrar cambios temporales:
```python
render_metric_card(
    title="Gastos del Mes",
    value=1800.50,
    delta=-5.2,  # -5.2% respecto al mes anterior
    trend="down",  # Indica que bajó (positivo en este caso)
    color="success"  # Verde porque bajaron los gastos
)
```

### 5. Layout Responsive
Usa `render_metric_row()` para layouts automáticos en lugar de columns manuales:
```python
# ✅ Recomendado
render_metric_row([metric1, metric2, metric3])

# ⚠️ Evitar
col1, col2, col3 = st.columns(3)
with col1: render_metric_card(**metric1)
with col2: render_metric_card(**metric2)
with col3: render_metric_card(**metric3)
```

## Demo

Para ver todas las funcionalidades en acción:

```bash
streamlit run demo_metric_card.py
```

## Personalización

### Colores Personalizados
Los colores están definidos en `utils/design_tokens.py`. Para modificarlos, edita ese archivo.

### Tamaños de Fuente
Los tamaños están en `Typography` del módulo design_tokens. Ajústalos allí para cambios globales.

### Sombras y Efectos
Las sombras premium están en `Colors.SHADOW_PREMIUM_*`. Modifícalas en design_tokens.py.

## Troubleshooting

### Error: ModuleNotFoundError
Asegúrate de importar con la ruta completa:
```python
from utils.components.metric_card import render_metric_card
```

### Las métricas no se ven bien en móvil
Usa `render_metric_row()` o `render_metric_grid()` para layouts responsive automáticos.

### Los gradientes no se ven
Verifica que estás usando `unsafe_allow_html=True` en st.markdown (el componente lo hace automáticamente).

## Changelog

### v1.0 (2025-12-04)
- Implementación inicial
- 5 variantes de color
- 4 tipos de formato
- Efectos glassmorphism
- Layouts responsive
- Integración con design_tokens.py

## Referencias

- Documento de diseño: `/Users/daniel/mi_app_finanzas/docs/ESTRATEGIA_OVERHAUL_DISEÑO.md` (Sección 4.2.1)
- Design tokens: `/Users/daniel/mi_app_finanzas/utils/design_tokens.py`
- Demo interactiva: `/Users/daniel/mi_app_finanzas/demo_metric_card.py`

## Autor

Daniel - 2025-12-04

## Licencia

Parte del proyecto FinanzasFlow
