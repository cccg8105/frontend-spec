---
description: "Planifica un requerimiento frontend bajo frontend-spec (Dos Velocidades) usando AskQuestion antes de modificar codigo fuente."
---

# /ui-plan — Planificacion Spec-Driven UI (Cursor)

Objetivo: Planificar `$ARGUMENTS` aplicando el Gatekeeper de **Dos Velocidades** de `frontend-spec`. **PROHIBIDO editar codigo fuente** hasta que el usuario apruebe el requerimiento en `docs/backlog/pending.md`.

## Flujo de Trabajo

1. **Contexto Selectivo O(1):**
   - Consulta `docs/functional/index.md`, `docs/design/index.md`, `docs/technical/index.md` y `graphify-out/` (si existe) antes de inspeccionar multiples componentes.
   - Si el cambio toca modulos en `Módulos / Rutas Legadas Detectadas`, documenta primero su flujo *As-Is* antes de disenar la evolucion *To-Be*.
2. **Evaluacion de Impacto (`MAJOR` / `MINOR` vs. `PATCH`):**
   - **Carril Completo (`MAJOR` / `MINOR`):** Despeja ambiguedades con `/ui-grill` (`AskQuestion`), formaliza `UF-*`, Diagrama/Invariantes FSM (`ui-contracts-guidelines.md`), `tokens-and-themes.md`, `routing-and-rendering.md`, `component-hierarchy.md`, `data-fetching-and-state.md` y test *Spec-First*.
   - **Fast-Track (`PATCH`):** Solo ajustes internos con tokens existentes, fixes a11y, bugs locales o parches de seguridad Dependabot compatibles (`REQ-UI-SEC-*`, diagnosticados con `gh api "repos/{owner}/{repo}/dependabot/alerts?state=open"` y auditor local) sin romper rutas/props/API. Usa `Referencia Funcional: N/A (PATCH / Fast-Track)`, reproduce el error con test en rojo y prepara bloque compacto (upgrades `MAJOR` con impacto en `src/` pasan a Carril Completo).
3. **Registro y Espera de Aprobacion:**
   - Agrega el `REQ-UI-*` en `docs/backlog/pending.md` declarando rutas `[NEW]`, `[MODIFY]`, `[DELETE]` y criterios de aceptacion.
   - Detente y solicita aprobacion explicita antes de implementar cambios en codigo fuente.
