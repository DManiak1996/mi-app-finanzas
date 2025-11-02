# Plan de Desarrollo Completo - Aplicación de Gestión de Finanzas Personales

## Contexto del Proyecto

Este documento está dirigido a Gemini Code Assist para guiar el desarrollo de una aplicación de gestión de finanzas personales en Python. El objetivo principal es crear una herramienta que permita importar datos de movimientos bancarios desde archivos Excel, almacenarlos en una base de datos local, clasificarlos automáticamente en categorías, y presentar métricas visuales significativas para el análisis de gastos e ingresos personales.

El usuario actualmente gestiona sus finanzas en un archivo Numbers que exporta a Excel, donde registra manualmente sus gastos categorizados en tres tipos principales: FIJOS (gastos recurrentes como casa, gimnasio), DISFRUTE (gastos variables de ocio y vida diaria), y EXTRAORDINARIOS (gastos puntuales de mayor cuantía). La aplicación debe automatizar este proceso y proporcionar capacidades de análisis superiores.

La estructura del archivo Excel actual incluye una hoja de balance general con resúmenes mensuales y múltiples hojas mensuales con detalles de transacciones. Cada hoja mensual tiene columnas para fecha, concepto, y las tres categorías de gastos. El archivo también contiene hojas duplicadas llamadas "Tabla 1-1" que son subproductos de la exportación desde Numbers y deben ser ignoradas.

## Arquitectura General

La aplicación seguirá una arquitectura modular de tres capas principales. La capa de datos utiliza SQLite como base de datos relacional embebida, perfecta para aplicaciones de escritorio que no requieren servidor. La capa de lógica de negocio contiene módulos utilitarios para lectura de Excel, clasificación automática de transacciones, cálculo de métricas y generación de visualizaciones. La capa de presentación utiliza Streamlit, un framework que permite crear interfaces web modernas ejecutándose localmente con mínimo código.

Esta arquitectura permite desarrollar y probar cada componente de forma independiente, facilita el mantenimiento futuro, y proporciona una clara separación de responsabilidades. SQLite fue elegido porque no requiere instalación de servidor adicional, todo se almacena en un único archivo de base de datos, y ofrece excelente rendimiento para aplicaciones de un solo usuario.

## Fase 0: Configuración del Entorno de Desarrollo

### Estructura de Directorios

Antes de comenzar a escribir código, es fundamental establecer una estructura de directorios clara y organizada. Esto facilitará el desarrollo modular y el mantenimiento futuro del proyecto. La estructura propuesta es la siguiente:

El directorio raíz se llamará `mi_app_finanzas` y contendrá el archivo principal `app.py` que será el punto de entrada de la aplicación Streamlit. El archivo `requirements.txt` listará todas las dependencias necesarias para que otro desarrollador o el mismo usuario pueda recrear el entorno fácilmente.

Dentro del directorio raíz, crearemos un subdirectorio `database` que contendrá todo lo relacionado con la base de datos. Aquí colocaremos `models.py` con las definiciones de las estructuras de datos, `db_manager.py` con las funciones para interactuar con SQLite, y el archivo `finanzas.db` que SQLite creará automáticamente cuando inicialicemos la base de datos.

El subdirectorio `utils` albergará las utilidades de procesamiento. El archivo `excel_reader.py` se encargará de leer y procesar los archivos Excel del banco. El archivo `categorizer.py` implementará la lógica de clasificación automática de transacciones. El archivo `metrics.py` calculará todas las métricas financieras. Y `visualizer.py` generará los gráficos y visualizaciones usando Plotly.

El subdirectorio `config` contendrá archivos de configuración, principalmente `categorias.json` que almacenará las reglas de clasificación automática que el usuario podrá personalizar.

### Instalación de Dependencias

El archivo requirements.txt debe contener las siguientes librerías con sus versiones específicas para asegurar compatibilidad. Streamlit versión 1.28.0 o superior proporciona la interfaz de usuario web. Pandas versión 2.1.0 o superior es fundamental para el manejo de datos tabulares y análisis. Openpyxl versión 3.1.2 permite leer archivos Excel en formato xlsx. Plotly versión 5.17.0 genera gráficos interactivos de alta calidad. SQLite3 viene incluido en la instalación estándar de Python, por lo que no requiere instalación adicional.

Para crear el entorno virtual en macOS, el usuario debe abrir la terminal, navegar hasta el directorio del proyecto, y ejecutar `python3 -m venv venv` para crear un entorno virtual aislado. Luego activará el entorno con `source venv/bin/activate`. El prompt de la terminal cambiará mostrando `(venv)` al inicio, indicando que el entorno está activo. Finalmente, instalará todas las dependencias con `pip install -r requirements.txt`.

Es importante mantener el entorno virtual activo durante todo el desarrollo. Cada vez que el usuario abra una nueva sesión de terminal, deberá activar el entorno nuevamente antes de trabajar en el proyecto.

## Fase 1: Implementación de la Base de Datos

### Diseño del Esquema de Base de Datos

La base de datos es el corazón de la aplicación, donde se almacenará todo el histórico de transacciones financieras. El diseño del esquema debe equilibrar normalización para evitar redundancia con practicidad para consultas rápidas. Dado que es una aplicación personal y no un sistema empresarial de alto volumen, podemos permitirnos cierta desnormalización para simplificar las consultas.

