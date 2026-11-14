---
description: "Entrevista tecnica UI/UX (FSM, estados borde, rutas/RBAC, RFC 7807, responsive y a11y) mediante tarjetas interactivas AskQuestion."
---

# /ui-grill — Entrevista Arquitectonica UI/UX (Cursor)

Objetivo: Resolver decisiones abiertas de diseno, estado y accesibilidad para `$ARGUMENTS` antes de redactar especificaciones o codigo.

## Reglas del Entrevistador

1. **"Codigo, Tokens y Grafo primero, humano despues":**
   - Inspecciona `docs/design/tokens-and-themes.md`, `docs/functional/index.md`, `docs/technical/` y `graphify-out/` (si existe) antes de preguntar.
   - No preguntes datos observables en codigo, CSS, mocks MSW o documentacion existente.
2. **Entrevista por Tarjeta Interactiva (`AskQuestion`):**
   - Presenta de **2 a 4 decisiones concretas** usando `AskQuestion`, ubicando primero la opcion recomendada con su justificacion y trade-offs.
3. **Areas Clave Frontend:**
   - **FSM e Invariantes (`ui-contracts-guidelines.md`):** Proteccion de doble clic/envio, conservacion de borrador ante `5xx`, estrategia optimista vs. bloqueo.
   - **Estados Borde (`_template_user_flow.md`):** `LoadingState`, `EmptyState` y recuperacion ante errores RFC 7807 (`403`, `409`, `429`, `5xx`).
   - **Rutas, Renderizado y Auth (`routing-and-rendering.md`):** CSR/SSR/SSG/RSC, guardia RBAC, validacion `returnTo` y query params en URL.
   - **Responsive y a11y:** Adaptacion en `390px` y restauracion de foco en modales/drawers.
   - **Brownfield Triage:** Confirma si un comportamiento heredado es *As-Is* intencional o deuda para `docs/backlog/audit-proposals.md`.
4. **Cierre:**
   - Resume los acuerdos alcanzados y formaliza los artefactos afectados o continua con `/ui-plan`.
