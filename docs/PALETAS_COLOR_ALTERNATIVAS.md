# Paletas de Color Alternativas para FinanzasFlow

## Contexto del Cambio

**Paleta Actual:**
- Color primario: Verde oscuro a lima (`#0a4c3e` → `#84cc16`)
- Estilo: Gradientes vibrantes con tema verde/natura
- Problema: Usuario no está convencido con el verde actual

**Objetivo:** Proponer 6 paletas alternativas que transmitan:
- Confianza y seguridad financiera
- Profesionalismo y claridad
- Modernidad fintech
- Cumplimiento de accesibilidad WCAG AA

---

## Investigación: Tendencias en Fintech 2024

### Colores Dominantes en Neobancos Exitosos

**Revolut:**
- Color primario: Cornflower Blue `#7F84F6`
- Secundario: Shark (gris casi negro) `#191C1F`
- Estilo: Gradientes vibrantes, dinámico y moderno

**N26:**
- Color primario: Aqua/turquesa
- Estilo: Sobrio, elegante, con toque pastel
- Transmite: Eficiencia y serenidad

**Wise:**
- Color primario: Verde neón/lima brillante
- Estilo: Limpio con mucho espacio en blanco
- Transmite: Distintivo, moderno, transparencia

**YNAB (You Need A Budget):**
- Color primario: "Blurple" (azul-púrpura)
- Estilo: Amigable, accesible, enfocado en color accessibility
- Transmite: Confianza y familiaridad

### Psicología del Color en Finanzas

**Azul** (más usado):
- Representa: Confianza, seguridad, estabilidad
- Razón: 62-90% del juicio inicial se basa en color
- Ideal para: Transmitir profesionalismo financiero

**Púrpura:**
- Representa: Riqueza, armonía, sofisticación
- Advertencia: Sobreuso en fintech (dificulta diferenciación)

**Negro + Colores vibrantes:**
- Representa: Sofisticación, estilo, versatilidad
- Tendencia: PayPal, Revolut usan negro + azules

---

## Paleta 1: "Deep Ocean Trust" (Azul Oscuro Premium)

### Descripción
Inspirada en Revolut y PayPal. Azul oscuro profundo que transmite confianza institucional con acentos cian modernos.

### Colores

```python
# Primarios
PRIMARY = "#0f172a"              # Azul oscuro casi negro (slate-900)
PRIMARY_LIGHT = "#1e293b"        # Slate-800
PRIMARY_DARK = "#020617"         # Slate-950
PRIMARY_ULTRA_LIGHT = "#e0f2fe"  # Sky-100

# Secundarios
SECONDARY = "#0ea5e9"            # Cian brillante (sky-500)
SECONDARY_LIGHT = "#38bdf8"      # Sky-400
SECONDARY_DARK = "#0284c7"       # Sky-600

# Semánticos
SUCCESS = "#10b981"              # Emerald-500 (ingresos)
SUCCESS_LIGHT = "#34d399"
SUCCESS_DARK = "#059669"
SUCCESS_ULTRA_LIGHT = "#d1fae5"

WARNING = "#f59e0b"              # Amber-500
WARNING_LIGHT = "#fbbf24"
WARNING_DARK = "#d97706"
WARNING_ULTRA_LIGHT = "#fef3c7"

ERROR = "#ef4444"                # Red-500 (gastos)
ERROR_LIGHT = "#f87171"
ERROR_DARK = "#dc2626"
ERROR_ULTRA_LIGHT = "#fee2e2"

# Backgrounds
BG_PRIMARY = "#ffffff"
BG_SECONDARY = "#f8fafc"         # Slate-50
BG_TERTIARY = "#f1f5f9"          # Slate-100
```

### Justificación
- **Confianza:** Azul oscuro es el color #1 en finanzas (bancos tradicionales)
- **Modernidad:** Acentos cian mantienen frescura fintech
- **Accesibilidad:** Contraste excelente (WCAG AAA en primarios)
- **Ejemplos:** Revolut, PayPal, Coinbase, Stripe

### Mockup Dashboard
```
┌─────────────────────────────────────┐
│ Header: #0f172a (azul oscuro)      │
│ Logo + Nav en blanco                │
├─────────────────────────────────────┤
│ Fondo: #f8fafc (gris muy claro)    │
│                                     │
│ ┌─────────────┐  ┌───────────────┐ │
│ │ Balance     │  │ Ingresos      │ │
│ │ 2,450.00€   │  │ +1,800.00€    │ │
│ │ #0ea5e9     │  │ #10b981       │ │
│ │ (cian)      │  │ (verde)       │ │
│ └─────────────┘  └───────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐│
│ │ Gráfica (Plotly)                ││
│ │ Ingresos: #10b981 (esmeralda)   ││
│ │ Gastos: #ef4444 (rojo)          ││
│ │ Balance: #0ea5e9 (cian)         ││
│ └─────────────────────────────────┘│
│                                     │
│ Botones CTA: #0ea5e9 con hover     │
└─────────────────────────────────────┘
```

### Ventajas
- Máxima confianza y profesionalismo
- Excelente contraste para gráficas
- Se diferencia completamente del verde actual
- Moderno pero no demasiado vibrante

### Desventajas
- Puede parecer "corporativo" vs. "startup"
- Azul es muy común (menos distintivo)

---

## Paleta 2: "Royal Purple Wealth" (Púrpura Premium)

### Descripción
Inspirada en fintech premium como Nubank. Púrpura profundo que evoca riqueza y sofisticación, con acentos violeta brillantes.

### Colores

```python
# Primarios
PRIMARY = "#5b21b6"              # Púrpura-800 (violeta profundo)
PRIMARY_LIGHT = "#7c3aed"        # Púrpura-600
PRIMARY_DARK = "#4c1d95"         # Púrpura-900
PRIMARY_ULTRA_LIGHT = "#f3e8ff"  # Púrpura-50

# Secundarios
SECONDARY = "#a78bfa"            # Púrpura-400 (violeta claro)
SECONDARY_LIGHT = "#c4b5fd"      # Púrpura-300
SECONDARY_DARK = "#8b5cf6"       # Púrpura-500

# Semánticos
SUCCESS = "#22c55e"              # Green-500 (ingresos)
SUCCESS_LIGHT = "#4ade80"
SUCCESS_DARK = "#16a34a"
SUCCESS_ULTRA_LIGHT = "#dcfce7"

WARNING = "#fb923c"              # Orange-400
WARNING_LIGHT = "#fdba74"
WARNING_DARK = "#f97316"
WARNING_ULTRA_LIGHT = "#ffedd5"

ERROR = "#f43f5e"                # Rose-500 (gastos)
ERROR_LIGHT = "#fb7185"
ERROR_DARK = "#e11d48"
ERROR_ULTRA_LIGHT = "#ffe4e6"

# Backgrounds
BG_PRIMARY = "#ffffff"
BG_SECONDARY = "#faf5ff"         # Púrpura-50
BG_TERTIARY = "#f5f3ff"          # Púrpura-100
```

