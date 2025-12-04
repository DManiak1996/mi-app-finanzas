"""
Tests simples para el componente MetricCard (sin pytest)
=========================================================

Ejecutar con:
    python tests/test_metric_card_simple.py
"""

import sys
sys.path.insert(0, '.')

from utils.components.metric_card import (
    _format_value,
    _format_delta,
    _get_trend_arrow,
    _get_delta_arrow,
    _get_delta_color,
    _get_color_config
)
from utils.design_tokens import Colors


def test_format_value():
    """Tests para _format_value()"""
    print("Testing _format_value()...")

    # Currency
    assert _format_value(1234.56, "currency") == "1.234,56 €", "Currency format failed"
    assert _format_value(0.50, "currency") == "0,50 €", "Currency format failed for small value"

    # Percent
    assert _format_value(28.5, "percent") == "28.5%", "Percent format failed"

    # Number
    assert _format_value(1234, "number") == "1.234", "Number format failed for >= 1000"
    assert "12.3" in _format_value(12.345, "number"), "Number format failed for >= 10"

    # Text
    assert _format_value("Custom", "text") == "Custom", "Text format failed"

    print("  ✅ All _format_value tests passed!")


def test_format_delta():
    """Tests para _format_delta()"""
    print("Testing _format_delta()...")

    # Positive delta
    formatted, icon, color = _format_delta(150.50, "currency", None)
    assert "150" in formatted, "Delta formatting failed"
    assert icon == "↗", "Delta arrow failed"
    assert color == Colors.SUCCESS, "Delta color failed"

    # Negative delta
    formatted, icon, color = _format_delta(-5.2, "percent", None)
    assert "-5.2" in formatted, "Negative delta formatting failed"
    assert icon == "↘", "Negative delta arrow failed"
    assert color == Colors.ERROR, "Negative delta color failed"

    print("  ✅ All _format_delta tests passed!")


def test_trend_arrows():
    """Tests para flechas de tendencia"""
    print("Testing trend arrows...")

    assert _get_trend_arrow("up") == "↗", "Up arrow failed"
    assert _get_trend_arrow("down") == "↘", "Down arrow failed"
    assert _get_trend_arrow("neutral") == "→", "Neutral arrow failed"
    assert _get_trend_arrow(None) == "", "None arrow failed"

    assert _get_delta_arrow(10) == "↗", "Positive delta arrow failed"
    assert _get_delta_arrow(-10) == "↘", "Negative delta arrow failed"
    assert _get_delta_arrow(0) == "→", "Zero delta arrow failed"

    print("  ✅ All trend arrow tests passed!")


def test_delta_color():
    """Tests para colores de delta"""
    print("Testing delta colors...")

    # By trend
    assert _get_delta_color(10, "up") == Colors.SUCCESS, "Success color failed"
    assert _get_delta_color(-10, "down") == Colors.ERROR, "Error color failed"
    assert _get_delta_color(0, "neutral") == Colors.GRAY_700, "Neutral color failed"

    # By value
    assert _get_delta_color(10, None) == Colors.SUCCESS, "Positive value color failed"
    assert _get_delta_color(-10, None) == Colors.ERROR, "Negative value color failed"

    print("  ✅ All delta color tests passed!")


def test_color_config():
    """Tests para configuración de colores"""
    print("Testing color configs...")

    # Success
    config = _get_color_config("success")
    assert config["gradient"] == Colors.PREMIUM_GRADIENT_TEAL, "Success gradient failed"
    assert config["base_color"] == Colors.SUCCESS, "Success base color failed"

    # Danger
    config = _get_color_config("danger")
    assert config["gradient"] == Colors.PREMIUM_GRADIENT_CORAL, "Danger gradient failed"
    assert config["base_color"] == Colors.ERROR, "Danger base color failed"

    # Info
    config = _get_color_config("info")
    assert config["gradient"] == Colors.PREMIUM_GRADIENT_SKY, "Info gradient failed"
    assert config["base_color"] == Colors.PRIMARY, "Info base color failed"

    # Warning
    config = _get_color_config("warning")
    assert config["gradient"] == Colors.PREMIUM_GRADIENT_GOLD, "Warning gradient failed"
    assert config["base_color"] == Colors.WARNING, "Warning base color failed"

    # Neutral
    config = _get_color_config("neutral")
    assert config["gradient"] == Colors.PREMIUM_GRADIENT_PRIMARY, "Neutral gradient failed"
    assert config["base_color"] == Colors.GRAY_700, "Neutral base color failed"

    # Invalid (should default to neutral)
    config = _get_color_config("invalid")
    assert config["gradient"] == Colors.PREMIUM_GRADIENT_PRIMARY, "Invalid config failed"

    print("  ✅ All color config tests passed!")


def test_edge_cases():
    """Tests para casos límite"""
    print("Testing edge cases...")

    # Large numbers
    result = _format_value(1_000_000_000, "currency")
    assert "€" in result, "Large number format failed"

    # Zero
    assert _format_value(0, "currency") == "0,00 €", "Zero currency failed"
    assert _format_value(0, "percent") == "0.0%", "Zero percent failed"

    # Negative
    result = _format_value(-1234.56, "currency")
    assert "-" in result and "€" in result, "Negative currency failed"

    print("  ✅ All edge case tests passed!")


def test_integration():
    """Tests de integración"""
    print("Testing integration scenarios...")

    # Success metric
    config = _get_color_config("success")
    formatted_value = _format_value(2500.00, "currency")
    formatted_delta, icon, color = _format_delta(8.5, "percent", "up")

    assert formatted_value == "2.500,00 €", "Success value failed"
    assert "8.5" in formatted_delta, "Success delta failed"
    assert icon == "↗", "Success arrow failed"
    assert config["base_color"] == Colors.SUCCESS, "Success config failed"

    # Danger metric
    config = _get_color_config("danger")
    formatted_value = _format_value(1800.50, "currency")
    formatted_delta, icon, color = _format_delta(-5.2, "percent", "down")

    assert formatted_value == "1.800,50 €", "Danger value failed"
    assert "-5.2" in formatted_delta, "Danger delta failed"
    assert icon == "↘", "Danger arrow failed"
    assert config["base_color"] == Colors.ERROR, "Danger config failed"

    print("  ✅ All integration tests passed!")


def main():
    """Ejecutar todos los tests"""
    print("=" * 60)
    print("Running MetricCard Component Tests")
    print("=" * 60)
    print()

    try:
        test_format_value()
        test_format_delta()
        test_trend_arrows()
        test_delta_color()
        test_color_config()
        test_edge_cases()
        test_integration()

        print()
        print("=" * 60)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("=" * 60)
        return 0

    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 60)
        return 1

    except Exception as e:
        print()
        print("=" * 60)
        print(f"💥 ERROR: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
