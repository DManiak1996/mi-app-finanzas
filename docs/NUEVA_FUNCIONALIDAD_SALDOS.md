# 🔧 Nueva Funcionalidad: Recálculo de Saldos Posteriores

## 📋 Resumen

Se ha añadido una nueva sección de **Utilidades de Mantenimiento** en la página de Configuración que permite recalcular automáticamente todos los saldos posteriores de las transacciones.

## 🎯 Ubicación en la UI

**Página**: Configuración → Utilidades de Mantenimiento (al final de la página)

## ✨ Características

### 1. Indicador de Estado
- Muestra cuántas transacciones tienen `saldo_posterior` calculado
- Alerta visual si hay transacciones sin saldo (⚠️ naranja)
- Confirmación visual cuando todo está correcto (✅ verde)

### 2. Botón de Recálculo
- **Botón**: "🔄 Recalcular Saldos"
- **Acción**: Recalcula el `saldo_posterior` de todas las transacciones en orden cronológico
- **Feedback**: Muestra mensaje de éxito con el número de transacciones actualizadas
- **Auto-refresh**: La página se recarga automáticamente tras el recálculo

### 3. Detalles Técnicos (Expander)
- Muestra las primeras 10 transacciones sin saldo (si las hay)
- Tabla con: Fecha, Concepto, Importe, Categoría
- Útil para debugging y verificación

## 🔧 Funciones Backend Añadidas

### En `database/db_manager.py`

#### 1. `recalcular_todos_saldos_posteriores()`
```python
def recalcular_todos_saldos_posteriores():
    """
    Recalcula el saldo_posterior para TODAS las transacciones
    en orden cronológico.

    Returns:
        int: Número de transacciones actualizadas
    """
```

**Lógica:**
1. Obtiene todas las transacciones ordenadas por fecha (ASC)
2. Calcula el saldo acumulado: `saldo = saldo_anterior + importe`
3. Actualiza cada transacción con su `saldo_posterior`

**Cuándo usar:**
- Después de crear transacciones manuales
- Si hay inconsistencias en los saldos
- Después de importar datos antiguos

#### 2. `calcular_saldo_actual()`
```python
def calcular_saldo_actual():
    """
    Calcula el saldo actual basándose en todas las transacciones.

    Returns:
        float: Saldo actual (suma de todos los importes)
    """
```

### Modificación en `pagar_recargas_mes()`

**Antes:**
- Las transacciones del coche eléctrico se creaban SIN `saldo_posterior`
- El campo quedaba como `NULL`

**Ahora:**
- Calcula el `saldo_posterior` automáticamente al crear la transacción
- Busca todas las transacciones anteriores a la fecha de pago
- Suma el importe del pago para obtener el nuevo saldo

**Código añadido** (líneas 788-797):
```python
# Calcular saldo_posterior
cursor.execute("""
    SELECT COALESCE(SUM(importe), 0) as saldo_anterior
    FROM transacciones
    WHERE fecha < ? OR (fecha = ? AND id < ?)
""", (fecha_pago_str, fecha_pago_str, id_transaccion))

saldo_anterior = cursor.fetchone()['saldo_anterior']
saldo_posterior = saldo_anterior + (-abs(total_coste))
```

## 📊 Casos de Uso

### Caso 1: Transacciones Manuales
**Problema**: Los pagos del coche eléctrico no tenían saldo_posterior
**Solución**: Ejecutar "🔄 Recalcular Saldos" desde Configuración

### Caso 2: Importación Masiva
**Problema**: Se importaron 500 transacciones sin saldo
**Solución**: Un clic en "🔄 Recalcular Saldos" actualiza las 500 automáticamente

### Caso 3: Corrección de Errores
**Problema**: Se detectaron inconsistencias en los saldos
**Solución**: Recalcular desde cero garantiza coherencia

## 🛠️ Scripts Auxiliares

### `scripts/recalcular_saldos.py`
Script standalone para recalcular saldos desde la terminal:

```bash
python3 scripts/recalcular_saldos.py
```

**Características:**
- Muestra transacciones sin saldo antes de ejecutar
- Pide confirmación interactiva
- Verifica el resultado después del recálculo

**Cuándo usar:**
- Mantenimiento programado
- Debugging fuera de la UI
- Scripts de automatización

## ✅ Verificación

Después de la implementación:

```bash
# 1. Se eliminó el duplicado
✅ Transacción "Sin concepto" duplicada eliminada

# 2. Se recalcularon 615 saldos
✅ Todas las transacciones tienen saldo_posterior

# 3. Pagos del coche eléctrico actualizados
✅ Recarga coche (-13.47€): Saldo -359.26€
✅ Recarga coche (-18.45€): Saldo -377.71€
```

## 📝 Notas Técnicas

1. **Orden de cálculo**: Las transacciones se procesan por `fecha ASC, id ASC`
2. **Atomicidad**: Todo el recálculo se hace en una transacción SQL (commit al final)
3. **Performance**: Con 615 transacciones tarda < 1 segundo
4. **Timestamps**: Se actualiza `updated_at` automáticamente
5. **Idempotencia**: Se puede ejecutar múltiples veces sin problemas

## 🚀 Próximas Mejoras (Opcionales)

- [ ] Añadir indicador de progreso para bases de datos grandes (>10k transacciones)
- [ ] Opción para recalcular solo un rango de fechas
- [ ] Log de auditoría: cuándo se ejecutó el último recálculo
- [ ] Exportar reporte de transacciones sin saldo antes de recalcular
- [ ] Validación de integridad: detectar gaps en las fechas

## 📚 Referencias

- [db_manager.py:1058-1144](../database/db_manager.py#L1058-L1144) - Función de recálculo
- [db_manager.py:788-806](../database/db_manager.py#L788-L806) - Cálculo en pagar_recargas_mes
- [app.py:2444-2505](../app.py#L2444-L2505) - Sección UI de Configuración
- [scripts/recalcular_saldos.py](../scripts/recalcular_saldos.py) - Script standalone
