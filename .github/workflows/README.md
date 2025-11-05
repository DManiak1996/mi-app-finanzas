# GitHub Actions - Keep Alive Workflow

## 📋 Descripción

Este workflow mantiene activa tu app de Streamlit Cloud haciendo ping cada 12 horas.

Streamlit Cloud apaga las apps después de varios días sin actividad. Este script evita que eso suceda.

## ⚙️ Configuración

### 1. Actualizar URL de tu App

Edita el archivo `keep-alive.yml` y reemplaza:

```yaml
APP_URL="https://tu-app.streamlit.app"
```

Por la URL real de tu app en Streamlit Cloud (ej: `https://mi-app-finanzas.streamlit.app`)

### 2. Hacer Commit y Push

```bash
git add .github/workflows/
git commit -m "Add: GitHub Actions keep-alive workflow"
git push origin main
```

### 3. Verificar en GitHub

1. Ve a tu repositorio en GitHub
2. Click en la pestaña "Actions"
3. Deberías ver el workflow "Keep Streamlit App Alive"
4. Puedes ejecutarlo manualmente haciendo click en "Run workflow"

## 🕐 Horario de Ejecución

- **Automático**: Cada 12 horas (6:00 AM y 6:00 PM UTC)
- **Manual**: Desde la pestaña Actions de GitHub

## ✅ Verificación

Para verificar que funciona:

1. Ve a Actions en GitHub
2. Click en el último run del workflow
3. Verás los logs con el resultado del ping

## 🔒 Seguridad

- Este workflow **NO** tiene acceso a tu base de datos
- Solo hace una petición HTTP GET pública
- No requiere autenticación (solo visita la URL pública)

## 💰 Costo

**GRATIS** - GitHub Actions ofrece 2,000 minutos/mes gratis.
Este workflow usa ~2 minutos/mes (insignificante).
