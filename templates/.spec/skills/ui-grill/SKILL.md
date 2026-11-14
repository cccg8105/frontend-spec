---
name: ui-grill
description: "Entrevista técnica estructurada de árbol de decisiones UI/UX (FSM, estados borde, rutas/RBAC, errores RFC 7807, responsive y accesibilidad) antes de especificar o codificar."
---

# ui-grill Skill

Esta skill activa el modo de entrevista arquitectónica y visual previa para eliminar ambigüedades de experiencia de usuario, contratos de estado y accesibilidad en cualquier stack frontend (React, Next.js, Vue/Nuxt, SvelteKit, Astro, Angular).

## Cuándo Activar esta Skill
- Invocada mediante `{{HARNESS_INTERVIEW_TRIGGER}}` al planificar requerimientos `MAJOR` o `MINOR` con decisiones abiertas en flujos, estados, permisos o diseño.
- Durante el onboarding *Brownfield* (`frontend-bootstrap`) para confirmar si un comportamiento legacy de UI es intencional (*As-Is*) o un defecto a registrar en `docs/backlog/audit-proposals.md`.

---

## Reglas de Oro del Entrevistador UI

1. **"Código, Tokens y Grafo primero, humano después":**
   Está **estrictamente prohibido** preguntar al usuario información observable en `docs/design/tokens-and-themes.md`, `docs/technical/`, componentes existentes, rutas, handlers MSW o `graphify-out/`. Inspecciona el repositorio antes de preguntar.
2. **Entrevista Concisa por Rondas:** {{HARNESS_QUESTION_STRATEGY}}. Formula de 2 a 4 decisiones concretas ordenadas con opción recomendada primero y trade-offs claros.
3. **Árbol de Decisión Quirúrgico Frontend:**
   Enfoca tus preguntas exclusivamente en las decisiones que impactan los artefactos de `frontend-spec`:
   - **Máquina de Estados e Invariantes (`ui-contracts-guidelines.md`):** ¿Qué pasa si el usuario hace doble clic al enviar? ¿Los valores del formulario se conservan ante error 500 o se limpian? ¿Usa actualización optimista o bloqueo con spinner?
   - **Estados Borde (`_template_user_flow.md`):** ¿Qué CTA o guía aparece en `EmptyState`? ¿Cuál es la acción de recuperación ante error `403`, `409` (conflicto) o `429`?
   - **Rutas, Renderizado y Auth (`routing-and-rendering.md`):** ¿La ruta es pública (SSG/SSR con SEO) o privada bajo guardia RBAC? ¿Los filtros deben persistir en URL query params o solo en estado local?
   - **Responsive y Accesibilidad:** ¿Cómo colapsan tablas o barras laterales en móvil (`390px`)? ¿Qué elemento recibe foco al abrir/cerrar el diálogo (`FocusRestoration`)?
   - **Brownfield As-Is vs. Bug:** *"En `PaymentModal.tsx:84` el botón permanece habilitado durante el POST: ¿es intencional o debo registrarlo como deuda en `audit-proposals.md`?"*

---

## Protocolo de Cierre
Al despejar las decisiones abiertas:
1. Resume brevemente los acuerdos alcanzados (tokens, estados, rutas e invariantes).
2. Formaliza los artefactos afectados (`UF-*`, `tokens-and-themes.md`, `routing-and-rendering.md`, `component-hierarchy.md`, `data-fetching-and-state.md`) y registra el `REQ-UI-*` en `docs/backlog/pending.md` (o la entrada `AUDIT-UI-*` si es triage Brownfield).
