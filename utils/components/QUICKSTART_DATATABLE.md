# DataTable Quick Start

Guía de 5 minutos para empezar a usar el componente DataTable.

## 1. Importar el Componente

```python
from utils.components import render_data_table
```

## 2. Uso Más Simple

```python
# Tienes un DataFrame
df = db_manager.obtener_transacciones(mes=3, año=2024)

# Renderiza la tabla
render_data_table(df)
```

Eso es todo. Ya tienes una tabla funcional.

## 3. Añadir Búsqueda y Exportación

```python
render_data_table(
    df,
    searchable=True,    # Añade búsqueda
    exportable=True,    # Añade botones CSV/Excel
)
```

## 4. Formatear Moneda y Fechas

```python
render_data_table(
    df,
    currency_columns=['importe', 'saldo'],  # Formatea como €
    date_columns=['fecha'],                  # Formatea como DD/MM/YYYY
)
```

## 5. Añadir Paginación

```python
render_data_table(
    df,
    pagination=True,    # Activa paginación
    page_size=20,       # 20 filas por página
)
```

## 6. Todo Junto

```python
from utils.components import render_data_table

df = db_manager.obtener_transacciones(mes=3, año=2024)

render_data_table(
    df,
    title="Transacciones de Marzo",
    searchable=True,
    pagination=True,
    page_size=15,
    exportable=True,
    currency_columns=['importe', 'saldo_posterior'],
    date_columns=['fecha'],
)
```

## Variantes Especializadas

### Tabla de Transacciones

```python
from utils.components import render_transaction_table

render_transaction_table(df)
```

Incluye formateo automático para transacciones financieras.

### Tabla de Resumen

```python
from utils.components import render_summary_table

render_summary_table(df_resumen)
```

Perfecta para mostrar totales y resúmenes.

### Tabla Compacta

```python
from utils.components import render_compact_table

render_compact_table(df, height=250)
```

Ideal para sidebars o widgets pequeños.

## Próximo Paso

Explora más ejemplos en la **página de demo**:

1. Ejecuta: `streamlit run app.py`
2. Navega a: "99 Demo DataTable"
3. Prueba los 5 tabs con ejemplos interactivos

O revisa la **documentación completa**:

- `utils/components/README_DATA_TABLE.md`
- `docs/DATATABLE_INTEGRATION_GUIDE.md`

## Cheat Sheet

```python
# Búsqueda
render_data_table(df, searchable=True)

# Paginación
render_data_table(df, pagination=True, page_size=20)

# Formateo
render_data_table(df,
    currency_columns=['importe'],
    date_columns=['fecha'],
    percentage_columns=['descuento'],
)

# Exportación
render_data_table(df, exportable=True, export_filename="mi_archivo")

# Todo
render_data_table(df,
    title="Mi Tabla",
    searchable=True,
    pagination=True,
    exportable=True,
    currency_columns=['importe'],
    date_columns=['fecha'],
)
```

---

**Tiempo estimado**: 5 minutos para el primer uso
**Nivel**: Principiante
**Fecha**: 2024-12-04