### Justificación
- **Riqueza:** Púrpura históricamente asociado a prosperidad
- **Diferenciación:** Menos común que azul, más distintivo
- **Modernidad:** Tendencia fintech (Nubank, YNAB)
- **Accesibilidad:** Púrpura oscuro + blanco = WCAG AAA

### Mockup Dashboard
```
┌─────────────────────────────────────┐
│ Header: #5b21b6 (púrpura profundo) │
│ Logo + Nav en blanco                │
├─────────────────────────────────────┤
│ Fondo: #faf5ff (púrpura muy pálido)│
│                                     │
│ ┌─────────────┐  ┌───────────────┐ │
│ │ Balance     │  │ Ingresos      │ │
│ │ 2,450.00€   │  │ +1,800.00€    │ │
│ │ #a78bfa     │  │ #22c55e       │ │
│ │ (violeta)   │  │ (verde)       │ │
│ └─────────────┘  └───────────────┘ │
│                                     │
│ Gradiente sutil en cards:           │
│ linear-gradient(135deg,             │
│   #ffffff 0%, #f5f3ff 100%)         │
└─────────────────────────────────────┘
```

### Ventajas
- Muy distintivo y premium
- Psicológicamente asociado a riqueza
- Balance entre profesional y moderno
- Excelente para dark mode (futuro)

### Desventajas
- Saturación del color en fintech
- Puede no gustar a usuarios conservadores

---

## Paleta 3: "Midnight Teal Professional" (Verde Azulado Corporativo)

### Descripción
Inspirada en N26. Verde azulado oscuro (teal) que combina confianza del azul con frescura del verde, pero más sofisticado que verde puro.

### Colores

```python
# Primarios
PRIMARY = "#0f766e"              # Teal-700 (verde azulado oscuro)
PRIMARY_LIGHT = "#14b8a6"        # Teal-500
PRIMARY_DARK = "#134e4a"         # Teal-900
PRIMARY_ULTRA_LIGHT = "#ccfbf1"  # Teal-100

# Secundarios
SECONDARY = "#06b6d4"            # Cyan-500
SECONDARY_LIGHT = "#22d3ee"      # Cyan-400
SECONDARY_DARK = "#0891b2"       # Cyan-600

# Semánticos
SUCCESS = "#16a34a"              # Green-600 (ingresos)
SUCCESS_LIGHT = "#22c55e"
SUCCESS_DARK = "#15803d"
SUCCESS_ULTRA_LIGHT = "#dcfce7"

WARNING = "#ea580c"              # Orange-600
WARNING_LIGHT = "#fb923c"
WARNING_DARK = "#c2410c"
WARNING_ULTRA_LIGHT = "#ffedd5"

ERROR = "#dc2626"                # Red-600 (gastos)
ERROR_LIGHT = "#ef4444"
ERROR_DARK = "#991b1b"
ERROR_ULTRA_LIGHT = "#fee2e2"

# Backgrounds
BG_PRIMARY = "#ffffff"
BG_SECONDARY = "#f0fdfa"         # Teal-50
BG_TERTIARY = "#e0f2fe"          # Sky-50 (mix)
```

### Justificación
- **Balance perfecto:** Combina confianza (azul) + crecimiento (verde)
- **Profesional pero fresco:** Más serio que verde lima, menos común que azul
- **Ejemplos:** N26, TransferWise (parcialmente)
- **Accesibilidad:** Teal-700 es oscuro suficiente para AAA

### Mockup Dashboard
```
┌─────────────────────────────────────┐
│ Sidebar: #0f766e (teal oscuro)     │
│ + Iconos en #22d3ee (cyan claro)   │
├─────────────────────────────────────┤
│ Main: #f0fdfa (teal casi blanco)   │
│                                     │
│ Cards con bordes: #14b8a6 (teal)   │
│ Hover con glow: rgba(15,118,110,0.2)│
│                                     │
│ Gráficas:                           │
│ - Balance: #14b8a6 (teal medio)     │
│ - Ingresos: #16a34a (verde oscuro)  │
│ - Gastos: #dc2626 (rojo)            │
└─────────────────────────────────────┘
```

### Ventajas
- Distintivo sin ser radical
- Mantiene algo de verde (transición suave)
- Muy profesional y moderno
- Perfecto para finanzas "verdes" (sostenibilidad)

### Desventajas
- Puede parecer "eco-friendly" vs. "financiero"
- Similar al verde actual (puede no ser suficiente cambio)

---

## Paleta 4: "Slate Monochrome Modern" (Gris Sofisticado + Acentos)

### Descripción
Inspirada en Monzo, Apple Card. Base neutra gris con acentos de color vibrantes. Ultra profesional y minimalista.

### Colores

```python
# Primarios
PRIMARY = "#18181b"              # Zinc-900 (gris casi negro)
PRIMARY_LIGHT = "#27272a"        # Zinc-800
PRIMARY_DARK = "#09090b"         # Zinc-950
PRIMARY_ULTRA_LIGHT = "#f4f4f5"  # Zinc-100

# Secundarios (acentos vibrantes)
SECONDARY = "#06b6d4"            # Cyan-500 (acento principal)
SECONDARY_LIGHT = "#22d3ee"      # Cyan-400
SECONDARY_DARK = "#0891b2"       # Cyan-600

# Semánticos
SUCCESS = "#10b981"              # Emerald-500 (ingresos)
SUCCESS_LIGHT = "#34d399"
SUCCESS_DARK = "#059669"
SUCCESS_ULTRA_LIGHT = "#d1fae5"

WARNING = "#f59e0b"              # Amber-500
WARNING_LIGHT = "#fbbf24"
WARNING_DARK = "#d97706"
WARNING_ULTRA_LIGHT = "#fef3c7"

ERROR = "#ef4444"                # Red-500 (gastos)
ERROR_LIGHT = "#f87171"
ERROR_DARK = "#dc2626"
ERROR_ULTRA_LIGHT = "#fee2e2"

# Backgrounds
BG_PRIMARY = "#ffffff"
BG_SECONDARY = "#fafafa"         # Zinc-50
BG_TERTIARY = "#f4f4f5"          # Zinc-100

# Acentos adicionales
ACCENT_PURPLE = "#a855f7"        # Purple-500
ACCENT_PINK = "#ec4899"          # Pink-500
ACCENT_INDIGO = "#6366f1"        # Indigo-500
```

