# test_db.py

import os
from database import db_manager
from datetime import date

# --- Configuración de la prueba ---
DB_FILE = 'finanzas.db'

def run_db_tests():
    """Ejecuta una secuencia de pruebas en el gestor de la base de datos."""
    
    # Limpiar la base de datos de pruebas anteriores si existe
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Base de datos anterior '{DB_FILE}' eliminada.")

    print("\n--- INICIO DE LAS PRUEBAS DE LA BASE DE DATOS ---")

    # 1. Crear tablas
    print("\n1. Probando la creación de tablas...")
    db_manager.crear_tablas()

    # 2. Insertar transacciones de ejemplo
    print("\n2. Probando la inserción de transacciones...")
    id1 = db_manager.insertar_transaccion(
        fecha=date(2024, 7, 1),
        concepto="Compra supermercado",
        importe=-75.50,
        categoria="DISFRUTE",
        tipo="GASTO",
        mes=7,
        año=2024
    )
    id2 = db_manager.insertar_transaccion(
        fecha=date(2024, 7, 5),
        concepto="Nómina Julio",
        importe=1800.00,
        categoria="INGRESO",
        tipo="INGRESO",
        mes=7,
        año=2024
    )
    id3 = db_manager.insertar_transaccion(
        fecha=date(2024, 7, 10),
        concepto="Alquiler",
        importe=-850.00,
        categoria="FIJOS",
        tipo="GASTO",
        mes=7,
        año=2024
    )
    print(f"Insertadas 3 transacciones con IDs: {id1}, {id2}, {id3}")

    # 3. Obtener y verificar transacciones
    print("\n3. Probando la obtención de transacciones...")
    transacciones = db_manager.obtener_transacciones()
    print(f"Se encontraron {len(transacciones)} transacciones:")
    for t in transacciones:
        print(f"  - {t['id']}: {t['fecha']} - {t['concepto']} ({t['importe']} €)")
    assert len(transacciones) == 3, "El número de transacciones debería ser 3"

    # 4. Actualizar una transacción
    print("\n4. Probando la actualización de una transacción...")
    campos_a_actualizar = {'categoria': 'SUPERMERCADO', 'notas': 'Compra semanal'}
    actualizacion_exitosa = db_manager.actualizar_transaccion(id1, campos_a_actualizar)
    if actualizacion_exitosa:
        print(f"Transacción {id1} actualizada correctamente.")
    else:
        print(f"Fallo al actualizar la transacción {id1}.")
    
    # Verificar la actualización
    transacciones_actualizadas = db_manager.obtener_transacciones()
    for t in transacciones_actualizadas:
        if t['id'] == id1:
            print(f"  - Datos actualizados: {t}")
            assert t['categoria'] == 'SUPERMERCADO', "La categoría debería haberse actualizado"
            assert t['notas'] == 'Compra semanal', "Las notas deberían haberse actualizado"

    # 5. Eliminar una transacción
    print("\n5. Probando la eliminación de una transacción...")
    eliminacion_exitosa = db_manager.eliminar_transaccion(id2)
    if eliminacion_exitosa:
        print(f"Transacción {id2} (Nómina) eliminada correctamente.")
    else:
        print(f"Fallo al eliminar la transacción {id2}.")

    # 6. Verificar la eliminación
    print("\n6. Verificando el estado final de la base de datos...")
    transacciones_finales = db_manager.obtener_transacciones()
    print(f"Quedan {len(transacciones_finales)} transacciones:")
    for t in transacciones_finales:
        print(f"  - {t['id']}: {t['fecha']} - {t['concepto']} ({t['importe']} €)")
    assert len(transacciones_finales) == 2, "El número de transacciones debería ser 2"

    # 7. Probar funciones de consulta adicionales
    print("\n7. Probando funciones de consulta adicionales...")
    
    # Totales por categoría
    totales = db_manager.obtener_totales_por_categoria(mes=7, año=2024)
    print(f"Totales de gastos por categoría para 07/2024: {totales}")
    assert 'FIJOS' in totales and totales['FIJOS'] == -850.00, "El total de FIJOS es incorrecto"

    # Búsqueda por concepto
    resultados_busqueda = db_manager.buscar_transacciones('super')
    print(f"Resultados de búsqueda para 'super': {len(resultados_busqueda)} encontrados")
    assert len(resultados_busqueda) == 1, "La búsqueda debería encontrar 1 resultado"

    print("\n--- PRUEBAS DE LA BASE DE DATOS COMPLETADAS EXITOSAMENTE ---")

if __name__ == "__main__":
    run_db_tests()
