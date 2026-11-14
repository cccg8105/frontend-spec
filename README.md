# frontend-spec v1.0.0

> **Framework y Convenciones de Especificación Viva para Ingeniería Frontend Multi-Ecosistema asistida por Agentes de IA (Spec-Driven Frontend)**

`frontend-spec` es la contraparte frontend de `backend-spec`. Estructura la colaboración entre desarrolladores y agentes de IA para erradicar el *"vibe coding"* en aplicaciones web modernas (**React/Vite, Next.js, Vue/Nuxt, SvelteKit, Astro y Angular**), imponiendo diseño intencional Anti-AI Slop, design tokens ejecutables, contratos formales validables mediante JSON Schema Draft-07, adaptadores multi-harness y verificación multi-nivel.

---

## Pilares Arquitectónicos

1. **Multi-Ecosistema con Abstracción Única:** Contratos agnósticos de componentes (`Props`/Slots/FSM), rutas y testing portables entre React, Next.js, Vue/Nuxt, SvelteKit, Astro y Angular.
2. **Anti-AI Slop & Diseño Intencional:** Incorpora directivas de `frontend-design` (tipografía con carácter, paleta restringida de 4-6 hex, asimetría espacial, microcopy directo y respeto a `prefers-reduced-motion`).
3. **Tokens Ejecutables y Temas Simétricos:** Basado en `theme-factory`, centraliza colores claro/oscuro, elevación, `z-index` y breakpoints en `docs/design/tokens-and-themes.md` con mapeo a CSS custom properties, Tailwind `@theme` y `shadcn-ui` / librerías de UI. Prohibido quemar valores arbitrarios.
4. **Contratos Formales Draft-07 & Puente Backend:** Esquemas sin dependencias (`schemas/`) para flujos UX, requisitos, tokens, jerarquía atómica, rutas/renderizado, RFC 7807 + `Idempotency-Key` + MSW, presupuestos Core Web Vitals y CI/CD.
5. **Ceremonia de Dos Velocidades y Multi-Harness:**
   - **Carril Completo (`MAJOR`/`MINOR`):** Entrevista (`/ui-grill` o `/grill-me` en Antigravity) -> Flujo UX (`UF-*`) + FSM -> Tokens/Rutas/Componentes/Estado -> Pruebas Unit (`Testing Library` + `axe-core`) y Playwright E2E (`@axe-core/playwright` + viewports) -> Gatekeeper `/ui-plan`.
   - **Carril Fast-Track (`PATCH`):** Fixes visuales, de accesibilidad o estado local sin alterar rutas ni contratos públicos; aplica `/diagnose` + test de regresión en rojo.

---

## Estructura Actual del Repositorio (`v1.0.0`)

