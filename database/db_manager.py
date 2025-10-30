
# database/db_manager.py

import sqlite3
from .models import ALL_TABLES

DB_NAME = 'finanzas.db'

def get_db_connection():
    """Establece la conexión con la base de datos."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tablas():
    """Crea todas las tablas en la base de datos si no existen."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for tabla_sql in ALL_TABLES:
            cursor.execute(tabla_sql)
        conn.commit()
        print("Tablas creadas exitosamente o ya existentes.")
    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")
    finally:
        conn.close()

def insertar_transaccion(fecha, concepto, importe, categoria, tipo, mes, año, notas='', saldo_posterior=None):
    """Inserta una nueva transacción en la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO transacciones (fecha, concepto, importe, categoria, tipo, mes, año, notas, saldo_posterior)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (fecha, concepto, importe, categoria, tipo, mes, año, notas, saldo_posterior))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al insertar transacción: {e}")
        return None
    finally:
        conn.close()

def obtener_transacciones(mes=None, año=None):
    """Obtiene transacciones, opcionalmente filtradas por mes y año."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM transacciones "
    params = []
    where_clauses = []
    if mes:
        where_clauses.append("mes = ?")
        params.append(mes)
    if año:
        where_clauses.append("año = ?")
        params.append(año)
    
    if where_clauses:
        query += "WHERE " + " AND ".join(where_clauses)
    query += " ORDER BY fecha DESC"
    
    cursor.execute(query, params)
    transacciones = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return transacciones

def actualizar_transaccion(id_transaccion, campos_a_actualizar):
    """Actualiza uno o más campos de una transacción existente."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener la transacción original para comparar
    cursor.execute("SELECT * FROM transacciones WHERE id = ?", (id_transaccion,))
    transaccion_original = dict(cursor.fetchone())

    # Filtrar solo los campos que realmente han cambiado
    campos_reales_a_actualizar = {}
    for key, value in campos_a_actualizar.items():
        if key in transaccion_original and transaccion_original[key] != value:
            campos_reales_a_actualizar[key] = value

    if not campos_reales_a_actualizar:
        return True # No hay nada que actualizar, se considera un éxito

    set_clause = ", ".join([f"{key} = ?" for key in campos_a_actualizar.keys()])
    params = list(campos_a_actualizar.values()) + [id_transaccion]
    query = f"UPDATE transacciones SET {set_clause} WHERE id = ?"
    
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error al actualizar transacción: {e}")
        return False
    finally:
        conn.close()

def eliminar_transaccion(id_transaccion):
    """Elimina una transacción de la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transacciones WHERE id = ?", (id_transaccion,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error al eliminar transacción: {e}")
        return False
    finally:
        conn.close()

def transaccion_existe(fecha, importe):
    """Verifica si ya existe una transacción con la misma fecha e importe."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Usamos LIMIT 1 para que la consulta sea más rápida, se detiene al encontrar la primera coincidencia.
        cursor.execute("SELECT 1 FROM transacciones WHERE fecha = ? AND importe = ? LIMIT 1", (fecha, importe))
        existe = cursor.fetchone() is not None
        return existe
    except sqlite3.Error as e:
        print(f"Error al verificar si la transacción existe: {e}")
        return False # En caso de error, asumimos que no existe para no bloquear la importación.
    finally:
        conn.close()

def obtener_transacciones_por_periodo(fecha_inicio, fecha_fin):
    """Obtiene todas las transacciones en un rango de fechas."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacciones WHERE fecha BETWEEN ? AND ? ORDER BY fecha DESC", (fecha_inicio, fecha_fin))
    transacciones = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return transacciones

def obtener_totales_por_categoria(mes, año):
    """Calcula la suma de importes por categoría, filtrando por mes y/o año."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT categoria, SUM(importe) as total
        FROM transacciones
        WHERE tipo = 'GASTO' 
    """
    params = []
    if mes:
        query += " AND mes = ?"
        params.append(mes)
    if año:
        query += " AND año = ?"
        params.append(año)
    query += """
        GROUP BY categoria
    """
    cursor.execute(query, tuple(params))
    totales = {row['categoria']: row['total'] for row in cursor.fetchall()}
    conn.close()
    return totales

def buscar_transacciones(termino_busqueda):
    """Busca transacciones cuyo concepto contenga un término de búsqueda."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacciones WHERE concepto LIKE ? ORDER BY fecha DESC", (f'%{termino_busqueda}%',))
    transacciones = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return transacciones

def resetear_base_de_datos():
    """Elimina todas las tablas y las vuelve a crear, limpiando la base de datos."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.executescript("""DROP TABLE IF EXISTS transacciones;""")
        crear_tablas()
        conn.close()
    except Exception as e:
        print(f"Error al resetear la base de datos: {e}")

def calcular_balance_total():
    """Calcula la suma total de todos los importes en la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(importe) FROM transacciones")
        resultado = cursor.fetchone()[0]
        return resultado if resultado is not None else 0.0
    except sqlite3.Error as e:
        print(f"Error al calcular el balance total: {e}")
        return 0.0
    finally:
        conn.close()

def obtener_ultimo_saldo():
    """Obtiene el saldo_posterior de la transacción más reciente."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT saldo_posterior FROM transacciones ORDER BY fecha DESC, id DESC LIMIT 1")
        resultado = cursor.fetchone()
        return resultado['saldo_posterior'] if resultado and resultado['saldo_posterior'] is not None else 0.0
    except (sqlite3.Error, TypeError) as e:
        print(f"Error al obtener el último saldo: {e}")
        return 0.0
    finally:
        conn.close()
