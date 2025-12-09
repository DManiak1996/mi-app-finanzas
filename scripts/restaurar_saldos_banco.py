#!/usr/bin/env python3
"""
Script para restaurar los saldos posteriores desde los Excel del banco.
Esto deshace el recálculo incorrecto que mezcló saldos del banco con acumulativos.
"""

import sys
import os
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import excel_reader
from database.db_manager import get_db_connection
import locale

# Configurar locale para parsear números españoles
try:
    locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_NUMERIC, 'es_ES')
    except:
        print("⚠️  No se pudo configurar locale español, los números pueden no parsearse correctamente")

def restaurar_saldos_desde_excels(directorio_excels):
    """
    Lee todos los Excel del banco y restaura los saldos_posteriores originales.

    Args:
        directorio_excels: Path al directorio con los archivos Excel
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Buscar todos los archivos Excel
    patron = os.path.join(directorio_excels, "movimientosCuenta*.xlsx")
    archivos_excel = sorted(glob.glob(patron))

    if not archivos_excel:
        print(f"❌ No se encontraron archivos Excel en {directorio_excels}")
        return 0

    print(f"📁 Encontrados {len(archivos_excel)} archivos Excel")
    print("=" * 80)

    transacciones_actualizadas = 0
    transacciones_no_encontradas = 0

    for archivo in archivos_excel:
        print(f"\n📄 Procesando: {os.path.basename(archivo)}")

        try:
            # Leer el Excel (devuelve tupla: transacciones, stats)
            transacciones_excel, stats = excel_reader.leer_excel(archivo)

            if not transacciones_excel:
                print(f"   ⚠️  No se encontraron transacciones en el archivo")
                continue

            print(f"   📊 {len(transacciones_excel)} transacciones en el archivo")

            # Para cada transacción del Excel
            for trans in transacciones_excel:
                fecha = trans.get('fecha')
                importe = trans.get('importe')
                saldo_posterior = trans.get('saldo_posterior')

                if saldo_posterior is None:
                    continue  # Saltar si no tiene saldo

                # Buscar la transacción en la BD por fecha e importe
                cursor.execute("""
                    SELECT id, concepto, saldo_posterior as saldo_actual
                    FROM transacciones
                    WHERE fecha = ? AND ABS(importe - ?) < 0.01
                    LIMIT 1
                """, (fecha, importe))

                resultado = cursor.fetchone()

                if resultado:
                    id_trans = resultado['id']
                    concepto = resultado['concepto']
                    saldo_actual = resultado['saldo_actual']

                    # Solo actualizar si el saldo es diferente
                    if abs(saldo_actual - saldo_posterior) > 0.01:
                        cursor.execute("""
                            UPDATE transacciones
                            SET saldo_posterior = ?,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE id = ?
                        """, (saldo_posterior, id_trans))

                        transacciones_actualizadas += 1
                        print(f"   ✅ {fecha}: {concepto[:40]:40} | Saldo: {saldo_actual:.2f}€ → {saldo_posterior:.2f}€")
                else:
                    transacciones_no_encontradas += 1

        except Exception as e:
            print(f"   ❌ Error procesando archivo: {e}")
            continue

    # Commit de todos los cambios
    conn.commit()
    conn.close()

    print("\n" + "=" * 80)
    print(f"✅ Proceso completado:")
    print(f"   - Transacciones actualizadas: {transacciones_actualizadas}")
    print(f"   - Transacciones no encontradas: {transacciones_no_encontradas}")

    return transacciones_actualizadas

def marcar_transacciones_del_banco():
    """
    Añade una columna para marcar qué transacciones vinieron del banco
    vs transacciones manuales.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(transacciones)")
        columnas = [col[1] for col in cursor.fetchall()]

        if 'saldo_es_del_banco' not in columnas:
            print("🔧 Añadiendo columna 'saldo_es_del_banco' a la tabla transacciones...")
            cursor.execute("""
                ALTER TABLE transacciones
                ADD COLUMN saldo_es_del_banco BOOLEAN DEFAULT 0
            """)
            conn.commit()
            print("✅ Columna añadida correctamente")
        else:
            print("ℹ️  La columna 'saldo_es_del_banco' ya existe")

        # Marcar transacciones que NO son del coche eléctrico y tienen concepto diferente de "Recarga coche"
        # (asumimos que las del banco tienen saldo_posterior y no son pagos manuales)
        cursor.execute("""
            UPDATE transacciones
            SET saldo_es_del_banco = 1
            WHERE concepto NOT LIKE '%Recarga coche%'
              AND saldo_posterior IS NOT NULL
        """)

        num_marcadas = cursor.rowcount
        conn.commit()

        print(f"✅ Marcadas {num_marcadas} transacciones como 'del banco'")

        return num_marcadas

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return 0
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 80)
    print("🔄 RESTAURAR SALDOS POSTERIORES DESDE EXCEL DEL BANCO")
    print("=" * 80)

    # Directorio donde están los Excel
    directorio = "/Users/daniel/Desktop/DANIEL/GASTOS/"

    # Paso 1: Añadir columna para distinguir origen
    print("\n📌 PASO 1: Marcar transacciones del banco")
    print("=" * 80)
    marcar_transacciones_del_banco()

    # Paso 2: Restaurar saldos desde Excel
    print("\n📌 PASO 2: Restaurar saldos desde archivos Excel")
    print("=" * 80)
    respuesta = input(f"¿Restaurar saldos desde {directorio}? (s/n): ")

    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        num_restauradas = restaurar_saldos_desde_excels(directorio)

        if num_restauradas > 0:
            print("\n✅ Saldos restaurados correctamente")
            print("💡 Ahora las transacciones del banco tienen sus saldos originales")
            print("💡 Las transacciones manuales (coche eléctrico) necesitarán recálculo selectivo")
        else:
            print("\n⚠️  No se restauró ningún saldo")
    else:
        print("\n❌ Operación cancelada")