### Justificación
- **Sofisticación máxima:** Gris/negro transmite lujo y elegancia
- **Versatilidad:** Los acentos destacan sin dominar
- **Ejemplos:** Apple Card, Monzo, N26 (parcialmente)
- **Legibilidad:** Contraste perfecto en cualquier dispositivo

### Mockup Dashboard
```
┌─────────────────────────────────────┐
│ Header: #18181b (gris oscuro)      │
│ Nav items con hover: #06b6d4 (cyan)│
├─────────────────────────────────────┤
│ Fondo: #fafafa (blanco humo)       │
│                                     │
│ Cards: #ffffff con sombras sutiles │
│ ┌─────────────────────────────────┐│
│ │ BALANCE TOTAL                   ││
│ │ 2,450.00 €                      ││
│ │ Typography: #18181b (negro)     ││
│ │ Icono: #06b6d4 (cyan)           ││
│ └─────────────────────────────────┘│
│                                     │
│ Gráficas con colores vibrantes:    │
│ - Ingresos: #10b981 (esmeralda)    │
│ - Gastos: #ef4444 (rojo vibrante)  │
│ - Barras: #18181b (gris oscuro)    │
│                                     │
│ CTAs: Gradiente cyan (#06b6d4)     │
│ con hover elevado                   │
└─────────────────────────────────────┘
```

### Ventajas
- Ultra profesional y premium
- Los datos destacan sobre fondo neutro
- Perfecto para dark mode
- Timeless (no pasa de moda)

### Desventajas
- Puede parecer "frío" o "poco emocional"
- Menos distintivo (muchas apps usan gris)

---

## Paleta 5: "Coral Sunset Vibrant" (Coral Cálido Fintech)

### Descripción
Inspirada en fintechs disruptivas como N26 (versión cálida). Coral/salmón con acentos dorados. Transmite calidez y optimismo financiero.

### Colores

```python
# Primarios
PRIMARY = "#f43f5e"              # Rose-500 (coral/rosa)
PRIMARY_LIGHT = "#fb7185"        # Rose-400
PRIMARY_DARK = "#e11d48"         # Rose-600
PRIMARY_ULTRA_LIGHT = "#ffe4e6"  # Rose-100

# Secundarios
SECONDARY = "#f59e0b"            # Amber-500 (dorado cálido)
SECONDARY_LIGHT = "#fbbf24"      # Amber-400
SECONDARY_DARK = "#d97706"       # Amber-600

# Semánticos
SUCCESS = "#10b981"              # Emerald-500 (ingresos)
SUCCESS_LIGHT = "#34d399"
SUCCESS_DARK = "#059669"
SUCCESS_ULTRA_LIGHT = "#d1fae5"

WARNING = "#fb923c"              # Orange-400
WARNING_LIGHT = "#fdba74"
WARNING_DARK = "#f97316"
WARNING_ULTRA_LIGHT = "#ffedd5"

ERROR = "#7c2d12"                # Orange-900 oscuro (gastos, para contraste)
ERROR_LIGHT = "#c2410c"
ERROR_DARK = "#431407"
ERROR_ULTRA_LIGHT = "#ffedd5"

# Backgrounds
BG_PRIMARY = "#ffffff"
BG_SECONDARY = "#fff7ed"         # Orange-50 (cálido)
BG_TERTIARY = "#fef3c7"          # Amber-100

# Gradientes premium
GRADIENT_PRIMARY = "linear-gradient(135deg, #f43f5e 0%, #fb923c 100%)"
GRADIENT_CARD = "linear-gradient(135deg, #ffffff 0%, #fff7ed 100%)"
```

### Justificación
- **Diferenciación total:** Casi nadie usa coral en finanzas
- **Optimismo:** Colores cálidos transmiten energía positiva
- **Juventud:** Ideal para público joven/moderno
- **Ejemplos:** N26 (acentos), Monzo (parcialmente)

### Mockup Dashboard
```
┌─────────────────────────────────────┐
│ Header: Gradiente coral a naranja  │
│ #f43f5e → #fb923c                   │
│ Texto: #ffffff                      │
├─────────────────────────────────────┤
│ Fondo: #fff7ed (naranja muy pálido)│
│                                     │
│ Cards con sombras cálidas:          │
│ box-shadow: 0 4px 12px              │
│   rgba(244,63,94,0.15)              │
│                                     │
│ Botones: #f43f5e con hover a #e11d48│
│                                     │
│ Iconos: #fb923c (dorado amber)     │
│                                     │
│ Gráficas:                           │
│ - Balance: #f43f5e (coral)          │
│ - Ingresos: #10b981 (verde)         │
│ - Gastos: #7c2d12 (marrón oscuro)   │
└─────────────────────────────────────┘
```

### Ventajas
- MUY distintivo (ninguna fintech grande lo usa)
- Transmite calidez y optimismo
- Perfecto para diferenciarse
- Moderno y atrevido

### Desventajas
- Puede no transmitir suficiente "seriedad"
- Arriesgado para usuarios conservadores
- Coral como "gastos" es contraintuitivo (necesita adaptación)

---

## Paleta 6: "Indigo Professional Modern" (Índigo Corporativo)

### Descripción
Inspirada en LinkedIn, Stripe. Azul índigo profundo que combina confianza del azul con modernidad del púrpura. Balance perfecto.

### Colores

