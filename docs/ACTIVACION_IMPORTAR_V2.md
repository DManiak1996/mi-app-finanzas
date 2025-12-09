# Guía de Activación: Importar Excel v2

**Versión:** 1.0
**Fecha:** 2025-12-04
**Estado Feature Flag:** `USE_NEW_IMPORTAR = False` (desactivado por defecto)

---

## Estado Actual

### ✅ Completado:
- [x] Versión v2 implementada en `app.py`
- [x] Feature flag `USE_NEW_IMPORTAR` configurado
- [x] Versión v1 preservada para rollback
- [x] Sintaxis verificada
- [x] Imports configurados
- [x] Documentación completa

### 🔄 Pendiente:
- [ ] Testing manual
- [ ] Activación en producción

---

## Cómo Activar la Versión v2

### Opción 1: Activación Permanente

Edita el archivo `utils/feature_flags.py`:

```python
# ANTES (línea 123)
USE_NEW_IMPORTAR = False

# DESPUÉS
USE_NEW_IMPORTAR = True
```

**Pasos:**
1. Abrir archivo: `/Users/daniel/mi_app_finanzas/utils/feature_flags.py`
2. Buscar línea 123: `USE_NEW_IMPORTAR = False`
3. Cambiar a: `USE_NEW_IMPORTAR = True`
4. Guardar archivo
5. Reiniciar la aplicación Streamlit
6. Navegar a "Importar desde Excel"
7. Verificar que se muestre el nuevo diseño

### Opción 2: Activación del Master Flag (Activa TODO el nuevo diseño)

```python
# En utils/feature_flags.py (línea 47)
USE_NEW_DESIGN = True  # Activa TODOS los flags
```

⚠️ **Advertencia:** Esto activa TODAS las páginas rediseñadas, no solo Importar.

---

## Checklist de Testing

### Pre-Activación (v1 - Diseño Original)

Antes de activar, verifica que v1 funciona:

- [ ] La aplicación inicia sin errores
- [ ] La página "Importar desde Excel" carga correctamente
- [ ] El file uploader funciona
- [ ] Las transacciones se importan correctamente
- [ ] Los duplicados se detectan
- [ ] Los mensajes de éxito/error funcionan

### Post-Activación (v2 - Nuevo Diseño)

Después de activar el flag, verifica:

#### 1. **Carga Inicial**
- [ ] La página carga sin errores
- [ ] Se muestra el header con título e icono
- [ ] Se muestra la Sección 1: "Seleccionar Archivo"
- [ ] El FormCard se renderiza correctamente
- [ ] Las instrucciones son visibles y claras

#### 2. **Upload de Archivo**
- [ ] El file uploader funciona
- [ ] Al subir un archivo, aparece progress bar
- [ ] Progress bar muestra: 30% → 60% → 100%
- [ ] La página hace rerun automáticamente

#### 3. **Sección 2: Resumen**
- [ ] Se muestran 3 métricas con colores:
  - Hojas Procesadas (azul)
  - Transacciones Nuevas (verde)
  - Duplicados Detectados (naranja)
- [ ] Los números son correctos

#### 4. **Sección 3: Preview**
- [ ] Se muestra tabla con primeras 10 transacciones
- [ ] Las fechas están formateadas (DD/MM/YYYY)
- [ ] Los importes están formateados (X,XXX.XX €)
- [ ] La tabla es scrollable si hay muchas columnas

#### 5. **Sección 4: Duplicados** (si hay duplicados)
- [ ] Se muestra mensaje warning
- [ ] Se muestra tabla de duplicados completa
- [ ] Los radio buttons funcionan:
  - "Omitir duplicados (Recomendado)"
  - "Importar todo (creará duplicados)"

#### 6. **Sección 5: Confirmación**
- [ ] Se muestra mensaje informativo correcto
- [ ] Hay dos botones:
  - "✅ Confirmar e Importar" (primario, azul)
  - "🔄 Cargar Otro Archivo" (secundario, gris)

#### 7. **Importación**
- [ ] Al hacer clic en "Confirmar e Importar":
  - Progress bar aparece
  - Muestra "Importando transacción X de Y..."
  - Progreso se actualiza en tiempo real
  - Al terminar, muestra mensaje de éxito verde
  - Aparecen balloons
  - Estado se limpia
  - Página hace rerun

#### 8. **Botón Reset**
- [ ] Al hacer clic en "🔄 Cargar Otro Archivo":
  - Estado se limpia
  - Vuelve a mostrar solo Sección 1
  - File uploader está vacío

#### 9. **Manejo de Errores**
- [ ] Si hay error en el archivo:
  - Se muestra mensaje de error rojo
  - NO se muestran las secciones siguientes
- [ ] Si no hay transacciones nuevas:
  - Se muestra mensaje info azul

---

## Casos de Prueba Sugeridos

### Caso 1: Archivo Válido Sin Duplicados

**Archivo:** Nuevo archivo Excel con transacciones únicas

**Resultado Esperado:**
- ✅ 3 métricas correctas
- ✅ Preview muestra transacciones
- ❌ NO se muestra sección de duplicados
- ✅ Importación exitosa
- ✅ Balloons

### Caso 2: Archivo Válido Con Duplicados

**Archivo:** Excel con algunas transacciones ya importadas

**Resultado Esperado:**
- ✅ Métrica de duplicados > 0
- ✅ Se muestra sección de duplicados
- ✅ Tabla de duplicados visible
- ✅ Radio buttons funcionan
- ✅ Al elegir "Omitir", solo importa nuevas
- ✅ Al elegir "Importar todo", importa todas

