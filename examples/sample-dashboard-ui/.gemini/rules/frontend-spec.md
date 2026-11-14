---
trigger: always_on
description: "Reglas obligatorias de frontend-spec para Antigravity (Dos Velocidades, FSM, tokens claro/oscuro, RFC 7807, Brownfield JIT y Graphify)."
---

<!-- FRONTEND-SPEC:START -->
# Reglas Operativas — frontend-spec (Antigravity)

> Este bloque es gestionado por `frontend-spec`. No modifiques manualmente el contenido entre marcadores `FRONTEND-SPEC:START` y `FRONTEND-SPEC:END`.

## 1. Gatekeeper de Dos Velocidades
- **PROHIBIDO** editar codigo fuente (`src/`, `app/`, `pages/`, `components/`) sin un `REQ-UI-*` activo en `docs/backlog/pending.md` aprobado por el usuario.
- **Carril Completo (`MAJOR` / `MINOR`):** Flujo obligatorio `/grill-me` -> `UF-*` (`.spec/templates/_template_user_flow.md`) -> Matriz FSM (`ui-contracts-guidelines.md`) -> Tokens / Rutas / Componentes / Estado -> Test *Spec-First* (`_template_ui_test.md` o `_template_e2e_test.md`) -> `docs/backlog/pending.md` -> Gatekeeper `/plan`.
- **Fast-Track (`PATCH`):** Solo ajustes internos con tokens existentes, fixes de accesibilidad o bugs de estado local sin romper rutas, props ni contratos API. Usa `Referencia Funcional: N/A (PATCH / Fast-Track)`, reproduce el fallo con `/diagnose` + test de regresion en rojo, pide confirmacion breve y aplica el fix minimo.

## 2. Protocolo de Diseno, Contratos y Contexto O(1)
- **Contexto Selectivo O(1):** Lee unicamente `docs/functional/index.md`, `docs/design/index.md`, `docs/technical/index.md` y los artefactos implicados antes de disenar. Si existe `graphify-out/graph.json`, consulta dependencias antes de leer archivos completos.
- **Entrevista (`/grill-me`):** Aplica *"Codigo, Tokens y Grafo primero, humano despues"*. No preguntes al usuario datos observables en codigo, CSS o documentacion.
- **Design Tokens Simetricos:** Consume estrictamente tokens de `docs/design/tokens-and-themes.md` con simetria modo claro y oscuro. Prohibido usar valores CSS, colores hex o espaciados quemados.
- **FSM e Invariantes:** Componentes complejos y formularios multipaso exigen diagrama `stateDiagram-v2` e invariantes de concurrencia (prevencion de doble envio, preservacion de borrador, restauracion de foco).
- **Integracion HTTP y Mocks:** Mapea errores segun RFC 7807 (`application/problem+json`), exige cabecera `Idempotency-Key` en mutaciones criticas y manten handlers MSW alineados al contrato backend.

## 3. Fronteras, Brownfield Just-In-Time y Cierre
- **Fronteras Estrictas:** Toca unicamente archivos declarados `[NEW]`, `[MODIFY]` o `[DELETE]` en `docs/backlog/pending.md`. Trata `docs/backlog/audit-proposals.md` como solo lectura salvo promocion explicita a `REQ-UI-*`.
- **Brownfield *Just-In-Time*:** Si el cambio afecta una ruta en `Módulos / Rutas Legadas Detectadas` dentro de `docs/functional/index.md`, documenta primero su flujo *As-Is* antes de planificar la evolucion *To-Be*. Para adopcion inicial usa `.gemini/skills/frontend-bootstrap/SKILL.md`.
- **Verificacion y Graphify:** Valida tests unitarios (`axe-core`) y Playwright E2E + viewports cuando aplique, realiza `/code-review` del diff, manten maximo 3 filas en historiales *Rolling Window* y actualiza `graphify update` respetando `.graphifyignore`.
<!-- FRONTEND-SPEC:END -->
