# 💰 App de Finanzas Personales

Aplicación web completa para gestión de finanzas personales desarrollada con Streamlit.

## ✨ Características Principales

### 📊 Dashboard Financiero
- **Métricas en tiempo real**: Líquido disponible, balance mensual, tasa de ahorro
- **Gráficos interactivos**: Distribución de gastos, evolución temporal, análisis histórico
- **Análisis avanzado**: Comparativas mensuales/anuales, proyecciones

### 💸 Gestión de Transacciones
- **Importación automática**: Desde Excel (extractos bancarios)
- **Clasificación inteligente**: Sistema de reglas personalizables
- **Añadir gastos manualmente**: Formulario rápido
- **Filtros y búsqueda**: Por fecha, categoría, concepto

### 🔌 Calculadora de Coche Eléctrico
- **Registro de recargas**: Batería, kWh, costes completos (energía + impuestos)
- **Facturas de electricidad**: Seguimiento mensual con participación del coche
- **Estadísticas**: Consumo medio, ahorro vs gasolina, evolución temporal
- **Costes precisos**: Cálculo por franja horaria (valle/llano/punta)

### 🔄 Sincronización
- **Exportación/Importación**: JSON con todas tus transacciones y recargas
- **Fusión inteligente**: Detecta duplicados automáticamente
- **Comparación**: Verifica diferencias entre dispositivos
- **Backup rápido**: Importación por lotes optimizada (20-40x más rápida)

### 🏷️ Categorías Personalizadas
- **3 categorías principales**: FIJOS, EXTRAORDINARIOS, DISFRUTE
- **Reglas automáticas**: Por patrón de texto e importes exactos
- **Editor visual**: Gestiona reglas sin tocar código
- **Reclasificación masiva**: Aplica nuevas reglas a transacciones pasadas

### 🔐 Seguridad
- **Autenticación simple**: Email + contraseña
- **Saldo inicial configurable**: Persiste aunque resetees la BD
- **Datos locales**: SQLite (opcional PostgreSQL para cloud)

### 📱 Multiplataforma
- **Responsive**: Funciona en móvil, tablet y escritorio
- **Cloud**: Deploy en Streamlit Cloud
- **Local**: Ejecución en tu Mac/PC

## 🚀 Inicio Rápido

### Instalación Local

```bash
# Clonar repositorio
git clone <tu-repo>
cd mi_app_finanzas

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Lanzar aplicación
streamlit run app.py
```

La app se abrirá en `http://localhost:8501`

### Deploy en Streamlit Cloud

1. Haz fork/push del repositorio a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repo y selecciona `app.py`
4. En **Settings > Secrets**, añade:

```toml
[auth]
authorized_email = "tu-email@gmail.com"
password = "tu-contraseña-segura"
```

5. ¡Deploy! Tu app estará online en minutos

## 📁 Estructura del Proyecto

```
mi_app_finanzas/
├── app.py                      # Aplicación principal Streamlit
├── auth_simple.py              # Sistema de autenticación
├── pages_coche_electrico.py    # Módulo completo coche eléctrico
├── requirements.txt            # Dependencias Python
├── database/
│   ├── db_manager.py           # Operaciones de base de datos
│   └── models.py               # Definición de tablas SQLite
├── utils/
│   ├── metrics.py              # Cálculos financieros
│   ├── visualizer.py           # Gráficos Plotly
│   ├── excel_reader.py         # Importación Excel
│   ├── categorizer.py          # Clasificación automática
│   ├── sync.py                 # Sincronización/exportación
│   ├── coche_electrico.py      # Cálculos de costes eléctricos
│   └── config_manager.py       # Gestión configuración
├── config/
│   ├── categorias.json         # Reglas de clasificación
│   └── config.json             # Saldo inicial y config
├── docs/                       # Documentación adicional
└── scripts/                    # Scripts de utilidad
    ├── importar_json.py        # Importar backup completo
    └── importar_solo_recargas.py
```

## 🛠️ Tecnologías

- **Python 3.13+**
- **Streamlit** - Framework web
- **Pandas** - Manipulación de datos
- **Plotly** - Gráficos interactivos
- **SQLite** - Base de datos
- **OpenPyXL** - Lectura de Excel

## 📖 Documentación

- [Guía de Sincronización](docs/GUIA_SINCRONIZACION.md)
- [Guía iPhone](docs/GUIA_IPHONE.md)
- [Instrucciones de Deploy](docs/DEPLOY_INSTRUCTIONS.md)
- [Futuras Mejoras](docs/FUTURAS_MEJORAS.md)

## 🔧 Scripts Útiles

```bash
# Importar backup completo
python scripts/importar_json.py ~/Downloads/finanzas_export_xxx.json

# Importar solo recargas
python scripts/importar_solo_recargas.py ~/Downloads/finanzas_export_xxx.json

# Reclasificar transacciones
python scripts/reclasificar_transacciones.py
```

## 💡 Consejos de Uso

### Evitar pérdida de datos en Streamlit Cloud

Streamlit Cloud tiene almacenamiento efímero. Para evitar perder datos:

1. **Exporta regularmente** (cada semana) desde la pestaña "Sincronización"
2. Guarda el JSON en iCloud/Google Drive/Dropbox
3. Si la app se resetea, importa el último JSON

### Saldo inicial

Configura tu saldo inicial en **Configuración > Saldo Inicial** (ej: 2781.72 €). Este valor:
- Se guarda en `config/config.json` (persiste con Git)
- Se suma a todas las transacciones para calcular el líquido disponible
- Sobrevive a resets de la base de datos

## 🤝 Contribuciones

Este es un proyecto personal, pero si tienes ideas o mejoras:
1. Abre un Issue describiendo la propuesta
2. Fork del proyecto
3. Crea una rama con tu feature
4. Pull Request

## 📄 Licencia

Proyecto personal - Úsalo libremente para tus finanzas

---

**Desarrollado con ❤️ y AI** (Claude Code + Anthropic)
_Para abogados que les gusta la tecnología_ 🎓⚖️💻
