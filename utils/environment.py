# utils/environment.py
import socket
import os
import requests

def check_ollama_availability(host="localhost", port=11434, timeout=2):
    """
    Verifica si el servidor de Ollama está corriendo localmente.
    Intenta conectar al puerto por defecto (11434).
    
    Args:
        host (str): Host de Ollama (default: localhost)
        port (int): Puerto de Ollama (default: 11434)
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si Ollama está disponible, False en caso contrario.
    """
    try:
        # Intento 1: Verificar puerto abierto (más rápido)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result != 0:
            return False
            
        # Intento 2: Verificar API (más seguro)
        response = requests.get(f"http://{host}:{port}/api/tags", timeout=timeout)
        return response.status_code == 200
        
    except Exception:
        return False

def is_local_environment():
    """
    Detecta si la app está corriendo en un entorno local (vs Streamlit Cloud).
    Usa variables de entorno o características del sistema.
    """
    # Streamlit Cloud suele definir variables específicas, pero la prueba de fuego
    # para nuestra feature es si tenemos acceso a Ollama.
    # Por tanto, para efectos de la UI, delegamos en check_ollama_availability
    return check_ollama_availability()
