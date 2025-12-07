#!/usr/bin/env python3
"""Test para verificar por qué el HTML se muestra como texto plano"""

import sys
sys.path.insert(0, '/Users/daniel/mi_app_finanzas')

from utils.components.metric_card import render_metric_card
from utils.design_tokens import Colors
import inspect

# Ver el código fuente de render_metric_card
source = inspect.getsource(render_metric_card)

# Buscar st.markdown
if 'st.markdown' in source and 'unsafe_allow_html=True' in source:
    print("✅ La función SÍ llama st.markdown(..., unsafe_allow_html=True)")
else:
    print("❌ La función NO llama st.markdown correctamente")

# Buscar si hay algún return statement
if 'return' in source and 'card_html' in source:
    print("⚠️  WARNING: La función podría estar retornando HTML en lugar de renderizarlo")
    # Buscar la línea exacta del return
    for i, line in enumerate(source.split('\n')):
        if 'return' in line and 'card_html' in line:
            print(f"   Línea {i}: {line.strip()}")

# Verificar que st.markdown está DESPUÉS de crear card_html
lines = source.split('\n')
card_html_line = None
st_markdown_line = None

for i, line in enumerate(lines):
    if 'card_html =' in line:
        card_html_line = i
    if 'st.markdown(card_html' in line:
        st_markdown_line = i

if card_html_line and st_markdown_line:
    if st_markdown_line > card_html_line:
        print(f"✅ st.markdown (línea {st_markdown_line}) está DESPUÉS de card_html (línea {card_html_line})")
    else:
        print(f"❌ ERROR: st.markdown está ANTES de card_html")
else:
    print(f"⚠️  card_html line: {card_html_line}, st.markdown line: {st_markdown_line}")

# Verificar si hay algún print o st.write antes de st.markdown
problematic_calls = []
for i, line in enumerate(lines):
    if i < (st_markdown_line or 999):
        if any(call in line for call in ['print(card_html', 'st.write(card_html', 'st.code(card_html', 'st.text(card_html']):
            problematic_calls.append((i, line.strip()))

if problematic_calls:
    print("\n⚠️  PROBLEMA ENCONTRADO: Hay llamadas que muestran HTML ANTES de st.markdown:")
    for line_num, line in problematic_calls:
        print(f"   Línea {line_num}: {line}")
else:
    print("\n✅ No hay llamadas problemáticas antes de st.markdown")

print("\n" + "="*60)
print("CONCLUSIÓN:")
print("="*60)

# Generar un HTML de prueba simple
test_html = f"""
<div style="background: {Colors.PREMIUM_CARD_GRADIENT}; padding: 20px;">
    <p>Test</p>
</div>
"""

print(f"\nHTML de prueba generado:")
print(repr(test_html[:100]))
print(f"\nLongitud: {len(test_html)} caracteres")
print(f"Tiene saltos de línea: {chr(10) in test_html}")
