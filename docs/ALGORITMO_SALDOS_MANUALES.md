# ✅ Algoritmo Final: Cálculo de saldo_posterior para Transacciones Manuales

## 🎯 Resumen

Se ha implementado un algoritmo inteligente que calcula el `saldo_posterior` de transacciones manuales basándose en:
1. El **líquido disponible** actual
2. La transacción del banco **más cercana** a ese valor
3. El **mismo mes** y **fecha igual o anterior**

## 🧮 El Algoritmo

### Entrada
- Transacción manual sin `saldo_posterior` (ej: Recarga coche del 01/12/2025, -13.47€)
- Líquido disponible: 3701.69€

### Proceso

**Paso 1: Buscar transacción "ancla"**
```sql
Buscar en diciembre 2025:
- Transacciones del banco (saldo_posterior NOT NULL)
- Con fecha <= 01/12/2025
- Ordenadas por: ABS(saldo_posterior - 3701.69) ASC
- LIMIT 1
```

**Resultado**: "Sin concepto" (01/12/2025) con saldo 3733.61€ ← ¡Solo 31.92€ de diferencia!

**Paso 2: Calcular suma de trans. manuales**
```sql
Sumar importes de transacciones manuales:
- Desde la fecha del ancla (01/12)
- Hasta la fecha de esta transacción (01/12)
- Con id <= id de esta transacción
```

**Resultado**: -13.47€ (solo esta recarga)

**Paso 3: Calcular saldo**
```
saldo_manual = saldo_ancla + suma_intermedias
             = 3733.61€ + (-13.47€)
             = 3720.14€ ✅
```

### Ejemplo Completo

```
Diciembre 2025 - Transacciones del 01/12:

🏦 NOMINA        +1564.53€ → Saldo: 4008.61€
🏦 Sin concepto   -275.00€ → Saldo: 3733.61€ ← ANCLA (más cercana a 3701.69€)
✋ Recarga 1       -13.47€ → Saldo: 3720.14€ (calculado: 3733.61 - 13.47)
✋ Recarga 2       -18.45€ → Saldo: 3701.69€ (calculado: 3733.61 - 31.92) ✅
🏦 KEBAB           -6.00€ → Saldo: 2445.73€
🏦 TUC             -1.65€ → Saldo: 2444.08€

Líquido Disponible: 3701.69€ ✅ (coincide con la última recarga)
```

## 💡 Por Qué Funciona

**La clave**: El líquido disponible (3701.69€) representa el saldo actual = último saldo banco + transacciones manuales.

Si encontramos la transacción del banco cuyo saldo está **más cerca** del líquido disponible, sabemos que las transacciones manuales están **justo después** de ella.

**Matemáticamente**:
```
Líquido = Saldo_inicial + Σ(todas las transacciones)
Líquido = Último_saldo_banco + Σ(trans_manuales_posteriores)

Si Saldo_ancla ≈ Líquido
Entonces: Trans_manuales están después del ancla
```

## 🛠️ Implementación

### Función Backend

**Archivo**: `database/db_manager.py`
**Función**: `recalcular_saldos_transacciones_manuales(mes=None, año=None)`

**Parámetros**:
- `mes` (opcional): Filtrar por mes específico (1-12)
- `año` (opcional): Filtrar por año específico

**Retorna**: Número de transacciones actualizadas

**Ejemplo de uso**:
```python
# Calcular saldos de todas las transacciones manuales
db_manager.recalcular_saldos_transacciones_manuales()

# Calcular solo diciembre 2025
db_manager.recalcular_saldos_transacciones_manuales(mes=12, año=2025)

# Calcular todo el año 2025
db_manager.recalcular_saldos_transacciones_manuales(año=2025)
```

### UI en Configuración

**Ubicación**: Configuración → Utilidades de Mantenimiento

**Controles**:
- **Selectbox Mes**: "Todos", 01, 02, ..., 12
- **Selectbox Año**: "Todos", 2024, 2025, 2026
- **Botón**: "🔄 Calcular Saldos Manuales"

**Ejemplo de uso en UI**:
1. Ve a Configuración
2. Selecciona "Mes: 09" y "Año: 2025"
3. Click en "🔄 Calcular Saldos Manuales"
4. Resultado: "✅ Se calcularon 3 saldos de 09/2025"

## 📊 Casos de Uso

### Caso 1: Ajustar transacciones de septiembre pasado

**Escenario**: En enero 2026, descubres que en septiembre 2025 había transacciones manuales sin saldo.

**Solución**:
```
1. Configuración → Utilidades de Mantenimiento
2. Seleccionar: Mes: 09, Año: 2025
3. Click "Calcular Saldos Manuales"
```

**Resultado**: Solo se recalculan las transacciones de 09/2025, sin tocar el resto.

### Caso 2: Recalcular todo un año

**Escenario**: Cambias de banco y quieres recalcular todos los saldos de 2025.