La tabla principal será `transacciones` que almacenará cada movimiento financiero individual. Esta tabla incluirá un campo `id` como clave primaria autoincremental que identifica únicamente cada transacción. El campo `fecha` de tipo DATE almacenará cuándo ocurrió la transacción. El campo `concepto` de tipo TEXT guardará la descripción del movimiento tal como aparece en el extracto bancario. El campo `importe` de tipo REAL almacenará la cantidad monetaria, usando números negativos para gastos y positivos para ingresos. El campo `categoria` de tipo TEXT indicará la clasificación: FIJOS, DISFRUTE, EXTRAORDINARIOS, o INGRESO. El campo `tipo` de tipo TEXT especificará si es GASTO o INGRESO. Los campos `mes` y `año` de tipo INTEGER facilitarán las consultas por período temporal. Finalmente, un campo `notas` de tipo TEXT permite al usuario añadir observaciones adicionales.

Una segunda tabla `categorias_personalizadas` permitirá al usuario definir sus propias categorías más allá de las tres predeterminadas. Esta tabla tendrá campos para `id`, `nombre` de la categoría, `tipo` que indica si es para gastos o ingresos, y `color` en formato hexadecimal para personalizar los gráficos.

La tabla `reglas_clasificacion` almacenará las reglas de clasificación automática. Cada regla tendrá un `patron` de texto que se buscará en el concepto de la transacción, una `categoria` asociada, y un campo `activa` booleano para habilitar o deshabilitar reglas sin eliminarlas.

Opcionalmente, una tabla `presupuestos` puede almacenar límites de gasto mensuales por categoría, permitiendo funcionalidades futuras de alertas de presupuesto.

### Implementación del Archivo models.py

El archivo `database/models.py` debe definir las estructuras SQL para crear las tablas. Este archivo contendrá constantes de string con las sentencias SQL CREATE TABLE. Es importante usar IF NOT EXISTS para que las sentencias sean idempotentes, es decir, se puedan ejecutar múltiples veces sin error.

La sentencia para crear la tabla de transacciones debe especificar cada columna con su tipo de dato y restricciones. Por ejemplo, la columna id debe ser INTEGER PRIMARY KEY AUTOINCREMENT para generar automáticamente valores únicos incrementales. La columna fecha debe ser DATE NOT NULL ya que toda transacción debe tener una fecha. El campo importe debe ser REAL NOT NULL porque toda transacción tiene un monto. Los campos mes y año deben ser INTEGER para facilitar operaciones numéricas y búsquedas rápidas.

Para las categorías personalizadas, la tabla debe permitir que el usuario expanda las categorías predeterminadas. El campo color debe tener un valor por defecto razonable como '#3498db' para que incluso sin especificar color, las visualizaciones funcionen correctamente.

La tabla de reglas de clasificación debe tener una estructura que permita búsquedas eficientes. El campo patron debe ser TEXT NOT NULL e idealmente estar indexado si el volumen de reglas crece. El campo activa debe ser BOOLEAN con valor por defecto TRUE, usando la convención de SQLite donde TRUE es 1 y FALSE es 0.

### Implementación del Archivo db_manager.py

El archivo `database/db_manager.py` es el intermediario entre la aplicación y la base de datos SQLite. Este módulo debe proporcionar una API limpia y fácil de usar para todas las operaciones de base de datos, ocultando los detalles de SQL del resto de la aplicación.

La función de conexión debe establecer una conexión con el archivo de base de datos SQLite. Es importante configurar `check_same_thread=False` para permitir que Streamlit use la conexión desde diferentes hilos. También debe configurar `row_factory = sqlite3.Row` para que los resultados se devuelvan como diccionarios accesibles por nombre de columna en lugar de tuplas.

La función `crear_tablas()` debe importar las definiciones SQL desde models.py y ejecutarlas secuencialmente. Esta función debe llamarse al inicio de la aplicación para asegurar que la base de datos está inicializada. Debe manejar excepciones de forma apropiada y registrar si las tablas se crearon exitosamente o ya existían.

La función `insertar_transaccion()` debe aceptar parámetros para todos los campos de una transacción y ejecutar una sentencia INSERT. Es crucial usar placeholders parametrizados `?` en lugar de formateo de strings para prevenir inyección SQL. La función debe retornar el id de la transacción recién insertada usando `cursor.lastrowid`, lo cual puede ser útil para operaciones subsecuentes.

La función `obtener_transacciones()` debe aceptar filtros opcionales como mes y año, y retornar todas las transacciones que coincidan. Si no se proporcionan filtros, debe retornar todas las transacciones. El resultado debe ser una lista de diccionarios para facilitar su uso en pandas DataFrames.

La función `actualizar_transaccion()` debe aceptar el id de la transacción y un diccionario con los campos a actualizar. Debe construir dinámicamente la sentencia UPDATE basándose en qué campos están presentes en el diccionario. Esto permite actualizaciones parciales sin necesidad de pasar todos los campos.

La función `eliminar_transaccion()` debe aceptar un id y eliminar permanentemente esa transacción. Debe retornar un booleano indicando si la eliminación fue exitosa. Opcionalmente, puede implementarse un sistema de "soft delete" donde las transacciones se marcan como eliminadas pero no se borran físicamente.

### Funciones Adicionales Útiles

Además de las funciones CRUD básicas, el db_manager debe incluir funciones de consulta más especializadas que faciliten las operaciones comunes de la aplicación.

La función `obtener_transacciones_por_periodo()` debe aceptar fechas de inicio y fin y retornar todas las transacciones en ese rango. Esto es útil para análisis de períodos personalizados.

La función `obtener_totales_por_categoria()` debe ejecutar una consulta GROUP BY que sume los importes agrupados por categoría para un mes y año dados. Esto proporciona los datos crudos para gráficos de distribución de gastos.

