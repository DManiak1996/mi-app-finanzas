import ollama
import sqlite3
import pandas as pd
from database.db_manager import DB_NAME

class LLMService:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name

    def get_schema_info(self):
        """
        Returns a string representation of the database schema for the prompt.
        """
        return """
        Tablas disponibles:
        1. transacciones (
            id TEXT PRIMARY KEY,
            fecha TEXT, -- Formato YYYY-MM-DD
            concepto TEXT,
            importe REAL, -- Negativo para gastos, positivo para ingresos
            categoria TEXT,
            tipo TEXT, -- 'GASTO' o 'INGRESO'
            mes INTEGER,
            año INTEGER,
            notas TEXT
        )
        2. recargas_coche (
            id TEXT PRIMARY KEY,
            fecha_recarga TEXT,
            kwh_cargados REAL,
            coste_total REAL,
            mes INTEGER,
            año INTEGER
        )
        3. facturas_electricidad (
            id TEXT PRIMARY KEY,
            mes INTEGER,
            año INTEGER,
            total_factura REAL,
            kwh_coche_mes REAL,
            coste_coche_mes REAL
        )
        """

    def validate_sql(self, sql):
        """
        Validates that the SQL is safe (read-only).
        """
        sql_upper = sql.strip().upper()
        if not sql_upper.startswith("SELECT"):
            return False, "Solo se permiten consultas de lectura (SELECT)."
        
        forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "REPLACE"]
        for keyword in forbidden_keywords:
            if keyword in sql_upper:
                return False, f"La consulta contiene palabras prohibidas: {keyword}"
        
        return True, ""

    def get_sql_from_question(self, question):
        """
        Generates a SQL query from a natural language question.
        """
        schema = self.get_schema_info()
        prompt = f"""
        Eres un experto en SQL y finanzas. Tu tarea es convertir una pregunta en lenguaje natural a una consulta SQL SQLite válida.
        
        Esquema de la base de datos:
        {schema}
        
        Reglas:
        1. Solo genera UNA ÚNICA sentencia SQL, sin explicaciones ni formato markdown.
        2. Usa siempre la tabla 'transacciones' para gastos e ingresos generales.
        3. Los gastos tienen importe NEGATIVO, los ingresos POSITIVO.
        4. Para sumar gastos, usa SUM(importe) y recuerda que el resultado será negativo.
        5. Si piden "cuánto gasté", el resultado debe ser la suma de los importes negativos.
        6. La fecha está en formato YYYY-MM-DD.
        7. Usa funciones de fecha de SQLite (strftime, date).
        8. IMPORTANTE: NO uses sintaxis de PostgreSQL como "interval '1 month'". Para restar tiempo usa: date('now', '-1 month').
        
        Ejemplos:
        - Pregunta: "¿Cuánto gasté en comida el mes pasado?"
          SQL: SELECT SUM(importe) FROM transacciones WHERE tipo='GASTO' AND concepto LIKE '%comida%' AND strftime('%Y-%m', fecha) = strftime('%Y-%m', date('now', '-1 month'));
          
        - Pregunta: "¿Qué tal mis finanzas este mes vs el pasado?"
          SQL: SELECT strftime('%Y-%m', fecha) as mes, SUM(importe) as total_gastos FROM transacciones WHERE tipo='GASTO' AND fecha >= date('now', 'start of month', '-1 month') GROUP BY mes;
          
        - Pregunta: "¿Cuál es mi saldo actual?"
          SQL: SELECT SUM(importe) FROM transacciones;
        
        Pregunta: {question}
        SQL:
        """
        
        # Lógica determinista para comparaciones temporales (fallback)
        question_lower = question.lower()
        if ("mejor que" in question_lower or "peor que" in question_lower or "comparado con" in question_lower or "diferencia" in question_lower) and ("mes" in question_lower):
             return "SELECT strftime('%Y-%m', fecha) as mes, SUM(importe) as total_gastos FROM transacciones WHERE tipo='GASTO' AND fecha >= date('now', 'start of month', '-1 month') GROUP BY mes ORDER BY mes DESC;"

        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            sql = response['response'].strip()
            # Clean up if the model adds markdown code blocks despite instructions
            sql = sql.replace("```sql", "").replace("```", "").strip()
            return sql
        except Exception as e:
            print(f"Error generando SQL: {e}")
            return None

    def execute_sql(self, sql):
        """
        Executes the SQL query safely.
        """
        is_valid, error = self.validate_sql(sql)
        if not is_valid:
            return None, error

        try:
            conn = sqlite3.connect(DB_NAME)
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return df, None
        except Exception as e:
            return None, f"Error ejecutando SQL: {e}"

    def generate_natural_response(self, question, sql, df):
        """
        Generates a natural language response based on the query results.
        """
        if df is None or df.empty:
            return "No encontré datos que respondan a tu pregunta."

        data_str = df.to_string()
        prompt = f"""
        Eres un asistente financiero personal.
        Pregunta del usuario: "{question}"
        Consulta SQL ejecutada: "{sql}"
        Resultados de la base de datos:
        {data_str}
        
        Responde a la pregunta del usuario basándote en estos datos de forma natural, concisa y amable.
        Si es una lista larga, resume los puntos clave.
        Si es un total, da la cifra exacta formateada en euros.
        """
        
        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"Error generando respuesta: {e}"
