# Paleta de Colores - Referencia Visual

**Guía rápida de colores para desarrollo**
**Fecha**: 2025-12-04

---

## 1. Colores Primarios (Identidad de Marca)

### Verde Oscuro → Lima (Gradiente Principal)

```
┌────────────────────────────────────────────────────┐
│ #0a4c3e ────────────────────────────► #84cc16      │
│ Verde bosque profundo          Lima brillante      │
│ [■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■]       │
│ Gradiente usado en: Logo, Botones primarios,       │
│ Barras de header, Métricas destacadas              │
└────────────────────────────────────────────────────┘

Uso en código:
--primary-start: #0a4c3e
--primary-end: #84cc16
--gradient-primary: linear-gradient(135deg, #0a4c3e 0%, #84cc16 100%)
```

### Variaciones del Verde Principal

```
Verde Ultra Oscuro:  #0a4c3e  ████  RGB(10, 76, 62)   - Headers, textos oscuros
Verde Medio:         #0d5f4e  ████  RGB(13, 95, 78)   - Estados hover
Verde Lima:          #84cc16  ████  RGB(132, 204, 22) - Acentos, CTAs
Verde Lima Claro:    #a3e635  ████  RGB(163, 230, 53) - Highlights
```

---

## 2. Colores Semánticos Financieros

### SUCCESS (Ingresos, Positivo, OK)

```
┌──────────────────────────────────────┐
│ 🟢 SUCCESS - Verde Teal               │
├──────────────────────────────────────┤
│ Ultra Light:  #e0f2f1  ░░░░  (BG)   │
│ Light:        #4db6ac  ████          │
│ Base:         #26a69a  ████  ⭐      │
│ Dark:         #00897b  ████          │
└──────────────────────────────────────┘

Cuándo usar:
✅ Ingresos en gráficos
✅ Balance positivo
✅ Mensaje de éxito
✅ Botones de confirmación
✅ Indicadores de meta cumplida

Ejemplo:
st.metric("Ingresos", "2,450€", delta="+12%")
    └── Delta positivo usa SUCCESS (#26a69a)
```

### ERROR (Gastos, Negativo, Alerta)

```
┌──────────────────────────────────────┐
│ 🔴 ERROR - Rojo Coral Suave           │
├──────────────────────────────────────┤
│ Ultra Light:  #ffebee  ░░░░  (BG)   │
│ Light:        #e57373  ████          │
│ Base:         #ef5350  ████  ⭐      │
│ Dark:         #c62828  ████          │
└──────────────────────────────────────┘

Cuándo usar:
❌ Gastos en gráficos
❌ Balance negativo
❌ Mensajes de error
❌ Botones destructivos (eliminar)
❌ Presupuesto excedido (>100%)

Ejemplo:
st.metric("Gastos", "1,850€")
    └── Valor negativo usa ERROR (#ef5350)
```

### WARNING (Advertencia, Precaución)

```
┌──────────────────────────────────────┐
│ ⚠️ WARNING - Naranja                  │
├──────────────────────────────────────┤
│ Ultra Light:  #fff3e0  ░░░░  (BG)   │
│ Light:        #ffb74d  ████          │
│ Base:         #ff9800  ████  ⭐      │
│ Dark:         #f57c00  ████          │
└──────────────────────────────────────┘

Cuándo usar:
⚠️ Presupuesto 70-90% usado
⚠️ Alertas no críticas
⚠️ Campos requeridos sin rellenar
⚠️ Avisos importantes

Ejemplo:
if porcentaje_presupuesto > 70 and porcentaje_presupuesto < 90:
    color = Colors.WARNING
```

### INFO (Información Neutral)

```
┌──────────────────────────────────────┐
│ ℹ️ INFO - Azul Cielo                  │
├──────────────────────────────────────┤
│ Light:        #00f2fe  ████          │
│ Base:         #4facfe  ████  ⭐      │
│ Background:   #e3f2fd  ░░░░          │
└──────────────────────────────────────┘

Cuándo usar:
ℹ️ Mensajes informativos
ℹ️ Tips y ayudas
ℹ️ Reembolsos (neutral, no es gasto ni ingreso puro)
ℹ️ Estados intermedios

Ejemplo:
st.info("Tip: Puedes importar Excel desde la pestaña Importar")
```

