# utils/components/data_table.py
"""
DataTable Component - Tablas consistentes y funcionales con estilo premium

Este módulo proporciona componentes de tabla reutilizables con:
- Formateo inteligente (moneda, fechas, porcentajes, números)
- Búsqueda y filtrado
- Ordenamiento por columnas
- Paginación opcional
- Acciones por fila (editar, eliminar, ver)
- Exportación (CSV, Excel)
- Estilos premium integrados con design_tokens

Uso:
    from utils.components.data_table import render_data_table, render_transaction_table

    # Tabla básica
    render_data_table(df, columns=['fecha', 'concepto', 'importe'])

    # Tabla de transacciones con acciones
    render_transaction_table(
        df,
        on_edit=lambda row: st.write(f"Editar {row['id']}"),
        on_delete=lambda row: st.write(f"Eliminar {row['id']}")
    )
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Optional, Callable, Dict, List, Any, Literal
import io

from utils.design_tokens import Colors, Typography, Spacing, BorderRadius, Config


# ========== FORMATTERS (Funciones de formateo) ==========

def format_currency_column(df: pd.DataFrame, column: str, symbol: str = "€") -> pd.DataFrame:
    """
    Formatea una columna como moneda con símbolo y separadores.

    Args:
        df: DataFrame a formatear
        column: Nombre de la columna
        symbol: Símbolo de moneda (default: €)

    Returns:
        DataFrame con columna formateada

    Example:
        >>> df = format_currency_column(df, 'importe')
        # 1234.56 -> 1,234.56 €
    """
    if column not in df.columns:
        return df

    df = df.copy()
    df[column] = df[column].apply(
        lambda x: f"{x:,.2f} {symbol}".replace(",", "X").replace(".", ",").replace("X", ".")
        if pd.notna(x) and isinstance(x, (int, float)) else x
    )
    return df


def format_date_column(df: pd.DataFrame, column: str, format: str = "%d/%m/%Y") -> pd.DataFrame:
    """
    Formatea una columna de fechas al formato deseado.

    Args:
        df: DataFrame a formatear
        column: Nombre de la columna
        format: Formato de fecha (default: DD/MM/YYYY)

    Returns:
        DataFrame con columna formateada

    Example:
        >>> df = format_date_column(df, 'fecha')
        # 2024-03-15 -> 15/03/2024
    """
    if column not in df.columns:
        return df

    df = df.copy()
    df[column] = pd.to_datetime(df[column], errors='coerce').dt.strftime(format)
    return df


def format_percentage_column(df: pd.DataFrame, column: str, decimals: int = 1) -> pd.DataFrame:
    """
    Formatea una columna como porcentaje con símbolo %.

    Args:
        df: DataFrame a formatear
        column: Nombre de la columna
        decimals: Número de decimales (default: 1)

    Returns:
        DataFrame con columna formateada

    Example:
        >>> df = format_percentage_column(df, 'porcentaje')
        # 0.856 -> 85.6%
    """
    if column not in df.columns:
        return df

    df = df.copy()
    df[column] = df[column].apply(
        lambda x: f"{x * 100:.{decimals}f}%" if pd.notna(x) and isinstance(x, (int, float)) else x
    )
    return df


def format_number_column(df: pd.DataFrame, column: str, decimals: int = 2) -> pd.DataFrame:
    """
    Formatea una columna numérica con separadores de miles.

    Args:
        df: DataFrame a formatear
        column: Nombre de la columna
        decimals: Número de decimales (default: 2)

    Returns:
        DataFrame con columna formateada

    Example:
        >>> df = format_number_column(df, 'cantidad')
        # 1234.56 -> 1,234.56
    """
    if column not in df.columns:
        return df

    df = df.copy()
    df[column] = df[column].apply(
        lambda x: f"{x:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        if pd.notna(x) and isinstance(x, (int, float)) else x
    )
    return df


def auto_format_dataframe(
    df: pd.DataFrame,
    currency_columns: List[str] = None,
    date_columns: List[str] = None,
    percentage_columns: List[str] = None,
    number_columns: List[str] = None
) -> pd.DataFrame:
    """
    Aplica formateo automático a múltiples columnas del DataFrame.

    Args:
        df: DataFrame a formatear
        currency_columns: Lista de columnas de moneda
        date_columns: Lista de columnas de fecha
        percentage_columns: Lista de columnas de porcentaje
        number_columns: Lista de columnas numéricas

    Returns:
        DataFrame formateado
    """
    df = df.copy()

    # Formatear monedas
    if currency_columns:
        for col in currency_columns:
            if col in df.columns:
                df = format_currency_column(df, col)

    # Formatear fechas
    if date_columns:
        for col in date_columns:
            if col in df.columns:
                df = format_date_column(df, col)

    # Formatear porcentajes
    if percentage_columns:
        for col in percentage_columns:
            if col in df.columns:
                df = format_percentage_column(df, col)

    # Formatear números
    if number_columns:
        for col in number_columns:
            if col in df.columns:
                df = format_number_column(df, col)

    return df


# ========== EXPORT FUNCTIONS ==========

def export_table(df: pd.DataFrame, filename: str, format: Literal['csv', 'excel'] = 'csv') -> bytes:
    """
    Exporta DataFrame a CSV o Excel.

    Args:
        df: DataFrame a exportar
        filename: Nombre base del archivo
        format: Formato de exportación ('csv' o 'excel')

    Returns:
        Bytes del archivo para descarga

    Example:
        >>> data = export_table(df, 'transacciones', 'excel')
        >>> st.download_button("Descargar", data, "transacciones.xlsx")
    """
    if format == 'csv':
        return df.to_csv(index=False).encode('utf-8')
    elif format == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Datos')
        return output.getvalue()
    else:
        raise ValueError(f"Formato no soportado: {format}")


# ========== COLUMN CONFIGURATION ==========

class ColumnConfig:
    """Configuración de columna para st.dataframe"""

    def __init__(
        self,
        label: str = None,
        width: str = None,
        help: str = None,
        disabled: bool = False,
        required: bool = False,
    ):
        self.label = label
        self.width = width
        self.help = help
        self.disabled = disabled
        self.required = required

    def to_streamlit_config(self):
        """Convierte a configuración de Streamlit"""
        config = {}
        if self.label:
            config['label'] = self.label
        if self.width:
            config['width'] = self.width
        if self.help:
            config['help'] = self.help
        if self.disabled:
            config['disabled'] = self.disabled
        if self.required:
            config['required'] = self.required
        return config


# ========== MAIN COMPONENTS ==========

def render_data_table(
    df: pd.DataFrame,
    title: str = None,
    columns: List[str] = None,
    column_config: Dict[str, ColumnConfig] = None,
    searchable: bool = True,
    search_placeholder: str = "Buscar...",
    pagination: bool = False,
    page_size: int = 20,
    height: int = None,
    use_container_width: bool = True,
    hide_index: bool = True,
    key: str = None,
    exportable: bool = True,
    export_filename: str = "datos",
    auto_format: bool = True,
    currency_columns: List[str] = None,
    date_columns: List[str] = None,
    percentage_columns: List[str] = None,
    number_columns: List[str] = None,
) -> pd.DataFrame:
    """
    Renderiza una tabla de datos con estilo premium y funcionalidades avanzadas.

    Args:
        df: DataFrame a mostrar
        title: Título opcional de la tabla
        columns: Lista de columnas a mostrar (None = todas)
        column_config: Configuración personalizada de columnas
        searchable: Habilitar búsqueda global
        search_placeholder: Placeholder del input de búsqueda
        pagination: Habilitar paginación
        page_size: Número de filas por página
        height: Altura de la tabla en pixels
        use_container_width: Usar ancho completo del contenedor
        hide_index: Ocultar índice de filas
        key: Key única para el componente
        exportable: Habilitar exportación
        export_filename: Nombre base del archivo a exportar
        auto_format: Aplicar formateo automático
        currency_columns: Columnas a formatear como moneda
        date_columns: Columnas a formatear como fecha
        percentage_columns: Columnas a formatear como porcentaje
        number_columns: Columnas a formatear como número

    Returns:
        DataFrame filtrado/procesado mostrado en la tabla

    Example:
        >>> render_data_table(
        ...     df,
        ...     title="Transacciones del Mes",
        ...     searchable=True,
        ...     currency_columns=['importe'],
        ...     date_columns=['fecha']
        ... )
    """
    # Validación
    if df is None or df.empty:
        st.info("No hay datos para mostrar")
        return df

    # Copiar DataFrame para no modificar el original
    display_df = df.copy()

    # Filtrar columnas si se especifican
    if columns:
        available_cols = [col for col in columns if col in display_df.columns]
        display_df = display_df[available_cols]

    # === HEADER CON TÍTULO Y ACCIONES ===
    if title or exportable:
        header_col1, header_col2 = st.columns([3, 1])

        with header_col1:
            if title:
                st.markdown(
                    f"""<h3 style='
                        margin: 0;
                        padding: 0;
                        font-size: {Typography.TEXT_XL};
                        font-weight: {Typography.WEIGHT_SEMIBOLD};
                        color: {Colors.GRAY_900};
                    '>{title}</h3>""",
                    unsafe_allow_html=True
                )

        with header_col2:
            if exportable:
                export_cols = st.columns([1, 1])

                with export_cols[0]:
                    csv_data = export_table(display_df, export_filename, 'csv')
                    st.download_button(
                        label="CSV",
                        data=csv_data,
                        file_name=f"{export_filename}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key=f"{key}_export_csv" if key else None
                    )

                with export_cols[1]:
                    excel_data = export_table(display_df, export_filename, 'excel')
                    st.download_button(
                        label="Excel",
                        data=excel_data,
                        file_name=f"{export_filename}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        key=f"{key}_export_excel" if key else None
                    )

        st.markdown(f"<div style='height: {Spacing.MD}'></div>", unsafe_allow_html=True)

    # === BÚSQUEDA GLOBAL ===
    if searchable:
        search_key = f"{key}_search" if key else "data_table_search"
        search_term = st.text_input(
            "Buscar",
            placeholder=search_placeholder,
            label_visibility="collapsed",
            key=search_key
        )

        if search_term:
            # Buscar en todas las columnas de texto
            mask = display_df.astype(str).apply(
                lambda row: row.str.contains(search_term, case=False, na=False).any(),
                axis=1
            )
            display_df = display_df[mask]

            if display_df.empty:
                st.warning(f"No se encontraron resultados para '{search_term}'")
                return display_df

        st.markdown(f"<div style='height: {Spacing.SM}'></div>", unsafe_allow_html=True)

    # === PAGINACIÓN ===
    total_rows = len(display_df)
    current_page = 0

    if pagination and total_rows > page_size:
        total_pages = (total_rows + page_size - 1) // page_size

        pagination_cols = st.columns([1, 2, 1])
        with pagination_cols[1]:
            current_page = st.number_input(
                f"Página (1-{total_pages})",
                min_value=1,
                max_value=total_pages,
                value=1,
                step=1,
                key=f"{key}_page" if key else "data_table_page",
                label_visibility="collapsed"
            ) - 1

        start_idx = current_page * page_size
        end_idx = min(start_idx + page_size, total_rows)
        display_df = display_df.iloc[start_idx:end_idx]

        st.caption(f"Mostrando {start_idx + 1}-{end_idx} de {total_rows} registros")

    # === FORMATEO AUTOMÁTICO ===
    if auto_format:
        display_df = auto_format_dataframe(
            display_df,
            currency_columns=currency_columns,
            date_columns=date_columns,
            percentage_columns=percentage_columns,
            number_columns=number_columns
        )

    # === CONFIGURACIÓN DE COLUMNAS ===
    st_column_config = {}
    if column_config:
        for col_name, col_cfg in column_config.items():
            if isinstance(col_cfg, ColumnConfig):
                st_column_config[col_name] = col_cfg.to_streamlit_config()
            else:
                st_column_config[col_name] = col_cfg

    # === RENDERIZAR TABLA ===
    st.dataframe(
        display_df,
        column_config=st_column_config,
        height=height,
        use_container_width=use_container_width,
        hide_index=hide_index,
        key=f"{key}_dataframe" if key else None
    )

    return display_df


