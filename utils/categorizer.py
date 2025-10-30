
# utils/categorizer.py

import json
import re
from pathlib import Path

# Cargar las reglas de clasificación desde el archivo JSON
RULES_FILE = Path(__file__).parent.parent / 'config' / 'categorias.json'

_rules = []

def load_rules():
    """Carga las reglas desde el archivo JSON a una variable global."""
    global _rules
    try:
        with open(RULES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            _rules = data.get('reglas', [])
            # Compilar los patrones de regex para eficiencia
            for rule in _rules:
                rule['regex'] = re.compile(rule['patron'], re.IGNORECASE)
        print(f"Reglas de clasificación cargadas exitosamente desde {RULES_FILE}")
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo de reglas en {RULES_FILE}. El clasificador no funcionará.")
        _rules = []
    except json.JSONDecodeError:
        print(f"Error: El archivo de reglas {RULES_FILE} no es un JSON válido.")
        _rules = []

def clasificar_transaccion(concepto, importe=None):
    """
    Clasifica una transacción basándose en su concepto y las reglas cargadas.
    Ahora también puede considerar el importe.
    Retorna la categoría si encuentra una coincidencia, de lo contrario None.
    """
    if not _rules:
        load_rules()
        if not _rules: # Si la carga falla, no hay nada que hacer
            return "SIN_CLASIFICAR"

    for rule in _rules:
        patron_coincide = False
        importe_coincide = False

        # 1. Verificar si el patrón de texto coincide
        if 'regex' in rule and rule['regex'].search(concepto):
            patron_coincide = True
        # Si no hay patrón en la regla, consideramos que el texto coincide por defecto
        elif 'patron' not in rule or not rule['patron']:
            patron_coincide = True

        # 2. Verificar si el importe coincide (si la regla tiene condición de importe)
        if 'importes_exactos' in rule and importe is not None:
            # Comparamos el valor absoluto del importe
            if abs(importe) in rule['importes_exactos']:
                importe_coincide = True
        else:
            # Si la regla no tiene condición de importe, consideramos que el importe coincide
            importe_coincide = True

        # 3. Si ambas condiciones se cumplen, aplicar la categoría
        if patron_coincide and importe_coincide:
            # Asegurarnos de que no estamos aplicando una regla de solo importe a todo
            if ('patron' in rule and rule['patron']) or 'importes_exactos' in rule:
                 return rule['categoria']
    
    return "SIN_CLASIFICAR" # Devolver una categoría por defecto si no hay coincidencia

# --- Funciones para la gestión de reglas (Fase avanzada) ---

def guardar_regla(patron, categoria, tipo, importes_exactos=None):
    """Añade una nueva regla al archivo JSON y recarga las reglas."""
    try:
        with open(RULES_FILE, 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"reglas": []}

            # Evitar duplicados de patrones si el patrón no está vacío
            if patron and any(r['patron'] == patron for r in data.get('reglas', [])):
                 print(f"La regla con el patrón '{patron}' ya existe.")
                 return False

            nueva_regla = {
                "patron": patron,
                "categoria": categoria,
                "tipo": tipo
            }
            if importes_exactos:
                nueva_regla["importes_exactos"] = importes_exactos

            data.setdefault('reglas', []).append(nueva_regla)
            f.seek(0) # Volver al inicio del archivo para sobreescribir
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()
        
        load_rules() # Recargar las reglas en memoria
        return True
    except Exception as e:
        print(f"Error al guardar la nueva regla: {e}")
        return False

def actualizar_regla(patron_original, regla_actualizada):
    """Actualiza una regla existente en el archivo JSON."""
    try:
        with open(RULES_FILE, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            reglas = data.get('reglas', [])
            
            # Encuentra el índice de la regla a actualizar
            index_a_actualizar = -1
            for i, regla in enumerate(reglas):
                if regla.get('patron') == patron_original:
                    index_a_actualizar = i
                    break
            
            if index_a_actualizar != -1:
                # Verificar si el nuevo patrón ya existe en otra regla
                nuevo_patron = regla_actualizada.get('patron')
                if nuevo_patron and any(r.get('patron') == nuevo_patron and i != index_a_actualizar for i, r in enumerate(reglas)):
                    print(f"Error: El nuevo patrón '{nuevo_patron}' ya existe en otra regla.")
                    return False

                reglas[index_a_actualizar] = regla_actualizada
                data['reglas'] = reglas
                f.seek(0)
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.truncate()
                load_rules()
                return True
            else:
                print(f"Error: No se encontró la regla con el patrón original '{patron_original}'.")
                return False
    except Exception as e:
        print(f"Error al actualizar la regla: {e}")
        return False

def eliminar_regla(patron_a_eliminar):
    """Elimina una regla del archivo JSON basándose en su patrón."""
    try:
        with open(RULES_FILE, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            reglas_originales = data.get('reglas', [])
            
            # Filtrar para mantener todas las reglas excepto la que se va a eliminar
            reglas_actualizadas = [regla for regla in reglas_originales if regla.get('patron') != patron_a_eliminar]
            
            if len(reglas_actualizadas) < len(reglas_originales):
                data['reglas'] = reglas_actualizadas
                f.seek(0)
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.truncate()
                load_rules()
                return True
            else:
                return False # No se encontró la regla
    except Exception as e:
        print(f"Error al eliminar la regla: {e}")
        return False

# Cargar las reglas al iniciar el módulo
load_rules()
