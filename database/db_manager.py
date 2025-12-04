
# database/db_manager.py

import sqlite3
import uuid
import os
from datetime import datetime
from .models import ALL_TABLES

# Obtener la ruta absoluta al directorio database
DB_NAME = "/Users/daniel/Library/Mobile Documents/com~apple~CloudDocs/Finanzas/finanzas.db"

def generar_uuid():
    """Genera un UUID único para usar como ID de transacción."""
    return str(uuid.uuid4())

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

def insertar_transaccion(fecha, concepto, importe, categoria, tipo, mes, año, notas='', saldo_posterior=None, id=None):
    """Inserta una nueva transacción en la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Generar UUID si no se proporciona (para sincronización)
        if id is None:
            id = generar_uuid()

        cursor.execute("""
            INSERT INTO transacciones (id, fecha, concepto, importe, categoria, tipo, mes, año, notas, saldo_posterior)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id, fecha, concepto, importe, categoria, tipo, mes, año, notas, saldo_posterior))
        conn.commit()
        return id
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

def obtener_gastos_netos_por_categoria(mes, año):
    """
    Calcula la suma de importes NETOS por categoría (gastos - reembolsos asignados).

    Los reembolsos asignados a una categoría específica tienen el formato:
    - categoria = 'REEMBOLSO'
    - tipo = 'INGRESO'
    - notas = 'REEMBOLSO_DE:{nombre_categoria}'

    Args:
        mes: Mes (1-12)
        año: Año

    Returns:
        Dict con {categoria: importe_neto} (valores negativos)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query para obtener gastos brutos y reembolsos por categoría
    cursor.execute("""
        WITH gastos_brutos AS (
            SELECT
                categoria,
                SUM(importe) as total_bruto
            FROM transacciones
            WHERE tipo = 'GASTO'
                AND mes = ?
                AND año = ?
            GROUP BY categoria
        ),
        reembolsos_categoria AS (
            SELECT
                REPLACE(notas, 'REEMBOLSO_DE:', '') as categoria,
                SUM(importe) as total_reembolsos
            FROM transacciones
            WHERE categoria = 'REEMBOLSO'
                AND tipo = 'INGRESO'
                AND mes = ?
                AND año = ?
                AND notas LIKE 'REEMBOLSO_DE:%'
            GROUP BY notas
        )
        SELECT
            g.categoria,
            g.total_bruto,
            COALESCE(r.total_reembolsos, 0) as reembolsos,
            g.total_bruto + COALESCE(r.total_reembolsos, 0) as total_neto
        FROM gastos_brutos g
        LEFT JOIN reembolsos_categoria r ON g.categoria = r.categoria
    """, (mes, año, mes, año))

    # Crear diccionario con totales netos
    # Nota: total_bruto es negativo, total_reembolsos es positivo
    # total_neto = total_bruto + total_reembolsos (resultado más cercano a 0)
    totales_netos = {row['categoria']: row['total_neto'] for row in cursor.fetchall()}

    conn.close()
    return totales_netos

def buscar_transacciones(termino_busqueda):
    """Busca transacciones cuyo concepto contenga un término de búsqueda."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacciones WHERE concepto LIKE ? ORDER BY fecha DESC", (f'%{termino_busqueda}%',))
    transacciones = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return transacciones

def resetear_base_de_datos():
    """Elimina TODAS las tablas y las vuelve a crear, limpiando completamente la base de datos."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Eliminar TODAS las tablas
        cursor.executescript("""
            DROP TABLE IF EXISTS transacciones;
            DROP TABLE IF EXISTS custom_categories;
            DROP TABLE IF EXISTS classification_rules;
            DROP TABLE IF EXISTS facturas_electricidad;
            DROP TABLE IF EXISTS recargas_coche;
        """)

        # Recrear todas las tablas
        crear_tablas()
        conn.close()
        print("✅ Base de datos reseteada completamente (transacciones + recargas + facturas)")
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
    """
    Obtiene el saldo total acumulado sumando todos los importes.
    Esta es la forma más confiable ya que no depende del campo saldo_posterior
    que puede estar NULL en algunas transacciones.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(importe) as saldo_total FROM transacciones")
        resultado = cursor.fetchone()
        return resultado['saldo_total'] if resultado and resultado['saldo_total'] is not None else 0.0
    except (sqlite3.Error, TypeError) as e:
        print(f"Error al obtener el último saldo: {e}")
        return 0.0
    finally:
        conn.close()


