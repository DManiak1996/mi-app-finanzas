# 🚀 Instrucciones de Deploy a Streamlit Cloud

## Paso 1: Crear Repositorio en GitHub (5 minutos)

1. Ve a **https://github.com/new**
2. Configura el repositorio:
   - **Repository name:** `mi-app-finanzas` (o el nombre que prefieras)
   - **Description:** "Aplicación de finanzas personales con Streamlit"
   - **Visibilidad:**
     - ✅ **Private** (recomendado - solo tú lo ves)
     - ⚠️ Public (cualquiera puede ver el código, pero NO tus datos)
   - ❌ NO marques "Add a README file"
   - ❌ NO marques "Add .gitignore"
   - ❌ NO marques "Choose a license"
3. Click en **"Create repository"**

## Paso 2: Subir el Código (2 minutos)

GitHub te mostrará instrucciones. Usa estas (ya tienes el repo inicializado):

```bash
# En tu terminal, desde /Users/daniel/mi_app_finanzas:

# Añadir el repositorio remoto (copia la URL de GitHub)
git remote add origin https://github.com/TU-USUARIO/mi-app-finanzas.git

# Subir el código
git branch -M main
git push -u origin main
```

**Importante:** Reemplaza `TU-USUARIO` con tu usuario de GitHub.

Si te pide credenciales:
- **Username:** Tu usuario de GitHub
- **Password:** Usa un **Personal Access Token** (no tu password)
  - Ve a: https://github.com/settings/tokens
  - Click "Generate new token" > "Classic"
  - Dale permisos: `repo` (todos los checkboxes)
  - Copia el token y úsalo como password

## Paso 3: Deploy a Streamlit Cloud (5 minutos)

1. Ve a **https://share.streamlit.io/**
2. Inicia sesión con GitHub (click en "Sign in with GitHub")
3. Autoriza Streamlit Cloud
4. Click en **"New app"**
5. Configura:
   - **Repository:** Selecciona `TU-USUARIO/mi-app-finanzas`
   - **Branch:** `main`
   - **Main file path:** `app.py`
6. Click en **"Advanced settings"** (IMPORTANTE)
7. Añade esto en **"Secrets"**:

```toml
[auth]
authorized_email = "TU-EMAIL@gmail.com"
password = "TU-CONTRASEÑA-SEGURA"
```

8. Click en **"Deploy!"**

⏳ Espera 2-3 minutos mientras se despliega...

## Paso 4: Acceder desde iPhone (2 minutos)

Una vez desplegado, Streamlit te dará una URL tipo:
```
https://tu-usuario-mi-app-finanzas-RANDOM.streamlit.app
```

**En tu iPhone:**

1. Abre Safari
2. Ve a la URL de tu app
3. Inicia sesión con tu email y contraseña
4. Click en el botón **"Compartir"** (el cuadrado con flecha hacia arriba)
5. Scroll y selecciona **"Añadir a pantalla de inicio"**
6. Dale un nombre (ej: "Mis Finanzas")
7. Click en **"Añadir"**

¡Listo! Ya tienes un icono en tu iPhone que abre la app.

## Paso 5: Subir Gastos desde iPhone

**Opción 1: Añadir Transacción Manual**
1. Abre la app desde tu iPhone
2. Ve a "Transacciones"
3. Usa el formulario "Añadir Transacción Manual" (en la parte inferior)
4. Rellena: fecha, concepto, importe, categoría
5. Submit

**Opción 2: Importar Excel desde iPhone**
1. Descarga el Excel del banco en tu iPhone
2. Abre la app
3. Ve a "Importar"
4. Click en "Browse files"
5. Selecciona el archivo Excel
6. Espera procesamiento
7. Confirmar e Importar

## 🔄 Cómo Publicar Actualizaciones

Cuando hagas cambios en el código:

```bash
# Hacer cambios en archivos
git add .
git commit -m "Descripción de los cambios"
git push

# ¡Streamlit Cloud se actualiza automáticamente en 1-2 minutos!
```

## ⚙️ Configuraciones Adicionales

### Cambiar Contraseña

1. Ve a Streamlit Cloud
2. Click en tu app > "Settings" > "Secrets"
3. Edita la contraseña
4. Save
5. La app se reinicia automáticamente

### Añadir Más Usuarios

En Secrets, cambia a:

```toml
[auth]
authorized_emails = ["email1@gmail.com", "email2@gmail.com"]
password = "contraseña-compartida"
```

Y modifica `auth.py` para soportar lista de emails.

## 🆘 Solución de Problemas

### "Module not found"
- Verifica que todas las dependencias estén en `requirements.txt`
- Streamlit Cloud reinstala automáticamente

### "Authentication error"
- Verifica que los Secrets estén configurados correctamente
- El formato debe ser exacto (con comillas)

### App muy lenta
- Normal en el plan free
- Streamlit Cloud hiberna apps inactivas (primer acceso es lento)
- Después va fluido

### Base de datos se resetea
- Streamlit Cloud usa sistema de archivos efímero
- La base de datos se recrea en cada deploy
- Para persistir datos: usar SQLite Cloud o PostgreSQL (avanzado)

## 📱 URLs Importantes

- **Tu App:** https://share.streamlit.io/
- **GitHub Tokens:** https://github.com/settings/tokens
- **Documentación Streamlit:** https://docs.streamlit.io/

---

¿Necesitas ayuda? Consulta la documentación o pregunta en el chat.