# ========== VARIANTES ESPECIALIZADAS ==========

def render_transaction_table(
    df: pd.DataFrame,
    title: str = "Transacciones",
    on_edit: Callable[[Dict], None] = None,
    on_delete: Callable[[Dict], None] = None,
    on_view: Callable[[Dict], None] = None,
    searchable: bool = True,
    pagination: bool = True,
    page_size: int = 20,
    key: str = None,
    show_actions: bool = True,
) -> pd.DataFrame:
    """
    Tabla especializada para transacciones financieras.

    Incluye formateo automático de:
    - Fecha (DD/MM/YYYY)
    - Importe (moneda €)
    - Colores por tipo (ingreso verde, gasto rojo)

    Args:
        df: DataFrame con transacciones (debe tener: fecha, concepto, importe, tipo)
        title: Título de la tabla
        on_edit: Callback para editar (recibe dict con datos de la fila)
        on_delete: Callback para eliminar (recibe dict con datos de la fila)
        on_view: Callback para ver detalles (recibe dict con datos de la fila)
        searchable: Habilitar búsqueda
        pagination: Habilitar paginación
        page_size: Filas por página
        key: Key única
        show_actions: Mostrar botones de acciones

    Returns:
        DataFrame procesado

    Example:
        >>> render_transaction_table(
        ...     df,
        ...     on_edit=lambda row: edit_transaction(row['id']),
        ...     on_delete=lambda row: delete_transaction(row['id'])
        ... )
    """
    if df is None or df.empty:
        st.info("No hay transacciones para mostrar")
        return df

    # Seleccionar y ordenar columnas relevantes
    display_columns = []
    available_columns = df.columns.tolist()

    # Orden preferido de columnas
    preferred_order = ['fecha', 'concepto', 'importe', 'categoria', 'tipo', 'mes', 'año', 'notas']

    for col in preferred_order:
        if col in available_columns:
            display_columns.append(col)

    # Añadir cualquier otra columna no mencionada
    for col in available_columns:
        if col not in display_columns and col != 'id':
            display_columns.append(col)

    # Configuración de columnas
    column_config = {
        'fecha': st.column_config.DateColumn(
            'Fecha',
            format='DD/MM/YYYY',
            width='medium'
        ),
        'concepto': st.column_config.TextColumn(
            'Concepto',
            width='large',
            help='Descripción de la transacción'
        ),
        'importe': st.column_config.NumberColumn(
            'Importe',
            format='%.2f €',
            width='medium'
        ),
        'categoria': st.column_config.TextColumn(
            'Categoría',
            width='medium'
        ),
        'tipo': st.column_config.TextColumn(
            'Tipo',
            width='small'
        ),
        'notas': st.column_config.TextColumn(
            'Notas',
            width='medium'
        ),
    }

    # === ACCIONES POR FILA ===
    if show_actions and (on_edit or on_delete or on_view):
        st.markdown(
            f"""<div style='
                padding: {Spacing.MD};
                background: {Colors.WARNING_ULTRA_LIGHT};
                border-left: 4px solid {Colors.WARNING};
                border-radius: {BorderRadius.SM};
                margin-bottom: {Spacing.MD};
            '>
                <strong>Acciones:</strong> Selecciona una fila y usa los botones de acción debajo de la tabla.
            </div>""",
            unsafe_allow_html=True
        )

    # Renderizar tabla principal
    result_df = render_data_table(
        df,
        title=title,
        columns=display_columns,
        column_config=column_config,
        searchable=searchable,
        pagination=pagination,
        page_size=page_size,
        key=key,
        exportable=True,
        export_filename="transacciones",
        auto_format=False,  # Ya usamos column_config de Streamlit
    )

    # === BOTONES DE ACCIÓN ===
    if show_actions and (on_edit or on_delete or on_view) and not result_df.empty:
        st.markdown(f"<div style='height: {Spacing.SM}'></div>", unsafe_allow_html=True)

        action_cols = []
        if on_view:
            action_cols.append(1)
        if on_edit:
            action_cols.append(1)
        if on_delete:
            action_cols.append(1)

        cols = st.columns(action_cols + [3])  # Rellenar con espacio vacío

        col_idx = 0

        if on_view and col_idx < len(cols):
            with cols[col_idx]:
                if st.button("Ver Detalles", use_container_width=True, key=f"{key}_view" if key else None):
                    # Por ahora, mostrar la primera fila como ejemplo
                    # En producción, esto podría ser una selección de fila
                    selected_row = result_df.iloc[0].to_dict()
                    on_view(selected_row)
            col_idx += 1

        if on_edit and col_idx < len(cols):
            with cols[col_idx]:
                if st.button("Editar", use_container_width=True, key=f"{key}_edit" if key else None):
                    selected_row = result_df.iloc[0].to_dict()
                    on_edit(selected_row)
            col_idx += 1

        if on_delete and col_idx < len(cols):
            with cols[col_idx]:
                if st.button("Eliminar", use_container_width=True, type="primary", key=f"{key}_delete" if key else None):
                    selected_row = result_df.iloc[0].to_dict()
                    on_delete(selected_row)

    return result_df


