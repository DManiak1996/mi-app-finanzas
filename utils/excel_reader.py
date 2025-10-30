
# utils/excel_reader.py

import pandas as pd
import logging
import locale
from . import categorizer # Importar el clasificador

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def leer_excel(file_path):
    """
    Lee un archivo Excel con transacciones financieras, lo procesa y 
    retorna una lista de transacciones normalizadas. Es flexible y procesa todas las hojas.
    """
    logging.info("--- Iniciando el proceso de importación de Excel ---")
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names_all = xls.sheet_names
        logging.info(f"Archivo Excel abierto. Hojas encontradas: {sheet_names_all}")
    except Exception as e:
        logging.error(f"Error fatal al abrir o leer el archivo Excel: {e}")
        return [], {"error": str(e)}

    transacciones = []
    hojas_procesadas = 0

    for sheet_name in sheet_names_all:
        try:
            logging.info(f"--- Procesando hoja: '{sheet_name}' ---")
            df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
            
            header_row_index = -1
            for i, row in df.head(10).iterrows():
                row_str = ' '.join(map(str, row.values)).lower()
                if 'fecha' in row_str and ('concepto' in row_str or 'descripcion' in row_str) and 'importe' in row_str:
                    header_row_index = i
                    logging.info(f"Fila de cabecera detectada en la fila {i+1}.")
                    break
            
            df = pd.read_excel(xls, sheet_name=sheet_name, header=header_row_index if header_row_index != -1 else 0)
            logging.info(f"Leídas {len(df)} filas de datos de la hoja.")
            hojas_procesadas += 1

            df.columns = df.columns.str.lower().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
            logging.info(f"Columnas normalizadas: {df.columns.tolist()}")

            # --- Lógica de identificación de columnas mejorada ---
            cols = df.columns
            def encontrar_columna(patterns):
                # Prioridad 1: Coincidencia exacta
                for p in patterns:
                    if p in cols:
                        return p
                # Prioridad 2: Coincidencia de subcadena
                for p in patterns:
                    match = next((c for c in cols if p in c), None)
                    if match:
                        return match
                return None

            col_fecha = encontrar_columna(['fecha'])
            col_concepto = encontrar_columna(['concepto', 'descripcion'])
            col_importe = encontrar_columna(['importe', 'cantidad'])
            col_saldo = encontrar_columna(['saldo posterior', 'saldo'])

            if not all([col_fecha, col_concepto, col_importe, col_saldo]):
                logging.warning("No se pudieron identificar todas las columnas por nombre. Usando fallback a orden posicional.")
                if len(df.columns) >= 4:
                    col_fecha, col_concepto, col_importe, col_saldo = df.columns[0], df.columns[1], df.columns[3], df.columns[4] # Ajustar índices si es necesario
                else:
                    logging.error(f"La hoja no tiene las 4 columnas mínimas requeridas (fecha, concepto, importe, saldo). Omitiendo.")
                    continue
            
            logging.info(f"Columnas identificadas -> Fecha: '{col_fecha}', Concepto: '{col_concepto}', Importe: '{col_importe}'")

            num_transacciones_hoja = 0
            for _, row in df.iterrows():
                if pd.isna(row[col_concepto]) or pd.isna(row[col_importe]):
                    continue

                fecha = pd.to_datetime(row[col_fecha], errors='coerce', dayfirst=True).date()
                if not fecha:
                    continue
                
                concepto = str(row[col_concepto])
                
                try:
                    # Usar locale para convertir el string a float
                    importe = locale.atof(str(row[col_importe]))
                except (ValueError, TypeError):
                    # Fallback si atof falla o el locale no estaba disponible
                    try:
                        importe_str = str(row[col_importe]).replace('.', '').replace(',', '.')
                        importe = float(importe_str)
                    except (ValueError, TypeError):
                        continue

                try:
                    saldo_posterior = locale.atof(str(row[col_saldo]))
                except (ValueError, TypeError, KeyError):
                    # Si la columna de saldo no existe o el valor es inválido, lo dejamos como nulo
                    saldo_posterior = None


                tipo = 'INGRESO' if importe > 0 else 'GASTO'
                categoria = categorizer.clasificar_transaccion(concepto, importe)

                transacciones.append({
                    'fecha': fecha,
                    'concepto': concepto,
                    'importe': importe,
                    'categoria': categoria,
                    'tipo': tipo,
                    'mes': fecha.month,
                    'año': fecha.year,
                    'notas': '',
                    'saldo_posterior': saldo_posterior
                })
                num_transacciones_hoja += 1
            
            logging.info(f"Encontradas {num_transacciones_hoja} transacciones válidas en la hoja.")

        except Exception as e:
            logging.error(f"Error procesando la hoja '{sheet_name}': {e}", exc_info=True)
            continue

    stats = {
        "total_sheets_processed": hojas_procesadas,
        "total_transactions_found": len(transacciones)
    }
    logging.info(f"--- Proceso de importación finalizado. {stats['total_sheets_processed']} hojas procesadas, {stats['total_transactions_found']} transacciones encontradas. ---")
    
    return transacciones, stats
