# Grid System - Guía de Migración

Guía práctica para migrar código existente que usa `st.columns()` al nuevo Grid System.

## Por qué Migrar?

### Antes (st.columns)
```python
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Ingresos", "2,500€", "+15%")

with col2:
    st.metric("Gastos", "1,800€", "-5%")

with col3:
    st.metric("Balance", "700€", "+10%")

with col4:
    st.metric("Ahorro", "28%", "+3%")
```

**Problemas:**
- ❌ No responsive (4 columnas fijas en mobile)
- ❌ Código repetitivo (4x `with col:`)
- ❌ Difícil de mantener con muchos items
- ❌ No reutilizable
- ❌ Gaps inconsistentes

### Después (Grid System)
```python
from utils.components import render_metric_grid

metrics = [
    {"label": "Ingresos", "value": "2,500€", "delta": "+15%"},
    {"label": "Gastos", "value": "1,800€", "delta": "-5%"},
    {"label": "Balance", "value": "700€", "delta": "+10%"},
    {"label": "Ahorro", "value": "28%", "delta": "+3%"}
]

render_metric_grid(metrics, cols=4, gap='lg')
```

**Ventajas:**
- ✅ Responsive automático (1 col en mobile)
- ✅ Código declarativo y limpio
- ✅ Fácil de mantener
- ✅ Reutilizable
- ✅ Gaps consistentes con design tokens

---

## Patrones de Migración

### 1. st.columns() → render_grid()

**Antes:**
```python
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Card 1")
    st.write("Contenido 1")

with col2:
    st.markdown("### Card 2")
    st.write("Contenido 2")

with col3:
    st.markdown("### Card 3")
    st.write("Contenido 3")
```

**Después:**
```python
from utils.components import render_grid

def render_card(data, idx):
    st.markdown(f"### {data['title']}")
    st.write(data['content'])

cards = [
    {"title": "Card 1", "content": "Contenido 1"},
    {"title": "Card 2", "content": "Contenido 2"},
    {"title": "Card 3", "content": "Contenido 3"}
]

render_grid(cards, cols=3, gap='lg', item_renderer=render_card)
```

---

### 2. Métricas → render_metric_grid()

**Antes:**
```python
cols = st.columns(4)

metrics = [
    ("Ingresos", "2,500€", "+15%"),
    ("Gastos", "1,800€", "-5%"),
    ("Balance", "700€", "+10%"),
    ("Ahorro", "28%", "+3%")
]

for col, (label, value, delta) in zip(cols, metrics):
    with col:
        st.metric(label, value, delta)
```

**Después:**
```python
from utils.components import render_metric_grid

metrics = [
    {"label": "Ingresos", "value": "2,500€", "delta": "+15%"},
    {"label": "Gastos", "value": "1,800€", "delta": "-5%"},
    {"label": "Balance", "value": "700€", "delta": "+10%"},
    {"label": "Ahorro", "value": "28%", "delta": "+3%"}
]

render_metric_grid(metrics, cols=4, gap='md')
```

---

### 3. Cards con estilo → render_card_grid()

**Antes:**
```python
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="border: 1px solid #ddd; padding: 1rem; border-radius: 8px;">
        <h3>FIJOS</h3>
        <p style="font-size: 2rem;">850€</p>
        <p>35% del total</p>
    </div>
    """, unsafe_allow_html=True)

# ... repetir para col2 y col3
```

**Después:**
```python
from utils.components import render_card_grid
from utils.design_tokens import Colors

cards = [
    {"title": "FIJOS", "content": "850€", "footer": "35% del total", "color": Colors.PRIMARY},
    {"title": "DISFRUTE", "content": "720€", "footer": "30% del total", "color": Colors.SUCCESS},
    {"title": "EXTRAORDINARIOS", "content": "230€", "footer": "10% del total", "color": Colors.WARNING}
]

render_card_grid(cards, cols=3, gap='lg')
```

---

### 4. Gráficos → render_grid() con renderer

**Antes:**
```python
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Gastos")
    fig1 = create_pie_chart()
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Evolución Mensual")
    fig2 = create_line_chart()
    st.plotly_chart(fig2, use_container_width=True)
```

