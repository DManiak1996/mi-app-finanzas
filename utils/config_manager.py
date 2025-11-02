# utils/config_manager.py
# Gestor de configuración de la aplicación

import json
import os

CONFIG_FILE = 'config/config.json'

def obtener_config():
    """
    Obtiene toda la configuración desde el archivo JSON.

    Returns:
        Dict con la configuración o valores por defecto si no existe
    """
    if not os.path.exists(CONFIG_FILE):
        return {
            'saldo_inicial': 0.0,
            'fecha_saldo_inicial': None,
            'notas': ''
        }

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error al leer configuración: {e}")
        return {
            'saldo_inicial': 0.0,
            'fecha_saldo_inicial': None,
            'notas': ''
        }


def guardar_config(config):
    """
    Guarda la configuración en el archivo JSON.

    Args:
        config: Dict con la configuración a guardar

    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    try:
        # Crear directorio config si no existe
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar configuración: {e}")
        return False


def obtener_saldo_inicial():
    """
    Obtiene el saldo inicial configurado.

    Returns:
        Float con el saldo inicial
    """
    config = obtener_config()
    return config.get('saldo_inicial', 0.0)


def actualizar_saldo_inicial(saldo, fecha=None, notas=''):
    """
    Actualiza el saldo inicial en la configuración.

    Args:
        saldo: Nuevo saldo inicial
        fecha: Fecha del saldo inicial (opcional)
        notas: Notas adicionales (opcional)

    Returns:
        True si se actualizó correctamente
    """
    config = obtener_config()
    config['saldo_inicial'] = float(saldo)

    if fecha:
        config['fecha_saldo_inicial'] = str(fecha)

    if notas:
        config['notas'] = notas

    return guardar_config(config)
