# utils/components/data_table_test.py
"""
Tests básicos para el componente DataTable

Estos tests verifican que las funciones de formateo y utilidades
funcionan correctamente sin necesidad de Streamlit.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Añadir el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.components.data_table import (
    format_currency_column,
    format_date_column,
    format_percentage_column,
    format_number_column,
    auto_format_dataframe,
    export_table,
)


def test_format_currency_column():
    """Test formateo de columna de moneda"""
    print("Test: format_currency_column")

    df = pd.DataFrame({
        'importe': [1234.56, 999.99, 0.50, 10000],
        'nombre': ['A', 'B', 'C', 'D']
    })

    df_formatted = format_currency_column(df, 'importe')

    print("Original:", df['importe'].tolist())
    print("Formateado:", df_formatted['importe'].tolist())

    # Verificar que se formateó correctamente
    assert '1.234,56 €' in df_formatted['importe'].iloc[0]
    assert '999,99 €' in df_formatted['importe'].iloc[1]

    print("✓ Test pasado\n")


def test_format_date_column():
    """Test formateo de columna de fecha"""
    print("Test: format_date_column")

    df = pd.DataFrame({
        'fecha': pd.date_range(start='2024-01-15', periods=3, freq='D'),
        'nombre': ['A', 'B', 'C']
    })

    df_formatted = format_date_column(df, 'fecha')

    print("Original:", df['fecha'].tolist())
    print("Formateado:", df_formatted['fecha'].tolist())

    # Verificar formato DD/MM/YYYY
    assert df_formatted['fecha'].iloc[0] == '15/01/2024'
    assert df_formatted['fecha'].iloc[1] == '16/01/2024'

    print("✓ Test pasado\n")


def test_format_percentage_column():
    """Test formateo de columna de porcentaje"""
    print("Test: format_percentage_column")

    df = pd.DataFrame({
        'porcentaje': [0.1234, 0.5, 0.999, 1.0],
        'nombre': ['A', 'B', 'C', 'D']
    })

    df_formatted = format_percentage_column(df, 'porcentaje', decimals=1)

    print("Original:", df['porcentaje'].tolist())
    print("Formateado:", df_formatted['porcentaje'].tolist())

    # Verificar formato con %
    assert '12.3%' in df_formatted['porcentaje'].iloc[0]
    assert '50.0%' in df_formatted['porcentaje'].iloc[1]
    assert '99.9%' in df_formatted['porcentaje'].iloc[2]

    print("✓ Test pasado\n")


def test_format_number_column():
    """Test formateo de columna numérica"""
    print("Test: format_number_column")

    df = pd.DataFrame({
        'cantidad': [1234.56, 999999.99, 0.5],
        'nombre': ['A', 'B', 'C']
    })

    df_formatted = format_number_column(df, 'cantidad', decimals=2)

    print("Original:", df['cantidad'].tolist())
    print("Formateado:", df_formatted['cantidad'].tolist())

    # Verificar formato con separadores
    assert '1.234,56' in df_formatted['cantidad'].iloc[0]
    assert '999.999,99' in df_formatted['cantidad'].iloc[1]

    print("✓ Test pasado\n")


def test_auto_format_dataframe():
    """Test formateo automático de múltiples columnas"""
    print("Test: auto_format_dataframe")

    df = pd.DataFrame({
        'fecha': pd.date_range(start='2024-01-01', periods=3, freq='D'),
        'concepto': ['A', 'B', 'C'],
        'importe': [1234.56, 999.99, 500.00],
        'porcentaje': [0.15, 0.25, 0.85],
        'cantidad': [100, 200, 300],
    })

    df_formatted = auto_format_dataframe(
        df,
        currency_columns=['importe'],
        date_columns=['fecha'],
        percentage_columns=['porcentaje'],
        number_columns=['cantidad']
    )

    print("DataFrame formateado:")
    print(df_formatted.head())

    # Verificar que todas las columnas se formatearon
    assert '€' in str(df_formatted['importe'].iloc[0])
    assert '%' in str(df_formatted['porcentaje'].iloc[0])
    assert '/' in str(df_formatted['fecha'].iloc[0])

    print("✓ Test pasado\n")


def test_export_table_csv():
    """Test exportación a CSV"""
    print("Test: export_table (CSV)")

    df = pd.DataFrame({
        'fecha': ['2024-01-01', '2024-01-02'],
        'concepto': ['A', 'B'],
        'importe': [100, 200],
    })

    csv_data = export_table(df, 'test', 'csv')

    print("Tamaño CSV:", len(csv_data), "bytes")
    print("Primeros 100 caracteres:", csv_data[:100])

    # Verificar que es bytes y contiene datos
    assert isinstance(csv_data, bytes)
    assert len(csv_data) > 0
    assert b'fecha' in csv_data
    assert b'concepto' in csv_data

    print("✓ Test pasado\n")


def test_export_table_excel():
    """Test exportación a Excel"""
    print("Test: export_table (Excel)")

    df = pd.DataFrame({
        'fecha': ['2024-01-01', '2024-01-02'],
        'concepto': ['A', 'B'],
        'importe': [100, 200],
    })

    excel_data = export_table(df, 'test', 'excel')

    print("Tamaño Excel:", len(excel_data), "bytes")

    # Verificar que es bytes y contiene datos
    assert isinstance(excel_data, bytes)
    assert len(excel_data) > 0
    # Los archivos Excel comienzan con PK (ZIP signature)
    assert excel_data[:2] == b'PK'

    print("✓ Test pasado\n")


def test_empty_dataframe():
    """Test con DataFrame vacío"""
    print("Test: DataFrame vacío")

    df = pd.DataFrame()

    df_formatted = format_currency_column(df, 'importe')

    assert df_formatted.empty

    print("✓ Test pasado\n")


def test_missing_column():
    """Test con columna inexistente"""
    print("Test: Columna inexistente")

    df = pd.DataFrame({
        'nombre': ['A', 'B', 'C']
    })

    # No debería fallar, solo retornar el df sin cambios
    df_formatted = format_currency_column(df, 'importe_inexistente')

    assert df_formatted.equals(df)

    print("✓ Test pasado\n")


def test_null_values():
    """Test con valores nulos"""
    print("Test: Valores nulos")

    df = pd.DataFrame({
        'importe': [1234.56, None, 999.99, np.nan],
        'nombre': ['A', 'B', 'C', 'D']
    })

    df_formatted = format_currency_column(df, 'importe')

    print("Original:", df['importe'].tolist())
    print("Formateado:", df_formatted['importe'].tolist())

    # Verificar que los nulos se mantienen
    assert pd.isna(df_formatted['importe'].iloc[1]) or df_formatted['importe'].iloc[1] is None

    print("✓ Test pasado\n")


def run_all_tests():
    """Ejecuta todos los tests"""
    print("=" * 60)
    print("EJECUTANDO TESTS DEL COMPONENTE DATA_TABLE")
    print("=" * 60)
    print()

    try:
        test_format_currency_column()
        test_format_date_column()
        test_format_percentage_column()
        test_format_number_column()
        test_auto_format_dataframe()
        test_export_table_csv()
        test_export_table_excel()
        test_empty_dataframe()
        test_missing_column()
        test_null_values()

        print("=" * 60)
        print("TODOS LOS TESTS PASARON CORRECTAMENTE")
        print("=" * 60)
        return True

    except AssertionError as e:
        print("\n" + "=" * 60)
        print("FALLÓ UN TEST")
        print("=" * 60)
        print(f"Error: {e}")
        return False

    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR INESPERADO")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