# ========== FUNCIONES COCHE ELÉCTRICO ==========

def insertar_recarga_coche(
    fecha_recarga, bateria_inicial, bateria_final, kwh_cargados,
    km_recorridos, consumo_medio, franja_horaria, tarifa_kwh,
    coste_energia, coste_potencia, coste_alquiler, coste_bono, coste_servicios,
    impuesto_electricidad, iva, coste_total, mes, año, categoria='COCHE_ELECTRICO', notas=''
):
    """
    Inserta una nueva recarga de coche eléctrico en la BD.
    La recarga queda como PENDIENTE (no afecta liquidez hasta que se marque como pagada).

    Returns:
        id_recarga si tiene éxito, None si falla
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Generar ID de recarga
        id_recarga = generar_uuid()

        # Convertir fecha_recarga a string si es necesario
        if hasattr(fecha_recarga, 'isoformat'):
            fecha_recarga_str = fecha_recarga.isoformat()
        else:
            fecha_recarga_str = str(fecha_recarga)

        # Insertar en tabla recargas_coche (SIN crear transacción todavía)
        cursor.execute("""
            INSERT INTO recargas_coche (
                id, fecha_recarga, bateria_inicial, bateria_final, kwh_cargados,
                km_recorridos, consumo_medio, franja_horaria, tarifa_kwh,
                coste_energia, coste_potencia, coste_alquiler, coste_bono, coste_servicios,
                impuesto_electricidad, iva, coste_total,
                mes, año, pagado, categoria, notas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_recarga, fecha_recarga_str, bateria_inicial, bateria_final, kwh_cargados,
            km_recorridos, consumo_medio, franja_horaria, tarifa_kwh,
            coste_energia, coste_potencia, coste_alquiler, coste_bono, coste_servicios,
            impuesto_electricidad, iva, coste_total,
            mes, año, 0,  # pagado = 0 (pendiente)
            categoria, notas
        ))

        conn.commit()
        return id_recarga

    except sqlite3.Error as e:
        import traceback
        print(f"Error al insertar recarga: {e}")
        print(f"Detalles completos del error:")
        traceback.print_exc()
        print(f"Valores que se intentaron insertar:")
        print(f"  fecha_recarga_str: {fecha_recarga_str} (tipo: {type(fecha_recarga_str)})")
        print(f"  mes: {mes} (tipo: {type(mes)})")
        print(f"  año: {año} (tipo: {type(año)})")
        conn.rollback()
        return None
    finally:
        conn.close()


