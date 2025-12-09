# DataTable Component

Componente de tabla reutilizable con estilo premium y funcionalidades avanzadas para la aplicación de finanzas.

## Características

- **Formateo Inteligente**: Moneda (€), fechas (DD/MM/YYYY), porcentajes (%), números con separadores
- **Búsqueda Global**: Busca en todas las columnas con filtrado en tiempo real
- **Paginación**: Control de filas por página para tablas grandes
- **Ordenamiento**: Click en headers para ordenar (nativo de Streamlit)
- **Exportación**: Descarga en CSV y Excel
- **Acciones por Fila**: Botones para editar, eliminar, ver detalles
- **Variantes Especializadas**: Tablas para transacciones, resúmenes, vistas compactas
- **Performance**: Optimizado para DataFrames grandes
- **Responsive**: Scroll horizontal automático en móviles

## Instalación

El componente ya está incluido en el proyecto. Solo necesitas importarlo:

```python
from utils.components.data_table import render_data_table, render_transaction_table
```

O importar todo el paquete:

```python
from utils.components import (
    render_data_table,
    render_transaction_table,
    render_summary_table,
    render_compact_table,
    format_currency_column,
    format_date_column,
)
```

## Uso Básico

### Tabla Simple

```python
import pandas as pd
from utils.components import render_data_table

# Preparar datos
df = pd.DataFrame({
    'fecha': pd.date_range('2024-01-01', periods=10),
    'concepto': ['Transacción ' + str(i) for i in range(10)],
    'importe': [100.50, 200.75, 150.00, ...],
})

# Renderizar tabla con formateo automático
render_data_table(
    df,
    title="Mis Transacciones",
    searchable=True,
    pagination=True,
    page_size=10,
    currency_columns=['importe'],
    date_columns=['fecha'],
)
```

### Tabla de Transacciones con Acciones

```python
from utils.components import render_transaction_table

def editar_transaccion(row):
    st.session_state['editing_id'] = row['id']
    st.rerun()

def eliminar_transaccion(row):
    db_manager.eliminar_transaccion(row['id'])
    st.success(f"Transacción {row['concepto']} eliminada")
    st.rerun()

render_transaction_table(
    df,
    title="Transacciones del Mes",
    on_edit=editar_transaccion,
    on_delete=eliminar_transaccion,
    searchable=True,
    pagination=True,
)
```

### Tabla de Resumen

```python
from utils.components import render_summary_table

# Crear resumen
resumen = pd.DataFrame({
    'Concepto': ['Total Ingresos', 'Total Gastos', 'Balance'],
    'Enero': [3000, 2400, 600],
    'Febrero': [3200, 2600, 600],
    'Total': [6200, 5000, 1200],
})

render_summary_table(
    resumen,
    title="Resumen Financiero",
    highlight_totals=True,
)
```

### Tabla Compacta

```python
from utils.components import render_compact_table

# Útil para widgets laterales o tarjetas pequeñas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Últimas Transacciones")
    render_compact_table(df.tail(5), height=200)

with col2:
    st.subheader("Top Gastos")
    render_compact_table(top_gastos_df, height=200)
```

## API Reference

### `render_data_table()`

Función principal para renderizar tablas con todas las funcionalidades.

**Parámetros:**

- `df` (pd.DataFrame): DataFrame a mostrar
- `title` (str, optional): Título de la tabla
- `columns` (List[str], optional): Columnas a mostrar (None = todas)
- `column_config` (Dict, optional): Configuración de columnas
- `searchable` (bool): Habilitar búsqueda (default: True)
- `search_placeholder` (str): Placeholder del input de búsqueda
- `pagination` (bool): Habilitar paginación (default: False)
- `page_size` (int): Filas por página (default: 20)
- `height` (int, optional): Altura en pixels
- `use_container_width` (bool): Usar ancho completo (default: True)
- `hide_index` (bool): Ocultar índice (default: True)
- `key` (str, optional): Key única para Streamlit
- `exportable` (bool): Habilitar exportación (default: True)
- `export_filename` (str): Nombre base del archivo (default: "datos")
- `auto_format` (bool): Aplicar formateo automático (default: True)
- `currency_columns` (List[str], optional): Columnas a formatear como moneda
- `date_columns` (List[str], optional): Columnas a formatear como fecha
- `percentage_columns` (List[str], optional): Columnas a formatear como porcentaje
- `number_columns` (List[str], optional): Columnas a formatear como número

**Retorna:** DataFrame filtrado/procesado

### `render_transaction_table()`

Tabla especializada para transacciones financieras.

**Parámetros:**

- `df` (pd.DataFrame): DataFrame con transacciones
- `title` (str): Título (default: "Transacciones")
- `on_edit` (Callable, optional): Callback para editar
- `on_delete` (Callable, optional): Callback para eliminar
- `on_view` (Callable, optional): Callback para ver detalles
- `searchable` (bool): Habilitar búsqueda (default: True)
- `pagination` (bool): Habilitar paginación (default: True)
- `page_size` (int): Filas por página (default: 20)
- `key` (str, optional): Key única
- `show_actions` (bool): Mostrar botones de acciones (default: True)

**Retorna:** DataFrame procesado

### `render_summary_table()`

Tabla para resúmenes y totales.

**Parámetros:**

- `df` (pd.DataFrame): DataFrame con resumen
- `title` (str): Título (default: "Resumen")
- `highlight_totals` (bool): Resaltar última fila (default: True)
- `key` (str, optional): Key única

### `render_compact_table()`

Tabla compacta sin decoraciones.

**Parámetros:**

- `df` (pd.DataFrame): DataFrame a mostrar
- `columns` (List[str], optional): Columnas a mostrar
- `height` (int): Altura en pixels (default: 300)
- `key` (str, optional): Key única

