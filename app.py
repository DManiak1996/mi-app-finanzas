# app.py

import streamlit as st
from database import db_manager
from utils import metrics, visualizer, excel_reader, categorizer
import datetime
import pandas as pd
import json
import auth  # Sistema de autenticación

# --- Configuración de la página ---
st.set_page_config(
    page_title="Mi App de Finanzas",
    page_icon="💰",
    layout="wide"
)

# --- Autenticación ---
if not auth.check_authentication():
    st.stop()  # Detiene la ejecución si no está autenticado

# --- Inicialización ---
@st.cache_resource
def inicializar_app():
    """Inicializa la base de datos creando las tablas si es necesario."""
    db_manager.crear_tablas()

inicializar_app()

# --- Barra lateral de navegación ---
st.sidebar.title("Navegación")
pagina_seleccionada = st.sidebar.radio(
    "Elige una página:",
    ["Dashboard", "Transacciones", "Importar", "Categorías", "Configuración"]
)

st.sidebar.markdown("---")
st.sidebar.info("Aplicación de finanzas personales desarrollada con la ayuda de Gemini.")

# Mostrar info de usuario autenticado
auth.show_user_info()

# --- Constantes y utilidades ---
NOMBRES_MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
MESES_INVERTIDO = {v: k for k, v in NOMBRES_MESES.items()}

# --- Contenido principal de la página ---