La función `obtener_balance_mensual()` debe calcular para un mes dado los totales de ingresos, gastos totales, gastos por categoría, y el balance neto. Esta función encapsula una lógica de negocio importante y evita cálculos redundantes en otras partes del código.

La función `buscar_transacciones()` debe permitir búsquedas por concepto usando LIKE para filtrado parcial. Esto facilita encontrar transacciones específicas en la interfaz de usuario.

### Testing de la Base de Datos

Antes de continuar con otras fases, es crítico verificar que la capa de base de datos funciona correctamente. Crear un archivo `test_db.py` en el directorio raíz que importe las funciones del db_manager y ejecute operaciones de prueba.

El script de test debe primero crear las tablas llamando a `crear_tablas()` y verificar que no haya errores. Luego debe insertar varias transacciones de ejemplo con diferentes categorías y fechas. Después debe leer esas transacciones y verificar que los datos recuperados coinciden con los insertados. Debe probar actualizar una transacción y verificar que los cambios se persisten. Finalmente debe probar eliminar una transacción y verificar que ya no existe en la base de datos.

Los asserts o prints deben confirmar cada operación. Si algo falla, el error debe ser claro sobre qué operación falló y por qué. Este script de test será invaluable para detectar problemas temprano antes de integrar con la interfaz de usuario.

## Fase 2: Lectura y Procesamiento de Archivos Excel

### Análisis del Formato de Entrada

El archivo Excel del usuario tiene una estructura particular que debemos entender completamente antes de escribir el código de lectura. Cada hoja mensual llamada "MES - GASTOS MENSUALES" contiene una tabla con columnas específicas. La primera fila es el encabezado con los nombres: FECHA, CONCEPTO, FIJOS, DISFRUTE, EXTRAORDINARIOS.

Las filas subsecuentes contienen las transacciones, pero hay peculiaridades importantes. Algunos conceptos no tienen fecha explícita, como "DISFRUTE MAX" que es una entrada de referencia para el límite de gasto de disfrute. Las transacciones reales tienen fecha y el importe aparece en solo una de las tres columnas de categoría. Las fechas pueden estar en formato de fecha Excel o en formato string como "18/8/25".

Al final de cada hoja mensual hay filas de totales: una fila "TOTAL POR TIPO" que suma cada columna, una fila "TOTAL SIN EXTRA" que suma FIJOS y DISFRUTE excluyendo EXTRAORDINARIOS, y una fila "TOTAL" con la suma absoluta. Estas filas de resumen deben ser identificadas y excluidas del procesamiento de transacciones individuales.

Las hojas "MES - Tabla 1-1" parecen ser metadatos o estructuras auxiliares de Numbers y pueden ser ignoradas completamente. La hoja "BALANCE - BALANCE CUENTA" contiene resúmenes mensuales pero por ahora no es crítica ya que recalcularemos esos resúmenes desde las transacciones individuales.

### Implementación del Lector de Excel

El archivo `utils/excel_reader.py` debe implementar la lógica para leer estos archivos Excel y convertirlos en una estructura de datos limpia y normalizada. La función principal `leer_excel()` debe aceptar una ruta de archivo o un objeto de archivo como parámetro.

El primer paso es abrir el archivo Excel usando openpyxl o pandas. Pandas es generalmente más conveniente ya que lee directamente a DataFrames. La función debe obtener la lista de nombres de hojas y filtrar para quedarse solo con las que contienen "GASTOS MENSUALES" en el nombre, excluyendo las que contienen "Tabla".

Para cada hoja relevante, el código debe leer los datos en un DataFrame. El parámetro `header=0` indica que la primera fila contiene los nombres de columnas. Es importante usar `dtype=str` inicialmente para la columna de fecha porque puede tener formatos mixtos, y luego convertir a datetime de manera más controlada.

Una vez leído el DataFrame, debe limpiarse. Primero, eliminar filas completamente vacías con `dropna(how='all')`. Segundo, identificar y eliminar las filas de totales buscando en la columna CONCEPTO strings que contengan "TOTAL". Tercero, filtrar filas donde todas las columnas de importes (FIJOS, DISFRUTE, EXTRAORDINARIOS) estén vacías, ya que estas son probablemente referencias o comentarios.

Para cada fila válida restante, debe determinarse la categoría. Dado que el importe aparece en solo una de las tres columnas, el código debe verificar cuál columna tiene un valor numérico válido. Si FIJOS tiene un valor, la categoría es "FIJOS". Si DISFRUTE tiene un valor, la categoría es "DISFRUTE". Si EXTRAORDINARIOS tiene un valor, la categoría es "EXTRAORDINARIOS".

El importe debe extraerse de la columna correspondiente y convertirse a float. Es importante manejar posibles errores de conversión si hay valores no numéricos. Los gastos deben almacenarse como números negativos para distinguirlos de los ingresos en el análisis posterior.

La fecha debe parsearse cuidadosamente. Si la celda contiene un objeto datetime de pandas, usarlo directamente. Si es un string, intentar parsearlo con `pd.to_datetime()` especificando posibles formatos como "%d/%m/%y" o "%d/%m/%Y". El mes y año deben extraerse de la fecha parseada para almacenarlos como campos separados en la base de datos.

Cada transacción procesada debe agregarse a una lista como un diccionario con las claves: fecha, concepto, importe, categoria, tipo, mes, año, notas. El campo tipo debe ser "GASTO" para todas estas transacciones. El campo notas puede dejarse vacío inicialmente.

### Manejo de Casos Especiales

Hay varios casos especiales que el código debe manejar robustamente. Si una transacción tiene fecha vacía, puede intentarse inferir la fecha del contexto, o asignar el primer día del mes basándose en el nombre de la hoja. Si un concepto está vacío, puede usarse un valor por defecto como "Sin descripción" para evitar valores NULL.

