# utils/components/data_table_examples.py
"""
Ejemplos de uso del componente DataTable

Este archivo contiene ejemplos prácticos de cómo usar el componente DataTable
en diferentes escenarios comunes de la aplicación.

NO ES PARTE DEL CÓDIGO DE PRODUCCIÓN - Solo documentación y ejemplos.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from .data_table import (
    render_data_table,
    render_transaction_table,
    render_summary_table,
    render_compact_table,
    format_currency_column,
    format_date_column,
    export_table,
    show_table_stats,
)


# ========== EJEMPLO 1: Tabla básica con formateo automático ==========

def example_basic_table():
    """Ejemplo de tabla básica con todas las funcionalidades"""
    st.header("Ejemplo 1: Tabla Básica")

    # Datos de ejemplo
    data = {
        'fecha': pd.date_range(start='2024-01-01', periods=50, freq='D'),
        'concepto': [f'Transacción {i}' for i in range(1, 51)],
        'importe': [round(100 + i * 10.5, 2) for i in range(50)],
        'categoria': ['Comida', 'Transporte', 'Ocio', 'Salud', 'Otros'] * 10,
        'porcentaje': [i / 100 for i in range(50)],
    }
    df = pd.DataFrame(data)

    # Renderizar tabla con todas las funciones
    render_data_table(
        df,
        title="Transacciones con Formateo Automático",
        searchable=True,
        pagination=True,
        page_size=10,
        exportable=True,
        export_filename="transacciones_ejemplo",
        currency_columns=['importe'],
        date_columns=['fecha'],
        percentage_columns=['porcentaje'],
        key="example_basic"
    )

    st.code("""
render_data_table(
    df,
    title="Transacciones con Formateo Automático",
    searchable=True,
    pagination=True,
    page_size=10,
    exportable=True,
    currency_columns=['importe'],
    date_columns=['fecha'],
    percentage_columns=['porcentaje'],
)
    """, language="python")


# ========== EJEMPLO 2: Tabla de transacciones con acciones ==========

def example_transaction_table():
    """Ejemplo de tabla especializada para transacciones"""
    st.header("Ejemplo 2: Tabla de Transacciones")

    # Datos de transacciones
    data = {
        'id': list(range(1, 21)),
        'fecha': pd.date_range(start='2024-01-01', periods=20, freq='D'),
        'concepto': [
            'Nómina', 'Supermercado', 'Gasolina', 'Netflix', 'Restaurante',
            'Luz', 'Internet', 'Gimnasio', 'Amazon', 'Farmacia'
        ] * 2,
        'importe': [
            2500, -85.50, -60, -15.99, -45.20,
            -80, -50, -40, -120, -25.50
        ] * 2,
        'categoria': [
            'Ingresos', 'Comida', 'Transporte', 'Ocio', 'Comida',
            'Hogar', 'Hogar', 'Salud', 'Compras', 'Salud'
        ] * 2,
        'tipo': [
            'Ingreso' if x > 0 else 'Gasto'
            for x in [2500, -85.50, -60, -15.99, -45.20, -80, -50, -40, -120, -25.50] * 2
        ],
        'notas': [''] * 20,
    }
    df = pd.DataFrame(data)

    # Callbacks de ejemplo
    def on_edit(row):
        st.info(f"Editar transacción: {row.get('concepto', 'N/A')}")

    def on_delete(row):
        st.warning(f"Eliminar transacción: {row.get('concepto', 'N/A')}")

    def on_view(row):
        st.success(f"Ver detalles de: {row.get('concepto', 'N/A')}")

    # Renderizar tabla de transacciones
    render_transaction_table(
        df,
        title="Transacciones del Mes",
        on_edit=on_edit,
        on_delete=on_delete,
        on_view=on_view,
        searchable=True,
        pagination=True,
        page_size=10,
        key="example_transactions"
    )

    st.code("""
render_transaction_table(
    df,
    title="Transacciones del Mes",
    on_edit=lambda row: edit_transaction(row['id']),
    on_delete=lambda row: delete_transaction(row['id']),
    on_view=lambda row: show_details(row),
    searchable=True,
    pagination=True,
)
    """, language="python")


# ========== EJEMPLO 3: Tabla de resumen ==========

def example_summary_table():
    """Ejemplo de tabla de resumen/totales"""
    st.header("Ejemplo 3: Tabla de Resumen")

    # Datos de resumen
    summary_data = {
        'Concepto': [
            'Total Ingresos',
            'Total Gastos',
            'Balance Final'
        ],
        'Enero': [3000, 2400, 600],
        'Febrero': [3200, 2600, 600],
        'Marzo': [2800, 2200, 600],
        'Total': [9000, 7200, 1800],
    }
    df = pd.DataFrame(summary_data)

    render_summary_table(
        df,
        title="Resumen Trimestral",
        highlight_totals=True,
        key="example_summary"
    )

    st.code("""
render_summary_table(
    df,
    title="Resumen Trimestral",
    highlight_totals=True,
)
    """, language="python")


# ========== EJEMPLO 4: Tabla compacta ==========

def example_compact_table():
    """Ejemplo de tabla compacta"""
    st.header("Ejemplo 4: Tabla Compacta")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Últimas Transacciones")
        data = {
            'Fecha': pd.date_range(start='2024-03-01', periods=5, freq='D'),
            'Concepto': ['Supermercado', 'Gasolina', 'Cine', 'Farmacia', 'Restaurante'],
            'Importe': [-85.50, -60, -25, -15.50, -45],
        }
        df1 = pd.DataFrame(data)
        render_compact_table(df1, height=200, key="compact1")

    with col2:
        st.subheader("Top Gastos")
        data = {
            'Categoría': ['Comida', 'Transporte', 'Ocio', 'Salud', 'Otros'],
            'Total': [450, 320, 180, 120, 90],
        }
        df2 = pd.DataFrame(data)
        render_compact_table(df2, height=200, key="compact2")

    st.code("""
