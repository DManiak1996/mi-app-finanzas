# Agentes de Claude Code

Esta carpeta contiene agentes especializados para ayudarte en diferentes aspectos del desarrollo de tus proyectos.

## 🎨 Agente UX/UI Designer

### Descripción
Experto en Experiencia de Usuario (UX) y Diseño de Interfaces (UI) con más de 10 años de experiencia. Te ayuda a mejorar la usabilidad, accesibilidad y experiencia general de tus aplicaciones.

**⚠️ IMPORTANTE: Este agente tiene personalidad fuerte y criterio profesional.**
- NO es un "yes man" que aprueba todo
- Te dirá directamente si algo está mal diseñado
- Rechazará propuestas que violen principios de UX (con justificación)
- Usa lenguaje directo y profesional, no tímido o complaciente
- Su lealtad es con el usuario final, no con tus sentimientos

### Archivo
[`ux-designer.md`](./ux-designer.md)

### ¿Cuándo usarlo?
- Al iniciar un nuevo proyecto (para definir UX desde el principio)
- Durante el desarrollo (para validar decisiones de diseño)
- Al finalizar features (para revisar antes de deployment)
- Cuando recibas feedback de usuarios sobre usabilidad
- Para preparar presentaciones o demos

### Comandos disponibles

#### 1. `/ux-review` - Auditoría completa de UX/UI
Realiza una revisión exhaustiva de toda la aplicación:
- Arquitectura de información
- Usabilidad
- Diseño visual
- Accesibilidad
- Responsive design
- Flujos de usuario

**Cuándo usarlo:**
- Al finalizar una versión importante
- Cada 2-3 meses como auditoría de mantenimiento
- Antes de un rediseño mayor

**Output:**
- Resumen ejecutivo con puntuación
- Análisis detallado por áreas
- Lista priorizada de mejoras
- Quick wins
- Roadmap de implementación

**Ejemplo:**
```
/ux-review
```

---

#### 2. `/ux-flow [nombre del flujo]` - Análisis de flujo específico
Analiza en profundidad un user journey concreto de tu aplicación.

**Cuándo usarlo:**
- Al diseñar un nuevo feature
- Cuando usuarios reportan dificultad en una tarea específica
- Para optimizar conversiones o completitud de tareas
- Antes de implementar cambios importantes en un flujo

**Output:**
- Mapa del flujo actual paso a paso
- Identificación de pain points
- Propuesta de flujo optimizado
- Código específico de mejoras

**Ejemplos:**
```
/ux-flow
Después especifica: "Analiza el flujo de importación de transacciones desde Excel"
```

```
/ux-flow
Después especifica: "Revisa el onboarding de nuevos usuarios"
```

---

#### 3. `/ux-quickwins` - Mejoras rápidas de alto impacto
Identifica 5-10 mejoras que puedes implementar en poco tiempo pero con gran impacto en la UX.

**Cuándo usarlo:**
- Cuando tengas 1-2 horas libres para mejorar la app
- Antes de una demo o presentación importante
- Para "limpiar" deuda de UX acumulada
- Cada sprint como mejora continua

**Output:**
- Lista de 5-10 quick wins
- Código específico listo para implementar
- Estimación de esfuerzo (minutos/horas)
- Impacto esperado

**Ejemplo:**
```
/ux-quickwins
```

---

#### 4. `/ux-accessibility` - Auditoría de accesibilidad
Revisa el cumplimiento de WCAG 2.1 y propone mejoras de diseño inclusivo.

**Cuándo usarlo:**
- Al inicio del proyecto (para establecer baseline)
- Antes de lanzar a producción
- Si tu aplicación es de uso público/gubernamental
- Para cumplir con requisitos legales de accesibilidad
- Como mejora de alcance de tu producto

**Output:**
- Puntuación de accesibilidad (A/AA/AAA)
- Lista de problemas por categoría
- Soluciones específicas con código
- Herramientas de testing recomendadas

**Ejemplo:**
```
/ux-accessibility
```

---

### Uso manual del agente (sin comandos)

Si prefieres invocar al agente manualmente en una conversación:

```
Hola Claude, activa el agente UX/UI Designer definido en .claude/agents/ux-designer.md
y realiza una [auditoría completa / análisis del flujo X / quick wins / revisión de accesibilidad].
```

O más simple:
```
Necesito una revisión de UX/UI de mi aplicación. Usa el agente ux-designer.
```

---

## 🎯 Mejores Prácticas

