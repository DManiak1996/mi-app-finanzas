#!/usr/bin/env python3
"""
Script para activar/desactivar el nuevo diseño de Transacciones (v2)

Uso:
    python scripts/toggle_transacciones_v2.py on   # Activar v2
    python scripts/toggle_transacciones_v2.py off  # Volver a v1
    python scripts/toggle_transacciones_v2.py      # Ver estado actual
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def get_current_state():
    """Lee el estado actual del flag desde feature_flags.py"""
    feature_flags_path = Path(__file__).parent.parent / "utils" / "feature_flags.py"

    with open(feature_flags_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar la línea USE_NEW_TRANSACCIONES
    for line in content.split('\n'):
        if 'USE_NEW_TRANSACCIONES' in line and '=' in line:
            if 'True' in line:
                return True
            elif 'False' in line:
                return False

    return None

def set_flag(enable: bool):
    """Modifica el feature flag en feature_flags.py"""
    feature_flags_path = Path(__file__).parent.parent / "utils" / "feature_flags.py"

    with open(feature_flags_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Modificar la línea correspondiente
    new_lines = []
    for line in lines:
        if 'USE_NEW_TRANSACCIONES' in line and '=' in line and not line.strip().startswith('#'):
            # Reemplazar el valor
            if enable:
                new_line = '    USE_NEW_TRANSACCIONES = True\n'
            else:
                new_line = '    USE_NEW_TRANSACCIONES = False\n'
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # Escribir de vuelta
    with open(feature_flags_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    return True

def main():
    """Main function"""
    current_state = get_current_state()

    if len(sys.argv) < 2:
        # Solo mostrar estado actual
        print("=" * 60)
        print("Estado actual de Transacciones v2")
        print("=" * 60)

        if current_state is True:
            print("✅ ACTIVO - Usando nuevo diseño (v2)")
            print("\nPara volver al diseño original:")
            print("  python scripts/toggle_transacciones_v2.py off")
        elif current_state is False:
            print("❌ INACTIVO - Usando diseño original (v1)")
            print("\nPara activar el nuevo diseño:")
            print("  python scripts/toggle_transacciones_v2.py on")
        else:
            print("⚠️  ERROR - No se pudo determinar el estado")

        print("=" * 60)
        return

    command = sys.argv[1].lower()

    if command == 'on':
        if current_state is True:
            print("ℹ️  Transacciones v2 ya está ACTIVO")
        else:
            set_flag(True)
            print("✅ Transacciones v2 ACTIVADO")
            print("\nPróximos pasos:")
            print("  1. Reinicia la aplicación Streamlit")
            print("  2. Navega a la página de Transacciones")
            print("  3. Verifica que el nuevo diseño se muestra correctamente")
            print("\nPara revertir:")
            print("  python scripts/toggle_transacciones_v2.py off")

    elif command == 'off':
        if current_state is False:
            print("ℹ️  Transacciones v2 ya está INACTIVO")
        else:
            set_flag(False)
            print("✅ Transacciones v2 DESACTIVADO (volvió a v1)")
            print("\nSe restauró el diseño original")
            print("\nPara reactivar:")
            print("  python scripts/toggle_transacciones_v2.py on")

    else:
        print("❌ Comando no reconocido")
        print("\nUso:")
        print("  python scripts/toggle_transacciones_v2.py on   # Activar v2")
        print("  python scripts/toggle_transacciones_v2.py off  # Volver a v1")
        print("  python scripts/toggle_transacciones_v2.py      # Ver estado")

if __name__ == '__main__':
    main()
