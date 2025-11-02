#!/usr/bin/env python3
# Script para importar SOLO las recargas desde un JSON (ignorando transacciones)

import json
import sys
from database import db_manager

def importar_solo_recargas(ruta_json):
    """
    Importa solo las recargas desde un archivo JSON.

    Args:
        ruta_json: Ruta al archivo JSON a importar
    """
    print(f"📂 Leyendo archivo: {ruta_json}")

    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        recargas = data.get('recargas_coche', [])

        print(f"✅ Archivo cargado correctamente")
        print(f"   - Versión: {data.get('metadata', {}).get('version', 'N/A')}")
        print(f"   - Recargas encontradas: {len(recargas)}")

        if not recargas:
            print("\n⚠️  No hay recargas en el archivo JSON")
            print("   Asegúrate de haber exportado desde Streamlit Cloud con el código actualizado.")
            return

        print("\n🔌 Recargas a importar:")
        for i, r in enumerate(recargas, 1):
            fecha = r.get('fecha_recarga', 'N/A')
            kwh = r.get('kwh_cargados', 0)
            coste = r.get('coste_total', 0)
            print(f"   {i}. {fecha[:10]} - {kwh:.2f} kWh - {coste:.2f} €")

        print()

        # Confirmar importación
        respuesta = input("¿Deseas importar estas recargas? (s/n): ")
        if respuesta.lower() != 's':
            print("❌ Importación cancelada")
            return

        print("\n🔄 Importando recargas...")

        # Conectar a BD
        import sqlite3
        conn = db_manager.get_db_connection()
        cursor = conn.cursor()

        try:
            # Obtener IDs de recargas existentes
            cursor.execute("SELECT id FROM recargas_coche")
            ids_existentes = {row['id'] for row in cursor.fetchall()}

            nuevas = 0
            duplicadas = 0
            errores = 0

            # Preparar recargas para inserción
            recargas_a_insertar = []

            for recarga in recargas:
                if recarga['id'] in ids_existentes:
                    duplicadas += 1
                    continue

                recargas_a_insertar.append(recarga)
                nuevas += 1

            # Inserción en lote
            if recargas_a_insertar:
                valores = [
                    (
                        r['id'],
                        r['fecha_recarga'],
                        r.get('bateria_inicial', 20),
                        r.get('bateria_final', 80),
                        r['kwh_cargados'],
                        r.get('km_recorridos', 0),
                        r.get('consumo_medio', 0),
                        r['franja_horaria'],
                        r['tarifa_kwh'],
                        r.get('coste_energia', 0),
                        r.get('coste_potencia', 0),
                        r.get('coste_alquiler', 0),
                        r.get('coste_bono', 0),
                        r.get('coste_servicios', 0),
                        r.get('impuesto_electricidad', 0),
                        r.get('iva', 0),
                        r['coste_total'],
                        r['mes'],
                        r['año'],
                        r.get('transaccion_id'),
                        r.get('categoria', 'FIJOS'),
                        r.get('notas', '')
                    )
                    for r in recargas_a_insertar
                ]

                cursor.executemany("""
                    INSERT INTO recargas_coche (
                        id, fecha_recarga, bateria_inicial, bateria_final, kwh_cargados,
                        km_recorridos, consumo_medio, franja_horaria, tarifa_kwh,
                        coste_energia, coste_potencia, coste_alquiler, coste_bono, coste_servicios,
                        impuesto_electricidad, iva, coste_total,
                        mes, año, transaccion_id, categoria, notas
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, valores)

                conn.commit()
                print(f"\n✅ Importación completada!")
            else:
                print(f"\n⚠️  No hay recargas nuevas para importar (todas ya existen)")

            print(f"\n🔌 RECARGAS:")
            print(f"   ✅ Nuevas: {nuevas}")
            print(f"   ⏭️  Duplicadas (omitidas): {duplicadas}")
            print(f"   ❌ Errores: {errores}")

            print("\n🎉 ¡Todo listo! Recarga la app de Streamlit para ver las recargas.")

        except Exception as e:
            print(f"❌ Error al importar recargas: {e}")
            import traceback
            traceback.print_exc()
            conn.rollback()
        finally:
            conn.close()

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {ruta_json}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: El archivo no es un JSON válido - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Ruta proporcionada como argumento
        ruta = sys.argv[1]
    else:
        # Buscar el archivo más reciente
        import glob
        import os

        archivos = glob.glob("/Users/daniel/Downloads/finanzas_export_*.json")
        if archivos:
            ruta = max(archivos, key=os.path.getmtime)
            print(f"⚠️  No se proporcionó ruta, usando archivo más reciente:")
            print(f"   {ruta}\n")
        else:
            print("❌ No se encontraron archivos de exportación en ~/Downloads")
            print("   Uso: python importar_solo_recargas.py <ruta_al_archivo.json>")
            sys.exit(1)

    importar_solo_recargas(ruta)