### 1. Usa el agente en diferentes fases del proyecto
- **Fase de diseño:** Para validar wireframes y propuestas
- **Durante desarrollo:** Para code reviews con foco en UX
- **Pre-launch:** Auditoría completa antes de liberar
- **Post-launch:** Análisis basado en feedback de usuarios

### 2. Combina análisis generales con específicos
- Empieza con `/ux-review` para entender el estado general
- Luego usa `/ux-flow` para profundizar en áreas problemáticas
- Implementa `/ux-quickwins` regularmente
- Revisa `/ux-accessibility` al menos 1 vez al trimestre

### 3. Prioriza según tu contexto
El agente te dará mejoras categorizadas:
- **CRÍTICO 🔴:** Implementa inmediatamente
- **ALTO 🟠:** Planifica para el próximo sprint
- **MEDIO 🟡:** Backlog prioritario
- **BAJO 🟢:** Nice to have, implementa cuando tengas tiempo

### 4. Documenta las decisiones
Cuando el agente recomiende algo que decides no implementar:
- Documenta por qué (limitaciones técnicas, prioridades, etc.)
- Revisa la decisión en futuras auditorías
- Considera alternativas propuestas

### 5. Itera
La UX no es "una vez y listo":
- Implementa mejoras gradualmente
- Mide el impacto cuando sea posible
- Solicita nuevas revisiones después de cambios importantes
- Mantén un backlog de mejoras de UX

---

## 📚 Conceptos que el agente domina

- **Leyes de UX:** Hick, Fitts, Jakob, Prägnanz, Von Restorff
- **Principios de Nielsen:** 10 heurísticas de usabilidad
- **WCAG 2.1:** Niveles A, AA, AAA
- **Design Thinking:** Metodología centrada en el usuario
- **Design Systems:** Material, HIG, Fluent, Carbon, Ant Design
- **Psicología del color y tipografía**
- **Responsive design y mobile-first**
- **Accesibilidad (A11y)**

---

## 🔧 Personalización del agente

Si quieres adaptar el agente a tus necesidades específicas, edita [`ux-designer.md`](./ux-designer.md):

### Añadir contexto específico de tu dominio
Por ejemplo, si haces apps médicas, añade:
```markdown
### Consideraciones para apps médicas:
- Cumplimiento HIPAA
- Terminología médica clara
- Procesos críticos con doble confirmación
```

### Modificar el formato de output
Cambia la sección "Ejemplo de Output" para que se ajuste a tu preferencia.

### Añadir herramientas específicas
Si usas herramientas concretas (ej: Chakra UI, Material-UI), menciónalo en el agente.

### Ajustar el nivel de detalle
Si prefieres análisis más concisos o más detallados, modifica las instrucciones.

---

## 🤝 Contribuir con nuevos agentes

¿Tienes ideas para nuevos agentes? Algunos candidatos:

- **Performance Auditor:** Optimización de velocidad y recursos
- **Security Reviewer:** Revisión de vulnerabilidades de seguridad
- **Code Quality Analyst:** Clean code, patrones, arquitectura
- **Testing Specialist:** Cobertura, estrategias de testing
- **Documentation Writer:** Generación de docs técnica
- **API Designer:** Diseño de APIs RESTful/GraphQL
- **Database Architect:** Optimización de queries, modelado de datos

Para crear un nuevo agente:
1. Crea un archivo `.md` en esta carpeta
2. Define su expertise, metodología y formato de output
3. Crea comandos slash en `.claude/commands/` si es necesario
4. Actualiza este README

---

## ⚡ Tips Rápidos

### Para obtener el máximo valor del agente UX/UI:

1. **Sé específico con el contexto**
   - "Mis usuarios son personas mayores de 60 años"
   - "La app se usa principalmente en móvil mientras se camina"
   - "Es para uso profesional en un entorno corporativo"

2. **Comparte feedback de usuarios reales**
   - "Los usuarios dicen que no encuentran el botón de exportar"
   - "La gente se confunde en el paso 3 del onboarding"

3. **Pregunta por alternativas**
   - "Dame 3 formas diferentes de resolver este problema de UX"

4. **Solicita referencias**
   - "Muéstrame ejemplos de apps que resuelven esto bien"

5. **Pide priorización personalizada**
   - "Tengo 4 horas, ¿qué debería implementar primero?"

---

## 📞 Contacto y Feedback

Si tienes sugerencias para mejorar este agente o encuentras bugs, considera:
- Actualizar directamente [`ux-designer.md`](./ux-designer.md)
- Documentar el cambio en tu historial de Git
- Compartir mejoras con otros desarrolladores si este proyecto es open source

---

**Última actualización:** Noviembre 2025
**Mantenedor:** Daniel (Desarrollador + AI)