## Funciones de Formateo

### `format_currency_column(df, column, symbol='€')`

Formatea una columna como moneda.

```python
df = format_currency_column(df, 'importe')
# 1234.56 → 1,234.56 €
```

### `format_date_column(df, column, format='%d/%m/%Y')`

Formatea una columna de fechas.

```python
df = format_date_column(df, 'fecha')
# 2024-03-15 → 15/03/2024
```

### `format_percentage_column(df, column, decimals=1)`

Formatea una columna como porcentaje.

```python
df = format_percentage_column(df, 'descuento')
# 0.15 → 15.0%
```

### `format_number_column(df, column, decimals=2)`

Formatea una columna numérica con separadores.

```python
df = format_number_column(df, 'cantidad')
# 1234.56 → 1,234.56
```

### `auto_format_dataframe(df, currency_columns, date_columns, percentage_columns, number_columns)`

Aplica formateo automático a múltiples columnas.

```python
df_formatted = auto_format_dataframe(
    df,
    currency_columns=['importe', 'saldo'],
    date_columns=['fecha', 'fecha_pago'],
    percentage_columns=['descuento'],
    number_columns=['cantidad'],
)
```

## Exportación

### `export_table(df, filename, format='csv')`

Exporta DataFrame a CSV o Excel.

```python
# CSV
csv_data = export_table(df, 'transacciones', 'csv')
st.download_button("Descargar CSV", csv_data, "transacciones.csv")

# Excel
excel_data = export_table(df, 'transacciones', 'excel')
st.download_button("Descargar Excel", excel_data, "transacciones.xlsx")
```

## Helpers

### `add_row_actions(on_edit, on_delete, on_view, row_id, key_prefix)`

Renderiza botones de acción para una fila específica.

```python
for idx, row in df.iterrows():
    st.write(row['concepto'])
    add_row_actions(
        on_edit=lambda: edit_tx(idx),
        on_delete=lambda: delete_tx(idx),
        row_id=idx,
        key_prefix=f"row_{idx}"
    )
```

### `show_table_stats(df, label='Estadísticas')`

Muestra estadísticas sobre la tabla.

```python
show_table_stats(df, "Datos de Transacciones")
# Muestra: Filas, Columnas, Memoria, Valores Nulos
```

## Ejemplos Completos

Ver el archivo `data_table_examples.py` para ejemplos completos y ejecutables de todas las funcionalidades.

Para ejecutar los ejemplos:

```bash
streamlit run utils/components/data_table_examples.py
```

## Integración con el Design System

El componente usa los tokens de diseño definidos en `utils/design_tokens.py`:

- Colores semánticos (SUCCESS, ERROR, WARNING, etc.)
- Tipografía consistente
- Spacing estandarizado
- Border radius y transiciones

Esto garantiza que todas las tablas tengan un aspecto consistente con el resto de la aplicación.

## Performance

El componente está optimizado para tablas grandes:

- Paginación para evitar renderizar miles de filas
- Búsqueda eficiente usando pandas vectorizado
- Formateo lazy (solo se formatea lo que se muestra)
- Export streaming para archivos grandes

**Recomendaciones:**

- Para más de 100 filas, usa `pagination=True`
- Para más de 1000 filas, considera filtrar en la BD antes de pasar a la tabla
- Usa `height` para limitar el scroll vertical
- Selecciona solo las columnas necesarias con el parámetro `columns`

## Responsive Design

La tabla es completamente responsive:

- **Desktop**: Ancho completo con todas las columnas visibles
- **Tablet**: Scroll horizontal automático
- **Mobile**: Scroll horizontal + columnas optimizadas

Streamlit maneja esto automáticamente con `use_container_width=True`.

## Testing

Para ejecutar los tests del componente:

```bash
python3 utils/components/data_table_test.py
```

Los tests verifican:
- Formateo de moneda, fechas, porcentajes, números
- Exportación CSV y Excel
- Manejo de valores nulos
- Columnas inexistentes
- DataFrames vacíos

## Troubleshooting

### La búsqueda no funciona

Asegúrate de que el parámetro `searchable=True` y que el DataFrame no esté vacío.

### Los números no se formatean

Verifica que la columna sea de tipo numérico (`float` o `int`). Usa `df['columna'] = pd.to_numeric(df['columna'])` si es necesario.

### Las fechas no se formatean

Asegúrate de que la columna sea de tipo `datetime`. Usa `df['fecha'] = pd.to_datetime(df['fecha'])` si es necesario.

### La paginación no aparece

La paginación solo se muestra si `len(df) > page_size`. Verifica que tu DataFrame tenga suficientes filas.

### Los botones de acción no funcionan

Asegúrate de pasar funciones válidas a `on_edit`, `on_delete`, etc. Las funciones deben recibir un diccionario con los datos de la fila.

## Contribuir

Si encuentras bugs o quieres añadir features:

1. Edita `utils/components/data_table.py`
2. Añade tests en `utils/components/data_table_test.py`
3. Añade ejemplos en `utils/components/data_table_examples.py`
4. Actualiza este README

## Roadmap

Features planificadas:

- [ ] Selección múltiple de filas con checkboxes
- [ ] Edición inline de celdas
- [ ] Filtros avanzados por columna
- [ ] Columnas sticky (fijas en scroll horizontal)
- [ ] Agrupación y subtotales
- [ ] Gráficos inline en celdas
- [ ] Modo dark theme
- [ ] Exportación a PDF

## Licencia

Este componente es parte de la aplicación de finanzas y sigue la misma licencia del proyecto principal.

## Soporte

Para preguntas o problemas, contacta al equipo de desarrollo.

---

**Última actualización:** 2024-12-04
**Versión:** 1.0.0
**Autor:** Daniel (Desarrollador principal)
