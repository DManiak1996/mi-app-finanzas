"""
Grid System Tests - Suite de pruebas para el sistema de grillas

Ejecutar con: python -m pytest utils/components/grid_system_test.py -v

O si prefieres ejecución simple:
    python utils/components/grid_system_test.py

Autor: Claude Code
Fecha: 2025-12-04
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))


def test_imports():
    """Test 1: Verificar que todos los imports funcionan"""
    print("\n🧪 Test 1: Verificando imports...")

    try:
        from utils.components.grid_system import (
            render_grid,
            render_card_grid,
            render_metric_grid,
            render_image_grid,
            render_masonry_grid,
            auto_grid,
            grid_item,
            responsive_columns,
            _get_spacing_value,
            _generate_grid_css
        )
        print("✅ Todos los imports exitosos")
        return True
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        return False


def test_get_spacing_value():
    """Test 2: Verificar conversión de gaps"""
    print("\n🧪 Test 2: Verificando conversión de gaps...")

    from utils.components.grid_system import _get_spacing_value
    from utils.design_tokens import Spacing

    tests = [
        ('xs', Spacing.XS),
        ('sm', Spacing.SM),
        ('md', Spacing.MD),
        ('lg', Spacing.LG),
        ('xl', Spacing.XL),
    ]

    all_passed = True
    for gap, expected in tests:
        result = _get_spacing_value(gap)
        if result == expected:
            print(f"  ✅ Gap '{gap}' = {result}")
        else:
            print(f"  ❌ Gap '{gap}': esperado {expected}, obtenido {result}")
            all_passed = False

    # Test valor inválido (debe usar default 'md')
    result = _get_spacing_value('invalid')
    if result == Spacing.MD:
        print(f"  ✅ Gap inválido usa default: {result}")
    else:
        print(f"  ❌ Gap inválido: esperado {Spacing.MD}, obtenido {result}")
        all_passed = False

    return all_passed


def test_generate_grid_css():
    """Test 3: Verificar generación de CSS"""
    print("\n🧪 Test 3: Verificando generación de CSS...")

    from utils.components.grid_system import _generate_grid_css

    # Test básico
    css = _generate_grid_css(cols=3, gap='1rem', responsive=False)

    checks = [
        ('.grid-container' in css, "Clase .grid-container presente"),
        ('.grid-item' in css, "Clase .grid-item presente"),
        ('display: grid' in css, "display: grid presente"),
        ('grid-template-columns' in css, "grid-template-columns presente"),
        ('repeat(3, 1fr)' in css, "3 columnas correctas"),
        ('gap: 1rem' in css, "gap correcto"),
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    # Test responsive
    css_responsive = _generate_grid_css(cols=4, gap='1.5rem', responsive=True)

    responsive_checks = [
        ('@media' in css_responsive, "Media queries presentes"),
        ('max-width' in css_responsive, "Breakpoints presentes"),
    ]

    for check, description in responsive_checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    # Test auto-grid
    css_auto = _generate_grid_css(
        cols=3,
        gap='1rem',
        responsive=True,
        min_width='300px',
        auto_fit=True
    )

    auto_checks = [
        ('repeat(auto-fit' in css_auto, "auto-fit presente"),
        ('minmax(300px, 1fr)' in css_auto, "minmax correcto"),
    ]

    for check, description in auto_checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    return all_passed


def test_grid_item():
    """Test 4: Verificar grid_item()"""
    print("\n🧪 Test 4: Verificando grid_item()...")

    from utils.components.grid_system import grid_item

    # Test básico
    item = grid_item("Test content")
    checks = [
        (item['content'] == "Test content", "Contenido correcto"),
        (item['span'] == 1, "Span por defecto = 1"),
        (item['row_span'] == 1, "Row span por defecto = 1"),
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    # Test con spans personalizados
    item2 = grid_item("Wide content", span=2, row_span=3)
    custom_checks = [
        (item2['span'] == 2, "Span personalizado correcto"),
        (item2['row_span'] == 3, "Row span personalizado correcto"),
    ]

    for check, description in custom_checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    return all_passed


def test_responsive_columns():
    """Test 5: Verificar responsive_columns()"""
    print("\n🧪 Test 5: Verificando responsive_columns()...")

    from utils.components.grid_system import responsive_columns

    css = responsive_columns(desktop=5, tablet=3, mobile=1, gap='lg')

    checks = [
        ('.responsive-grid' in css, "Clase .responsive-grid presente"),
        ('repeat(5, 1fr)' in css, "Desktop: 5 columnas"),
        ('repeat(3, 1fr)' in css, "Tablet: 3 columnas"),
        ('repeat(1, 1fr)' in css, "Mobile: 1 columna"),
        ('@media' in css, "Media queries presentes"),
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    return all_passed


def test_data_structures():
    """Test 6: Verificar estructuras de datos"""
    print("\n🧪 Test 6: Verificando estructuras de datos...")

    all_passed = True

    # Test card data
    card_data = {
        "title": "Test Card",
        "content": "1000€",
        "footer": "Test footer",
        "color": "#1f77b4"
    }

    card_checks = [
        ('title' in card_data, "Card tiene 'title'"),
        ('content' in card_data, "Card tiene 'content'"),
        ('footer' in card_data, "Card tiene 'footer'"),
        ('color' in card_data, "Card tiene 'color'"),
    ]

    for check, description in card_checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    # Test metric data
    metric_data = {
        "label": "Test Metric",
        "value": "100",
        "delta": "+10%",
        "delta_color": "normal",
        "help": "Test help"
    }

    metric_checks = [
        ('label' in metric_data, "Metric tiene 'label'"),
        ('value' in metric_data, "Metric tiene 'value'"),
        ('delta' in metric_data, "Metric tiene 'delta'"),
    ]

    for check, description in metric_checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    # Test image data
    image_data = {
        "url": "test.jpg",
        "caption": "Test image",
        "alt": "Test alt text"
    }

    image_checks = [
        ('url' in image_data, "Image tiene 'url'"),
        ('caption' in image_data, "Image tiene 'caption'"),
        ('alt' in image_data, "Image tiene 'alt'"),
    ]

    for check, description in image_checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    return all_passed


def test_integration_with_design_tokens():
    """Test 7: Verificar integración con design_tokens"""
    print("\n🧪 Test 7: Verificando integración con design_tokens...")

    from utils.design_tokens import Spacing, Colors, BorderRadius, Breakpoints

    checks = [
        (hasattr(Spacing, 'XS'), "Spacing.XS existe"),
        (hasattr(Spacing, 'SM'), "Spacing.SM existe"),
        (hasattr(Spacing, 'MD'), "Spacing.MD existe"),
        (hasattr(Spacing, 'LG'), "Spacing.LG existe"),
        (hasattr(Spacing, 'XL'), "Spacing.XL existe"),
        (hasattr(Colors, 'PRIMARY'), "Colors.PRIMARY existe"),
        (hasattr(Colors, 'SUCCESS'), "Colors.SUCCESS existe"),
        (hasattr(Colors, 'ERROR'), "Colors.ERROR existe"),
        (hasattr(BorderRadius, 'BASE'), "BorderRadius.BASE existe"),
        (hasattr(Breakpoints, 'MD'), "Breakpoints.MD existe"),
        (hasattr(Breakpoints, 'LG'), "Breakpoints.LG existe"),
    ]

    all_passed = True
    for check, description in checks:
        if check:
            print(f"  ✅ {description}")
        else:
            print(f"  ❌ {description}")
            all_passed = False

    return all_passed


def test_edge_cases():
    """Test 8: Verificar casos extremos"""
    print("\n🧪 Test 8: Verificando casos extremos...")

    from utils.components.grid_system import _generate_grid_css, _get_spacing_value

    all_passed = True

    # Test columnas fuera de rango
    print("  🔍 Probando valores extremos...")

    # 1 columna (mínimo)
    css_min = _generate_grid_css(cols=1, gap='1rem', responsive=False)
    if 'repeat(1, 1fr)' in css_min:
        print("    ✅ 1 columna funciona")
    else:
        print("    ❌ 1 columna falla")
        all_passed = False

    # 12 columnas (máximo recomendado)
    css_max = _generate_grid_css(cols=12, gap='1rem', responsive=False)
    if 'repeat(12, 1fr)' in css_max:
        print("    ✅ 12 columnas funciona")
    else:
        print("    ❌ 12 columnas falla")
        all_passed = False

    # Gap inválido
    result = _get_spacing_value('invalid_gap')
    from utils.design_tokens import Spacing
    if result == Spacing.MD:
        print("    ✅ Gap inválido usa default MD")
    else:
        print("    ❌ Gap inválido no usa default")
        all_passed = False

    return all_passed


def run_all_tests():
    """Ejecuta todos los tests"""
    print("=" * 70)
    print("GRID SYSTEM - SUITE DE TESTS")
    print("=" * 70)

    tests = [
        ("Imports", test_imports),
        ("Spacing Values", test_get_spacing_value),
        ("CSS Generation", test_generate_grid_css),
        ("Grid Item", test_grid_item),
        ("Responsive Columns", test_responsive_columns),
        ("Data Structures", test_data_structures),
        ("Design Tokens Integration", test_integration_with_design_tokens),
        ("Edge Cases", test_edge_cases),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ Test '{name}' falló con excepción: {e}")
            results.append((name, False))

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)

    total = len(results)
    passed = sum(1 for _, result in results if result)
    failed = total - passed

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print("\n" + "-" * 70)
    print(f"Total: {total} tests")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    print("=" * 70)

    return failed == 0


def run_interactive_test():
    """Test interactivo con Streamlit (opcional)"""
    print("\n" + "=" * 70)
    print("TEST INTERACTIVO")
    print("=" * 70)
    print("\nPara ejecutar tests interactivos con Streamlit:")
    print("\n  streamlit run utils/components/grid_system_examples.py")
    print("\nEsto abrirá una interfaz web donde podrás probar:")
    print("  - Todos los tipos de grids")
    print("  - Configuraciones responsive")
    print("  - Casos de uso reales")
    print("  - Ajustes en tiempo real")


if __name__ == "__main__":
    # Ejecutar tests
    success = run_all_tests()

    # Información adicional
    run_interactive_test()

    # Exit code
    sys.exit(0 if success else 1)
