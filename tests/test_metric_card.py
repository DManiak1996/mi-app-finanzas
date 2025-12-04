"""
Tests unitarios para el componente MetricCard
==============================================

Ejecutar con:
    pytest tests/test_metric_card.py -v
"""

import pytest
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


class TestFormatValue:
    """Tests para _format_value()"""

    def test_format_currency(self):
        """Debe formatear números como moneda europea"""
        assert _format_value(1234.56, "currency") == "1.234,56 €"
        assert _format_value(0.50, "currency") == "0,50 €"
        assert _format_value(1000000, "currency") == "1.000.000,00 €"

    def test_format_percent(self):
        """Debe formatear números como porcentaje"""
        assert _format_value(28.5, "percent") == "28.5%"
        assert _format_value(100, "percent") == "100.0%"
        assert _format_value(0.5, "percent") == "0.5%"

    def test_format_number(self):
        """Debe formatear números según magnitud"""
        # >= 1000: sin decimales
        assert _format_value(1234, "number") == "1.234"
        assert _format_value(10000, "number") == "10.000"

        # >= 10: 1 decimal
        assert _format_value(12.345, "number") == "12.3"
        assert _format_value(99.99, "number") == "100.0"

        # < 10: 2 decimales
        assert _format_value(9.876, "number") == "9.88"
        assert _format_value(0.5, "number") == "0.50"

    def test_format_text(self):
        """Debe retornar texto sin modificar"""
        assert _format_value("Custom Value", "text") == "Custom Value"
        assert _format_value("100€", "text") == "100€"

    def test_string_input(self):
        """Debe manejar strings en formato currency/number"""
        assert _format_value("1234.56", "currency") == "1.234,56 €"
        assert _format_value("100", "percent") == "100.0%"

    def test_invalid_input(self):
        """Debe manejar inputs inválidos sin crash"""
        assert _format_value("invalid", "number") == "invalid"
        assert _format_value(None, "currency") == "None"


class TestFormatDelta:
    """Tests para _format_delta()"""

    def test_format_delta_currency(self):
        """Debe formatear delta como moneda"""
        formatted, icon, color = _format_delta(150.50, "currency", None)
        assert formatted == "+150,50 €"
        assert icon == "↗"
        assert color == Colors.SUCCESS

    def test_format_delta_percent(self):
        """Debe formatear delta como porcentaje"""
        formatted, icon, color = _format_delta(8.5, "percent", None)
        assert formatted == "+8.5%"

    def test_format_delta_negative(self):
        """Debe manejar deltas negativos"""
        formatted, icon, color = _format_delta(-5.2, "percent", None)
        assert formatted == "-5.2%"
        assert icon == "↘"
        assert color == Colors.ERROR

    def test_format_delta_with_trend(self):
        """Debe usar trend si se proporciona"""
        formatted, icon, color = _format_delta(-5.2, "percent", "down")
        assert icon == "↘"
        assert color == Colors.ERROR

    def test_format_delta_string(self):
        """Debe manejar delta como string"""
        formatted, icon, color = _format_delta("+15% vs mes anterior", "text", None)
        assert formatted == "+15% vs mes anterior"
        assert icon == ""
        assert color == Colors.GRAY_700


class TestTrendArrows:
    """Tests para funciones de flechas de tendencia"""

    def test_get_trend_arrow(self):
        """Debe retornar flecha correcta según tendencia"""
        assert _get_trend_arrow("up") == "↗"
        assert _get_trend_arrow("down") == "↘"
        assert _get_trend_arrow("neutral") == "→"
        assert _get_trend_arrow(None) == ""
        assert _get_trend_arrow("invalid") == ""

    def test_get_delta_arrow(self):
        """Debe retornar flecha correcta según valor delta"""
        assert _get_delta_arrow(10) == "↗"
        assert _get_delta_arrow(-10) == "↘"
        assert _get_delta_arrow(0) == "→"


