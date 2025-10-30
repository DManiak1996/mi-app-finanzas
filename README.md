# 💰 Mi App de Finanzas Personales

Aplicación web para gestión de finanzas personales desarrollada con Streamlit.

## Características

- 📊 Dashboard con métricas y visualizaciones
- 💸 Gestión de transacciones
- 📥 Importación desde Excel
- 🏷️ Clasificación automática de gastos
- 🔐 Autenticación segura
- 📱 Funciona en móvil y escritorio

## Demo

🌐 **App en vivo:** [Próximamente en Streamlit Cloud]

## Uso Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Lanzar aplicación
streamlit run app.py
```

## Configuración para Streamlit Cloud

En Streamlit Cloud > Settings > Secrets, añadir:

```toml
[auth]
authorized_email = "tu-email@gmail.com"
password = "tu-contraseña-segura"
```

## Estructura del Proyecto

- `app.py` - Aplicación principal
- `auth.py` - Sistema de autenticación
- `database/` - Gestión de base de datos SQLite
- `utils/` - Módulos utilitarios (métricas, gráficos, etc.)
- `config/` - Reglas de clasificación

## Tecnologías

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- SQLite

---

Desarrollado con ❤️ y IA (Gemini + Claude)
