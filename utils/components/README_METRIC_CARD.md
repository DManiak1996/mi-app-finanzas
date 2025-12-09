# MetricCard Component

Componente reutilizable para métricas financieras con diseño premium.

## Características

- 🎨 **5 variantes de color**: success, danger, info, warning, neutral
- 💰 **4 formatos automáticos**: currency, percent, number, text
- 📊 **Indicadores de tendencia**: flechas visuales (↗ ↘ →)
- ✨ **Efectos premium**: glassmorphism, gradientes, sombras multicapa
- 🚀 **Animaciones hover**: transiciones suaves
- 📱 **Responsive**: layouts automáticos
- 🎯 **Design tokens**: integración completa con design_tokens.py

## Instalación

El componente está disponible en `/Users/daniel/mi_app_finanzas/utils/components/metric_card.py`.

## Quickstart

```python
from utils.components.metric_card import render_metric_card

# Uso básico
render_metric_card(
    title="Balance del Mes",
    value=700.50,
    icon="⚖️"
)

# Con delta y tendencia
render_metric_card(
    title="Ingresos",
    value=2500.00,
    delta=8.5,
    icon="💰",
    color="success",
    trend="up"
)
```

## Funciones Helper

```python
from utils.components.metric_card import (
    metric_card_success,
    metric_card_danger,
    metric_card_info
)

metric_card_success("Ingresos", 2500.00, delta=8.5, icon="💰")
metric_card_danger("Gastos", 1800.50, delta=-5.2, icon="💸")
metric_card_info("Balance", 700.25, icon="⚖️")
```

## Layout Automático

```python
from utils.components.metric_card import render_metric_row

render_metric_row([
    {"title": "Ingresos", "value": 2500, "color": "success", "icon": "💰"},
    {"title": "Gastos", "value": 1800, "color": "danger", "icon": "💸"},
    {"title": "Balance", "value": 700, "color": "info", "icon": "⚖️"}
])
```

## Archivos

```
utils/components/
├── metric_card.py           # Componente principal
├── __init__.py              # Exportaciones
└── README_METRIC_CARD.md    # Este archivo

docs/
└── METRIC_CARD_USAGE.md     # Documentación completa

examples/
└── metric_card_quickstart.py # Ejemplo rápido

tests/
├── test_metric_card.py         # Tests con pytest
└── test_metric_card_simple.py  # Tests sin pytest

demo_metric_card.py          # Demo interactiva completa
```

## Demostración

```bash
# Demo completa con todos los ejemplos
streamlit run demo_metric_card.py

# Quickstart con ejemplos básicos
streamlit run examples/metric_card_quickstart.py
```

## Tests

```bash
# Con pytest (si está instalado)
pytest tests/test_metric_card.py -v

# Sin pytest
python tests/test_metric_card_simple.py
```

## Documentación

- **Guía completa**: `/Users/daniel/mi_app_finanzas/docs/METRIC_CARD_USAGE.md`
- **Estrategia de diseño**: `/Users/daniel/mi_app_finanzas/docs/ESTRATEGIA_OVERHAUL_DISEÑO.md` (Sección 4.2.1)
- **Design tokens**: `/Users/daniel/mi_app_finanzas/utils/design_tokens.py`

## API Reference

### render_metric_card()

```python
render_metric_card(
    title: str,                          # Título de la métrica
    value: Union[float, str],            # Valor principal
    delta: Optional[Union[float, str]],  # Delta vs período anterior
    icon: Optional[str],                 # Emoji decorativo
    color: Literal[...],                 # success|danger|info|warning|neutral
    trend: Optional[Literal[...]],       # up|down|neutral
    format_type: Literal[...],           # currency|percent|number|text
    help_text: Optional[str],            # Texto de ayuda
    show_border: bool = True,            # Barra decorativa superior
    glassmorphism: bool = False          # Efecto glassmorphism
) -> None
```

### Helper Functions

- `metric_card_success()`: Variante verde
- `metric_card_danger()`: Variante roja
- `metric_card_info()`: Variante azul
- `metric_card_warning()`: Variante naranja
- `metric_card_neutral()`: Variante gris