---

## 3. Colores para Categorías de Gasto

### FIJOS (Gastos Fijos)

```
┌──────────────────────────────────────┐
│ 🛡️ FIJOS - Índigo                     │
├──────────────────────────────────────┤
│ Base:         #5c6bc0  ████  ⭐      │
│ Significado:  Estabilidad, predecible│
│ Icono:        Escudo                 │
└──────────────────────────────────────┘

Gastos típicos:
- Alquiler/Hipoteca
- Luz, Agua, Gas
- Internet, Móvil
- Seguros
- Suscripciones (Netflix, Spotify)
```

### DISFRUTE (Ocio y Entretenimiento)

```
┌──────────────────────────────────────┐
│ 🍹 DISFRUTE - Rosa Suave              │
├──────────────────────────────────────┤
│ Base:         #f48fb1  ████  ⭐      │
│ Significado:  Placer, diversión      │
│ Icono:        Copa de cóctel         │
└──────────────────────────────────────┘

Gastos típicos:
- Restaurantes, bares
- Cine, teatro
- Viajes, hoteles
- Hobbies
- Compras no esenciales
```

### EXTRAORDINARIOS (Imprevistos)

```
┌──────────────────────────────────────┐
│ ⚡ EXTRAORDINARIOS - Naranja           │
├──────────────────────────────────────┤
│ Base:         #ffa726  ████  ⭐      │
│ Significado:  Atención, imprevisto   │
│ Icono:        Rayo                   │
└──────────────────────────────────────┘

Gastos típicos:
- Reparaciones
- Multas
- Regalos grandes
- Emergencias médicas
- Gastos únicos
```

### COCHE (Coche Eléctrico)

```
┌──────────────────────────────────────┐
│ 🔌 COCHE - Azul Tecnológico            │
├──────────────────────────────────────┤
│ Base:         #42a5f5  ████  ⭐      │
│ Significado:  Movilidad, tecnología  │
│ Icono:        Coche con rayo verde   │
└──────────────────────────────────────┘

Gastos típicos:
- Recargas eléctricas
- Seguro del coche
- ITV, revisiones
- Peajes
- Parking
```

### AHORRO (Inversiones y Ahorro)

```
┌──────────────────────────────────────┐
│ 💰 AHORRO - Verde Crecimiento          │
├──────────────────────────────────────┤
│ Base:         #26a69a  ████  ⭐      │
│ Significado:  Crecimiento, futuro    │
│ Icono:        Hucha o gráfico subida │
└──────────────────────────────────────┘

Conceptos:
- Transferencias a ahorro
- Inversiones
- Plan de pensiones
- Fondo de emergencia
```

---

## 4. Grises (Neutrales)

```
Escala de Grises (de oscuro a claro):

GRAY_900:  #262730  ████  ← Textos principales (títulos, labels)
GRAY_800:  #2d2e38  ████
GRAY_700:  #31333F  ████  ← Textos secundarios (descripciones)
GRAY_600:  #4a4c5a  ████
GRAY_500:  #757575  ████  ← Textos deshabilitados, placeholders
GRAY_400:  #9e9e9e  ████
GRAY_300:  #bdbdbd  ████  ← Bordes, dividers
GRAY_200:  #e0e0e0  ████
GRAY_100:  #f0f2f6  ████  ← Backgrounds secundarios
GRAY_50:   #fafafa  ████  ← Backgrounds hover

Uso:
- Títulos:         GRAY_900 (#262730)
- Texto normal:    GRAY_700 (#31333F)
- Texto suave:     GRAY_500 (#757575)
- Bordes:          GRAY_300 (#bdbdbd)
- Fondo cards:     GRAY_100 (#f0f2f6)
```

---

## 5. Backgrounds y Gradientes

### Light Mode (Actual)