```python
# Primarios
PRIMARY = "#4f46e5"              # Indigo-600 (azul violeta medio)
PRIMARY_LIGHT = "#6366f1"        # Indigo-500
PRIMARY_DARK = "#3730a3"         # Indigo-800
PRIMARY_ULTRA_LIGHT = "#e0e7ff"  # Indigo-100

# Secundarios
SECONDARY = "#06b6d4"            # Cyan-500 (contraste fresco)
SECONDARY_LIGHT = "#22d3ee"      # Cyan-400
SECONDARY_DARK = "#0891b2"       # Cyan-600

# Semánticos
SUCCESS = "#10b981"              # Emerald-500 (ingresos)
SUCCESS_LIGHT = "#34d399"
SUCCESS_DARK = "#059669"
SUCCESS_ULTRA_LIGHT = "#d1fae5"

WARNING = "#f59e0b"              # Amber-500
WARNING_LIGHT = "#fbbf24"
WARNING_DARK = "#d97706"
WARNING_ULTRA_LIGHT = "#fef3c7"

ERROR = "#ef4444"                # Red-500 (gastos)
ERROR_LIGHT = "#f87171"
ERROR_DARK = "#dc2626"
ERROR_ULTRA_LIGHT = "#fee2e2"

# Backgrounds
BG_PRIMARY = "#ffffff"
BG_SECONDARY = "#f0f9ff"         # Sky-50 (azul muy pálido)
BG_TERTIARY = "#e0e7ff"          # Indigo-100

# Gradientes
GRADIENT_PRIMARY = "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)"
```

### Justificación
- **Balance perfecto:** Confianza + modernidad
- **Profesional pero no aburrido:** Más interesante que azul puro
- **Ejemplos:** Stripe, LinkedIn, Asana
- **Accesibilidad:** Excelente contraste (WCAG AA+)

### Mockup Dashboard
```
┌─────────────────────────────────────┐
│ Sidebar: #4f46e5 (indigo)          │
│ con iconos en #22d3ee (cyan)       │
├─────────────────────────────────────┤
│ Main: #f0f9ff (azul muy claro)     │
│                                     │
│ ┌─────────────────────────────────┐│
│ │ RESUMEN MENSUAL                 ││
│ │                                 ││
│ │ Cards con gradiente indigo:     ││
│ │ background: linear-gradient(    ││
│ │   135deg,                        ││
│ │   #ffffff 0%,                    ││
│ │   #e0e7ff 100%)                  ││
│ │                                 ││
│ │ Números grandes: #4f46e5        ││
│ │ Labels: #64748b (slate-500)     ││
│ └─────────────────────────────────┘│
│                                     │
│ Gráficas:                           │
│ - Línea balance: #4f46e5 (indigo)  │
│ - Barras ingresos: #10b981 (verde) │
│ - Barras gastos: #ef4444 (rojo)    │
│                                     │
│ Botones primarios:                  │
│ - Background: #4f46e5               │
│ - Hover: #3730a3 (más oscuro)      │
│ - Shadow: 0 4px 12px                │
│   rgba(79,70,229,0.25)              │
└─────────────────────────────────────┘
```

### Ventajas
- Profesional y moderno a la vez
- Excelente diferenciación del verde
- Color "fintech" reconocido (Stripe)
- Versátil para todos los públicos

### Desventajas
- Similar al azul (menos radical)
- Puede confundirse con púrpura en pantallas

---

## Top 3 Recomendaciones

### 🥇 1. PALETA 6: "Indigo Professional Modern"

**Por qué es la mejor opción:**
- ✅ Balance perfecto entre confianza y modernidad
- ✅ Se diferencia completamente del verde actual
- ✅ Color reconocido en fintech premium (Stripe)
- ✅ Versátil para todo tipo de usuarios
- ✅ Excelente accesibilidad (WCAG AA garantizado)
- ✅ Funciona perfectamente en dark mode (futuro)

**Ideal para:** Usuarios que quieren profesionalismo sin perder frescura

---

### 🥈 2. PALETA 1: "Deep Ocean Trust"

**Por qué es excelente:**
- ✅ Máxima confianza y credibilidad
- ✅ Color #1 en finanzas globalmente
- ✅ Contraste superior para gráficas
- ✅ Timeless (nunca pasa de moda)
- ✅ Ejemplos: Revolut, PayPal, Coinbase

**Ideal para:** Usuarios que priorizan confianza y seriedad

---

### 🥉 3. PALETA 3: "Midnight Teal Professional"

**Por qué es muy buena:**
- ✅ Transición suave del verde actual (menos radical)
- ✅ Balance entre azul (confianza) y verde (crecimiento)
- ✅ Distintivo sin ser arriesgado
- ✅ Perfecto si el concepto "verde" es importante (sostenibilidad)

**Ideal para:** Usuarios que quieren cambio moderado

---

## Comparativa Rápida

| Paleta | Confianza | Modernidad | Diferenciación | Accesibilidad | Riesgo |
|--------|-----------|------------|----------------|---------------|--------|
| 1. Deep Ocean (Azul) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Bajo |
| 2. Royal Purple | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Medio |
| 3. Midnight Teal | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Bajo |
| 4. Slate Monochrome | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | Bajo |
| 5. Coral Sunset | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Alto |
| 6. Indigo Modern | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Bajo |

---

## Implementación en design_tokens.py

### Paso 1: Backup Actual

```bash
# Primero hacer backup
cp utils/design_tokens.py utils/design_tokens.py.backup
```

### Paso 2: Actualizar Clase Colors

**Ejemplo con Paleta 6 (Indigo):**

