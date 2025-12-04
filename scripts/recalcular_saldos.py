#!/usr/bin/env python3
"""
Script para recalcular todos los saldos_posteriores de las transacciones existentes.
Útil después de corregir bugs o cuando hay transacciones sin saldo_posterior.
"""

import sys
import os

# Añadir el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import recalcular_todos_saldos_posteriores, get_db_connection

def mostrar_transacciones_sin_saldo():
    """Muestra las transacciones que actualmente no tienen saldo_posterior"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) as total
        FROM transacciones
        WHERE saldo_posterior IS NULL
    """)

    total_sin_saldo = cursor.fetchone()['total']

    if total_sin_saldo > 0:
        print(f"\n⚠️  Hay {total_sin_saldo} transacciones sin saldo_posterior")
        print("\nEjemplos:")

        cursor.execute("""
            SELECT fecha, concepto, importe, categoria
            FROM transacciones
            WHERE saldo_posterior IS NULL
            ORDER BY fecha DESC
            LIMIT 5
        """)

        for t in cursor.fetchall():
            print(f"  - {t['fecha']}: {t['concepto'][:40]:40} | {t['importe']:8.2f}€ | {t['categoria']}")
    else:
        print("\n✅ Todas las transacciones tienen saldo_posterior calculado")

    conn.close()

if __name__ == "__main__":
    print("=" * 80)
    print("🔧 RECÁLCULO DE SALDOS POSTERIORES")
    print("=" * 80)

    # Mostrar estado actual
    mostrar_transacciones_sin_saldo()

    # Preguntar confirmación
    print("\n" + "=" * 80)
    respuesta = input("¿Deseas recalcular todos los saldos posteriores? (s/n): ")

    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        print()
        num_actualizadas = recalcular_todos_saldos_posteriores()

        if num_actualizadas > 0:
            print("\n" + "=" * 80)
            print("🔍 Verificando resultado...")
            mostrar_transacciones_sin_saldo()
    else:
        print("\n❌ Operación cancelada")
