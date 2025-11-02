#!/usr/bin/env python3
"""
Script para reclasificar todas las transacciones existentes según las nuevas reglas.
"""

import sqlite3
from utils import categorizer

def reclasificar_todas():
    """Reclasifica todas las transacciones en la base de datos."""

    db_path = 'finanzas.db'

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Obtener todas las transacciones
        cursor.execute("SELECT id, concepto, importe, categoria FROM transacciones")
        transacciones = cursor.fetchall()

        print(f"📊 Encontradas {len(transacciones)} transacciones en la base de datos")
        print("🔄 Reclasificando...\n")

        # Estadísticas
        stats = {
            'FIJOS': {'antes': 0, 'despues': 0},
            'DISFRUTE': {'antes': 0, 'despues': 0},
            'EXTRAORDINARIOS': {'antes': 0, 'despues': 0},
            'SIN_CLASIFICAR': {'antes': 0, 'despues': 0}
        }

        cambios = []
        actualizadas = 0

        for trans_id, concepto, importe, categoria_actual in transacciones:
            # Contar categoría anterior
            if categoria_actual:
                stats[categoria_actual]['antes'] = stats.get(categoria_actual, {}).get('antes', 0) + 1

            # Clasificar con nuevas reglas
            nueva_categoria = categorizer.clasificar_transaccion(concepto, importe)

            # Contar nueva categoría
            stats[nueva_categoria]['despues'] = stats.get(nueva_categoria, {}).get('despues', 0) + 1

            # Si cambió, registrar y actualizar
            if nueva_categoria != categoria_actual:
                cambios.append({
                    'id': trans_id,
                    'concepto': concepto[:50],
                    'importe': importe,
                    'antes': categoria_actual or 'None',
                    'despues': nueva_categoria
                })

                # Actualizar en BD
                cursor.execute(
                    "UPDATE transacciones SET categoria = ? WHERE id = ?",
                    (nueva_categoria, trans_id)
                )
                actualizadas += 1

        # Commit de los cambios
        conn.commit()
        conn.close()

        # Mostrar resultados
        print("=" * 80)
        print("📈 ESTADÍSTICAS DE RECLASIFICACIÓN")
        print("=" * 80)
        print(f"\n{'Categoría':<20} {'Antes':<10} {'Después':<10} {'Cambio':<10}")
        print("-" * 80)

        for cat in ['FIJOS', 'DISFRUTE', 'EXTRAORDINARIOS', 'SIN_CLASIFICAR']:
            antes = stats[cat]['antes']
            despues = stats[cat]['despues']
            cambio = despues - antes
            signo = '+' if cambio > 0 else ''
            print(f"{cat:<20} {antes:<10} {despues:<10} {signo}{cambio:<10}")

        print("\n" + "=" * 80)
        print(f"✅ TOTAL ACTUALIZADAS: {actualizadas}/{len(transacciones)} transacciones")
        print("=" * 80)

        # Mostrar algunos ejemplos de cambios
        if cambios:
            print(f"\n📝 EJEMPLOS DE CAMBIOS (mostrando primeros 20):\n")
            for i, cambio in enumerate(cambios[:20], 1):
                print(f"{i}. {cambio['concepto']:<50} {cambio['importe']:>8.2f}€")
                print(f"   {cambio['antes']:>20} → {cambio['despues']:<20}\n")

        print("✅ Reclasificación completada exitosamente!")
        return True

    except Exception as e:
        print(f"❌ Error durante la reclasificación: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando reclasificación de transacciones...\n")
    reclasificar_todas()