Algunos bancos usan cantidades positivas para ambos ingresos y gastos, diferenciándolos con otra columna o convención. El código debe ser flexible para detectar si hay transacciones que claramente son ingresos (como "NOMINA" o "TRANSFERENCIA RECIBIDA") y manejarlas apropiadamente incluso si están en las columnas de gastos.

Los importes pueden tener separadores de miles o usar coma decimal en lugar de punto. El código debe normalizar estos formatos antes de convertir a float. Una función auxiliar `limpiar_importe()` puede manejar estas variaciones.

### Validación de Datos

Después de procesar todas las hojas, el código debe validar los datos extraídos. Debe verificar que todas las transacciones tienen fecha válida dentro de un rango razonable (por ejemplo, no fechas del futuro o de hace más de 10 años). Debe verificar que todos los importes son números válidos y no cero. Debe verificar que todas las categorías son una de las esperadas.

Si se encuentran datos inválidos, el código debe loggear advertencias pero no necesariamente fallar completamente. Puede marcar esas transacciones con una categoría especial "REVISAR" para que el usuario las inspeccione manualmente en la interfaz.

### Retorno de Datos

La función `leer_excel()` debe retornar una lista de diccionarios, donde cada diccionario representa una transacción válida y lista para insertar en la base de datos. Esta estructura de datos es ideal porque pandas puede convertirla fácilmente a DataFrame para visualización, y cada diccionario puede pasarse directamente a la función `insertar_transaccion()` del db_manager usando unpacking `**diccionario`.

Opcionalmente, la función puede retornar también un diccionario de estadísticas de la importación: número total de transacciones procesadas, número de transacciones válidas, número de transacciones con advertencias, resumen de totales por categoría. Esto es útil para mostrar feedback al usuario sobre el proceso de importación.

## Fase 3: Sistema de Clasificación Automática

### Diseño del Sistema de Reglas

El sistema de clasificación automática es una característica clave que ahorrará tiempo al usuario. La idea es aprender de las transacciones ya clasificadas para sugerir automáticamente categorías para nuevas transacciones basándose en el concepto.

El enfoque más simple y efectivo es un sistema basado en reglas de coincidencia de patrones. Cada regla asocia un patrón de texto con una categoría. Por ejemplo, si el concepto contiene "ZONA AZUL", se clasifica como DISFRUTE. Si contiene "GYM" o "GIMNASIO", se clasifica como FIJOS.

Las reglas deben almacenarse en un archivo JSON para que sean fáciles de editar sin modificar código. El archivo `config/categorias.json` debe tener una estructura que permita múltiples patrones por categoría y configuración adicional como sensibilidad a mayúsculas o expresiones regulares.

### Estructura del Archivo categorias.json

El archivo JSON debe tener una estructura que permita flexibilidad y crecimiento. Una estructura recomendada es un objeto con una clave "reglas" que contiene un array de objetos de regla. Cada regla debe tener campos para "patron" con el string a buscar, "categoria" con la categoría a asignar, "tipo" indicando si es GASTO o INGRESO, y opcionalmente "prioridad" para cuando múltiples reglas coinciden.

Es útil agrupar patrones relacionados. Por ejemplo, todas las variantes de conceptos relacionados con combustible pueden clasificarse como FIJOS o TRANSPORTE. Los patrones deben ser lo suficientemente específicos para evitar falsos positivos pero lo suficientemente generales para capturar variaciones.

El archivo debe incluir comentarios (aunque JSON estándar no los soporta, se pueden incluir como campos "_comentario" que el código ignora) explicando el propósito de cada sección de reglas. Esto facilita que el usuario entienda y modifique el archivo.

### Implementación del Clasificador

El archivo `utils/categorizer.py` debe implementar la lógica de clasificación. La función principal `clasificar_transaccion()` acepta el concepto de la transacción y opcionalmente otros campos como el importe o la fecha que podrían ser relevantes para reglas más sofisticadas.

La función debe primero cargar las reglas desde el archivo JSON si no están ya en memoria. Para eficiencia, las reglas pueden cargarse una vez al inicio de la aplicación y mantenerse en una variable global o caché.

Para cada regla, el código debe verificar si el patrón aparece en el concepto. La comparación debe ser case-insensitive por defecto usando `concepto.lower()` y `patron.lower()`. Si el patrón contiene caracteres especiales que podrían ser expresión regular, debe escaparse apropiadamente o usar coincidencia de substring simple con `in`.

Cuando múltiples reglas coinciden, debe aplicarse alguna heurística para desempatar. La opción más simple es usar la primera coincidencia. Una opción más sofisticada es usar el campo de prioridad o preferir coincidencias más largas (más específicas) sobre coincidencias más cortas.

Si ninguna regla coincide, la función debe retornar None o una categoría especial "SIN_CLASIFICAR". Esto señala al usuario que debe clasificar manualmente esa transacción, y opcionalmente puede sugerirse crear una nueva regla basada en esa clasificación manual.

### Aprendizaje de Nuevas Reglas

Una funcionalidad avanzada pero muy útil es permitir que el sistema aprenda nuevas reglas basándose en las clasificaciones manuales del usuario. Cuando el usuario clasifica manualmente una transacción que estaba sin clasificar, el sistema puede ofrecer crear una regla basada en esa clasificación.

Por ejemplo, si el usuario clasifica manualmente una transacción con concepto "NETFLIX SPAIN" como DISFRUTE, el sistema puede preguntar: "¿Quieres que en el futuro todas las transacciones con NETFLIX se clasifiquen automáticamente como DISFRUTE?" Si el usuario acepta, se añade una nueva regla al archivo JSON.

