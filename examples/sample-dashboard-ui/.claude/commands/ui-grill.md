---
description: "Entrevista tecnica UI/UX previa (FSM, estados borde, rutas/RBAC, RFC 7807, responsive y a11y) mediante AskUserQuestion."
---

# /ui-grill — Entrevista Arquitectonica UI/UX

Objetivo: Despejar todas las ambiguedades de experiencia de usuario, estado y accesibilidad para `$ARGUMENTS` antes de especificar o codificar.

## Reglas de Entrevista

1. **"Codigo, Tokens y Grafo primero, humano despues":**
   - Inspecciona `docs/design/tokens-and-themes.md`, `docs/functional/index.md`, `docs/technical/` y `graphify-out/` (si existe) antes de formular cualquier pregunta.
   - Prohibido preguntar datos que ya constan en codigo, hojas CSS, configuracion o documentacion.
2. **Rondas Quirurgicas con `AskUserQuestion`:**
   - Formula entre **2 y 4 decisiones concretas** por ronda mediante la herramienta `AskUserQuestion`, colocando siempre la opcion recomendada primero con el prefijo `(Recommended)` y explicando los trade-offs.
3. **Ejes del Arbol de Decision:**
   - **FSM e Invariantes (`ui-contracts-guidelines.md`):** Proteccion contra doble envio, conservacion de borrador ante `5xx`, estrategia optimista vs. bloqueo.
   - **Estados Borde (`_template_user_flow.md`):** Diseno de `LoadingState` (skeleton), `EmptyState` (CTA) y recuperacion ante RFC 7807 (`403`, `409`, `429`, `5xx`).
   - **Rutas, Renderizado y Auth (`routing-and-rendering.md`):** Modo CSR/SSR/SSG/RSC, guardia RBAC, validacion de `returnTo` y filtros en query params.
   - **Responsive y a11y:** Colapso en `390px` (movil) y restauracion de foco al abrir/cerrar modales o drawers.
   - **Brownfield Triage:** Pregunta si un comportamiento heredado detectado en codigo es *As-Is* intencional o deuda a registrar en `docs/backlog/audit-proposals.md`.
4. **Cierre:**
   - Resume los acuerdos alcanzados (tokens, estados FSM, rutas e invariantes) y procede a documentarlos o a ejecutar `/ui-plan`.