**Después:**
```python
from utils.components import render_grid

def render_chart(chart_data, idx):
    st.subheader(chart_data["title"])
    st.plotly_chart(chart_data["fig"], use_container_width=True)

charts = [
    {"title": "Distribución de Gastos", "fig": create_pie_chart()},
    {"title": "Evolución Mensual", "fig": create_line_chart()}
]

render_grid(charts, cols=2, gap='xl', item_renderer=render_chart)
```

---

### 5. Número Variable de Columnas → auto_grid()

**Antes:**
```python
# Problema: Número fijo de columnas no se adapta bien
items = get_items()  # Puede tener 3, 5, 7, 10 items...

# Solución fea con st.columns
num_cols = min(len(items), 4)  # Max 4 cols
cols = st.columns(num_cols)

for idx, item in enumerate(items):
    col_idx = idx % num_cols
    with cols[col_idx]:
        render_item(item)
```

**Después:**
```python
from utils.components import auto_grid

items = get_items()  # Cualquier número de items

def render_item_func(item, idx):
    st.markdown(f"### {item['title']}")
    st.write(item['content'])

# Se ajusta automáticamente según espacio disponible
auto_grid(items, min_width='280px', gap='md', item_renderer=render_item_func)
```

---

## Migración Paso a Paso

### Ejemplo Real: Dashboard de app.py

**Estado Actual (app.py líneas ~200-250):**
```python
# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Ingresos",
        value=f"{datos_mes['total_ingresos']:,.2f}€",
        delta=f"{variacion_ingresos:+.1f}%"
    )

with col2:
    st.metric(
        label="Total Gastos",
        value=f"{abs(datos_mes['total_gastos']):,.2f}€",
        delta=f"{variacion_gastos:.1f}%",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="Balance",
        value=f"{datos_mes['balance_mes']:,.2f}€",
        delta=f"{variacion_balance:+.1f}%"
    )

with col4:
    ahorro = datos_mes['tasa_ahorro']
    st.metric(
        label="Tasa de Ahorro",
        value=f"{ahorro:.1f}%",
        delta=f"{variacion_ahorro:+.1f}%"
    )
```

**Migración - Paso 1: Preparar datos**
```python
# Extraer la lógica de construcción de métricas
def preparar_metricas_principales(datos_mes, variaciones):
    """Prepara las métricas principales del dashboard"""
    return [
        {
            "label": "Total Ingresos",
            "value": f"{datos_mes['total_ingresos']:,.2f}€",
            "delta": f"{variaciones['ingresos']:+.1f}%",
            "help": "Total de ingresos del mes actual"
        },
        {
            "label": "Total Gastos",
            "value": f"{abs(datos_mes['total_gastos']):,.2f}€",
            "delta": f"{variaciones['gastos']:.1f}%",
            "delta_color": "inverse",
            "help": "Total de gastos del mes actual"
        },
        {
            "label": "Balance",
            "value": f"{datos_mes['balance_mes']:,.2f}€",
            "delta": f"{variaciones['balance']:+.1f}%",
            "help": "Diferencia entre ingresos y gastos"
        },
        {
            "label": "Tasa de Ahorro",
            "value": f"{datos_mes['tasa_ahorro']:.1f}%",
            "delta": f"{variaciones['ahorro']:+.1f}%",
            "help": "Porcentaje de ingresos ahorrados"
        }
    ]
```

**Migración - Paso 2: Usar Grid System**
```python
from utils.components import render_metric_grid

# Preparar datos
variaciones = calcular_variaciones(mes_actual, mes_anterior)
metricas = preparar_metricas_principales(datos_mes, variaciones)

# Renderizar con Grid System
render_metric_grid(metricas, cols=4, gap='lg')
```

**Resultado:**
- ✅ Menos código (de 40 líneas a 15)
- ✅ Más mantenible (datos separados de presentación)
- ✅ Responsive automático
- ✅ Reutilizable en otras páginas

---

## Checklist de Migración

Para cada uso de `st.columns()`, evalúa:

### ¿Debo migrar?
- [ ] Hay más de 2 items en las columnas
- [ ] El contenido es similar entre columnas
- [ ] Necesito que sea responsive
- [ ] Quiero gaps consistentes
- [ ] Planeo reutilizar este patrón

Si marcaste 3+ items → **Migrar**

### ¿Qué función usar?