def obtener_recargas(mes=None, año=None, limit=None):
    """
    Obtiene recargas del coche, opcionalmente filtradas por mes/año.

    Args:
        mes: Mes (1-12) opcional
        año: Año opcional
        limit: Número máximo de resultados

    Returns:
        Lista de diccionarios con datos de recargas
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM recargas_coche"
    params = []
    where_clauses = []

    if mes:
        where_clauses.append("mes = ?")
        params.append(mes)
    if año:
        where_clauses.append("año = ?")
        params.append(año)

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    query += " ORDER BY fecha_recarga DESC"

    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query, params)
    recargas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return recargas


def obtener_ultima_recarga():
    """Obtiene la recarga más reciente."""
    recargas = obtener_recargas(limit=1)
    return recargas[0] if recargas else None


def obtener_estadisticas_recargas_mes(mes, año):
    """
    Obtiene estadísticas agregadas de recargas de un mes específico.

    Returns:
        Dict con totales y promedios
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                COUNT(*) as total_recargas,
                SUM(kwh_cargados) as kwh_totales,
                SUM(km_recorridos) as km_totales,
                SUM(coste_total) as coste_total,
                AVG(consumo_medio) as consumo_promedio,
                AVG(coste_total) as coste_promedio_recarga
            FROM recargas_coche
            WHERE mes = ? AND año = ?
        """, (mes, año))

        resultado = cursor.fetchone()

        if resultado and resultado['total_recargas'] > 0:
            return dict(resultado)
        else:
            return {
                'total_recargas': 0,
                'kwh_totales': 0,
                'km_totales': 0,
                'coste_total': 0,
                'consumo_promedio': 0,
                'coste_promedio_recarga': 0
            }
    finally:
        conn.close()


def insertar_factura_electricidad(
    mes, año, fecha_factura,
    consumo_punta_kwh, consumo_llano_kwh, consumo_valle_kwh,
    tarifa_punta, tarifa_llano, tarifa_valle,
    potencia, alquiler_contador, bono_social, servicios,
    energia_generada=0, energia_exportada=0, precio_compensacion=0.07,
    excedentes_kwh=0, excedentes_compensacion=0, notas=''
):
    """
    Inserta una nueva factura de electricidad en la BD.
    Calcula automáticamente todos los totales e impuestos siguiendo la estructura de Iberdrola:

    ESTRUCTURA:
    1. ENERGÍA: Coste consumo por franjas + Potencia + Bono social + Compensación excedentes
    2. CARGOS NORMATIVOS: Impuesto electricidad (5,11%) sobre energía
    3. SERVICIOS: Alquiler contador
    4. IMPORTE TOTAL: Suma de energía + cargos + servicios
    5. IVA: 21% sobre importe total
    6. TOTAL FACTURA: Importe total + IVA

    Returns:
        ID de la factura si tiene éxito, None si falla
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. CONSUMO DE LA RED (ya desagregado por franjas - lo que se factura)
        consumo_red_kwh = consumo_punta_kwh + consumo_llano_kwh + consumo_valle_kwh

        # 2. CALCULAR AUTOCONSUMO Y COMPENSACIÓN
        # Si se proporciona energía_generada y energía_exportada, calcula automáticamente el autoconsumo
        if energia_generada > 0:
            energia_autoconsumida = energia_generada - energia_exportada
            # Calcular compensación real: energía_exportada × precio_compensacion
            if energia_exportada > 0:
                excedentes_compensacion = -(energia_exportada * precio_compensacion)
        else:
            energia_autoconsumida = 0

        # 3. CONSUMO TOTAL DEL HOGAR (para porcentaje del coche)
        # Red + Autoconsumo = Total disponible en el hogar
        consumo_total_kwh = consumo_red_kwh + energia_autoconsumida

        # 4. CALCULAR COSTE DE ENERGÍA POR FRANJA (basado en consumo de RED)
        # Los consumos ya están desglosados por franja (red)
        coste_energia_consumo = (
            consumo_punta_kwh * tarifa_punta +
            consumo_llano_kwh * tarifa_llano +
            consumo_valle_kwh * tarifa_valle
        )

        # 5. SECCIÓN ENERGÍA (según Iberdrola)
        # Incluye: coste consumo + potencia + bono social + compensación excedentes
        energia_consumo = coste_energia_consumo
        energia_potencia = potencia
        energia_bono = bono_social
        energia_compensacion = excedentes_compensacion  # Valor negativo reduce la factura

        total_energia = energia_consumo + energia_potencia + energia_bono + energia_compensacion

        # 6. CARGOS NORMATIVOS (Impuesto electricidad)
        # Se aplica sobre el total de energía
        impuesto_electricidad = total_energia * 0.0511269632

        # 7. SERVICIOS Y OTROS (Solo alquiler contador)
        # En Iberdrola, "SERVICIOS Y OTROS CONCEPTOS" = Alquiler de equipos de medida
        servicios_total = alquiler_contador

        # 8. IMPORTE TOTAL (antes de IVA)
        importe_total = total_energia + impuesto_electricidad + servicios_total

        # 9. IVA (21% sobre importe total)
        iva = importe_total * 0.21

        # 10. TOTAL FACTURA
        total_factura = importe_total + iva

        # 11. Obtener recargas del mes para calcular participación del coche
        estadisticas_coche = obtener_estadisticas_recargas_mes(mes, año)
        kwh_coche_mes = estadisticas_coche['kwh_totales']
        coste_coche_mes = estadisticas_coche['coste_total']  # Coste REAL de las recargas

        # IMPORTANTE: Porcentaje del coche basado en COSTE REAL, no en kWh teórico
        # Razón: El coche puede cargar en franjas más baratas (ej: valle)
        # mientras que la factura incluye franjas más caras (ej: punta)
        # Por tanto, el coste real del coche es diferente al porcentaje teórico de kWh
        porcentaje_coche = (coste_coche_mes / total_factura * 100) if total_factura > 0 else 0

        # Generar ID
        id_factura = generar_uuid()

        # Insertar factura
        # IMPORTANTE: Guardamos consumo DE LA RED (no el total con autoconsumo)
        cursor.execute("""
            INSERT INTO facturas_electricidad (
                id, mes, año, fecha_factura,
                consumo_punta_kwh, consumo_llano_kwh, consumo_valle_kwh, consumo_total_kwh,
                tarifa_punta, tarifa_llano, tarifa_valle,
                potencia, alquiler_contador, bono_social, servicios,
                coste_energia, impuesto_electricidad, iva, total_factura,
                excedentes_kwh, excedentes_compensacion,
                kwh_coche_mes, coste_coche_mes, porcentaje_coche,
                notas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_factura, mes, año, fecha_factura,
            consumo_punta_kwh, consumo_llano_kwh, consumo_valle_kwh, consumo_red_kwh,
            tarifa_punta, tarifa_llano, tarifa_valle,
            potencia, alquiler_contador, bono_social, servicios,
            coste_energia_consumo, impuesto_electricidad, iva, total_factura,
            energia_autoconsumida, excedentes_compensacion,
            kwh_coche_mes, coste_coche_mes, porcentaje_coche,
            notas
        ))

        conn.commit()
        return id_factura

    except sqlite3.Error as e:
        print(f"Error al insertar factura: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()


def obtener_facturas_electricidad(año=None, limit=None):
    """
    Obtiene facturas de electricidad, opcionalmente filtradas por año.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM facturas_electricidad"
    params = []

    if año:
        query += " WHERE año = ?"
        params.append(año)

    query += " ORDER BY año DESC, mes DESC"

    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query, params)
    facturas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return facturas


