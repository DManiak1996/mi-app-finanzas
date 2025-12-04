# 🎯 Propuesta: Cómo Manejar saldo_posterior en Transacciones Manuales

## El Problema

**Pregunta**: ¿Cuál es el `saldo_posterior` correcto de una transacción manual (pago coche eléctrico)?

**Ejemplo Real**:
```
01/12/2025:
  10:00 - NOMINA (+1564.53€) → Saldo: 4008.61€ ✅ (del banco)
  12:00 - Sin concepto (-275€) → Saldo: 3733.61€ ✅ (del banco)
  ??:?? - Recarga coche (-13.47€) → Saldo: ??? ❓
  ??:?? - Recarga coche (-18.45€) → Saldo: ??? ❓
  18:00 - RICO KEBAB (-6€) → Saldo: 2445.73€ ✅ (del banco)
  19:00 - TUC (-1.65€) → Saldo: 2444.08€ ✅ (del banco)
```

**Problema**: No sabemos la hora exacta de las recargas → No podemos calcular su saldo real

## Opciones Evaluadas

### ❌ Opción 1: Calcular basándose en el último saldo conocido

```python
# Si última trans del día tiene saldo 2444.08€
saldo_recarga_1 = 2444.08 - 13.47 = 2430.61€
saldo_recarga_2 = 2430.61 - 18.45 = 2412.16€
```

**Problemas**:
- ✗ Asume que las recargas fueron DESPUÉS del TUC
- ✗ Si fueron ANTES, los saldos son incorrectos
- ✗ Genera datos falsos que parecen reales

### ❌ Opción 2: Calcular basándose en la primera trans siguiente

```python
# Si primera trans después tiene saldo conocido
# Calcular hacia atrás
```

**Problemas**:
- ✗ Solo funciona si hay transacciones posteriores
- ✗ En diciembre (mes actual), no hay siguiente
- ✗ Sigue asumiendo orden

### ❌ Opción 3: Pedir saldo al usuario

```
UI: "¿Cuál era el saldo antes de este pago?"
```

**Problemas**:
- ✗ Fricción en UX
- ✗ Usuario puede no recordar
- ✗ Error humano

### ✅ Opción 4: NO calcular (RECOMENDADA)

```python
# Transacciones manuales
saldo_posterior = NULL  # Siempre
```

**Ventajas**:
- ✓ No inventa datos
- ✓ Honesto: "no lo sabemos"
- ✓ Simple de implementar
- ✓ Gráficas funcionan igual (calculan en memoria)

## Solución Propuesta: Sistema Híbrido

### Arquitectura

```
┌─────────────────────────────────────────┐
│ TRANSACCIONES DEL BANCO (importadas)    │
├─────────────────────────────────────────┤
│ - Tienen saldo_posterior REAL           │
│ - Son la fuente de verdad                │
│ - Se muestran en tablas y gráficas      │
└─────────────────────────────────────────┘
             │
             │ Referencia
             ▼
┌─────────────────────────────────────────┐
│ TRANSACCIONES MANUALES                   │
├─────────────────────────────────────────┤
│ - saldo_posterior = NULL (siempre)       │
│ - NO se calcula automáticamente          │
│ - Se incluyen en gráficas (memoria)     │
│ - En tablas: muestran "N/A" o "--"      │
└─────────────────────────────────────────┘
             │
             │ Ambas
             ▼
┌─────────────────────────────────────────┐
│ GRÁFICA DE EVOLUCIÓN                     │
├─────────────────────────────────────────┤
│ saldo = saldo_inicial + SUM(importes)   │
│ Calcula en MEMORIA, no usa BD            │
│ Incluye banco + manuales                │
└─────────────────────────────────────────┘
```

### Implementación

#### 1. En la Base de Datos

```sql
-- Transacciones del banco
saldo_posterior: 4008.61, 3733.61, 2445.73, 2444.08

-- Transacciones manuales
saldo_posterior: NULL, NULL
```

#### 2. En la UI - Tabla de Transacciones

```
| Fecha      | Concepto      | Importe   | Saldo Posterior |
|------------|---------------|-----------|-----------------|
| 2025-12-01 | NOMINA        | +1564.53€ | 4008.61€        |
| 2025-12-01 | Sin concepto  | -275.00€  | 3733.61€        |
| 2025-12-01 | Recarga coche | -13.47€   | --              |  ← NULL
| 2025-12-01 | Recarga coche | -18.45€   | --              |  ← NULL
| 2025-12-01 | RICO KEBAB    | -6.00€    | 2445.73€        |
| 2025-12-01 | TUC PAMPLONA  | -1.65€    | 2444.08€        |
```

