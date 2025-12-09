#!/usr/bin/env python3
"""
Script para corregir las transacciones del coche eléctrico que fueron pagadas
en diciembre pero se asignaron incorrectamente a octubre y noviembre.
"""

import sqlite3
import sys
import os

# Añadir el directorio padre al path para poder importar
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import get_db_connection

def corregir_transacciones_coche():
    """
    Actualiza las transacciones del coche eléctrico que tienen fecha de diciembre
    pero están asignadas a meses anteriores (octubre y noviembre).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # IDs de las transacciones a actualizar (obtenidos del análisis)
    transacciones_a_corregir = [
        ('49d6a520-9c65-44bf-b542-c8e7ab77e6c6', 10),  # Octubre -> Diciembre
        ('4a73ddfa-d11f-46c0-94e5-0ff0ad8ce3f1', 11)   # Noviembre -> Diciembre
    ]

    print("🔧 Corrigiendo transacciones del coche eléctrico...")
    print("=" * 70)

    for transaccion_id, mes_actual in transacciones_a_corregir:
        # Obtener información actual de la transacción
        cursor.execute("""
            SELECT fecha, concepto, importe, mes, año
            FROM transacciones
            WHERE id = ?
        """, (transaccion_id,))

        transaccion = cursor.fetchone()

        if transaccion:
            print(f"\n📝 Transacción ID: {transaccion_id}")
            print(f"   Concepto: {transaccion[1]}")
            print(f"   Importe: {transaccion[2]}€")
            print(f"   Fecha: {transaccion[0]}")
            print(f"   Mes actual: {transaccion[3]}/{transaccion[4]}")
            print(f"   ➡️  Cambiando mes a: 12/{transaccion[4]}")

            # Actualizar el mes a diciembre (12)
            cursor.execute("""
                UPDATE transacciones
                SET mes = 12, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (transaccion_id,))

            print("   ✅ Actualizado correctamente")
        else:
            print(f"❌ No se encontró la transacción {transaccion_id}")

    # Commit de los cambios
    conn.commit()

    # Verificar los cambios
    print("\n" + "=" * 70)
    print("🔍 Verificando cambios...")
    print("=" * 70)

    cursor.execute("""
        SELECT id, fecha, concepto, importe, mes, año
        FROM transacciones
        WHERE categoria = 'FIJOS'
        AND concepto LIKE '%Recarga coche%'
        AND fecha LIKE '2025-12-%'
        ORDER BY fecha DESC
    """)

    transacciones_diciembre = cursor.fetchall()

    if transacciones_diciembre:
        print(f"\n✅ Transacciones de recarga coche con fecha diciembre 2025:")
        total = 0
        for t in transacciones_diciembre:
            print(f"   - {t[1]}: {t[2]} = {t[3]}€ (Mes: {t[4]}/{t[5]})")
            total += t[3]
        print(f"\n💰 Total gastos coche eléctrico en diciembre: {total:.2f}€")
    else:
        print("\n⚠️  No se encontraron transacciones de recarga coche en diciembre")

    conn.close()
    print("\n✅ Proceso completado")

if __name__ == "__main__":
    try:
        corregir_transacciones_coche()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
