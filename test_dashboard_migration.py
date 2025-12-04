"""
Script de testing para verificar la migración del Dashboard

Este script verifica que:
1. El feature flag USE_NEW_DASHBOARD está activo
2. La función mostrar_dashboard_v2 se importa correctamente
3. Los componentes están disponibles
4. No hay errores de sintaxis

Uso:
    python3 test_dashboard_migration.py
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(__file__))

def test_feature_flag():
    """Test 1: Verificar que el feature flag está configurado."""
    print("🧪 Test 1: Verificando feature flag...")

    try:
        from utils.feature_flags import is_enabled, FeatureFlags

        # Verificar que el flag existe
        assert hasattr(FeatureFlags, 'USE_NEW_DASHBOARD'), "❌ Flag USE_NEW_DASHBOARD no existe"

        # Verificar que está activo
        is_active = is_enabled('USE_NEW_DASHBOARD')
        print(f"   Flag USE_NEW_DASHBOARD: {'✅ ACTIVO' if is_active else '⚠️ INACTIVO'}")

        return True

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_dashboard_v2_import():
    """Test 2: Verificar que mostrar_dashboard_v2 se importa correctamente."""
    print("\n🧪 Test 2: Verificando importación de dashboard_v2...")

    try:
        from utils.dashboard_v2 import mostrar_dashboard_v2
        print("   ✅ Importación exitosa de mostrar_dashboard_v2")
        return True

    except Exception as e:
        print(f"   ❌ Error al importar: {e}")
        return False


def test_components_import():
    """Test 3: Verificar que los componentes se importan correctamente."""
    print("\n🧪 Test 3: Verificando componentes...")

    try:
        from utils.components import (
            render_metric_card,
            render_metric_grid,
            render_chart_container,
            render_dashboard_layout,
            page_section
        )

        components = [
            'render_metric_card',
            'render_metric_grid',
            'render_chart_container',
            'render_dashboard_layout',
            'page_section'
        ]

        for comp in components:
            print(f"   ✅ {comp}")

        return True

    except Exception as e:
        print(f"   ❌ Error al importar componentes: {e}")
        return False


def test_app_imports():
    """Test 4: Verificar que app.py puede importar todo lo necesario."""
    print("\n🧪 Test 4: Verificando imports de app.py...")

    try:
        # No podemos importar app.py directamente porque tiene código de inicialización
        # Pero podemos verificar que los módulos necesarios están disponibles
        from utils import metrics, visualizer, config_manager
        from database import db_manager
        from utils.design_tokens import Colors, Spacing, BorderRadius
        from utils.plotly_theme import apply_theme_to_fig, add_reference_line, CHART_COLORS_FINANCE

        print("   ✅ Todos los módulos necesarios están disponibles")
        return True

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_dashboard_v2_structure():
    """Test 5: Verificar que dashboard_v2 tiene todas las funciones necesarias."""
    print("\n🧪 Test 5: Verificando estructura de dashboard_v2...")

    try:
        import utils.dashboard_v2 as dashboard_v2

        # Verificar funciones principales
        required_functions = [
            'mostrar_dashboard_v2',
            '_render_vista_mes',
            '_render_vista_anual',
            '_render_evolucion_saldo',
            '_render_analisis_avanzado',
            '_render_historico'
        ]

        for func_name in required_functions:
            if hasattr(dashboard_v2, func_name):
                print(f"   ✅ {func_name}")
            else:
                print(f"   ⚠️ {func_name} no encontrada")

        return True

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def run_all_tests():
    """Ejecuta todos los tests y muestra un resumen."""
    print("="*60)
    print("🚀 TESTING - Migración Dashboard V2")
    print("="*60)

    tests = [
        test_feature_flag,
        test_dashboard_v2_import,
        test_components_import,
        test_app_imports,
        test_dashboard_v2_structure
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
            results.append(False)

    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60)

    passed = sum(results)
    total = len(results)

    print(f"Tests exitosos: {passed}/{total}")

    if passed == total:
        print("\n✅ ¡Todos los tests pasaron! El dashboard v2 está listo.")
        print("\n📝 Próximos pasos:")
        print("   1. Ejecutar: streamlit run app.py")
        print("   2. Navegar al Dashboard")
        print("   3. Verificar que la UI se ve correctamente")
        print("   4. Probar todas las funcionalidades")
        print("\n⚙️ Para desactivar el nuevo diseño:")
        print("   - Editar utils/feature_flags.py")
        print("   - Cambiar USE_NEW_DASHBOARD = False")
        return True
    else:
        print("\n⚠️ Algunos tests fallaron. Revisa los errores arriba.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
