# Instrucciones Canónicas para Agentes de IA (`frontend-spec` v1.2.0)

Este proyecto implementa la metodología **`frontend-spec` v1.2.0** con soporte multi-ecosistema (React/Vite, Next.js, Remix, Vue/Nuxt, SvelteKit, SolidJS, Qwik, Astro, Angular) y compatibilidad multi-harness (Antigravity, Claude Code, Cursor, Windsurf). El agente actúa como Arquitecto UI e Ingeniero Frontend gobernando el ciclo de vida mediante el **Protocolo Conversacional Gatekeeper de Dos Velocidades**.

> **Nota de Entorno / Harness:** En los harnesses compatibles (`Claude Code`, `Cursor`, `Windsurf`), utiliza los comandos `/ui-grill`, `/ui-plan`, `/ui-bootstrap` y `/ui-resolve` (o `/ui-execute` en Windsurf). En `Antigravity`, utiliza los slash nativos `/grill-me`, `/plan`, `/diagnose` y `/code-review`. En monorepos con `backend-spec`, las reglas conviven de forma aislada bajo el bloque `<!-- FRONTEND-SPEC:START -->`..`<!-- FRONTEND-SPEC:END -->`.

---

## PROTOCOLO GATEKEEPER DE DOS VELOCIDADES

### REGLA DE ORO: PROHIBIDO CODIFICAR SIN REQUERIMIENTO EN EL BACKLOG
**Nunca modifiques código fuente (`src/`, `app/`, `pages/`, `components/`) sin que exista un requerimiento `REQ-UI-*` registrado en `docs/backlog/pending.md` y aprobado explícitamente por el usuario.**
**Solo lectura de auditoría:** Trata `docs/backlog/audit-proposals.md` como buzón de triage; nunca implementes cambios desde allí sin promoverlos antes a `pending.md`.

Ante cualquier solicitud del usuario, clasifica primero su impacto según `docs/backlog/versioning-strategy.md`:

| Tipo de Cambio | Impacto | Carril Activado | Ceremonia Requerida |
| :--- | :--- | :--- | :--- |
| Nuevas vistas, rutas, componentes complejos o cambio de sistema de diseño | `MAJOR` / `MINOR` | **Carril Completo** | Entrevista (`/ui-grill`) -> Flujo UX (`UF-*`) + Matriz Heurística FSM -> Tokens/Rutas/Componentes/Estado -> Test *Spec-First* (Unit+`axe` / Playwright E2E) -> `pending.md` -> Gatekeeper `/plan`. |
| Ajuste cosmético menor, fix de accesibilidad o bug de estado local sin alterar rutas/contratos | `PATCH` | **Carril Fast-Track (Micro-Spec)** | Omite crear nuevos flujos UX (`Referencia Funcional: N/A (PATCH / Fast-Track)`). Registra bloque compacto en `pending.md`, aplica `/diagnose` + test de regresión en rojo, pide confirmación breve y aplica el fix. |

---

## FLUJO DEL CARRIL COMPLETO (`MAJOR` / `MINOR`)

### Paso 1: Diagnóstico y Entrevista UI (`/ui-grill`)
1. Consulta `docs/functional/index.md`, `docs/design/index.md` y `docs/technical/index.md` cargando únicamente los archivos afectados.
2. Inspecciona primero código fuente, tokens y `graphify-out/` si existe (*Código y Tokens primero, humano después*).
3. Si persisten ambigüedades, pregunta sobre máquina de estados, estados borde (`loading`/`empty`/`error`), guardias de ruta, responsive y foco por teclado.

### Paso 2: Especificación Viva, Tokens y Matriz Heurística FSM
1. **Flujo UX:** Crea o actualiza `docs/functional/user-flows/UF-[DOMINIO]-[NUM]-[slug].md` usando `.spec/templates/_template_user_flow.md`.
2. **Evaluación Autónoma FSM:** Aplica la Matriz Heurística de `.spec/templates/ui-contracts-guidelines.md` (obligatorio en pagos/mutaciones críticas, wizards, widgets complejos o guardias de sesión; omitir en presentacionales puros).
3. **Diseño e Ingeniería:** Actualiza únicamente los documentos técnicos afectados:
   - `docs/design/tokens-and-themes.md` (simetría claro/oscuro, contraste WCAG, mapeo a variables CSS).
   - `docs/technical/component-hierarchy.md` (árbol atómico, Props/Slots, FSM `stateDiagram-v2`).
   - `docs/technical/routing-and-rendering.md` (rutas, layouts, guardias RBAC, Error Boundaries, CSR/SSR/SSG, SEO).
   - `docs/technical/data-fetching-and-state.md` (estado servidor/URL/cliente, mapeo RFC 7807, `Idempotency-Key`, formularios y mocks MSW).
   - `docs/technical/tech-stack.md` y `docs/technical/deployment-strategy.md` si cambian Web Vitals, políticas XSS/CSP, variables públicas o pipeline.
4. **Historial Rolling Window:** Mantén `## Historial de Revisiones` con un máximo de **3 filas** por documento.

### Paso 3: Backlog y Puerta de Enlace (`/plan`)
1. Registra `[REQ-UI-DOMINIO-XXX]` en `docs/backlog/pending.md` siguiendo `agent-prompts/commands/03_create_requirement.md`.
2. Genera el test inicial (*Spec-First*) con `.spec/templates/_template_ui_test.md` (y `_template_e2e_test.md` en flujos críticos).
3. Presenta el plan acotado a las fronteras del `REQ-UI-*` (`/plan`) y **detén la ejecución hasta recibir aprobación explícita**.

---

## FLUJO DEL CARRIL FAST-TRACK (`PATCH` / Hotfix)
1. Verifica que no cambia rutas públicas, contratos de API ni APIs públicas de componentes compartidos.
2. Registra bloque compacto `REQ-UI-[DOMINIO]-[XXX]` con `Referencia Funcional: N/A (PATCH / Fast-Track)` en `docs/backlog/pending.md`.
3. Solicita confirmación breve listando los archivos exactos a tocar.
4. Ejecuta `/diagnose` (reproduce, aísla, formula hipótesis) y escribe primero el test de regresión en rojo antes de aplicar la corrección mínima.

---

## EXPANSIÓN PROGRESIVA BROWNFIELD (Just-In-Time)
Si una solicitud toca una ruta o módulo listado en `docs/functional/index.md` bajo `Módulos / Rutas Legadas Detectadas`:
1. Documenta primero su flujo *As-Is* (`status: "As-Is (Brownfield)"`) con `.spec/templates/_template_user_flow.md` (y test de caracterización si la cobertura es nula).
2. Registra deuda visual/a11y detectada en `docs/backlog/audit-proposals.md` sin alterar código fuera de alcance.
3. Planifica entonces la evolución *To-Be* bajo el flujo habitual.

---

## CICLO OBLIGATORIO DE GRAPHIFY Y REVISIÓN
1. **Antes de Editar:** Si existe `graphify-out/graph.json`, consulta dependencias (`graphify query` / `graphify path`).
2. **Al Finalizar Tests:** Revisa el diff (`/code-review`) verificando reglas anti-AI slop, ausencia de valores CSS quemados y foco accesible, y ejecuta `graphify update` respetando `.graphifyignore`.
