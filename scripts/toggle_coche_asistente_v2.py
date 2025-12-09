#!/usr/bin/env python3
"""
Script para activar/desactivar las versiones v2 de Coche Eléctrico y Asistente IA

Uso:
    python scripts/toggle_coche_asistente_v2.py --enable     # Activar versión v2
    python scripts/toggle_coche_asistente_v2.py --disable    # Desactivar versión v2
    python scripts/toggle_coche_asistente_v2.py --status     # Ver estado actual
"""

import sys
from pathlib import Path

# Añadir el directorio raíz al path para poder importar módulos
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from utils.feature_flags import (
    FeatureFlags,
    is_enabled,
    enable_flag,
    disable_flag,
    save_flags_to_file,
    load_flags_from_file
)


def show_status():
    """Muestra el estado actual de los feature flags."""
    print("\n" + "=" * 60)
    print("📊 ESTADO ACTUAL DE FEATURE FLAGS")
    print("=" * 60 + "\n")

    flags_to_check = [
        ('USE_NEW_COCHE_ELECTRICO', 'Coche Eléctrico v2'),
        ('USE_NEW_ASISTENTE_IA', 'Asistente IA v2'),
    ]

    for flag_name, description in flags_to_check:
        status = is_enabled(flag_name)
        icon = "✅" if status else "⬜"
        status_text = "ACTIVO" if status else "INACTIVO"
        print(f"{icon} {description:30} [{status_text}]")

    print("\n" + "=" * 60 + "\n")


def enable_pages_v2():
    """Activa las versiones v2 de las páginas."""
    print("\n🔄 Activando versiones v2...\n")

    flags_to_enable = [
        ('USE_NEW_COCHE_ELECTRICO', 'Coche Eléctrico v2'),
        ('USE_NEW_ASISTENTE_IA', 'Asistente IA v2'),
    ]

    for flag_name, description in flags_to_enable:
        if enable_flag(flag_name):
            print(f"✅ {description} activado")
        else:
            print(f"❌ Error activando {description}")

    # Guardar cambios
    if save_flags_to_file():
        print("\n💾 Cambios guardados correctamente")
        print("🔄 Reinicia la aplicación para ver los cambios\n")
        show_status()
    else:
        print("\n❌ Error guardando cambios")
        return False

    return True


def disable_pages_v2():
    """Desactiva las versiones v2 de las páginas."""
    print("\n🔄 Desactivando versiones v2...\n")

    flags_to_disable = [
        ('USE_NEW_COCHE_ELECTRICO', 'Coche Eléctrico v2'),
        ('USE_NEW_ASISTENTE_IA', 'Asistente IA v2'),
    ]

    for flag_name, description in flags_to_disable:
        if disable_flag(flag_name):
            print(f"⬜ {description} desactivado")
        else:
            print(f"❌ Error desactivando {description}")

    # Guardar cambios
    if save_flags_to_file():
        print("\n💾 Cambios guardados correctamente")
        print("🔄 Reinicia la aplicación para ver los cambios\n")
        show_status()
    else:
        print("\n❌ Error guardando cambios")
        return False

    return True


def main():
    """Función principal del script."""
    # Cargar flags actuales
    load_flags_from_file()

    # Parsear argumentos
    if len(sys.argv) < 2:
        print("\n⚠️  Error: Debes especificar una acción")
        print("\nUso:")
        print("  python scripts/toggle_coche_asistente_v2.py --enable     # Activar v2")
        print("  python scripts/toggle_coche_asistente_v2.py --disable    # Desactivar v2")
        print("  python scripts/toggle_coche_asistente_v2.py --status     # Ver estado")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action in ['--enable', '-e', 'enable', 'on']:
        enable_pages_v2()

    elif action in ['--disable', '-d', 'disable', 'off']:
        disable_pages_v2()

    elif action in ['--status', '-s', 'status']:
        show_status()

    else:
        print(f"\n⚠️  Error: Acción desconocida '{action}'")
        print("\nAcciones válidas: --enable, --disable, --status")
        sys.exit(1)


if __name__ == '__main__':
    main()
