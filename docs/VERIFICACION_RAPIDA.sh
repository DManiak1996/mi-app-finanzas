#!/bin/bash

# VERIFICACIÓN RÁPIDA DEL OVERHAUL DE DISEÑO
# ============================================
# Script para verificar rápidamente el estado del código
# Autor: Claude Code
# Fecha: 2025-12-04

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║      VERIFICACIÓN RÁPIDA - OVERHAUL DE DISEÑO                    ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
ERRORS=0
WARNINGS=0
SUCCESS=0

# Función helper para verificar
check() {
    local name="$1"
    local command="$2"

    echo -n "Verificando $name... "

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ OK${NC}"
        ((SUCCESS++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        ((ERRORS++))
        return 1
    fi
}

# ============================================================
# 1. VERIFICAR SINTAXIS PYTHON
# ============================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. VERIFICACIÓN DE SINTAXIS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check "app.py" "python3 -m py_compile app.py"
check "pages_coche_electrico.py" "python3 -m py_compile pages_coche_electrico.py"
check "pages_asistente_ia.py" "python3 -m py_compile pages_asistente_ia.py"
check "utils/feature_flags.py" "python3 -m py_compile utils/feature_flags.py"
check "utils/dashboard_v2.py" "python3 -m py_compile utils/dashboard_v2.py"
check "utils/design_tokens.py" "python3 -m py_compile utils/design_tokens.py"
check "utils/components/page_layout.py" "python3 -m py_compile utils/components/page_layout.py"
check "utils/components/chart_container.py" "python3 -m py_compile utils/components/chart_container.py"
check "utils/components/grid_system.py" "python3 -m py_compile utils/components/grid_system.py"

# ============================================================
# 2. VERIFICAR EXISTENCIA DE ARCHIVOS CRÍTICOS
# ============================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. VERIFICACIÓN DE ARCHIVOS CRÍTICOS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check "Design tokens" "test -f utils/design_tokens.py"
check "Feature flags" "test -f utils/feature_flags.py"
check "Dashboard V2" "test -f utils/dashboard_v2.py"
check "Page layout" "test -f utils/components/page_layout.py"
check "Chart container" "test -f utils/components/chart_container.py"
check "Grid system" "test -f utils/components/grid_system.py"
check "Components __init__" "test -f utils/components/__init__.py"

# ============================================================
# 3. VERIFICAR FEATURE FLAGS
# ============================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. ESTADO DE FEATURE FLAGS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 << 'PYTHON'
import sys
sys.path.insert(0, '.')

from utils.feature_flags import get_all_flags, get_active_flags

all_flags = get_all_flags()
active_flags = get_active_flags()

print(f"Total de flags: {len(all_flags)}")
print(f"Flags activos: {len(active_flags)}")
print(f"Porcentaje: {len(active_flags) / len(all_flags) * 100:.0f}%")

# Mostrar flags críticos
critical_flags = [
    'USE_NEW_DESIGN',
    'USE_NEW_DASHBOARD',
    'USE_NEW_TRANSACCIONES',
    'USE_NEW_COCHE_ELECTRICO',
    'USE_NEW_ASISTENTE_IA'
]

print("\nFlags críticos:")
for flag in critical_flags:
    status = "✅" if all_flags.get(flag, False) else "❌"
    print(f"  {status} {flag} = {all_flags.get(flag, False)}")
PYTHON

# ============================================================
# 4. VERIFICAR ESTRUCTURA DE FUNCIONES
# ============================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. VERIFICACIÓN DE FUNCIONES V2"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Verificar que existen las funciones _v2
check "mostrar_dashboard_v2" "grep -q 'def mostrar_dashboard_v2' utils/dashboard_v2.py"
check "mostrar_transacciones_v2" "grep -q 'def mostrar_transacciones_v2' app.py"
check "mostrar_estadisticas_coche_v2" "grep -q 'def mostrar_estadisticas_coche_v2' pages_coche_electrico.py"
check "mostrar_asistente_ia_v2" "grep -q 'def mostrar_asistente_ia_v2' pages_asistente_ia.py"

# ============================================================
# 5. VERIFICAR IMPORTS
# ============================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. VERIFICACIÓN DE IMPORTS CRÍTICOS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 << 'PYTHON'
import sys
sys.path.insert(0, '.')

imports_to_check = [
    ('feature_flags', 'from utils.feature_flags import is_enabled'),
    ('design_tokens', 'from utils.design_tokens import Colors'),
    ('dashboard_v2', 'from utils.dashboard_v2 import mostrar_dashboard_v2'),
]

for name, import_statement in imports_to_check:
    try:
        exec(import_statement)
        print(f"✅ {name}")
    except ImportError as e:
        print(f"❌ {name}: {e}")
PYTHON

# ============================================================
# 6. VERIFICAR DOCUMENTACIÓN
# ============================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. VERIFICACIÓN DE DOCUMENTACIÓN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check "Auditoría final" "test -f docs/AUDITORIA_FINAL_OVERHAUL.md"
check "Resumen auditoría" "test -f docs/AUDITORIA_RESUMEN.txt"
check "Design doc" "test -f MUSATRO_DESIGN_DOC.md"
check "Estrategia overhaul" "test -f 'docs/ESTRATEGIA_OVERHAUL_DISEÑO.md'"

# ============================================================
# 7. ESTADÍSTICAS DEL PROYECTO
# ============================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. ESTADÍSTICAS DEL PROYECTO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "Archivos Python totales:"
find . -name "*.py" -not -path "./.archive/*" -not -path "./__pycache__/*" -not -path "./venv/*" | wc -l | xargs echo

echo ""
echo "Componentes creados:"
ls -1 utils/components/*.py 2>/dev/null | grep -v "__pycache__" | wc -l | xargs echo

echo ""
echo "Líneas de código en archivos críticos:"
echo "  app.py: $(wc -l < app.py) líneas"
echo "  pages_coche_electrico.py: $(wc -l < pages_coche_electrico.py) líneas"
echo "  pages_asistente_ia.py: $(wc -l < pages_asistente_ia.py) líneas"
echo "  utils/dashboard_v2.py: $(wc -l < utils/dashboard_v2.py) líneas"

# ============================================================
# RESUMEN FINAL
# ============================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "RESUMEN FINAL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✅ Verificaciones exitosas: $SUCCESS${NC}"
echo -e "${YELLOW}⚠️  Warnings: $WARNINGS${NC}"
echo -e "${RED}❌ Errores: $ERRORS${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                ✅ TODO OK - LISTO PARA PRODUCCIÓN                ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔═══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║              ❌ HAY ERRORES - REVISAR ANTES DE DEPLOY             ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
