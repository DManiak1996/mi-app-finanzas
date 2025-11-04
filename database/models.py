
# database/models.py

# Sentencia SQL para crear la tabla de transacciones
CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transacciones (
    id TEXT PRIMARY KEY,
    fecha DATE NOT NULL,
    concepto TEXT NOT NULL,
    importe REAL NOT NULL,
    categoria TEXT,
    tipo TEXT NOT NULL, -- 'GASTO' o 'INGRESO'
    mes INTEGER,
    año INTEGER,
    notas TEXT,
    saldo_posterior REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

# Sentencia SQL para crear la tabla de facturas de electricidad
CREATE_FACTURAS_ELECTRICIDAD_TABLE = """
CREATE TABLE IF NOT EXISTS facturas_electricidad (
    id TEXT PRIMARY KEY,
    mes INTEGER NOT NULL,
    año INTEGER NOT NULL,
    fecha_factura DATE,

    -- Consumos por franja (kWh)
    consumo_punta_kwh REAL DEFAULT 0,
    consumo_llano_kwh REAL DEFAULT 0,
    consumo_valle_kwh REAL DEFAULT 0,
    consumo_total_kwh REAL DEFAULT 0,

    -- Tarifas aplicadas (€/kWh) - guardadas para histórico
    tarifa_punta REAL DEFAULT 0.184576,
    tarifa_llano REAL DEFAULT 0.131892,
    tarifa_valle REAL DEFAULT 0.099904,

    -- Costes fijos mensuales (€)
    potencia REAL DEFAULT 13.71,
    alquiler_contador REAL DEFAULT 0.80,
    bono_social REAL DEFAULT 0.38,
    servicios REAL DEFAULT 4.69,

    -- Calculados automáticamente
    coste_energia REAL DEFAULT 0,
    impuesto_electricidad REAL DEFAULT 0,
    iva REAL DEFAULT 0,
    total_factura REAL DEFAULT 0,

    -- Excedentes solares (informativo, no afecta cálculos coche)
    excedentes_kwh REAL DEFAULT 0,
    excedentes_compensacion REAL DEFAULT 0,

    -- Desglose participación coche
    kwh_coche_mes REAL DEFAULT 0,
    coste_coche_mes REAL DEFAULT 0,
    porcentaje_coche REAL DEFAULT 0,

    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(mes, año)
);
"""

# Sentencia SQL para crear la tabla de recargas del coche eléctrico
CREATE_RECARGAS_COCHE_TABLE = """
CREATE TABLE IF NOT EXISTS recargas_coche (
    id TEXT PRIMARY KEY,
    fecha_recarga TIMESTAMP NOT NULL,

    -- Datos batería VW ID.3 Pro S (77 kWh)
    bateria_inicial REAL DEFAULT 20,
    bateria_final REAL DEFAULT 80,
    kwh_cargados REAL NOT NULL,

    -- Datos de conducción
    km_recorridos REAL DEFAULT 0,
    consumo_medio REAL DEFAULT 0,  -- kWh/100km mostrado en el coche

    -- Configuración de recarga
    franja_horaria TEXT NOT NULL,  -- 'punta', 'llano', 'valle'
    tarifa_kwh REAL NOT NULL,

    -- Desglose de costes (calculados al momento)
    coste_energia REAL DEFAULT 0,
    coste_potencia REAL DEFAULT 0,
    coste_alquiler REAL DEFAULT 0,
    coste_bono REAL DEFAULT 0,
    coste_servicios REAL DEFAULT 0,
    impuesto_electricidad REAL DEFAULT 0,
    iva REAL DEFAULT 0,
    coste_total REAL DEFAULT 0,

    -- Agrupación temporal
    mes INTEGER NOT NULL,
    año INTEGER NOT NULL,

    -- Estado de pago
    pagado BOOLEAN DEFAULT 0,  -- 0 = pendiente, 1 = pagado
    fecha_pago TIMESTAMP,  -- Fecha en la que se registró el pago

    -- Referencias
    transaccion_id TEXT,  -- FK a transacciones (se crea solo cuando pagado=1)
    categoria TEXT DEFAULT 'COCHE_ELECTRICO',

    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Sentencia SQL para crear la tabla de presupuestos mensuales
CREATE_PRESUPUESTOS_TABLE = """
CREATE TABLE IF NOT EXISTS presupuestos_mensuales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,
    limite_mensual REAL NOT NULL,
    activo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(categoria)
);
"""

# Lista de todas las sentencias de creación de tablas
ALL_TABLES = [
    CREATE_TRANSACTIONS_TABLE,
    CREATE_CUSTOM_CATEGORIES_TABLE,
    CREATE_CLASSIFICATION_RULES_TABLE,
    CREATE_FACTURAS_ELECTRICIDAD_TABLE,
    CREATE_RECARGAS_COCHE_TABLE,
    CREATE_PRESUPUESTOS_TABLE
]