col1, col2 = st.columns(2)

with col1:
    render_compact_table(recent_transactions_df, height=200)

with col2:
    render_compact_table(top_expenses_df, height=200)
    """, language="python")


# ========== EJEMPLO 5: Formateo manual de columnas ==========

def example_manual_formatting():
    """Ejemplo de formateo manual de columnas"""
    st.header("Ejemplo 5: Formateo Manual")

    # Datos sin formatear
    data = {
        'producto': ['Laptop', 'Mouse', 'Teclado', 'Monitor'],
        'precio': [1299.99, 45.50, 89.99, 450.00],
        'descuento': [0.15, 0.10, 0.20, 0.05],
        'stock': [25, 150, 80, 45],
    }
    df = pd.DataFrame(data)

    st.subheader("Antes del formateo")
    st.dataframe(df)

    # Aplicar formateo manual
    df_formatted = df.copy()
    df_formatted = format_currency_column(df_formatted, 'precio')
    # Para porcentaje, necesitamos usar la función directamente
    from .data_table import format_percentage_column
    df_formatted = format_percentage_column(df_formatted, 'descuento')

    st.subheader("Después del formateo")
    st.dataframe(df_formatted)

    st.code("""
from utils.components.data_table import format_currency_column, format_percentage_column

df_formatted = df.copy()
df_formatted = format_currency_column(df_formatted, 'precio')
df_formatted = format_percentage_column(df_formatted, 'descuento')
    """, language="python")


# ========== EJEMPLO 6: Exportación de datos ==========

def example_export():
    """Ejemplo de exportación de datos"""
    st.header("Ejemplo 6: Exportación")

    data = {
        'fecha': pd.date_range(start='2024-01-01', periods=10, freq='D'),
        'concepto': [f'Transacción {i}' for i in range(1, 11)],
        'importe': [round(100 + i * 10.5, 2) for i in range(10)],
    }
    df = pd.DataFrame(data)

    st.dataframe(df)

    col1, col2 = st.columns(2)

    with col1:
        csv_data = export_table(df, 'datos', 'csv')
        st.download_button(
            "Descargar CSV",
            data=csv_data,
            file_name="datos.csv",
            mime="text/csv",
        )

    with col2:
        excel_data = export_table(df, 'datos', 'excel')
        st.download_button(
            "Descargar Excel",
            data=excel_data,
            file_name="datos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    st.code("""
from utils.components.data_table import export_table

# Exportar a CSV
csv_data = export_table(df, 'datos', 'csv')
st.download_button("Descargar CSV", data=csv_data, file_name="datos.csv")

# Exportar a Excel
excel_data = export_table(df, 'datos', 'excel')
st.download_button("Descargar Excel", data=excel_data, file_name="datos.xlsx")
    """, language="python")


# ========== EJEMPLO 7: Estadísticas de tabla ==========

def example_table_stats():
    """Ejemplo de mostrar estadísticas de tabla"""
    st.header("Ejemplo 7: Estadísticas")

    # Generar datos grandes
    data = {
        'fecha': pd.date_range(start='2024-01-01', periods=1000, freq='H'),
        'sensor': [f'Sensor {i % 10}' for i in range(1000)],
        'temperatura': [20 + (i % 30) for i in range(1000)],
        'humedad': [50 + (i % 40) for i in range(1000)],
    }
    df = pd.DataFrame(data)

    show_table_stats(df, "Datos de Sensores")

    st.dataframe(df.head(20))

    st.code("""
from utils.components.data_table import show_table_stats

show_table_stats(df, "Datos de Sensores")
# Muestra: Filas, Columnas, Memoria, Valores Nulos
    """, language="python")


# ========== DEMO PRINCIPAL ==========

def run_demo():
    """Ejecuta todos los ejemplos"""
    st.title("DataTable Component - Ejemplos de Uso")

    st.markdown("""
    Este componente proporciona tablas consistentes y funcionales para toda la aplicación.

    ### Características principales:
    - Formateo inteligente (moneda, fechas, porcentajes, números)
    - Búsqueda global en todos los campos
    - Paginación opcional
    - Ordenamiento por columnas (nativo de Streamlit)
    - Exportación a CSV y Excel
    - Acciones por fila (editar, eliminar, ver)
    - Variantes especializadas (transacciones, resúmenes, compactas)
    - Performance optimizada con DataFrames grandes
    - Responsive (scroll horizontal en móvil)
    """)

    st.divider()

    # Selector de ejemplo
    ejemplo = st.selectbox(
        "Selecciona un ejemplo",
        [
            "1. Tabla Básica",
            "2. Tabla de Transacciones",
            "3. Tabla de Resumen",
            "4. Tabla Compacta",
            "5. Formateo Manual",
            "6. Exportación",
            "7. Estadísticas",
        ]
    )

    st.divider()

    # Ejecutar ejemplo seleccionado
    if ejemplo.startswith("1"):
        example_basic_table()
    elif ejemplo.startswith("2"):
        example_transaction_table()
    elif ejemplo.startswith("3"):
        example_summary_table()
    elif ejemplo.startswith("4"):
        example_compact_table()
    elif ejemplo.startswith("5"):
        example_manual_formatting()
    elif ejemplo.startswith("6"):
        example_export()
    elif ejemplo.startswith("7"):
        example_table_stats()


if __name__ == "__main__":
    # Para probar los ejemplos, crear una página de Streamlit:
    # streamlit run utils/components/data_table_examples.py
    run_demo()