def mostrar_dashboard():
    st.title("📊 Dashboard")

    # --- Métrica Global: Líquido Disponible ---
    liquido_disponible = metrics.calcular_liquido_disponible()
    st.metric(
        label="**💧 Líquido Disponible (Balance Total)**",
        value=f"{liquido_disponible:.2f} €",
        help="Suma total de todos los ingresos y gastos registrados en la base de datos."
    )
    st.markdown("---")

    # --- Selectores de período ---
    año_actual = datetime.date.today().year
    año = st.sidebar.selectbox("Año", range(año_actual - 5, año_actual + 1), index=5)
    
    st.header(f"Resumen del año {año}")

    tab_mensual, tab_anual = st.tabs(["Vista Mensual", "Vista Anual"])

    with tab_mensual:
        st.subheader("Análisis Mensual")
        mes_actual = datetime.date.today().month
        nombre_mes_seleccionado = st.selectbox("Selecciona un Mes", list(NOMBRES_MESES.values()), index=mes_actual - 1)
        mes = MESES_INVERTIDO[nombre_mes_seleccionado]

        with st.spinner(f"Calculando métricas para {nombre_mes_seleccionado}..."):
            datos_mes = metrics.calcular_totales_mes(mes, año)

            # Métricas clave
            col1, col2, col3 = st.columns(3)
            col1.metric(label="💰 Ingresos del Mes", value=f"{datos_mes['total_ingresos']:.2f} €")
            col2.metric(label="💸 Gastos del Mes", value=f"{datos_mes['total_gastos']:.2f} €")
            col3.metric(
                label="⚖️ Balance del Mes",
                value=f"{datos_mes['balance_neto']:.2f} €",
                delta=f"{datos_mes['balance_neto']:.2f} €",
                delta_color=("normal" if datos_mes['balance_neto'] > 0 else "inverse")
            )

            st.markdown("---")

            # Gráfico de distribución mensual
            col_grafico, col_leyenda = st.columns([2, 1])
            with col_grafico:
                st.subheader(f"Distribución de Gastos de {nombre_mes_seleccionado}")
                fig_distribucion_mes = visualizer.grafico_distribucion_gastos(datos_mes['gastos_por_categoria'])
                if fig_distribucion_mes:
                    st.plotly_chart(fig_distribucion_mes, use_container_width=True)
                else:
                    st.info("No hay datos de gastos para mostrar en este mes.")
            
            with col_leyenda:
                st.subheader("Detalle por Categoría")
                gastos_cat = datos_mes['gastos_por_categoria']
                if gastos_cat:
                    df_gastos = pd.DataFrame(list(gastos_cat.items()), columns=['Categoría', 'Importe'])
                    df_gastos['Importe'] = df_gastos['Importe'].abs()
                    total_gastos = df_gastos['Importe'].sum()
                    df_gastos['Porcentaje'] = (df_gastos['Importe'] / total_gastos * 100).round(2)
                    
                    st.dataframe(
                        df_gastos,
                        column_config={
                            "Importe": st.column_config.NumberColumn(format="%.2f €"),
                            "Porcentaje": st.column_config.NumberColumn(format="%d%%"),
                        },
                        hide_index=True, use_container_width=True)

    with tab_anual:
        st.subheader("Análisis Anual")
        with st.spinner(f"Calculando métricas para el año {año}..."):
            datos_anuales = metrics.calcular_totales_anual(año)
            if datos_anuales:
                # Métricas clave anuales
                col1, col2, col3 = st.columns(3)
                col1.metric(label="💰 Ingresos Anuales", value=f"{datos_anuales['total_ingresos']:.2f} €")
                col2.metric(label="💸 Gastos Anuales", value=f"{datos_anuales['total_gastos']:.2f} €")
                col3.metric(
                    label="⚖️ Balance Anual",
                    value=f"{datos_anuales['balance_neto']:.2f} €",
                    delta=f"{datos_anuales['balance_neto']:.2f} €",
                    delta_color=("normal" if datos_anuales['balance_neto'] > 0 else "inverse")
                )
                st.markdown("---")

                # Gráficos anuales
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Evolución de Ingresos y Gastos")
                    fig_evolucion_anual = visualizer.grafico_evolucion_anual(datos_anuales['evolucion_mensual'], NOMBRES_MESES)
                    if fig_evolucion_anual:
                        st.plotly_chart(fig_evolucion_anual, use_container_width=True)
                    else:
                        st.info("No hay datos para mostrar la evolución anual.")
                
                with col2:
                    st.subheader("Distribución Anual de Gastos")
                    gastos_anuales_cat = datos_anuales['gastos_por_categoria']
                    fig_distribucion_anual = visualizer.grafico_distribucion_gastos(gastos_anuales_cat)
                    
                    if fig_distribucion_anual:
                        st.plotly_chart(fig_distribucion_anual, use_container_width=True)
                        
                        # Crear la leyenda detallada
                        df_gastos_anual = pd.DataFrame(list(gastos_anuales_cat.items()), columns=['Categoría', 'Importe'])
                        df_gastos_anual['Importe'] = df_gastos_anual['Importe'].abs()
                        total_gastos_anual = df_gastos_anual['Importe'].sum()
                        df_gastos_anual['Porcentaje'] = (df_gastos_anual['Importe'] / total_gastos_anual * 100).round(2)
                        
                        st.dataframe(
                            df_gastos_anual,
                            column_config={
                                "Importe": st.column_config.NumberColumn(format="%.2f €"),
                                "Porcentaje": st.column_config.NumberColumn(format="%d%%"),
                            },
                            hide_index=True, use_container_width=True)
                    else:
                        st.info("No hay datos de gastos para mostrar en el gráfico anual.")
            else:
                st.info(f"No se encontraron transacciones para el año {año}.")

    st.markdown("---")
    st.subheader("Evolución Histórica (Últimos 12 meses)")
    df_evolucion = metrics.calcular_evolucion_mensual()
    fig_evolucion = visualizer.grafico_evolucion_mensual(df_evolucion)
    if fig_evolucion:
        st.plotly_chart(fig_evolucion, use_container_width=True)
    else:
        st.info("No hay suficientes datos históricos para mostrar la evolución.")

