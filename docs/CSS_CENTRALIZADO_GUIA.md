# Guía del Sistema CSS Centralizado

## Descripción General

El CSS de la aplicación ha sido completamente refactorizado y centralizado en el módulo `utils/styles.py`. Esta guía explica cómo usar el nuevo sistema.

## Estructura

```
utils/
├── styles.py              # Módulo CSS centralizado (NUEVO)
├── design_tokens.py       # Tokens de diseño (colores, tipografía, etc)
└── brand_assets.py        # Assets de marca (logos, etc)
```

## Uso Básico

### 1. Inyectar Estilos Globales

En `app.py`, después de `st.set_page_config()`:

```python
from utils.styles import inject_global_styles

# Configuración de la página
st.set_page_config(
    page_title="Mi App",
    page_icon="💰",
    layout="wide"
)

# Inyectar estilos globales (UNA SOLA VEZ)
inject_global_styles()
```

### 2. CSS Personalizado Adicional

Si necesitas CSS adicional específico para una página:

```python
from utils.styles import inject_custom_css

inject_custom_css('''
    .mi-clase-custom {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
    }
''')
```

### 3. Componentes HTML Reutilizables

#### Métrica Premium

```python
from utils.styles import ComponentStyles

# Crear métrica con estilo premium
metric_html = ComponentStyles.metric_card(
    title="Balance Total",
    value="2,450.50 €",
    delta="+15.5% vs mes anterior",
    icon="💰"
)

st.markdown(metric_html, unsafe_allow_html=True)
```

#### Caja Informativa

```python
from utils.styles import ComponentStyles

# Caja de información
info_html = ComponentStyles.info_box(
    content="<strong>Tip:</strong> Revisa tus gastos fijos cada trimestre.",
    style="info"  # Opciones: info, success, warning, error
)

st.markdown(info_html, unsafe_allow_html=True)
```

## Organización del CSS

El CSS está organizado en 16 secciones semánticas:

### 1. Reset y Base Styles
- Prevención de scroll horizontal
- Fondo global con gradiente
- Container principal

### 2. Typography System
- Font family global
- Headings (h1, h2, h3)
- Text rendering optimizado

### 3. Components - Cards
- Glassmorphism effects
- Hover states
- Transiciones suaves

### 4. Components - Metrics
- Métricas con barra superior
- Valores con gradiente
- Hover effects

### 5. Components - Buttons
- Primary buttons con gradiente
- Secondary buttons
- Ripple effects

### 6. Components - Forms & Inputs
- Text inputs
- Select boxes
- Focus states

### 7. Components - Tabs
- Tab list container
- Active tab styles
- Hover effects

### 8. Components - Tables
- DataFrames
- Header gradientes
- Row hover

### 9. Components - Charts
- Plotly charts
- Glass effects
- Hover animations

### 10. Components - Alerts
- Success, error, warning, info
- Border accents
- Backdrop blur

### 11. Components - Modals
- Dialog glassmorphism
- Premium shadows

### 12. Layout - Sidebar
- Sidebar premium
- Radio buttons custom
- Indicador visual

### 13. Animations
- fadeInUp
- pulse
- shimmer

### 14. Special Effects
- Custom scrollbar
- Text selection
- Smooth scroll

### 15. Utility Classes
- `.premium-glass`
- `.premium-gradient`
- `.premium-shadow`
- `.premium-card`

### 16. Responsive Design
- Tablet breakpoint (768px)
- Mobile breakpoint (480px)
- Touch-friendly

## Design Tokens

Todos los valores CSS usan tokens centralizados de `design_tokens.py`:

```python
from utils.design_tokens import Colors, Typography, Spacing, BorderRadius

# Colores
Colors.PREMIUM_PRIMARY_START      # Verde esmeralda
Colors.PREMIUM_GRADIENT_PRIMARY   # Gradiente principal
Colors.GRAY_900                   # Texto oscuro

# Tipografía
Typography.FONT_PRIMARY           # 'Inter', sans-serif
Typography.TEXT_4XL               # 2.25rem
Typography.WEIGHT_BOLD            # 700

# Espaciado
Spacing.SM                        # 0.5rem
Spacing.BASE                      # 1rem
Spacing.XL                        # 2rem

# Border radius
BorderRadius.MD                   # 0.5rem
BorderRadius.LG                   # 0.75rem
BorderRadius.FULL                 # 9999px
```

## Utility Classes CSS