**Decisión:**
- `st.metric()` en columnas → `render_metric_grid()`
- Cards similares → `render_card_grid()`
- Contenido custom pero similar → `render_grid()` con renderer
- Número variable de items → `auto_grid()`
- Heights muy diferentes → `render_masonry_grid()`
- Imágenes → `render_image_grid()`

### Pasos de migración:
1. [ ] Identificar el patrón actual (métricas, cards, custom)
2. [ ] Extraer datos a una lista de diccionarios
3. [ ] Elegir la función de Grid System apropiada
4. [ ] Crear renderer si es necesario
5. [ ] Testear en desktop y mobile
6. [ ] Verificar gaps y spacing
7. [ ] Commit con mensaje claro

---

## Compatibilidad Temporal

Durante la migración, ambos sistemas pueden coexistir:

```python
from utils.feature_flags import FeatureFlags

if FeatureFlags.USE_NEW_GRID_SYSTEM:
    # Nueva implementación con Grid System
    from utils.components import render_metric_grid
    render_metric_grid(metrics, cols=4)
else:
    # Implementación legacy con st.columns
    col1, col2, col3, col4 = st.columns(4)
    # ... código viejo
```

Esto permite:
- Rollback instantáneo si hay problemas
- Testing A/B
- Migración gradual página por página

---

## Casos Especiales

### Caso 1: Columnas con Anchos Diferentes

**Antes:**
```python
col1, col2 = st.columns([2, 1])  # 2/3 y 1/3
```

**Después:**
No hay equivalente directo en Grid System para proporciones.
**Opción 1:** Usar colspan en CSS Grid (requiere HTML custom)
**Opción 2:** Mantener st.columns() para este caso
**Opción 3:** Rediseñar usando columnas iguales

### Caso 2: Contenido Muy Heterogéneo

Si cada columna tiene contenido completamente diferente:
```python
col1, col2 = st.columns(2)

with col1:
    st.metric("Métrica", "100")
    st.plotly_chart(fig)
    st.dataframe(df)

with col2:
    st.form("my_form")
    # ... form fields
```

**Recomendación:** Mantener `st.columns()` en este caso.
Grid System es mejor cuando los items son similares en estructura.

### Caso 3: Nested Columns

**Antes:**
```python
col1, col2 = st.columns(2)

with col1:
    subcol1, subcol2 = st.columns(2)
    # ...
```

**Después:**
Grid System soporta nesting, pero evalúa si es realmente necesario.
Muchas veces un solo nivel con más columnas es más simple.

---

## Testing Post-Migración

Después de migrar, verifica:

### Desktop
- [ ] Número correcto de columnas
- [ ] Gaps consistentes
- [ ] Alineación correcta
- [ ] Sin overflow horizontal

### Tablet
- [ ] Se reduce a 2 columnas (o menos)
- [ ] Contenido legible
- [ ] Gaps apropiados

### Mobile
- [ ] Se reduce a 1 columna
- [ ] Scroll vertical funciona
- [ ] Touch targets suficientemente grandes
- [ ] Sin zoom out involuntario

---

## Ayuda y Soporte

### Recursos
- [README completo](README_GRID_SYSTEM.md)
- [Quick Start](QUICK_START_GRID_SYSTEM.md)
- [Ejemplos interactivos](grid_system_examples.py)
- [Integración con componentes](GRID_INTEGRATION_EXAMPLES.md)

### Comandos Útiles
```bash
# Ver ejemplos
streamlit run utils/components/grid_system_examples.py

# Ejecutar tests
python utils/components/grid_system_test.py

# Verificar imports
python -c "from utils.components import render_grid; print('OK')"
```

---

## Roadmap de Migración Sugerido

### Fase 1: Páginas Simples (1-2 días)
- [ ] Dashboard - Métricas principales
- [ ] Dashboard - Cards de categorías

### Fase 2: Páginas Complejas (2-3 días)
- [ ] Transacciones - Vista de lista
- [ ] Categorías - Grid de categorías
- [ ] Importar - Vista previa

### Fase 3: Nuevas Features (1 día)
- [ ] Usar Grid System en nuevos desarrollos
- [ ] Establecer como estándar del proyecto

**Total estimado:** 4-6 días de migración gradual

---

**Última actualización:** 2025-12-04
**Versión:** 1.0.0
