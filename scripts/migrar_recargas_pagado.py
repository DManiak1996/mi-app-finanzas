#!/usr/bin/env python3
# Script para migrar la tabla recargas_coche añadiendo campos pagado y fecha_pago

import sys
import os

# Añadir directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db_manager

def migrar_recargas():
    """
    Añade los campos 'pagado' y 'fecha_pago' a la tabla recargas_coche
    sin perder los datos existentes.
    """
    print("🔄 Iniciando migración de tabla recargas_coche...")

    try:
        conn = db_manager.get_db_connection()
        cursor = conn.cursor()

        # Verificar si los campos ya existen
        cursor.execute("PRAGMA table_info(recargas_coche)")
        columnas = [col[1] for col in cursor.fetchall()]

        if 'pagado' in columnas and 'fecha_pago' in columnas:
            print("✅ Los campos 'pagado' y 'fecha_pago' ya existen. No se necesita migración.")
            conn.close()
            return

        print("📋 Añadiendo campos nuevos a recargas_coche...")

        # Añadir campo 'pagado' si no existe
        if 'pagado' not in columnas:
            cursor.execute("""
                ALTER TABLE recargas_coche
                ADD COLUMN pagado BOOLEAN DEFAULT 0
            """)
            print("  ✅ Campo 'pagado' añadido")

        # Añadir campo 'fecha_pago' si no existe
        if 'fecha_pago' not in columnas:
            cursor.execute("""
                ALTER TABLE recargas_coche
                ADD COLUMN fecha_pago TIMESTAMP
            """)
            print("  ✅ Campo 'fecha_pago' añadido")

        # Marcar todas las recargas existentes como no pagadas
        cursor.execute("UPDATE recargas_coche SET pagado = 0 WHERE pagado IS NULL")

        conn.commit()
        conn.close()

        print()
        print("🎉 ¡Migración completada exitosamente!")
        print()
        print("📝 Las recargas existentes han sido marcadas como 'pendientes' (pagado=0)")
        print("   Puedes usar el botón 'Pagar Recargas del Mes' para marcarlas como pagadas")

    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    migrar_recargas()
