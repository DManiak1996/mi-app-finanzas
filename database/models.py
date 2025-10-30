
# database/models.py

# Sentencia SQL para crear la tabla de transacciones
CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATE NOT NULL,
    concepto TEXT NOT NULL,
    importe REAL NOT NULL,
    categoria TEXT,
    tipo TEXT NOT NULL, -- 'GASTO' o 'INGRESO'
    mes INTEGER,
    año INTEGER,
    notas TEXT,
    saldo_posterior REAL
);
"""

# Sentencia SQL para crear la tabla de categorías personalizadas
CREATE_CUSTOM_CATEGORIES_TABLE = """
CREATE TABLE IF NOT EXISTS categorias_personalizadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL, -- 'GASTO' o 'INGRESO'
    color TEXT DEFAULT '#3498db'
);
"""

# Sentencia SQL para crear la tabla de reglas de clasificación
CREATE_CLASSIFICATION_RULES_TABLE = """
CREATE TABLE IF NOT EXISTS reglas_clasificacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patron TEXT NOT NULL UNIQUE,
    categoria TEXT NOT NULL,
    activa BOOLEAN DEFAULT 1
);
"""

# Lista de todas las sentencias de creación de tablas
ALL_TABLES = [
    CREATE_TRANSACTIONS_TABLE,
    CREATE_CUSTOM_CATEGORIES_TABLE,
    CREATE_CLASSIFICATION_RULES_TABLE
]
