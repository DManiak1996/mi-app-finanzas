# Guía de Integración del DataTable Component

Esta guía te ayudará a integrar el componente DataTable en las páginas existentes de la aplicación.

## Migración Rápida

### Antes y Después

#### Caso 1: Tabla Simple

**Antes:**
```python
df = db_manager.obtener_transacciones(mes, año)
st.dataframe(df)
```

**Después:**
```python
from utils.components import render_data_table

df = db_manager.obtener_transacciones(mes, año)
render_data_table(
    df,
    title="Transacciones del Mes",
    searchable=True,
    exportable=True,
    currency_columns=['importe', 'saldo_posterior'],
    date_columns=['fecha'],
)
```

**Beneficios:**
- Búsqueda integrada
- Exportación CSV/Excel
- Formateo automático
- Título consistente

---

#### Caso 2: Tabla con Formateo Manual

**Antes:**
```python
df = db_manager.obtener_transacciones(mes, año)
df['importe'] = df['importe'].apply(lambda x: f"{x:.2f} €")
df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%d/%m/%Y')
st.dataframe(df)
```

**Después:**
```python
from utils.components import render_data_table

df = db_manager.obtener_transacciones(mes, año)
render_data_table(
    df,
    currency_columns=['importe'],
    date_columns=['fecha'],
)
```

**Beneficios:**
- Menos código
- Formateo consistente
- No modifica el DataFrame original

---

#### Caso 3: Tabla Grande con Scroll

**Antes:**
```python
df = db_manager.obtener_transacciones()  # Todas las transacciones
st.dataframe(df, height=400)
```

**Después:**
```python
from utils.components import render_data_table

df = db_manager.obtener_transacciones()
render_data_table(
    df,
    pagination=True,
    page_size=20,
    searchable=True,
)
```

**Beneficios:**
- Paginación automática
- Mejor performance
- Búsqueda integrada

---

#### Caso 4: Tabla de Transacciones con Acciones

**Antes:**
```python
df = db_manager.obtener_transacciones(mes, año)
st.dataframe(df)

# Editar transacción
tx_id = st.number_input("ID a editar")
if st.button("Editar"):
    # Lógica de edición
    pass

# Eliminar transacción
if st.button("Eliminar"):
    # Lógica de eliminación
    pass
```

**Después:**
```python
from utils.components import render_transaction_table

def editar_transaccion(row):
    st.session_state['editing_id'] = row['id']
    st.rerun()

def eliminar_transaccion(row):
    if db_manager.eliminar_transaccion(row['id']):
        st.success(f"Transacción {row['concepto']} eliminada")
        st.rerun()

df = db_manager.obtener_transacciones(mes, año)
render_transaction_table(
    df,
    on_edit=editar_transaccion,
    on_delete=eliminar_transaccion,
)
```

**Beneficios:**
- Acciones por fila
- UX mejorado
- Código más limpio

---

## Integración por Página

### app.py (Página Principal)

**Secciones a actualizar:**

1. **Tabla de transacciones del mes**

```python
# Ubicación: Alrededor de línea 500-600
from utils.components import render_transaction_table

# Reemplazar la tabla manual con:
render_transaction_table(
    df_transacciones_mes,
    title=f"Transacciones de {nombre_mes} {año}",
    searchable=True,
    pagination=True,
    page_size=15,
    key="main_transactions"
)
```

2. **Tabla de transacciones pendientes**

```python
from utils.components import render_data_table

render_data_table(
    df_pendientes,
    title="Transacciones Pendientes de Categorizar",
    searchable=True,
    currency_columns=['importe'],
    date_columns=['fecha'],
    key="pending_transactions"
)
```

---

### pages_coche_electrico.py

**Secciones a actualizar:**

1. **Tabla de recargas**

```python
from utils.components import render_data_table

df_recargas = coche_electrico.obtener_recargas()

render_data_table(
    df_recargas,
    title="Historial de Recargas",
    searchable=True,
    pagination=True,
    currency_columns=['coste_total', 'coste_por_kwh'],
    date_columns=['fecha'],
    number_columns=['kwh_cargados', 'km_autonomia'],
    exportable=True,
    export_filename="recargas_coche",
    key="recargas_table"
)
```

