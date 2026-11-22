# Guía 04: Referencia de CLI, Harnesses, Estructura y Contratos

Esta guía concentra la referencia técnica completa de instalación, subcomandos CLI, arquitectura del framework y del proyecto consumidor, coexistencia en monorepos y garantías de estabilidad SemVer desde `v1.0.0`.

---

## 1. Instalación y Actualización

### Prerrequisitos del Sistema y GitHub CLI (`gh`)

1. **Python `>=3.9`:** `frontend-spec` utiliza exclusivamente la biblioteca estándar de Python sin dependencias externas en tiempo de ejecución.
2. **Git:** Necesario para inicialización del historial y la activación del hook `.git/hooks/pre-commit`.
3. **GitHub CLI (`gh`) — Prerrequisito para Diagnóstico de Vulnerabilidades (Dependabot):** Para que los agentes de IA y `fspec check --security` puedan consultar alertas de seguridad de GitHub y PRs de Dependabot automáticamente, instala `gh` y autentica tu sesión:

```bash
# Windows (winget)
winget install --id GitHub.cli

# macOS (Homebrew)
brew install gh

# Debian / Ubuntu Linux
sudo apt update && sudo apt install gh

# Autenticación y verificación de permisos sobre alertas de seguridad
gh auth login
gh auth status
# Si tu token actual no tiene permiso para alertas de Dependabot en repos privados/propios:
gh auth refresh -s security_events
# Prueba rápida dentro del repositorio del proyecto:
gh api "repos/{owner}/{repo}/dependabot/alerts?state=open&per_page=1"
```

### Instalación del CLI (`frontend-spec` / `fspec`)

```bash
# Instalación global recomendada desde GitHub (uv)
uv tool install git+https://github.com/cccg8105/frontend-spec.git

# Instalación reproducible fijada a un tag de release (recomendada para equipos/CI)
uv tool install git+https://github.com/cccg8105/frontend-spec.git@v1.3.0

# Instalación directa desde el wheel publicado en GitHub Releases (sin clonar el repo)
uv tool install https://github.com/cccg8105/frontend-spec/releases/download/v1.3.0/frontend_spec-1.3.0-py3-none-any.whl

# Alternativa con pipx o ejecución efímera sin instalación global
pipx install git+https://github.com/cccg8105/frontend-spec.git
uvx --from git+https://github.com/cccg8105/frontend-spec.git frontend-spec --version

# Instalación local desde el repositorio clonado (desarrollo / contribución)
uv tool install --from . frontend-spec
pip install -e .

# Actualización del CLI global y sincronización segura en un proyecto consumidor
uv tool upgrade frontend-spec
fspec update --dir . --dry-run
fspec update --dir .
```

También dispone de los lanzadores locales [`fspec`](../fspec) y [`fspec.ps1`](../fspec.ps1) dentro del repositorio del framework.

---

## 2. Catálogo de Subcomandos (`frontend-spec` / `fspec`)

