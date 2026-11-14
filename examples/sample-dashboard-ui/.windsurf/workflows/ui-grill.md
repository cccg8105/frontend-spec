---
description: "Entrevista arquitectonica UI/UX mediante pausa estructurada en chat (A/B/C) para despejar FSM, tokens, rutas y accesibilidad."
---

# /ui-grill — Entrevista Tecnica UI/UX (Windsurf)

1. **"Codigo, Tokens y Grafo primero, humano despues":**
   - Revisa `docs/design/tokens-and-themes.md`, `docs/functional/index.md`, `docs/technical/` y `graphify-out/` (si existe) antes de preguntar.
   - Prohibido preguntar hechos visibles en el repositorio, CSS o configuracion.
2. **Pausa Estructurada en Chat:**
   - Presenta de **2 a 4 decisiones concretas** listando opciones claras con formato `A) (Recomendado) / B) / C)` y sus trade-offs.
   - Detente y espera la respuesta del usuario antes de redactar especificaciones o codigo.
3. **Aristas de Decision Frontend:**
   - **FSM e Invariantes (`ui-contracts-guidelines.md`):** Prevencion de doble clic, borrador en error `5xx`, bloqueo vs. optimista.
   - **Estados Borde (`_template_user_flow.md`):** `LoadingState`, `EmptyState`, errores RFC 7807 (`403`, `409`, `429`, `5xx`).
   - **Rutas, Renderizado y Auth (`routing-and-rendering.md`):** CSR/SSR/SSG/RSC, guardias RBAC, `returnTo` y query params.
   - **Responsive y a11y:** Comportamiento movil (`390px`) y restauracion de foco.
   - **Brownfield Triage:** Verificar si un patron legado es *As-Is* o deuda para `docs/backlog/audit-proposals.md`.
4. **Cierre:**
   - Consolida los acuerdos y continua con `/ui-plan`.