class TestDeltaColor:
    """Tests para _get_delta_color()"""

    def test_delta_color_by_trend(self):
        """Debe usar color según trend si se proporciona"""
        assert _get_delta_color(10, "up") == Colors.SUCCESS
        assert _get_delta_color(-10, "down") == Colors.ERROR
        assert _get_delta_color(0, "neutral") == Colors.GRAY_700

    def test_delta_color_by_value(self):
        """Debe usar color según valor si no hay trend"""
        assert _get_delta_color(10, None) == Colors.SUCCESS
        assert _get_delta_color(-10, None) == Colors.ERROR
        assert _get_delta_color(0, None) == Colors.GRAY_700


class TestColorConfig:
    """Tests para _get_color_config()"""

    def test_success_config(self):
        """Debe retornar config para success"""
        config = _get_color_config("success")
        assert "gradient" in config
        assert "border_color" in config
        assert "base_color" in config
        assert config["gradient"] == Colors.PREMIUM_GRADIENT_TEAL
        assert config["base_color"] == Colors.SUCCESS

    def test_danger_config(self):
        """Debe retornar config para danger"""
        config = _get_color_config("danger")
        assert config["gradient"] == Colors.PREMIUM_GRADIENT_CORAL
        assert config["base_color"] == Colors.ERROR

    def test_info_config(self):
        """Debe retornar config para info"""
        config = _get_color_config("info")
        assert config["gradient"] == Colors.PREMIUM_GRADIENT_SKY
        assert config["base_color"] == Colors.PRIMARY

    def test_warning_config(self):
        """Debe retornar config para warning"""
        config = _get_color_config("warning")
        assert config["gradient"] == Colors.PREMIUM_GRADIENT_GOLD
        assert config["base_color"] == Colors.WARNING

    def test_neutral_config(self):
        """Debe retornar config para neutral"""
        config = _get_color_config("neutral")
        assert config["gradient"] == Colors.PREMIUM_GRADIENT_PRIMARY
        assert config["base_color"] == Colors.GRAY_700

    def test_invalid_config(self):
        """Debe retornar neutral por defecto si variante inválida"""
        config = _get_color_config("invalid")
        assert config["gradient"] == Colors.PREMIUM_GRADIENT_PRIMARY


class TestEdgeCases:
    """Tests para casos límite"""

    def test_very_large_numbers(self):
        """Debe manejar números muy grandes"""
        result = _format_value(1_000_000_000, "currency")
        assert "€" in result

    def test_very_small_numbers(self):
        """Debe manejar números muy pequeños"""
        result = _format_value(0.001, "currency")
        assert "0,00 €" in result

    def test_negative_numbers_currency(self):
        """Debe manejar números negativos en currency"""
        result = _format_value(-1234.56, "currency")
        assert "-" in result
        assert "€" in result

    def test_zero_values(self):
        """Debe manejar ceros correctamente"""
        assert _format_value(0, "currency") == "0,00 €"
        assert _format_value(0, "percent") == "0.0%"
        assert _format_value(0, "number") == "0.00"


class TestIntegration:
    """Tests de integración para flujos completos"""

    def test_metric_card_params_success(self):
        """Debe generar config correcta para métrica success"""
        config = _get_color_config("success")
        formatted_value = _format_value(2500.00, "currency")
        formatted_delta, icon, color = _format_delta(8.5, "percent", "up")

        assert formatted_value == "2.500,00 €"
        assert formatted_delta == "+8.5%"
        assert icon == "↗"
        assert config["base_color"] == Colors.SUCCESS

    def test_metric_card_params_danger(self):
        """Debe generar config correcta para métrica danger"""
        config = _get_color_config("danger")
        formatted_value = _format_value(1800.50, "currency")
        formatted_delta, icon, color = _format_delta(-5.2, "percent", "down")

        assert formatted_value == "1.800,50 €"
        assert formatted_delta == "-5.2%"
        assert icon == "↘"
        assert config["base_color"] == Colors.ERROR


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