def render_summary_table(
    df: pd.DataFrame,
    title: str = "Resumen",
    highlight_totals: bool = True,
    key: str = None,
) -> None:
    """
    Tabla especializada para resúmenes y totales.

    Características:
    - Sin búsqueda ni paginación
    - Resalta totales en la última fila
    - Formateo automático de números grandes
    - Vista compacta

    Args:
        df: DataFrame con resumen (típicamente pocas filas)
        title: Título de la tabla
        highlight_totals: Resaltar última fila como total
        key: Key única

    Example:
        >>> summary_df = pd.DataFrame({
        ...     'Concepto': ['Ingresos', 'Gastos', 'Balance'],
        ...     'Importe': [3000, 2500, 500]
        ... })
        >>> render_summary_table(summary_df, title="Resumen del Mes")
    """
    if df is None or df.empty:
        st.info("No hay datos de resumen")
        return

    # Header
    if title:
        st.markdown(
            f"""<h3 style='
                margin: 0 0 {Spacing.MD} 0;
                font-size: {Typography.TEXT_LG};
                font-weight: {Typography.WEIGHT_SEMIBOLD};
                color: {Colors.GRAY_900};
            '>{title}</h3>""",
            unsafe_allow_html=True
        )

    # Aplicar estilo especial a la última fila si es total
    if highlight_totals and len(df) > 0:
        # Crear copia para aplicar estilos
        styled_df = df.copy()

        # st.dataframe no soporta estilos CSS personalizados por fila
        # Alternativa: usar st.table para tablas pequeñas con mejor estilo
        st.table(styled_df)
    else:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            key=f"{key}_summary" if key else None
        )


