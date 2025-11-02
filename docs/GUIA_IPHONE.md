# 📱 Guía de Uso en iPhone

## Instalación como App (2 minutos)

Una vez que tu app esté en Streamlit Cloud:

### Paso 1: Abrir en Safari
1. Abre **Safari** en tu iPhone
2. Ve a la URL de tu app: `https://tu-usuario-mi-app-finanzas-xxx.streamlit.app`
3. Inicia sesión con tu email y contraseña

### Paso 2: Añadir a Pantalla de Inicio
1. Toca el botón **"Compartir"** en la parte inferior (cuadrado con flecha ↑)
2. Scroll hacia abajo
3. Toca **"Añadir a pantalla de inicio"**
4. Personaliza:
   - **Nombre:** "Mis Finanzas" (o lo que prefieras)
   - El icono se añadirá automáticamente
5. Toca **"Añadir"** en la esquina superior derecha

✅ ¡Listo! Ahora tienes un icono en tu home screen.

---

## Uso Diario desde iPhone

### 📊 Ver Dashboard
1. Abre la app desde el icono
2. Ya estás en el Dashboard
3. Desliza para ver:
   - Líquido Disponible
   - Gráficos mensuales
   - Distribución de gastos

**Trucos:**
- Pellizca para hacer zoom en gráficos
- Toca los gráficos para ver detalles
- Usa el selector de mes/año para navegar

---

### ✏️ Añadir Gasto Rápido (desde cualquier lugar)

**Método 1: Formulario Manual**
1. Abre la app
2. Ve a **"Transacciones"** (menú lateral)
3. Scroll hasta el final
4. Usa el formulario **"Añadir Transacción Manual"**
5. Rellena:
   - **Fecha:** Usa el selector de calendario
   - **Concepto:** Ej: "Café en Starbucks"
   - **Importe:** Ej: -3.50 (negativo para gastos)
   - **Categoría:** Selecciona FIJOS/DISFRUTE/EXTRAORDINARIOS
6. Toca **"Añadir"**

**Método 2: Importar desde Excel**
1. Descarga el extracto de tu banco (formato Excel)
2. Guarda en iPhone (Files, iCloud, etc.)
3. Abre la app
4. Ve a **"Importar"**
5. Toca **"Browse files"**
6. Selecciona tu archivo Excel
7. Espera mientras procesa (puede tardar unos segundos)
8. Revisa la preview
9. Toca **"Confirmar e Importar"**

---

## 🎯 Flujos de Uso Recomendados

### Escenario 1: "Acabo de pagar algo y quiero registrarlo"
```
1. Abrir app desde home screen (1 tap)
2. Ir a "Transacciones" (1 tap)
3. Scroll al formulario (swipe)
4. Llenar y añadir (30 segundos)
```
**Tiempo total:** ~1 minuto

### Escenario 2: "Es fin de mes y descargo extracto del banco"
```
1. Descargar Excel del banco
2. Abrir app
3. Ir a "Importar"
4. Seleccionar archivo
5. Confirmar
```
**Tiempo total:** ~2 minutos (procesa automáticamente 100+ transacciones)

### Escenario 3: "Quiero revisar cuánto gasté este mes"
```
1. Abrir app
2. Ya estás en Dashboard
3. Mirar métricas y gráficos
```
**Tiempo total:** ~10 segundos

---

## 🔍 Características Optimizadas para Móvil

### ✅ Funciona Perfecto:
- Dashboard con gráficos interactivos
- Añadir transacciones manuales
- Ver tabla de transacciones
- Filtrar por mes/año
- Importar archivos Excel
- Gestionar categorías

### ⚠️ Limitaciones en Móvil:
- Editar transacciones en tabla (mejor en ordenador)
- Subir archivos muy grandes puede ser lento
- Algunos gráficos se ven mejor en pantalla grande

### 💡 Trucos:
- **Modo horizontal:** Gira el iPhone para ver mejor los gráficos
- **Zoom:** Los gráficos son interactivos, puedes hacer zoom
- **Offline:** No funciona sin internet (requiere conexión)
- **Widgets:** Puedes añadir un widget de Safari para acceso rápido

---

## 📸 Atajos Útiles de iPhone

### Crear Atajo de Siri (Opcional - Avanzado)
1. Abre **Atajos** (app de iOS)
2. Crear nuevo atajo
3. Añadir acción: "Abrir URL"
4. URL: Tu app de Streamlit
5. Nombrar: "Abrir Finanzas"
6. Ahora puedes decir: **"Hey Siri, abrir finanzas"**

### Widget en Home Screen
1. Mantén presionado en home screen
2. Toca el **+** en la esquina
3. Busca "Safari"
4. Añade widget de Safari
5. Configura para que muestre tu app

---

## 🔐 Seguridad en iPhone

### Buenas Prácticas:
- ✅ Usa Face ID / Touch ID para desbloquear iPhone
- ✅ La app requiere login cada vez
- ✅ Cierra sesión si usas iPhone compartido (botón en sidebar)
- ✅ No guardes la contraseña en Safari (mantenla privada)

### Si pierdes el iPhone:
1. La app requiere autenticación
2. Usa "Buscar mi iPhone" para bloquearlo
3. Cambia la contraseña en Streamlit Cloud > Settings > Secrets
4. Tu información sigue segura en la nube

---

## 🆘 Problemas Comunes

### "La app tarda en cargar"
- **Causa:** Streamlit Cloud hiberna apps inactivas (plan free)
- **Solución:** Espera 10-20 segundos en la primera carga del día
- **Tip:** Después de la primera carga, va rápido

### "No puedo subir archivo Excel"
- **Verifica:** El archivo es .xlsx (no .xls ni .csv)
- **Verifica:** El archivo no está corrupto
- **Verifica:** Tienes buena conexión (wifi preferible para archivos grandes)

### "Los gráficos no se ven bien"
- **Solución:** Gira el iPhone a modo horizontal
- **Solución:** Haz zoom con dos dedos
- **Solución:** Prueba en iPad si tienes (se ve genial)

### "La app está en inglés"
- **No debería pasar:** Toda la app está en español
- **Si pasa:** Verifica que estás en la URL correcta

### "Olvidé mi contraseña"
- Ve a tu ordenador
- Abre Streamlit Cloud
- Settings > Secrets
- Cambia la contraseña
- La app se reinicia automáticamente

---

## 📊 Ejemplo de Flujo Completo

### Lunes - Viernes: Gastos Diarios
- Café: Añadir manual (-3€)
- Comida: Añadir manual (-12€)
- Total: 2 minutos al día

### Fin de Mes: Reconciliación
- Descargo extracto del banco
- Lo importo en la app
- La app clasifica automáticamente 90% de transacciones
- Reviso las "SIN_CLASIFICAR" y las categorizo
- **Total: 10 minutos/mes**

### Resultado:
- Dashboard siempre actualizado
- Sé exactamente en qué gasto
- Puedo tomar decisiones informadas
- **Ahorro de tiempo vs Excel manual: ~2 horas/mes**

---

## 🎨 Personalización

### Cambiar Categorías
1. Ve a "Categorías" en la app
2. Añade reglas personalizadas
3. Ejemplo: "SPOTIFY" → DISFRUTE
4. Desde ahora, Spotify se clasifica automáticamente

### Añadir Nuevas Páginas (Requiere código)
- Modifica `app.py` en GitHub
- Haz commit y push
- La app se actualiza automáticamente

---

¿Necesitas más ayuda? Abre un issue en GitHub o consulta DEPLOY_INSTRUCTIONS.md
