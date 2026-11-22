# Guía 03: Flujo de Trabajo Diario (Dos Velocidades y Multi-Harness)

Una vez inicializado el repositorio (Greenfield o Brownfield), todo cambio de código fuente se gobierna bajo el **Protocolo Conversacional Gatekeeper de Dos Velocidades**, respaldado automáticamente por `fspec check --staged`.

> **Regla de Oro:** Prohibido modificar código fuente (`src/`, `app/`, `pages/`, `components/`) sin un requerimiento `REQ-UI-*` activo en `docs/backlog/pending.md` aprobado explícitamente por el usuario. `docs/backlog/audit-proposals.md` es un buzón de solo lectura salvo promoción explícita con `--from-audit`.

---

## Árbol de Decisión de Dos Velocidades

```mermaid
flowchart TD
    S["Solicitud de Cambio UI"] --> Q{"Altera rutas, props publicas, tokens globales o contratos API?"}
    Q -->|"Si (MAJOR / MINOR)"| F1["Carril Completo: Entrevista /ui-grill"]
    F1 --> F2["Flujo UF-* + Evaluacion Heuristica FSM"]
    F2 --> F3["Tokens / Rutas / Componentes / Estado + Test Spec-First"]
    F3 --> F4["fspec req:new + Plan /ui-plan -> Aprobacion Humana"]
    F4 --> EXEC["Implementacion acotada a Fronteras [NEW]/[MODIFY]/[DELETE]"]
    Q -->|"No (PATCH / Hotfix)"| P1["Carril Fast-Track: fspec req:new --impact PATCH"]
    P1 --> P2["Diagnostico /diagnose + Test de regresion en rojo"]
    P2 --> P3["Confirmacion breve de archivos"]
    P3 --> EXEC
    EXEC --> CHK["fspec check + Suite Unit/E2E + /code-review"]
    CHK --> RES["fspec resolve REQ-UI-XXX --bump"]
```

---

## 1. Carril Completo (`MAJOR` / `MINOR`)

Aplica para nuevas vistas, rutas, componentes complejos, cambios en el sistema de diseño o cambios de contrato frontend-backend:

1. **Entrevista Preventiva (`/ui-grill` o `/grill-me`):** El agente consulta los índices `docs/functional/index.md`, `docs/design/index.md` y `docs/technical/index.md` (y `graphify-out/` si existe) aplicando *Código y Tokens primero, humano después*. Solo pregunta decisiones de diseño o UX aún abiertas (estados `Loading`/`Empty`/`Error`, máquina de estados, guardias RBAC, responsive, foco).
2. **Flujo UX (`UF-*`) y Matriz FSM:** Crea o actualiza `docs/functional/user-flows/UF-[DOMINIO]-[NUM]-[slug].md` usando `.spec/templates/_template_user_flow.md` y evalúa la Matriz Heurística FSM de `.spec/templates/ui-contracts-guidelines.md`.
3. **Diseño e Ingeniería Selectiva:** Actualiza únicamente los documentos impactados:
   - `docs/design/tokens-and-themes.md` (paleta claro/oscuro simétrica, contraste WCAG, mapeo CSS/Tailwind).
   - `docs/technical/component-hierarchy.md` (árbol atómico `CMP-*`, `Props`/Slots y FSM `stateDiagram-v2`).
   - `docs/technical/routing-and-rendering.md` (rutas, guardias RBAC, Error Boundaries, CSR/SSR/SSG).
   - `docs/technical/data-fetching-and-state.md` (estado servidor/URL, mapeo RFC 7807, `Idempotency-Key`, handlers MSW).
   - Sidecars opcionales `.spec/specs/*.json` validados contra `schemas/` si el proyecto utiliza validación estructurada JSON.
4. **Registro en Backlog y Test *Spec-First*:** Registra el requerimiento vinculando el flujo funcional:
   ```bash
   fspec req:new "Tabla de analitica con exportacion CSV" --domain DASH --impact MINOR --uf docs/functional/user-flows/UF-DASH-001-analytics-datatable.md
   ```
   El agente prepara el plan de fronteras exactas (`[NEW]`, `[MODIFY]`, `[DELETE]`) y los tests iniciales (Vitest/Testing Library + `axe-core`, y Playwright E2E si el flujo es crítico). **La ejecución se detiene hasta tu aprobación (`/ui-plan` o `/plan`).**
5. **Implementación, Verificación, Integración (`Staging`) y Release (`Producción`):** Tras implementar únicamente los archivos declarados y aprobar pruebas unitarias, a11y, E2E y `/code-review`:
   ```bash
   fspec sync
   fspec check
   # Integración en main -> despliega a Staging (sin subir versión de package.json aún):
   fspec resolve REQ-UI-DASH-001

   # Promoción a Producción -> actualiza package.json y corta el tag anotado:
   fspec resolve REQ-UI-DASH-001 --bump
   git tag -a v1.1.0 -m "Release v1.1.0"
   ```
   *(Para pipelines, sincronización de `.env.example` + GitHub Environments `vars.*`, cabeceras caché/CSP y pre-vuelo con `gh variable/secret list`, apoya la operación en la skill `frontend-deploy`).*

---

## 2. Carril Fast-Track (`PATCH` / Hotfix)

Aplica cuando corriges estilos usando tokens existentes, bugs de estado local o ajustes menores de accesibilidad sin alterar rutas públicas, props compartidas ni contratos de API:

1. Omite crear flujos `UF-*` nuevos. Registra un Micro-Spec compacto directamente en modo Fast-Track:
   ```bash
   fspec req:new "Corrige foco visible en selector de rango" --domain DASH --impact PATCH
   ```
   *(El CLI asigna automáticamente `Referencia Funcional: N/A (PATCH / Fast-Track)`).*
2. El agente aplica `/diagnose` (reproduce, aísla, formula hipótesis), escribe el test de regresión en rojo y solicita confirmación breve indicando los archivos exactos a modificar.
3. Tras verificar el fix en verde:
   ```bash
   fspec check
   fspec resolve REQ-UI-DASH-002 --bump
   ```

---

## 3. Diagnóstico y Remediación de Vulnerabilidades (Dependabot y `gh` CLI)

Cuando GitHub Dependabot detecta paquetes vulnerables, el framework estandariza un flujo seguro para diagnosticar alertas reales en terminal sin romper la arquitectura ni saltar el Gatekeeper.

### Prerrequisito Obligatorio y Comandos de Diagnóstico

El usuario debe tener instalado y autenticado **GitHub CLI (`gh`)** (ver [Guía 04 — Prerrequisitos](04-cli-harnesses-and-contracts.md#1-instalación-y-actualización)). Con `gh` activo, el agente o el propio CLI ejecutan el pre-vuelo y extraen el diagnóstico estructurado:

```bash
# 1. Pre-vuelo de sesión y remoto
gh auth status
gh repo view --json nameWithOwner -q .nameWithOwner

# 2. Listar alertas abiertas de Dependabot (severidad, CVE/GHSA y first_patched_version)
gh api "repos/{owner}/{repo}/dependabot/alerts?state=open&per_page=100"

# 3. Inspeccionar PRs abiertos por Dependabot y checks de CI
gh pr list --author "app/dependabot" --state open

# 4. Atajo automatizado desde el CLI de frontend-spec
fspec check --security
```

*(Si `gh` no está autenticado o no existe remoto en GitHub, el agente advierte del prerrequisito y recurre al auditor local del gestor de paquetes: `npm audit`, `pnpm audit` o `yarn npm audit`).*

### Tres Rutas de Decisión

1. **Ruta 1 — Parche SemVer compatible o dependencia transitiva (`PATCH` Fast-Track):**
   - `first_patched_version` pertenece al mismo rango mayor o puede fijarse mediante `overrides` / `resolutions` sin cambiar llamadas en `src/`.
   - Flujo del agente:
     ```bash
     fspec req:new "Remediacion Dependabot: actualizar vite a 5.4.11" --domain SEC --impact PATCH
     ```
     Declara `package.json` y el lockfile (`package-lock.json` / `pnpm-lock.yaml` / `yarn.lock`) en `Fronteras y Artefactos`, aplica el ajuste mínimo, valida que el auditor local quede en cero + suite de tests + `fspec check --security` y cierra con `fspec resolve REQ-UI-SEC-001 --bump`.
2. **Ruta 2 — Actualización `MAJOR` con *breaking changes* (`MINOR` / `MAJOR` Carril Completo):**
   - El parche exige saltar de versión mayor en una dependencia crítica (ej. framework, router, librerías UI) alterando archivos en `src/`, rutas o `docs/technical/tech-stack.md`.
   - Flujo del agente: detiene cualquier modificación directa en `src/`, analiza impacto con `graphify` (si está activo), sincroniza versiones si corresponde (`fspec update --refresh-stack`) y presenta un plan formal (`/ui-plan` o `/plan`) solicitando tu aprobación explícita.
3. **Ruta 3 — Sin parche disponible o exclusivo de tooling de desarrollo:**
   - Informa el detalle exacto (GHSA, cadena de dependencia, exposición real) y pregunta al usuario si desea aplicar un *workaround* o descartar la alerta en GitHub con motivo documentado (`tolerable_risk` o `inaccurate`).

---

## 4. Equivalencia de Comandos por Harness

`frontend-spec` adapta los disparadores conversacionales a la interfaz nativa de cada herramienta:

| Harness | Archivo de Regla Instalado | Comandos / Workflows UI | Estrategia de Entrevista Interactiva |
| :--- | :--- | :--- | :--- |
| **Antigravity** | `.gemini/rules/frontend-spec.md` | Slash nativos: `/grill-me`, `/plan`, `/boost`, `/goal`, `/diagnose`, `/code-review`, `/compact` | `/grill-me` interactivo nativo |
| **Claude Code** | `CLAUDE.md` (bloque gestionado) | `/ui-bootstrap`, `/ui-grill`, `/ui-plan`, `/ui-resolve` (`.claude/commands/`) | Herramienta `AskUserQuestion` (2-4 decisiones, `(Recommended)` primero) |
| **Cursor** | `.cursor/rules/frontend-spec.mdc` | `/ui-bootstrap`, `/ui-grill`, `/ui-plan` (`.cursor/commands/`) | Herramienta `AskQuestion` por tarjeta interactiva |
| **Windsurf** | `.windsurfrules` (bloque gestionado) | `/ui-bootstrap`, `/ui-grill`, `/ui-plan`, `/ui-execute` (`.windsurf/workflows/`) | Pausa estructurada en chat (`A) (Recomendado) / B) / C)`) |

---

## Siguiente Paso

- Consulta todos los flags del CLI, estructura de archivos y contratos congelados en [Guía 04: Referencia de CLI, Harnesses, Estructura y Contratos](04-cli-harnesses-and-contracts.md).
- Vuelve al índice principal en [README.md](../README.md).