def mostrar_transacciones():
    st.title("💸 Transacciones")
    st.markdown("Aquí puedes ver, filtrar y editar tus transacciones.")

    # --- Filtros ---
    col1, col2, col3 = st.columns(3)
    with col1:
        # Usar valores por defecto para el mes y año actual
        año_actual = datetime.date.today().year
        mes_actual = datetime.date.today().month
        año = st.selectbox("Año", range(año_actual - 5, año_actual + 1), index=5)
    with col2:
        nombre_mes_seleccionado = st.selectbox("Mes", list(NOMBRES_MESES.values()), index=mes_actual - 1, key="trans_mes_selector")
        mes = MESES_INVERTIDO[nombre_mes_seleccionado]
    with col3:
        # Obtener categorías de la base de datos para el filtro
        # Se podría mejorar el rendimiento cacheando esta llamada
        # (Esta es una simplificación, se podría cachear)
        categorias_db = list(db_manager.obtener_totales_por_categoria(mes, año).keys())
        categorias_seleccionadas = st.multiselect("Categorías", ["Todas"] + categorias_db, default="Todas")

    # --- Cargar y mostrar datos ---
    with st.spinner("Cargando transacciones..."):
        transacciones = db_manager.obtener_transacciones(mes=mes, año=año)
        df_original = pd.DataFrame(transacciones)

        if not df_original.empty:
            df_filtrado = df_original.copy()
            if "Todas" not in categorias_seleccionadas and categorias_seleccionadas:
                df_filtrado = df_filtrado[df_filtrado['categoria'].isin(categorias_seleccionadas)]
            
            # Convertir la columna de fecha a objetos de fecha para el editor
            df_filtrado['fecha'] = pd.to_datetime(df_filtrado['fecha'])

            st.info("Puedes editar las celdas directamente. Haz clic en 'Guardar Cambios' para persistir las modificaciones.")
            
            # Configuración del editor de datos
            configuracion_columnas = {
                "id": st.column_config.NumberColumn("ID", disabled=True),
                "fecha": st.column_config.DateColumn("Fecha", format="YYYY-MM-DD"),
                "concepto": st.column_config.TextColumn("Concepto", width="large"), # 'width' aquí se refiere al tamaño de la columna, no al aviso.
                "importe": st.column_config.NumberColumn("Importe", format="%.2f €"),
                "categoria": st.column_config.SelectboxColumn("Categoría", options=["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "INGRESO", "SIN_CLASIFICAR"], width="medium")
            }
            
            df_editado = st.data_editor(
                df_filtrado,
                column_config=configuracion_columnas,
                num_rows="fixed",
                hide_index=True,
                use_container_width=True
            )

            if st.button("💾 Guardar Cambios"):
                # Asegurarse de que los dataframes originales y editados tengan los mismos tipos y orden de columnas para una comparación justa
                df_original_comp = df_original.set_index('id').sort_index()
                df_editado_comp = df_editado.set_index('id').sort_index()
                
                # Convertir la fecha del df_original a datetime para comparar con el editor
                df_original_comp['fecha'] = pd.to_datetime(df_original_comp['fecha'])
                
                # Encontrar las filas que han cambiado
                try:
                    # `compare` devuelve un DataFrame con las diferencias
                    diferencias = df_original_comp.compare(df_editado_comp)
                except ValueError: # Ocurre si no hay cambios
                    diferencias = pd.DataFrame()
                
                if not diferencias.empty:
                    with st.spinner("Guardando cambios en la base de datos..."):
                        updates_exitosos = 0
                        # Iterar sobre los índices de las filas modificadas
                        for id_transaccion in diferencias.index.unique():
                            # Obtener la fila completa de datos editados
                            fila_editada = df_editado_comp.loc[id_transaccion]
                            campos_a_actualizar = fila_editada.to_dict()
                            # **LA SOLUCIÓN CLAVE**: Convertir Timestamp a objeto date
                            if 'fecha' in campos_a_actualizar and isinstance(campos_a_actualizar['fecha'], pd.Timestamp):
                                campos_a_actualizar['fecha'] = campos_a_actualizar['fecha'].date()
                                
                            if campos_a_actualizar:
                                if db_manager.actualizar_transaccion(id_transaccion, campos_a_actualizar):
                                    updates_exitosos += 1
                    st.success(f"{updates_exitosos} transacciones actualizadas correctamente.")
                    st.rerun()
                else:
                    st.info("No se detectaron cambios para guardar.")
        else:
            st.info("No se encontraron transacciones para el período seleccionado.")

def mostrar_importar():
    st.title("📥 Importar desde Excel")
    st.markdown("Sube aquí tu archivo Excel con los movimientos bancarios para procesarlos e importarlos a la base de datos.")

    uploaded_file = st.file_uploader(
        "Elige un archivo Excel (.xlsx)", 
        type=['xlsx']
    )

    if uploaded_file is not None:
        # Almacenar el estado de la importación en la sesión
        if 'import_data' not in st.session_state or st.session_state.get('uploaded_filename') != uploaded_file.name:
            with st.spinner("Procesando archivo Excel..."):
                transacciones, stats = excel_reader.leer_excel(uploaded_file)
                st.session_state.import_data = transacciones
                st.session_state.import_stats = stats
                st.session_state.uploaded_filename = uploaded_file.name
                # --- Detección de duplicados ---
                st.session_state.nuevas_transacciones = []
                st.session_state.transacciones_duplicadas = []
                for t in transacciones:
                    if db_manager.transaccion_existe(fecha=t['fecha'], importe=t['importe']):
                        st.session_state.transacciones_duplicadas.append(t)
                    else:
                        st.session_state.nuevas_transacciones.append(t)

        stats = st.session_state.import_stats
        transacciones = st.session_state.import_data

        st.subheader("Resumen de la importación")
        if "error" in stats:
            st.error(f"Ocurrió un error al leer el archivo: {stats['error']}")
        else:
            nuevas = st.session_state.get('nuevas_transacciones', [])
            duplicadas = st.session_state.get('transacciones_duplicadas', [])

            col1, col2, col3 = st.columns(3)
            col1.metric("Hojas procesadas", stats.get('total_sheets_processed', 0))
            col2.metric("Transacciones Nuevas", len(nuevas))
            col3.metric("Potenciales Duplicados", len(duplicadas), delta_color="off")

            if transacciones:
                st.subheader("Vista Previa de Transacciones a Importar")
                st.dataframe(pd.DataFrame(nuevas).head(10))

                accion_duplicados = "omitir"
                if duplicadas:
                    st.warning(f"Se han detectado {len(duplicadas)} transacciones que podrían estar ya registradas (misma fecha e importe).")
                    st.write("Transacciones duplicadas detectadas:")
                    st.dataframe(pd.DataFrame(duplicadas))
                    accion_duplicados = st.radio(
                        "¿Qué quieres hacer con estas transacciones duplicadas?",
                        ('Omitir duplicados (Recomendado)', 'Importar todo (creará duplicados)'),
                        key='accion_duplicados'
                    )

                if st.button("✅ Confirmar e Importar"):
                    transacciones_a_importar = []
                    if accion_duplicados == 'Omitir duplicados (Recomendado)':
                        transacciones_a_importar = nuevas
                        st.info(f"Se omitirán {len(duplicadas)} transacciones duplicadas.")
                    else: # Importar todo
                        transacciones_a_importar = transacciones
                        st.warning("Se importarán todas las transacciones, incluyendo posibles duplicados.")

                    if not transacciones_a_importar:
                        st.info("No hay nuevas transacciones para importar.")
                    else:
                        with st.spinner("Importando transacciones..."):
                            count = 0
                            for t in transacciones_a_importar:
                                categoria_final = categorizer.clasificar_transaccion(t['concepto'], t['importe'])
                                db_manager.insertar_transaccion(
                                    fecha=t['fecha'],
                                    concepto=t['concepto'],
                                    importe=t['importe'],
                                    categoria=categoria_final,
                                    tipo=t['tipo'],
                                    mes=t['mes'],
                                    año=t['año'],
                                    notas=t.get('notas', ''),
                                    saldo_posterior=t.get('saldo_posterior')
                                )
                                count += 1
                        
                        st.success(f"¡Éxito! Se importaron {count} nuevas transacciones.")
                        st.balloons()
                        # Limpiar el estado para permitir una nueva subida
                        for key in ['import_data', 'import_stats', 'uploaded_filename', 'nuevas_transacciones', 'transacciones_duplicadas']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.rerun()

def mostrar_categorias():
    st.title("🏷️ Categorías y Reglas de Clasificación")
    st.markdown("Gestiona las reglas que se usan para clasificar automáticamente tus transacciones.")

    # Cargar y mostrar las reglas actuales
    try:
        with open(categorizer.RULES_FILE, 'r', encoding='utf-8') as f:
            reglas_actuales = json.load(f)['reglas']
        st.subheader("Reglas Actuales")

        # Mostrar cada regla en un expander para poder editarla o eliminarla
        for i, regla in enumerate(reglas_actuales):
            patron = regla.get("patron", "")
            importes = regla.get("importes_exactos", [])
            categoria = regla.get("categoria", "N/A")
            
            # Crear un título descriptivo para el expander
            titulo_expander = f"Patrón: `{patron}`" if patron else f"Importes: `{', '.join(map(str, importes))}`"
            titulo_expander += f" -> **{categoria}**"

            with st.expander(titulo_expander):
                st.write(f"**Categoría:** {regla.get('categoria')}")
                st.write(f"**Tipo:** {regla.get('tipo')}")
                if importes:
                    st.write(f"**Importes exactos:** {', '.join(map(str, importes))}")

                col1, col2 = st.columns([1, 0.1])
                
                with col1:
                    # El botón de editar podría abrir un modal o un formulario aquí mismo
                    # Por simplicidad, por ahora solo mostramos la opción
                    if st.button("✏️ Editar", key=f"edit_{i}"):
                        st.info("Funcionalidad de edición en desarrollo. Por ahora, elimina la regla y créala de nuevo.", icon="🚧")

                with col2:
                    if st.button("🗑️ Eliminar", key=f"del_{i}", help="Eliminar esta regla permanentemente"):
                        if categorizer.eliminar_regla(patron):
                            st.success(f"Regla para '{patron}' eliminada.")
                            st.rerun()
                        else:
                            st.error("No se pudo eliminar la regla.")

    except (FileNotFoundError, json.JSONDecodeError):
        st.error("No se pudo cargar el archivo de reglas.")
        reglas_actuales = []
    except KeyError:
        st.info("El archivo de reglas está vacío o no tiene el formato correcto.")
        reglas_actuales = []

    st.markdown("---")

    # Formulario para añadir nueva regla
    st.subheader("Añadir Nueva Regla")
    with st.form(key="nueva_regla_form", clear_on_submit=True):
        nuevo_patron = st.text_input("Patrón de texto (puede ser una expresión regular)")
        importes_str = st.text_input("Importes exactos (opcional, separados por coma, ej: 500, 275)")
        nueva_categoria = st.selectbox("Categoría a asignar", ["FIJOS", "DISFRUTE", "EXTRAORDINARIOS", "INGRESO"])
        nuevo_tipo = st.selectbox("Tipo de transacción", ["GASTO", "INGRESO"])
        
        submit_button = st.form_submit_button(label="✨ Añadir Regla")

        if submit_button:
            if nuevo_patron or importes_str:
                importes_exactos = []
                if importes_str:
                    try:
                        # Convertir el string de importes a una lista de floats
                        importes_exactos = [float(i.strip()) for i in importes_str.split(',')]
                    except ValueError:
                        st.error("El formato de los importes no es válido. Usa números separados por comas (ej: 500, 275.5).")
                        return # Detener la ejecución si hay error
                if categorizer.guardar_regla(nuevo_patron, nueva_categoria, nuevo_tipo, importes_exactos):
                    st.success(f"¡Regla '{nuevo_patron}' -> '{nueva_categoria}' guardada!")
                    st.rerun()
                else:
                    st.error("No se pudo guardar la regla. ¿Quizás el patrón ya existe?")
            else:
                st.warning("Debes proporcionar al menos un patrón de texto o uno o más importes exactos.")

def mostrar_configuracion():
    st.title("⚙️ Configuración")
    st.subheader("Opciones de la Base de Datos")

    if st.button("⚠️ Resetear Base de Datos"):
        confirmacion = st.warning(
            "¿Estás seguro de que quieres resetear la base de datos? ¡Esta acción borrará todos los datos!",
            icon="⚠️"
        )
        if confirmacion:
            with st.spinner("Reseteando la base de datos..."):
                db_manager.resetear_base_de_datos()
            st.success("¡Base de datos reseteada con éxito!")
            st.rerun()
    
    st.write("Aquí irán otros ajustes generales de la aplicación.")

# --- Lógica para mostrar la página seleccionada ---
if pagina_seleccionada == "Dashboard":
    mostrar_dashboard()
elif pagina_seleccionada == "Transacciones":
    mostrar_transacciones()
elif pagina_seleccionada == "Importar":
    mostrar_importar()
elif pagina_seleccionada == "Categorías":
    mostrar_categorias()
elif pagina_seleccionada == "Configuración":
    mostrar_configuracion()