### Layout Functions

- `render_metric_row(metrics: list[dict])`: Fila horizontal
- `render_metric_grid(metrics: list[dict], columns_desktop: int)`: Grid responsive

## Variantes de Color

| Color | Uso | Gradiente | Base Color |
|-------|-----|-----------|------------|
| success | Ingresos, positivo | Verde oscuro → Lima | #26a69a |
| danger | Gastos, negativo | Rosa coral → Amarillo | #ef5350 |
| info | Información | Azul cielo → Cyan | #1f77b4 |
| warning | Advertencias | Dorado → Coral | #ff9800 |
| neutral | Datos generales | Verde oscuro → Lima (sutil) | #757575 |

## Formatos

| Format | Input | Output | Uso |
|--------|-------|--------|-----|
| currency | 1234.56 | 1.234,56 € | Moneda europea |
| percent | 28.5 | 28.5% | Porcentajes |
| number | 12345 | 1.234 | Números enteros |
| text | "Custom" | Custom | Sin formato |

## Iconos Recomendados

```python
"💰"  # Ingresos
"💸"  # Gastos
"⚖️"  # Balance
"📊"  # Estadísticas
"📈"  # Tendencia positiva
"📉"  # Tendencia negativa
"🎯"  # Objetivos
"⚡"  # Alertas
"📅"  # Tiempo
"📋"  # Transacciones
"💯"  # Puntuaciones
```

## Ejemplos de Uso Real

### Dashboard Mensual

```python
render_metric_row([
    {
        "title": "Total Ingresos",
        "value": 2500.00,
        "delta": 5.2,
        "icon": "💰",
        "color": "success",
        "trend": "up"
    },
    {
        "title": "Total Gastos",
        "value": 1850.50,
        "delta": -3.1,
        "icon": "💸",
        "color": "danger",
        "trend": "down"
    },
    {
        "title": "Balance",
        "value": 649.50,
        "delta": 12.8,
        "icon": "⚖️",
        "color": "info",
        "trend": "up"
    }
])
```

### Métricas Avanzadas

```python
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card_info("Tasa Ahorro", 26.0, format_type="percent", icon="🎯")

with col2:
    metric_card_neutral("Gasto/Día", 61.68, icon="📅")

with col3:
    metric_card_info("Transacciones", 87, format_type="number", icon="📋")

with col4:
    metric_card_success("Health Score", 85, format_type="number", icon="💯")
```

## Integración con Feature Flags

```python
from utils.feature_flags import FeatureFlags

if FeatureFlags.USE_NEW_METRIC_CARDS:
    render_metric_card("Balance", 700.50, color="success")
else:
    st.metric("Balance", "700.50 €")
```

## Best Practices

1. **Consistencia de iconos**: Usa el mismo icono para el mismo tipo de métrica
2. **Colores semánticos**: success para positivo, danger para negativo
3. **Help text**: Añade explicaciones para métricas complejas
4. **Layout automático**: Usa `render_metric_row()` en lugar de columns manuales
5. **Deltas informativos**: Muestra cambios temporales con delta y trend

## Troubleshooting

**Error: ModuleNotFoundError**
```python
# Solución: importar con ruta completa
from utils.components.metric_card import render_metric_card
```

**Las métricas no se ven bien en móvil**
```python
# Solución: usar layouts automáticos
render_metric_row([...])  # En lugar de st.columns()
```

## Changelog

### v1.0 (2025-12-04)
- ✅ Implementación inicial
- ✅ 5 variantes de color
- ✅ 4 tipos de formato
- ✅ Efectos glassmorphism
- ✅ Layouts responsive
- ✅ Integración con design_tokens.py
- ✅ Tests completos
- ✅ Documentación completa
- ✅ Demo interactiva

## Autor

Daniel - 2025-12-04

## Referencias

- Design tokens: `/Users/daniel/mi_app_finanzas/utils/design_tokens.py`
- Estrategia: `/Users/daniel/mi_app_finanzas/docs/ESTRATEGIA_OVERHAUL_DISEÑO.md`
- Material Design 3: https://m3.material.io/
