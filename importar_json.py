#!/usr/bin/env python3
# Script para importar un archivo JSON exportado

import json
import sys
from utils import sync

def importar_archivo(ruta_json):
    """
    Importa un archivo JSON a la base de datos.

    Args:
        ruta_json: Ruta al archivo JSON a importar
    """
    print(f"📂 Leyendo archivo: {ruta_json}")

    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✅ Archivo cargado correctamente")
        print(f"   - Versión: {data.get('metadata', {}).get('version', 'N/A')}")
        print(f"   - Transacciones: {data.get('metadata', {}).get('total_transactions', 0)}")
        print(f"   - Recargas: {data.get('metadata', {}).get('total_recargas', 0)}")
        print()

        # Confirmar importación
        respuesta = input("¿Deseas importar estos datos? (s/n): ")
        if respuesta.lower() != 's':
            print("❌ Importación cancelada")
            return

        print("\n🔄 Importando datos...")
        stats = sync.importar_base_datos(data, modo="fusionar")

        print("\n✅ Importación completada!\n")

        # Mostrar estadísticas de transacciones
        print("📋 TRANSACCIONES:")
        print(f"   ✅ Nuevas: {stats['nuevas']}")
        print(f"   ⏭️  Duplicadas (omitidas): {stats['duplicadas']}")
        print(f"   ❌ Errores: {stats['errores']}")

        # Mostrar estadísticas de recargas
        if 'total_recargas' in stats and stats['total_recargas'] > 0:
            print("\n🔌 RECARGAS DE COCHE:")
            print(f"   ✅ Nuevas: {stats.get('nuevas_recargas', 0)}")
            print(f"   ⏭️  Duplicadas (omitidas): {stats.get('duplicadas_recargas', 0)}")
            print(f"   ❌ Errores: {stats.get('errores_recargas', 0)}")

        print("\n🎉 ¡Todo listo! Recarga la app de Streamlit para ver los cambios.")

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
        # Usar el archivo más reciente por defecto
        ruta = "/Users/daniel/Downloads/finanzas_export_20251102_162116.json"
        print(f"⚠️  No se proporcionó ruta, usando archivo más reciente:")
        print(f"   {ruta}\n")

    importar_archivo(ruta)