Puedes usar estas clases en cualquier HTML personalizado:

```html
<!-- Glassmorphism -->
<div class="premium-glass">
    Contenido con efecto glass
</div>

<!-- Gradiente premium -->
<div class="premium-gradient">
    Texto con gradiente de fondo
</div>

<!-- Sombra premium -->
<div class="premium-shadow">
    Elemento con sombra elevada
</div>

<!-- Card premium -->
<div class="premium-card">
    Card con todos los efectos
</div>
```

## Mejoras Aplicadas

### ✅ Antes de la Refactorización
- 2,558 líneas en app.py
- CSS disperso en múltiples `st.markdown()` inline
- ~535 líneas de CSS mezcladas con lógica
- Difícil de mantener
- CSS duplicado
- Sin organización clara

### ✅ Después de la Refactorización
- 2,029 líneas en app.py (529 líneas menos)
- CSS centralizado en `utils/styles.py`
- Una sola llamada: `inject_global_styles()`
- Organizado en 16 secciones
- Sin duplicados
- Fácil de mantener
- Comentarios descriptivos
- Utility classes reutilizables

## Ventajas del Nuevo Sistema

### 🎯 Mantenibilidad
- Todo el CSS en un solo lugar
- Fácil de actualizar colores/estilos globales
- Cambios se propagan automáticamente

### 🔄 Reutilización
- Design tokens consistentes
- Utility classes
- Componentes HTML predefinidos

### 📱 Responsive
- Mobile-first approach
- Breakpoints organizados
- Touch-friendly en mobile

### 🎨 Consistencia
- Todos los componentes usan los mismos tokens
- Transiciones uniformes
- Spacing consistente

### 🚀 Performance
- CSS se carga una sola vez
- No hay múltiples inyecciones inline
- Mejor cacheo del navegador

## Ejemplos de Uso

### Ejemplo 1: Página con Estilos Globales

```python
import streamlit as st
from utils.styles import inject_global_styles

st.set_page_config(page_title="Mi Página", layout="wide")
inject_global_styles()

# Todos los componentes de Streamlit ya tienen estilos
st.title("Mi Dashboard")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Ingresos", "2,500 €", delta="+15%")

with col2:
    st.metric("Gastos", "1,800 €", delta="-5%")

with col3:
    st.metric("Ahorro", "700 €", delta="+28%")
```

### Ejemplo 2: Card Personalizada con Utility Classes

```python
import streamlit as st
from utils.styles import inject_global_styles

inject_global_styles()

custom_card = """
<div class="premium-card" style="text-align: center;">
    <h3 style="margin-bottom: 1rem;">🎯 Objetivo del Mes</h3>
    <div style="font-size: 3rem; font-weight: 800;">
        500 €
    </div>
    <p style="color: #64748b; margin-top: 1rem;">
        Ahorro planificado
    </p>
</div>
"""

st.markdown(custom_card, unsafe_allow_html=True)
```

### Ejemplo 3: Alerta Custom

```python
from utils.styles import ComponentStyles

success_box = ComponentStyles.info_box(
    content="""
    <strong>✅ Objetivo Alcanzado!</strong><br>
    Has superado tu meta de ahorro este mes.
    """,
    style="success"
)

st.markdown(success_box, unsafe_allow_html=True)
```

## Troubleshooting

### Los estilos no se aplican

1. Verifica que `inject_global_styles()` se llame DESPUÉS de `st.set_page_config()`
2. Asegúrate de que se llame solo UNA vez
3. Verifica que `utils/styles.py` esté correctamente importado

### Necesito añadir estilos específicos

Usa `inject_custom_css()` para CSS adicional sin modificar el módulo central:

```python
from utils.styles import inject_custom_css

inject_custom_css('''
    .mi-componente-especial {
        /* tus estilos aquí */
    }
''')
```

### Quiero cambiar un color global

Modifica `utils/design_tokens.py` para cambios globales, o usa CSS custom para overrides locales.

## Próximos Pasos

1. **Themes**: Implementar soporte para dark mode
2. **More Components**: Añadir más componentes HTML reutilizables
3. **CSS Variables**: Migrar a CSS custom properties nativas
4. **Animations**: Añadir más animaciones y micro-interacciones

## Referencias

- [Estrategia de Diseño](./ESTRATEGIA_OVERHAUL_DISEÑO.md)
- [Design Tokens](../utils/design_tokens.py)
- [Módulo de Estilos](../utils/styles.py)
