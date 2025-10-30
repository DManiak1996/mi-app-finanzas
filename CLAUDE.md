# Mi App de Finanzas - Documentación del Proyecto

## Descripción General

Aplicación web de gestión de finanzas personales desarrollada con **Streamlit** y **Python**. Permite importar movimientos bancarios desde archivos Excel, clasificarlos automáticamente en categorías personalizadas, y visualizar métricas financieras mediante gráficos interactivos.

### Objetivo Principal
Automatizar el proceso de seguimiento de gastos e ingresos personales que anteriormente se gestionaba manualmente en archivos Numbers/Excel, proporcionando análisis avanzados y visualizaciones dinámicas.

## Tecnologías y Stack

### Core
- **Python 3.8+**: Lenguaje principal
- **Streamlit >= 1.28.0**: Framework para la interfaz web interactiva
- **SQLite3**: Base de datos embebida (incluida en Python)

### Librerías
- **pandas >= 2.1.0**: Manipulación y análisis de datos
- **openpyxl >= 3.1.2**: Lectura de archivos Excel (.xlsx)
- **plotly >= 5.17.0**: Generación de gráficos interactivos

## Estructura del Proyecto

```
mi_app_finanzas/
├── app.py                      # Punto de entrada principal de Streamlit
├── requirements.txt            # Dependencias del proyecto
├── finanzas.db                 # Base de datos SQLite (generada automáticamente)
├── INSTRUCCIONES.md            # Guía de lanzamiento de la aplicación
├── plan_desarrollo_finanzas.md # Documentación detallada del desarrollo
├── launch_app.command          # Script de lanzamiento para macOS
├── test_db.py                  # Script de testing de la base de datos
│
├── database/                   # Capa de datos
│   ├── models.py              # Definiciones SQL de las tablas
│   └── db_manager.py          # Funciones de acceso a la base de datos
│
├── utils/                      # Módulos utilitarios
│   ├── excel_reader.py        # Lectura y procesamiento de archivos Excel
│   ├── categorizer.py         # Clasificación automática de transacciones
│   ├── metrics.py             # Cálculo de métricas financieras
│   └── visualizer.py          # Generación de gráficos con Plotly
│
├── config/                     # Archivos de configuración
│   └── categorias.json        # Reglas de clasificación personalizables
│
└── venv/                       # Entorno virtual (no se versiona)
```

## Arquitectura

### Arquitectura de 3 Capas

1. **Capa de Presentación** (`app.py`)
   - Interfaz de usuario con Streamlit
   - Páginas: Dashboard, Transacciones, Importar, Categorías, Configuración
   - Navegación mediante sidebar con `st.radio()`

2. **Capa de Lógica de Negocio** (`utils/`)
   - Procesamiento de archivos Excel bancarios
   - Sistema de clasificación automática basado en reglas
   - Cálculos de métricas y agregaciones
   - Generación de visualizaciones

3. **Capa de Datos** (`database/`)
   - Gestión de la base de datos SQLite
   - Operaciones CRUD sobre transacciones
   - Consultas optimizadas con índices

## Modelo de Datos

### Tabla Principal: `transacciones`

```sql
CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATE NOT NULL,
    concepto TEXT NOT NULL,
    importe REAL NOT NULL,
    categoria TEXT NOT NULL,
    tipo TEXT NOT NULL,
    mes INTEGER NOT NULL,
    año INTEGER NOT NULL,
    notas TEXT,
    saldo_posterior REAL
)
```

**Campos clave:**
- `importe`: Negativo para gastos, positivo para ingresos
- `categoria`: FIJOS, DISFRUTE, EXTRAORDINARIOS, INGRESO, SIN_CLASIFICAR
- `tipo`: GASTO o INGRESO
- `mes` y `año`: Campos denormalizados para consultas rápidas

### Sistema de Categorías

El proyecto usa un sistema de 3 categorías principales para gastos:

1. **FIJOS**: Gastos recurrentes (alquiler, gimnasio, suscripciones)
2. **DISFRUTE**: Gastos variables de ocio y vida diaria
3. **EXTRAORDINARIOS**: Gastos puntuales de mayor cuantía