**Solución**:
```
1. Configuración → Utilidades de Mantenimiento
2. Seleccionar: Mes: Todos, Año: 2025
3. Click "Calcular Saldos Manuales"
```

### Caso 3: Recalcular mes actual

**Escenario**: Acabas de pagar las recargas del coche de diciembre.

**Solución**:
```
1. Configuración → Utilidades de Mantenimiento
2. Seleccionar: Mes: 12, Año: 2025
3. Click "Calcular Saldos Manuales"
```

## ⚙️ Detalles Técnicos

### Orden de Procesamiento

Las transacciones se procesan en orden cronológico:
```sql
ORDER BY fecha ASC, id ASC
```

Esto asegura que:
1. Las transacciones más antiguas se calculan primero
2. Si hay múltiples trans. manuales el mismo día, se procesan en orden de creación
3. Cada transacción se basa en las anteriores

### Búsqueda del Ancla

**Criterios de selección**:
```sql
WHERE saldo_posterior IS NOT NULL  -- Solo banco
  AND mes = ? AND año = ?           -- Mismo período
  AND fecha <= ?                    -- Mismo día o anterior
ORDER BY ABS(saldo_posterior - liquido) ASC  -- Más cercana
LIMIT 1
```

**Por qué `fecha <=`**:
- Asegura que el ancla sea anterior o del mismo día
- Evita usar transacciones futuras como referencia

**Por qué `ABS(saldo - liquido)`**:
- Encuentra la transacción más cercana al saldo real
- Minimiza el error en el cálculo

### Fallback sin Ancla

Si no se encuentra transacción ancla (raro), se usa suma acumulativa desde inicio:
```python
saldo_calculado = SUM(todos los importes hasta esta trans)
```

## 🔒 Garantías

1. **No modifica transacciones del banco**: Solo actualiza `saldo_posterior IS NULL`
2. **Idempotente**: Se puede ejecutar múltiples veces con el mismo resultado
3. **Filtrable**: Permite recalcular solo períodos específicos
4. **Transaccional**: Si falla, hace rollback (no deja datos a medias)

## 📈 Rendimiento

**Complejidad**:
- Por transacción: O(log N) - búsqueda del ancla con índice
- Total: O(M * log N) donde M = trans. manuales, N = trans. totales

**Tiempos estimados**:
- 2 transacciones: < 0.1s
- 100 transacciones: < 1s
- 1000 transacciones: < 10s

## 🐛 Casos Límite

### Sin transacciones del banco ese mes

**Escenario**: Mes sin importar Excel del banco.

**Comportamiento**: Usa fallback (suma acumulativa desde inicio).

**Solución**: Importar Excel del banco para ese mes.

### Múltiples trans. manuales mismo día

**Escenario**: 5 recargas el 01/12.

**Comportamiento**:
- Se procesan en orden de ID
- Cada una se basa en las anteriores
- Saldo se va acumulando correctamente

### Cambio de año

**Escenario**: Trans. manual del 31/12/2025.

**Comportamiento**: Busca ancla en diciembre 2025 (mismo mes/año).

## 📚 Archivos Relacionados

| Archivo | Cambios |
|---------|---------|
| `database/db_manager.py` | Función `recalcular_saldos_transacciones_manuales()` actualizada |
| `app.py` | UI con filtros de mes/año añadida |
| `docs/ALGORITMO_SALDOS_MANUALES.md` | Esta documentación |

## ✅ Verificación

```bash
# Script de verificación
python3 -c "
import sys
sys.path.insert(0, '/Users/daniel/mi_app_finanzas')
from database.db_manager import get_db_connection
from utils import metrics

conn = get_db_connection()
cursor = conn.cursor()

# Obtener líquido disponible
liquido = metrics.calcular_liquido_disponible()
print(f'💧 Líquido Disponible: {liquido:.2f}€')

# Última transacción manual
cursor.execute('''
    SELECT saldo_posterior FROM transacciones
    WHERE saldo_posterior IS NOT NULL
    ORDER BY fecha DESC, id DESC
    LIMIT 1
''')

ultimo_saldo = cursor.fetchone()
if ultimo_saldo and abs(ultimo_saldo[0] - liquido) < 0.01:
    print('✅ El último saldo coincide con el líquido disponible')
else:
    print(f'⚠️  Diferencia: {abs(ultimo_saldo[0] - liquido):.2f}€')
"
```

## 🎓 Lecciones Aprendidas

1. **El líquido disponible es la clave**: Es el "punto de referencia" que nos dice dónde están las transacciones manuales
2. **Buscar por cercanía, no por orden**: Usar `ABS(saldo - liquido)` es más robusto que asumir orden cronológico
3. **Filtrar por mes es esencial**: No se puede comparar saldos de meses diferentes
4. **La UI debe ser flexible**: Permitir filtrar por mes/año facilita el mantenimiento futuro
