# 🔄 Guía de Sincronización

## Cómo Sincronizar entre Mac y Cloud (iPhone)

Tu app ahora tiene un sistema de sincronización manual que te permite mantener tus datos actualizados entre tu Mac local y Streamlit Cloud (iPhone).

---

## 🎯 Funcionamiento

```
┌─────────────┐                         ┌─────────────┐
│   Mac       │  📤 Exportar JSON       │  Cloud      │
│   (Local)   │  ─────────────────→     │  (iPhone)   │
│             │                         │             │
│             │  📥 Importar JSON       │             │
│             │  ←─────────────────     │             │
└─────────────┘                         └─────────────┘
```

---

## 📱 Escenario 1: De Mac a iPhone

### **Situación:**
Has añadido gastos en tu Mac local y quieres verlos en el iPhone.

### **Pasos:**

1. **En Mac (Local):**
   - Abre la app: `http://localhost:8501`
   - Login con tus credenciales
   - Ve a **"Sincronización"**
   - Tab **"📤 Exportar"**
   - Click en **"Generar Archivo de Exportación"**
   - Click en **"⬇️ Descargar Archivo JSON"**
   - Se descarga: `finanzas_export_YYYYMMDD_HHMMSS.json`

2. **Transferir el archivo:**
   - **Opción A:** Envíatelo por email
   - **Opción B:** Súbelo a iCloud/Dropbox
   - **Opción C:** AirDrop a tu iPhone

3. **En iPhone (Cloud):**
   - Abre la app desde Chrome
   - Ve a **"Sincronización"**
   - Tab **"📥 Importar"**
   - Click en **"Selecciona archivo JSON"**
   - Elige el archivo que enviaste
   - Verás un análisis de diferencias:
     ```
     En este dispositivo: 50 transacciones
     En el archivo: 75 transacciones
     En ambos: 50

     ✨ 25 transacciones nuevas encontradas
     ```
   - Expande **"Ver transacciones nuevas"** para revisarlas
   - Click en **"🔄 Importar y Fusionar"**
   - ✅ Listo! Ahora tienes las 75 transacciones en iPhone

---

## 💻 Escenario 2: De iPhone a Mac

### **Situación:**
Has añadido gastos desde el iPhone y quieres verlos en el Mac.

### **Pasos:**

1. **En iPhone (Cloud):**
   - Abre la app desde Chrome
   - Ve a **"Sincronización"**
   - Tab **"📤 Exportar"**
   - Click en **"Generar Archivo de Exportación"**
   - Click en **"⬇️ Descargar Archivo JSON"**
   - El archivo se descarga a tu iPhone

2. **Transferir el archivo:**
   - **Opción A:** Envíatelo por email
   - **Opción B:** Guárdalo en iCloud
   - **Opción C:** AirDrop a tu Mac

3. **En Mac (Local):**
   - Abre la app: `http://localhost:8501`
   - Ve a **"Sincronización"**
   - Tab **"📥 Importar"**
   - Arrastra el archivo JSON o click en "Browse"
   - Verás el análisis de diferencias
   - Click en **"🔄 Importar y Fusionar"**
   - ✅ Sincronizado!

---

## 🔍 Escenario 3: Solo Comparar (Sin Importar)

### **Situación:**
Quieres ver qué diferencias hay sin cambiar nada.

### **Pasos:**

1. En cualquier dispositivo:
   - Ve a **"Sincronización"**
   - Tab **"🔍 Comparar"**
   - Sube el archivo JSON del otro dispositivo
   - Verás un análisis completo:
     - Transacciones solo en este dispositivo
     - Transacciones solo en el archivo
     - Transacciones en ambos

2. **Interpretación:**
   ```
   Solo en este dispositivo: 10
   → Tienes 10 transacciones que el otro no tiene

   Solo en el archivo: 5
   → El otro tiene 5 transacciones que tú no tienes

   En ambos: 100
   → 100 transacciones están sincronizadas
   ```

---

## 🛡️ Detección de Duplicados

El sistema **NUNCA** creará duplicados. Detecta transacciones duplicadas de dos formas:

### **1. Por UUID (ID Único):**
Cada transacción tiene un ID único. Si ya existe, se omite.

### **2. Por Contenido:**
Si dos transacciones tienen:
- Misma fecha
- Mismo importe
- Mismo concepto

Se consideran duplicadas y se omite la nueva.

---

## 💡 Flujo Recomendado

### **Opción A: Sincronización Diaria**
```
Lunes - Viernes:
  - Usas el iPhone para añadir gastos rápidos

Viernes noche:
  - iPhone → Exportar
  - Mac → Importar
  - Ahora tienes todo en Mac para análisis
```

