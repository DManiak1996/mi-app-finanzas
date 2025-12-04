import sys
import os
import sqlite3

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_service import LLMService

def test_sqlite_syntax():
    print("Testing SQLite Syntax Generation...")
    service = LLMService()
    
    # Test query that triggered the error
    question = "Que tal ves mis finanzas este mes? Mejor que el mes pasado?"
    print(f"\nQuestion: {question}")
    
    sql = service.get_sql_from_question(question)
    print(f"Generated SQL: {sql}")
    
    if not sql:
        print("❌ Failed to generate SQL")
        return

    # Check for forbidden PostgreSQL syntax
    if "interval" in sql.lower():
        print("❌ Failed: SQL still contains 'interval' keyword")
    else:
        print("✅ SQL does not contain 'interval'")

    # Try to explain (dry run) to see if it's valid SQLite syntax
    # We don't need real data, just syntax check
    try:
        conn = sqlite3.connect(":memory:")
        # Create dummy table to test syntax
        conn.execute("""
            CREATE TABLE transacciones (
                id TEXT, fecha TEXT, concepto TEXT, importe REAL, 
                categoria TEXT, tipo TEXT, mes INTEGER, año INTEGER, notas TEXT
            )
        """)
        conn.execute(sql)
        print("✅ SQL Syntax is valid SQLite")
    except sqlite3.Error as e:
        print(f"❌ SQL Syntax Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    test_sqlite_syntax()
