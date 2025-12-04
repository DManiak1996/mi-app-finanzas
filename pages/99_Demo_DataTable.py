# pages/99_Demo_DataTable.py
"""
Página de demostración del componente DataTable

Esta página muestra ejemplos prácticos del uso del componente DataTable
integrado con la base de datos real de la aplicación.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import db_manager
from utils.components import (
    render_data_table,
    render_transaction_table,
    render_summary_table,
    render_compact_table,
    show_table_stats,
)
from utils.design_tokens import Colors, Typography, Spacing, spacer_html
from utils.styles import inject_global_styles
import auth_simple as auth

# === CONFIGURACIÓN DE PÁGINA ===
st.set_page_config(
    page_title="Demo DataTable",
    page_icon="📊",
    layout="wide"
)

# === AUTENTICACIÓN ===
if not auth.check_authentication():
    st.stop()

# === ESTILOS GLOBALES ===
inject_global_styles()

# === TÍTULO ===
st.title("📊 Demo: Componente DataTable")
st.markdown("""
Esta página demuestra el uso del componente DataTable con datos reales de tu base de datos.
""")

st.divider()

# === TABS ===
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Tabla Básica",
    "💰 Transacciones",
    "📈 Resumen",
    "📦 Compacta",
    "📚 Documentación"
])

# ========== TAB 1: TABLA BÁSICA ==========
with tab1:
    st.header("Tabla Básica con Todas las Funcionalidades")

    st.markdown("""
    Ejemplo de tabla básica con:
    - Búsqueda global
    - Paginación
    - Formateo automático de moneda, fechas
    - Exportación CSV/Excel
    """)

    # Obtener transacciones del mes actual
    mes_actual = datetime.now().month
    año_actual = datetime.now().year

    df_transacciones = db_manager.obtener_transacciones(mes_actual, año_actual)

    if df_transacciones is not None and not df_transacciones.empty:
        st.markdown(spacer_html("MD"), unsafe_allow_html=True)

        # Mostrar estadísticas
        show_table_stats(df_transacciones, f"Transacciones {mes_actual}/{año_actual}")

        st.markdown(spacer_html("MD"), unsafe_allow_html=True)

        # Renderizar tabla básica
        render_data_table(
            df_transacciones,
            title=f"Transacciones - {mes_actual}/{año_actual}",
            searchable=True,
            pagination=True,
            page_size=15,
            exportable=True,
            export_filename=f"transacciones_{mes_actual}_{año_actual}",
            currency_columns=['importe', 'saldo_posterior'],
            date_columns=['fecha'],
            key="demo_basic_table"
        )

        st.markdown(spacer_html("LG"), unsafe_allow_html=True)

        with st.expander("📝 Ver código de este ejemplo"):
            st.code("""
from utils.components import render_data_table

df_transacciones = db_manager.obtener_transacciones(mes_actual, año_actual)

render_data_table(
    df_transacciones,
    title=f"Transacciones - {mes_actual}/{año_actual}",
    searchable=True,
    pagination=True,
    page_size=15,
    exportable=True,
    currency_columns=['importe', 'saldo_posterior'],
    date_columns=['fecha'],
)
            """, language="python")
    else:
        st.info("No hay transacciones para este mes. Añade algunas en la página principal.")

# ========== TAB 2: TABLA DE TRANSACCIONES ==========
with tab2:
    st.header("Tabla Especializada para Transacciones")

    st.markdown("""
    Tabla con formateo específico para transacciones financieras:
    - Colores por tipo (ingreso/gasto)
    - Acciones por fila (editar, eliminar, ver)
    - Formateo automático de moneda y fechas
    """)

    df_transacciones = db_manager.obtener_transacciones()

    if df_transacciones is not None and not df_transacciones.empty:
        st.markdown(spacer_html("MD"), unsafe_allow_html=True)

        # Callbacks de ejemplo
        def on_edit(row):
            st.toast(f"✏️ Editar: {row.get('concepto', 'N/A')}", icon="✏️")

        def on_delete(row):
            st.toast(f"🗑️ Eliminar: {row.get('concepto', 'N/A')}", icon="🗑️")

        def on_view(row):
            st.toast(f"👁️ Ver detalles: {row.get('concepto', 'N/A')}", icon="👁️")

        # Renderizar tabla de transacciones
        render_transaction_table(
            df_transacciones.head(50),  # Limitar a 50 para demo
            title="Transacciones Recientes",
            on_edit=on_edit,
            on_delete=on_delete,
            on_view=on_view,
            searchable=True,
            pagination=True,
            page_size=10,
            key="demo_transaction_table"
        )

        st.markdown(spacer_html("MD"), unsafe_allow_html=True)

        st.info("""
        **Nota**: Los botones de acción son solo demostrativos. En producción, estos callbacks
        ejecutarían la lógica real de edición/eliminación de transacciones.
        """)

        with st.expander("📝 Ver código de este ejemplo"):
            st.code("""