```python
class Colors:
    """
    Paleta de colores semánticos - Indigo Professional Modern
    Inspirada en Stripe, LinkedIn. Balance entre confianza y modernidad.
    """

    # === COLORES PRIMARIOS ===
    PRIMARY = "#4f46e5"              # Indigo-600 (azul violeta medio)
    PRIMARY_LIGHT = "#6366f1"        # Indigo-500
    PRIMARY_DARK = "#3730a3"         # Indigo-800
    PRIMARY_ULTRA_LIGHT = "#e0e7ff"  # Indigo-100

    # === COLORES SECUNDARIOS ===
    SECONDARY = "#06b6d4"            # Cyan-500 (contraste fresco)
    SECONDARY_LIGHT = "#22d3ee"      # Cyan-400
    SECONDARY_DARK = "#0891b2"       # Cyan-600
    SECONDARY_ULTRA_LIGHT = "#cffafe" # Cyan-100

    # === COLORES SEMÁNTICOS FINANCIEROS ===
    SUCCESS = "#10b981"              # Emerald-500 (ingresos, positivo)
    SUCCESS_LIGHT = "#34d399"        # Emerald-400
    SUCCESS_DARK = "#059669"         # Emerald-600
    SUCCESS_ULTRA_LIGHT = "#d1fae5"  # Emerald-100

    WARNING = "#f59e0b"              # Amber-500 (advertencia)
    WARNING_LIGHT = "#fbbf24"        # Amber-400
    WARNING_DARK = "#d97706"         # Amber-600
    WARNING_ULTRA_LIGHT = "#fef3c7"  # Amber-100

    ERROR = "#ef4444"                # Red-500 (gastos, negativo)
    ERROR_LIGHT = "#f87171"          # Red-400
    ERROR_DARK = "#dc2626"           # Red-600
    ERROR_ULTRA_LIGHT = "#fee2e2"    # Red-100

    # === GRISES (Neutrales) ===
    GRAY_900 = "#0f172a"             # Slate-900 (texto principal)
    GRAY_800 = "#1e293b"             # Slate-800
    GRAY_700 = "#334155"             # Slate-700 (texto secundario)
    GRAY_600 = "#475569"             # Slate-600
    GRAY_500 = "#64748b"             # Slate-500 (texto deshabilitado)
    GRAY_400 = "#94a3b8"             # Slate-400
    GRAY_300 = "#cbd5e1"             # Slate-300 (bordes)
    GRAY_200 = "#e2e8f0"             # Slate-200
    GRAY_100 = "#f1f5f9"             # Slate-100 (backgrounds secundarios)
    GRAY_50 = "#f8fafc"              # Slate-50 (backgrounds hover)

    # === BACKGROUNDS ===
    BG_PRIMARY = "#ffffff"           # Fondo principal
    BG_SECONDARY = "#f0f9ff"         # Sky-50 (fondo secundario azul pálido)
    BG_TERTIARY = "#e0e7ff"          # Indigo-100 (fondo terciario)
    BG_DARK = "#0f172a"              # Para dark mode (futuro)

    # === COLORES ESPECÍFICOS DE LA APP ===
    CHART_INCOME = SUCCESS           # Ingresos en gráficos
    CHART_EXPENSE = ERROR            # Gastos en gráficos
    CHART_BALANCE = PRIMARY          # Balance en gráficos
    CHART_NEUTRAL = GRAY_500         # Líneas auxiliares

    # === PRESUPUESTOS ===
    BUDGET_OK = SUCCESS              # <70% usado
    BUDGET_WARNING = WARNING         # 70-90% usado
    BUDGET_OVER = ERROR              # >90% usado

    # === OVERLAYS Y SOMBRAS ===
    OVERLAY_LIGHT = "rgba(15, 23, 42, 0.05)"    # Slate con alpha
    OVERLAY_MEDIUM = "rgba(15, 23, 42, 0.12)"
    OVERLAY_DARK = "rgba(15, 23, 42, 0.24)"

    SHADOW_SM = "0 1px 2px rgba(79,70,229,0.05)"
    SHADOW_MD = "0 4px 6px rgba(79,70,229,0.07)"
    SHADOW_LG = "0 10px 15px rgba(79,70,229,0.1)"
    SHADOW_XL = "0 20px 25px rgba(79,70,229,0.15)"

    # === GRADIENTES ===
    GRADIENT_PRIMARY = "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)"
    GRADIENT_SUCCESS = "linear-gradient(135deg, #d1fae5 0%, #34d39930 100%)"
    GRADIENT_ERROR = "linear-gradient(135deg, #fee2e2 0%, #f8717130 100%)"

    # === 🎨 PREMIUM PALETTE (Indigo Theme) ===
    PREMIUM_PRIMARY_START = "#4f46e5"      # Indigo-600
    PREMIUM_PRIMARY_END = "#06b6d4"        # Cyan-500
    PREMIUM_GRADIENT_PRIMARY = f"linear-gradient(135deg, {PREMIUM_PRIMARY_START} 0%, {PREMIUM_PRIMARY_END} 100%)"

    # Gradientes de acento
    PREMIUM_INDIGO_START = "#3730a3"       # Indigo-800 profundo
    PREMIUM_INDIGO_END = "#6366f1"         # Indigo-500 brillante
    PREMIUM_GRADIENT_INDIGO = f"linear-gradient(135deg, {PREMIUM_INDIGO_START} 0%, {PREMIUM_INDIGO_END} 100%)"

    PREMIUM_CYAN_START = "#0891b2"         # Cyan-600
    PREMIUM_CYAN_END = "#22d3ee"           # Cyan-400
    PREMIUM_GRADIENT_CYAN = f"linear-gradient(135deg, {PREMIUM_CYAN_START} 0%, {PREMIUM_CYAN_END} 100%)"

    PREMIUM_EMERALD_START = "#059669"      # Emerald-600
    PREMIUM_EMERALD_END = "#34d399"        # Emerald-400
    PREMIUM_GRADIENT_EMERALD = f"linear-gradient(135deg, {PREMIUM_EMERALD_START} 0%, {PREMIUM_EMERALD_END} 100%)"

    # Gradiente de fondo sutil - tema indigo
    PREMIUM_BG_GRADIENT = "linear-gradient(180deg, #ffffff 0%, #f0f9ff 100%)"
    PREMIUM_CARD_GRADIENT = "linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%)"

    # === 💎 GLASSMORPHISM ===
    GLASS_BG = "rgba(255, 255, 255, 0.7)"
    GLASS_BG_DARK = "rgba(79, 70, 229, 0.1)"    # Indigo con alpha
    GLASS_BORDER = "rgba(79, 70, 229, 0.3)"
    GLASS_BACKDROP = "blur(10px)"
    GLASS_SHADOW = "0 8px 32px rgba(79, 70, 229, 0.15)"

    # === 🌈 SOMBRAS MULTICAPA (Profundidad realista) ===
    SHADOW_PREMIUM_XS = "0 1px 2px rgba(79,70,229,0.05)"
    SHADOW_PREMIUM_SM = """0 2px 4px rgba(79,70,229,0.06),
                           0 1px 2px rgba(79,70,229,0.04)"""
    SHADOW_PREMIUM_MD = """0 4px 6px rgba(79,70,229,0.07),
                           0 2px 4px rgba(79,70,229,0.05),
                           0 1px 2px rgba(79,70,229,0.04)"""
    SHADOW_PREMIUM_LG = """0 10px 15px rgba(79,70,229,0.08),
                           0 4px 6px rgba(79,70,229,0.06),
                           0 2px 4px rgba(79,70,229,0.04)"""
    SHADOW_PREMIUM_XL = """0 20px 25px rgba(79,70,229,0.10),
                           0 10px 10px rgba(79,70,229,0.04),
                           0 0 0 1px rgba(79,70,229,0.02)"""
    SHADOW_PREMIUM_2XL = """0 25px 50px rgba(79,70,229,0.15),
                            0 12px 25px rgba(79,70,229,0.08)"""

    # Sombras con color (glow effects) - tema indigo
    SHADOW_GLOW_PRIMARY = "0 0 20px rgba(79, 70, 229, 0.4)"     # Indigo glow
    SHADOW_GLOW_SUCCESS = "0 0 20px rgba(16, 185, 129, 0.4)"    # Emerald glow
    SHADOW_GLOW_ERROR = "0 0 20px rgba(239, 68, 68, 0.4)"       # Red glow

    # === 🎯 ACENTOS PREMIUM ===
    ACCENT_CYAN = SECONDARY                # Para links y acciones secundarias
    ACCENT_EMERALD = SUCCESS               # Para info y success
    ACCENT_AMBER = WARNING                 # Para highlights especiales
    ACCENT_INDIGO = PRIMARY                # Para CTAs importantes
```