```
┌────────────────────────────────────────────────────┐
│ Fondo Principal (Blanco)                           │
│ #ffffff                                            │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ Fondo con Gradiente Sutil                          │
│ linear-gradient(180deg, #ffffff 0%, #f0fdf4 100%)  │
│ Blanco ──────────────────────────► Verde muy claro │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ Card con Gradiente                                 │
│ linear-gradient(135deg, #ffffff 0%, #f7fee7 100%)  │
│ Blanco ──────────────────────────► Verde ultra claro│
└────────────────────────────────────────────────────┘
```

### Dark Mode (Propuesto - No implementar aún)

```
┌────────────────────────────────────────────────────┐
│ Fondo Principal Dark                               │
│ #1a1a1a (Casi negro)                               │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ Fondo Secundario Dark                              │
│ #2d2d2d (Gris muy oscuro)                          │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ Card Dark                                          │
│ linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%)  │
└────────────────────────────────────────────────────┘
```

---

## 6. Gradientes Decorativos (Adicionales)

### Gradiente Dorado (Para destacados especiales)

```
┌────────────────────────────────────────────────────┐
│ #f6d365 ──────────────────────────► #fda085        │
│ Dorado suave             Coral-naranja             │
│ [■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■]       │
│ Uso: Badges premium, ofertas, destacados           │
└────────────────────────────────────────────────────┘
```

### Gradiente Teal (Alternativa verde)

```
┌────────────────────────────────────────────────────┐
│ #0d5f4e ──────────────────────────► #a3e635        │
│ Verde bosque profundo    Lima vibrante             │
│ [■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■]       │
│ Uso: Variación del gradiente principal             │
└────────────────────────────────────────────────────┘
```

### Gradiente Coral (Para errores suaves)

```
┌────────────────────────────────────────────────────┐
│ #fa709a ──────────────────────────► #fee140        │
│ Rosa coral                Amarillo suave           │
│ [■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■]       │
│ Uso: Errores amigables, warnings críticas          │
└────────────────────────────────────────────────────┘
```

### Gradiente Sky (Para información)

```
┌────────────────────────────────────────────────────┐
│ #4facfe ──────────────────────────► #00f2fe        │
│ Azul cielo                Cyan brillante           │
│ [■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■]       │
│ Uso: Info boxes, tooltips, links                   │
└────────────────────────────────────────────────────┘
```

---

## 7. Reglas de Uso (Do's and Don'ts)

### ✅ DO - Hacer

```
✅ Usar SUCCESS (#26a69a) para:
   - Valores de ingresos
   - Saldos positivos
   - Mensajes de confirmación
   - Botones de "Guardar exitoso"

✅ Usar ERROR (#ef5350) para:
   - Valores de gastos
   - Saldos negativos
   - Mensajes de error
   - Botones destructivos

✅ Usar WARNING (#ff9800) para:
   - Presupuestos 70-90%
   - Alertas moderadas
   - Campos incompletos

✅ Usar gradiente principal (#0a4c3e → #84cc16) para:
   - Logo y branding
   - Botones primarios
   - Headers importantes
   - Métricas destacadas

✅ Usar grises para:
   - Textos (GRAY_700, GRAY_900)
   - Bordes (GRAY_300)
   - Backgrounds (GRAY_100)
```

### ❌ DON'T - Evitar

```
❌ NO usar SUCCESS para gastos
   - Incorrecto: Gasto de 100€ en verde
   - Correcto: Gasto de 100€ en rojo

❌ NO usar ERROR para ingresos
   - Incorrecto: Ingreso de 2000€ en rojo
   - Correcto: Ingreso de 2000€ en verde

❌ NO mezclar más de 2 gradientes en la misma vista
   - Incorrecto: Card con 3 gradientes diferentes
   - Correcto: Card con 1 gradiente + colores planos

❌ NO usar colores saturados para textos largos
   - Incorrecto: Párrafo en #84cc16 (lima brillante)
   - Correcto: Párrafo en #31333F (gris oscuro)

❌ NO usar menos de 4.5:1 de contraste (WCAG AA)
   - Incorrecto: Texto #bdbdbd sobre #ffffff (3:1)
   - Correcto: Texto #31333F sobre #ffffff (12:1)
```