2. **Tabla de estadísticas por mes**

```python
from utils.components import render_summary_table, format_currency_column

df_stats = calcular_estadisticas_mensuales()
df_stats = format_currency_column(df_stats, 'Coste Total')
df_stats = format_currency_column(df_stats, 'Coste Promedio')

render_summary_table(
    df_stats,
    title="Estadísticas Mensuales",
    highlight_totals=True,
    key="stats_mensuales"
)
```

---

### Páginas Futuras

#### Página de Presupuestos

```python
from utils.components import render_data_table

df_presupuestos = db_manager.obtener_presupuestos(año)

render_data_table(
    df_presupuestos,
    title="Presupuestos por Categoría",
    searchable=True,
    currency_columns=['presupuesto', 'gastado', 'disponible'],
    percentage_columns=['porcentaje_usado'],
    key="presupuestos_table"
)
```

#### Página de Estadísticas

```python
from utils.components import render_compact_table

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Top Gastos")
    render_compact_table(df_top_gastos, height=250)

with col2:
    st.subheader("Top Categorías")
    render_compact_table(df_top_categorias, height=250)

with col3:
    st.subheader("Tendencias")
    render_compact_table(df_tendencias, height=250)
```

---

## Patrones Comunes

### Patrón 1: Tabla con Búsqueda y Export

Ideal para listados generales.

```python
from utils.components import render_data_table

render_data_table(
    df,
    title="Título de la Tabla",
    searchable=True,
    exportable=True,
    export_filename="nombre_archivo",
    currency_columns=['columnas', 'de', 'moneda'],
    date_columns=['columnas', 'de', 'fecha'],
)
```

---

### Patrón 2: Tabla Grande con Paginación

Para tablas con más de 50 filas.

```python
from utils.components import render_data_table

render_data_table(
    df,
    title="Tabla Grande",
    searchable=True,
    pagination=True,
    page_size=20,
    height=500,
)
```

---

### Patrón 3: Tabla Compacta en Sidebar

Para widgets en el sidebar.

```python
from utils.components import render_compact_table

with st.sidebar:
    st.subheader("Resumen Rápido")
    render_compact_table(
        df[['concepto', 'importe']].head(5),
        height=200,
        key="sidebar_compact"
    )
```

---

### Patrón 4: Tabla de Resumen con Totales

Para resúmenes financieros.

```python
from utils.components import render_summary_table, format_currency_column

# Preparar datos con fila de totales
df_resumen = calcular_resumen()
totales = calcular_totales()
df_resumen = pd.concat([df_resumen, pd.DataFrame([totales])], ignore_index=True)

# Formatear
df_resumen = format_currency_column(df_resumen, 'Total')

render_summary_table(
    df_resumen,
    title="Resumen del Período",
    highlight_totals=True,
)
```

---

### Patrón 5: Tabla con Acciones CRUD

Para tablas donde se puede editar/eliminar.

```python
from utils.components import render_transaction_table

def on_edit(row):
    st.session_state['editing_row'] = row
    st.rerun()

def on_delete(row):
    if st.session_state.get('confirm_delete') == row['id']:
        db_manager.eliminar(row['id'])
        st.success("Eliminado correctamente")
        del st.session_state['confirm_delete']
        st.rerun()
    else:
        st.session_state['confirm_delete'] = row['id']
        st.warning("Haz clic de nuevo para confirmar")

render_transaction_table(
    df,
    on_edit=on_edit,
    on_delete=on_delete,
)
```

---

## Configuración Avanzada

### Configurar Columnas Específicas

```python
from utils.components import render_data_table, ColumnConfig

column_config = {
    'fecha': ColumnConfig(
        label='Fecha Transacción',
        width='medium',
        help='Fecha en que se realizó la transacción'
    ),
    'importe': ColumnConfig(
        label='Importe Total',
        width='small',
    ),
    'notas': ColumnConfig(
        label='Observaciones',
        width='large',
    ),
}

render_data_table(
    df,
    column_config=column_config,
)
```

---

### Formateo Manual Avanzado

