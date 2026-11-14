<!-- FRONTEND-SPEC:START -->
# frontend-spec — Reglas Operativas para Claude Code

> Bloque gestionado por `frontend-spec`. Coexiste con otros bloques gestionados en este archivo (como `BACKEND-SPEC`). No edites dentro de `FRONTEND-SPEC:START` / `FRONTEND-SPEC:END`.

## 1. Regla de Oro (Gatekeeper de Dos Velocidades)
- **PROHIBIDO** modificar codigo fuente (`src/`, `app/`, `pages/`, `components/`) sin un requerimiento `REQ-UI-*` activo en `docs/backlog/pending.md` aprobado por el usuario.
- **Carril Completo (`MAJOR` / `MINOR`):** Ejecuta `/ui-grill` -> `UF-*` (`_template_user_flow.md`) -> Matriz FSM (`ui-contracts-guidelines.md`) -> Tokens / Rutas / Componentes / Estado -> Test *Spec-First* -> `docs/backlog/pending.md` -> espera aprobacion antes de editar codigo. Usa `/ui-plan` para planificar y `/ui-resolve` para implementar un requerimiento aprobado.
- **Fast-Track (`PATCH`):** Usa `Referencia Funcional: N/A (PATCH / Fast-Track)`, valida primero con test de regresion en rojo, solicita confirmacion breve y aplica el fix minimo usando tokens existentes.

## 2. Arquitectura UI, Estado y Diseno Anti-AI Slop
- **Contexto Selectivo O(1):** Consulta `docs/functional/index.md`, `docs/design/index.md`, `docs/technical/index.md` y `graphify-out/` (si existe) antes de cargar archivos de codigo.
- **Estrategia de Entrevista:** En `/ui-grill` y `/ui-plan`, aplica *"Codigo, Tokens y Grafo primero, humano despues"* y formula de 2 a 4 decisiones por ronda mediante `AskUserQuestion` colocando la opcion `(Recommended)` primero.
- **Design Tokens Claro/Oscuro:** Cero valores CSS o colores hex quemados; consume exclusivamente `docs/design/tokens-and-themes.md`.
- **FSM, RFC 7807 e Idempotencia:** Exige `stateDiagram-v2` en vistas/organismos complejos, mapeo de errores RFC 7807 (`400`/`401`/`403`/`409`/`422`/`429`/`5xx`), `Idempotency-Key` en mutaciones criticas y handlers MSW deterministas.

## 3. Fronteras, Brownfield Just-In-Time y Cierre
- **Fronteras Estrictas:** Toca solo rutas listadas como `[NEW]`, `[MODIFY]` o `[DELETE]` en `docs/backlog/pending.md`. Trata `docs/backlog/audit-proposals.md` como solo lectura salvo promocion explicita.
- **Brownfield *Just-In-Time*:** Ante rutas marcadas en `Módulos / Rutas Legadas Detectadas`, documenta su flujo *As-Is* antes del cambio *To-Be*; usa `/ui-bootstrap` para onboarding inicial de repositorios existentes.
- **Cierre y Graphify:** Ejecuta tests unitarios con `axe-core` y Playwright E2E + viewports cuando aplique, actualiza el historial *Rolling Window* (maximo 3 filas) y corre `graphify update` respetando `.graphifyignore`.
<!-- FRONTEND-SPEC:END -->
