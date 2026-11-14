---
description: "Planifica un requerimiento frontend (Carril Completo MAJOR/MINOR o Fast-Track PATCH) usando frontend-spec sin tocar codigo fuente antes de aprobacion."
---

# /ui-plan — Planificacion Spec-Driven UI

Objetivo: Planificar `$ARGUMENTS` siguiendo el protocolo de **Dos Velocidades** de `frontend-spec`. **NO edites codigo fuente** hasta recibir aprobacion explicita del usuario sobre el `REQ-UI-*` en `docs/backlog/pending.md`.

## Pasos Obligatorios

1. **Contexto Selectivo O(1):**
   - Lee `docs/functional/index.md`, `docs/design/index.md` y `docs/technical/index.md`.
   - Si existe `graphify-out/graph.json`, consulta los nodos relacionados antes de abrir archivos fuente.
   - Si el cambio afecta una ruta en `Módulos / Rutas Legadas Detectadas`, documenta primero su flujo *As-Is* antes de disenar el cambio *To-Be*.
2. **Clasificacion de Impacto (`docs/backlog/versioning-strategy.md`):**
   - **`MAJOR` / `MINOR` (Carril Completo):** Ejecuta primero `/ui-grill` si existen decisiones abiertas sobre FSM, estados borde, rutas/RBAC, tokens o responsive (usa `AskUserQuestion` con la opcion `(Recommended)` primero). Luego formaliza `UF-*`, Diagrama/Invariantes FSM (`ui-contracts-guidelines.md`), `tokens-and-themes.md`, `routing-and-rendering.md`, `component-hierarchy.md`, `data-fetching-and-state.md` y el blueprint de test *Spec-First* (`_template_ui_test.md` / `_template_e2e_test.md`).
   - **`PATCH` (Fast-Track):** Ajustes cosmeticos con tokens existentes, fixes a11y o bugs locales sin romper rutas/props/API. Usa `Referencia Funcional: N/A (PATCH / Fast-Track)`, reproduce el fallo con test de regresion en rojo y prepara bloque compacto en `docs/backlog/pending.md`.
3. **Gatekeeper de Fronteras:**
   - Registra el requerimiento `REQ-UI-*` en `docs/backlog/pending.md` con rutas exactas `[NEW]`, `[MODIFY]` y `[DELETE]` y criterios de aceptacion verificables.
   - Detente y presenta el plan al usuario para su aprobacion explicita antes de pasar a `/ui-resolve`.