**Cambio en app.py**:
```python
# Al mostrar tabla de transacciones
saldo_display = f"{row['saldo_posterior']:.2f}€" if row['saldo_posterior'] else "--"
st.write(saldo_display)
```

#### 3. En la Gráfica de Evolución (YA FUNCIONA ASÍ)

```python
# app.py línea 1138
saldo_inicial = obtener_ultimo_saldo_mes_anterior()  # 2444.08€ (del banco)

# Incluye TODAS las transacciones del mes (banco + manuales)
df_trans = obtener_transacciones_mes(12, 2025)

# Calcula saldo acumulado
df_trans['saldo_disponible'] = saldo_inicial + df_trans['importe'].cumsum()

# Resultado:
# 2444.08 → 4008.61 (nómina) → 3733.61 (sin concepto) →
# 3720.14 (recarga) → 3701.69 (recarga) → 3695.69 (kebab) → 3694.04 (tuc)
```

### Casos de Uso

#### Caso 1: Usuario quiere saber el saldo exacto de una transacción manual

**Respuesta**: "No se puede calcular automáticamente. Consulta tu extracto bancario para ver el saldo exacto en ese momento."

**Alternativa**: Importar un Excel del banco que incluya esa transacción

#### Caso 2: Usuario quiere ver la evolución del saldo del mes

**Respuesta**: "Mira la gráfica de Evolución del Saldo. Incluye todas las transacciones (banco + manuales) y muestra el saldo disponible en cada momento."

#### Caso 3: Usuario quiere reconciliar cuentas

**Recomendación**:
1. Importar Excel actualizado del banco
2. Comparar saldo final del Excel vs saldo calculado
3. Diferencia = transacciones manuales no registradas o errores

## Mejoras Futuras (Opcionales)

### 1. Columna `origen` para distinguir fuentes

```sql
ALTER TABLE transacciones ADD COLUMN origen TEXT DEFAULT 'banco';
```

Valores:
- `'banco'`: Importada del Excel (tiene saldo real)
- `'manual'`: Creada en la app (sin saldo)
- `'api'`: Futura integración con API bancaria

**Usar en UI**:
```python
# Mostrar icono según origen
if row['origen'] == 'banco':
    icon = "🏦"
elif row['origen'] == 'manual':
    icon = "✋"
```

### 2. Cálculo de "saldo estimado" (opcional)

**Solo para visualización**, nunca guardar en BD:

```python
def calcular_saldo_estimado(transaccion):
    """
    Calcula un saldo ESTIMADO basándose en el último saldo conocido.
    SOLO para visualización, NO se guarda en BD.
    """
    if transaccion['saldo_posterior'] is not None:
        return transaccion['saldo_posterior']  # Usar real

    # Buscar último saldo anterior
    ultimo_saldo = buscar_ultimo_saldo_anterior(transaccion['fecha'])

    # Sumar todos los importes intermedios
    suma_intermedios = sumar_importes_hasta(transaccion['id'])

    return ultimo_saldo + suma_intermedios  # ESTIMADO
```

**Mostrar en UI**:
```
Saldo Posterior: ~3720.14€ (estimado)
```

### 3. Validación al importar Excel

**Detectar si hay transacciones manuales "huérfanas"**:

```python
# Al importar Excel nuevo
for trans_manual in get_transacciones_manuales():
    fecha = trans_manual['fecha']

    # Buscar en Excel si hay transacciones ese día
    trans_excel_dia = get_transacciones_excel(fecha)

    if not trans_excel_dia:
        warning(f"Transacción manual {trans_manual['concepto']} del {fecha} "
                f"no tiene referencia en el Excel importado")
```

## Conclusión

**Respuesta a tu pregunta**:

> ¿Cómo "adivinamos" el saldo posterior?

**No lo adivinamos.** Dejamos `saldo_posterior = NULL` para transacciones manuales porque:

1. **No tenemos información suficiente** (hora exacta)
2. **Calcular sería inventar datos** (el saldo "real" podría ser diferente)
3. **Las gráficas funcionan sin este campo** (calculan en memoria)
4. **La fuente de verdad es el banco** (solo el Excel tiene saldos reales)

**Lo que SÍ podemos hacer**:

✅ Mostrar evolución del saldo en gráficas (incluye manuales)
✅ Calcular saldo disponible actual (suma de todos los importes)
✅ Mostrar "N/A" en la tabla para transacciones manuales
✅ Permitir reconciliación manual con el extracto bancario

**Lo que NO debemos hacer**:

❌ Calcular saldos ficticios que parecen reales
❌ Asumir el orden de transacciones del mismo día
❌ Guardar saldos estimados como si fueran reales