Si necesitas formateo más específico:

```python
from utils.components import (
    format_currency_column,
    format_date_column,
    format_percentage_column,
    render_data_table
)

# Formatear manualmente antes de renderizar
df_formatted = df.copy()
df_formatted = format_currency_column(df_formatted, 'importe')
df_formatted = format_date_column(df_formatted, 'fecha', format='%d/%m/%Y')
df_formatted = format_percentage_column(df_formatted, 'descuento', decimals=2)

render_data_table(
    df_formatted,
    auto_format=False,  # Desactivar formateo automático
)
```

---

### Exportación Personalizada

```python
from utils.components import export_table

# Preparar DataFrame
df_export = df[['fecha', 'concepto', 'importe', 'categoria']]

# Exportar
col1, col2 = st.columns(2)

with col1:
    csv_data = export_table(df_export, 'transacciones', 'csv')
    st.download_button(
        "📥 Descargar CSV",
        data=csv_data,
        file_name=f"transacciones_{mes}_{año}.csv",
        mime="text/csv",
    )

with col2:
    excel_data = export_table(df_export, 'transacciones', 'excel')
    st.download_button(
        "📥 Descargar Excel",
        data=excel_data,
        file_name=f"transacciones_{mes}_{año}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
```

---

## Checklist de Integración

Para cada página que integres el DataTable, verifica:

- [ ] Importar el componente correcto (render_data_table, render_transaction_table, etc.)
- [ ] Especificar currency_columns para columnas de dinero
- [ ] Especificar date_columns para columnas de fecha
- [ ] Añadir title descriptivo
- [ ] Habilitar searchable si la tabla tiene >10 filas
- [ ] Habilitar pagination si la tabla tiene >50 filas
- [ ] Añadir export si los usuarios pueden necesitar los datos
- [ ] Usar key única para evitar conflictos de estado
- [ ] Añadir callbacks (on_edit, on_delete) si aplica
- [ ] Probar en móvil para verificar responsive

---

## Troubleshooting

### La tabla no se muestra

**Posible causa**: DataFrame vacío o None

**Solución**:
```python
if df is None or df.empty:
    st.info("No hay datos para mostrar")
else:
    render_data_table(df, ...)
```

---

### Los números no se formatean correctamente

**Posible causa**: Columna no es numérica

**Solución**:
```python
# Convertir a numérico antes de formatear
df['importe'] = pd.to_numeric(df['importe'], errors='coerce')

render_data_table(df, currency_columns=['importe'])
```

---

### Las fechas no se formatean

**Posible causa**: Columna no es datetime

**Solución**:
```python
# Convertir a datetime antes de formatear
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

render_data_table(df, date_columns=['fecha'])
```

---

### Error de key duplicada

**Posible causa**: Múltiples tablas sin key única

**Solución**:
```python
# Añadir key única a cada tabla
render_data_table(df1, key="tabla1")
render_data_table(df2, key="tabla2")
```

---

### Los callbacks no funcionan

**Posible causa**: Función mal definida

**Solución**:
```python
# Asegurarse de que la función recibe el parámetro row
def on_edit(row):  # ✅ Correcto - recibe row
    print(row['id'])

def on_edit():  # ❌ Incorrecto - no recibe row
    print("hola")

render_transaction_table(df, on_edit=on_edit)
```

---

## Recursos Adicionales

- **Documentación Completa**: `utils/components/README_DATA_TABLE.md`
- **Ejemplos de Código**: `utils/components/data_table_examples.py`
- **Tests**: `utils/components/data_table_test.py`
- **Página de Demo**: Ejecutar app y navegar a "99 Demo DataTable"
- **Design Tokens**: `utils/design_tokens.py`
- **Estrategia de Diseño**: `docs/ESTRATEGIA_OVERHAUL_DISEÑO.md`

---

## Soporte

Si tienes problemas integrando el componente:

1. Revisa los ejemplos en `data_table_examples.py`
2. Verifica la página de demo (99_Demo_DataTable.py)
3. Consulta el README completo
4. Revisa los tests para ver casos específicos

---

**Última actualización**: 2024-12-04
**Versión del componente**: 1.0.0