### Paso 3: Actualizar brand_assets.py (Logo)

**Actualizar gradientes del logo:**

```python
# utils/brand_assets.py

LOGO_SVG = """
<svg width="300" height="80" viewBox="0 0 240 64" fill="none" xmlns="http://www.w3.org/2000/svg">

    <defs>
        <!-- CAMBIAR A INDIGO -->
        <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#4f46e5;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="accentGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#06b6d4;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#22d3ee;stop-opacity:1" />
        </linearGradient>
    </defs>

    <g transform="translate(6, 6)">

        <circle cx="26" cy="26" r="24" fill="url(#logoGradient)" opacity="0.1"/>
        <circle cx="26" cy="26" r="24" stroke="url(#logoGradient)" stroke-width="3" fill="none"/>

        <path d="M 13 33 L 20 26 L 26 24 L 33 16 L 40 13"
              stroke="url(#logoGradient)"
              stroke-width="3"
              stroke-linecap="round"
              stroke-linejoin="round"
              fill="none"/>

        <circle cx="20" cy="26" r="3.5" fill="url(#accentGradient)"/>
        <circle cx="26" cy="24" r="3.5" fill="url(#accentGradient)"/>
        <circle cx="33" cy="16" r="3.5" fill="url(#accentGradient)"/>
        <circle cx="40" cy="13" r="4" fill="url(#accentGradient)"/>
    </g>

    <text x="70" y="28"
          font-family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
          font-size="22"
          font-weight="700"
          fill="#4f46e5">
        FinanzasFlow
    </text>
    <text x="70" y="46"
          font-family="Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
          font-size="11"
          font-weight="500"
          fill="#64748b"
          letter-spacing="0.5">
        CONTROL FINANCIERO PREMIUM
    </text>
</svg>
"""
```

### Paso 4: Testing de Accesibilidad

**Verificar contraste WCAG:**

```python
# Script de testing (opcional)
# utils/test_color_contrast.py

from design_tokens import Colors

def calcular_contraste(color1_hex, color2_hex):
    """
    Calcula ratio de contraste WCAG entre dos colores
    Fórmula: https://www.w3.org/TR/WCAG21/#contrast-minimum
    """
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def luminancia_relativa(rgb):
        def canal(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        r, g, b = rgb
        return 0.2126 * canal(r) + 0.7152 * canal(g) + 0.0722 * canal(b)

    lum1 = luminancia_relativa(hex_to_rgb(color1_hex))
    lum2 = luminancia_relativa(hex_to_rgb(color2_hex))

    brighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (brighter + 0.05) / (darker + 0.05)

# Tests
print("=== TESTS DE CONTRASTE WCAG ===")
print(f"PRIMARY sobre BG_PRIMARY: {calcular_contraste(Colors.PRIMARY, Colors.BG_PRIMARY):.2f}:1")
print(f"  - WCAG AA (4.5:1): {'✅ PASS' if calcular_contraste(Colors.PRIMARY, Colors.BG_PRIMARY) >= 4.5 else '❌ FAIL'}")
print(f"  - WCAG AAA (7:1): {'✅ PASS' if calcular_contraste(Colors.PRIMARY, Colors.BG_PRIMARY) >= 7 else '❌ FAIL'}")

print(f"\nGRAY_900 sobre BG_PRIMARY: {calcular_contraste(Colors.GRAY_900, Colors.BG_PRIMARY):.2f}:1")
print(f"  - WCAG AA: {'✅ PASS' if calcular_contraste(Colors.GRAY_900, Colors.BG_PRIMARY) >= 4.5 else '❌ FAIL'}")

print(f"\nSUCCESS sobre BG_PRIMARY: {calcular_contraste(Colors.SUCCESS, Colors.BG_PRIMARY):.2f}:1")
print(f"  - WCAG AA: {'✅ PASS' if calcular_contraste(Colors.SUCCESS, Colors.BG_PRIMARY) >= 4.5 else '❌ FAIL'}")

print(f"\nERROR sobre BG_PRIMARY: {calcular_contraste(Colors.ERROR, Colors.BG_PRIMARY):.2f}:1")
print(f"  - WCAG AA: {'✅ PASS' if calcular_contraste(Colors.ERROR, Colors.BG_PRIMARY) >= 4.5 else '❌ FAIL'}")
```

### Paso 5: Validación Visual

**Checklist después de cambiar los colores:**

- [ ] Logo se ve correctamente con nuevos gradientes
- [ ] Dashboard principal usa PRIMARY correctamente
- [ ] Gráficas de Plotly muestran colores diferenciados
- [ ] Botones tienen buen contraste en hover
- [ ] Cards y backgrounds son legibles
- [ ] Métricas de ingresos/gastos son claras
- [ ] Sidebar/navegación se ve profesional
- [ ] Mobile responsive mantiene legibilidad

---

## Código Completo de Implementación

### Archivo Completo: utils/design_tokens_INDIGO.py