```text
frontend-spec/
├── .gitignore                                # Exclusiones Node, meta-frameworks, Playwright y Python CLI
├── CHANGELOG.md                              # Historial SemVer 2.0.0 del framework
├── README.md                                 # Documentación y mapa estructural del framework
├── pyproject.toml                            # Empaquetado Hatchling (Python >=3.9, cero dependencias)
├── fspec                                     # Lanzador CLI POSIX local (python -m cli.main)
├── fspec.ps1                                 # Lanzador CLI PowerShell local
│
├── cli/                                      # Motor CLI determinista en biblioteca estándar Python
│   ├── main.py                               # Punto de entrada CLI UTF-8
│   ├── tests/                                # Matriz modular de pruebas CLI (unitarias, integración y E2E)
│   │   ├── test_ecosystem_detector.py        # Detección de perfiles y frameworks UI
│   │   ├── test_version_extractor.py         # Extracción SemVer y resolución de versiones
│   │   ├── test_cli_workflow.py              # Flujo completo init -> bootstrap -> req:new -> resolve -> sync -> check
│   │   ├── test_validator_and_negative.py    # Reglas Draft-07, Mermaid, Rolling Window y casos negativos
│   │   ├── test_update_and_brownfield.py     # Actualizaciones idempotentes y modo brownfield
│   │   └── test_packaging_and_e2e.py         # Empaquetado Hatchling y ejecución CLI en subproceso
│   └── frontend_spec/
│       ├── commands/                         # 7 subcomandos: init, update, bootstrap, req:new, sync, check, resolve
│       ├── detector/                         # Detectores multi-ecosistema (7 perfiles) y version_extractor
│       └── validator/                        # Validador Draft-07, enlaces, Mermaid, Rolling Window y --staged
│
├── schemas/                                  # Contratos JSON Schema Draft-07 (subconjunto cero dependencias)
│   ├── requirement.schema.json               # Esquema para requerimientos REQ-UI-* en pending.md/changelog.md
│   ├── user-flow.schema.json                 # Esquema para flujos UX (UF-*) con estados borde y a11y
│   ├── design/
│   │   └── tokens-and-themes.schema.json     # Tokens semánticos claro/oscuro, tipografía y breakpoints
│   └── technical/
│       ├── component-hierarchy.schema.json   # Catálogo atómico CMP-* y reglas FSM
│       ├── routing-and-rendering.schema.json # Rutas, layouts, CSR/SSR/SSG/RSC, guardias RBAC y fallbacks
│       ├── data-fetching-and-state.schema.json # Estado servidor/URL, mapeo RFC 7807, Idempotency-Key y MSW
│       ├── tech-stack.schema.json            # Ecosistema, presupuestos Web Vitals y seguridad XSS/CSP
│       └── deployment-strategy.schema.json   # Pipeline Mermaid, variables públicas, cabeceras y rollback
│
├── harnesses/                                # Reglas gestionadas (<!-- FRONTEND-SPEC:START/END -->) por IDE/CLI
│   ├── antigravity/rules/frontend-spec.md    # Regla para Antigravity (.gemini/rules/frontend-spec.md)
│   ├── claude/CLAUDE.md                      # Bloque gestionado para Claude Code (coexiste con backend-spec)
│   ├── cursor/rules/frontend-spec.mdc        # Regla MDC con globs UI para Cursor
│   └── windsurf/.windsurfrules               # Bloque gestionado para Windsurf (Cascade)
│
├── templates/                                # Activos distribuibles parametrizados para proyectos consumidores
│   ├── .gitignore                            # Plantilla .gitignore base para aplicaciones frontend
│   ├── .graphifyignore                       # Exclusiones frontend para Graphify
│   ├── .githooks/pre-commit                  # Hook Git portable (check --staged, bloque FRONTEND-SPEC:START/END)
│   ├── .claude/commands/                     # Slash commands: ui-plan, ui-grill, ui-bootstrap, ui-resolve
│   ├── .cursor/commands/                     # Slash commands: ui-plan, ui-grill, ui-bootstrap
│   ├── .windsurf/workflows/                  # Workflows Cascade: ui-plan, ui-grill, ui-bootstrap, ui-execute
│   └── .spec/
│       ├── config.yaml                       # Perfil parametrizado multi-ecosistema, rutas y SemVer
│       ├── templates/                        # 12 blueprints canónicos (_template_user_flow, ui-contracts, etc.)
│       ├── skills/                           # 6 skills con placeholders por harness (SKILL.md)
│       └── docs/                             # Plantilla inicial docs/{functional,design,technical,backlog}/
│
├── examples/
│   └── sample-dashboard-ui/                  # Proyecto piloto de referencia (React + Vite + TS + Tailwind + MSW)
│
└── agent-prompts/                            # Prompts portables agnósticos al harness
    ├── AGENTS.md                             # Protocolo Gatekeeper canónico
    └── commands/                             # Etapas 01 a 04 paso a paso
```

### Estructura Generada en un Proyecto Consumidor

Al ejecutar `frontend-spec init` y `frontend-spec bootstrap`, el repositorio destino incorpora:

```text
mi-app-frontend/
├── .spec/
│   ├── config.yaml                           # Configuración de versionamiento, idioma y harness activo
│   ├── bootstrap-report.md                   # Mapa GPS de descubrimiento brownfield/greenfield
│   ├── specs/                                # Sidecars JSON validados contra Draft-07
│   └── docs/
│       ├── backlog/                          # pending.md, completed.md, changelog.md (Rolling Window)
│       ├── architecture/                     # component-hierarchy.md y decisiones UI
│       ├── flows/                            # Flujos de usuario (UF-*) con diagramas Mermaid
│       ├── audit/                            # Hallazgos y deuda técnica UI (AUDIT-UI-*)
│       └── testing/                          # Estrategia y cobertura de pruebas UI
└── docs/
    └── AGENTS.md / ...                       # Adaptadores del harness seleccionado
```

---

## Instalación y Motor CLI (`v1.0.0`)

`frontend-spec` no requiere dependencias externas en tiempo de ejecución (solo Python `>=3.9`):

```bash
# Instalación global recomendada desde GitHub (uv)
uv tool install git+https://github.com/cccg8105/frontend-spec.git

# Alternativa con pipx o ejecución efímera con uvx
pipx install git+https://github.com/cccg8105/frontend-spec.git
uvx --from git+https://github.com/cccg8105/frontend-spec.git frontend-spec --version

# Instalación local editable o desde el repositorio clonado
uv tool install --from . frontend-spec
pip install -e .

# Actualización global y sincronización en un proyecto consumidor
uv tool upgrade frontend-spec
frontend-spec update
```

Comandos principales (`frontend-spec` o su alias corto `fspec`):

