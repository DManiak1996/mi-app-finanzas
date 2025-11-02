# app.py

import streamlit as st
from database import db_manager
from utils import metrics, visualizer, excel_reader, categorizer, sync, coche_electrico, config_manager
import datetime
import pandas as pd
import json
import sqlite3
import plotly.graph_objects as go
import auth_simple as auth  # Sistema de autenticación (sin cookies temporalmente)

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

# Sincronizar navegación por botón con radio
PAGINAS = ["Dashboard", "Añadir Gasto", "Transacciones", "Importar", "Categorías", "🔌 Coche Eléctrico", "Sincronización", "Configuración"]

if 'pagina_navegacion' in st.session_state:
    indice_inicial = PAGINAS.index(st.session_state['pagina_navegacion'])
    del st.session_state['pagina_navegacion']  # Limpiar después de usarlo
else:
    indice_inicial = 0

pagina_seleccionada = st.sidebar.radio(
    "Elige una página:",
    PAGINAS,
    index=indice_inicial
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
    st.title("📊 Dashboard Financiero")

    # --- Selectores de período en columnas ---
    col_selector1, col_selector2, col_selector3, col_selector4 = st.columns([1, 1, 2, 1])

    año_actual = datetime.date.today().year
    mes_actual = datetime.date.today().month

    with col_selector1:
        año = st.selectbox("📅 Año", range(año_actual - 5, año_actual + 1), index=5)

    with col_selector2:
        nombre_mes_seleccionado = st.selectbox("📆 Mes", list(NOMBRES_MESES.values()), index=mes_actual - 1)
        mes = MESES_INVERTIDO[nombre_mes_seleccionado]

    with col_selector3:
        # Métrica Global: Líquido Disponible
        liquido_disponible = metrics.calcular_liquido_disponible()
        st.metric(
            label="💧 Líquido Disponible Total",
            value=f"{liquido_disponible:.2f} €",
            help="Balance acumulado de todas tus transacciones"
        )

    with col_selector4:
        # Botón para añadir gasto
        st.markdown("<br>", unsafe_allow_html=True)  # Espaciado para alinear con los selectores
        if st.button("➕ Añadir Gasto", type="primary", use_container_width=True):
            st.session_state['pagina_navegacion'] = "Añadir Gasto"
            st.rerun()

    st.markdown("---")

    # Tabs principales reorganizados
    tab_resumen, tab_analisis, tab_historico = st.tabs([
        "📊 Resumen General",
        "📈 Análisis Avanzado",
        "📉 Histórico"
    ])

    # ========== TAB 1: RESUMEN GENERAL ==========
    with tab_resumen:
        # Sub-tabs para mensual y anual
        subtab_mes, subtab_año = st.tabs([f"📆 {nombre_mes_seleccionado} {año}", f"📅 Año {año}"])

        with subtab_mes:
            with st.spinner("Calculando métricas mensuales..."):
                datos_mes = metrics.calcular_totales_mes(mes, año)

                # Métricas principales en cards
                col1, col2, col3, col4 = st.columns(4)
                col1.metric(
                    "💰 Ingresos",
                    f"{datos_mes['total_ingresos']:.2f} €",
                    help="Suma de todos los ingresos del mes seleccionado"
                )
                col2.metric(
                    "💸 Gastos",
                    f"{abs(datos_mes['total_gastos']):.2f} €",
                    help="Suma total de todos los gastos del mes (en valor absoluto)"
                )
                col3.metric(
                    "⚖️ Balance",
                    f"{datos_mes['balance_neto']:.2f} €",
                    delta=f"{datos_mes['balance_neto']:.2f} €",
                    delta_color="normal" if datos_mes['balance_neto'] > 0 else "inverse",
                    help="Diferencia entre ingresos y gastos (Ingresos - Gastos). Positivo = superávit, Negativo = déficit"
                )

                # Tasa de ahorro rápida
                tasa = metrics.calcular_tasa_ahorro(mes, año)
                col4.metric(
                    "💾 Tasa Ahorro",
                    f"{tasa['tasa_ahorro']:.1f}%",
                    delta=f"{tasa['ahorro_absoluto']:.0f} €",
                    help="Porcentaje de tus ingresos que has logrado ahorrar. Ideal: >20%. Te ayuda a medir tu capacidad de ahorro"
                )

                st.markdown("---")

                # Gráficos en columnas
                col_grafico, col_detalle = st.columns([2, 1])

                with col_grafico:
                    st.markdown("### 📊 Distribución de Gastos")
                    fig = visualizer.grafico_distribucion_gastos(datos_mes['gastos_por_categoria'])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True, key="plot_gastos_mes")
                    else:
                        st.info("Sin datos de gastos")

                with col_detalle:
                    st.markdown("### 📋 Desglose")
                    if datos_mes['gastos_por_categoria']:
                        df = pd.DataFrame(list(datos_mes['gastos_por_categoria'].items()),
                                        columns=['Categoría', 'Importe'])
                        df['Importe'] = df['Importe'].abs()
                        total = df['Importe'].sum()
                        df['%'] = (df['Importe'] / total * 100).round(1)

                        st.dataframe(
                            df,
                            column_config={
                                "Importe": st.column_config.NumberColumn(format="%.0f €"),
                                "%": st.column_config.NumberColumn(format="%.1f%%"),
                            },
                            hide_index=True,
                            use_container_width=True
                        )

                st.markdown("---")

                # Gráfico de evolución del saldo disponible
                st.markdown("### 📈 Evolución del Saldo Disponible")
                transacciones = db_manager.obtener_transacciones(mes=mes, año=año)

                if transacciones:
                    df_trans = pd.DataFrame(transacciones)
                    df_trans['fecha'] = pd.to_datetime(df_trans['fecha'])
                    df_trans = df_trans.sort_values('fecha')

                    # Calcular el saldo inicial del mes:
                    # Líquido disponible total MENOS las transacciones del mes actual
                    liquido_total = metrics.calcular_liquido_disponible()
                    importe_mes_actual = df_trans['importe'].sum()
                    saldo_inicial = liquido_total - importe_mes_actual

                    # Añadir punto inicial del mes (saldo al cierre del mes anterior)
                    fecha_inicial = df_trans['fecha'].min() - pd.Timedelta(days=1)
                    df_inicial = pd.DataFrame([{
                        'fecha': fecha_inicial,
                        'importe': 0,
                        'saldo_disponible': saldo_inicial
                    }])

                    # Combinar con las transacciones del mes
                    df_trans['saldo_disponible'] = saldo_inicial + df_trans['importe'].cumsum()
                    df_completo = pd.concat([df_inicial, df_trans[['fecha', 'saldo_disponible']]], ignore_index=True)

                    # Crear gráfico de línea
                    fig = go.Figure()

                    # Preparar etiquetas de fecha para el eje X
                    df_completo['fecha_str'] = df_completo['fecha'].dt.strftime('%d/%m/%Y')

                    # Línea de evolución del saldo (usando índices para equidistancia)
                    fig.add_trace(go.Scatter(
                        x=df_completo['fecha_str'],
                        y=df_completo['saldo_disponible'],
                        mode='lines+markers',
                        name='Saldo',
                        line=dict(color='#1f77b4', width=2.5),
                        marker=dict(
                            size=8,
                            color=df_completo['saldo_disponible'],
                            colorscale=[[0, '#ef5350'], [0.5, '#ff9800'], [1, '#26a69a']],
                            showscale=False,
                            line=dict(width=1, color='white')
                        ),
                        fill='tonexty',
                        fillcolor='rgba(31, 119, 180, 0.1)',
                        hovertemplate='<b>%{x}</b><br>Saldo: %{y:.2f} €<extra></extra>'
                    ))

                    # Línea de referencia en y=0
                    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5,
                                 annotation_text="Break Even", annotation_position="right")

                    # Línea de saldo inicial
                    fig.add_hline(y=saldo_inicial, line_dash="dot", line_color="blue", opacity=0.3,
                                 annotation_text=f"Inicial: {saldo_inicial:.0f}€",
                                 annotation_position="left")

                    fig.update_layout(
                        title=f"Evolución del Saldo - {nombre_mes_seleccionado} {año}",
                        xaxis_title="Fecha",
                        yaxis_title="Saldo Disponible (€)",
                        hovermode='closest',
                        height=450,
                        showlegend=False,
                        xaxis=dict(
                            tickangle=-45,
                            tickmode='auto',
                            nticks=20
                        )
                    )

                    st.plotly_chart(fig, use_container_width=True, key="plot_evolucion_saldo_mes")

                    # Estadísticas del mes
                    col1, col2, col3, col4 = st.columns(4)
                    num_transacciones = len(df_trans)
                    col1.metric(
                        "📊 Transacciones",
                        num_transacciones,
                        help="Número total de transacciones registradas en el mes"
                    )
                    col2.metric(
                        "📈 Saldo Inicial",
                        f"{saldo_inicial:.2f} €",
                        help="Saldo disponible al inicio del mes (cierre del mes anterior)"
                    )
                    col3.metric(
                        "💰 Saldo Final",
                        f"{df_trans['saldo_disponible'].iloc[-1]:.2f} €",
                        delta=f"{df_trans['saldo_disponible'].iloc[-1] - saldo_inicial:.2f} €",
                        help="Saldo disponible al final del mes con la variación respecto al inicio"
                    )
                    col4.metric(
                        "📊 Variación (Max-Min)",
                        f"{df_trans['saldo_disponible'].max() - df_trans['saldo_disponible'].min():.2f} €",
                        help="Diferencia entre el saldo máximo y mínimo alcanzado durante el mes"
                    )
                else:
                    st.info("No hay transacciones registradas en este mes")

        with subtab_año:
            with st.spinner("Calculando métricas anuales..."):
                datos_anuales = metrics.calcular_totales_anual(año)

                if datos_anuales:
                    # Métricas anuales
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric(
                        "💰 Ingresos Anuales",
                        f"{datos_anuales['total_ingresos']:.2f} €",
                        help="Suma total de ingresos en todos los meses del año"
                    )
                    col2.metric(
                        "💸 Gastos Anuales",
                        f"{abs(datos_anuales['total_gastos']):.2f} €",
                        help="Suma total de gastos en todos los meses del año"
                    )
                    col3.metric(
                        "⚖️ Balance Anual",
                        f"{datos_anuales['balance_neto']:.2f} €",
                        delta_color="normal" if datos_anuales['balance_neto'] > 0 else "inverse",
                        help="Balance neto del año completo (Total Ingresos - Total Gastos)"
                    )

                    # Ahorro anual
                    ahorro_anual = datos_anuales['balance_neto']
                    if datos_anuales['total_ingresos'] > 0:
                        tasa_anual = (ahorro_anual / datos_anuales['total_ingresos']) * 100
                    else:
                        tasa_anual = 0
                    col4.metric(
                        "💾 Tasa Ahorro Anual",
                        f"{tasa_anual:.1f}%",
                        help="Porcentaje de ahorro sobre el total de ingresos del año. Mide tu capacidad de ahorro anual"
                    )

                    st.markdown("---")

                    # Gráficos anuales
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 📈 Evolución Mensual")
                        fig = visualizer.grafico_evolucion_anual(datos_anuales['evolucion_mensual'], NOMBRES_MESES)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True, key="plot_evolucion_anual")

                    with col2:
                        st.markdown("### 📊 Distribución Anual")
                        fig = visualizer.grafico_distribucion_gastos(datos_anuales['gastos_por_categoria'])
                        if fig:
                            st.plotly_chart(fig, use_container_width=True, key="plot_distribucion_anual")
                else:
                    st.info(f"No hay datos para el año {año}")

    # ========== TAB 2: ANÁLISIS AVANZADO ==========
    with tab_analisis:
        analisis_tabs = st.tabs(["📆 Mensual", "📅 Anual"])

        # ANÁLISIS MENSUAL
        with analisis_tabs[0]:
            with st.spinner("Calculando análisis avanzado..."):
                # Financial Health Score destacado
                health = metrics.calcular_financial_health_score(mes, año)

                st.markdown("### 🏆 Financial Health Score")

                score_cols = st.columns([1, 2, 1])
                with score_cols[1]:
                    # Score grande y centrado
                    score_emoji = {
                        'verde': '🌟',
                        'azul': '👍',
                        'amarillo': '⚠️',
                        'rojo': '❌'
                    }.get(health['color'], '📊')

                    st.markdown(f"""
                    <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
                        <h1 style='font-size: 4em; margin: 0;'>{health['score']}</h1>
                        <p style='font-size: 1.5em; margin: 0;'>{score_emoji} {health['evaluacion']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # Métricas en expanders organizados
                with st.expander("💰 Ahorro y Proyecciones", expanded=True):
                    col1, col2, col3 = st.columns(3)

                    tasa_ahorro = metrics.calcular_tasa_ahorro(mes, año)
                    col1.metric(
                        "Tasa de Ahorro",
                        f"{tasa_ahorro['tasa_ahorro']:.1f}%",
                        delta=f"{tasa_ahorro['ahorro_absoluto']:.0f} €",
                        help="% de tus ingresos que lograste ahorrar. Ideal >20%. Útil para evaluar tu disciplina financiera"
                    )

                    gasto_diario = metrics.calcular_gasto_promedio_diario(mes, año)
                    col2.metric(
                        "Gasto Promedio/Día",
                        f"{gasto_diario['promedio_diario']:.2f} €",
                        delta=f"Proyección mes: {gasto_diario['proyeccion_mes']:.0f} €",
                        help="Cuánto gastas en promedio cada día. Te ayuda a controlar tus gastos diarios y proyectar el total del mes"
                    )

                    proyeccion = metrics.calcular_proyeccion_balance(3)
                    col3.metric(
                        "Balance en 3 Meses",
                        f"{proyeccion['balance_proyectado']:.0f} €",
                        delta=f"Confianza: {proyeccion['confianza']}",
                        help="Proyección de tu balance en 3 meses basado en tu comportamiento histórico. Útil para planificar gastos futuros"
                    )

                with st.expander("📊 Efficiency Ratios"):
                    ratios = metrics.calcular_efficiency_ratios(mes, año)
                    st.info(f"**{ratios['evaluacion']}**")

                    col1, col2, col3 = st.columns(3)
                    col1.metric(
                        "FIJOS/Ingresos",
                        f"{ratios.get('ratio_fijos', 0):.1f}%",
                        delta="Ideal <30%",
                        help="% de gastos fijos sobre tus ingresos. Ideal <30%. Mide qué porción de tus ingresos va a gastos obligatorios (vivienda, servicios, etc.)"
                    )
                    col2.metric(
                        "DISFRUTE/Ingresos",
                        f"{ratios.get('ratio_disfrute', 0):.1f}%",
                        delta="Ideal <30%",
                        help="% de gastos de disfrute sobre tus ingresos. Ideal <30%. Mide cuánto destinas a ocio, entretenimiento y placeres personales"
                    )
                    col3.metric(
                        "EXTRA/Ingresos",
                        f"{ratios.get('ratio_extraordinarios', 0):.1f}%",
                        delta="Ideal <10%",
                        help="% de gastos extraordinarios sobre tus ingresos. Ideal <10%. Gastos imprevistos o no recurrentes que afectan tu presupuesto"
                    )

                with st.expander("📉 Variación vs Mes Anterior"):
                    variacion = metrics.calcular_variacion_mensual(mes, año)

                    if variacion['gastos_anterior'] > 0:
                        delta = variacion['variacion_total']
                        if delta < 0:
                            st.success(f"✅ **{abs(delta):.1f}% menos** que el mes pasado")
                        elif delta > 0:
                            st.warning(f"⚠️ **{delta:.1f}% más** que el mes pasado")
                        else:
                            st.info("➡️ Gastos similares")

                        col1, col2 = st.columns(2)
                        col1.metric("Mes Actual", f"{variacion['gastos_actual']:.2f} €")
                        col2.metric("Mes Anterior", f"{variacion['gastos_anterior']:.2f} €")

                        # Por categoría
                        for cat, datos in variacion['por_categoria'].items():
                            if datos['variacion'] != 0:
                                icono = "📈" if datos['variacion'] > 0 else "📉"
                                st.caption(f"{icono} **{cat}**: {datos['variacion']:+.1f}%")
                    else:
                        st.info("Sin datos del mes anterior")

                with st.expander("🔝 Top 10 Gastos"):
                    top = metrics.calcular_top_gastos(mes, año, 10)
                    if top:
                        df = pd.DataFrame(top)
                        df['importe'] = df['importe'].abs()
                        st.dataframe(
                            df[['fecha', 'concepto', 'importe', 'categoria']],
                            column_config={
                                "fecha": "Fecha",
                                "concepto": "Concepto",
                                "importe": st.column_config.NumberColumn("Importe", format="%.2f €"),
                                "categoria": "Categoría"
                            },
                            hide_index=True,
                            use_container_width=True
                        )

                        total_top = df['importe'].sum()
                        datos_mes_top = metrics.calcular_totales_mes(mes, año)
                        pct = (total_top / abs(datos_mes_top['total_gastos'])) * 100
                        st.caption(f"💡 Representan el **{pct:.1f}%** del total")

                with st.expander("🔍 Desglose del Health Score"):
                    col1, col2, col3, col4 = st.columns(4)
                    desg = health['desglose']

                    col1.metric(
                        "Ahorro",
                        f"{desg['ahorro']}/30",
                        help="Puntos por tu capacidad de ahorro. Máximo 30pts. Basado en tu tasa de ahorro mensual"
                    )
                    col2.metric(
                        "Eficiencia",
                        f"{desg['eficiencia_fijos']}/25",
                        help="Puntos por eficiencia en gastos fijos. Máximo 25pts. Cuanto menor sea tu ratio de gastos fijos, más puntos"
                    )
                    col3.metric(
                        "Estabilidad",
                        f"{desg['estabilidad']}/25",
                        help="Puntos por estabilidad financiera. Máximo 25pts. Basado en tu balance positivo y consistencia"
                    )
                    col4.metric(
                        "Tendencia",
                        f"{desg['tendencia']}/20",
                        help="Puntos por tendencia de mejora. Máximo 20pts. Si gastas menos que el mes anterior, ganas puntos"
                    )

        # ANÁLISIS ANUAL
        with analisis_tabs[1]:
            st.markdown("### 📅 Métricas Anuales Avanzadas")

            datos_anuales = metrics.calcular_totales_anual(año)

            if datos_anuales:
                col1, col2, col3 = st.columns(3)

                # Ahorro anual total
                ahorro_anual = datos_anuales['balance_neto']
                ingresos_anuales = datos_anuales['total_ingresos']
                gastos_anuales = abs(datos_anuales['total_gastos'])

                tasa_ahorro_anual = (ahorro_anual / ingresos_anuales * 100) if ingresos_anuales > 0 else 0

                col1.metric(
                    "💰 Ahorro Anual Total",
                    f"{ahorro_anual:.2f} €",
                    delta=f"Tasa: {tasa_ahorro_anual:.1f}%",
                    help="Total ahorrado en el año completo. La tasa muestra qué % de tus ingresos anuales has logrado ahorrar"
                )

                # Promedio mensual
                promedio_gasto_mensual = gastos_anuales / 12
                col2.metric(
                    "📊 Promedio Gasto/Mes",
                    f"{promedio_gasto_mensual:.2f} €",
                    help="Gasto promedio mensual del año. Útil para establecer un presupuesto mensual realista"
                )

                promedio_ingreso_mensual = ingresos_anuales / 12
                col3.metric(
                    "💵 Promedio Ingreso/Mes",
                    f"{promedio_ingreso_mensual:.2f} €",
                    help="Ingreso promedio mensual del año. Te ayuda a entender tu capacidad financiera mensual típica"
                )

                st.markdown("---")

                # Mejor y peor mes
                evol = datos_anuales['evolucion_mensual']
                if not evol.empty and 'balance' in evol.columns:
                    mejor_mes_idx = evol['balance'].idxmax()
                    peor_mes_idx = evol['balance'].idxmin()

                    col1, col2 = st.columns(2)

                    with col1:
                        st.success(f"🌟 **Mejor Mes:** {NOMBRES_MESES.get(mejor_mes_idx + 1, 'N/A')}")
                        st.write(f"Balance: {evol.loc[mejor_mes_idx, 'balance']:.2f} €")

                    with col2:
                        st.error(f"⚠️ **Peor Mes:** {NOMBRES_MESES.get(peor_mes_idx + 1, 'N/A')}")
                        st.write(f"Balance: {evol.loc[peor_mes_idx, 'balance']:.2f} €")

                st.markdown("---")

                # Distribución anual por categoría
                st.markdown("### 📊 Distribución Anual Detallada")

                gastos_cat = datos_anuales['gastos_por_categoria']
                if gastos_cat:
                    df_cat = pd.DataFrame(list(gastos_cat.items()), columns=['Categoría', 'Total'])
                    df_cat['Total'] = df_cat['Total'].abs()
                    df_cat['%'] = (df_cat['Total'] / df_cat['Total'].sum() * 100).round(1)
                    df_cat['Promedio/Mes'] = (df_cat['Total'] / 12).round(2)

                    st.dataframe(
                        df_cat,
                        column_config={
                            "Total": st.column_config.NumberColumn(format="%.2f €"),
                            "%": st.column_config.NumberColumn(format="%.1f%%"),
                            "Promedio/Mes": st.column_config.NumberColumn(format="%.2f €")
                        },
                        hide_index=True,
                        use_container_width=True
                    )
            else:
                st.info(f"No hay datos para el año {año}")

    # ========== TAB 3: HISTÓRICO ==========
    with tab_historico:
        st.markdown("### 📉 Evolución Últimos 12 Meses")

        df_evol = metrics.calcular_evolucion_mensual()
        fig = visualizer.grafico_evolucion_mensual(df_evol)

        if fig:
            st.plotly_chart(fig, use_container_width=True, key="plot_historico_mensual")

            # Estadísticas del histórico
            if not df_evol.empty:
                with st.expander("📊 Estadísticas del Período"):
                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric("💰 Total Ingresos", f"{df_evol['ingresos'].sum():.2f} €")
                    col2.metric("💸 Total Gastos", f"{abs(df_evol['gastos'].sum()):.2f} €")
                    col3.metric("⚖️ Balance Total", f"{df_evol['balance'].sum():.2f} €")
                    col4.metric("📈 Promedio Balance/Mes", f"{df_evol['balance'].mean():.2f} €")
        else:
            st.info("No hay suficientes datos históricos")

def mostrar_añadir_gasto():
    """Página para añadir gastos individuales manualmente"""
    st.title("➕ Añadir Nuevo Gasto")
    st.markdown("Registra gastos individuales que no están en tu extracto bancario o que quieres anotar inmediatamente.")

    # Formulario de añadir gasto
    with st.form("form_nuevo_gasto", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            fecha_gasto = st.date_input(
                "📅 Fecha",
                value=datetime.date.today(),
                help="Fecha del gasto"
            )

            concepto = st.text_input(
                "📝 Concepto",
                placeholder="Ej: Café con amigos, Uber, etc.",
                help="Descripción del gasto"
            )

        with col2:
            importe = st.number_input(
                "💶 Importe (€)",
                min_value=0.01,
                value=10.00,
                step=0.01,
                format="%.2f",
                help="Cantidad gastada (siempre positiva, se guardará como negativa)"
            )

            categoria = st.selectbox(
                "🏷️ Categoría",
                ["DISFRUTE", "FIJOS", "EXTRAORDINARIOS"],
                help="Tipo de gasto"
            )

        notas = st.text_area(
            "📋 Notas (opcional)",
            placeholder="Añade cualquier información adicional...",
            height=80
        )

        # Botones
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        with col_btn1:
            submit = st.form_submit_button("💾 Guardar Gasto", use_container_width=True, type="primary")
        with col_btn2:
            clear = st.form_submit_button("🗑️ Limpiar", use_container_width=True)

        if submit:
            # Validaciones
            if not concepto or concepto.strip() == "":
                st.error("❌ El concepto no puede estar vacío")
            elif importe <= 0:
                st.error("❌ El importe debe ser mayor que 0")
            else:
                # Insertar en base de datos
                try:
                    # Convertir importe a negativo (es un gasto)
                    importe_negativo = -abs(importe)

                    # Generar ID único
                    id_transaccion = db_manager.generar_uuid()

                    # Insertar transacción
                    db_manager.insertar_transaccion(
                        id=id_transaccion,
                        fecha=fecha_gasto,
                        concepto=concepto.strip(),
                        importe=importe_negativo,
                        categoria=categoria,
                        tipo='GASTO',
                        mes=fecha_gasto.month,
                        año=fecha_gasto.year,
                        notas=notas.strip() if notas else None,
                        saldo_posterior=None  # Se calculará al importar Excel
                    )

                    st.success(f"✅ Gasto guardado: {concepto} - {abs(importe_negativo):.2f}€")
                    st.balloons()

                    # Mostrar resumen
                    with st.expander("📊 Ver resumen del gasto", expanded=True):
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Fecha", fecha_gasto.strftime("%d/%m/%Y"))
                        col2.metric("Importe", f"{abs(importe_negativo):.2f} €")
                        col3.metric("Categoría", categoria)

                except Exception as e:
                    st.error(f"❌ Error al guardar: {str(e)}")

    # Separador
    st.markdown("---")

    # Últimos gastos añadidos manualmente
    st.subheader("📝 Últimos gastos registrados")

    try:
        # Obtener últimos 10 gastos
        conn = db_manager.get_db_connection()
        query = """
        SELECT fecha, concepto, importe, categoria
        FROM transacciones
        WHERE tipo = 'GASTO'
        ORDER BY fecha DESC, id DESC
        LIMIT 10
        """
        df_ultimos = pd.read_sql_query(query, conn)
        conn.close()

        if not df_ultimos.empty:
            df_ultimos['importe'] = df_ultimos['importe'].abs()
            df_ultimos.columns = ['Fecha', 'Concepto', 'Importe (€)', 'Categoría']

            st.dataframe(
                df_ultimos,
                column_config={
                    "Fecha": st.column_config.DateColumn(format="DD/MM/YYYY"),
                    "Importe (€)": st.column_config.NumberColumn(format="%.2f €"),
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("Aún no has registrado ningún gasto")

    except Exception as e:
        st.error(f"Error al cargar últimos gastos: {e}")

    # Información sobre duplicados
    with st.expander("ℹ️ ¿Qué pasa cuando importo mi extracto bancario?"):
        st.markdown("""
        **Detección automática de duplicados:**

        Cuando importes tu extracto bancario del mes:
        1. El sistema buscará transacciones duplicadas (misma fecha + importe + concepto)
        2. Si encuentra un duplicado con un gasto que añadiste manualmente:
           - **Prioriza los datos del banco** (son más fiables)
           - Actualiza la transacción con los datos bancarios
           - Mantiene tu categoría si ya la habías clasificado

        **Recomendación:**
        - Usa esta página para gastos que quieres registrar inmediatamente
        - Al final del mes, importa tu extracto bancario normalmente
        - El sistema se encargará de evitar duplicados automáticamente
        """)

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

def mostrar_sincronizacion():
    st.title("🔄 Sincronización")
    st.markdown("Sincroniza tu base de datos entre diferentes dispositivos (Mac ↔ Cloud)")

    st.markdown("---")

    # Tabs para exportar e importar
    tab_export, tab_import, tab_comparar = st.tabs(["📤 Exportar", "📥 Importar", "🔍 Comparar"])

    with tab_export:
        st.subheader("Exportar Base de Datos")
        st.info("Descarga tu base de datos completa en formato JSON para importarla en otro dispositivo.")

        # Mostrar estadísticas
        transacciones = db_manager.obtener_transacciones()
        col1, col2 = st.columns(2)
        col1.metric("Total de Transacciones", len(transacciones))

        if transacciones:
            importes_totales = sum(t['importe'] for t in transacciones)
            col2.metric("Balance Total", f"{importes_totales:.2f} €")

        st.markdown("---")

        if st.button("📥 Generar Archivo de Exportación", type="primary"):
            with st.spinner("Generando archivo..."):
                json_export = sync.generar_json_exportacion()

                # Ofrecer descarga
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"finanzas_export_{timestamp}.json"

                st.download_button(
                    label="⬇️ Descargar Archivo JSON",
                    data=json_export,
                    file_name=filename,
                    mime="application/json"
                )

                st.success(f"✅ Archivo generado: {len(transacciones)} transacciones")

    with tab_import:
        st.subheader("Importar Base de Datos")
        st.info("Sube un archivo JSON exportado desde otro dispositivo para sincronizar datos.")

        uploaded_file = st.file_uploader(
            "Selecciona archivo JSON de exportación",
            type=['json'],
            key="sync_upload"
        )

        if uploaded_file is not None:
            try:
                # Leer y parsear el JSON
                json_string = uploaded_file.read().decode('utf-8')
                data_importar = sync.parsear_json_importacion(json_string)

                # Mostrar preview
                st.success("✅ Archivo válido cargado")

                metadata = data_importar.get("metadata", {})
                transacciones_importar = data_importar.get("transacciones", [])

                st.write(f"**Exportado en:** {metadata.get('exported_at', 'N/A')}")
                st.write(f"**Total transacciones:** {len(transacciones_importar)}")

                # Comparar con DB actual
                comparacion = sync.comparar_bases_datos(data_importar)

                st.markdown("### 📊 Análisis de Diferencias")

                col1, col2, col3 = st.columns(3)
                col1.metric("En este dispositivo", comparacion['total_local'])
                col2.metric("En el archivo", comparacion['total_remota'])
                col3.metric("En ambos", comparacion['en_ambas'])

                st.markdown("---")

                # Mostrar transacciones nuevas
                if comparacion['solo_en_remota']['count'] > 0:
                    st.success(f"✨ **{comparacion['solo_en_remota']['count']} transacciones nuevas** encontradas en el archivo")

                    with st.expander("Ver transacciones nuevas"):
                        df_nuevas = pd.DataFrame(comparacion['solo_en_remota']['transacciones'])
                        st.dataframe(df_nuevas[['fecha', 'concepto', 'importe', 'categoria']], use_container_width=True)
                else:
                    st.info("No hay transacciones nuevas en el archivo")

                if comparacion['solo_en_local']['count'] > 0:
                    st.warning(f"⚠️ **{comparacion['solo_en_local']['count']} transacciones** existen aquí pero no en el archivo")

                st.markdown("---")

                # Modo de importación
                modo_import = st.radio(
                    "Modo de importación:",
                    ["Fusionar (Añadir solo nuevas)", "Sobrescribir (Reemplazar todo)"],
                    help="Fusionar: Añade solo transacciones nuevas. Sobrescribir: Elimina todo y reemplaza (NO DISPONIBLE por seguridad)"
                )

                modo = "fusionar" if "Fusionar" in modo_import else "sobrescribir"

                if modo == "sobrescribir":
                    st.error("⚠️ Modo sobrescribir desactivado por seguridad. Usa 'Fusionar'.")
                else:
                    if st.button("🔄 Importar y Fusionar", type="primary", disabled=(comparacion['solo_en_remota']['count'] == 0)):
                        with st.spinner("Importando transacciones..."):
                            stats = sync.importar_base_datos(data_importar, modo=modo)

                        st.success("✅ Importación completada")

                        # Estadísticas de transacciones
                        st.markdown("### 📋 Transacciones")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Nuevas", stats['nuevas'], delta=f"+{stats['nuevas']}")
                        col2.metric("Duplicadas (omitidas)", stats['duplicadas'])
                        col3.metric("Errores", stats['errores'], delta_color="inverse")

                        # Estadísticas de recargas (si las hay)
                        if 'total_recargas' in stats and stats['total_recargas'] > 0:
                            st.markdown("### 🔌 Recargas de Coche")
                            col4, col5, col6 = st.columns(3)
                            col4.metric("Nuevas recargas", stats.get('nuevas_recargas', 0), delta=f"+{stats.get('nuevas_recargas', 0)}")
                            col5.metric("Duplicadas", stats.get('duplicadas_recargas', 0))
                            col6.metric("Errores", stats.get('errores_recargas', 0), delta_color="inverse")

                        if stats['nuevas'] > 0 or stats.get('nuevas_recargas', 0) > 0:
                            st.balloons()

                        st.info("💡 Refresca la página para ver los datos actualizados")

            except Exception as e:
                st.error(f"❌ Error al procesar el archivo: {e}")

    with tab_comparar:
        st.subheader("Comparar con Archivo")
        st.info("Compara tu base de datos actual con un archivo exportado sin importar nada.")

        uploaded_file_compare = st.file_uploader(
            "Selecciona archivo JSON para comparar",
            type=['json'],
            key="sync_compare"
        )

        if uploaded_file_compare is not None:
            try:
                json_string = uploaded_file_compare.read().decode('utf-8')
                data_comparar = sync.parsear_json_importacion(json_string)

                comparacion = sync.comparar_bases_datos(data_comparar)

                st.markdown("### 📊 Resultados de la Comparación")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Total en este dispositivo", comparacion['total_local'])
                    st.metric("Solo en este dispositivo", comparacion['solo_en_local']['count'])

                    if comparacion['solo_en_local']['count'] > 0:
                        with st.expander(f"Ver {comparacion['solo_en_local']['count']} transacciones"):
                            df = pd.DataFrame(comparacion['solo_en_local']['transacciones'])
                            st.dataframe(df[['fecha', 'concepto', 'importe']], use_container_width=True)

                with col2:
                    st.metric("Total en el archivo", comparacion['total_remota'])
                    st.metric("Solo en el archivo", comparacion['solo_en_remota']['count'])

                    if comparacion['solo_en_remota']['count'] > 0:
                        with st.expander(f"Ver {comparacion['solo_en_remota']['count']} transacciones"):
                            df = pd.DataFrame(comparacion['solo_en_remota']['transacciones'])
                            st.dataframe(df[['fecha', 'concepto', 'importe']], use_container_width=True)

                st.metric("En ambos (sincronizadas)", comparacion['en_ambas'])

                # Recomendación
                if comparacion['solo_en_remota']['count'] > 0 and comparacion['solo_en_local']['count'] > 0:
                    st.warning("⚠️ Ambos dispositivos tienen transacciones únicas. Considera importar en ambas direcciones.")
                elif comparacion['solo_en_remota']['count'] > 0:
                    st.info("💡 El archivo tiene transacciones nuevas. Ve a la pestaña 'Importar' para sincronizar.")
                elif comparacion['solo_en_local']['count'] > 0:
                    st.info("💡 Este dispositivo tiene transacciones nuevas. Ve a 'Exportar' para compartirlas.")
                else:
                    st.success("✅ Ambas bases de datos están completamente sincronizadas")

            except Exception as e:
                st.error(f"❌ Error al comparar: {e}")

def mostrar_configuracion():
    st.title("⚙️ Configuración")

    # ========== SECCIÓN: SALDO INICIAL ==========
    st.subheader("💰 Saldo Inicial")
    st.info("El saldo inicial se suma a todas las transacciones para calcular el líquido disponible total. "
            "Úsalo para establecer el saldo de tu cuenta al comenzar a usar la app.")

    config_actual = config_manager.obtener_config()

    with st.form("form_saldo_inicial"):
        col1, col2 = st.columns(2)

        with col1:
            saldo_inicial = st.number_input(
                "Saldo inicial (€)",
                value=config_actual.get('saldo_inicial', 0.0),
                step=0.01,
                format="%.2f",
                help="Saldo de tu cuenta al comenzar a usar la aplicación"
            )

            fecha_inicial = st.date_input(
                "Fecha del saldo inicial",
                value=datetime.datetime.strptime(config_actual.get('fecha_saldo_inicial', '2025-01-01'), '%Y-%m-%d').date()
                      if config_actual.get('fecha_saldo_inicial') else datetime.date.today(),
                help="Fecha a la que corresponde este saldo"
            )

        with col2:
            notas_inicial = st.text_area(
                "Notas (opcional)",
                value=config_actual.get('notas', ''),
                height=100,
                help="Información adicional sobre este saldo inicial"
            )

            st.metric(
                "💧 Líquido Disponible Actual",
                f"{metrics.calcular_liquido_disponible():.2f} €",
                help="Saldo inicial + suma de todas las transacciones"
            )

        submitted = st.form_submit_button("💾 Guardar Saldo Inicial", type="primary", use_container_width=True)

        if submitted:
            if config_manager.actualizar_saldo_inicial(saldo_inicial, fecha_inicial, notas_inicial):
                st.success(f"✅ Saldo inicial actualizado: {saldo_inicial:.2f} €")
                st.rerun()
            else:
                st.error("❌ Error al guardar el saldo inicial")

    st.markdown("---")

    # ========== SECCIÓN: BASE DE DATOS ==========
    st.subheader("🗄️ Gestión de Base de Datos")

    col_info, col_reset = st.columns([2, 1])

    with col_info:
        st.warning(
            "⚠️ **Resetear la base de datos eliminará todas las transacciones**, "
            "pero el saldo inicial se mantendrá guardado y podrás restaurarlo después.",
            icon="⚠️"
        )

    with col_reset:
        if st.button("⚠️ Resetear Base de Datos", type="secondary", use_container_width=True):
            confirmacion = st.warning(
                "¿Estás seguro de que quieres resetear la base de datos? ¡Esta acción borrará todos los datos!",
                icon="⚠️"
            )
            if confirmacion:
                with st.spinner("Reseteando la base de datos..."):
                    db_manager.resetear_base_de_datos()
                st.success("¡Base de datos reseteada con éxito!")
                st.info(f"💡 Tu saldo inicial de {config_actual.get('saldo_inicial', 0):.2f} € se mantiene guardado en la configuración.")
                st.rerun()

# --- Importar módulo de Coche Eléctrico ---
import pages_coche_electrico

# --- Routing principal ---
if pagina_seleccionada == "Dashboard":
    mostrar_dashboard()
elif pagina_seleccionada == "Añadir Gasto":
    mostrar_añadir_gasto()
elif pagina_seleccionada == "Transacciones":
    mostrar_transacciones()
elif pagina_seleccionada == "Importar":
    mostrar_importar()
elif pagina_seleccionada == "Categorías":
    mostrar_categorias()
elif pagina_seleccionada == "🔌 Coche Eléctrico":
    pages_coche_electrico.mostrar_coche_electrico()
elif pagina_seleccionada == "Sincronización":
    mostrar_sincronizacion()
elif pagina_seleccionada == "Configuración":
    mostrar_configuracion()