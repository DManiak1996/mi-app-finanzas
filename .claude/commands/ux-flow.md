---
description: "Analiza un flujo de usuario específico"
---

Activa el agente UX/UI Designer para analizar un flujo de usuario específico del proyecto.

**Instrucciones para el usuario:**
Después de ejecutar este comando, especifica qué flujo quieres analizar. Por ejemplo:
- "Flujo de importación de transacciones desde Excel"
- "Flujo de añadir un gasto manualmente"
- "Flujo de configuración de categorías"
- "Flujo de registro de recarga del coche eléctrico"
- "Flujo de exportación/sincronización de datos"

**Instrucciones para el agente:**
1. Lee el agente definido en `.claude/agents/ux-designer.md`
2. Solicita al usuario que especifique el flujo a analizar (si no lo ha hecho ya)
3. Revisa el código relacionado con ese flujo específico
4. Realiza un análisis profundo del user journey:
   - Mapa el flujo paso a paso
   - Identifica puntos de fricción
   - Evalúa claridad de los CTAs
   - Revisa feedback y validaciones
   - Analiza el happy path y los edge cases
5. Propón mejoras específicas para ese flujo

**Entregables esperados:**
- Diagrama del flujo actual (textual)
- Identificación de pain points
- Lista de mejoras priorizadas para ese flujo
- Propuesta de flujo optimizado
- Ejemplos de código específicos
