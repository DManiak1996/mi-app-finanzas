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

    # Obtener IDs existentes para detectar duplicados
    transacciones_existentes = db_manager.obtener_transacciones()
    ids_existentes = {t['id'] for t in transacciones_existentes}

    # Crear un conjunto de transacciones existentes por (fecha, importe, concepto)
    # para detectar duplicados por contenido
    transacciones_por_contenido = {
        (t['fecha'], t['importe'], t['concepto']): t['id']
        for t in transacciones_existentes
    }

    for transaccion in transacciones_importar:
        try:
            # Verificar si ya existe por ID
            if transaccion['id'] in ids_existentes:
                stats["duplicadas"] += 1
                continue

            # Verificar si existe una transacción similar (mismo fecha, importe, concepto)
            clave_contenido = (
                transaccion['fecha'],
                transaccion['importe'],
                transaccion['concepto']
            )

            if clave_contenido in transacciones_por_contenido:
                stats["duplicadas"] += 1
                continue

            # Insertar nueva transacción
            db_manager.insertar_transaccion(
                id=transaccion['id'],
                fecha=transaccion['fecha'],
                concepto=transaccion['concepto'],
                importe=transaccion['importe'],
                categoria=transaccion['categoria'],
                tipo=transaccion['tipo'],
                mes=transaccion['mes'],
                año=transaccion['año'],
                notas=transaccion.get('notas', ''),
                saldo_posterior=transaccion.get('saldo_posterior')
            )

            stats["nuevas"] += 1

        except Exception as e:
            print(f"Error al importar transacción: {e}")
            stats["errores"] += 1

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
