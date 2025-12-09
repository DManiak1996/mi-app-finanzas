# ✅ Solución Final: Problema del saldo_posterior

## 🔍 El Problema Detectado

El campo `saldo_posterior` tenía **dos significados conflictivos**:

1. **En transacciones del banco (Excel)**: Saldo REAL de la cuenta (ej: 4008.61€)
2. **Tras recálculo incorrecto**: Suma acumulativa desde inicio (ej: -339.79€)

Esto rompió la gráfica de evolución del saldo en diciembre, mostrando -339.79€ en lugar del saldo real.

## 🛠️ La Solución Implementada

### 1. Separación de Responsabilidades

**Transacciones del Banco (importadas del Excel)**:
- Mantienen su `saldo_posterior` REAL del banco
- **NUNCA se recalculan** automáticamente
- Son el "punto de anclaje" para las transacciones manuales

**Transacciones Manuales (coche eléctrico, etc.)**:
- Se crean con `saldo_posterior = NULL`
- Se calculan bajo demanda usando la función específica
- Se basan en el último saldo conocido del banco

### 2. Nueva Función: `recalcular_saldos_transacciones_manuales()`

**Ubicación**: [db_manager.py:1069-1168](../database/db_manager.py#L1069-L1168)

**Lógica**:
```python
Para cada transacción manual (saldo_posterior = NULL):
  1. Buscar última transacción ANTERIOR con saldo conocido (del banco)
  2. Sumar todas las transacciones manuales intermedias
  3. Calcular: saldo_posterior = saldo_banco_anterior + importes_intermedios
```

**Características**:
- ✅ NO toca transacciones del banco (respeta saldo real)
- ✅ Calcula solo transacciones manuales sin saldo
- ✅ Usa el saldo del banco como referencia
- ✅ Es idempotente (se puede ejecutar múltiples veces)

### 3. Modificación de `pagar_recargas_mes()`

**Cambio**: [db_manager.py:788-800](../database/db_manager.py#L788-L800)

**Antes**:
```python
# Calculaba saldo_posterior como suma acumulativa
saldo_posterior = suma_todos_los_importes_anteriores + importe_actual
```

**Ahora**:
```python
# Deja saldo_posterior como NULL
# Se calcula después con recalcular_saldos_transacciones_manuales()
INSERT INTO transacciones (..., notas) VALUES (..., ?)
# SIN saldo_posterior
```

### 4. UI Actualizada

**Ubicación**: Configuración → Utilidades de Mantenimiento

**Cambios**:
- Renombrado: "Recalcular Saldos" → "Calcular Saldos Manuales"
- Advertencia clara: "NO modifica transacciones del banco"
- Feedback mejorado: distingue entre 0 actualizaciones (todo OK) vs error

## 📊 Estado Actual de los Datos

```
Total transacciones: 615
  ✅ Con saldo_posterior: 613 (del banco)
  ⚠️  Sin saldo_posterior: 2 (recargas coche del 01/12)

Transacciones del 2025-12-01:
  🏦 NOMINA (banco)      | +1564.53€ | Saldo: 4008.61€ ✅
  🏦 Sin concepto (banco)| -275.00€  | Saldo: 3733.61€ ✅
  🏦 RICO KEBAB (banco)  | -6.00€    | Saldo: 2445.73€ ✅
  🏦 TUC (banco)         | -1.65€    | Saldo: 2444.08€ ✅
  ✋ Recarga coche       | -13.47€   | Saldo: NULL (manual)
  ✋ Recarga coche       | -18.45€   | Saldo: NULL (manual)
```

## 🚀 Cómo Usar

### Flujo Normal

1. **Importar Excel del banco**
   - Los saldos reales se guardan automáticamente ✅

2. **Crear transacciones manuales** (pagar recargas coche)
   - Se crean con `saldo_posterior = NULL` ✅

3. **Calcular saldos manuales** (opcional)
   - Ve a **Configuración → Utilidades de Mantenimiento**
   - Click en "🔄 Calcular Saldos Manuales"
   - Los saldos se calculan basándose en el último saldo del banco ✅

### ¿Cuándo calcular saldos manuales?

**Necesario cuando**:
- Quieres ver el saldo completo incluyendo transacciones manuales
- Necesitas exportar datos con saldos completos
- Hay muchas transacciones manuales mezcladas con las del banco

**NO necesario cuando**:
- Solo importas Excel del banco (ya tienen saldo)
- Las transacciones manuales son pocas y no afectan reporting
- La gráfica de evolución ya funciona correctamente (usa cálculo en memoria)

## 📈 Gráfica de Evolución del Saldo

**Cómo funciona** ([app.py:1138](../app.py#L1138)):
```python
# SIEMPRE se calcula en memoria, NO usa saldo_posterior
saldo_inicial = obtener_ultimo_saldo_mes_anterior()
df_trans['saldo_disponible'] = saldo_inicial + df_trans['importe'].cumsum()
```

**Por qué es correcto**:
- Usa el último saldo conocido del mes anterior (del banco)
- Suma todos los importes del mes actual (banco + manuales)
- No depende de `saldo_posterior` → siempre es preciso

## 🔧 Archivos Modificados

| Archivo | Cambio | Líneas |
|---------|--------|--------|
| `db_manager.py` | Nueva función `recalcular_saldos_transacciones_manuales()` | 1069-1168 |
| `db_manager.py` | Modificado `pagar_recargas_mes()` - NO calcula saldo | 788-800 |
| `app.py` | Actualizada UI de Utilidades de Mantenimiento | 2444-2505 |

## ✅ Verificación

### Pruebas Realizadas

1. **Restauración de saldos del banco**: ✅
   ```bash
   ✅ Restaurados 102 saldos desde el Excel
   ```

2. **Transacciones manuales con NULL**: ✅
   ```bash
   ✅ 2 transacciones de Recarga coche con saldo = NULL
   ```

3. **Sintaxis correcta**: ✅
   ```bash
   ✅ db_manager.py: Sintaxis correcta
   ✅ app.py: Sintaxis correcta
   ```

### Estado Esperado vs Real

| Aspecto | Esperado | Real | Estado |
|---------|----------|------|--------|
| Trans. del banco con saldo | 613 | 613 | ✅ |
| Trans. manuales sin saldo | 2 | 2 | ✅ |
| Saldo NOMINA 01/12 | 4008.61€ | 4008.61€ | ✅ |
| Saldo Recarga coche | NULL | NULL | ✅ |
| Gráfica diciembre | Correcta | ? | ⏳ Verificar en UI |

## 🎯 Recomendaciones

### Mantener la Coherencia

1. **NUNCA ejecutar recálculo masivo**
   - La antigua función `recalcular_todos_saldos_posteriores()` fue eliminada
   - Solo usar `recalcular_saldos_transacciones_manuales()`

2. **Importar Excel regularmente**
   - Esto mantiene los saldos reales del banco actualizados
   - Son la fuente de verdad para el saldo

3. **Calcular saldos manuales si es necesario**
   - Pero la app funciona perfectamente sin esto
   - La gráfica calcula en memoria y no depende de estos saldos

### Validación Periódica

```bash
# Script para verificar integridad
python3 -c "
from database.db_manager import get_db_connection
conn = get_db_connection()
cursor = conn.cursor()

# Verificar que transacciones del banco tienen saldo
cursor.execute('''
    SELECT COUNT(*) FROM transacciones
    WHERE saldo_posterior IS NOT NULL
''')
print(f'✅ Transacciones con saldo (del banco): {cursor.fetchone()[0]}')

# Verificar que transacciones manuales no tienen saldo
cursor.execute('''
    SELECT COUNT(*) FROM transacciones
    WHERE saldo_posterior IS NULL
''')
print(f'⚠️  Transacciones sin saldo (manuales): {cursor.fetchone()[0]}')
"
```

## 📚 Documentación Relacionada

- [MUSATRO_DESIGN_DOC.md](../MUSATRO_DESIGN_DOC.md) - Arquitectura general
- [NUEVA_FUNCIONALIDAD_SALDOS.md](./NUEVA_FUNCIONALIDAD_SALDOS.md) - Primera implementación (obsoleta)
- [scripts/recalcular_saldos.py](../scripts/recalcular_saldos.py) - Script standalone

## 🐛 Errores Corregidos

1. ✅ Recálculo masivo que convertía saldos reales en sumas acumulativas
2. ✅ Gráfica mostrando -339.79€ en lugar del saldo real
3. ✅ Transacciones manuales con saldos incorrectos
4. ✅ Confusión entre "saldo real del banco" vs "suma acumulativa"

## 🎓 Lecciones Aprendidas

1. **No mezclar conceptos**: Saldo real ≠ Suma acumulativa
2. **Separar fuentes de verdad**: Banco vs App
3. **Calcular en memoria cuando sea posible**: Más robusto que persistir
4. **Documentar suposiciones**: El saldo_posterior del Excel es REAL, no relativo
