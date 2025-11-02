# 🚀 Quick Start - Agente UX/UI Designer

Esta guía te ayudará a empezar a usar el agente UX/UI en menos de 2 minutos.

## 🎯 ¿Qué hace este agente?

Te ayuda a mejorar la **experiencia de usuario (UX)** y el **diseño de interfaz (UI)** de tus aplicaciones mediante:
- Auditorías completas de usabilidad
- Análisis de flujos de usuario
- Recomendaciones de accesibilidad (A11y)
- Identificación de mejoras rápidas (quick wins)

## ⚠️ Importante: Este agente tiene personalidad fuerte

**Este NO es un agente complaciente que aprueba todo.**

- Te dirá directamente si algo está mal diseñado
- Rechazará propuestas que violen principios de UX
- Usará lenguaje directo: "Esto está mal" en lugar de "quizás podrías considerar..."
- SIEMPRE justificará sus críticas con principios de UX, estudios o estándares
- SIEMPRE propondrá soluciones concretas después de criticar

**¿Por qué?** Porque su lealtad es con el usuario final, no con tus sentimientos. Un diseñador complaciente es un diseñador inútil.

## ⚡ Uso Rápido

### 1️⃣ Auditoría completa de UX/UI
```
/ux-review
```
**Qué hace:** Analiza toda tu aplicación y te da un informe completo con mejoras priorizadas.

**Cuándo usarlo:** Cada 2-3 meses, o antes de lanzar una versión importante.

---

### 2️⃣ Mejoras rápidas (Quick Wins)
```
/ux-quickwins
```
**Qué hace:** Te da 5-10 mejoras fáciles de implementar (menos de 1-2h cada una) pero con alto impacto.

**Cuándo usarlo:** Cuando tengas un par de horas libres para mejorar la UX.

---

### 3️⃣ Análisis de un flujo específico
```
/ux-flow
```
Luego especifica qué flujo: _"Analiza el flujo de importación de transacciones"_

**Qué hace:** Revisa en detalle un user journey concreto y propone optimizaciones.

**Cuándo usarlo:** Cuando estés diseñando un nuevo feature o cuando usuarios reporten dificultad en una tarea.

---

### 4️⃣ Auditoría de Accesibilidad
```
/ux-accessibility
```
**Qué hace:** Revisa si tu app cumple con WCAG 2.1 (estándares de accesibilidad).

**Cuándo usarlo:** Antes de lanzar a producción, o para hacer tu app accesible para personas con discapacidades.

---

## 📋 Ejemplo Práctico

Imagina que acabas de terminar un nuevo feature:

1. **Primero** → `/ux-flow` para revisar ese flujo específico
2. **Si hay problemas** → Implementa las mejoras sugeridas
3. **Mensualmente** → `/ux-quickwins` para mejorar continuamente
4. **Cada trimestre** → `/ux-review` para auditoría completa

## 🎨 ¿Qué tipo de mejoras propone?

El agente puede sugerirte:

- ✅ **Usabilidad:** "El botón de 'Guardar' debería ser más visible"
- ✅ **Accesibilidad:** "Este texto tiene poco contraste, cambia de #999 a #666"
- ✅ **Flujo:** "Este formulario tiene 5 pasos, puedes reducirlo a 2"
- ✅ **Feedback:** "Falta un mensaje de éxito al guardar"
- ✅ **Errores:** "Los mensajes de error no son claros para el usuario"
- ✅ **Visual:** "Estos espaciados son inconsistentes (16px vs 20px)"

## 💡 Tips para Obtener el Mejor Resultado

1. **Proporciona contexto:**
   - "Mis usuarios son personas mayores de 60 años"
   - "La app se usa principalmente en móvil"

2. **Comparte problemas reales:**
   - "Los usuarios no encuentran el botón de exportar"
   - "La gente se confunde en el paso 3"

3. **Pregunta por alternativas:**
   - "Dame 3 formas diferentes de mejorar este formulario"

4. **Pide ejemplos:**
   - "Muéstrame apps que hacen esto bien"

## 📚 ¿Quieres más detalles?

Lee la documentación completa en:
- [README de agentes](./.claude/agents/README.md)
- [Definición del agente UX/UI](./.claude/agents/ux-designer.md)

## 🔥 Empieza AHORA

El mejor momento para mejorar tu UX es **ahora**. Ejecuta:

```
/ux-quickwins
```

Y en 10 minutos tendrás una lista de mejoras concretas que implementar. 🚀

---

**¿Necesitas ayuda?** Simplemente pregunta en el chat:
```
Explícame cómo usar el agente UX/UI
```