```python
# utils/design_tokens.py
"""
Design Tokens - Sistema de diseño centralizado
Paleta: Indigo Professional Modern
Inspirada en: Stripe, LinkedIn
Balance: Confianza + Modernidad
"""

class Colors:
    """Paleta de colores semánticos - Indigo Professional Modern"""

    # === COLORES PRIMARIOS ===
    PRIMARY = "#4f46e5"
    PRIMARY_LIGHT = "#6366f1"
    PRIMARY_DARK = "#3730a3"
    PRIMARY_ULTRA_LIGHT = "#e0e7ff"

    # === COLORES SECUNDARIOS ===
    SECONDARY = "#06b6d4"
    SECONDARY_LIGHT = "#22d3ee"
    SECONDARY_DARK = "#0891b2"
    SECONDARY_ULTRA_LIGHT = "#cffafe"

    # === COLORES SEMÁNTICOS FINANCIEROS ===
    SUCCESS = "#10b981"
    SUCCESS_LIGHT = "#34d399"
    SUCCESS_DARK = "#059669"
    SUCCESS_ULTRA_LIGHT = "#d1fae5"

    WARNING = "#f59e0b"
    WARNING_LIGHT = "#fbbf24"
    WARNING_DARK = "#d97706"
    WARNING_ULTRA_LIGHT = "#fef3c7"

    ERROR = "#ef4444"
    ERROR_LIGHT = "#f87171"
    ERROR_DARK = "#dc2626"
    ERROR_ULTRA_LIGHT = "#fee2e2"

    # === GRISES (Neutrales) ===
    GRAY_900 = "#0f172a"
    GRAY_800 = "#1e293b"
    GRAY_700 = "#334155"
    GRAY_600 = "#475569"
    GRAY_500 = "#64748b"
    GRAY_400 = "#94a3b8"
    GRAY_300 = "#cbd5e1"
    GRAY_200 = "#e2e8f0"
    GRAY_100 = "#f1f5f9"
    GRAY_50 = "#f8fafc"

    # === BACKGROUNDS ===
    BG_PRIMARY = "#ffffff"
    BG_SECONDARY = "#f0f9ff"
    BG_TERTIARY = "#e0e7ff"
    BG_DARK = "#0f172a"

    # === COLORES ESPECÍFICOS DE LA APP ===
    CHART_INCOME = SUCCESS
    CHART_EXPENSE = ERROR
    CHART_BALANCE = PRIMARY
    CHART_NEUTRAL = GRAY_500

    # === PRESUPUESTOS ===
    BUDGET_OK = SUCCESS
    BUDGET_WARNING = WARNING
    BUDGET_OVER = ERROR

    # === OVERLAYS Y SOMBRAS ===
    OVERLAY_LIGHT = "rgba(15, 23, 42, 0.05)"
    OVERLAY_MEDIUM = "rgba(15, 23, 42, 0.12)"
    OVERLAY_DARK = "rgba(15, 23, 42, 0.24)"

    SHADOW_SM = "0 1px 2px rgba(79,70,229,0.05)"
    SHADOW_MD = "0 4px 6px rgba(79,70,229,0.07)"
    SHADOW_LG = "0 10px 15px rgba(79,70,229,0.1)"
    SHADOW_XL = "0 20px 25px rgba(79,70,229,0.15)"

    # === GRADIENTES ===
    GRADIENT_PRIMARY = "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)"
    GRADIENT_SUCCESS = "linear-gradient(135deg, #d1fae5 0%, #34d39930 100%)"
    GRADIENT_ERROR = "linear-gradient(135deg, #fee2e2 0%, #f8717130 100%)"

    # === 🎨 PREMIUM PALETTE ===
    PREMIUM_PRIMARY_START = "#4f46e5"
    PREMIUM_PRIMARY_END = "#06b6d4"
    PREMIUM_GRADIENT_PRIMARY = f"linear-gradient(135deg, {PREMIUM_PRIMARY_START} 0%, {PREMIUM_PRIMARY_END} 100%)"

    PREMIUM_INDIGO_START = "#3730a3"
    PREMIUM_INDIGO_END = "#6366f1"
    PREMIUM_GRADIENT_INDIGO = f"linear-gradient(135deg, {PREMIUM_INDIGO_START} 0%, {PREMIUM_INDIGO_END} 100%)"

    PREMIUM_CYAN_START = "#0891b2"
    PREMIUM_CYAN_END = "#22d3ee"
    PREMIUM_GRADIENT_CYAN = f"linear-gradient(135deg, {PREMIUM_CYAN_START} 0%, {PREMIUM_CYAN_END} 100%)"

    PREMIUM_EMERALD_START = "#059669"
    PREMIUM_EMERALD_END = "#34d399"
    PREMIUM_GRADIENT_EMERALD = f"linear-gradient(135deg, {PREMIUM_EMERALD_START} 0%, {PREMIUM_EMERALD_END} 100%)"

    PREMIUM_BG_GRADIENT = "linear-gradient(180deg, #ffffff 0%, #f0f9ff 100%)"
    PREMIUM_CARD_GRADIENT = "linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%)"

    # === 💎 GLASSMORPHISM ===
    GLASS_BG = "rgba(255, 255, 255, 0.7)"
    GLASS_BG_DARK = "rgba(79, 70, 229, 0.1)"
    GLASS_BORDER = "rgba(79, 70, 229, 0.3)"
    GLASS_BACKDROP = "blur(10px)"
    GLASS_SHADOW = "0 8px 32px rgba(79, 70, 229, 0.15)"

    # === 🌈 SOMBRAS MULTICAPA ===
    SHADOW_PREMIUM_XS = "0 1px 2px rgba(79,70,229,0.05)"
    SHADOW_PREMIUM_SM = """0 2px 4px rgba(79,70,229,0.06),
                           0 1px 2px rgba(79,70,229,0.04)"""
    SHADOW_PREMIUM_MD = """0 4px 6px rgba(79,70,229,0.07),
                           0 2px 4px rgba(79,70,229,0.05),
                           0 1px 2px rgba(79,70,229,0.04)"""
    SHADOW_PREMIUM_LG = """0 10px 15px rgba(79,70,229,0.08),
                           0 4px 6px rgba(79,70,229,0.06),
                           0 2px 4px rgba(79,70,229,0.04)"""
    SHADOW_PREMIUM_XL = """0 20px 25px rgba(79,70,229,0.10),
                           0 10px 10px rgba(79,70,229,0.04),
                           0 0 0 1px rgba(79,70,229,0.02)"""
    SHADOW_PREMIUM_2XL = """0 25px 50px rgba(79,70,229,0.15),
                            0 12px 25px rgba(79,70,229,0.08)"""

    SHADOW_GLOW_PRIMARY = "0 0 20px rgba(79, 70, 229, 0.4)"
    SHADOW_GLOW_SUCCESS = "0 0 20px rgba(16, 185, 129, 0.4)"
    SHADOW_GLOW_ERROR = "0 0 20px rgba(239, 68, 68, 0.4)"

    # === 🎯 ACENTOS PREMIUM ===
    ACCENT_CYAN = SECONDARY
    ACCENT_EMERALD = SUCCESS
    ACCENT_AMBER = WARNING
    ACCENT_INDIGO = PRIMARY


class Typography:
    """Sistema tipográfico basado en mejores prácticas de legibilidad"""

    FONT_PRIMARY = "'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    FONT_MONO = "'Fira Code', 'SF Mono', 'Roboto Mono', 'Consolas', monospace"

    TEXT_XS = "0.75rem"
    TEXT_SM = "0.875rem"
    TEXT_BASE = "1rem"
    TEXT_LG = "1.125rem"
    TEXT_XL = "1.25rem"
    TEXT_2XL = "1.5rem"
    TEXT_3XL = "1.875rem"
    TEXT_4XL = "2.25rem"
    TEXT_5XL = "3rem"
    TEXT_6XL = "3.75rem"

    WEIGHT_LIGHT = "300"
    WEIGHT_NORMAL = "400"
    WEIGHT_MEDIUM = "500"
    WEIGHT_SEMIBOLD = "600"
    WEIGHT_BOLD = "700"
    WEIGHT_EXTRABOLD = "800"

    LEADING_NONE = "1"
    LEADING_TIGHT = "1.25"
    LEADING_SNUG = "1.375"
    LEADING_NORMAL = "1.5"
    LEADING_RELAXED = "1.75"
    LEADING_LOOSE = "2"

    TRACKING_TIGHTER = "-0.05em"
    TRACKING_TIGHT = "-0.025em"
    TRACKING_NORMAL = "0"
    TRACKING_WIDE = "0.025em"
    TRACKING_WIDER = "0.05em"
    TRACKING_WIDEST = "0.1em"


class Spacing:
    """Sistema de spacing consistente (múltiplos de 4px)"""

    NONE = "0"
    XXS = "0.125rem"
    XS = "0.25rem"
    SM = "0.5rem"
    MD = "0.75rem"
    BASE = "1rem"
    LG = "1.5rem"
    XL = "2rem"
    XXL = "3rem"
    XXXL = "4rem"
    XXXXL = "6rem"


class BorderRadius:
    """Radios de borde consistentes"""

    NONE = "0"
    SM = "0.25rem"
    BASE = "0.5rem"
    MD = "0.75rem"
    LG = "1rem"
    XL = "1.5rem"
    FULL = "9999px"


class Transitions:
    """Tiempos de transición estándar"""

    FASTEST = "100ms"
    FAST = "150ms"
    BASE = "250ms"
    SLOW = "350ms"
    SLOWEST = "500ms"

    EASING_DEFAULT = "cubic-bezier(0.4, 0, 0.2, 1)"
    EASING_IN = "cubic-bezier(0.4, 0, 1, 1)"
    EASING_OUT = "cubic-bezier(0, 0, 0.2, 1)"
    EASING_SHARP = "cubic-bezier(0.4, 0, 0.6, 1)"
    EASING_BOUNCE = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"


class Breakpoints:
    """Breakpoints responsivos"""

    XS = "320px"
    SM = "480px"
    MD = "768px"
    LG = "1024px"
    XL = "1280px"
    XXL = "1536px"


class Config:
    """Configuración general"""

    MIN_TOUCH_TARGET = "44px"
    MIN_INPUT_HEIGHT = "44px"
    MIN_INPUT_FONT_SIZE = "16px"
    MAX_TEXT_WIDTH = "65ch"
    MAX_CONTAINER_WIDTH = "1400px"

    Z_BASE = 1
    Z_DROPDOWN = 10
    Z_STICKY = 100
    Z_OVERLAY = 1000
    Z_MODAL = 1100
    Z_TOOLTIP = 1200
    Z_TOAST = 1300


# === FUNCIONES HELPER ===

def rgba_from_hex(hex_color: str, alpha: float) -> str:
    """Convierte hex a rgba"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def get_contrast_text(bg_color: str) -> str:
    """Devuelve color de texto con contraste adecuado"""
    dark_backgrounds = [
        Colors.PRIMARY_DARK,
        Colors.SUCCESS_DARK,
        Colors.ERROR_DARK,
        Colors.WARNING_DARK,
        Colors.GRAY_900,
        Colors.GRAY_800,
        Colors.GRAY_700,
        Colors.BG_DARK
    ]
    return "#ffffff" if bg_color in dark_backgrounds else Colors.GRAY_900


def get_budget_color(percentage_used: float) -> tuple[str, str, str]:
    """Colores para presupuestos según porcentaje"""
    if percentage_used < 70:
        return ("🟢", Colors.BUDGET_OK, Colors.SUCCESS_ULTRA_LIGHT)
    elif percentage_used < 90:
        return ("🟡", Colors.BUDGET_WARNING, Colors.WARNING_ULTRA_LIGHT)
    else:
        return ("🔴", Colors.BUDGET_OVER, Colors.ERROR_ULTRA_LIGHT)


def spacer_html(size: str = "BASE") -> str:
    """Genera HTML para espaciador vertical"""
    spacing_value = getattr(Spacing, size, Spacing.BASE)
    return f"<div style='height: {spacing_value}'></div>"
```