Esta funcionalidad requiere funciones adicionales en categorizer.py: `sugerir_regla()` que analiza el concepto y sugiere un patrón relevante (por ejemplo, extraer la palabra clave principal), y `guardar_regla()` que añade la nueva regla al archivo JSON de forma segura preservando las reglas existentes.

### Validación y Corrección de Clasificaciones

El clasificador debe incluir mecanismos de validación para prevenir clasificaciones obviamente erróneas. Por ejemplo, si una transacción tiene un importe muy alto y se clasifica como DISFRUTE, podría ser una señal de error y el sistema puede marcarla para revisión manual.

Debe haber una función `validar_clasificacion()` que acepta una transacción con su clasificación y retorna una confianza entre 0 y 1 o un booleano indicando si la clasificación parece razonable. Factores a considerar incluyen el importe respecto a promedios históricos de esa categoría, la presencia de palabras clave conflictivas, o patrones temporales inusuales.

## Fase 4: Interfaz de Usuario con Streamlit

### Diseño de la Estructura de la Aplicación

Streamlit funciona de manera reactiva, ejecutando el script completo de arriba hacia abajo cada vez que hay interacción del usuario. Esto hace que el código sea muy simple pero requiere pensar cuidadosamente sobre el estado de la aplicación y las operaciones costosas como lectura de base de datos.

El archivo `app.py` debe estructurarse en secciones lógicas. Primero, imports y configuración inicial. Segundo, carga de datos estáticos y inicialización de la base de datos. Tercero, sidebar con controles de navegación e importación. Cuarto, contenido principal que cambia según la vista seleccionada. Quinto, footer con información adicional.

Streamlit permite múltiples páginas usando `st.sidebar.radio()` o `st.tabs()`. Para esta aplicación, las páginas principales serían: Dashboard (vista general con métricas y gráficos), Transacciones (tabla detallada editable), Importar (subir y procesar archivos Excel), Categorías (gestionar reglas de clasificación), Configuración (ajustes generales).

### Implementación del Dashboard

El dashboard es la página principal y debe proporcionar una vista de alto nivel del estado financiero. La parte superior debe mostrar métricas clave usando `st.metric()` en columnas. Por ejemplo, tres métricas en una fila: Total Gastos del mes, Total Ingresos del mes, Balance Neto. Cada métrica puede mostrar un delta comparando con el mes anterior.

Debajo de las métricas, un selector de período permite al usuario elegir el mes y año a visualizar. Esto se implementa con `st.selectbox()` para el mes y año, o un `st.date_input()` con modo de rango para períodos personalizados.

La sección central del dashboard contiene gráficos visuales. El primer gráfico debe ser un pie chart o donut chart mostrando la distribución de gastos por categoría. Este gráfico se genera llamando a la función de visualizer con los datos del período seleccionado.

El segundo gráfico debe ser un gráfico de barras o líneas mostrando la evolución de gastos mes a mes para el año actual o últimos 12 meses. Esto permite identificar tendencias y variaciones estacionales.

Un tercer gráfico puede ser un stacked bar chart comparando gastos vs ingresos mes a mes, mostrando claramente los meses con superávit o déficit.

Debajo de los gráficos, una sección expandible "Ver Detalles" puede mostrar tablas con los top 10 gastos del mes, distribución diaria de gastos, o cualquier otra métrica detallada que sea útil.

### Implementación de la Página de Transacciones

Esta página muestra todas las transacciones en una tabla interactiva usando `st.data_editor()`. Esta función de Streamlit permite edición en línea de DataFrames, lo cual es perfecto para que el usuario corrija fechas, conceptos, categorías o importes directamente en la tabla.

La parte superior debe tener filtros para facilitar la navegación cuando hay muchas transacciones. Filtros útiles incluyen rango de fechas, categoría específica, búsqueda por concepto, y rango de importes. Estos filtros se implementan con widgets de Streamlit y se aplican al DataFrame antes de mostrarlo.

La tabla debe incluir botones de acción por fila, como eliminar transacción o añadir nota. Estos botones se pueden implementar usando columnas adicionales en el DataFrame con emojis o texto que funcionan como botones cuando el usuario edita esa celda.

Cuando el usuario modifica datos en la tabla, Streamlit retorna el DataFrame modificado. El código debe detectar cambios comparando el DataFrame original con el modificado, identificar qué filas cambiaron, y actualizar la base de datos usando `actualizar_transaccion()` del db_manager. Un botón "Guardar Cambios" debe confirmar las modificaciones antes de persistirlas.

Debajo de la tabla, un formulario "Añadir Transacción Manual" permite al usuario ingresar transacciones que no vienen del banco. Este formulario incluye campos para fecha, concepto, importe, categoría, y notas. Al submitir, se inserta en la base de datos y se recarga la tabla.

### Implementación de la Página de Importación

Esta página facilita el proceso de importar nuevos datos desde archivos Excel del banco. Un mensaje explicativo al inicio orienta al usuario sobre cómo exportar datos de su app bancaria y qué formato debe tener el archivo.

Un `st.file_uploader()` permite seleccionar el archivo Excel. Cuando se sube un archivo, el código debe procesarlo inmediatamente llamando a `leer_excel()` del módulo excel_reader. Mientras procesa, mostrar un spinner con `st.spinner("Procesando archivo...")`.

Una vez procesado, mostrar un resumen de lo importado: número de transacciones encontradas, rango de fechas, totales por categoría. Mostrar una preview de las primeras 10 transacciones en una tabla para que el usuario verifique que todo se leyó correctamente.

