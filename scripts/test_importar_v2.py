#!/usr/bin/env python3
"""
Script de prueba para verificar que mostrar_importar_v2() funciona correctamente.

NO ejecuta Streamlit, solo verifica imports y sintaxis.

Uso:
    python3 scripts/test_importar_v2.py
"""

import sys
from pathlib import Path

# Añadir directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def test_imports():
    """Verifica que todos los imports necesarios funcionen"""
    print("🔍 Verificando imports...")

    try:
        # Imports básicos
        import streamlit as st
        print("  ✅ streamlit")

        # Feature flags
        from utils.feature_flags import is_enabled
        print("  ✅ utils.feature_flags")

        # Design tokens
        from utils.design_tokens import Colors, Typography, Spacing, BorderRadius
        print("  ✅ utils.design_tokens")

        # Componentes
        from utils.components.page_layout import render_form_layout, page_section
        print("  ✅ utils.components.page_layout")

        from utils.components.form_card import render_form_card, show_form_feedback
        print("  ✅ utils.components.form_card")

        from utils.components.data_table import render_data_table
        print("  ✅ utils.components.data_table")

        # Módulos de lógica
        from utils import excel_reader, categorizer
        print("  ✅ utils.excel_reader")
        print("  ✅ utils.categorizer")

        from database import db_manager
        print("  ✅ database.db_manager")

        print("\n✅ Todos los imports exitosos!")
        return True

    except ImportError as e:
        print(f"\n❌ Error de import: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False


def test_feature_flag():
    """Verifica que el feature flag USE_NEW_IMPORTAR existe"""
    print("\n🔍 Verificando feature flag USE_NEW_IMPORTAR...")

    try:
        from utils.feature_flags import FeatureFlags, is_enabled

        # Verificar que existe
        if hasattr(FeatureFlags, 'USE_NEW_IMPORTAR'):
            print(f"  ✅ USE_NEW_IMPORTAR existe")

            # Verificar valor actual
            valor = FeatureFlags.USE_NEW_IMPORTAR
            print(f"  📊 Valor actual: {valor}")

            # Verificar función is_enabled
            enabled = is_enabled('USE_NEW_IMPORTAR')
            print(f"  📊 is_enabled('USE_NEW_IMPORTAR'): {enabled}")

            return True
        else:
            print("  ❌ USE_NEW_IMPORTAR NO existe en FeatureFlags")
            return False

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_syntax():
    """Verifica sintaxis de app.py"""
    print("\n🔍 Verificando sintaxis de app.py...")

    try:
        import py_compile
        app_path = root_dir / "app.py"

        py_compile.compile(str(app_path), doraise=True)
        print("  ✅ Sintaxis correcta")
        return True

    except py_compile.PyCompileError as e:
        print(f"  ❌ Error de sintaxis: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def test_functions_exist():
    """Verifica que las funciones existen en app.py"""
    print("\n🔍 Verificando funciones en app.py...")

    try:
        app_path = root_dir / "app.py"
        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar funciones
        functions = [
            'mostrar_importar',
            'mostrar_importar_v1',
            'mostrar_importar_v2'
        ]

        all_found = True
        for func in functions:
            if f"def {func}(" in content:
                print(f"  ✅ {func}()")
            else:
                print(f"  ❌ {func}() NO encontrada")
                all_found = False

        return all_found

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Ejecuta todos los tests"""
    print("=" * 60)
    print("TEST: mostrar_importar_v2()")
    print("=" * 60)

    results = {
        "Imports": test_imports(),
        "Feature Flag": test_feature_flag(),
        "Sintaxis": test_syntax(),
        "Funciones": test_functions_exist()
    }

    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 ¡Todos los tests pasaron!")
        print("\n📝 Próximos pasos:")
        print("   1. Ejecutar la aplicación: streamlit run app.py")
        print("   2. Ir a la página 'Importar desde Excel'")
        print("   3. Verificar que se muestra la versión v1 (flag desactivado)")
        print("   4. Activar flag en utils/feature_flags.py")
        print("   5. Verificar versión v2")
        return 0
    else:
        print("\n❌ Algunos tests fallaron. Revisa los errores arriba.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
