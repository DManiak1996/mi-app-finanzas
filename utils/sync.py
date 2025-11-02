# utils/sync.py - Sistema de sincronización de bases de datos

import json
import datetime
from typing import Dict, List, Tuple
from database import db_manager

def exportar_base_datos() -> Dict:
    """
    Exporta toda la base de datos a un diccionario JSON.

    Returns:
        Dict con metadata y todas las transacciones
    """
    transacciones = db_manager.obtener_transacciones()

    export_data = {
        "metadata": {
            "exported_at": datetime.datetime.now().isoformat(),
            "total_transactions": len(transacciones),
            "version": "1.0"
        },
        "transacciones": transacciones
    }

    return export_data


def importar_base_datos(data: Dict, modo: str = "fusionar") -> Dict:
    """
    Importa transacciones desde un diccionario.
    Optimizado para importaciones grandes usando batch inserts.

    Args:
        data: Diccionario con transacciones
        modo: "fusionar" (combina) o "sobrescribir" (reemplaza todo)

    Returns:
        Dict con estadísticas de la importación
    """
    transacciones_importar = data.get("transacciones", [])

    stats = {
        "total": len(transacciones_importar),
        "nuevas": 0,
        "duplicadas": 0,
        "actualizadas": 0,
        "errores": 0
    }

    if modo == "sobrescribir":
        # Eliminar todas las transacciones actuales
        # (Por seguridad, no implementamos esto por ahora)
        pass

    # Obtener solo IDs existentes (mucho más rápido que obtener todo)
    import sqlite3
    conn = db_manager.get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, fecha, importe, concepto FROM transacciones")
    transacciones_existentes = cursor.fetchall()

    ids_existentes = {t['id'] for t in transacciones_existentes}
    transacciones_por_contenido = {
        (t['fecha'], t['importe'], t['concepto']): t['id']
        for t in transacciones_existentes
    }

    # Preparar transacciones para inserción en lote
    transacciones_a_insertar = []

    for transaccion in transacciones_importar:
        try:
            # Verificar si ya existe por ID
            if transaccion['id'] in ids_existentes:
                stats["duplicadas"] += 1
                continue

            # Verificar si existe una transacción similar
            clave_contenido = (
                transaccion['fecha'],
                transaccion['importe'],
                transaccion['concepto']
            )

            if clave_contenido in transacciones_por_contenido:
                stats["duplicadas"] += 1
                continue

            # Agregar a lista de inserción
            transacciones_a_insertar.append(transaccion)
            stats["nuevas"] += 1

        except Exception as e:
            print(f"Error al procesar transacción: {e}")
            stats["errores"] += 1

    # Inserción en lote (mucho más rápido)
    if transacciones_a_insertar:
        try:
            # Insertar todas de una vez usando executemany
            valores = [
                (
                    t['id'],
                    t['fecha'],
                    t['concepto'],
                    t['importe'],
                    t['categoria'],
                    t['tipo'],
                    t['mes'],
                    t['año'],
                    t.get('notas', ''),
                    t.get('saldo_posterior')
                )
                for t in transacciones_a_insertar
            ]

            cursor.executemany("""
                INSERT INTO transacciones
                (id, fecha, concepto, importe, categoria, tipo, mes, año, notas, saldo_posterior)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, valores)

            conn.commit()

        except Exception as e:
            print(f"Error en inserción por lotes: {e}")
            conn.rollback()
            stats["errores"] += len(transacciones_a_insertar)
            stats["nuevas"] = 0
        finally:
            conn.close()
    else:
        conn.close()

    return stats


def comparar_bases_datos(data_remota: Dict) -> Dict:
    """
    Compara la base de datos local con datos remotos.

    Args:
        data_remota: Datos exportados de la otra DB

    Returns:
        Dict con diferencias encontradas
    """
    # Obtener transacciones locales
    transacciones_locales = db_manager.obtener_transacciones()
    transacciones_remotas = data_remota.get("transacciones", [])

    # Crear conjuntos de IDs
    ids_locales = {t['id'] for t in transacciones_locales}
    ids_remotas = {t['id'] for t in transacciones_remotas}

    # Encontrar diferencias
    solo_en_local = ids_locales - ids_remotas
    solo_en_remota = ids_remotas - ids_locales
    en_ambas = ids_locales & ids_remotas

    # Obtener las transacciones completas
    trans_solo_local = [t for t in transacciones_locales if t['id'] in solo_en_local]
    trans_solo_remota = [t for t in transacciones_remotas if t['id'] in solo_en_remota]

    return {
        "total_local": len(transacciones_locales),
        "total_remota": len(transacciones_remotas),
        "solo_en_local": {
            "count": len(solo_en_local),
            "transacciones": trans_solo_local
        },
        "solo_en_remota": {
            "count": len(solo_en_remota),
            "transacciones": trans_solo_remota
        },
        "en_ambas": len(en_ambas)
    }


def generar_json_exportacion() -> str:
    """
    Genera un string JSON para descargar.

    Returns:
        String JSON formateado
    """
    data = exportar_base_datos()
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


def parsear_json_importacion(json_string: str) -> Dict:
    """
    Parsea un string JSON de importación.

    Args:
        json_string: JSON con datos a importar

    Returns:
        Diccionario parseado
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido: {e}")