La preview debe resaltar transacciones sin clasificar o con posibles errores usando colores. Streamlit permite estilizar DataFrames con `df.style.applymap()` o `apply()` para colorear celdas condicionalmente.

Un botón "Confirmar e Importar a Base de Datos" debe estar deshabilitado hasta que se procese un archivo válido. Al clickear, las transacciones se insertan en la base de datos. Debe haber lógica para detectar duplicados basándose en fecha, concepto, e importe para evitar importar dos veces los mismos movimientos.

Después de importar, mostrar un mensaje de éxito con estadísticas finales y un botón para ir directamente al dashboard o página de transacciones para ver los datos importados.

### Gestión del Estado de la Aplicación

Streamlit proporciona `st.session_state` para mantener datos entre reruns del script. Esto es crucial para mantener el estado de la aplicación y evitar recargar datos innecesariamente.

Al inicio de app.py, debe verificarse si ciertos objetos ya existen en session_state. Por ejemplo, la conexión a la base de datos puede abrirse una vez y guardarse en session_state para reutilizarla. Las transacciones cargadas pueden cachearse en session_state y solo recargarse cuando el usuario explícitamente refresca o modifica datos.

Las funciones decoradas con `@st.cache_data` permiten cachear el resultado de operaciones costosas como consultas a base de datos. Por ejemplo, una función que retorna todas las transacciones de un mes puede cachearse para que múltiples componentes de la página puedan usarla sin duplicar consultas.

Es importante limpiar el caché apropiadamente cuando los datos cambian. Si el usuario importa nuevas transacciones, el caché debe invalidarse para reflejar los datos actualizados. Esto se hace con `st.cache_data.clear()` o mediante el uso de `ttl` (time to live) en el decorador de caché.

## Fase 5: Visualizaciones y Gráficos

### Elección de Biblioteca de Visualización

Plotly es la mejor opción para esta aplicación porque genera gráficos interactivos que permiten zoom, hover para ver detalles, y exportación de imágenes. Plotly se integra perfectamente con Streamlit usando `st.plotly_chart()`.

El archivo `utils/visualizer.py` debe contener funciones que aceptan datos en formato pandas DataFrame o listas/diccionarios y retornan objetos Figure de Plotly listos para mostrar.

### Gráfico de Distribución de Gastos por Categoría

La función `grafico_gastos_categoria()` acepta un DataFrame con transacciones y genera un pie chart o donut chart. Debe filtrar solo los gastos (importes negativos) y agrupar por categoría sumando los importes.

El gráfico debe usar colores consistentes para cada categoría. Definir un diccionario de mapeo categoría-color que se use en todos los gráficos para mantener consistencia visual. Por ejemplo, FIJOS siempre azul, DISFRUTE siempre verde, EXTRAORDINARIOS siempre rojo.

Los labels deben mostrar tanto el nombre de la categoría como el porcentaje del total. El hover debe mostrar el importe exacto en euros con dos decimales. La función debe retornar el objeto Figure de Plotly.

### Gráfico de Evolución Temporal

La función `grafico_evolucion_mensual()` genera un gráfico de líneas mostrando cómo varían los gastos totales mes a mes. Acepta un DataFrame con transacciones de múltiples meses.

Primero debe agrupar las transacciones por mes y año, sumando los importes. Luego crear una serie temporal ordenada cronológicamente. El eje X serán los meses, el eje Y los importes totales.

Este gráfico puede tener múltiples líneas: una para gastos totales, otra para ingresos, y otra para el balance neto. Usar colores distintos para cada línea y incluir una leyenda clara.

Opcionalmente, añadir una línea horizontal mostrando el promedio de los últimos 12 meses como referencia. Esto ayuda a identificar meses inusuales.

### Gráfico de Comparación con Período Anterior

La función `grafico_comparativa_periodos()` genera un gráfico de barras agrupadas comparando el mes actual con el mes anterior, desglosado por categoría. Acepta dos DataFrames, uno para cada período a comparar.

Cada grupo de barras representa una categoría, con dos barras: una para el período anterior (color más claro) y otra para el período actual (color más oscuro). Esto permite visualizar rápidamente en qué categorías aumentaron o disminuyeron los gastos.

Debajo de cada grupo, mostrar el delta numérico y porcentual de cambio. Esto facilita la lectura sin tener que hacer cálculos mentales.

### Gráfico de Distribución Diaria

La función `grafico_calendario_gastos()` puede generar un heatmap tipo calendario mostrando los gastos diarios del mes. Cada celda representa un día, coloreada según la cantidad gastada ese día. Los días sin gastos aparecen en blanco o gris muy claro, mientras que días con muchos gastos aparecen en rojo intenso.

Este tipo de visualización es útil para identificar patrones semanales o días específicos con gastos inusuales. Por ejemplo, puede revelar que los fines de semana se gasta consistentemente más.

### Personalización de Gráficos

Todos los gráficos deben tener un estilo consistente que refleje profesionalismo y sea agradable visualmente. Configurar un template global de Plotly al inicio del módulo visualizer con especificaciones de fuentes, colores de fondo, estilos de grid, etc.

Los títulos de gráficos deben ser descriptivos pero concisos. Los ejes deben tener labels claros y unidades apropiadas. Para importes monetarios, usar formato con símbolo de euro y dos decimales.

Los gráficos deben ser responsivos, adaptándose al ancho de la ventana del navegador. Plotly maneja esto automáticamente, pero puede especificarse explícitamente con `fig.update_layout(autosize=True)`.

## Fase 6: Edición Interactiva de Transacciones

### Implementación de la Tabla Editable