### Caso 3: Archivo con Formato Incorrecto

**Archivo:** Excel sin columnas esperadas

**Resultado Esperado:**
- ❌ Se muestra mensaje de error
- ❌ NO se muestran secciones 2-5

### Caso 4: Archivo Vacío

**Archivo:** Excel sin transacciones

**Resultado Esperado:**
- ✅ Procesamiento sin errores
- ⚠️ Métrica de "Transacciones Nuevas" = 0
- ℹ️ Mensaje informativo

---

## Rollback en Caso de Problemas

Si algo falla después de activar v2:

### Rollback Inmediato (< 1 minuto)

1. Abrir `utils/feature_flags.py`
2. Cambiar línea 123:
   ```python
   USE_NEW_IMPORTAR = False  # ⬅️ Volver a False
   ```
3. Guardar
4. Reiniciar Streamlit
5. Verificar que funciona v1

**No es necesario:**
- ❌ Revertir código de app.py
- ❌ Modificar otros archivos
- ❌ Limpiar base de datos

---

## Diferencias Visuales v1 vs v2

### v1 (Original)
```
📥 Importar desde Excel
Sube aquí tu archivo Excel...

[File Uploader]

Resumen de la importación
┌─────────────┬─────────────┬─────────────┐
│ Hojas: 2    │ Nuevas: 45  │ Duplicados:5│
└─────────────┴─────────────┴─────────────┘

Vista Previa de Transacciones a Importar
[Tabla st.dataframe simple]

⚠️ Se han detectado 5 transacciones...
[Tabla de duplicados]

○ Omitir duplicados (Recomendado)
○ Importar todo

[✅ Confirmar e Importar]
```

### v2 (Nuevo)
```
═══════════════════════════════════════════
📥 Importar desde Excel
Sube tu archivo Excel con los movimientos...
═══════════════════════════════════════════

┌─────────────────────────────────────────┐
│ 📂 1. Seleccionar Archivo               │
│                                         │
│ ┌──────────────────────────────────┐   │
│ │ 📥 Cargar Archivo Excel           │   │
│ │                                   │   │
│ │ ℹ️ Instrucciones:                 │   │
│ │ • Formato: Excel (.xlsx)          │   │
│ │ • Columnas: Fecha, Concepto...   │   │
│ │ • Detección automática duplicados│   │
│ │                                   │   │
│ │ [File Uploader]                   │   │
│ └──────────────────────────────────┘   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 📊 2. Resumen del Archivo               │
│                                         │
│ ┌──────┐  ┌──────┐  ┌──────┐          │
│ │  2   │  │  45  │  │  5   │          │
│ │ Hojas│  │Nuevas│  │Duplic│          │
│ └──────┘  └──────┘  └──────┘          │
│  (azul)   (verde)   (naranja)          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ 👀 3. Preview de Transacciones Nuevas   │
│                                         │
│ [Tabla DataTable formateada]            │
│  - Moneda: 1.234,56 €                  │
│  - Fecha: 15/03/2024                   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ⚠️ 4. Transacciones Duplicadas          │
│                                         │
│ ⚠️ Atención: Se encontraron 5...        │
│                                         │
│ [Tabla DataTable de duplicados]         │
│                                         │
│ ○ Omitir duplicados (Recomendado)       │
│ ○ Importar todo (creará duplicados)     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ✅ 5. Confirmar Importación             │
│                                         │
│ ℹ️ Se importarán 45 transacciones...    │
│                                         │
│ [✅ Confirmar] [🔄 Cargar Otro Archivo] │
└─────────────────────────────────────────┘
```

---

## Métricas de Éxito

Considera la migración exitosa si:

- ✅ **Funcionalidad:** Todas las funciones de v1 funcionan igual
- ✅ **UX:** Los usuarios pueden completar el flujo sin problemas
- ✅ **Performance:** No hay ralentización perceptible
- ✅ **Estabilidad:** No hay errores en consola
- ✅ **Diseño:** Se ve consistente con el resto de la app

---

## Soporte y Troubleshooting

### Problema: La página no carga después de activar

**Solución:**
1. Verificar que no hay errores en consola del navegador
2. Verificar logs de Streamlit
3. Hacer rollback temporalmente
4. Revisar imports en app.py

### Problema: Los componentes se ven mal

**Solución:**
1. Verificar que los archivos de componentes existen:
   - `/utils/components/page_layout.py`
   - `/utils/components/form_card.py`
   - `/utils/components/data_table.py`
2. Verificar que design_tokens.py está actualizado
3. Limpiar caché del navegador

### Problema: El file uploader no funciona

**Solución:**
1. Verificar que la key es única: `file_uploader_v2`
2. Verificar que el estado se limpia correctamente
3. Probar con otro navegador

### Problema: Las transacciones no se importan

**Solución:**
1. Verificar que la lógica de inserción no cambió
2. Verificar logs de base de datos
3. Comparar con comportamiento de v1
4. Hacer rollback si persiste

---

## Contacto

Si encuentras problemas durante la activación:

1. **Rollback inmediato** (cambia flag a False)
2. **Documenta el error:**
   - Captura de pantalla
   - Logs de consola
   - Pasos para reproducir
3. **Reporta** el problema con toda la información

---

## Conclusión

La versión v2 está lista para ser activada. Sigue esta guía paso a paso para una activación segura y verifica cada punto del checklist. En caso de problemas, el rollback es instantáneo.

**¡Buena suerte con la activación!** 🚀
