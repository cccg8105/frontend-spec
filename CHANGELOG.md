# Registro de Cambios (Changelog)

Todos los cambios notables en `frontend-spec` se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto se adhiere a [Semantic Versioning 2.0.0](https://semver.org/lang/es/).

---

## Guía de Versionamiento Semántico (SemVer)

Las versiones del framework se estructuran bajo `MAJOR.MINOR.PATCH` (mientras el prefijo sea `0.y.z`, el framework se encuentra en desarrollo inicial previo a estabilizar su API pública en `1.0.0`):

- **MAJOR (x.0.0):** Cambios que rompen la compatibilidad hacia atrás (*breaking changes*). Ejemplos: reestructuración obligatoria de `.spec/` o `docs/`, cambios incompatibles en campos requeridos de `schemas/` que invaliden especificaciones anteriores, o eliminación/cambio incompatible de comandos o flags en el CLI.
- **MINOR (0.x.0):** Nuevas capacidades compatibles hacia atrás. Ejemplos: nuevos blueprints en `.spec/templates/`, soporte para nuevos harnesses de IA, nuevos detectores de ecosistemas frontend (React, Next.js, Vue/Nuxt, SvelteKit, Astro, Angular), nuevos subcomandos o validaciones opcionales.
- **PATCH (0.0.x):** Correcciones y ajustes compatibles hacia atrás. Ejemplos: corrección de expresiones regulares en validadores, ajustes de plantillas/enlaces o mejoras de documentación sin alterar contratos.

---

## [Unreleased]

### Planned
- Soporte para exportación de tokens en formato W3C Design Tokens (`*.tokens.json`).
- Integración opcional con Storybook para documentación viva de componentes y regresión visual.
- Nuevos perfiles de ecosistema (`SolidJS`, `Remix`, `Qwik`) en el detector CLI.

---

## [1.1.0] - 2026-11-14

### Added
- Flags `--ecosystem` y `--mode {auto,greenfield,brownfield}` en `fspec init` para fijar el perfil técnico en proyectos vacíos sin depender de `-i` o forzar la modalidad Greenfield/Brownfield.
- Flag `--refresh-stack` en `fspec update` (compatible con `--dry-run`) para re-detectar `package.json`/stack real después de inicializar un directorio vacío y sincronizar `.spec/config.yaml` junto con el bloque `<!-- SYNC:TECH_STACK:START/END -->` de `docs/technical/tech-stack.md` sin sobrescribir documentos vivos.
- Heurística `_is_fresh_scaffold()` y campos aditivos `project_state` (`empty`, `scaffold`, `brownfield`) e `is_fresh_scaffold` en `detect_frontend_ecosystem()`, diferenciando un boilerplate recién generado de un proyecto Brownfield real.

### Changed
- `build_profile_context()` ahora asume `TypeScript` (`.tsx`/`.ts`) por defecto en directorios vacíos sin `package.json` ni marcadores exclusivos JavaScript, manteniendo la detección `JavaScript` cuando existe `package.json` sin `tsconfig.json`.
- Actualización de `guides/01-new-projects-greenfield.md` y `guides/04-cli-harnesses-and-contracts.md` documentando los nuevos flags y el flujo optimizado para scaffolds iniciales vs. repositorios vacíos.
- Incremento de versión a `1.1.0` en manifiesto, CLI y plantillas base.

---

## [1.0.1] - 2026-11-14

### Added
- Directorio modular `guides/` con 4 guías operativas por escenario de uso:
  - `guides/01-new-projects-greenfield.md`: flujo recomendado para proyectos nuevos con scaffold (`create-vite`, `create-next-app`, `nuxi`, `ng new`) vs. repositorios totalmente vacíos (*Zero-File Spec-First*), orden de commits para evitar bloqueos de `pre-commit` y Ceremonia de Fundación (`REQ-UI-CORE-001`).
  - `guides/02-existing-projects-brownfield.md`: adopción paso a paso en repositorios existentes (`fspec init`, `fspec bootstrap`, `/ui-bootstrap`, modo `progressive` vs. `full`, expansión *Just-In-Time* y promoción `--from-audit`).
  - `guides/03-daily-workflow-two-speeds.md`: operación diaria del Carril Completo (`MAJOR`/`MINOR`) vs. Fast-Track (`PATCH`) y matriz de comandos por harness.
  - `guides/04-cli-harnesses-and-contracts.md`: referencia técnica completa del CLI, estructura real del framework y del proyecto consumidor, coexistencia en monorepos y contratos `v1.0.0+`.

### Changed
- Reestructuración de `README.md` bajo el patrón Hub & Spoke como portada ejecutiva ligera que enlaza directamente a cada guía de `guides/`, reduciendo la carga cognitiva inicial sin perder profundidad técnica.
- Inclusión de `guides/**` en la distribución fuente (`sdist`) de `pyproject.toml`, manteniendo el paquete instalable `wheel` libre de `guides/` y `examples/`.
- Sincronización de versión `1.0.1` en `pyproject.toml`, CLI y plantillas base.

---

## [1.0.0] - 2026-11-14

### Added
- Proyecto piloto de referencia en `examples/sample-dashboard-ui/` (React + Vite + TypeScript + Tailwind + TanStack Query + MSW + Vitest + Playwright) con `.spec/`, 6 sidecars JSON validados contra `schemas/` y ciclo completo `init -> bootstrap -> req:new -> resolve -> sync -> check` sin advertencias.
- Matriz modular de pruebas en `cli/tests/` dividida en 6 suites (`test_ecosystem_detector.py`, `test_version_extractor.py`, `test_cli_workflow.py`, `test_validator_and_negative.py`, `test_update_and_brownfield.py`, `test_packaging_and_e2e.py`).
- Documentación en `README.md` para instalación remota (`uv tool install`, `pipx`, `uvx`, `uv tool upgrade`), estructura de proyecto consumidor y sección de estabilidad y contratos públicos `v1.0.0`.

### Changed
- Endurecimiento de `cli/frontend_spec/commands/check_cmd.py`: exigencia de `Referencia Funcional` no vacía en requerimientos `REQ-UI-*` no-PATCH (`MAJOR`/`MINOR`), mapeo explícito de `user-flow*.json` y rechazo de archivos `.json` no reconocidos en `.spec/specs/`.
- Actualización de versión a `1.0.0` en `pyproject.toml`, `cli/frontend_spec/__init__.py`, `templates/.spec/config.yaml`, `templates/.spec/docs/backlog/changelog.md`, `templates/.githooks/pre-commit` y `agent-prompts/AGENTS.md`.
- Congelamiento de contratos públicos (CLI, JSON Schemas Draft-07, plantillas y adaptadores multi-harness) bajo SemVer estricto.

### Removed
- Archivo monolítico `cli/tests/test_phase3_cli.py`, reemplazado por la matriz modular de 6 archivos.

---

## [0.4.0] - 2026-11-13

### Added
- **Empaquetado Python Estándar + Hatchling (`pyproject.toml`):** Cero dependencias externas (`dependencies = []`, Python `>=3.9`), scripts de consola `frontend-spec` y `fspec`, inclusión empaquetada de `templates/`, `harnesses/` y `schemas/`, más lanzadores locales `fspec` y `fspec.ps1`.
- **Detectores Multi-Ecosistema y Versionamiento (`cli/frontend_spec/detector/`):**
  - Detección automática para 7 perfiles (`nextjs`, `nuxt`, `sveltekit`, `astro`, `angular`, `vue-vite`, `react-vite`) y fallback Greenfield, identificando estilo (`Tailwind CSS`, `CSS Modules`, `CSS Custom Properties`), librerías de componentes (`Radix`, `Shadcn`, `Vuetify`, etc.), gestión de estado y runners de test (`Vitest`, `Playwright`, `Testing Library`).
  - Extractor de versiones multi-formato (`package.json`, `.spec/config.yaml`, `VERSION`) con soporte SemVer, CalVer y secuencial y guardián anti-downgrade al sincronizar manifiestos.
- **Motor CLI Completo de 7 Subcomandos (`cli/frontend_spec/commands/`):**
  - `init`: inicialización Greenfield/Brownfield, generación de `.spec/config.yaml`, blueprints, 4 módulos `docs/`, `.graphifyignore`, `.gitignore`, harnesses e instalación no destructiva de `.git/hooks/pre-commit`.
  - `update`: actualización idempotente de blueprints, documentos faltantes, bloques delimitados `<!-- FRONTEND-SPEC:START/END -->` (coexistencia segura en monorepos con `backend-spec`), skills por harness y hook `pre-commit`, con soporte `--dry-run`.
  - `bootstrap`: inventario determinista de rutas, componentes UI, archivos de estilos/tokens, mocks/estado y tests, más actualización de `tech-stack.md` y `.spec/bootstrap-report.md` con checkbox preservation y soporte `--reset`/`--mode`.
  - `req:new`: creación interactiva/CLI de requerimientos `REQ-UI-*` (`MAJOR`/`MINOR`/`PATCH`) y promoción desde `AUDIT-UI-*` (`--from-audit`) con detección heurística de FSM/invariantes UI y actualización automática de índices.
  - `sync`: reconstrucción idempotente de tablas en `docs/backlog/index.md` y `docs/functional/index.md` con conteos consistentes.
  - `check`: validación progresiva de artefactos, enlaces relativos, encabezados `artifact_type`, diagramas Mermaid, Rolling Window de `changelog.md` (máximo 3 entradas), validación estructural `.spec/specs/*.json` contra Draft-07 y bloqueo anti-fantasma en `--staged` cuando hay cambios frontend sin `REQ-UI-*` activo.
  - `resolve`: archivado de requerimientos en `changelog.md` aplicando Rolling Window y sincronización segura de versión `--bump` con protección anti-downgrade.
- **Suite de Pruebas CLI (`cli/tests/test_phase3_cli.py`):** 6 pruebas de unidad e integración cubriendo detectores, extractores, ciclo de vida completo, Brownfield/auditoría, coexistencia monorepo con `backend-spec` y bloqueo anti-fantasmas `--staged`.

### Changed
- Normalización interna de cabeceras y metadatos de plantillas a `v0.4.0`.
- Resolución del placeholder `{{HARNESS_INTERVIEW_TRIGGER}}` también en `docs/backlog/versioning-strategy.md` durante `init` y `update`.

---

## [0.3.0] - 2026-11-13

### Added
- Reestructuración distribuible bajo `templates/` separando los activos de desarrollo del propio framework respecto a las plantillas parametrizadas para proyectos consumidores (`{{PROJECT_NAME}}`, `{{ECOSYSTEM_NAME}}`, `{{CURRENT_VERSION}}`, `{{TODAY}}`, `{{HARNESS_INTERVIEW_TRIGGER}}`, `{{HARNESS_QUESTION_STRATEGY}}`).
- Plantillas operativas base para proyectos consumidores: `templates/.gitignore` multi-ecosistema y `templates/.githooks/pre-commit` con bloque gestionado `# FRONTEND-SPEC:START`..`# FRONTEND-SPEC:END`.
- Ocho esquemas formales JSON Schema Draft-07 en `schemas/` compatibles con validador sin dependencias (`type`, `required`, `properties`, `items`, `enum`, `minLength`, `pattern`):
  - `schemas/requirement.schema.json` y `schemas/user-flow.schema.json`
  - `schemas/design/tokens-and-themes.schema.json`
  - `schemas/technical/component-hierarchy.schema.json`, `routing-and-rendering.schema.json`, `data-fetching-and-state.schema.json`, `tech-stack.schema.json` y `deployment-strategy.schema.json`.
- Capa multi-harness en `harnesses/` con bloques gestionados `<!-- FRONTEND-SPEC:START -->`..`<!-- FRONTEND-SPEC:END -->` compatibles en monorepos con `backend-spec`:
  - Antigravity (`harnesses/antigravity/rules/frontend-spec.md`), Claude Code (`harnesses/claude/CLAUDE.md`), Cursor (`harnesses/cursor/rules/frontend-spec.mdc`) y Windsurf (`harnesses/windsurf/.windsurfrules`).
- Once comandos y workflows dedicados con prefijo `/ui-*` para evitar colisiones en monorepos:
  - `templates/.claude/commands/ui-{plan,grill,bootstrap,resolve}.md`
  - `templates/.cursor/commands/ui-{plan,grill,bootstrap}.md`
  - `templates/.windsurf/workflows/ui-{plan,grill,bootstrap,execute}.md`.

### Changed
- Migración limpia de `.spec/`, `.agents/skills/`, `docs/` y `.graphifyignore` desde raíz hacia `templates/.spec/` y `templates/.graphifyignore`.
- Inyección de placeholders `{{HARNESS_INTERVIEW_TRIGGER}}` y `{{HARNESS_QUESTION_STRATEGY}}` en `templates/.spec/skills/{frontend-spec,ui-grill,frontend-bootstrap}/SKILL.md`.
- Actualización de `agent-prompts/AGENTS.md`, `README.md` y `templates/.spec/config.yaml` a `v0.3.0`.

---

## [0.2.0] - 2026-11-13

### Added
- Soporte multi-ecosistema formalizado desde `.spec/config.yaml` y `docs/technical/tech-stack.md` para React/Vite, Next.js, Vue/Nuxt, SvelteKit, Astro y Angular.
- Blueprints faltantes en `.spec/templates/`: `_template_user_flow.md`, `ui-contracts-guidelines.md` (Matriz Heurística FSM e invariantes verificables UI), `_template_routing.md`, `_template_state_contracts.md`, `_template_tech_stack.md`, `_template_deployment.md`, `_template_e2e_test.md` (Playwright + `@axe-core/playwright` + viewports) y `_template_audit_proposals.md`.
- Documentos técnicos y de gobernanza en `docs/`: `routing-and-rendering.md`, `tech-stack.md`, `deployment-strategy.md` y buzón de solo lectura `docs/backlog/audit-proposals.md`.
- Comandos faltantes en `agent-prompts/commands/`: `01_plan_user_flow.md`, `02a_plan_tokens_and_themes.md`, `02b_plan_components_and_routing.md`, `02c_plan_state_and_api.md` y `02d_plan_ui_guarantees_and_deploy.md`.
- Skill `frontend-bootstrap` en `.agents/skills/frontend-bootstrap/SKILL.md` para onboarding Brownfield en 4 fases.
- Archivo `.graphifyignore` adaptado a meta-frameworks frontend, Playwright y artefactos de build.

### Changed
- Migración de `_template_ui_component.md` a YAML Frontmatter estándar con adaptaciones para React, Vue, Svelte y Angular.
- Actualización de `_template_design_tokens.md` y `docs/design/tokens-and-themes.md` con variables CSS ejecutables, elevación, `z-index`, breakpoints, `prefers-reduced-motion` y mapeo Tailwind/`shadcn-ui`.
- Enriquecimiento de `_template_ui_test.md` con ejemplos multi-ecosistema y auditoría `vitest-axe`.
- Adición de marcadores `<!-- SYNC:...:START/END -->`, tablas de historial Rolling Window (máx. 3 filas) y guía detallada de Dos Velocidades en `docs/`.
- Expansión integral de `AGENTS.md`, `03_create_requirement.md`, `04_execute_requirement.md` y las 5 skills originales (`.agents/skills/`) con reglas de diagnóstico `/diagnose`, `/code-review`, seguridad XSS/CSP, Web Vitals, RFC 7807 e `Idempotency-Key`.

---

## [0.1.0] - 2026-11-13

### Added
- Inicialización del repositorio `frontend-spec` con estructura conceptual base (`.spec/`, `.agents/skills/`, `docs/`, `agent-prompts/`).
- Incorporación local de directivas de `frontend-design`, `theme-factory`, `webapp-testing`, `ui-grill` y `frontend-spec`.
- Normalización de línea base SemVer 2.0.0, configuración de Git y `.gitignore` multi-ecosistema.
