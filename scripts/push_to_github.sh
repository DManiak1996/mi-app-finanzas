#!/bin/bash

# Script para subir el repositorio a GitHub

echo "🚀 Subiendo código a GitHub..."
echo ""

# Verificar si ya existe el remote
if git remote | grep -q origin; then
    echo "✅ Remote 'origin' ya configurado"
else
    echo "⚠️  Necesitas añadir el remote de GitHub"
    echo ""
    echo "1. Ve a: https://github.com/new"
    echo "2. Crea un repositorio llamado 'mi-app-finanzas' (Private recomendado)"
    echo "3. NO añadas README, .gitignore ni license"
    echo "4. Copia la URL del repositorio (ejemplo: https://github.com/TU-USUARIO/mi-app-finanzas.git)"
    echo ""
    read -p "Pega la URL de tu repositorio: " REPO_URL

    git remote add origin "$REPO_URL"
    echo "✅ Remote añadido"
fi

echo ""
echo "📤 Subiendo archivos..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡Código subido exitosamente!"
    echo ""
    echo "📋 Próximos pasos:"
    echo "1. Ve a: https://share.streamlit.io/"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Selecciona tu repositorio 'mi-app-finanzas'"
    echo "5. Main file: app.py"
    echo "6. En 'Advanced settings' > 'Secrets', añade:"
    echo ""
    echo "[auth]"
    echo 'authorized_email = "tu-email@gmail.com"'
    echo 'password = "tu-contraseña-segura"'
    echo ""
    echo "7. Click 'Deploy!'"
    echo ""
    echo "📖 Instrucciones completas en: DEPLOY_INSTRUCTIONS.md"
else
    echo ""
    echo "❌ Error al subir. Posibles causas:"
    echo "  - Necesitas configurar credenciales de GitHub"
    echo "  - Usa un Personal Access Token como password"
    echo "  - Genera uno en: https://github.com/settings/tokens"
fi