| Comando | Flags Principales | Propósito |
| :--- | :--- | :--- |
| `fspec init [ruta]` | `--dir`, `--harness {all,antigravity,cursor,claude,windsurf}`, `--versioning {semver,calver,sequential}`, `--ecosystem {nextjs,remix,nuxt,sveltekit,solid,qwik,astro,angular,vue-vite,react-vite}`, `--mode {auto,greenfield,brownfield}`, `--ci {none,github}`, `-i/--interactive`, `-f/--force` | Inicializa `.spec/`, `docs/`, blueprints, reglas del harness, skills (incluyendo `frontend-deploy`), `.graphifyignore`, `.gitignore`, hook `pre-commit` y opcionalmente el guardrail `.github/workflows/frontend-spec-check.yml` (`--ci github`). |
| `fspec update [ruta]` | `--dir`, `--harness`, `--dry-run`, `--refresh-stack`, `--ci {none,github}` | Actualiza de forma idempotente `.spec/templates/`, skills, comandos `/ui-*`, bloques delimitados de reglas, hook `pre-commit` y workflow CI gestionado (`# FRONTEND-SPEC-CI-MANAGED`) **sin destruir `docs/` existentes**. Con `--refresh-stack`, re-detecta `package.json` y sincroniza `.spec/config.yaml` y `tech-stack.md`. |
| `fspec bootstrap [ruta]` | `--dir`, `--mode {auto,full,progressive}`, `--reset` | Escanea un proyecto existente (Brownfield), detecta Storybook e inventaria `*.stories.*`, actualiza `tech-stack.md` / `.spec/config.yaml` y genera `.spec/bootstrap-report.md` preservando casillas `- [x]`. |
| `fspec req:new [titulo]` | `--dir`, `--domain`, `--priority {P1,P2,P3}`, `--impact {MAJOR,MINOR,PATCH}`, `--version`, `--uf`, `--tokens`, `--fast-track`, `--from-audit` | Crea bloques `REQ-UI-*` en `docs/backlog/pending.md` (o promueve hallazgos `AUDIT-UI-*`), sugiere FSM según dominio y sincroniza índices. |
| `fspec sync [ruta]` | `--dir`, `--export-tokens` | Reconstruye de forma idempotente las tablas y resúmenes en `docs/backlog/index.md`, `docs/functional/index.md` y `docs/design/index.md`; con `--export-tokens` genera `.spec/specs/design.tokens.json` en formato W3C DTCG. |
| `fspec check [ruta]` | `--dir`, `--staged`, `--strict-tokens`, `--security` | Valida enlaces relativos, `artifact_type`, sintaxis Mermaid, tokens, sidecars `*.tokens.json` (W3C DTCG), Rolling Window (`<= 3` filas en `## Historial de Revisiones`), esquemas `.spec/specs/*.json` contra Draft-07, consistencia de `Referencia Funcional` no vacía en no-`PATCH`, commits staged (`--staged`), hexadecimales quemados (`--strict-tokens`) y alertas abiertas de Dependabot en GitHub vía `gh` CLI (`--security`, bloqueante ante `critical`/`high`). |
| `fspec resolve <REQ-ID>` | `--dir`, `--bump`, `--force-version` | Archiva un requerimiento en `docs/backlog/changelog.md` manteniendo Rolling Window y actualiza opcionalmente la versión en el manifiesto (`package.json` y `.spec/config.yaml`) bloqueando downgrades salvo `--force-version`. |

---

## 3. Estructura del Repositorio y Proyecto Consumidor

### Estructura del Framework (`frontend-spec`)

```text
frontend-spec/
├── .gitignore                                # Exclusiones Node, meta-frameworks, Playwright y Python CLI
├── CHANGELOG.md                              # Historial SemVer 2.0.0 del framework
├── README.md                                 # Portada ejecutiva y mapa de accesos (Hub & Spoke)
├── pyproject.toml                            # Empaquetado Hatchling (Python >=3.9, cero dependencias)
├── fspec / fspec.ps1                         # Lanzadores CLI locales POSIX y PowerShell
│
├── guides/                                   # Guías operativas modulares por escenario de uso
│   ├── 01-new-projects-greenfield.md
│   ├── 02-existing-projects-brownfield.md
│   ├── 03-daily-workflow-two-speeds.md
│   └── 04-cli-harnesses-and-contracts.md
│
├── cli/                                      # Motor CLI determinista en biblioteca estándar Python
│   ├── main.py                               # Punto de entrada CLI UTF-8
│   ├── tests/                                # Matriz modular de 6 suites (25 pruebas unitarias, integración y E2E)
│   └── frontend_spec/
│       ├── commands/                         # 7 subcomandos: init, update, bootstrap, req:new, sync, check, resolve
│       ├── detector/                         # Detectores multi-ecosistema (10 perfiles + Storybook) y version_extractor
│       └── validator/                        # Validador Draft-07, W3C DTCG, tokens quemados, enlaces, Mermaid y --staged
│
├── schemas/                                  # 8 contratos JSON Schema Draft-07 (cero dependencias)
├── harnesses/                                # Reglas gestionadas por IDE/CLI (antigravity, claude, cursor, windsurf)
├── templates/                                # Activos distribuibles parametrizados (.spec/, hooks, slash commands)
├── examples/
│   └── sample-dashboard-ui/                  # Proyecto piloto de referencia (React + Vite + TS + Tailwind + MSW)
└── agent-prompts/                            # Protocolo Gatekeeper agnóstico y comandos paso a paso
```

### Estructura Generada en un Proyecto Consumidor

Al ejecutar `fspec init` (y `fspec bootstrap` en Brownfield) en una aplicación destino, el repositorio recibe:

```text
mi-app-frontend/
├── .spec/
│   ├── config.yaml                           # Perfil de ecosistema, versionamiento, rutas y harnesses activos
│   ├── bootstrap-report.md                   # Mapa GPS de inventario Brownfield (generado por fspec bootstrap)
│   ├── specs/                                # Sidecars JSON opcionales validados contra schemas/ Draft-07
│   └── templates/                            # 12 blueprints de consulta (user flow, ui contracts, tokens, tests)
├── docs/
│   ├── functional/                           # index.md + user-flows/UF-*.md (con diagramas Mermaid y estados borde)
│   ├── design/                               # index.md + tokens-and-themes.md (claro/oscuro, contraste, CSS vars)
│   ├── technical/                            # index.md, tech-stack.md, component-hierarchy.md, routing, state, deploy
│   └── backlog/                              # index.md, pending.md, audit-proposals.md, changelog.md, versioning-strategy.md
├── .gitignore / .graphifyignore              # Exclusiones frontend para Git y Graphify
├── .git/hooks/pre-commit                     # Guardrail Git portable (fspec check --staged)
├── .github/workflows/
│   └── frontend-spec-check.yml               # Guardrail CI opt-in (--ci github, gestionado con marcador)
└── [Adaptadores del harness]                 # .gemini/, CLAUDE.md + .claude/, .cursor/, .windsurfrules + .windsurf/ (incl. skill frontend-deploy)
```

---

## 4. Coexistencia en Monorepos y Guardrail `pre-commit`

* **Bloques Delimitados:** Todos los archivos compartibles utilizan marcadores `<!-- FRONTEND-SPEC:START -->`..`<!-- FRONTEND-SPEC:END -->` (`CLAUDE.md`, `.windsurfrules`) y `# FRONTEND-SPEC:START`..`# FRONTEND-SPEC:END` (`.git/hooks/pre-commit`). Esto permite ejecutar `fspec init` y `fspec update` en el mismo monorepo donde ya existe `backend-spec` u otras instrucciones del equipo sin sobrescribirlas.
* **Bloqueo Anti-Fantasmas (`fspec check --staged`):** Al hacer `git commit`, el hook verifica los archivos en staging bajo carpetas frontend (`src/`, `app/`, `pages/`, `components/`, etc.). Si detecta cambios en código sin un `REQ-UI-*` activo en `docs/backlog/pending.md` cuyas fronteras `[NEW]`/`[MODIFY]`/`[DELETE]` cubran esos archivos (o sin actualización simultánea de cierre), detiene el commit con código `1`. Para emergencias críticas de producción existe el escape `git commit --no-verify`.

---

## 5. Contratos Públicos y JSON Schemas (`v1.0.0+`)

A partir de `v1.0.0`, `frontend-spec` congela sus contratos públicos bajo **Semantic Versioning 2.0.0** estricto:

1. **Contratos CLI:** Nombres de los 7 subcomandos, alias `fspec`, flags principales y códigos de salida (`0` éxito, `1` fallo de validación o contrato).
2. **Contratos de Schemas (`schemas/`):** Los 8 esquemas JSON Schema Draft-07 (subconjunto cero dependencias):
   - [`schemas/requirement.schema.json`](../schemas/requirement.schema.json)
   - [`schemas/user-flow.schema.json`](../schemas/user-flow.schema.json)
   - [`schemas/design/tokens-and-themes.schema.json`](../schemas/design/tokens-and-themes.schema.json)
   - [`schemas/technical/component-hierarchy.schema.json`](../schemas/technical/component-hierarchy.schema.json)
   - [`schemas/technical/routing-and-rendering.schema.json`](../schemas/technical/routing-and-rendering.schema.json)
   - [`schemas/technical/data-fetching-and-state.schema.json`](../schemas/technical/data-fetching-and-state.schema.json)
   - [`schemas/technical/tech-stack.schema.json`](../schemas/technical/tech-stack.schema.json)
   - [`schemas/technical/deployment-strategy.schema.json`](../schemas/technical/deployment-strategy.schema.json)
3. **Contratos de Plantillas y Prompts:** Separación `.spec/` vs. `docs/` en `templates/`, adaptadores en `harnesses/` y protocolo Gatekeeper en `agent-prompts/`.

Cualquier cambio incompatible en estos contratos requerirá un incremento `MAJOR` (`2.0.0`).

---

- Vuelve al índice principal en [README.md](../README.md).
