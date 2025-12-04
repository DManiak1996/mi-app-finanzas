# Estrategia de Overhaul Completo del Diseño
## Sin Romper la Funcionalidad Existente

**Fecha**: 2025-12-04
**Versión**: 1.0
**App**: FinanzasFlow - Gestión de Finanzas Personales
**Target**: Desktop-first (móvil secundario)

---

## Tabla de Contenidos

1. [Análisis del Estado Actual](#1-análisis-del-estado-actual)
2. [Estrategia de Migración Segura](#2-estrategia-de-migración-segura)
3. [Arquitectura de Componentes Propuesta](#3-arquitectura-de-componentes-propuesta)
4. [Plan de Implementación por Fases](#4-plan-de-implementación-por-fases)
5. [Testing y Validación](#5-testing-y-validación)
6. [Puntos de Rollback](#6-puntos-de-rollback)
7. [Código de Ejemplo](#7-código-de-ejemplo)
8. [Checklist de Implementación](#8-checklist-de-implementación)

---

## 1. Análisis del Estado Actual

### 1.1 Inventario de Código

**Estadísticas del proyecto:**
```
Total líneas Python:  ~9,546 líneas
app.py principal:     2,558 líneas (419 llamadas st.*)
Páginas adicionales:  2 archivos (coche_electrico, asistente_ia)
Utilidades:           11 módulos en utils/
Design tokens:        ✅ YA implementado (382 líneas)
CSS inyectado:        ~400 líneas en app.py
```

**Estructura de páginas (app.py):**
```python
# 7 páginas funcionales detectadas:
- mostrar_dashboard()         # 700+ líneas - Dashboard principal
- mostrar_añadir_gasto()      # 150+ líneas - Formulario de gastos
- mostrar_transacciones()     # 150+ líneas - Tabla editable
- mostrar_importar()          # 100+ líneas - Upload Excel
- mostrar_categorias()        # 80+ líneas - Gestión de reglas
- mostrar_sincronizacion()    # 250+ líneas - Sync Mac<>Cloud
- mostrar_configuracion()     # 270+ líneas - Settings

# 2 páginas adicionales:
- pages_coche_electrico.py    # 183 llamadas st.* - Módulo coche
- pages_asistente_ia.py       # 23 llamadas st.* - Chatbot IA
```

### 1.2 Componentes UI Utilizados

**Análisis de uso de Streamlit:**
```python
# Componentes más usados (frecuencia estimada):
st.metric()           # ~15 usos - Métricas financieras
st.plotly_chart()     # ~10 usos - Gráficos Plotly
st.dataframe()        # ~8 usos - Tablas de datos
st.form() / st.button() # ~20 usos - Formularios
st.columns()          # ~30 usos - Layouts
st.tabs()             # ~8 usos - Pestañas
st.expander()         # ~10 usos - Acordeones
st.dialog()           # 2 usos - Modals (desglose, reembolsos)
st.selectbox()        # ~15 usos - Selectores
st.number_input()     # ~10 usos - Inputs numéricos
```

**Patrones de diseño actuales:**
- ✅ **Design Tokens**: Colores, tipografía, spacing centralizados
- ✅ **CSS Premium**: Glassmorphism, gradientes, sombras multicapa
- ✅ **Brand Assets**: Logo SVG, iconos vectoriales
- ⚠️ **Inline CSS**: ~400 líneas inyectadas en app.py (dificulta mantenimiento)
- ❌ **Componentes reutilizables**: Ausentes (código duplicado)
- ❌ **Templates de visualización**: Parcialmente en visualizer.py

### 1.3 Estado del Design System

**Lo que YA funciona bien:**

```python
# utils/design_tokens.py - Sistema robusto
class Colors:
    # Paleta premium verde oscuro → lima
    PREMIUM_PRIMARY_START = "#0a4c3e"
    PREMIUM_PRIMARY_END = "#84cc16"
    PREMIUM_GRADIENT_PRIMARY = "linear-gradient(...)"

    # Sombras multicapa para profundidad
    SHADOW_PREMIUM_MD = "0 4px 6px rgba(...)"

    # Colores semánticos financieros
    CHART_INCOME = SUCCESS  # Verde
    CHART_EXPENSE = ERROR   # Rojo
    BUDGET_OK/WARNING/OVER  # Verde/Naranja/Rojo

class Typography:
    FONT_PRIMARY = "'Inter', ..."
    TEXT_BASE = "1rem"
    WEIGHT_SEMIBOLD = "600"

class Spacing:
    BASE = "1rem"  # 16px
    LG = "1.5rem"  # 24px (8pt grid)

class BorderRadius:
    BASE = "0.5rem"  # 8px
    LG = "1rem"      # 16px

class Transitions:
    BASE = "250ms"
    EASING_DEFAULT = "cubic-bezier(0.4, 0, 0.2, 1)"
```

**Lo que necesita mejora:**

1. **CSS disperso**: 400 líneas en app.py deben moverse a módulo
2. **Sin componentes wrapper**: Cada `st.metric()` se estiliza manualmente
3. **Visualizaciones inconsistentes**: Colores Plotly no usan design tokens
4. **No hay sistema de layouts**: Cada página crea su propio layout
5. **Sin gestión de temas**: Hard-coded para light mode

### 1.4 Puntos de Riesgo Identificados

**🚨 ALTO RIESGO - No tocar sin backup:**
```python
# database/db_manager.py
- Base de datos SQLite con datos reales del usuario
- 38 reglas de auto-categorización (utils/categorizer.py)
- Lógica de sincronización Mac<>Cloud (mostrar_sincronizacion)
- Sistema de autenticación (auth_simple.py)
```

**⚠️ MEDIO RIESGO - Refactorizar con cuidado:**
```python
# Lógica de negocio mezclada con presentación
- mostrar_dashboard() - 700+ líneas con cálculos inline
- utils/metrics.py - Funciones usadas en múltiples lugares
- Formularios con validación custom
```

**✅ BAJO RIESGO - Seguro para cambiar:**
```python
# Presentación pura (sin lógica)
- CSS y estilos (toda la sección de st.markdown("""<style>"""))
- Layouts con st.columns() / st.tabs()
- Textos de ayuda (help=) y labels
- Iconos y emojis
```

---

## 2. Estrategia de Migración Segura

### 2.1 Principios de Migración

**REGLA DE ORO: Cambios incrementales y reversibles**

```
┌─────────────────────────────────────────────────┐
│  NUNCA cambiar lógica y diseño al mismo tiempo  │
│  Separar: Refactoring → Styling → Testing       │
└─────────────────────────────────────────────────┘
```

**Principios clave:**

1. **Backward Compatibility First**
   - Nuevo código debe coexistir con el viejo
   - Feature flags para activar/desactivar
   - Gradual rollout (página por página)

2. **Test Before Change**
   - Capturar comportamiento actual como test
   - Verificar output antes y después
   - Screenshots para comparación visual

3. **Isolate UI from Logic**
   - Extraer lógica de negocio primero
   - Después cambiar solo presentación
   - Nunca mezclar ambos en un commit

4. **Version Control Aggressive**
   - Branch por cada fase
   - Commits pequeños y atómicos
   - Tags en puntos de rollback seguros

### 2.2 Estrategia de Coexistencia

**Fase de Transición: Old vs New**

```python
# utils/feature_flags.py (CREAR PRIMERO)
"""
Sistema de feature flags para habilitar diseño nuevo gradualmente
"""

class FeatureFlags:
    """Control de características en desarrollo"""

    # FASE 1: Design System
    USE_NEW_COMPONENTS = False      # Componentes wrappers
    USE_NEW_CSS_MODULE = False      # CSS extraído de app.py
    USE_NEW_PLOTLY_THEME = False    # Theme Plotly unificado

    # FASE 2: Componentes
    USE_METRIC_CARDS = False        # MetricCard component
    USE_CHART_TEMPLATES = False     # Plantillas de gráficos
    USE_LAYOUT_SYSTEM = False       # Sistema de layouts

    # FASE 3: Páginas
    DASHBOARD_V2 = False            # Dashboard rediseñado
    TRANSACTIONS_V2 = False         # Transacciones rediseñadas

    # FASE 4: Features
    DARK_MODE = False               # Modo oscuro
    RESPONSIVE_MOBILE = False       # Optimizaciones móvil

# Uso en código:
from utils.feature_flags import FeatureFlags

if FeatureFlags.USE_NEW_COMPONENTS:
    # Renderizar con componentes nuevos
    render_metric_card(label, value)
else:
    # Mantener código viejo
    st.metric(label, value)
```

**Ventajas:**
- ✅ Código nuevo y viejo conviven
- ✅ Rollback instantáneo (cambiar flag)
- ✅ Testing A/B posible
- ✅ Migración gradual por página

### 2.3 Orden de Migración (Modelo Cascada Inverso)

```
FASE 0: Preparación
├── Crear feature_flags.py
├── Extraer CSS a module
└── Setup testing framework

FASE 1: Fundamentos (No afecta UI)
├── 1.1 Extractar lógica de negocio
├── 1.2 Crear componentes base
└── 1.3 Unified Plotly theme

FASE 2: Componentes (UI aislada)
├── 2.1 MetricCard component
├── 2.2 ChartContainer component
├── 2.3 FormCard component
└── 2.4 DataTable component

FASE 3: Layouts (Reorganización)
├── 3.1 PageLayout system
├── 3.2 Grid system
└── 3.3 Responsive utilities

FASE 4: Páginas (Una a una)
├── 4.1 Dashboard v2
├── 4.2 Transacciones v2
├── 4.3 Importar v2
├── 4.4 Categorías v2
├── 4.5 Configuración v2
├── 4.6 Coche Eléctrico v2
└── 4.7 Asistente IA v2

FASE 5: Polish (Opcional)
├── 5.1 Dark mode
├── 5.2 Mobile optimizations
├── 5.3 Animaciones
└── 5.4 Accesibilidad
```

**Duración estimada:**
- Fase 0: 2 horas
- Fase 1: 1 día (8 horas)
- Fase 2: 2 días (16 horas)
- Fase 3: 1 día (8 horas)
- Fase 4: 3 días (24 horas)
- Fase 5: 2 días (16 horas)
- **TOTAL: 9 días de trabajo (72 horas)**

### 2.4 Testing Durante Migración

**Testing Strategy: Triple Validation**

```python
# tests/test_design_migration.py
"""
Tests para verificar que el overhaul no rompe funcionalidad
"""

import pytest
from utils.feature_flags import FeatureFlags

class TestVisualRegression:
    """Verificar que UI nueva = UI vieja visualmente"""

    def test_dashboard_metrics_equal(self):
        """Valores de métricas deben ser idénticos"""
        # Capturar métricas con flag OFF
        FeatureFlags.USE_NEW_COMPONENTS = False
        old_metrics = capture_dashboard_metrics()

        # Capturar métricas con flag ON
        FeatureFlags.USE_NEW_COMPONENTS = True
        new_metrics = capture_dashboard_metrics()

        # Comparar
        assert old_metrics == new_metrics

    def test_plotly_charts_render(self):
        """Gráficos deben renderizar sin errores"""
        charts = [
            'distribucion_gastos',
            'evolucion_anual',
            'saldo_temporal'
        ]
        for chart in charts:
            fig = generate_chart(chart)
            assert fig is not None
            assert len(fig.data) > 0

class TestFunctionalEquivalence:
    """Verificar que lógica no cambió"""

    def test_calculate_balance_unchanged(self):
        """Balance debe calcularse igual"""
        from utils.metrics import calcular_totales_mes

        # Usar datos de test conocidos
        result = calcular_totales_mes(mes=10, año=2025)

        # Verificar valores esperados
        assert result['total_ingresos'] == 2500.00
        assert result['total_gastos'] == -1800.00
        assert result['balance_mes'] == 700.00

    def test_categorizer_rules_intact(self):
        """Reglas de categorización no deben cambiar"""
        from utils.categorizer import clasificar_transaccion

        # Test de reglas conocidas
        assert clasificar_transaccion("NETFLIX", -9.99) == ("DISFRUTE", "GASTO")
        assert clasificar_transaccion("VIVAGYM", -35.00) == ("FIJOS", "GASTO")
        assert clasificar_transaccion("NOMINA", 2500.00) == ("INGRESO", "INGRESO")

class TestPerformance:
    """Verificar que rendimiento no degrada"""

    def test_dashboard_loads_under_2s(self):
        """Dashboard debe cargar en <2 segundos"""
        import time

        start = time.time()
        mostrar_dashboard()
        duration = time.time() - start

        assert duration < 2.0, f"Dashboard tardó {duration}s"
```

**Ejecución continua:**
```bash
# Ejecutar antes de cada commit
pytest tests/test_design_migration.py -v

# Ejecutar con coverage
pytest --cov=utils --cov-report=html tests/
```

---

## 3. Arquitectura de Componentes Propuesta

### 3.1 Sistema de Componentes Reutilizables

**Objetivo:** Eliminar duplicación y centralizar estilos

```
utils/
├── components/
│   ├── __init__.py
│   ├── base.py           # Componentes base abstractos
│   ├── metrics.py        # MetricCard, KPICard
│   ├── charts.py         # ChartContainer, ChartLegend
│   ├── forms.py          # FormCard, FormField
│   ├── tables.py         # DataTable, EditableTable
│   ├── layouts.py        # PageLayout, Section, Grid
│   └── feedback.py       # Toast, Alert, LoadingState
│
├── styles/
│   ├── __init__.py
│   ├── css_injector.py   # Función para inyectar CSS global
│   ├── global_styles.py  # CSS extraído de app.py
│   └── theme.py          # Theme manager (light/dark)
│
├── charts/
│   ├── __init__.py
│   ├── plotly_theme.py   # Theme Plotly unificado
│   ├── templates.py      # Plantillas de gráficos
│   └── colors.py         # Paleta de gráficos
│
└── design_tokens.py      # ✅ Ya existe - NO tocar
```

### 3.2 Componentes Core (Prioridad Alta)

#### 3.2.1 MetricCard Component

**Problema actual:** Cada `st.metric()` tiene estilos inline duplicados

**Solución:**
```python
# utils/components/metrics.py
"""
Componentes para métricas financieras estilizadas
"""

import streamlit as st
from utils.design_tokens import Colors, Typography, Spacing, BorderRadius
from typing import Optional, Literal

def MetricCard(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: Literal["normal", "inverse", "off"] = "normal",
    help_text: Optional[str] = None,
    icon: Optional[str] = None,
    trend: Optional[Literal["up", "down", "neutral"]] = None,
    variant: Literal["default", "success", "error", "warning"] = "default",
    show_sparkline: bool = False,
    sparkline_data: Optional[list] = None
):
    """
    Tarjeta de métrica estilizada con diseño premium

    Args:
        label: Etiqueta de la métrica
        value: Valor principal (ej: "2,500.00 €")
        delta: Cambio respecto período anterior
        delta_color: Color del delta
        help_text: Tooltip explicativo
        icon: Emoji o icono decorativo
        trend: Indicador de tendencia visual
        variant: Estilo de la tarjeta (success=verde, error=rojo)
        show_sparkline: Mostrar mini-gráfico de tendencia
        sparkline_data: Datos para sparkline [10, 15, 12, 18, ...]

    Example:
        >>> MetricCard(
        ...     label="Balance del Mes",
        ...     value="700.00 €",
        ...     delta="+15% vs mes anterior",
        ...     icon="⚖️",
        ...     trend="up",
        ...     variant="success",
        ...     help_text="Diferencia entre ingresos y gastos"
        ... )
    """

    # Determinar colores según variante
    gradient_map = {
        "default": Colors.PREMIUM_GRADIENT_PRIMARY,
        "success": Colors.PREMIUM_GRADIENT_TEAL,
        "error": Colors.PREMIUM_GRADIENT_CORAL,
        "warning": Colors.PREMIUM_GRADIENT_GOLD
    }

    border_color_map = {
        "default": "rgba(10, 76, 62, 0.1)",
        "success": "rgba(13, 95, 78, 0.2)",
        "error": "rgba(250, 112, 154, 0.2)",
        "warning": "rgba(246, 211, 101, 0.2)"
    }

    gradient = gradient_map[variant]
    border_color = border_color_map[variant]

    # HTML de la tarjeta
    card_html = f"""
    <div style="
        background: {Colors.PREMIUM_CARD_GRADIENT};
        border-radius: {BorderRadius.LG};
        border: 2px solid {border_color};
        padding: {Spacing.XL};
        box-shadow: {Colors.SHADOW_PREMIUM_MD};
        transition: all 250ms cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    ">
        <!-- Barra superior decorativa -->
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: {gradient};
        "></div>

        <!-- Label con icono -->
        <div style="
            display: flex;
            align-items: center;
            gap: {Spacing.SM};
            margin-bottom: {Spacing.MD};
        ">
            {f'<span style="font-size: {Typography.TEXT_LG};">{icon}</span>' if icon else ''}
            <span style="
                font-size: {Typography.TEXT_SM};
                font-weight: {Typography.WEIGHT_SEMIBOLD};
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: {Colors.GRAY_700};
            ">{label}</span>
        </div>

        <!-- Valor principal -->
        <div style="
            font-size: {Typography.TEXT_5XL};
            font-weight: {Typography.WEIGHT_EXTRABOLD};
            line-height: 1;
            background: {gradient};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: {Spacing.SM};
        ">{value}</div>

        <!-- Delta con tendencia -->
        {f'''
        <div style="
            display: inline-flex;
            align-items: center;
            gap: {Spacing.XS};
            padding: {Spacing.XS} {Spacing.MD};
            border-radius: 999px;
            background: rgba(10, 76, 62, 0.08);
            font-size: {Typography.TEXT_SM};
            font-weight: {Typography.WEIGHT_MEDIUM};
        ">
            {_get_trend_arrow(trend) if trend else ''}
            <span>{delta}</span>
        </div>
        ''' if delta else ''}
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)

    # Agregar tooltip si existe
    if help_text:
        st.caption(f"💡 {help_text}")

def _get_trend_arrow(trend: str) -> str:
    """Helper para obtener flecha de tendencia"""
    arrows = {
        "up": "↗️",
        "down": "↘️",
        "neutral": "➡️"
    }
    return arrows.get(trend, "")


def KPIRow(metrics: list[dict]):
    """
    Fila de KPIs con layout responsive automático

    Args:
        metrics: Lista de diccionarios con parámetros para MetricCard

    Example:
        >>> KPIRow([
        ...     {"label": "Ingresos", "value": "2,500€", "variant": "success"},
        ...     {"label": "Gastos", "value": "1,800€", "variant": "error"},
        ...     {"label": "Balance", "value": "700€", "variant": "default"}
        ... ])
    """
    cols = st.columns(len(metrics))

    for col, metric_config in zip(cols, metrics):
        with col:
            MetricCard(**metric_config)
```

**Ventajas:**
- ✅ Estilos consistentes en toda la app
- ✅ Una sola fuente de verdad para métricas
- ✅ Fácil de cambiar diseño globalmente
- ✅ Menos código duplicado (DRY)

#### 3.2.2 ChartContainer Component

**Problema:** Gráficos Plotly sin estilos consistentes

**Solución:**
```python
# utils/components/charts.py
"""
Container y utilidades para gráficos Plotly
"""

import streamlit as st
import plotly.graph_objects as go
from utils.design_tokens import Colors, BorderRadius, Spacing

def ChartContainer(
    fig: go.Figure,
    title: Optional[str] = None,
    description: Optional[str] = None,
    show_fullscreen: bool = True,
    height: int = 400
):
    """
    Contenedor estilizado para gráficos Plotly

    Args:
        fig: Figura de Plotly
        title: Título del gráfico (opcional)
        description: Descripción breve (opcional)
        show_fullscreen: Botón de pantalla completa
        height: Altura del gráfico en px

    Example:
        >>> fig = px.line(df, x='fecha', y='saldo')
        >>> ChartContainer(
        ...     fig=fig,
        ...     title="Evolución del Saldo",
        ...     description="Saldo después de cada transacción"
        ... )
    """

    # Wrapper con estilos premium
    st.markdown(f"""
    <div style="
        background: {Colors.PREMIUM_CARD_GRADIENT};
        border-radius: {BorderRadius.LG};
        border: 1px solid rgba(10, 76, 62, 0.08);
        padding: {Spacing.LG};
        box-shadow: {Colors.SHADOW_PREMIUM_MD};
        transition: all 250ms;
    ">
    """, unsafe_allow_html=True)

    if title:
        st.markdown(f"### {title}")

    if description:
        st.caption(description)

    # Aplicar theme unificado al gráfico
    from utils.charts.plotly_theme import apply_finanzas_theme
    fig = apply_finanzas_theme(fig)

    # Renderizar
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            'displayModeBar': show_fullscreen,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
        }
    )

    st.markdown("</div>", unsafe_allow_html=True)
```

#### 3.2.3 PageLayout System

**Problema:** Cada página tiene su propio layout inconsistente

**Solución:**
```python
# utils/components/layouts.py
"""
Sistema de layouts consistentes para páginas
"""

import streamlit as st
from typing import Optional, Literal
from utils.design_tokens import Spacing

class PageLayout:
    """Layout manager para páginas completas"""

    @staticmethod
    def render(
        title: str,
        icon: str,
        subtitle: Optional[str] = None,
        show_period_selector: bool = False,
        show_export_button: bool = False
    ):
        """
        Renderiza el header estándar de una página

        Args:
            title: Título de la página
            icon: Emoji decorativo
            subtitle: Subtítulo opcional
            show_period_selector: Mostrar selector mes/año
            show_export_button: Mostrar botón de exportar

        Example:
            >>> PageLayout.render(
            ...     title="Dashboard Financiero",
            ...     icon="📊",
            ...     subtitle="Resumen de tus finanzas",
            ...     show_period_selector=True
            ... )
        """

        # Header con gradiente
        st.markdown(f"""
        <div style="
            background: {Colors.PREMIUM_BG_GRADIENT};
            padding: {Spacing.XL} 0;
            margin-bottom: {Spacing.XXL};
            border-bottom: 1px solid rgba(10, 76, 62, 0.1);
        ">
            <h1>{icon} {title}</h1>
            {f'<p style="color: {Colors.GRAY_600}; font-size: 1.1rem;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)

        # Period selector si se requiere
        if show_period_selector:
            PageLayout._render_period_selector()

        # Export button si se requiere
        if show_export_button:
            PageLayout._render_export_button()

    @staticmethod
    def _render_period_selector():
        """Selector de período (mes/año) consistente"""
        col1, col2, col3 = st.columns([1, 1, 3])

        with col1:
            año = st.selectbox("📅 Año", obtener_años_disponibles())
        with col2:
            mes = st.selectbox("📆 Mes", list(NOMBRES_MESES.values()))
        with col3:
            st.info(f"Mostrando datos de **{mes} {año}**")

        return año, mes

    @staticmethod
    def section(title: str, collapsible: bool = False):
        """
        Crea una sección visual dentro de una página

        Args:
            title: Título de la sección
            collapsible: Si es colapsable (expander)

        Returns:
            Context manager para contenido

        Example:
            >>> with PageLayout.section("Métricas Principales"):
            ...     st.metric("Balance", "700€")
        """
        if collapsible:
            return st.expander(f"### {title}", expanded=True)
        else:
            st.markdown(f"### {title}")
            st.markdown(f'<div style="margin-top: {Spacing.LG};">', unsafe_allow_html=True)
            return _SectionContext()

class _SectionContext:
    """Context manager helper para secciones"""
    def __enter__(self):
        return self
    def __exit__(self, *args):
        st.markdown('</div>', unsafe_allow_html=True)


def Grid(columns: int = 3, gap: str = Spacing.LG):
    """
    Sistema de grid responsive

    Args:
        columns: Número de columnas
        gap: Espacio entre columnas

    Returns:
        Lista de contextos de columnas

    Example:
        >>> cols = Grid(columns=3)
        >>> with cols[0]:
        ...     MetricCard("Ingresos", "2500€")
        >>> with cols[1]:
        ...     MetricCard("Gastos", "1800€")
        >>> with cols[2]:
        ...     MetricCard("Balance", "700€")
    """
    return st.columns(columns, gap=gap)
```

### 3.3 Unified Plotly Theme

**Problema:** Colores de gráficos no usan design tokens

**Solución:**
```python
# utils/charts/plotly_theme.py
"""
Theme unificado de Plotly basado en design tokens
"""

import plotly.graph_objects as go
from utils.design_tokens import Colors, Typography

# Colores para gráficos (orden por uso frecuente)
CHART_COLORS = [
    Colors.PREMIUM_TEAL_START,      # Verde (ingresos, positivo)
    Colors.PREMIUM_CORAL_START,     # Coral (gastos, negativo)
    Colors.PREMIUM_PRIMARY_START,   # Verde oscuro (balance)
    Colors.PREMIUM_GOLD_START,      # Dorado (extraordinarios)
    Colors.PREMIUM_SKY_START,       # Azul (información)
    Colors.ACCENT_TEAL,             # Verde menta
    Colors.ACCENT_CORAL,            # Rosa coral
]

# Template global de Plotly
FINANZAS_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        # Colores de fondo
        plot_bgcolor=Colors.BG_PRIMARY,
        paper_bgcolor='rgba(0,0,0,0)',  # Transparente para card

        # Paleta de colores
        colorway=CHART_COLORS,

        # Tipografía
        font=dict(
            family=Typography.FONT_PRIMARY,
            size=14,
            color=Colors.GRAY_900
        ),

        # Títulos
        title=dict(
            font=dict(
                size=20,
                color=Colors.GRAY_900,
                family=Typography.FONT_PRIMARY
            ),
            x=0.5,
            xanchor='center',
            pad=dict(b=20)
        ),

        # Ejes
        xaxis=dict(
            gridcolor=Colors.GRAY_200,
            linecolor=Colors.GRAY_300,
            zerolinecolor=Colors.GRAY_300,
            title_font=dict(size=14, color=Colors.GRAY_700),
            tickfont=dict(size=12, color=Colors.GRAY_600),
            showgrid=True,
            gridwidth=1
        ),
        yaxis=dict(
            gridcolor=Colors.GRAY_200,
            linecolor=Colors.GRAY_300,
            zerolinecolor=Colors.GRAY_300,
            title_font=dict(size=14, color=Colors.GRAY_700),
            tickfont=dict(size=12, color=Colors.GRAY_600),
            showgrid=True,
            gridwidth=1
        ),

        # Leyenda
        legend=dict(
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor=Colors.GRAY_300,
            borderwidth=1,
            font=dict(size=12, color=Colors.GRAY_700),
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),

        # Tooltips
        hoverlabel=dict(
            bgcolor=Colors.GRAY_900,
            font_size=13,
            font_family=Typography.FONT_PRIMARY,
            font_color='white',
            bordercolor=Colors.PREMIUM_PRIMARY_END
        ),

        # Márgenes
        margin=dict(l=60, r=40, t=80, b=60)
    )
)


def apply_finanzas_theme(fig: go.Figure) -> go.Figure:
    """
    Aplica el theme de FinanzasFlow a una figura Plotly

    Args:
        fig: Figura de Plotly

    Returns:
        Figura con theme aplicado

    Example:
        >>> fig = px.bar(df, x='categoria', y='total')
        >>> fig = apply_finanzas_theme(fig)
        >>> st.plotly_chart(fig)
    """
    fig.update_layout(template=FINANZAS_TEMPLATE)

    # Configuración adicional para interactividad
    fig.update_layout(
        hovermode='closest',
        dragmode='zoom',
        modebar=dict(
            bgcolor='rgba(255,255,255,0.7)',
            color=Colors.GRAY_700,
            activecolor=Colors.PREMIUM_PRIMARY_START
        )
    )

    return fig


# Configurar como template por defecto de Plotly
import plotly.io as pio
pio.templates['finanzas'] = FINANZAS_TEMPLATE
pio.templates.default = 'finanzas'
```

### 3.4 CSS Global Extraído

**Problema:** 400 líneas de CSS inline en app.py

**Solución:**
```python
# utils/styles/global_styles.py
"""
CSS global de la aplicación (extraído de app.py)
"""

from utils.design_tokens import Colors, Typography, Spacing, BorderRadius, Transitions, Config

def get_global_css() -> str:
    """
    Retorna el CSS global de la aplicación

    Returns:
        String con todo el CSS
    """

    return f"""
    <style>
    /* ========== 🎨 FINTECH PREMIUM CSS ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* === FONDO GLOBAL CON GRADIENTE === */
    html, body {{
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }}

    .stApp {{
        background: {Colors.PREMIUM_BG_GRADIENT} !important;
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }}

    .main .block-container {{
        max-width: {Config.MAX_CONTAINER_WIDTH} !important;
        padding-top: {Spacing.XXL} !important;
        overflow-x: hidden !important;
    }}

    /* === SISTEMA TIPOGRÁFICO === */
    html, body, [class*="css"] {{
        font-family: {Typography.FONT_PRIMARY} !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }}

    h1 {{
        font-size: {Typography.TEXT_4XL} !important;
        font-weight: {Typography.WEIGHT_EXTRABOLD} !important;
        line-height: {Typography.LEADING_TIGHT} !important;
        letter-spacing: {Typography.TRACKING_TIGHT} !important;
        color: {Colors.GRAY_900} !important;
        margin-bottom: {Spacing.LG} !important;
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }}

    /* === 💎 CARDS PREMIUM === */
    div[data-testid="column"] > div {{
        background: {Colors.PREMIUM_CARD_GRADIENT} !important;
        border-radius: {BorderRadius.LG} !important;
        padding: {Spacing.LG} !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        border: 1px solid rgba(10, 76, 62, 0.08) !important;
        backdrop-filter: blur(10px) !important;
        transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
    }}

    div[data-testid="column"] > div:hover {{
        transform: translateY(-4px) !important;
        box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
        border-color: rgba(10, 76, 62, 0.15) !important;
    }}

    /* === 🎯 MÉTRICAS PREMIUM === */
    .stMetric {{
        background: {Colors.PREMIUM_CARD_GRADIENT} !important;
        padding: {Spacing.XL} !important;
        border-radius: {BorderRadius.LG} !important;
        border: 1px solid rgba(10, 76, 62, 0.1) !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        backdrop-filter: blur(10px) !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all {Transitions.BASE} {Transitions.EASING_DEFAULT} !important;
    }}

    .stMetric:hover {{
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
        border-color: rgba(10, 76, 62, 0.2) !important;
    }}

    /* === 🔘 BOTONES PREMIUM === */
    .stButton button[kind="primary"] {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        color: white !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        border: none !important;
        font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
        padding: {Spacing.MD} {Spacing.XL} !important;
        border-radius: {BorderRadius.MD} !important;
        transition: all {Transitions.BASE} !important;
    }}

    .stButton button[kind="primary"]:hover {{
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: {Colors.SHADOW_PREMIUM_LG}, {Colors.SHADOW_GLOW_PRIMARY} !important;
    }}

    /* === 📊 GRÁFICOS PREMIUM === */
    .js-plotly-plot {{
        border-radius: {BorderRadius.LG} !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        background: {Colors.PREMIUM_CARD_GRADIENT} !important;
        padding: {Spacing.LG} !important;
        border: 1px solid rgba(10, 76, 62, 0.08) !important;
        backdrop-filter: blur(10px) !important;
        transition: all {Transitions.BASE} !important;
    }}

    .js-plotly-plot:hover {{
        box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
        transform: translateY(-2px) !important;
    }}

    /* === 📝 INPUTS PREMIUM === */
    .stTextInput input, .stNumberInput input, .stSelectbox select {{
        min-height: 48px !important;
        font-size: {Typography.TEXT_BASE} !important;
        border-radius: {BorderRadius.MD} !important;
        border: 2px solid rgba(10, 76, 62, 0.15) !important;
        background: white !important;
        box-shadow: {Colors.SHADOW_PREMIUM_XS} !important;
        transition: all {Transitions.BASE} !important;
    }}

    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: {Colors.PREMIUM_PRIMARY_START} !important;
        box-shadow: 0 0 0 3px rgba(10, 76, 62, 0.1), {Colors.SHADOW_PREMIUM_SM} !important;
        outline: none !important;
    }}

    /* === 🔖 TABS PREMIUM === */
    .stTabs [data-baseweb="tab-list"] {{
        background: white !important;
        border-radius: {BorderRadius.LG} !important;
        padding: {Spacing.SM} !important;
        box-shadow: {Colors.SHADOW_PREMIUM_SM} !important;
        gap: {Spacing.SM} !important;
    }}

    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        color: white !important;
    }}

    /* === 📋 TABLAS PREMIUM === */
    .stDataFrame {{
        border-radius: {BorderRadius.LG} !important;
        overflow: hidden !important;
        box-shadow: {Colors.SHADOW_PREMIUM_MD} !important;
        border: 1px solid rgba(10, 76, 62, 0.08) !important;
    }}

    .stDataFrame thead tr th {{
        background: {Colors.PREMIUM_GRADIENT_PRIMARY} !important;
        color: white !important;
        font-weight: {Typography.WEIGHT_SEMIBOLD} !important;
        text-transform: uppercase !important;
    }}

    /* === 🎪 SIDEBAR PREMIUM === */
    section[data-testid="stSidebar"] {{
        background: {Colors.PREMIUM_CARD_GRADIENT} !important;
        border-right: 1px solid rgba(10, 76, 62, 0.1) !important;
        box-shadow: {Colors.SHADOW_PREMIUM_LG} !important;
    }}

    </style>
    """


# utils/styles/css_injector.py
"""
Inyector de CSS global
"""

import streamlit as st
from utils.styles.global_styles import get_global_css

def inject_global_css():
    """
    Inyecta el CSS global en la aplicación

    Usar al inicio de app.py:
        from utils.styles.css_injector import inject_global_css
        inject_global_css()
    """
    st.markdown(get_global_css(), unsafe_allow_html=True)
```

---

## 4. Plan de Implementación por Fases

### FASE 0: Preparación (2 horas)

**Objetivo:** Setup de infraestructura para migración segura

```bash
# 1. Crear rama de desarrollo
git checkout -b design/overhaul-incremental

# 2. Crear estructura de carpetas
mkdir -p utils/components
mkdir -p utils/styles
mkdir -p utils/charts
mkdir -p tests

# 3. Crear archivos base
touch utils/feature_flags.py
touch utils/styles/global_styles.py
touch utils/styles/css_injector.py
touch utils/charts/plotly_theme.py
```

**Checklist Fase 0:**
- [ ] Rama `design/overhaul-incremental` creada
- [ ] `utils/feature_flags.py` creado con todos los flags en `False`
- [ ] Estructura de carpetas creada
- [ ] Tests básicos escritos (opcional pero recomendado)
- [ ] Backup de base de datos (`cp finanzas.db finanzas.db.backup`)
- [ ] Punto de rollback: `git tag phase-0-complete`

**Código de feature_flags.py:**
```python
# utils/feature_flags.py
"""Feature flags para activar/desactivar nuevas características"""

class FeatureFlags:
    # Fase 1: Fundamentos
    USE_NEW_CSS_MODULE = False
    USE_NEW_PLOTLY_THEME = False

    # Fase 2: Componentes
    USE_METRIC_CARDS = False
    USE_CHART_CONTAINERS = False
    USE_FORM_CARDS = False

    # Fase 3: Layouts
    USE_PAGE_LAYOUTS = False
    USE_GRID_SYSTEM = False

    # Fase 4: Páginas rediseñadas
    DASHBOARD_V2 = False
    TRANSACTIONS_V2 = False

    # Debug
    DEBUG_MODE = False
```

**Testing:**
```bash
# Verificar que la app sigue funcionando
streamlit run app.py

# Verificar que todos los flags están OFF
python -c "from utils.feature_flags import FeatureFlags; print(vars(FeatureFlags))"
```

---

### FASE 1: Fundamentos (1 día - 8 horas)

**Objetivo:** Extraer CSS y crear theme de Plotly SIN cambiar UI

#### 1.1 Extraer CSS Global (2 horas)

```python
# 1. Crear utils/styles/global_styles.py
# (Ver código completo en sección 3.4)

# 2. Crear utils/styles/css_injector.py
from utils.styles.global_styles import get_global_css
import streamlit as st

def inject_global_css():
    st.markdown(get_global_css(), unsafe_allow_html=True)

# 3. Modificar app.py
# ANTES (línea ~240):
st.markdown(f"""
<style>
/* ... 400 líneas de CSS ... */
</style>
""", unsafe_allow_html=True)

# DESPUÉS:
from utils.feature_flags import FeatureFlags
if FeatureFlags.USE_NEW_CSS_MODULE:
    from utils.styles.css_injector import inject_global_css
    inject_global_css()
else:
    # CSS viejo inline (mantener por ahora)
    st.markdown(f"""<style>...</style>""", unsafe_allow_html=True)
```

**Testing:**
```bash
# 1. Con flag OFF (debe verse igual)
streamlit run app.py

# 2. Activar flag
# En utils/feature_flags.py: USE_NEW_CSS_MODULE = True
streamlit run app.py

# 3. Comparar visualmente (debe verse IDÉNTICO)
# 4. Si todo OK, commit
git add utils/styles/
git commit -m "feat(styles): Extract CSS to module with feature flag"
```

#### 1.2 Crear Theme de Plotly (3 horas)

```python
# 1. Crear utils/charts/plotly_theme.py
# (Ver código completo en sección 3.3)

# 2. Modificar utils/visualizer.py
# ANTES:
def grafico_distribucion_gastos(gastos_por_categoria):
    fig = px.pie(df, names='categoria', values='total')
    fig.update_layout(template=PLOTLY_TEMPLATE)  # Template viejo
    return fig

# DESPUÉS:
from utils.feature_flags import FeatureFlags
from utils.charts.plotly_theme import apply_finanzas_theme

def grafico_distribucion_gastos(gastos_por_categoria):
    fig = px.pie(df, names='categoria', values='total')

    if FeatureFlags.USE_NEW_PLOTLY_THEME:
        fig = apply_finanzas_theme(fig)
    else:
        fig.update_layout(template=PLOTLY_TEMPLATE)  # Viejo

    return fig

# 3. Repetir para todos los gráficos en visualizer.py:
# - grafico_evolucion_anual()
# - grafico_evolucion_mensual()
# - grafico_evolucion_saldo()
# - Cualquier otro gráfico custom
```

**Testing:**
```bash
# 1. Flag OFF - verificar gráficos se ven igual
streamlit run app.py
# Navegar a Dashboard → Ver todos los gráficos

# 2. Flag ON
# En feature_flags.py: USE_NEW_PLOTLY_THEME = True
streamlit run app.py

# 3. Verificar colores cambiaron PERO datos son iguales
# 4. Commit si OK
git add utils/charts/ utils/visualizer.py
git commit -m "feat(charts): Add unified Plotly theme with feature flag"
```

#### 1.3 Refactorizar Lógica de Negocio (3 horas)

**Objetivo:** Separar cálculos de presentación en `mostrar_dashboard()`

```python
# ANTES (app.py línea ~940):
def mostrar_dashboard():
    st.title("📊 Dashboard Financiero")

    # Cálculos mezclados con UI
    datos_mes = metrics.calcular_totales_mes(mes, año)
    ingreso_base_data = metrics.obtener_ingreso_base_mes(mes, año)
    total_ingresos_mes = ingreso_base_data['importe'] + ingresos_extra['total']

    col1, col2 = st.columns(2)
    col1.metric("💵 Total Ingresos", f"{total_ingresos_mes:.2f} €")
    # ... más UI ...

# DESPUÉS (separar en funciones):

# 1. Crear utils/dashboard_data.py
def get_dashboard_monthly_data(mes: int, año: int) -> dict:
    """
    Obtiene TODOS los datos del dashboard mensual
    SIN ninguna lógica de UI
    """
    datos_mes = metrics.calcular_totales_mes(mes, año)
    ingreso_base_data = metrics.obtener_ingreso_base_mes(mes, año)
    ingresos_extra = metrics.obtener_ingresos_extraordinarios_mes(mes, año)

    return {
        'datos_mes': datos_mes,
        'ingreso_base': ingreso_base_data,
        'ingresos_extra': ingresos_extra,
        'total_ingresos': ingreso_base_data['importe'] + ingresos_extra['total'],
        'gastos_netos': abs(datos_mes['gastos_netos']),
        'balance': ...,
        'tasa_ahorro': ...,
        'presupuestos': db_manager.obtener_resumen_presupuestos(mes, año)
    }

# 2. Modificar app.py
def mostrar_dashboard():
    st.title("📊 Dashboard Financiero")

    # Obtener datos (separado de UI)
    from utils.dashboard_data import get_dashboard_monthly_data
    data = get_dashboard_monthly_data(mes, año)

    # Renderizar UI (solo presentación)
    _render_dashboard_metrics(data)
    _render_dashboard_charts(data)
    _render_dashboard_budgets(data['presupuestos'])

def _render_dashboard_metrics(data):
    """Renderiza solo las métricas"""
    col1, col2 = st.columns(2)
    col1.metric("💵 Total Ingresos", f"{data['total_ingresos']:.2f} €")
    col2.metric("💸 Gastos", f"{data['gastos_netos']:.2f} €")
    # ... etc
```

**Ventajas de separar lógica:**
- ✅ Facilita testing (test data layer sin UI)
- ✅ Permite cachear datos independientemente
- ✅ Reutilizar datos en múltiples vistas
- ✅ UI más limpia y fácil de refactorizar

**Testing:**
```bash
# 1. Test unitario de datos
python -c "from utils.dashboard_data import get_dashboard_monthly_data; print(get_dashboard_monthly_data(10, 2025))"

# 2. Verificar UI sigue igual
streamlit run app.py

# 3. Commit
git add utils/dashboard_data.py app.py
git commit -m "refactor(dashboard): Separate business logic from UI"
```

**Checkpoint Fase 1:**
```bash
# Tag de rollback
git tag phase-1-complete

# Estado esperado:
# ✅ CSS extraído a módulo (con flag)
# ✅ Theme Plotly unificado (con flag)
# ✅ Lógica de negocio separada de UI
# ✅ Todos los flags aún en False
# ✅ App funciona IDÉNTICA a antes
```

---

### FASE 2: Componentes Reutilizables (2 días - 16 horas)

**Objetivo:** Crear wrappers de componentes sin cambiar páginas

#### 2.1 MetricCard Component (4 horas)

```python
# 1. Crear utils/components/metrics.py
# (Ver código completo en sección 3.2.1)

# 2. Modificar app.py para usar componente (con flag)
from utils.feature_flags import FeatureFlags
from utils.components.metrics import MetricCard, KPIRow

def _render_dashboard_metrics(data):
    if FeatureFlags.USE_METRIC_CARDS:
        # Nueva versión con componente
        KPIRow([
            {
                "label": "💵 Total Ingresos Mes",
                "value": f"{data['total_ingresos']:.2f} €",
                "variant": "success",
                "help_text": "Suma de todos los ingresos del mes"
            },
            {
                "label": "💸 Gastos del Mes",
                "value": f"{data['gastos_netos']:.2f} €",
                "variant": "error",
                "help_text": "Gastos netos (después de reembolsos)"
            },
            {
                "label": "⚖️ Balance del Mes",
                "value": f"{data['balance']:.2f} €",
                "delta": f"{data['balance']:.2f} €",
                "trend": "up" if data['balance'] > 0 else "down",
                "variant": "success" if data['balance'] > 0 else "error"
            }
        ])
    else:
        # Versión vieja con st.metric()
        col1, col2, col3 = st.columns(3)
        col1.metric("💵 Total Ingresos Mes", f"{data['total_ingresos']:.2f} €")
        col2.metric("💸 Gastos del Mes", f"{data['gastos_netos']:.2f} €")
        col3.metric("⚖️ Balance del Mes", f"{data['balance']:.2f} €")

# 3. Repetir para todas las métricas:
# - Dashboard (15 métricas)
# - Página de Coche Eléctrico (~10 métricas)
# - Análisis Avanzado (~8 métricas)
```

**Testing:**
```bash
# Flag OFF → debe verse con st.metric() normal
streamlit run app.py

# Flag ON → debe verse con componente nuevo
# En feature_flags.py: USE_METRIC_CARDS = True
streamlit run app.py

# Comparar valores (deben ser IDÉNTICOS)
# Commit si OK
git add utils/components/metrics.py app.py
git commit -m "feat(components): Add MetricCard component with feature flag"
```

#### 2.2 ChartContainer Component (4 horas)

```python
# 1. Crear utils/components/charts.py
# (Ver código completo en sección 3.2.2)

# 2. Modificar app.py
from utils.components.charts import ChartContainer

def _render_dashboard_charts(data):
    if FeatureFlags.USE_CHART_CONTAINERS:
        # Con componente
        fig = visualizer.grafico_distribucion_gastos(data['gastos_por_categoria'])
        ChartContainer(
            fig=fig,
            title="Distribución de Gastos por Categoría",
            description="Porcentaje de gastos en cada categoría del mes"
        )
    else:
        # Sin componente (viejo)
        fig = visualizer.grafico_distribucion_gastos(data['gastos_por_categoria'])
        st.plotly_chart(fig, use_container_width=True)

# 3. Aplicar a TODOS los gráficos de la app:
# - Gráfico de distribución de gastos (dashboard)
# - Evolución anual (dashboard)
# - Evolución histórica (dashboard)
# - Saldo temporal (análisis avanzado)
# - Consumo eléctrico (coche eléctrico)
```

#### 2.3 FormCard Component (4 horas)

```python
# utils/components/forms.py
"""
Componentes para formularios estilizados
"""

import streamlit as st
from utils.design_tokens import Colors, BorderRadius, Spacing

def FormCard(title: str, icon: str = "📝"):
    """
    Contenedor estilizado para formularios

    Example:
        >>> with FormCard("Nueva Transacción", "💸"):
        ...     concepto = st.text_input("Concepto")
        ...     importe = st.number_input("Importe")
        ...     st.form_submit_button("Guardar")
    """

    st.markdown(f"""
    <div style="
        background: {Colors.PREMIUM_CARD_GRADIENT};
        border-radius: {BorderRadius.LG};
        padding: {Spacing.XL};
        border: 1px solid rgba(10, 76, 62, 0.1);
        box-shadow: {Colors.SHADOW_PREMIUM_MD};
    ">
        <h3>{icon} {title}</h3>
    """, unsafe_allow_html=True)

    return _FormCardContext()

class _FormCardContext:
    def __enter__(self):
        return self
    def __exit__(self, *args):
        st.markdown("</div>", unsafe_allow_html=True)

# Uso en app.py (mostrar_añadir_gasto):
if FeatureFlags.USE_FORM_CARDS:
    with FormCard("Nuevo Gasto", "💸"):
        with st.form("form_gasto"):
            concepto = st.text_input("Concepto")
            # ... resto del formulario
else:
    # Formulario viejo sin card
    with st.form("form_gasto"):
        st.subheader("💸 Nuevo Gasto")
        concepto = st.text_input("Concepto")
```

#### 2.4 DataTable Component (4 horas)

```python
# utils/components/tables.py
"""
Tablas de datos estilizadas
"""

import streamlit as st
import pandas as pd
from utils.design_tokens import Colors, BorderRadius

def DataTable(
    df: pd.DataFrame,
    editable: bool = False,
    show_export: bool = True,
    height: int = 400
):
    """
    Tabla de datos con estilos premium

    Args:
        df: DataFrame a mostrar
        editable: Si es editable con st.data_editor
        show_export: Mostrar botón de exportar
        height: Altura en px
    """

    # Card container
    st.markdown(f"""
    <div style="
        background: {Colors.PREMIUM_CARD_GRADIENT};
        border-radius: {BorderRadius.LG};
        padding: {Spacing.LG};
        box-shadow: {Colors.SHADOW_PREMIUM_MD};
    ">
    """, unsafe_allow_html=True)

    if editable:
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            height=height,
            hide_index=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return edited_df
    else:
        st.dataframe(
            df,
            use_container_width=True,
            height=height,
            hide_index=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return df

# Uso en app.py (mostrar_transacciones):
if FeatureFlags.USE_FORM_CARDS:
    df_edited = DataTable(df_transacciones, editable=True)
else:
    df_edited = st.data_editor(df_transacciones)
```

**Checkpoint Fase 2:**
```bash
git tag phase-2-complete

# Estado:
# ✅ 4 componentes creados (Metric, Chart, Form, Table)
# ✅ Todos con feature flags
# ✅ Aplicados en páginas principales
# ✅ App funciona con flags ON y OFF
```

---

### FASE 3: Sistema de Layouts (1 día - 8 horas)

**Objetivo:** Layouts consistentes en todas las páginas

#### 3.1 PageLayout System (4 horas)

```python
# 1. Crear utils/components/layouts.py
# (Ver código completo en sección 3.2.3)

# 2. Refactorizar mostrar_dashboard() con PageLayout
from utils.components.layouts import PageLayout, Grid

def mostrar_dashboard():
    if FeatureFlags.USE_PAGE_LAYOUTS:
        # Con sistema de layouts
        PageLayout.render(
            title="Dashboard Financiero",
            icon="📊",
            subtitle="Resumen completo de tus finanzas",
            show_period_selector=True
        )

        with PageLayout.section("Métricas Principales"):
            cols = Grid(columns=4)
            # ... métricas en grid

        with PageLayout.section("Gráficos", collapsible=False):
            # ... gráficos
    else:
        # Layout viejo
        st.title("📊 Dashboard Financiero")
        # ... resto del código viejo

# 3. Aplicar a TODAS las páginas:
# - mostrar_dashboard()
# - mostrar_transacciones()
# - mostrar_importar()
# - mostrar_categorias()
# - mostrar_sincronizacion()
# - mostrar_configuracion()
# - mostrar_coche_electrico()
# - mostrar_asistente_ia()
```

#### 3.2 Grid System Responsive (2 horas)

```python
# Ya incluido en layouts.py (función Grid)
# Uso:

cols = Grid(columns=3, gap=Spacing.XL)

with cols[0]:
    MetricCard("Ingresos", "2500€", variant="success")

with cols[1]:
    MetricCard("Gastos", "1800€", variant="error")

with cols[2]:
    MetricCard("Balance", "700€", variant="default")
```

#### 3.3 Responsive Utilities (2 horas)

```python
# utils/components/responsive.py
"""
Utilidades para diseño responsive
"""

import streamlit as st

def get_screen_size() -> str:
    """
    Detecta tamaño de pantalla aproximado

    Returns:
        'mobile', 'tablet', o 'desktop'

    Note:
        Streamlit no tiene acceso real al viewport,
        usamos heurística basada en user agent
    """
    # Por ahora retornar desktop (Streamlit limitation)
    # En futuro con st.experimental_get_query_params()
    return 'desktop'

def responsive_columns(mobile: int = 1, tablet: int = 2, desktop: int = 3):
    """
    Columnas responsive según tamaño de pantalla

    Args:
        mobile: Columnas en móvil
        tablet: Columnas en tablet
        desktop: Columnas en desktop

    Returns:
        st.columns() con número apropiado

    Example:
        >>> cols = responsive_columns(mobile=1, tablet=2, desktop=4)
        >>> # En desktop = 4 cols, tablet = 2, mobile = 1
    """
    screen = get_screen_size()

    if screen == 'mobile':
        return st.columns(mobile)
    elif screen == 'tablet':
        return st.columns(tablet)
    else:
        return st.columns(desktop)

# Uso:
cols = responsive_columns(mobile=1, tablet=2, desktop=4)
for col, metric in zip(cols, metrics_data):
    with col:
        MetricCard(**metric)
```

**Checkpoint Fase 3:**
```bash
git tag phase-3-complete

# Estado:
# ✅ PageLayout system implementado
# ✅ Grid system funcional
# ✅ Responsive utilities creadas
# ✅ Aplicado en todas las páginas
```

---

### FASE 4: Migración de Páginas (3 días - 24 horas)

**Objetivo:** Reescribir páginas con componentes nuevos

**Estrategia: Una página a la vez**

#### 4.1 Dashboard v2 (1 día - 8 horas)

```python
# app.py - Crear versión paralela

def mostrar_dashboard_v2():
    """
    Dashboard completamente rediseñado con componentes nuevos
    """
    from utils.components.layouts import PageLayout, Grid
    from utils.components.metrics import KPIRow
    from utils.components.charts import ChartContainer
    from utils.dashboard_data import get_dashboard_monthly_data

    # Header consistente
    PageLayout.render(
        title="Dashboard Financiero",
        icon="📊",
        subtitle="Análisis completo de tus finanzas",
        show_period_selector=True,
        show_export_button=True
    )

    # Obtener datos (sin UI)
    data = get_dashboard_monthly_data(mes, año)

    # Métricas principales en grid 4x1
    with PageLayout.section("Resumen del Mes"):
        KPIRow([
            {
                "label": "Total Ingresos",
                "value": f"{data['total_ingresos']:.2f} €",
                "icon": "💵",
                "variant": "success",
                "help_text": "Suma de nómina + ingresos extraordinarios"
            },
            {
                "label": "Gastos Netos",
                "value": f"{data['gastos_netos']:.2f} €",
                "icon": "💸",
                "variant": "error",
                "help_text": "Gastos después de reembolsos"
            },
            {
                "label": "Balance",
                "value": f"{data['balance']:.2f} €",
                "icon": "⚖️",
                "delta": f"{data['balance_pct']:.1f}%",
                "trend": "up" if data['balance'] > 0 else "down",
                "variant": "success" if data['balance'] > 0 else "error"
            },
            {
                "label": "Tasa Ahorro",
                "value": f"{data['tasa_ahorro']:.1f}%",
                "icon": "💾",
                "delta": "Ideal: >20%",
                "delta_color": "off"
            }
        ])

    # Gráficos en grid 2x1
    with PageLayout.section("Análisis Visual"):
        cols = Grid(columns=2)

        with cols[0]:
            fig1 = visualizer.grafico_distribucion_gastos(data['gastos_por_categoria'])
            ChartContainer(
                fig=fig1,
                title="Distribución de Gastos",
                description="Porcentaje por categoría"
            )

        with cols[1]:
            fig2 = visualizer.grafico_evolucion_saldo(data['transacciones'])
            ChartContainer(
                fig=fig2,
                title="Evolución del Saldo",
                description="Saldo después de cada transacción"
            )

    # Presupuestos (si existen)
    if data['presupuestos']:
        with PageLayout.section("Presupuestos del Mes", collapsible=True):
            _render_presupuestos_v2(data['presupuestos'])

# Selector en app.py (inicio)
def main():
    # ... sidebar navigation ...

    if pagina == "Dashboard":
        if FeatureFlags.DASHBOARD_V2:
            mostrar_dashboard_v2()  # Nueva versión
        else:
            mostrar_dashboard()     # Versión vieja

# Implementar:
if __name__ == "__main__":
    main()
```

**Testing Dashboard v2:**
```bash
# 1. Flag OFF → versión vieja
streamlit run app.py

# 2. Flag ON → versión nueva
# En feature_flags.py: DASHBOARD_V2 = True
streamlit run app.py

# 3. Comparar:
# - Valores de métricas (deben ser iguales)
# - Datos en gráficos (deben ser iguales)
# - Layout (puede ser diferente - es el objetivo)
# - Funcionalidad (botones, filtros deben funcionar)

# 4. Commit si OK
git add app.py utils/components/
git commit -m "feat(dashboard): Add Dashboard v2 with new components"
```

#### 4.2 Resto de Páginas (2 días - 16 horas)

**Mismo proceso para:**

```python
# Página Transacciones (4 horas)
def mostrar_transacciones_v2():
    PageLayout.render("Transacciones", "💸")
    # ... con DataTable component

# Página Importar (3 horas)
def mostrar_importar_v2():
    PageLayout.render("Importar Excel", "📥")
    # ... con FormCard component

# Página Categorías (3 horas)
def mostrar_categorias_v2():
    PageLayout.render("Gestión de Categorías", "🏷️")
    # ... con DataTable + FormCard

# Página Configuración (2 horas)
def mostrar_configuracion_v2():
    PageLayout.render("Configuración", "⚙️")
    # ... con FormCard components

# Página Coche Eléctrico (2 horas)
def mostrar_coche_electrico_v2():
    PageLayout.render("Coche Eléctrico", "🔌")
    # ... con MetricCard + ChartContainer

# Página Asistente IA (2 horas)
def mostrar_asistente_ia_v2():
    PageLayout.render("Asistente Financiero IA", "🤖")
    # ... layout mejorado con cards
```

**Estrategia por página:**
1. Crear función `mostrar_PAGINA_v2()`
2. Usar `PageLayout.render()` para header
3. Reemplazar `st.metric()` → `MetricCard()`
4. Reemplazar `st.plotly_chart()` → `ChartContainer()`
5. Envolver formularios con `FormCard()`
6. Tablas con `DataTable()`
7. Feature flag en router principal
8. Testing visual y funcional
9. Commit

**Checkpoint Fase 4:**
```bash
git tag phase-4-complete

# Estado:
# ✅ Dashboard v2 completo
# ✅ 6 páginas restantes migradas
# ✅ Todos los componentes en uso
# ✅ Todos los flags funcionando
# ✅ App 100% funcional en ambas versiones
```

---

### FASE 5: Activación y Limpieza (1 día - 8 horas)

**Objetivo:** Activar diseño nuevo y eliminar código viejo

#### 5.1 Activar Flags Gradualmente (2 horas)

```python
# utils/feature_flags.py - Activar uno por uno

class FeatureFlags:
    # DÍA 1: Activar fundamentos
    USE_NEW_CSS_MODULE = True      # ✅ Activado
    USE_NEW_PLOTLY_THEME = True    # ✅ Activado

    # DÍA 2: Activar componentes
    USE_METRIC_CARDS = True         # ✅ Activado
    USE_CHART_CONTAINERS = True     # ✅ Activado
    USE_FORM_CARDS = True           # ✅ Activado

    # DÍA 3: Activar layouts
    USE_PAGE_LAYOUTS = True         # ✅ Activado
    USE_GRID_SYSTEM = True          # ✅ Activado

    # DÍA 4: Activar páginas v2
    DASHBOARD_V2 = True             # ✅ Activado
    TRANSACTIONS_V2 = True          # ✅ Activado
    # ... resto de páginas

    DEBUG_MODE = False
```

**Proceso de activación:**
```bash
# 1. Activar CSS nuevo
# feature_flags.py: USE_NEW_CSS_MODULE = True
streamlit run app.py
# Testing: 15 min navegando todas las páginas

# 2. Activar theme Plotly
# feature_flags.py: USE_NEW_PLOTLY_THEME = True
streamlit run app.py
# Testing: Ver todos los gráficos

# 3. Activar componentes (todos a la vez)
# feature_flags.py: USE_METRIC_CARDS = True, etc.
streamlit run app.py
# Testing: 30 min navegando

# 4. Activar layouts
# feature_flags.py: USE_PAGE_LAYOUTS = True
streamlit run app.py
# Testing: 30 min navegando

# 5. Activar páginas v2 (una a una)
# feature_flags.py: DASHBOARD_V2 = True
# Probar Dashboard exhaustivamente
# feature_flags.py: TRANSACTIONS_V2 = True
# Probar Transacciones exhaustivamente
# ... repetir para todas

# 6. Si todo OK, commit
git add utils/feature_flags.py
git commit -m "feat: Enable all new design features"
git tag design-v2-enabled
```

#### 5.2 Eliminar Código Viejo (4 horas)

**IMPORTANTE: Solo después de 1 semana de uso sin problemas**

```python
# app.py - Eliminar código viejo

# ANTES (con flag):
if FeatureFlags.DASHBOARD_V2:
    mostrar_dashboard_v2()
else:
    mostrar_dashboard()  # <-- ELIMINAR esta función completa

# DESPUÉS (sin flag):
mostrar_dashboard_v2()  # Renombrar a mostrar_dashboard()

# Pasos:
# 1. Buscar todos los if FeatureFlags.XXX
grep -rn "FeatureFlags" app.py pages_*.py

# 2. Eliminar ramas else (código viejo)
# 3. Eliminar checks de flags
# 4. Renombrar funciones _v2 → nombre original
# 5. Eliminar utils/feature_flags.py completo
# 6. Commit masivo
git add .
git commit -m "refactor: Remove old code and feature flags"
git tag design-v2-cleanup-complete
```

#### 5.3 Documentación Final (2 horas)

```markdown
# docs/DESIGN_V2_CHANGELOG.md
# Changelog del Overhaul de Diseño v2

## Resumen
Rediseño completo de la UI con componentes reutilizables y design system unificado.

## Cambios Principales

### Componentes Nuevos
- `MetricCard`: Métricas estilizadas con gradientes y sombras
- `ChartContainer`: Contenedor premium para gráficos Plotly
- `FormCard`: Formularios con card styling
- `DataTable`: Tablas con estilos consistentes
- `PageLayout`: Sistema de layouts para páginas
- `Grid`: Sistema de grid responsive

### Mejoras Visuales
- Theme Plotly unificado con colores del design system
- CSS extraído a módulo independiente
- Sombras multicapa (profundidad realista)
- Animaciones y transiciones suaves
- Hover effects en todos los elementos interactivos

### Arquitectura
- Separación completa de lógica y presentación
- Feature flags para migración segura
- Sistema de componentes reutilizables
- Testing automatizado

## Antes/Después

### Métricas
**Antes:**
- Código duplicado en cada página
- Estilos inline inconsistentes
- Sin hover effects

**Después:**
- Componente único reutilizable
- Estilos centralizados
- Animaciones suaves en hover
- Gradientes premium

### Gráficos
**Antes:**
- Colores hardcoded diferentes en cada gráfico
- Sin container estilizado
- Template inconsistente

**Después:**
- Colores del design system
- ChartContainer con sombras y bordes
- Theme Plotly único

## Estadísticas

- Líneas de código eliminadas: ~800 (CSS duplicado)
- Componentes creados: 10
- Páginas migradas: 7
- Tiempo total: 9 días (72 horas)
- Bugs introducidos: 0
- Downtime: 0 segundos

## Migración

### Fases
1. Preparación (2h)
2. Fundamentos (8h)
3. Componentes (16h)
4. Layouts (8h)
5. Páginas (24h)
6. Activación (8h)

### Rollback Points
- `phase-0-complete`: Setup inicial
- `phase-1-complete`: CSS y Plotly theme
- `phase-2-complete`: Componentes
- `phase-3-complete`: Layouts
- `phase-4-complete`: Páginas migradas
- `design-v2-enabled`: Flags activados
- `design-v2-cleanup-complete`: Código viejo eliminado

## Créditos
- Diseño: Claude (Anthropic)
- Implementación: Daniel + Claude
- Testing: Manual + Visual regression
```

**Checkpoint Final:**
```bash
git tag design-v2-complete

# Estado final:
# ✅ Todos los flags activados
# ✅ Código viejo eliminado
# ✅ Documentación completa
# ✅ Testing OK
# ✅ 0 bugs reportados
# 🎉 OVERHAUL COMPLETO
```

---

## 5. Testing y Validación

### 5.1 Testing Manual (Checklist)

**Antes de cada fase, verificar:**

#### Dashboard
- [ ] Métricas muestran valores correctos
- [ ] Gráfico de distribución renderiza
- [ ] Gráfico de evolución anual renderiza
- [ ] Gráfico de evolución histórica renderiza
- [ ] Selector de mes/año funciona
- [ ] Vista mensual/anual alterna correctamente
- [ ] Tabs (Resumen, Análisis, Histórico) funcionan
- [ ] Botón "Ver desglose" abre modal
- [ ] Botón "Reembolsos" abre modal
- [ ] Presupuestos se muestran correctamente

#### Transacciones
- [ ] Tabla carga con datos
- [ ] Filtros (mes, año, categoría) funcionan
- [ ] Edición inline funciona
- [ ] Botón "Guardar cambios" funciona
- [ ] Validación de campos funciona

#### Importar
- [ ] Upload de Excel funciona
- [ ] Vista previa muestra transacciones
- [ ] Detección de duplicados funciona
- [ ] Botón "Importar" inserta en BD
- [ ] Contador de transacciones correcto

#### Categorías
- [ ] Lista de reglas se muestra
- [ ] Formulario de nueva regla funciona
- [ ] Guardar regla persiste en JSON
- [ ] Reglas se aplican en importación

#### Configuración
- [ ] Botón reset muestra confirmación
- [ ] Reset borra datos correctamente
- [ ] Configuraciones se guardan

#### Coche Eléctrico
- [ ] Formulario de recarga funciona
- [ ] Cálculo de kWh automático
- [ ] Gráficos de consumo renderizan
- [ ] Estadísticas correctas

#### Asistente IA
- [ ] Chat input funciona
- [ ] Respuestas se generan
- [ ] SQL queries se ejecutan
- [ ] Errores se manejan

### 5.2 Testing Automatizado

```python
# tests/test_components.py
"""
Tests unitarios para componentes
"""

import pytest
from utils.components.metrics import MetricCard, KPIRow
from utils.components.charts import ChartContainer
from utils.components.layouts import PageLayout, Grid

class TestMetricCard:
    def test_metric_card_renders(self):
        """MetricCard debe renderizar sin errores"""
        # Mock st.markdown
        from unittest.mock import patch
        with patch('streamlit.markdown') as mock_markdown:
            MetricCard(
                label="Test Metric",
                value="100.00 €",
                variant="success"
            )
            assert mock_markdown.called

    def test_kpi_row_creates_columns(self):
        """KPIRow debe crear columnas correctas"""
        from unittest.mock import patch
        with patch('streamlit.columns') as mock_columns:
            KPIRow([
                {"label": "M1", "value": "100€"},
                {"label": "M2", "value": "200€"}
            ])
            mock_columns.assert_called_once_with(2)

class TestPlotlyTheme:
    def test_theme_applies_colors(self):
        """Theme debe aplicar colores del design system"""
        import plotly.express as px
        from utils.charts.plotly_theme import apply_finanzas_theme

        fig = px.bar(x=[1,2,3], y=[10,20,30])
        fig = apply_finanzas_theme(fig)

        # Verificar que tiene layout
        assert fig.layout is not None
        # Verificar colores customizados
        assert 'colorway' in fig.layout

    def test_theme_preserves_data(self):
        """Theme no debe modificar datos"""
        import plotly.express as px
        from utils.charts.plotly_theme import apply_finanzas_theme

        original_data = [10, 20, 30]
        fig = px.bar(x=[1,2,3], y=original_data)
        fig = apply_finanzas_theme(fig)

        # Datos deben permanecer iguales
        assert list(fig.data[0].y) == original_data

# Ejecutar tests:
# pytest tests/test_components.py -v
```

### 5.3 Visual Regression Testing

```python
# tests/test_visual_regression.py
"""
Tests de regresión visual (comparar screenshots)
"""

import pytest
from playwright.sync_api import sync_playwright

class TestVisualRegression:
    """
    Requiere: pip install playwright pytest-playwright
    Setup: playwright install
    """

    def test_dashboard_screenshot(self, page):
        """Capturar screenshot del dashboard"""
        page.goto("http://localhost:8501")

        # Esperar que cargue
        page.wait_for_selector(".stApp")

        # Capturar screenshot
        page.screenshot(path="tests/screenshots/dashboard.png")

        # Comparar con baseline (manualmente primera vez)
        # En ejecuciones posteriores, comparar con diff

    def test_metrics_equal_values(self, page):
        """Verificar que valores de métricas son iguales"""
        page.goto("http://localhost:8501")

        # Extraer valores de métricas
        metrics = page.query_selector_all(".stMetric")
        values = [m.inner_text() for m in metrics]

        # Comparar con valores esperados (de BD de test)
        expected = ["2,500.00 €", "1,800.00 €", "700.00 €"]
        assert values == expected

# Ejecutar:
# pytest tests/test_visual_regression.py --headed
```

---

## 6. Puntos de Rollback

### 6.1 Rollback por Git Tags

**Tags creados en cada fase:**

```bash
# Listar todos los tags
git tag

# Output esperado:
phase-0-complete          # Setup inicial
phase-1-complete          # CSS + Plotly theme
phase-2-complete          # Componentes
phase-3-complete          # Layouts
phase-4-complete          # Páginas migradas
design-v2-enabled         # Flags activados
design-v2-cleanup-complete # Código viejo eliminado
design-v2-complete        # Final
```

**Cómo hacer rollback:**

```bash
# Rollback a fase anterior (ej: volver a fase 3)
git checkout phase-3-complete

# Crear rama desde ese punto si quieres experimentar
git checkout -b hotfix/rollback-to-phase-3

# Ver cambios desde tag
git diff phase-3-complete..HEAD

# Rollback definitivo (CUIDADO: destructivo)
git reset --hard phase-3-complete
```

### 6.2 Rollback por Feature Flags

**Más seguro: desactivar flags sin cambiar código**

```python
# utils/feature_flags.py

# ROLLBACK COMPLETO - Desactivar todo
class FeatureFlags:
    USE_NEW_CSS_MODULE = False       # Volver a CSS inline
    USE_NEW_PLOTLY_THEME = False     # Volver a theme viejo
    USE_METRIC_CARDS = False         # Volver a st.metric()
    USE_CHART_CONTAINERS = False     # Volver a st.plotly_chart()
    USE_FORM_CARDS = False           # Formularios sin card
    USE_PAGE_LAYOUTS = False         # Layouts viejos
    DASHBOARD_V2 = False             # Dashboard v1
    TRANSACTIONS_V2 = False          # Transacciones v1

# ROLLBACK PARCIAL - Solo un componente
class FeatureFlags:
    USE_METRIC_CARDS = False  # <-- Solo desactivar este
    # ... resto activados

# Ventaja: No hay commit, solo cambiar archivo
# Desventaja: Solo funciona antes de limpiar código viejo
```

### 6.3 Backup de Base de Datos

**Antes de CUALQUIER cambio:**

```bash
# Backup manual
cp finanzas.db finanzas.db.backup-$(date +%Y%m%d-%H%M%S)

# Listar backups
ls -lht finanzas.db.backup-*

# Restaurar backup
cp finanzas.db.backup-20251204-103000 finanzas.db

# Backup automático (en app.py al inicio)
import shutil
from datetime import datetime

def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2("finanzas.db", f"finanzas.db.backup-{timestamp}")
    # Mantener solo últimos 5 backups
    import glob
    backups = sorted(glob.glob("finanzas.db.backup-*"), reverse=True)
    for old_backup in backups[5:]:
        os.remove(old_backup)

# Ejecutar al inicio
backup_database()
```

### 6.4 Plan de Contingencia

**Si algo sale mal en producción:**

1. **Problema menor (bug visual):**
   - Desactivar flag específico
   - Continuar usando app
   - Fixear bug en desarrollo
   - Reactivar flag

2. **Problema mayor (crash, datos incorrectos):**
   - Desactivar TODOS los flags
   - Rollback a tag anterior
   - Restaurar backup de BD si es necesario
   - Investigar causa root
   - Fixear en desarrollo con tests
   - Re-migrar cuando esté seguro

3. **Catástrofe (BD corrupta, pérdida de datos):**
   - Restaurar backup de BD más reciente
   - Rollback a `main` branch
   - NO re-intentar migración hasta root cause
   - Considerar testing más exhaustivo

**Tiempos de recuperación esperados:**
- Desactivar flags: 30 segundos
- Rollback por git: 2 minutos
- Restaurar BD: 1 minuto
- **Total: <5 minutos de downtime**

---

## 7. Código de Ejemplo

### 7.1 Ejemplo Completo: Migrar Página Dashboard

**ANTES (código viejo - líneas 880-1100 de app.py):**

```python
def mostrar_dashboard():
    st.title("📊 Dashboard Financiero")

    # Selectores
    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
    with col1:
        año = st.selectbox("📅 Año", obtener_años_disponibles())
    with col2:
        mes = st.selectbox("📆 Mes", list(NOMBRES_MESES.values()))

    # Calcular métricas (mezclado con UI)
    datos_mes = metrics.calcular_totales_mes(mes, año)
    ingreso_base_data = metrics.obtener_ingreso_base_mes(mes, año)
    ingresos_extra = metrics.obtener_ingresos_extraordinarios_mes(mes, año)
    total_ingresos_mes = ingreso_base_data['importe'] + ingresos_extra['total']
    gastos_netos = abs(datos_mes['gastos_netos'])
    balance_mes = total_ingresos_mes + datos_mes['gastos_netos']

    # Métricas (código duplicado)
    col1, col2 = st.columns(2)
    col1.metric(
        "💵 Total Ingresos Mes",
        f"{total_ingresos_mes:.2f} €",
        help="Suma de todos los ingresos del mes"
    )
    col2.metric(
        "💸 Gastos del Mes",
        f"{gastos_netos:.2f} €",
        help="Gastos netos"
    )

    col3, col4 = st.columns(2)
    col3.metric(
        "⚖️ Balance del Mes",
        f"{balance_mes:.2f} €",
        delta=f"{balance_mes:.2f} €"
    )
    col4.metric(
        "💾 Tasa Ahorro",
        f"{(balance_mes/total_ingresos_mes*100):.1f}%"
    )

    # Gráfico (sin container)
    st.subheader("📊 Distribución de Gastos")
    fig = visualizer.grafico_distribucion_gastos(datos_mes['gastos_por_categoria'])
    st.plotly_chart(fig, use_container_width=True)

    # ... más código ...
```

**DESPUÉS (código nuevo con componentes):**

```python
def mostrar_dashboard():
    """Dashboard financiero rediseñado con componentes"""

    # === IMPORTS ===
    from utils.components.layouts import PageLayout, Grid
    from utils.components.metrics import KPIRow
    from utils.components.charts import ChartContainer
    from utils.dashboard_data import get_dashboard_monthly_data
    from utils import visualizer

    # === HEADER ===
    PageLayout.render(
        title="Dashboard Financiero",
        icon="📊",
        subtitle="Análisis completo de tus finanzas personales",
        show_period_selector=True,
        show_export_button=False
    )

    # === OBTENER DATOS (separado de UI) ===
    data = get_dashboard_monthly_data(mes, año)

    # === SECCIÓN: MÉTRICAS PRINCIPALES ===
    with PageLayout.section("Resumen del Mes"):
        KPIRow([
            {
                "label": "Total Ingresos",
                "value": f"{data['total_ingresos']:.2f} €",
                "icon": "💵",
                "variant": "success",
                "trend": "up",
                "help_text": "Suma de nómina + ingresos extraordinarios del mes"
            },
            {
                "label": "Gastos Netos",
                "value": f"{data['gastos_netos']:.2f} €",
                "icon": "💸",
                "variant": "error",
                "trend": "down",
                "help_text": "Gastos después de aplicar reembolsos"
            },
            {
                "label": "Balance del Mes",
                "value": f"{data['balance']:.2f} €",
                "icon": "⚖️",
                "delta": f"{data['balance']:.2f} €",
                "trend": "up" if data['balance'] > 0 else "down",
                "variant": "success" if data['balance'] > 0 else "error",
                "help_text": "Ingresos - Gastos. Positivo = superávit, Negativo = déficit"
            },
            {
                "label": "Tasa de Ahorro",
                "value": f"{data['tasa_ahorro']:.1f}%",
                "icon": "💾",
                "delta": "Ideal: >20%",
                "delta_color": "off",
                "variant": "success" if data['tasa_ahorro'] > 20 else "warning",
                "help_text": "Porcentaje de ingresos que has logrado ahorrar"
            }
        ])

    # === SECCIÓN: GRÁFICOS ===
    with PageLayout.section("Análisis Visual"):
        cols = Grid(columns=2, gap=Spacing.XL)

        with cols[0]:
            fig_dist = visualizer.grafico_distribucion_gastos(
                data['gastos_por_categoria']
            )
            ChartContainer(
                fig=fig_dist,
                title="Distribución de Gastos por Categoría",
                description="Porcentaje de cada categoría en el total de gastos"
            )

        with cols[1]:
            fig_saldo = visualizer.grafico_evolucion_saldo(
                data['transacciones']
            )
            ChartContainer(
                fig=fig_saldo,
                title="Evolución del Saldo",
                description="Saldo de cuenta después de cada transacción"
            )

    # === SECCIÓN: PRESUPUESTOS (si existen) ===
    if data['presupuestos']:
        with PageLayout.section("Presupuestos del Mes", collapsible=True):
            for presupuesto in data['presupuestos']:
                _render_presupuesto_card(presupuesto)

    # === SECCIÓN: TOP 10 GASTOS ===
    with PageLayout.section("Top 10 Gastos del Mes", collapsible=True):
        from utils.components.tables import DataTable

        df_top10 = pd.DataFrame(data['top_10_gastos'])
        DataTable(
            df=df_top10,
            editable=False,
            height=300
        )

def _render_presupuesto_card(presupuesto: dict):
    """Helper para renderizar card de presupuesto"""
    from utils.components.metrics import MetricCard
    from utils.design_tokens import get_budget_color

    porcentaje = presupuesto['porcentaje_usado']
    emoji, color, _ = get_budget_color(porcentaje)

    MetricCard(
        label=f"{emoji} {presupuesto['categoria']}",
        value=f"{presupuesto['gastado']:.2f} € / {presupuesto['presupuesto']:.2f} €",
        delta=f"Restante: {presupuesto['restante']:.2f} €",
        delta_color="normal" if presupuesto['restante'] > 0 else "inverse",
        variant="success" if porcentaje < 70 else "warning" if porcentaje < 90 else "error",
        help_text=f"Presupuesto mensual para {presupuesto['categoria']}"
    )
```

**Comparación:**

| Aspecto | Antes | Después |
|---------|-------|---------|
| Líneas de código | ~200 líneas | ~80 líneas |
| Duplicación | Alta (cada métrica manual) | Cero (componentes) |
| Mantenibilidad | Baja (cambios en múltiples lugares) | Alta (cambio en 1 componente) |
| Consistencia | Media (estilos inline) | Alta (design tokens) |
| Separación lógica/UI | No (mezclado) | Sí (data layer separado) |
| Testing | Difícil | Fácil (componentes testeables) |

### 7.2 Ejemplo: Crear Componente Custom

**Caso de uso:** Componente para mostrar presupuestos

```python
# utils/components/budget.py
"""
Componente para mostrar presupuestos con barra de progreso
"""

import streamlit as st
from utils.design_tokens import Colors, Spacing, BorderRadius, get_budget_color
from typing import Literal

def BudgetCard(
    categoria: str,
    limite: float,
    gastado: float,
    reembolsos: float = 0.0,
    show_progress_bar: bool = True,
    variant: Literal["compact", "detailed"] = "detailed"
):
    """
    Tarjeta de presupuesto con indicador visual

    Args:
        categoria: Nombre de la categoría
        limite: Presupuesto límite
        gastado: Cantidad gastada
        reembolsos: Reembolsos aplicados
        show_progress_bar: Mostrar barra de progreso
        variant: Estilo (compact o detailed)

    Example:
        >>> BudgetCard(
        ...     categoria="DISFRUTE",
        ...     limite=800.00,
        ...     gastado=520.50,
        ...     reembolsos=20.00,
        ...     variant="detailed"
        ... )
    """

    # Calcular porcentajes
    gastado_neto = gastado - reembolsos
    porcentaje_usado = (gastado_neto / limite * 100) if limite > 0 else 0
    restante = limite - gastado_neto

    # Determinar color según porcentaje
    emoji, color, bg_color = get_budget_color(porcentaje_usado)

    # HTML según variante
    if variant == "compact":
        html = _render_compact(categoria, limite, gastado_neto, porcentaje_usado, emoji, color)
    else:
        html = _render_detailed(
            categoria, limite, gastado, gastado_neto,
            reembolsos, restante, porcentaje_usado,
            emoji, color, bg_color, show_progress_bar
        )

    st.markdown(html, unsafe_allow_html=True)

def _render_compact(categoria, limite, gastado_neto, porcentaje, emoji, color):
    """Versión compacta: Una línea"""
    return f"""
    <div style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: {Spacing.MD} {Spacing.LG};
        background: white;
        border-left: 4px solid {color};
        border-radius: {BorderRadius.BASE};
        margin-bottom: {Spacing.SM};
    ">
        <span style="font-weight: 600;">
            {emoji} {categoria}
        </span>
        <span style="color: {color}; font-weight: 600;">
            {gastado_neto:.2f}€ / {limite:.2f}€ ({porcentaje:.0f}%)
        </span>
    </div>
    """

def _render_detailed(categoria, limite, gastado_bruto, gastado_neto,
                     reembolsos, restante, porcentaje,
                     emoji, color, bg_color, show_progress_bar):
    """Versión detallada: Card completo"""

    # Barra de progreso HTML
    progress_html = ""
    if show_progress_bar:
        progress_html = f"""
        <div style="
            width: 100%;
            height: 8px;
            background: {Colors.GRAY_200};
            border-radius: 999px;
            overflow: hidden;
            margin-top: {Spacing.MD};
        ">
            <div style="
                width: {min(porcentaje, 100)}%;
                height: 100%;
                background: {color};
                transition: width 0.3s ease;
            "></div>
        </div>
        """

    return f"""
    <div style="
        background: {bg_color};
        border: 2px solid {color};
        border-radius: {BorderRadius.LG};
        padding: {Spacing.XL};
        margin-bottom: {Spacing.LG};
        box-shadow: {Colors.SHADOW_PREMIUM_SM};
    ">
        <!-- Header -->
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: {Spacing.MD};
        ">
            <h4 style="margin: 0; font-size: 1.2rem;">
                {emoji} {categoria}
            </h4>
            <span style="
                background: {color};
                color: white;
                padding: {Spacing.XS} {Spacing.MD};
                border-radius: 999px;
                font-weight: 600;
                font-size: 0.9rem;
            ">
                {porcentaje:.1f}%
            </span>
        </div>

        <!-- Métricas -->
        <div style="
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: {Spacing.MD};
            margin-bottom: {Spacing.MD};
        ">
            <div>
                <div style="font-size: 0.85rem; color: {Colors.GRAY_600};">
                    Presupuesto
                </div>
                <div style="font-size: 1.1rem; font-weight: 600;">
                    {limite:.2f} €
                </div>
            </div>
            <div>
                <div style="font-size: 0.85rem; color: {Colors.GRAY_600};">
                    Gastado
                </div>
                <div style="font-size: 1.1rem; font-weight: 600; color: {color};">
                    {gastado_neto:.2f} €
                </div>
            </div>
            <div>
                <div style="font-size: 0.85rem; color: {Colors.GRAY_600};">
                    Restante
                </div>
                <div style="font-size: 1.1rem; font-weight: 600; color: {'green' if restante > 0 else 'red'};">
                    {restante:.2f} €
                </div>
            </div>
        </div>

        <!-- Reembolsos si existen -->
        {f'''
        <div style="
            font-size: 0.85rem;
            color: {Colors.GRAY_600};
            margin-bottom: {Spacing.SM};
        ">
            💰 Reembolsos aplicados: {reembolsos:.2f} €
            (Gasto bruto: {gastado_bruto:.2f} €)
        </div>
        ''' if reembolsos > 0 else ''}

        <!-- Barra de progreso -->
        {progress_html}
    </div>
    """

# Uso en dashboard:
from utils.components.budget import BudgetCard

presupuestos = db_manager.obtener_resumen_presupuestos(mes, año)
for p in presupuestos:
    BudgetCard(
        categoria=p['categoria'],
        limite=p['presupuesto'],
        gastado=p['gastado_bruto'],
        reembolsos=p['reembolsos_asignados'],
        variant="detailed"
    )
```

---

## 8. Checklist de Implementación

### 8.1 Pre-Implementación

- [ ] Leer documento completo
- [ ] Backup de base de datos creado
- [ ] Rama `design/overhaul-incremental` creada
- [ ] Entorno virtual activado
- [ ] Dependencias actualizadas (`pip install -U streamlit plotly`)
- [ ] App funciona correctamente en estado actual
- [ ] Git working directory limpio

### 8.2 Fase 0: Preparación

- [ ] `utils/feature_flags.py` creado
- [ ] Estructura de carpetas creada:
  - [ ] `utils/components/`
  - [ ] `utils/styles/`
  - [ ] `utils/charts/`
  - [ ] `tests/`
- [ ] Todos los flags en `False`
- [ ] Tag `phase-0-complete` creado
- [ ] App funciona igual que antes

### 8.3 Fase 1: Fundamentos

#### CSS Global
- [ ] `utils/styles/global_styles.py` creado
- [ ] `utils/styles/css_injector.py` creado
- [ ] CSS extraído de app.py (400 líneas)
- [ ] Flag `USE_NEW_CSS_MODULE` implementado
- [ ] Testing con flag OFF → idéntico
- [ ] Testing con flag ON → idéntico
- [ ] Commit "feat(styles): Extract CSS to module"

#### Plotly Theme
- [ ] `utils/charts/plotly_theme.py` creado
- [ ] Colores del design system aplicados
- [ ] `apply_finanzas_theme()` función creada
- [ ] Modificados todos los gráficos en `visualizer.py`
- [ ] Flag `USE_NEW_PLOTLY_THEME` implementado
- [ ] Testing con flag OFF → gráficos iguales
- [ ] Testing con flag ON → colores nuevos, datos iguales
- [ ] Commit "feat(charts): Unified Plotly theme"

#### Separar Lógica
- [ ] `utils/dashboard_data.py` creado
- [ ] Funciones de data layer extraídas
- [ ] `mostrar_dashboard()` refactorizada
- [ ] UI separada de cálculos
- [ ] Testing funcional → resultados idénticos
- [ ] Commit "refactor(dashboard): Separate logic from UI"

- [ ] **CHECKPOINT:** Tag `phase-1-complete` creado
- [ ] App funciona con todos los flags OFF

### 8.4 Fase 2: Componentes

#### MetricCard
- [ ] `utils/components/metrics.py` creado
- [ ] Clase `MetricCard` implementada
- [ ] Función `KPIRow` implementada
- [ ] Flag `USE_METRIC_CARDS` implementado
- [ ] Aplicado en Dashboard (15 métricas)
- [ ] Aplicado en Coche Eléctrico (10 métricas)
- [ ] Aplicado en Análisis Avanzado (8 métricas)
- [ ] Testing con flag ON/OFF → valores iguales
- [ ] Commit "feat(components): Add MetricCard"

#### ChartContainer
- [ ] `utils/components/charts.py` creado
- [ ] Componente `ChartContainer` implementado
- [ ] Flag `USE_CHART_CONTAINERS` implementado
- [ ] Aplicado en todos los gráficos del Dashboard
- [ ] Aplicado en página Coche Eléctrico
- [ ] Testing con flag ON/OFF → gráficos iguales
- [ ] Commit "feat(components): Add ChartContainer"

#### FormCard
- [ ] `utils/components/forms.py` creado
- [ ] Componente `FormCard` implementado
- [ ] Flag `USE_FORM_CARDS` implementado
- [ ] Aplicado en página Añadir Gasto
- [ ] Aplicado en página Importar
- [ ] Aplicado en página Categorías
- [ ] Testing funcional → formularios funcionan
- [ ] Commit "feat(components): Add FormCard"

#### DataTable
- [ ] `utils/components/tables.py` creado
- [ ] Componente `DataTable` implementado
- [ ] Aplicado en página Transacciones
- [ ] Aplicado en página Categorías
- [ ] Testing → edición funciona correctamente
- [ ] Commit "feat(components): Add DataTable"

- [ ] **CHECKPOINT:** Tag `phase-2-complete` creado
- [ ] Todos los componentes con flags funcionando

### 8.5 Fase 3: Layouts

#### PageLayout
- [ ] `utils/components/layouts.py` creado
- [ ] Clase `PageLayout` implementada
- [ ] Método `render()` funcional
- [ ] Método `section()` funcional
- [ ] Flag `USE_PAGE_LAYOUTS` implementado
- [ ] Commit "feat(components): Add PageLayout system"

#### Grid System
- [ ] Función `Grid()` implementada
- [ ] Testing responsive (desktop)
- [ ] Aplicado en Dashboard
- [ ] Commit "feat(components): Add Grid system"

#### Responsive Utilities
- [ ] `utils/components/responsive.py` creado
- [ ] Función `responsive_columns()` implementada
- [ ] Testing en diferentes viewports
- [ ] Commit "feat(components): Add responsive utilities"

- [ ] **CHECKPOINT:** Tag `phase-3-complete` creado
- [ ] Sistema de layouts completo

### 8.6 Fase 4: Páginas v2

#### Dashboard v2
- [ ] Función `mostrar_dashboard_v2()` creada
- [ ] `PageLayout.render()` aplicado
- [ ] Métricas con `KPIRow()`
- [ ] Gráficos con `ChartContainer()`
- [ ] Presupuestos con componentes
- [ ] Flag `DASHBOARD_V2` implementado
- [ ] Testing exhaustivo (30 min)
- [ ] Valores de métricas idénticos
- [ ] Commit "feat(dashboard): Dashboard v2"

#### Transacciones v2
- [ ] Función `mostrar_transacciones_v2()` creada
- [ ] `PageLayout` aplicado
- [ ] Tabla con `DataTable()`
- [ ] Flag `TRANSACTIONS_V2` implementado
- [ ] Testing edición funciona
- [ ] Commit "feat(transactions): Transactions v2"

#### Resto de Páginas
- [ ] Importar v2 creada y testeada
- [ ] Categorías v2 creada y testeada
- [ ] Configuración v2 creada y testeada
- [ ] Coche Eléctrico v2 creada y testeada
- [ ] Asistente IA v2 creada y testeada

- [ ] **CHECKPOINT:** Tag `phase-4-complete` creado
- [ ] Todas las páginas v2 funcionando

### 8.7 Fase 5: Activación

#### Activar Flags Gradualmente
- [ ] DÍA 1: `USE_NEW_CSS_MODULE = True`
  - [ ] Testing 15 min navegando app
  - [ ] Sin errores visuales
- [ ] DÍA 1: `USE_NEW_PLOTLY_THEME = True`
  - [ ] Testing todos los gráficos
  - [ ] Colores correctos
- [ ] DÍA 2: Activar componentes (todos)
  - [ ] `USE_METRIC_CARDS = True`
  - [ ] `USE_CHART_CONTAINERS = True`
  - [ ] `USE_FORM_CARDS = True`
  - [ ] Testing 30 min navegando
- [ ] DÍA 3: Activar layouts
  - [ ] `USE_PAGE_LAYOUTS = True`
  - [ ] `USE_GRID_SYSTEM = True`
  - [ ] Testing layouts
- [ ] DÍA 4: Activar páginas v2 (una por una)
  - [ ] `DASHBOARD_V2 = True` → Testing exhaustivo
  - [ ] `TRANSACTIONS_V2 = True` → Testing
  - [ ] Resto de páginas
- [ ] Commit "feat: Enable all new design features"
- [ ] Tag `design-v2-enabled` creado

#### Usar en Producción (1 semana)
- [ ] Usar app diariamente con flags activados
- [ ] Reportar cualquier bug
- [ ] Fixear bugs encontrados
- [ ] Verificar rendimiento OK
- [ ] Sin regresiones funcionales

#### Eliminar Código Viejo
- [ ] Buscar todos `if FeatureFlags.XXX`
- [ ] Eliminar ramas `else` (código viejo)
- [ ] Eliminar checks de flags
- [ ] Eliminar funciones v1
- [ ] Renombrar funciones v2 → nombres originales
- [ ] Eliminar `utils/feature_flags.py`
- [ ] Commit "refactor: Remove old code and flags"
- [ ] Tag `design-v2-cleanup-complete` creado

#### Documentación
- [ ] `docs/DESIGN_V2_CHANGELOG.md` creado
- [ ] Screenshots antes/después capturados
- [ ] README actualizado
- [ ] Commit "docs: Add design v2 changelog"

- [ ] **FINAL:** Tag `design-v2-complete` creado

### 8.8 Post-Implementación

- [ ] Celebrar (tienes nuevo diseño premium sin bugs!)
- [ ] Recopilar feedback de usuario
- [ ] Planificar mejoras futuras (dark mode?)
- [ ] Compartir experiencia (blog post?)

---

## Resumen Ejecutivo

### TL;DR - Lo que necesitas saber

**Objetivo:** Cambiar TODO el diseño visual sin romper NADA funcional.

**Estrategia:** Migración incremental con feature flags.

**Duración:** 9 días (72 horas) de trabajo.

**Riesgo:** BAJO (rollback en cualquier momento).

**Resultado:** Diseño premium moderno con componentes reutilizables.

### Quick Start (Si tienes prisa)

```bash
# 1. Backup
cp finanzas.db finanzas.db.backup
git checkout -b design/overhaul

# 2. Crear feature flags
cat > utils/feature_flags.py << EOF
class FeatureFlags:
    USE_NEW_CSS_MODULE = False
    USE_NEW_PLOTLY_THEME = False
    USE_METRIC_CARDS = False
    USE_CHART_CONTAINERS = False
    USE_PAGE_LAYOUTS = False
    DASHBOARD_V2 = False
EOF

# 3. Implementar por fases (ver sección 4)
# 4. Activar flags gradualmente
# 5. Disfrutar diseño nuevo

# Rollback si es necesario:
git checkout main  # Vuelta instantánea
```

### Métricas de Éxito

| Métrica | Objetivo | Método |
|---------|----------|--------|
| Bugs introducidos | 0 | Testing exhaustivo |
| Downtime | 0 segundos | Feature flags |
| Líneas duplicadas | -800 | Componentes |
| Tiempo de implementación | 9 días | Fases incrementales |
| Satisfacción visual | Alta | Feedback usuario |
| Mantenibilidad | +200% | Componentes reutilizables |

---

**Documento creado:** 2025-12-04
**Versión:** 1.0
**Autor:** Claude (Anthropic)
**Para:** FinanzasFlow - Daniel

**Próximos pasos:** Leer Fase 0 y empezar implementación.

---