Además:
- **INGRESO**: Para todos los ingresos
- **SIN_CLASIFICAR**: Transacciones pendientes de clasificación

## Funcionalidades Principales

### 1. Dashboard (📊)
- **Líquido Disponible**: Métrica global del balance total
- **Resumen Anual**: Selectores de año para análisis temporal
- **Vista Mensual**:
  - Métricas: Ingresos, Gastos, Balance del mes
  - Gráfico de distribución de gastos por categoría (pie chart)
  - Tabla detallada con porcentajes
- **Vista Anual**:
  - Métricas consolidadas del año
  - Evolución mensual de ingresos/gastos (gráfico de líneas)
  - Distribución anual de gastos
- **Evolución Histórica**: Últimos 12 meses

### 2. Transacciones (💸)
- Tabla interactiva editable con `st.data_editor()`
- Filtros por año, mes y categoría
- Edición en línea de campos:
  - Fecha, concepto, importe, categoría
- Guardado de cambios con detección de modificaciones
- Conversión automática de tipos (Timestamp → date)

### 3. Importar desde Excel (📥)
- Upload de archivos `.xlsx`
- Procesamiento automático de hojas mensuales
- **Detección de duplicados**: Por fecha e importe
- Opciones:
  - Omitir duplicados (recomendado)
  - Importar todo (puede crear duplicados)
- Vista previa de transacciones
- Clasificación automática durante la importación
- Feedback con estadísticas de importación

### 4. Categorías (🏷️)
- Gestión visual de reglas de clasificación
- Vista en expanders por regla
- Campos por regla:
  - Patrón de texto (regex)
  - Importes exactos (opcional)
  - Categoría destino
  - Tipo (GASTO/INGRESO)
- Añadir nuevas reglas mediante formulario
- Eliminar reglas (funcionalidad de edición en desarrollo)

### 5. Configuración (⚙️)
- Reset de base de datos (con confirmación)
- Espacio para futuras configuraciones

## Flujo de Trabajo Típico

1. **Exportar movimientos bancarios** a Excel
2. **Importar archivo** en la página "Importar"
3. Sistema **clasifica automáticamente** según reglas
4. Revisar transacciones **SIN_CLASIFICAR** y clasificarlas manualmente
5. Opcionalmente, **crear nuevas reglas** basadas en clasificaciones manuales
6. **Analizar métricas** en el Dashboard
7. **Editar transacciones** si es necesario

## Módulos Detallados

### database/db_manager.py
**Funciones principales:**
- `crear_tablas()`: Inicializa el esquema de la base de datos
- `insertar_transaccion(**kwargs)`: Inserta nueva transacción
- `obtener_transacciones(mes=None, año=None)`: Consulta con filtros opcionales
- `actualizar_transaccion(id, campos)`: Actualización parcial de campos
- `transaccion_existe(fecha, importe)`: Detección de duplicados
- `obtener_totales_por_categoria(mes, año)`: Agregaciones para gráficos
- `resetear_base_de_datos()`: Elimina y recrea todas las tablas

**Optimizaciones:**
- Uso de `row_factory = sqlite3.Row` para acceso por nombre de columna
- Placeholders parametrizados (`?`) para prevenir SQL injection
- Índices en `fecha`, `categoria`, `mes`, `año`

### utils/excel_reader.py
**Función principal:** `leer_excel(archivo)`

**Proceso:**
1. Lee todas las hojas del archivo Excel
2. Filtra hojas con "GASTOS MENSUALES" (excluye "Tabla 1-1")
3. Para cada hoja:
   - Lee DataFrame con `pandas`
   - Limpia filas vacías y totales
   - Extrae fecha, concepto, importe
   - Determina categoría (FIJOS/DISFRUTE/EXTRAORDINARIOS)
   - Convierte importes a negativos (gastos)
   - Parsea fechas en múltiples formatos
4. Retorna lista de diccionarios + estadísticas

