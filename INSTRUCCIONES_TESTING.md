# Instrucciones de Testing - Componentes Nativos

## Verificación Rápida (5 minutos)

### 1. Test Básico de Componentes
```bash
streamlit run test_native_metrics.py
```

**Qué verificar:**
- ✅ Las métricas se muestran con `st.metric()` nativo
- ✅ Los iconos aparecen en los títulos
- ✅ Los deltas tienen colores (verde/rojo)
- ✅ Los valores están formateados correctamente (€, %, números)
- ✅ No hay HTML visible como texto plano

### 2. Test del Dashboard Principal
```bash
streamlit run app.py
```

**Qué verificar:**
- ✅ El Dashboard carga sin errores
- ✅ Las 4 métricas principales se muestran correctamente:
  - Total Ingresos Mes
  - Gastos del Mes
  - Balance del Mes
  - Tasa Ahorro
- ✅ Las métricas en "Estadísticas del Mes" se muestran
- ✅ Las métricas en "Vista Anual" funcionan
- ✅ No hay código HTML visible como texto

## Verificación Detallada

### 3. Test de Diferentes Formatos

En `test_native_metrics.py` verifica:

| Formato | Ejemplo Esperado | Ubicación |
|---------|-----------------|-----------|
| `currency` | `2.500,50 €` | Test 1 y 2 |
| `percent` | `28.5%` | Test 2 (última métrica) |
| `number` | `100`, `200`, `300` | Test 3 |
| `text` | Cualquier string | - |

### 4. Test de Deltas

Verifica que los deltas muestren:
- ✅ Color verde para valores positivos
- ✅ Color rojo para valores negativos
- ✅ Flecha hacia arriba/abajo
- ✅ Formato correcto (€, %, número)

### 5. Test de Grid Layouts

Verifica:
- ✅ **4 columnas** en Test 2 (dashboard)
- ✅ **3 columnas** en Test 3 (última fila con 2 métricas)
- ✅ Las columnas están alineadas
- ✅ No hay espacios raros o columnas vacías

## Problemas Comunes y Soluciones

### Problema: "No module named 'streamlit'"
**Solución:**
```bash
pip install streamlit
```

### Problema: "ModuleNotFoundError: No module named 'utils'"
**Solución:**
```bash
# Asegúrate de estar en el directorio correcto
cd /Users/daniel/mi_app_finanzas
streamlit run test_native_metrics.py
```

### Problema: Las métricas no se ven
**Solución:**
1. Verifica que usas Streamlit 1.28.0 o superior
2. Limpia cache: `streamlit cache clear`
3. Reinicia la app

### Problema: Sigue apareciendo HTML como texto
**Solución:**
1. Verifica que estás usando el archivo correcto: `utils/components/metric_card.py`
2. Verifica que el archivo fue modificado:
   ```bash
   grep "st.metric" utils/components/metric_card.py
   ```
   Debería mostrar la línea 130-137 con `st.metric(...)`

## Comparación Visual

### ANTES (HTML sanitizado)
```
<div class="metric-card-...">
  <div style="position: absolute; ...">
  ...
  2.500,50 €
</div>
```

### AHORA (Componente nativo)
```
[Métrica de Streamlit nativa con diseño limpio]
💰 Total Ingresos
2.500,50 €
↗ +150,25 €
```

## Checklist de Aceptación

Marca cada item después de verificarlo:

- [ ] `test_native_metrics.py` ejecuta sin errores
- [ ] Las métricas usan `st.metric()` nativo (no HTML)
- [ ] Los iconos aparecen en los títulos
- [ ] Los deltas tienen colores correctos
- [ ] Los formatos (€, %, números) funcionan
- [ ] El dashboard principal carga sin errores
- [ ] Las 4 métricas principales se ven correctamente
- [ ] Los grids de 3 y 4 columnas funcionan
- [ ] No hay HTML visible como texto plano
- [ ] No hay errores en la consola del navegador

## Si Todo Funciona

¡Felicidades! La migración fue exitosa. Puedes:

1. **Eliminar archivos de test (opcional):**
   ```bash
   rm test_native_metrics.py
   ```

2. **Personalizar diseño (opcional):**
   - Editar `.streamlit/config.toml` para cambiar tema
   - Agregar CSS global en `app.py` para estilos custom

3. **Continuar usando la app normalmente**

## Si Algo Falla

1. **Lee el error completo** en la terminal
2. **Toma screenshot** del error
3. **Verifica** que los archivos fueron modificados correctamente:
   ```bash
   head -50 utils/components/metric_card.py
   ```
4. **Comparte** el error para debugging

---

**Última actualización:** 2025-12-07
**Versión:** 2.0 (Native Components)