Streamlit 1.23+ incluye `st.data_editor()` que transforma un DataFrame en una tabla editable con soporte para diferentes tipos de columnas. Esta funcionalidad es perfecta para permitir al usuario modificar transacciones directamente en la interfaz.

La tabla debe configurarse con tipos de columna apropiados. La columna de fecha debe ser tipo `st.column_config.DateColumn()`, la columna de importe tipo `st.column_config.NumberColumn()` con formato de dos decimales, la columna de categoría tipo `st.column_config.SelectboxColumn()` con las categorías permitidas como opciones.

El parámetro `num_rows="dynamic"` permite al usuario añadir nuevas filas directamente en la tabla, lo cual es conveniente para añadir transacciones manuales rápidamente.

La configuración `hide_index=True` oculta el índice del DataFrame para una apariencia más limpia. El parámetro `use_container_width=True` hace que la tabla ocupe todo el ancho disponible.

### Detección y Persistencia de Cambios

Cuando el usuario edita celdas en el data_editor, Streamlit retorna un nuevo DataFrame con los cambios. El código debe comparar este DataFrame con el original para detectar qué filas fueron modificadas.

Una estrategia efectiva es añadir una columna oculta con el ID de base de datos de cada transacción. Al comparar DataFrames, se puede identificar qué IDs tienen cambios y actualizar solo esas filas en la base de datos.

La comparación puede hacerse con pandas usando `df.compare()` o iterando por las filas y comparando valores. Para eficiencia, solo procesar cambios cuando el usuario clickea un botón "Guardar Cambios" en lugar de actualizar la base de datos en cada rerun.

Cuando se detectan cambios, llamar a `actualizar_transaccion()` del db_manager para cada fila modificada. Mostrar un mensaje de éxito indicando cuántas transacciones fueron actualizadas.

### Validación de Ediciones

Antes de persistir cambios en la base de datos, validar que los nuevos valores son válidos. Por ejemplo, verificar que las fechas están en formato correcto, que los importes son números válidos, que las categorías son valores permitidos.

Si se detectan valores inválidos, mostrar un mensaje de error usando `st.error()` y no permitir guardar hasta que se corrijan. Resaltar las celdas con errores puede hacerse coloreando el DataFrame antes de mostrarlo en el data_editor.

La validación debe ser amigable. Si el usuario ingresa una fecha en formato diferente al esperado, intentar parsearlo en formatos comunes antes de marcar error. Si ingresa un importe con coma decimal, convertirlo automáticamente a punto decimal.

### Eliminación de Transacciones

Junto a la tabla editable, incluir una columna con checkboxes o botones para seleccionar transacciones a eliminar. Esta columna no viene del DataFrame original sino que se añade dinámicamente en la interfaz.

Cuando el usuario marca transacciones para eliminar y clickea un botón "Eliminar Seleccionadas", mostrar un cuadro de confirmación usando `st.confirm()` o similar para prevenir eliminaciones accidentales.

Solo después de confirmar, eliminar las transacciones de la base de datos y recargar la tabla. Mostrar un mensaje indicando cuántas transacciones fueron eliminadas.

Opcionalmente, implementar eliminación "suave" donde las transacciones no se borran permanentemente sino que se marcan como eliminadas y se ocultan de la vista principal. Esto permite deshacer eliminaciones si el usuario se arrepiente.

## Fase 7: Cálculo de Métricas Financieras Avanzadas

### Diseño del Módulo de Métricas

El archivo `utils/metrics.py` debe contener funciones que calculan estadísticas y métricas útiles para análisis financiero personal. Estas funciones deben ser puras, es decir, aceptan datos como entrada y retornan resultados sin efectos secundarios.

Cada función debe estar bien documentada con docstrings explicando qué calcula, qué parámetros acepta, y qué retorna. Esto facilita el mantenimiento y permite que otros desarrolladores entiendan rápidamente qué hace cada función.

### Métrica: Totales Mensuales

La función `calcular_totales_mes()` acepta mes y año y retorna un diccionario con los totales de ese mes: total de ingresos, total de gastos (desglosado por categoría), balance neto, y comparación con el mes anterior.

Esta función debe consultar la base de datos para obtener todas las transacciones del mes especificado, separarlas en ingresos y gastos, y calcular las sumas. Para la comparación con el mes anterior, debe obtener también las transacciones del mes previo y calcular el delta.

El resultado debe ser un diccionario estructurado que sea fácil de mostrar en la interfaz o usar para generar gráficos.

### Métrica: Porcentaje por Categoría

La función `calcular_porcentajes_categoria()` acepta transacciones y retorna un diccionario mapeando cada categoría a su porcentaje del total de gastos. Esto es útil para entender la distribución relativa de gastos.

Primero filtra solo los gastos, suma el importe total, luego agrupa por categoría y calcula qué porcentaje representa cada categoría del total. Los porcentajes deben sumar 100 con precisión, manejando correctamente el redondeo.

### Métrica: Promedio de Ahorro

La función `calcular_ahorro_promedio()` calcula el ahorro promedio mensual basándose en el histórico de transacciones. Acepta un parámetro para especificar el número de meses a considerar, por defecto últimos 12 meses.

Para cada mes en el rango, calcula el balance neto (ingresos menos gastos). Luego calcula el promedio de esos balances. Si hay meses sin datos, deben manejarse apropiadamente, ya sea excluyéndolos del promedio o tratándolos como balance cero.

Esta métrica es valiosa para proyecciones de ahorro a largo plazo y para establecer objetivos financieros realistas.

### Métrica: Identificación de Gastos Inusuales