def render_compact_table(
    df: pd.DataFrame,
    columns: List[str] = None,
    height: int = 300,
    key: str = None,
) -> None:
    """
    Tabla compacta sin decoraciones para mostrar datos rápidos.

    Características:
    - Sin título, búsqueda, paginación, exportación
    - Altura fija y scroll
    - Máxima simplicidad

    Args:
        df: DataFrame a mostrar
        columns: Columnas a mostrar
        height: Altura en pixels
        key: Key única

    Example:
        >>> render_compact_table(df[['fecha', 'concepto', 'importe']], height=250)
    """
    if df is None or df.empty:
        st.caption("Sin datos")
        return

    display_df = df.copy()

    if columns:
        available_cols = [col for col in columns if col in display_df.columns]
        display_df = display_df[available_cols]

    st.dataframe(
        display_df,
        height=height,
        use_container_width=True,
        hide_index=True,
        key=f"{key}_compact" if key else None
    )


# ========== ROW ACTIONS HELPER ==========

def add_row_actions(
    on_edit: Callable[[int], None] = None,
    on_delete: Callable[[int], None] = None,
    on_view: Callable[[int], None] = None,
    row_id: int = None,
    key_prefix: str = "",
) -> None:
    """
    Renderiza botones de acción para una fila específica.

    Útil cuando se necesita control más granular sobre las acciones por fila.

    Args:
        on_edit: Callback para editar (recibe row_id)
        on_delete: Callback para eliminar (recibe row_id)
        on_view: Callback para ver detalles (recibe row_id)
        row_id: ID de la fila
        key_prefix: Prefijo para las keys de los botones

    Example:
        >>> # En un loop de filas
        >>> for idx, row in df.iterrows():
        ...     st.write(row['concepto'])
        ...     add_row_actions(
        ...         on_edit=lambda: edit_tx(idx),
        ...         on_delete=lambda: delete_tx(idx),
        ...         row_id=idx,
        ...         key_prefix=f"row_{idx}"
        ...     )
    """
    actions = []
    if on_view:
        actions.append(("Ver", on_view, "secondary"))
    if on_edit:
        actions.append(("Editar", on_edit, "secondary"))
    if on_delete:
        actions.append(("Eliminar", on_delete, "primary"))

    if not actions:
        return

    cols = st.columns(len(actions))

    for idx, (label, callback, btn_type) in enumerate(actions):
        with cols[idx]:
            if st.button(
                label,
                key=f"{key_prefix}_action_{label.lower()}_{row_id}",
                type=btn_type,
                use_container_width=True
            ):
                callback(row_id)


# ========== UTILITY: TABLE STATS ==========

def show_table_stats(df: pd.DataFrame, label: str = "Estadísticas") -> None:
    """
    Muestra estadísticas rápidas sobre una tabla de datos.

    Args:
        df: DataFrame
        label: Etiqueta para las estadísticas

    Example:
        >>> show_table_stats(transactions_df, "Transacciones")
        # Muestra: Total filas, columnas, memoria usada
    """
    if df is None or df.empty:
        return

    stats_cols = st.columns(4)

    with stats_cols[0]:
        st.metric(label="Filas", value=f"{len(df):,}")

    with stats_cols[1]:
        st.metric(label="Columnas", value=len(df.columns))

    with stats_cols[2]:
        # Calcular memoria usada
        memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
        st.metric(label="Memoria", value=f"{memory_mb:.2f} MB")

    with stats_cols[3]:
        # Valores nulos
        null_count = df.isnull().sum().sum()
        st.metric(label="Nulos", value=null_count)