---

## 8. Código de Referencia Rápida

### Acceder a colores en Python

```python
from utils.design_tokens import Colors

# Colores principales
verde_oscuro = Colors.PREMIUM_PRIMARY_START  # #0a4c3e
verde_lima = Colors.PREMIUM_PRIMARY_END      # #84cc16
gradiente = Colors.PREMIUM_GRADIENT_PRIMARY  # linear-gradient(...)

# Semánticos
exito = Colors.SUCCESS      # #26a69a (ingresos)
error = Colors.ERROR        # #ef5350 (gastos)
alerta = Colors.WARNING     # #ff9800 (70-90%)
info = Colors.INFO          # #4facfe (neutral)

# Categorías
fijos = Colors.CATEGORIA_FIJOS              # #5c6bc0
disfrute = Colors.CATEGORIA_DISFRUTE        # #f48fb1
extra = Colors.CATEGORIA_EXTRAORDINARIOS    # #ffa726
coche = Colors.CATEGORIA_COCHE              # #42a5f5

# Grises
texto = Colors.GRAY_900        # #262730 (principal)
texto_suave = Colors.GRAY_500  # #757575 (secundario)
borde = Colors.GRAY_300        # #bdbdbd (dividers)
fondo = Colors.BG_PRIMARY      # #ffffff (blanco)
```

### Helper: Color según porcentaje de presupuesto

```python
from utils.design_tokens import get_budget_color

porcentaje_usado = 85.5

emoji, color, bg_color = get_budget_color(porcentaje_usado)

# Si porcentaje < 70:
#   emoji = "🟢"
#   color = "#26a69a" (SUCCESS)
#   bg_color = "#e0f2f1" (SUCCESS_ULTRA_LIGHT)

# Si 70 <= porcentaje < 90:
#   emoji = "🟡"
#   color = "#ff9800" (WARNING)
#   bg_color = "#fff3e0" (WARNING_ULTRA_LIGHT)

# Si porcentaje >= 90:
#   emoji = "🔴"
#   color = "#ef5350" (ERROR)
#   bg_color = "#ffebee" (ERROR_ULTRA_LIGHT)

# Uso:
st.markdown(f"{emoji} Presupuesto usado: {porcentaje_usado:.1f}%")
st.progress(porcentaje_usado / 100)
```

### Helper: Color con opacidad

```python
from utils.design_tokens import rgba_from_hex, Colors

# Convertir hex a rgba con transparencia
color_transparente = rgba_from_hex(Colors.SUCCESS, 0.2)
# Resultado: "rgba(38, 166, 154, 0.2)"

# Uso en CSS:
st.markdown(f"""
<div style="background: {color_transparente}; padding: 1rem;">
    Fondo verde con 20% opacidad
</div>
""", unsafe_allow_html=True)
```

---

## 9. Testing de Contraste (Accesibilidad)

### Combinaciones Aprobadas (WCAG AA mínimo 4.5:1)

```
✅ PASA - Buenas combinaciones:

Texto oscuro sobre fondo claro:
  #262730 sobre #ffffff    →  12.6:1  (AAA) ⭐⭐⭐
  #31333F sobre #ffffff    →  11.8:1  (AAA) ⭐⭐⭐
  #757575 sobre #ffffff    →   4.6:1  (AA)  ⭐⭐

Texto claro sobre fondo oscuro:
  #ffffff sobre #0a4c3e    →   7.5:1  (AAA) ⭐⭐⭐
  #ffffff sobre #26a69a    →   3.1:1  (Falla AA) ❌

Colores sobre blanco:
  #26a69a sobre #ffffff    →   4.8:1  (AA)  ⭐⭐
  #ef5350 sobre #ffffff    →   5.2:1  (AA)  ⭐⭐
  #ff9800 sobre #ffffff    →   3.5:1  (Falla AA) ❌
```

### Combinaciones a Evitar