def obtener_factura_por_mes(mes, año):
    """Obtiene la factura de un mes específico."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM facturas_electricidad
        WHERE mes = ? AND año = ?
    """, (mes, año))

    resultado = cursor.fetchone()
    conn.close()
    return dict(resultado) if resultado else None


def actualizar_recarga_coche(id_recarga, **campos):
    """
    Actualiza una recarga existente.

    Args:
        id_recarga: ID de la recarga a actualizar
        **campos: Campos a actualizar (bateria_inicial, bateria_final, kwh_cargados, etc.)

    Returns:
        True si se actualizó correctamente, False en caso contrario
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Construir la query dinámicamente con los campos proporcionados
        set_clauses = []
        valores = []

        for campo, valor in campos.items():
            if campo in ['fecha_recarga'] and hasattr(valor, 'isoformat'):
                valor = valor.isoformat()
            set_clauses.append(f"{campo} = ?")
            valores.append(valor)

        if not set_clauses:
            return False

        valores.append(id_recarga)

        query = f"UPDATE recargas_coche SET {', '.join(set_clauses)} WHERE id = ?"
        cursor.execute(query, valores)

        # También actualizar la transacción asociada si existe
        if 'coste_total' in campos:
            cursor.execute("""
                UPDATE transacciones
                SET importe = ?
                WHERE id = (SELECT transaccion_id FROM recargas_coche WHERE id = ?)
            """, (-abs(campos['coste_total']), id_recarga))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"Error al actualizar recarga: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def eliminar_recarga_coche(id_recarga):
    """
    Elimina una recarga y su transacción asociada.

    Args:
        id_recarga: ID de la recarga a eliminar

    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Obtener el ID de la transacción asociada
        cursor.execute("SELECT transaccion_id FROM recargas_coche WHERE id = ?", (id_recarga,))
        resultado = cursor.fetchone()

        if resultado:
            transaccion_id = resultado['transaccion_id']

            # Eliminar la recarga
            cursor.execute("DELETE FROM recargas_coche WHERE id = ?", (id_recarga,))

            # Eliminar la transacción asociada
            if transaccion_id:
                cursor.execute("DELETE FROM transacciones WHERE id = ?", (transaccion_id,))

            conn.commit()
            return True
        else:
            return False

    except sqlite3.Error as e:
        print(f"Error al eliminar recarga: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def obtener_recarga_por_id(id_recarga):
    """
    Obtiene una recarga específica por su ID.

    Args:
        id_recarga: ID de la recarga

    Returns:
        Dict con los datos de la recarga o None si no existe
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recargas_coche WHERE id = ?", (id_recarga,))
    resultado = cursor.fetchone()
    conn.close()

    return dict(resultado) if resultado else None


def pagar_recargas_mes(mes, año, fecha_pago, categoria='COCHE_ELECTRICO', notas=''):
    """
    Marca todas las recargas pendientes de un mes como pagadas y crea UNA transacción
    con la suma total de todas las recargas.

    Args:
        mes: Mes de las recargas (1-12)
        año: Año de las recargas
        fecha_pago: Fecha en la que se realiza el pago (ej: fecha del bizum)
        categoria: Categoría para la transacción (default: 'COCHE_ELECTRICO')
        notas: Notas adicionales

    Returns:
        Tuple (id_transaccion, total_pagado, num_recargas) si tiene éxito, None si falla
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Obtener todas las recargas pendientes del mes
        cursor.execute("""
            SELECT * FROM recargas_coche
            WHERE mes = ? AND año = ? AND pagado = 0
            ORDER BY fecha_recarga ASC
        """, (mes, año))

        recargas_pendientes = [dict(row) for row in cursor.fetchall()]

        if not recargas_pendientes:
            print(f"No hay recargas pendientes para {mes}/{año}")
            return None

        # 2. Calcular total a pagar y recopilar datos
        total_coste = sum(r['coste_total'] for r in recargas_pendientes)
        total_kwh = sum(r['kwh_cargados'] for r in recargas_pendientes)
        num_recargas = len(recargas_pendientes)

        # 3. Crear la transacción única
        id_transaccion = generar_uuid()

        # Convertir fecha_pago a string si es necesario
        if hasattr(fecha_pago, 'isoformat'):
            fecha_pago_str = fecha_pago.isoformat()
        else:
            fecha_pago_str = str(fecha_pago)

        # Concepto genérico para que Excel lo detecte y omita duplicados
        concepto = f"Recarga coche"
        if notas:
            notas_completas = f"{notas} | {num_recargas} recargas, {total_kwh:.1f} kWh"
        else:
            notas_completas = f"{num_recargas} recargas del mes {mes}/{año}, {total_kwh:.1f} kWh totales"

        # Extraer mes y año de la fecha de pago (no del mes de las recargas)
        # Esto asegura que la transacción se registre en el mes que realmente se pagó
        fecha_pago_obj = datetime.strptime(fecha_pago_str, '%Y-%m-%d').date()
        mes_pago = fecha_pago_obj.month
        año_pago = fecha_pago_obj.year

        # NO calcular saldo_posterior aquí
        # Las transacciones manuales se dejan con saldo_posterior = NULL
        # Luego se puede usar recalcular_saldos_transacciones_manuales() para calcularlos
        # basándose en el último saldo conocido del banco

        cursor.execute("""
            INSERT INTO transacciones (
                id, fecha, concepto, importe, categoria, tipo, mes, año, notas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_transaccion, fecha_pago_str, concepto, -abs(total_coste),
            categoria, 'GASTO', mes_pago, año_pago, notas_completas
        ))

        # 4. Marcar todas las recargas como pagadas y vincularlas a la transacción
        for recarga in recargas_pendientes:
            cursor.execute("""
                UPDATE recargas_coche
                SET pagado = 1, fecha_pago = ?, transaccion_id = ?
                WHERE id = ?
            """, (fecha_pago_str, id_transaccion, recarga['id']))

        conn.commit()
        print(f"✅ Pagadas {num_recargas} recargas del mes {mes}/{año} por {total_coste:.2f}€")
        return (id_transaccion, total_coste, num_recargas)

    except sqlite3.Error as e:
        print(f"Error al pagar recargas: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()


def obtener_recargas_pendientes(mes=None, año=None):
    """
    Obtiene las recargas pendientes de pago, opcionalmente filtradas por mes/año.

    Args:
        mes: Mes (1-12) opcional
        año: Año opcional

    Returns:
        Lista de diccionarios con recargas pendientes
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM recargas_coche WHERE pagado = 0"
    params = []

    if mes:
        query += " AND mes = ?"
        params.append(mes)
    if año:
        query += " AND año = ?"
        params.append(año)

    query += " ORDER BY fecha_recarga DESC"

    cursor.execute(query, params)
    recargas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return recargas


# ========== FUNCIONES PRESUPUESTOS MENSUALES ==========

def crear_presupuesto(categoria, limite_mensual):
    """
    Crea o actualiza un presupuesto mensual para una categoría.

    Args:
        categoria: Nombre de la categoría
        limite_mensual: Límite mensual en euros

    Returns:
        True si se creó/actualizó correctamente, False en caso contrario
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO presupuestos_mensuales (categoria, limite_mensual, activo)
            VALUES (?, ?, 1)
            ON CONFLICT(categoria) DO UPDATE SET
                limite_mensual = excluded.limite_mensual,
                activo = 1,
                updated_at = CURRENT_TIMESTAMP
        """, (categoria, limite_mensual))

        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al crear presupuesto: {e}")
        return False
    finally:
        conn.close()


def obtener_presupuestos():
    """
    Obtiene todos los presupuestos mensuales activos.

    Returns:
        Lista de diccionarios con los presupuestos
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM presupuestos_mensuales
        WHERE activo = 1
        ORDER BY categoria ASC
    """)

    presupuestos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return presupuestos