### **Opción B: Sincronización Bidireccional Semanal**
```
Domingo:
  1. Mac → Exportar → Guardar como "mac_export.json"
  2. Cloud → Exportar → Guardar como "cloud_export.json"
  3. Mac → Importar cloud_export.json
  4. Cloud → Importar mac_export.json

✅ Ambos dispositivos 100% sincronizados
```

### **Opción C: Cloud como Fuente de Verdad**
```
- Usas SOLO Cloud (iPhone + navegador)
- Mac solo para análisis offline
- Periódicamente: Cloud → Exportar → Mac → Importar
```

---

## 📊 Estadísticas de Importación

Después de importar, verás:

```
✅ Importación completada

Nuevas: +15        ← Transacciones añadidas
Duplicadas: 5      ← Omitidas (ya existían)
Errores: 0         ← Si hay problemas
```

Si `Nuevas > 0`: ¡Éxito! Se añadieron transacciones.
Si `Duplicadas > 0`: No pasa nada, simplemente no se duplicaron.
Si `Errores > 0`: Revisa los logs o contacta soporte.

---

## ⚠️ Notas Importantes

### **1. Modo "Sobrescribir" está DESACTIVADO**
Por seguridad, solo puedes **fusionar** (añadir nuevas).
NO puedes sobrescribir todo (para evitar pérdida accidental de datos).

### **2. Refresca después de Importar**
Después de importar, refresca la página (F5) para ver los datos actualizados en el Dashboard.

### **3. Base de Datos en Cloud es Efímera**
Streamlit Cloud puede resetear la app si:
- Está inactiva mucho tiempo
- Haces cambios en el código
- Hay mantenimiento de Streamlit

**Solución:** Exporta periódicamente como backup.

### **4. Formato del Archivo**
El archivo JSON tiene esta estructura:
```json
{
  "metadata": {
    "exported_at": "2025-10-30T20:30:00",
    "total_transactions": 127,
    "version": "1.0"
  },
  "transacciones": [
    {
      "id": "uuid-unico",
      "fecha": "2025-10-15",
      "concepto": "Café",
      "importe": -3.5,
      "categoria": "DISFRUTE",
      ...
    }
  ]
}
```

---

## 🆘 Solución de Problemas

### **"Error al procesar el archivo"**
- Verifica que es un archivo JSON válido
- Verifica que fue exportado desde esta misma app
- No edites el JSON manualmente

### **"No hay transacciones nuevas"**
- Ya están sincronizados
- O el archivo es más antiguo que tu DB actual

### **"Muchas duplicadas, pocas nuevas"**
- Normal si ya sincronizaste antes
- Las duplicadas se omiten automáticamente

### **"El archivo no se descarga en iPhone"**
- Verifica permisos de Safari/Chrome
- Prueba desde otro navegador
- O envíate el archivo por email

---

## 🎯 Mejores Prácticas

1. **Exporta semanalmente** como backup
2. **Nombra los archivos** descriptivamente:
   - `mac_2025_10_30.json`
   - `iphone_2025_10_30.json`
3. **Guarda exports antiguos** por si necesitas recuperar algo
4. **Sincroniza antes de cambios grandes** (como resetear DB)
5. **Usa la tab "Comparar"** primero si no estás seguro

---

## 🚀 Ejemplo Completo: Fin de Semana

**Viernes 18:00 - En el trabajo (Mac):**
```
1. Has añadido gastos toda la semana en Mac
2. Dashboard → "Sincronización" → "Exportar"
3. Descargar JSON → Enviarte por email
```

**Viernes 19:00 - Camino a casa (iPhone):**
```
1. Abrir email con JSON en iPhone
2. Abrir app de finanzas en Chrome
3. "Sincronización" → "Importar"
4. Seleccionar archivo del email
5. Revisar diferencias → Importar
6. ✅ Ahora tienes todo en el iPhone
```

**Sábado - Todo el día (iPhone):**
```
1. Añades gastos del fin de semana desde iPhone
2. Cafés, restaurantes, compras...
```

**Domingo 20:00 - En casa (Mac):**
```
1. Quieres actualizar tu Mac con gastos del finde
2. iPhone → "Exportar" → AirDrop a Mac
3. Mac → "Importar" → Fusionar
4. ✅ Ahora Mac tiene TODO sincronizado
5. Haces tus análisis mensuales en pantalla grande
```

---

¿Necesitas más ayuda? Consulta CLAUDE.md o pregunta en GitHub Issues.
