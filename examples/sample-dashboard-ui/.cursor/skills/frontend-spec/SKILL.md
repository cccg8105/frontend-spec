---
name: frontend-spec
description: "Orquestador completo del ciclo de vida frontend Spec-Driven bajo Dos Velocidades (MAJOR/MINOR con flujos UX, tokens y FSM vs PATCH Fast-Track) con soporte multi-ecosistema."
---

# frontend-spec Skill

Esta skill gobierna el ciclo completo de ingeniería frontend asistida por agentes IA bajo **`frontend-spec`**, garantizando diseño intencional Anti-AI Slop, trazabilidad contractual, accesibilidad WCAG AA y verificación multi-nivel.

## Regla de Oro (Gatekeeper de Dos Velocidades)
**PROHIBIDO** modificar código fuente (`src/`, `app/`, `pages/`, `components/`) sin un `REQ-UI-*` activo en `docs/backlog/pending.md` aprobado por el usuario.

| Impacto (`versioning-strategy.md`) | Carril | Ceremonia Mínima Exigida |
| :--- | :--- | :--- |
| **`MAJOR` / `MINOR`** (Nuevas vistas, rutas, componentes complejos o cambio de tokens) | **Carril Completo** | /ui-grill -> Flujo UX (`UF-*`) + Matriz FSM (`ui-contracts-guidelines.md`) -> Tokens/Rutas/Componentes/Estado -> Test *Spec-First* (`_template_ui_test.md` / `_template_e2e_test.md`) -> `pending.md` -> Gatekeeper `/plan`. |
| **`PATCH`** (Ajuste cosmético con tokens existentes, fix a11y o bug de estado local sin romper rutas/props/API) | **Fast-Track** | `Referencia Funcional: N/A (PATCH / Fast-Track)`. Bloque compacto en `pending.md` -> `/diagnose` + test de regresión en rojo -> confirmación breve -> fix mínimo. |

## Protocolo Operativo Estándar
1. **Contexto Selectivo O(1):** Consulta únicamente `docs/functional/index.md`, `docs/design/index.md` y `docs/technical/index.md` para cargar solo los archivos implicados. Si existe `graphify-out/`, consulta dependencias antes de diseñar.
2. **Aclaración Preventiva (/ui-grill):** Aplica la regla *"Código y Tokens primero, humano después"*. Despeja ambigüedades antes de especificar (Utiliza `AskQuestion` por tarjeta interactiva (2 a 4 decisiones por ronda, opcion `(Recommended)` primero)).
3. **Blueprints Obligatorios (`.spec/templates/`):**
   - Flujo UX: `_template_user_flow.md` (con estado `Loading`, `Empty`, `Error` y foco).
   - Complejidad UI: `ui-contracts-guidelines.md` (determina si FSM `stateDiagram-v2` e invariantes son obligatorios).
   - Tokens y Estética: `design-guidelines.md` y `_template_design_tokens.md` (simetría claro/oscuro, cero valores CSS quemados).
   - Técnico: `_template_ui_component.md`, `_template_routing.md`, `_template_state_contracts.md` (RFC 7807, `Idempotency-Key`, MSW), `_template_tech_stack.md` (Web Vitals, XSS/CSP), `_template_deployment.md`.
4. **Historial Rolling Window:** Mantén máximo **3 filas** en `## Historial de Revisiones` de cada documento.
5. **Fronteras Estrictas y Solo Lectura de Auditoría:** Toca exclusivamente archivos declarados `[NEW]`/`[MODIFY]`/`[DELETE]` en `pending.md`. Trata `docs/backlog/audit-proposals.md` como solo lectura salvo promoción explícita.
6. **Expansión Progresiva Brownfield:** Si el cambio toca una ruta/módulo en `Módulos / Rutas Legadas Detectadas` dentro de `docs/functional/index.md`, documenta primero su flujo *As-Is* antes de planificar la evolución *To-Be*.
7. **Verificación y Cierre:** Ejecuta tests unitarios (`axe-core`) y Playwright E2E + viewports cuando aplique, realiza `/code-review` del diff, actualiza índices y ejecuta `graphify update` respetando `.graphifyignore`.
