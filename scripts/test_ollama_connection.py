import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.llm_service import LLMService

def test_ollama():
    print("Testing Ollama connection...")
    try:
        service = LLMService()
        
        # Test 1: Simple SQL generation
        question = "Cuanto gasté en comida el mes pasado?"
        print(f"\nQuestion: {question}")
        sql = service.get_sql_from_question(question)
        print(f"Generated SQL: {sql}")
        
        if sql and "SELECT" in sql.upper():
            print("✅ SQL Generation Test Passed")
        else:
            print("❌ SQL Generation Test Failed")
            
        # Test 2: Safety check
        unsafe_sql = "DELETE FROM transacciones"
        is_valid, msg = service.validate_sql(unsafe_sql)
        if not is_valid:
            print(f"✅ Safety Check Passed (Blocked: {msg})")
        else:
            print("❌ Safety Check Failed (Allowed unsafe SQL)")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure Ollama is running and the model is pulled.")

if __name__ == "__main__":
    test_ollama()
