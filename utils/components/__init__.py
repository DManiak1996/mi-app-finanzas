"""
Componentes reutilizables para la UI

Este paquete contiene componentes de diseño centralizados que siguen
los design tokens definidos en utils/design_tokens.py
"""

from .form_card import (
    render_form_card,
    form_section,
    form_field_group,
    form_actions,
    show_form_feedback,
    validate_required_fields,
    show_validation_error,
)

from .data_table import (
    # Funciones principales
    render_data_table,
    render_transaction_table,
    render_summary_table,
    render_compact_table,

    # Formatters
    format_currency_column,
    format_date_column,
    format_percentage_column,
    format_number_column,
    auto_format_dataframe,

    # Export
    export_table,

    # Helpers
    add_row_actions,
    show_table_stats,

    # Classes
    ColumnConfig,
)

from .chart_container import (
    # Función principal
    render_chart_container,

    # Variantes
    render_chart_full,
    render_chart_half,
    render_chart_compact,

    # Helpers
    add_chart_actions,
    show_chart_loading,
    show_chart_empty,

    # Utilidades
    create_chart_grid,
    render_chart_with_tabs,
    get_chart_export_button,
    render_chart_preset,

    # Presets
    PRESET_CONFIGS
)

from .metric_card import (
    # Función principal
    render_metric_card,

    # Variantes
    metric_card_success,
    metric_card_danger,
    metric_card_info,
    metric_card_warning,
    metric_card_neutral,

    # Utilidades
    render_metric_row,
    render_metric_grid,
)

from .page_layout import (
    # Función principal
    render_page_layout,

    # Layouts predefinidos
    render_dashboard_layout,
    render_form_layout,
    render_table_layout,
    render_detail_layout,

    # Helpers
    page_header,
    page_breadcrumbs,
    page_section,
    page_divider,
    page_footer,
)

from .grid_system import (
    # Funciones principales
    render_grid,
    render_card_grid,
    render_metric_grid as grid_metric_render,  # Alias to avoid conflict
    render_image_grid,
    render_masonry_grid,
    auto_grid,

    # Helpers
    grid_item,
    responsive_columns,
)

__all__ = [
    # Form components
    "render_form_card",
    "form_section",
    "form_field_group",
    "form_actions",
    "show_form_feedback",
    "validate_required_fields",
    "show_validation_error",

    # Data Table components
    "render_data_table",
    "render_transaction_table",
    "render_summary_table",
    "render_compact_table",
    "format_currency_column",
    "format_date_column",
    "format_percentage_column",
    "format_number_column",
    "auto_format_dataframe",
    "export_table",
    "add_row_actions",
    "show_table_stats",
    "ColumnConfig",

    # Chart components
    "render_chart_container",
    "render_chart_full",
    "render_chart_half",
    "render_chart_compact",
    "add_chart_actions",
    "show_chart_loading",
    "show_chart_empty",
    "create_chart_grid",
    "render_chart_with_tabs",
    "get_chart_export_button",
    "render_chart_preset",
    "PRESET_CONFIGS",

    # Metric Card components
    "render_metric_card",
    "metric_card_success",
    "metric_card_danger",
    "metric_card_info",
    "metric_card_warning",
    "metric_card_neutral",
    "render_metric_row",
    "render_metric_grid",

    # Page Layout components
    "render_page_layout",
    "render_dashboard_layout",
    "render_form_layout",
    "render_table_layout",
    "render_detail_layout",
    "page_header",
    "page_breadcrumbs",
    "page_section",
    "page_divider",
    "page_footer",

    # Grid System components
    "render_grid",
    "render_card_grid",
    "grid_metric_render",
    "render_image_grid",
    "render_masonry_grid",
    "auto_grid",
    "grid_item",
    "responsive_columns",
]