**Manejo de casos especiales:**
- Fechas en formatos mixtos (datetime Excel, strings)
- Filas de referencia sin fecha (ej: "DISFRUTE MAX")
- Filas de totales (identificadas por concepto)

### utils/categorizer.py
**Sistema basado en reglas** almacenadas en `config/categorias.json`

**Funciones:**
- `clasificar_transaccion(concepto, importe)`: Aplica reglas de clasificación
- `guardar_regla(patron, categoria, tipo, importes_exactos)`: Añade nueva regla
- `eliminar_regla(patron)`: Elimina regla existente

**Estructura de regla:**
```json
{
  "patron": "NETFLIX|HBO",
  "categoria": "DISFRUTE",
  "tipo": "GASTO",
  "importes_exactos": [9.99, 14.99]
}
```

**Lógica:**
- Matching case-insensitive en el concepto
- Soporte para expresiones regulares
- Matching por importes exactos (opcional)
- Primera coincidencia gana
- Retorna `SIN_CLASIFICAR` si no hay match

### utils/metrics.py
**Funciones de cálculo:**
- `calcular_liquido_disponible()`: Suma total de todos los movimientos
- `calcular_totales_mes(mes, año)`: Métricas mensuales
  - Total ingresos, gastos, balance
  - Desglose por categoría
- `calcular_totales_anual(año)`: Métricas anuales
  - Agregaciones de todo el año
  - Evolución mensual (para gráficos)
- `calcular_evolucion_mensual()`: Últimos 12 meses
  - DataFrame con columnas: mes_año, ingresos, gastos, balance

**Optimizaciones:**
- Consultas SQL con GROUP BY en lugar de agregaciones en Python
- Uso de `@st.cache_data` para cachear resultados
- Cálculos incrementales cuando es posible

### utils/visualizer.py
**Funciones de visualización con Plotly:**
- `grafico_distribucion_gastos(gastos_por_categoria)`: Pie chart
- `grafico_evolucion_anual(datos_mensuales, nombres_meses)`: Line chart
- `grafico_evolucion_mensual(df_evolucion)`: Multi-line chart

**Configuración:**
- Colores consistentes por categoría
- Formato de moneda con símbolo € y 2 decimales
- Interactividad: hover, zoom, pan
- Tooltips con información detallada
- Responsive design (`use_container_width=True`)

## Gestión de Estado

### st.session_state
**Variables de sesión principales:**
- `import_data`: Transacciones procesadas del Excel
- `import_stats`: Estadísticas de la importación
- `uploaded_filename`: Nombre del archivo cargado
- `nuevas_transacciones`: Transacciones no duplicadas
- `transacciones_duplicadas`: Duplicados detectados

**Propósito:**
- Evitar reprocesar archivos en cada rerun
- Mantener estado entre interacciones del usuario
- Cacheo de datos costosos

### @st.cache_resource
Usado en `inicializar_app()` para crear tablas solo una vez al iniciar la aplicación.

## Formato de Archivos Excel

### Estructura Esperada
- **Hojas mensuales**: Nombre contiene "GASTOS MENSUALES"
- **Columnas**: FECHA, CONCEPTO, FIJOS, DISFRUTE, EXTRAORDINARIOS
- **Filas**: Una transacción por fila
- **Importes**: Solo en una columna (la categoría correspondiente)
- **Filas especiales**: Totales (se excluyen), referencias sin fecha (se omiten)

### Hojas Ignoradas
- "Tabla 1-1" (metadatos de Numbers)
- "BALANCE - BALANCE CUENTA" (por ahora)

## Configuración y Lanzamiento

### Requisitos
- Python 3.8 o superior
- macOS, Linux o Windows

### Instalación

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar (macOS/Linux)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

### Script de lanzamiento (macOS)
El archivo `launch_app.command` permite lanzar con doble clic:
- Activa el entorno virtual
- Ejecuta Streamlit
- Abre el navegador automáticamente

## Testing