| Comando | Propósito |
| :--- | :--- |
| `fspec init [ruta]` | Inicializa `.spec/`, `docs/`, blueprints, reglas multi-harness, skills y hook `pre-commit` (soporta `--harness`, `--versioning`, `-i`, `--force`). |
| `fspec update [ruta]` | Actualiza blueprints, skills, bloques gestionados y hook de forma idempotente sin destruir `docs/` existentes (soporta `--dry-run`, `--harness`). |
| `fspec bootstrap [ruta]` | Inventaría rutas, componentes UI, estilos/tokens, mocks/estado y tests en proyectos Brownfield generando `.spec/bootstrap-report.md` (soporta `--mode`, `--reset`). |
| `fspec req:new` | Crea bloques `REQ-UI-*` (`MAJOR`/`MINOR`/`PATCH`) o promueve propuestas `AUDIT-UI-*` (`--from-audit`) actualizando índices y sugiriendo FSM/invariantes. |
| `fspec sync [ruta]` | Reconstruye de forma idempotente los catálogos `docs/backlog/index.md` y `docs/functional/index.md`. |
| `fspec check [ruta]` | Valida enlaces, `artifact_type`, Mermaid, tokens, Rolling Window (máx. 3 entradas), esquemas `.spec/specs/*.json` y cambios frontend `--staged`. |
| `fspec resolve <REQ-ID>` | Archiva el requerimiento en `docs/backlog/changelog.md` manteniendo Rolling Window y aplica `--bump` seguro en el manifiesto sin permitir downgrades. |

---

## Compatibilidad Multi-Harness (`v1.0.0`)

Todos los adaptadores utilizan bloques delimitados `<!-- FRONTEND-SPEC:START -->`..`<!-- FRONTEND-SPEC:END -->` (y `# FRONTEND-SPEC:START`..`# FRONTEND-SPEC:END` en `pre-commit`) para convivir limpiamente en monorepos junto a `<!-- BACKEND-SPEC:START -->` u otras reglas del equipo.

| Harness | Regla Principal Instalada | Comandos / Workflows UI | Estrategia de Entrevista |
| :--- | :--- | :--- | :--- |
| **Antigravity** | `.gemini/rules/frontend-spec.md` | Slash nativos: `/grill-me`, `/boost`, `/plan`, `/goal`, `/compact`, `/diagnose`, `/code-review` | `/grill-me` interactivo nativo |
| **Claude Code** | `CLAUDE.md` (bloque gestionado) | `/ui-plan`, `/ui-grill`, `/ui-bootstrap`, `/ui-resolve` (`.claude/commands/`) | `AskUserQuestion` (2-4 decisiones, `(Recommended)` primero) |
| **Cursor** | `.cursor/rules/frontend-spec.mdc` | `/ui-plan`, `/ui-grill`, `/ui-bootstrap` (`.cursor/commands/`) | `AskQuestion` por tarjeta interactiva |
| **Windsurf** | `.windsurfrules` (bloque gestionado) | `/ui-plan`, `/ui-grill`, `/ui-bootstrap`, `/ui-execute` (`.windsurf/workflows/`) | Pausa estructurada en chat (`A) (Recomendado) / B) / C)`) |

---

## Proyecto Piloto de Referencia (`examples/sample-dashboard-ui/`)

El repositorio incluye un proyecto piloto completo en [`examples/sample-dashboard-ui/`](examples/sample-dashboard-ui/) construido sobre React, Vite, TypeScript, Tailwind CSS, TanStack Query, MSW, Vitest y Playwright, completamente alineado con `.spec/`, los 6 sidecars JSON en `.spec/specs/` y el ciclo completo `init -> bootstrap -> req:new -> resolve -> sync -> check` con cero advertencias.

## Estabilidad y Contratos Públicos (`v1.0.0`)

A partir de `v1.0.0`, `frontend-spec` congela sus contratos públicos bajo SemVer estricto:
- **Contratos CLI:** subcomandos (`init`, `update`, `bootstrap`, `req:new`, `sync`, `check`, `resolve`), alias `fspec`, flags principales y códigos de salida (`0` éxito, `1` fallo de validación/contrato).
- **Contratos de Schemas:** esquemas JSON Draft-07 en `schemas/` (`config`, `tokens-and-themes`, `component-hierarchy`, `routing-and-rendering`, `data-fetching-and-state`, `tech-stack`, `deployment-strategy`, `user-flow`).
- **Contratos de Plantillas y Prompts:** estructura de `.spec/` en `templates/`, adaptadores en `harnesses/` y protocolo Gatekeeper en `agent-prompts/`.

Cualquier cambio incompatible en estos contratos requerirá un incremento `MAJOR` (`2.0.0`).

---

## Hoja de Ruta SemVer del Framework

- **`v0.1.0`** — Inicialización Git, normalización SemVer y estructura conceptual base. *(Completado)*
- **`v0.2.0`** — Completitud metodológica, blueprints multi-ecosistema, puente frontend-backend, RNFs UI, skills operativas y `frontend-bootstrap`. *(Completado)*
- **`v0.3.0`** — Separación `templates/` distribuible vs. proyecto consumidor, JSON Schemas Draft-07 (`schemas/`), comandos `/ui-*` y adaptadores multi-harness (`harnesses/`). *(Completado)*
- **`v0.4.0`** — Motor CLI en Python estándar (`>=3.9`, cero dependencias con Hatchling), 7 subcomandos (`init`, `update`, `bootstrap`, `req:new`, `sync`, `check`, `resolve`), detectores multi-ecosistema y guardrail `pre-commit`. *(Completado)*
- **`v1.0.0`** — Suite de pruebas de extremo a extremo (matriz modular de 6 archivos), proyecto piloto de referencia (`examples/sample-dashboard-ui/`), endurecimiento del validador y congelamiento de contratos públicos. *(Actual)*
