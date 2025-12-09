#!/usr/bin/env python3
"""
Script para verificar qué versión de render_metric_card se está usando
"""

import sys
import inspect

# Agregar path
sys.path.insert(0, '/Users/daniel/mi_app_finanzas')

# Importar la función
from utils.components.metric_card import render_metric_card

# Obtener código fuente
source = inspect.getsource(render_metric_card)

# Verificar qué versión es
if 'st.metric(' in source:
    print("✅ VERSIÓN CORRECTA: Usando st.metric() nativo")
    print("   La función está reimplementada correctamente")
    print()
    print("Si sigues viendo HTML en la pantalla:")
    print("1. Detén Streamlit completamente (Ctrl+C)")
    print("2. Ejecuta: streamlit cache clear")
    print("3. Reinicia: streamlit run app.py")
else:
    print("❌ VERSIÓN ANTIGUA: Todavía usa HTML custom")
    print("   El archivo no se ha actualizado o Streamlit no lo recargó")
    print()
    print("Solución:")
    print("1. Verifica que git pull esté actualizado")
    print("2. Reinicia Streamlit completamente")

# Mostrar primeras líneas de la función
print("\n" + "="*60)
print("Primeras 10 líneas de render_metric_card():")
print("="*60)
lines = source.split('\n')[:15]
for i, line in enumerate(lines, 1):
    print(f"{i:3d}: {line}")