### test_db.py
Script de prueba de la capa de base de datos:
- Creación de tablas
- Inserción de transacciones
- Lectura y filtrado
- Actualización de registros
- Eliminación

**Ejecutar:**
```bash
python test_db.py
```

## Consideraciones de Diseño

### Decisiones Arquitectónicas

1. **SQLite sobre archivos**:
   - No requiere servidor
   - Perfecto para uso personal
   - Excelente rendimiento para este volumen

2. **Streamlit sobre frameworks tradicionales**:
   - Desarrollo ultra-rápido
   - Actualizaciones reactivas automáticas
   - Ideal para aplicaciones analíticas

3. **Clasificación basada en reglas vs ML**:
   - Más predecible y transparente
   - Fácil de depurar y modificar
   - Sin necesidad de training data
   - Usuario tiene control total

4. **Denormalización (mes, año)**:
   - Trade-off: espacio vs velocidad
   - Facilita consultas por período
   - Redundancia mínima y justificada

### Rendimiento

**Optimizaciones implementadas:**
- Índices en columnas de filtrado frecuente
- `@st.cache_data` para consultas costosas
- Consultas SQL con agregaciones nativas
- Lazy loading de visualizaciones (spinner mientras carga)

**Límites esperados:**
- Decenas de miles de transacciones sin problemas
- Para cientos de miles, considerar paginación

### Seguridad

- **SQL Injection**: Prevenido con placeholders parametrizados
- **Datos sensibles**: Base de datos local (no en la nube)
- **Validación**: Tipos de datos validados antes de insertar

## Extensibilidad

### Funcionalidades Futuras Sugeridas

1. **Categorías personalizadas ilimitadas**
   - Tabla `categorias_personalizadas`
   - Colores personalizables

2. **Presupuestos mensuales**
   - Límites por categoría
   - Alertas al superar presupuesto

3. **Exportación de reportes**
   - PDF con gráficos
   - Excel con análisis

4. **Proyecciones financieras**
   - Predicción de balance futuro
   - Análisis de tendencias

5. **Múltiples cuentas**
   - Soporte para varias cuentas bancarias
   - Consolidación multi-cuenta

6. **Soft delete**
   - Papelera de transacciones eliminadas
   - Posibilidad de recuperar

7. **Backup automático**
   - Exportación periódica de la DB
   - Sincronización con cloud

### Cómo Extender

**Añadir nueva página en Streamlit:**
1. Crear función `mostrar_nueva_pagina()`
2. Añadir opción en `st.sidebar.radio()`
3. Añadir condición en el bloque de lógica de páginas

**Añadir nueva métrica:**
1. Crear función en `utils/metrics.py`
2. Llamarla desde el Dashboard
3. Mostrar con `st.metric()` o en gráfico

**Añadir nueva visualización:**
1. Crear función en `utils/visualizer.py`
2. Retornar objeto `plotly.graph_objects.Figure`
3. Mostrar con `st.plotly_chart()`

## Troubleshooting

### Problemas Comunes

**La aplicación no inicia:**
- Verificar que el entorno virtual está activado
- Verificar que todas las dependencias están instaladas
- Comprobar versión de Python (>= 3.8)

**Error al importar Excel:**
- Verificar formato del archivo (debe ser .xlsx)
- Comprobar que las hojas tienen los nombres esperados
- Revisar que las columnas coinciden con el formato

**Transacciones duplicadas:**
- Sistema detecta duplicados por fecha + importe
- Elegir "Omitir duplicados" en la importación
- Si es intencionado, elegir "Importar todo"

**Gráficos no se muestran:**
- Verificar que hay datos para el período seleccionado
- Comprobar que las transacciones tienen categoría válida
- Revisar console de Streamlit para errores

## Créditos y Licencia

**Desarrollado con la ayuda de:**
- Gemini AI (según nota en sidebar)
- Claude Code (esta documentación)

**Tecnologías Open Source:**
- Streamlit
- Pandas
- Plotly
- SQLite

---

**Última actualización:** Octubre 2025
**Versión:** 1.0
**Mantenedor:** Daniel
