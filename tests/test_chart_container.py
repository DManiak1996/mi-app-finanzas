#!/usr/bin/env python3
# tests/test_chart_container.py
"""
Tests unitarios para el componente ChartContainer

Ejecutar con:
    python tests/test_chart_container.py
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_imports():
    """Test que todas las importaciones funcionan correctamente."""
    print("Test 1: Verificando importaciones...")

    try:
        from utils.components.chart_container import (
            render_chart_container,
            render_chart_full,
            render_chart_half,
            render_chart_compact,
            add_chart_actions,
            show_chart_loading,
            show_chart_empty,
            create_chart_grid,
            render_chart_with_tabs,
            get_chart_export_button,
            render_chart_preset,
            PRESET_CONFIGS
        )
        print("  ✓ Importación desde chart_container exitosa")
    except Exception as e:
        print(f"  ✗ Error en importación: {e}")
        return False

    try:
        from utils.components import (
            render_chart_container,
            add_chart_actions,
            PRESET_CONFIGS
        )
        print("  ✓ Importación desde utils.components exitosa")
    except Exception as e:
        print(f"  ✗ Error en importación del paquete: {e}")
        return False

    return True


def test_presets():
    """Test que los presets están correctamente definidos."""
    print("\nTest 2: Verificando presets...")

    from utils.components import PRESET_CONFIGS

    expected_presets = ['finance_dashboard', 'compact_widget', 'fullscreen_analysis']

    for preset in expected_presets:
        if preset in PRESET_CONFIGS:
            print(f"  ✓ Preset '{preset}' encontrado")
            config = PRESET_CONFIGS[preset]
            # Verificar que tiene las keys necesarias
            if 'variant' in config and 'height' in config:
                print(f"    - variant: {config['variant']}, height: {config['height']}")
            else:
                print(f"  ✗ Preset '{preset}' incompleto")
                return False
        else:
            print(f"  ✗ Preset '{preset}' no encontrado")
            return False

    return True


def test_actions_helper():
    """Test que add_chart_actions genera acciones correctamente."""
    print("\nTest 3: Verificando add_chart_actions...")

    from utils.components import add_chart_actions

    # Test con todas las opciones
    actions = add_chart_actions(export=True, filter=True, refresh=True)

    if not isinstance(actions, list):
        print("  ✗ add_chart_actions no retorna una lista")
        return False

    if len(actions) != 3:
        print(f"  ✗ Se esperaban 3 acciones, se obtuvieron {len(actions)}")
        return False

    print(f"  ✓ add_chart_actions generó {len(actions)} acciones")

    # Verificar estructura de acciones
    for i, action in enumerate(actions):
        if not isinstance(action, dict):
            print(f"  ✗ Acción {i} no es un diccionario")
            return False

        if 'type' not in action:
            print(f"  ✗ Acción {i} no tiene 'type'")
            return False

        print(f"    - Acción {i}: type={action['type']}, label={action.get('label', 'N/A')}")

    # Test con solo export
    actions = add_chart_actions(export=True, filter=False, refresh=False)
    if len(actions) != 1:
        print(f"  ✗ Se esperaba 1 acción con solo export, se obtuvieron {len(actions)}")
        return False

    print("  ✓ add_chart_actions con opciones selectivas funciona")

    # Test con acciones custom
    custom = [{"type": "button", "label": "Custom"}]
    actions = add_chart_actions(export=False, filter=False, custom_actions=custom)
    if len(actions) != 1:
        print(f"  ✗ Se esperaba 1 acción custom, se obtuvieron {len(actions)}")
        return False

    print("  ✓ add_chart_actions con acciones custom funciona")

    return True


def test_integration_with_design_tokens():
    """Test que la integración con design_tokens funciona."""
    print("\nTest 4: Verificando integración con design_tokens...")

    try:
        from utils.components.chart_container import _get_container_styles
        from utils.design_tokens import Colors, BorderRadius, Spacing

        # Test variante default
        styles = _get_container_styles("default")

        if not isinstance(styles, dict):
            print("  ✗ _get_container_styles no retorna un diccionario")
            return False

        required_keys = ['background', 'border_radius', 'border', 'padding', 'shadow']
        for key in required_keys:
            if key not in styles:
                print(f"  ✗ Falta key '{key}' en styles")
                return False

        print(f"  ✓ Variante 'default' tiene todas las keys necesarias")

        # Test otras variantes
        for variant in ['premium', 'minimal', 'glass']:
            styles = _get_container_styles(variant)
            if not styles or not isinstance(styles, dict):
                print(f"  ✗ Variante '{variant}' no retorna estilos válidos")
                return False
            print(f"  ✓ Variante '{variant}' funciona correctamente")

        return True

    except Exception as e:
        print(f"  ✗ Error en integración: {e}")
        return False


def test_integration_with_plotly_theme():
    """Test que la integración con plotly_theme funciona."""
    print("\nTest 5: Verificando integración con plotly_theme...")

    try:
        from utils.plotly_theme import apply_theme_to_fig
        import plotly.graph_objects as go

        # Crear figura simple
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 5, 6])])

        # Aplicar tema
        fig_with_theme = apply_theme_to_fig(fig)

        if not isinstance(fig_with_theme, go.Figure):
            print("  ✗ apply_theme_to_fig no retorna una Figure")
            return False

        print("  ✓ apply_theme_to_fig funciona correctamente")
        return True

    except Exception as e:
        print(f"  ✗ Error en integración con plotly_theme: {e}")
        return False


def test_feature_flags_integration():
    """Test que la integración con feature flags funciona."""
    print("\nTest 6: Verificando integración con feature_flags...")

    try:
        from utils.feature_flags import is_enabled

        # Test con flag que puede o no existir
        try:
            result = is_enabled("enable_chart_containers")
            print(f"  ✓ Flag existe y retorna: {result}")
        except:
            print("  ✓ Flag no existe, el componente usará comportamiento por defecto")

        # Verificar que is_enabled es callable
        if not callable(is_enabled):
            print("  ✗ is_enabled no es callable")
            return False

        print(f"  ✓ is_enabled funciona correctamente")
        return True

    except Exception as e:
        print(f"  ✗ Error en integración con feature_flags: {e}")
        return False


def run_all_tests():
    """Ejecuta todos los tests."""
    print("=" * 60)
    print("TESTS DEL COMPONENTE CHART_CONTAINER")
    print("=" * 60)

    tests = [
        test_imports,
        test_presets,
        test_actions_helper,
        test_integration_with_design_tokens,
        test_integration_with_plotly_theme,
        test_feature_flags_integration
    ]

    results = []

    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test falló con excepción: {e}")
            results.append(False)

    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"Tests pasados: {passed}/{total}")

    if passed == total:
        print("\n✓ TODOS LOS TESTS PASARON")
        return 0
    else:
        print(f"\n✗ FALLARON {total - passed} TESTS")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