def obtener_presupuesto_categoria(categoria):
    """
    Obtiene el presupuesto de una categoría específica.

    Args:
        categoria: Nombre de la categoría

    Returns:
        Dict con el presupuesto o None si no existe
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM presupuestos_mensuales
        WHERE categoria = ? AND activo = 1
    """, (categoria,))

    resultado = cursor.fetchone()
    conn.close()

    return dict(resultado) if resultado else None


def eliminar_presupuesto(categoria):
    """
    Desactiva un presupuesto (no lo elimina físicamente).

    Args:
        categoria: Nombre de la categoría

    Returns:
        True si se desactivó correctamente, False en caso contrario
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE presupuestos_mensuales
            SET activo = 0, updated_at = CURRENT_TIMESTAMP
            WHERE categoria = ?
        """, (categoria,))

        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error al eliminar presupuesto: {e}")
        return False
    finally:
        conn.close()


def obtener_resumen_presupuestos(mes, año):
    """
    Obtiene el resumen de presupuestos vs gastos reales para un mes específico.

    Calcula los gastos NETOS por categoría, restando los reembolsos que han sido
    asignados específicamente a cada categoría (mediante notas 'REEMBOLSO_DE:{categoria}').

    Args:
        mes: Mes (1-12)
        año: Año

    Returns:
        Lista de diccionarios con el resumen por categoría
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        WITH gastos_brutos AS (
            SELECT
                p.categoria,
                p.limite_mensual,
                COALESCE(SUM(ABS(t.importe)), 0) as gastado_bruto
            FROM presupuestos_mensuales p
            LEFT JOIN transacciones t ON
                t.categoria = p.categoria
                AND t.tipo = 'GASTO'
                AND t.mes = ?
                AND t.año = ?
            WHERE p.activo = 1
            GROUP BY p.categoria, p.limite_mensual
        ),
        reembolsos_categoria AS (
            SELECT
                REPLACE(notas, 'REEMBOLSO_DE:', '') as categoria,
                SUM(importe) as total_reembolsos
            FROM transacciones
            WHERE categoria = 'REEMBOLSO'
                AND tipo = 'INGRESO'
                AND mes = ?
                AND año = ?
                AND notas LIKE 'REEMBOLSO_DE:%'
            GROUP BY notas
        )
        SELECT
            g.categoria,
            g.limite_mensual as presupuesto,
            g.gastado_bruto,
            COALESCE(r.total_reembolsos, 0) as reembolsos_asignados,
            g.gastado_bruto - COALESCE(r.total_reembolsos, 0) as gastado,
            g.limite_mensual - (g.gastado_bruto - COALESCE(r.total_reembolsos, 0)) as restante,
            CASE
                WHEN g.limite_mensual > 0 THEN
                    ((g.gastado_bruto - COALESCE(r.total_reembolsos, 0)) / g.limite_mensual) * 100
                ELSE 0
            END as porcentaje_usado
        FROM gastos_brutos g
        LEFT JOIN reembolsos_categoria r ON g.categoria = r.categoria
        ORDER BY porcentaje_usado DESC
    """, (mes, año, mes, año))

    resumen = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return resumen