La función `identificar_gastos_inusuales()` usa estadística para detectar transacciones que son atípicas. Acepta transacciones de un período y retorna una lista de transacciones que están fuera del patrón normal.

El enfoque más simple es calcular el promedio y desviación estándar de los importes por categoría, y marcar como inusual cualquier transacción que esté más de 2 desviaciones estándar por encima del promedio.

Un enfoque más sofisticado puede usar percentiles, marcando como inusual el top 5% de gastos por categoría. O usar análisis temporal, marcando gastos que son inusuales para ese día de la semana o época del mes basándose en patrones históricos.

Estas transacciones inusuales deben destacarse en la interfaz para revisión del usuario, ya que podrían ser errores de clasificación o gastos que merecen atención especial.

### Métrica: Proyección de Balance Futuro

La función `proyectar_balance()` predice el balance de cuenta en fechas futuras basándose en tendencias históricas. Acepta una fecha objetivo y retorna el balance proyectado.

El algoritmo más simple es calcular el promedio de cambio mensual en los últimos N meses y proyectar linealmente ese cambio. Por ejemplo, si en promedio se ahorra 200 euros mensuales, en 6 meses el balance aumentará aproximadamente 1200 euros.

Un algoritmo más sofisticado puede usar regresión lineal o técnicas de serie temporal para capturar tendencias y estacionalidad. Librerías como scikit-learn o statsmodels pueden ser útiles para esto, aunque añaden dependencias adicionales.

La proyección debe incluir intervalos de confianza o margen de error para comunicar la incertidumbre inherente a las predicciones financieras.

### Métrica: Tasa de Ahorro

La función `calcular_tasa_ahorro()` calcula qué porcentaje de los ingresos se está ahorrando. Acepta un período y retorna la tasa de ahorro como porcentaje.

La fórmula es simple: (Ingresos - Gastos) / Ingresos * 100. Sin embargo, debe manejarse el caso donde los gastos superan los ingresos (tasa negativa) y el caso donde no hay ingresos en el período.

Esta métrica es importante para evaluar salud financiera. Una tasa de ahorro saludable generalmente está entre 10% y 20% de los ingresos, aunque varía según circunstancias personales.

## Consideraciones de Rendimiento y Optimización

### Optimización de Consultas a Base de Datos

A medida que se acumulan transacciones, las consultas pueden volverse lentas. Índices en la base de datos son cruciales para mantener rendimiento.

Las columnas fecha, categoria, mes, y año deben tener índices porque son las más usadas en filtros y agregaciones. Crear índices con sentencias CREATE INDEX después de crear las tablas.

Las consultas deben solicitar solo las columnas necesarias en lugar de SELECT *. Esto reduce transferencia de datos y parsing. Por ejemplo, si solo se necesitan importes y categorías para un gráfico, no incluir concepto o notas en la consulta.

Usar GROUP BY y SUM en SQL en lugar de cargar todos los datos en Python y agrupar con pandas. SQLite es muy eficiente en agregaciones y debe aprovecharse esa capacidad.

### Caché de Streamlit

Como mencionado anteriormente, `@st.cache_data` es fundamental para evitar recalcular o recargar datos innecesariamente. Las funciones que consultan la base de datos o calculan métricas complejas deben cachearse.

El decorador puede aceptar parámetros como `ttl=3600` para cachear por una hora, o basarse en cambios de argumentos. Si los argumentos de la función no cambian entre reruns, Streamlit usa el resultado cacheado.

Tener cuidado con cachear objetos mutables como DataFrames. Streamlit hace una copia profunda para prevenir mutaciones accidentales del caché, pero esto puede ser costoso. En general, cachear datos inmutables o DataFrames que no se modificarán.

### Lazy Loading

Para tablas con miles de transacciones, mostrar todas simultáneamente puede ser lento. Implementar paginación o lazy loading mostrando solo las primeras N filas con opciones para cargar más o navegar por páginas.

Streamlit no tiene paginación built-in perfecta, pero puede implementarse manualmente con slicing del DataFrame y botones "Anterior" y "Siguiente" que actualizan un índice en session_state.

Otra opción es cargar datos en demanda basándose en filtros. Mostrar inicialmente solo las transacciones del mes actual, y cargar meses adicionales solo cuando el usuario los selecciona explícitamente.

## Manejo de Errores y Logging

### Estrategia de Manejo de Errores

Todo código que interactúa con archivos, base de datos, o parsing de datos debe estar envuelto en try-except para capturar excepciones y manejarlas gracefully.

Cuando ocurre un error, no debe simplemente crashear la aplicación. En su lugar, mostrar un mensaje claro al usuario usando `st.error()` explicando qué salió mal y posibles soluciones. Por ejemplo, si falla la lectura del Excel, el mensaje puede decir "Error al leer el archivo. Verifica que es un archivo Excel válido y no está corrupto."

Los errores deben loggearse para facilitar debugging. Python incluye el módulo logging que debe configurarse al inicio de la aplicación. Crear un archivo de log que registre errores con timestamps y stack traces.

### Validación de Entradas

Toda entrada del usuario debe validarse antes de procesarse. Si el usuario sube un archivo, verificar que es del tipo esperado. Si ingresa fechas, verificar que están en formato válido. Si ingresa importes, verificar que son números.

La validación debe ser robusta pero permisiva. Intentar corregir errores comunes automáticamente antes de rechazar la entrada. Por ejemplo, si el usuario ingresa una fecha sin ceros leading como "1/8/2025", parsearlo correctamente en lugar de rechazarlo.

Mostrar mensajes de validación en tiempo real cuando sea posible usando widgets de Streamlit que pueden mostrar errores inline.