```
❌ FALLA - Malas combinaciones:

  #84cc16 sobre #ffffff    →   2.8:1  (Muy bajo)
  #a3e635 sobre #ffffff    →   2.1:1  (Crítico)
  #f48fb1 sobre #ffffff    →   3.2:1  (Bajo)

Solución: Usar estos colores solo para:
  - Backgrounds con texto oscuro encima
  - Iconos grandes (no requieren tanto contraste)
  - Elementos decorativos (no informativos)
```

---

## 10. Ejemplos Visuales de Uso

### Dashboard Métricas

```
┌─────────────────────────────────────────────────┐
│ 💵 Total Ingresos                               │
│ 2,450.00 €                  (gradiente verde)   │
│ +12% vs mes anterior        (SUCCESS #26a69a)   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 💸 Gastos del Mes                               │
│ 1,850.00 €                  (texto gris)        │
│ (Bruto: 1900€ - Reembolsos: 50€)  (GRAY_500)   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ ⚖️ Balance                                       │
│ +600.00 €                   (SUCCESS #26a69a)   │
│ (Si fuera negativo: ERROR #ef5350)              │
└─────────────────────────────────────────────────┘
```

### Presupuestos

```
┌─────────────────────────────────────────────────┐
│ 🟢 FIJOS (#5c6bc0)                   650€ / 800€│
│ [████████████████████────────]  81.3%           │
│ Restante: 150€                                  │
└─────────────────────────────────────────────────┘
                                 ↑
                          Color: SUCCESS (#26a69a)
                          Emoji: 🟢 (OK, <90%)

┌─────────────────────────────────────────────────┐
│ 🟡 DISFRUTE (#f48fb1)                420€ / 500€│
│ [████████████████████████████────]  84.0%       │
│ Restante: 80€                                   │
└─────────────────────────────────────────────────┘
                                 ↑
                          Color: WARNING (#ff9800)
                          Emoji: 🟡 (Alerta, 70-90%)

┌─────────────────────────────────────────────────┐
│ 🔴 EXTRAORDINARIOS (#ffa726)         280€ / 200€│
│ [████████████████████████████████████████] 140% │
│ Excedido: -80€                                  │
└─────────────────────────────────────────────────┘
                                 ↑
                          Color: ERROR (#ef5350)
                          Emoji: 🔴 (Crítico, >90%)
```

### Gráfico de Distribución

```
Pie Chart (Gastos por Categoría):

  🛡️ FIJOS          650€  ████  #5c6bc0 (Índigo)
  🍹 DISFRUTE        420€  ████  #f48fb1 (Rosa)
  ⚡ EXTRAORDINARIOS  280€  ████  #ffa726 (Naranja)
  🔌 COCHE           200€  ████  #42a5f5 (Azul)
  💰 AHORRO          300€  ████  #26a69a (Verde)

Total: 1,850€
```

---

## 11. Resumen de Valores Más Usados

### Top 10 Colores (Copiar/Pegar)

```python
# === COPIA ESTOS ===

# Identidad de marca
VERDE_OSCURO = "#0a4c3e"
VERDE_LIMA = "#84cc16"
GRADIENTE_PRINCIPAL = "linear-gradient(135deg, #0a4c3e 0%, #84cc16 100%)"

# Estados financieros
INGRESO = "#26a69a"   # Verde teal
GASTO = "#ef5350"     # Rojo coral
ALERTA = "#ff9800"    # Naranja
INFO = "#4facfe"      # Azul cielo

# Textos
TEXTO_PRINCIPAL = "#262730"     # Gris muy oscuro
TEXTO_SECUNDARIO = "#31333F"    # Gris oscuro
TEXTO_SUAVE = "#757575"         # Gris medio

# Bordes y fondos
BORDE = "#bdbdbd"              # Gris claro
FONDO = "#ffffff"              # Blanco
FONDO_SECUNDARIO = "#f0f2f6"   # Gris muy claro
```

---

**Guía completa de paleta**
**Para dudas**: Consultar `utils/design_tokens.py` - Código fuente de verdad