from utils.components import render_transaction_table

def on_edit(row):
    # Lógica de edición
    st.session_state['editing_id'] = row['id']
    st.rerun()

def on_delete(row):
    # Lógica de eliminación
    db_manager.eliminar_transaccion(row['id'])
    st.success("Transacción eliminada")
    st.rerun()

render_transaction_table(
    df_transacciones,
    title="Transacciones Recientes",
    on_edit=on_edit,
    on_delete=on_delete,
    searchable=True,
    pagination=True,
)
            """, language="python")
    else:
        st.info("No hay transacciones para mostrar.")

# ========== TAB 3: TABLA DE RESUMEN ==========
with tab3:
    st.header("Tabla de Resumen/Totales")

    st.markdown("""
    Tabla especializada para mostrar resúmenes y totales:
    - Sin búsqueda ni paginación
    - Resalta totales automáticamente
    - Formato compacto
    """)

    # Obtener datos del año actual
    df_año = db_manager.obtener_transacciones(año=año_actual)

    if df_año is not None and not df_año.empty:
        st.markdown(spacer_html("MD"), unsafe_allow_html=True)

        # Calcular resumen por mes
        df_año['mes'] = pd.to_datetime(df_año['fecha']).dt.month
        df_año['importe_num'] = pd.to_numeric(df_año['importe'], errors='coerce')

        resumen_mensual = []
        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

        for mes in range(1, 13):
            df_mes = df_año[df_año['mes'] == mes]
            if not df_mes.empty:
                ingresos = df_mes[df_mes['tipo'] == 'Ingreso']['importe_num'].sum()
                gastos = abs(df_mes[df_mes['tipo'] == 'Gasto']['importe_num'].sum())
                balance = ingresos - gastos

                resumen_mensual.append({
                    'Mes': meses[mes - 1],
                    'Ingresos': ingresos,
                    'Gastos': gastos,
                    'Balance': balance
                })

        if resumen_mensual:
            df_resumen = pd.DataFrame(resumen_mensual)

            # Añadir fila de totales
            totales = {
                'Mes': 'TOTAL',
                'Ingresos': df_resumen['Ingresos'].sum(),
                'Gastos': df_resumen['Gastos'].sum(),
                'Balance': df_resumen['Balance'].sum()
            }
            df_resumen = pd.concat([df_resumen, pd.DataFrame([totales])], ignore_index=True)

            # Formatear como moneda
            from utils.components import format_currency_column
            df_resumen_fmt = df_resumen.copy()
            df_resumen_fmt = format_currency_column(df_resumen_fmt, 'Ingresos')
            df_resumen_fmt = format_currency_column(df_resumen_fmt, 'Gastos')
            df_resumen_fmt = format_currency_column(df_resumen_fmt, 'Balance')

            render_summary_table(
                df_resumen_fmt,
                title=f"Resumen Financiero {año_actual}",
                highlight_totals=True,
                key="demo_summary_table"
            )

            st.markdown(spacer_html("MD"), unsafe_allow_html=True)

            with st.expander("📝 Ver código de este ejemplo"):
                st.code("""
from utils.components import render_summary_table, format_currency_column

# Preparar resumen
df_resumen = pd.DataFrame({
    'Mes': ['Ene', 'Feb', 'Mar', 'Total'],
    'Ingresos': [3000, 3200, 2800, 9000],
    'Gastos': [2400, 2600, 2200, 7200],
    'Balance': [600, 600, 600, 1800],
})

# Formatear columnas
df_resumen = format_currency_column(df_resumen, 'Ingresos')
df_resumen = format_currency_column(df_resumen, 'Gastos')
df_resumen = format_currency_column(df_resumen, 'Balance')

