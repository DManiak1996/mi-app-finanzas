# 🚀 Quick Start: Activar Coche Eléctrico y Asistente IA v2

## ⚡ Activación Rápida

```bash
# 1. Activar versiones v2
python scripts/toggle_coche_asistente_v2.py --enable

# 2. Reiniciar la aplicación
streamlit run app.py
```

Eso es todo! Las nuevas versiones están activas.

---

## 📊 Ver Estado Actual

```bash
python scripts/toggle_coche_asistente_v2.py --status
```

**Output esperado:**
```
📊 ESTADO ACTUAL DE FEATURE FLAGS
============================================================

✅ Coche Eléctrico v2              [ACTIVO]
✅ Asistente IA v2                 [ACTIVO]

============================================================
```

---

## 🔙 Rollback (Desactivar v2)

Si algo sale mal, rollback instantáneo:

```bash
# Volver a versión legacy (v1)
python scripts/toggle_coche_asistente_v2.py --disable

# Reiniciar la aplicación
streamlit run app.py
```

---

## ✅ Checklist de Verificación

Después de activar, verifica que:

### Coche Eléctrico
- [ ] Dashboard con gradiente verde se muestra
- [ ] Métricas en grid (4 columnas)
- [ ] Gráficos en containers estilizados
- [ ] Tabla con botones de exportación CSV/Excel
- [ ] Secciones organizadas con títulos e iconos

### Asistente IA
- [ ] Header con descripción se muestra
- [ ] Sección de bienvenida con instrucciones
- [ ] Mensajes del asistente en cards verdes
- [ ] Verificación de Ollama funciona
- [ ] Botón "Limpiar Chat" visible

---

## 🎨 Qué Esperar Visualmente

### Coche Eléctrico (v2)
- **Fondo:** Gradiente verde claro
- **Métricas:** Cards organizadas en grid
- **Gráficos:** Containers con sombras y bordes
- **Tablas:** Botones de exportación visibles
- **Spacing:** Más aire entre elementos

### Asistente IA (v2)
- **Header:** Título grande con descripción
- **Bienvenida:** Card verde con instrucciones
- **Mensajes IA:** Cards con gradiente y borde verde
- **Errores:** Cards rojas bien diferenciadas
- **Ancho:** Limitado a 1000px (más legible)

---

## 📝 Comandos Disponibles

```bash
# Activar
python scripts/toggle_coche_asistente_v2.py --enable
python scripts/toggle_coche_asistente_v2.py -e
python scripts/toggle_coche_asistente_v2.py on

# Desactivar
python scripts/toggle_coche_asistente_v2.py --disable
python scripts/toggle_coche_asistente_v2.py -d
python scripts/toggle_coche_asistente_v2.py off

# Ver estado
python scripts/toggle_coche_asistente_v2.py --status
python scripts/toggle_coche_asistente_v2.py -s
python scripts/toggle_coche_asistente_v2.py status
```

---

## 🐛 Troubleshooting

### Problema: "No se ven cambios después de activar"
**Solución:**
1. Verifica que los flags están activos: `python scripts/toggle_coche_asistente_v2.py --status`
2. Reinicia completamente Streamlit (Ctrl+C y volver a ejecutar)
3. Borra cache del navegador si es necesario

### Problema: "Error al importar componentes"
**Solución:**
1. Verifica que estás en el directorio correcto: `/Users/daniel/mi_app_finanzas`
2. Verifica que los archivos de componentes existen en `utils/components/`

### Problema: "Ollama no disponible en Asistente IA"
**Solución:**
1. Instala Ollama: https://ollama.ai
2. Ejecuta: `ollama pull llama3`
3. Verifica que Ollama está corriendo: `curl http://localhost:11434/api/tags`

---

## 📚 Documentación Completa

Para más detalles, consulta:
- [Documentación Completa de Migración](docs/MIGRACION_COCHE_ASISTENTE.md)
- [Resumen Final](RESUMEN_MIGRACION_FINAL.md)

---

**¿Listo para empezar?**

```bash
python scripts/toggle_coche_asistente_v2.py --enable && streamlit run app.py
```