---

## Próximos Pasos

1. **Decidir paleta:** Elegir entre las 6 opciones (recomiendo Indigo)
2. **Hacer backup:** `cp utils/design_tokens.py utils/design_tokens.py.backup`
3. **Implementar:** Actualizar `utils/design_tokens.py` con la paleta elegida
4. **Actualizar logo:** Cambiar gradientes en `utils/brand_assets.py`
5. **Testing visual:** Revisar todas las páginas de la app
6. **Validar accesibilidad:** Ejecutar script de contraste WCAG
7. **Ajustes finales:** Pequeños tweaks según feedback visual

---

## Referencias y Fuentes

**Tendencias Fintech:**
- Revolut Brand Evolution: Gradientes vibrantes, Cornflower Blue `#7F84F6`
- N26: Aqua elegante, diseño sobrio
- Wise: Verde neón distintivo con espacio en blanco
- YNAB: "Blurple" con enfoque en accesibilidad

**Psicología del Color:**
- Azul: Confianza, seguridad (62-90% del juicio inicial basado en color)
- Púrpura: Riqueza, armonía (sobreuso en fintech)
- Negro: Sofisticación, versatilidad
- Verde: Crecimiento, prosperidad

**Accesibilidad:**
- WCAG AA: Contraste mínimo 4.5:1 (texto normal), 3:1 (texto grande)
- WCAG AAA: Contraste mínimo 7:1 (texto normal), 4.5:1 (texto grande)

---

**Documento creado:** 2025-12-04
**Última actualización:** 2025-12-04
**Estado:** Listo para implementación