def obtener_años_disponibles():
    """
    Obtiene la lista de años disponibles basándose en:
    1. Años con transacciones registradas en la BD
    2. Año actual (siempre disponible)
    3. Año siguiente (para planificación)

    Returns:
        list: Lista ordenada de años disponibles [2023, 2024, 2025, ...]
    """
    import datetime

    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener años únicos de las transacciones
    cursor.execute("""
        SELECT DISTINCT año
        FROM transacciones
        ORDER BY año ASC
    """)

    años_con_datos = [row['año'] for row in cursor.fetchall()]
    conn.close()

    # Obtener año actual y siguiente
    año_actual = datetime.date.today().year
    año_siguiente = año_actual + 1

    # Combinar y eliminar duplicados
    años_disponibles = sorted(list(set(años_con_datos + [año_actual, año_siguiente])))

    return años_disponibles

def recalcular_saldos_transacciones_manuales(mes=None, año=None):
    """
    Calcula el saldo_posterior SOLO para transacciones manuales (sin saldo).

    Algoritmo:
    1. Para cada transacción manual (sin saldo_posterior)
    2. Buscar en el mismo mes la transacción del banco más cercana al líquido disponible
       que sea del mismo día o anterior
    3. Calcular: saldo_manual = saldo_ancla + suma(trans_manuales_hasta_esta)

    IMPORTANTE: NO modifica transacciones importadas del banco que ya tienen
    saldo_posterior. El saldo del banco es el saldo REAL y no debe recalcularse.

    Args:
        mes: Mes a procesar (1-12). Si es None, procesa todos los meses.
        año: Año a procesar. Si es None, procesa todos los años.

    Returns:
        int: Número de transacciones manuales actualizadas
    """
    from utils import metrics

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Obtener líquido disponible (referencia para encontrar el ancla)
        liquido_disponible = metrics.calcular_liquido_disponible()

        filtro_msg = ""
        if mes and año:
            filtro_msg = f" del mes {mes}/{año}"
            print(f"🔄 Calculando saldos para transacciones manuales{filtro_msg}...")
        else:
            print("🔄 Calculando saldos para TODAS las transacciones manuales...")

        # Obtener transacciones sin saldo_posterior (con filtro opcional)
        query = """
            SELECT id, fecha, importe, mes, año
            FROM transacciones
            WHERE saldo_posterior IS NULL
        """
        params = []

        if mes is not None:
            query += " AND mes = ?"
            params.append(mes)
        if año is not None:
            query += " AND año = ?"
            params.append(año)

        query += " ORDER BY fecha ASC, id ASC"

        cursor.execute(query, params)
        transacciones_sin_saldo = cursor.fetchall()

        if not transacciones_sin_saldo:
            print(f"✅ No hay transacciones manuales{filtro_msg}")
            return 0

        print(f"📋 Encontradas {len(transacciones_sin_saldo)} transacciones sin saldo{filtro_msg}")
        transacciones_actualizadas = 0

        for transaccion in transacciones_sin_saldo:
            t_id = transaccion['id']
            t_fecha = transaccion['fecha']
            t_mes = transaccion['mes']
            t_año = transaccion['año']

            # Buscar transacción ancla:
            # - Mismo mes y año
            # - Fecha <= fecha de la transacción manual
            # - Saldo más cercano al líquido disponible
            cursor.execute("""
                SELECT fecha, saldo_posterior
                FROM transacciones
                WHERE saldo_posterior IS NOT NULL
                  AND mes = ? AND año = ?
                  AND fecha <= ?
                ORDER BY ABS(saldo_posterior - ?) ASC
                LIMIT 1
            """, (t_mes, t_año, t_fecha, liquido_disponible))

            ancla = cursor.fetchone()

            if ancla:
                # Calcular suma de transacciones manuales desde el ancla hasta esta
                cursor.execute("""
                    SELECT COALESCE(SUM(importe), 0) as suma
                    FROM transacciones
                    WHERE saldo_posterior IS NULL
                      AND fecha >= ?
                      AND fecha <= ?
                      AND id <= ?
                """, (ancla['fecha'], t_fecha, t_id))

                suma_intermedias = cursor.fetchone()['suma']
                saldo_calculado = ancla['saldo_posterior'] + suma_intermedias
            else:
                # No hay ancla: calcular desde el inicio (fallback)
                cursor.execute("""
                    SELECT COALESCE(SUM(importe), 0) as suma
                    FROM transacciones
                    WHERE fecha < ? OR (fecha = ? AND id <= ?)
                """, (t_fecha, t_fecha, t_id))

                saldo_calculado = cursor.fetchone()['suma']

            # Actualizar esta transacción
            cursor.execute("""
                UPDATE transacciones
                SET saldo_posterior = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (saldo_calculado, t_id))

            transacciones_actualizadas += 1

        conn.commit()
        print(f"✅ Calculados {transacciones_actualizadas} saldos{filtro_msg}")

        return transacciones_actualizadas

    except sqlite3.Error as e:
        print(f"❌ Error al calcular saldos: {e}")
        conn.rollback()
        return 0
    finally:
        conn.close()

def calcular_saldo_actual():
    """
    Calcula el saldo actual basándose en todas las transacciones.

    Returns:
        float: Saldo actual (suma de todos los importes)
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT COALESCE(SUM(importe), 0) as saldo_total
            FROM transacciones
        """)

        resultado = cursor.fetchone()
        saldo_actual = resultado['saldo_total'] if resultado else 0

        return saldo_actual

    finally:
        conn.close()
