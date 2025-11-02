---
description: "Auditoría de accesibilidad (A11y) del proyecto"
---

Activa el agente UX/UI Designer en modo auditoría de accesibilidad para revisar el cumplimiento de las WCAG 2.1 y mejoras de diseño inclusivo.

**Objetivo:** Asegurar que la aplicación sea usable por personas con discapacidades visuales, motoras, auditivas y cognitivas.

**Instrucciones para el agente:**
1. Lee el agente definido en `.claude/agents/ux-designer.md`
2. Revisa el código buscando problemas de accesibilidad:

   **Nivel A (Básico - debe cumplirse):**
   - Contraste de color (mínimo 4.5:1 para texto normal, 3:1 para texto grande)
   - Textos alternativos en imágenes
   - Estructura de headings correcta (h1, h2, h3...)
   - Labels en formularios
   - Navegación por teclado
   - Identificación de errores clara

   **Nivel AA (Recomendado):**
   - Contraste mejorado
   - Resize de texto hasta 200% sin pérdida de funcionalidad
   - Orientación múltiple (no forzar landscape/portrait)
   - Identificación de input purpose
   - Status messages anunciados

   **Nivel AAA (Óptimo):**
   - Contraste máximo (7:1)
   - Sin imágenes de texto
   - Contexto adicional en links

3. Identifica problemas específicos con referencias al código
4. Propón soluciones concretas
5. Prioriza por severidad de impacto

**Entregables esperados:**
- Puntuación de accesibilidad actual (nivel A/AA/AAA)
- Lista de problemas categorizados por tipo:
  - Perceptibilidad
  - Operabilidad
  - Comprensibilidad
  - Robustez
- Para cada problema:
  - Criterio WCAG violado
  - Ubicación en el código
  - Impacto en usuarios
  - Solución propuesta con código
- Herramientas recomendadas para testing continuo
- Roadmap de mejoras de a11y