render_summary_table(
    df_resumen,
    title="Resumen Financiero",
    highlight_totals=True,
)
                """, language="python")
        else:
            st.warning("No hay datos suficientes para crear el resumen.")
    else:
        st.info("No hay transacciones para este año.")

# ========== TAB 4: TABLA COMPACTA ==========
with tab4:
    st.header("Tablas Compactas")

    st.markdown("""
    Tablas compactas para widgets pequeños o layouts de dos columnas:
    - Sin decoraciones
    - Altura fija con scroll
    - Máxima simplicidad
    """)

    df_transacciones = db_manager.obtener_transacciones()

    if df_transacciones is not None and not df_transacciones.empty:
        st.markdown(spacer_html("MD"), unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📌 Últimas 10 Transacciones")
            render_compact_table(
                df_transacciones[['fecha', 'concepto', 'importe']].head(10),
                height=300,
                key="demo_compact_1"
            )

        with col2:
            st.subheader("📊 Por Categoría")
            if 'categoria' in df_transacciones.columns:
                df_categorias = df_transacciones.groupby('categoria')['importe'].sum().reset_index()
                df_categorias.columns = ['Categoría', 'Total']
                df_categorias = df_categorias.sort_values('Total', ascending=False).head(10)

                render_compact_table(
                    df_categorias,
                    height=300,
                    key="demo_compact_2"
                )
            else:
                st.info("No hay datos de categorías")

        st.markdown(spacer_html("MD"), unsafe_allow_html=True)

        with st.expander("📝 Ver código de este ejemplo"):
            st.code("""
from utils.components import render_compact_table

col1, col2 = st.columns(2)

with col1:
    st.subheader("Últimas Transacciones")
    render_compact_table(df.head(10), height=300)

with col2:
    st.subheader("Por Categoría")
    render_compact_table(df_categorias, height=300)
            """, language="python")
    else:
        st.info("No hay transacciones para mostrar.")

# ========== TAB 5: DOCUMENTACIÓN ==========
with tab5:
    st.header("📚 Documentación del Componente")

    st.markdown("""
    ### Instalación

    ```python
    from utils.components import render_data_table, render_transaction_table
    ```

    ### Características Principales

    - **Formateo Inteligente**: Moneda (€), fechas (DD/MM/YYYY), porcentajes (%), números con separadores
    - **Búsqueda Global**: Busca en todas las columnas
    - **Paginación**: Control de filas por página
    - **Ordenamiento**: Click en headers para ordenar
    - **Exportación**: CSV y Excel
    - **Acciones por Fila**: Editar, eliminar, ver detalles
    - **Performance**: Optimizado para tablas grandes
    - **Responsive**: Scroll horizontal en móvil

    ### Variantes Disponibles

    1. **`render_data_table()`** - Tabla básica con todas las funcionalidades
    2. **`render_transaction_table()`** - Especializada para transacciones
    3. **`render_summary_table()`** - Para resúmenes y totales
    4. **`render_compact_table()`** - Versión compacta sin decoraciones

    ### Funciones de Formateo

    - `format_currency_column(df, column)` - Formatea como moneda
    - `format_date_column(df, column)` - Formatea fechas
    - `format_percentage_column(df, column)` - Formatea porcentajes
    - `format_number_column(df, column)` - Formatea números
    - `auto_format_dataframe(df, ...)` - Formatea múltiples columnas

    ### Helpers

    - `export_table(df, filename, format)` - Exporta a CSV/Excel
    - `show_table_stats(df, label)` - Muestra estadísticas
    - `add_row_actions(...)` - Añade botones de acción

    ### Documentación Completa

    Para más detalles, consulta:
    - **README**: `utils/components/README_DATA_TABLE.md`
    - **Ejemplos**: `utils/components/data_table_examples.py`
    - **Tests**: `utils/components/data_table_test.py`
    """)

    st.divider()

    st.subheader("🔗 Enlaces Útiles")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Documentación**
        - [README Completo](utils/components/README_DATA_TABLE.md)
        - [Design Tokens](utils/design_tokens.py)
        - [Estrategia de Diseño](docs/ESTRATEGIA_OVERHAUL_DISEÑO.md)
        """)

    with col2:
        st.markdown("""
        **Código Fuente**
        - [data_table.py](utils/components/data_table.py)
        - [data_table_examples.py](utils/components/data_table_examples.py)
        - [data_table_test.py](utils/components/data_table_test.py)
        """)

    with col3:
        st.markdown("""
        **Recursos**
        - [Streamlit Docs](https://docs.streamlit.io/library/api-reference/data/st.dataframe)
        - [Pandas Docs](https://pandas.pydata.org/docs/)
        - [Plotly Theme](utils/plotly_theme.py)
        """)

# === FOOTER ===
st.divider()
st.caption("Demo del componente DataTable | Implementado el 2024-12-04")
