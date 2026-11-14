# Guía 01: Proyectos Nuevos (Con Scaffold vs. Repositorio Vacío)

En ingeniería frontend moderna existen dos maneras de comenzar un proyecto nuevo con `frontend-spec`. Elegir el orden correcto evita bloqueos del hook `pre-commit` y falsos diagnósticos de código legado (*Brownfield*).

| Aspecto | Escenario A: Nuevo con Scaffold *(Recomendado)* | Escenario B: Totalmente Vacío (*Zero-File Spec-First*) |
| :--- | :--- | :--- |
| **Punto de partida** | Ya creaste la base con `create-vite`, `create-next-app`, `nuxi` o `ng new`. | Carpeta vacía (`0` archivos o solo `.git`), sin `package.json`. |
| **Autodetección CLI** | Detecta framework, `TypeScript`, Tailwind y runner de tests desde `package.json`. | Sin manifiesto: requiere usar `-i` (`--interactive`) para elegir perfil inicial. |
| **¿Se usa `fspec bootstrap`?** | **No.** El código es boilerplate de fábrica sin lógica ni rutas de negocio. | **No.** No existe código previo que inventariar. |
| **Primer paso documental** | Ceremonia de Fundación (Día 0): tokens, App Shell y `REQ-UI-CORE-001`. | Especificación *To-Be* (`UF-*`, tokens, rutas) antes de instalar paquetes. |

---

## Escenario A: Repositorio Nuevo con Scaffold

Este flujo es el **recomendado** para proyectos desde cero porque evita que los generadores oficiales (`create-vite`, `create-next-app`, etc.) fallen por encontrar carpetas `.spec/` o `docs/` previas y permite que `fspec init` autodetecte tu stack real.

### Paso 1: Generar el scaffold y fijar el commit base en Git

Genera el proyecto con la herramienta oficial de tu framework e inicializa Git **antes** de instalar `frontend-spec`:

```bash
# Ejemplo con React + Vite + TypeScript
npm create vite@latest mi-app-web -- --template react-ts
cd mi-app-web
git init
git add .
git commit -m "chore: initial framework scaffold"
```

> **Por qué este orden importa:** `fspec init` instala `.git/hooks/pre-commit` con `fspec check --staged`. Si ya hiciste este commit inicial, el hook nunca bloqueará los archivos boilerplate de fábrica ni te exigirá un `REQ-UI-*` por ellos.

### Paso 2: Inicializar `frontend-spec` sobre el scaffold

Con `package.json` y `tsconfig.json` ya presentes en disco, ejecuta:

```bash
fspec init --dir . --harness all --versioning semver
```

El CLI creará `.spec/`, `docs/`, las reglas de harness (Antigravity, Claude Code, Cursor, Windsurf) y el hook `pre-commit`, pre-poblando `docs/technical/tech-stack.md` con tu framework, gestor de paquetes, librerías CSS y runners detectados.

> **Importante:** Aunque `init` informe que detectó archivos existentes, **no necesitas ejecutar `fspec bootstrap`** ni inventariar la pantalla de bienvenida de Vite/Next.js como código legado *As-Is*. El objetivo ahora es reemplazar ese boilerplate de forma ordenada.

### Paso 3: Ceremonia de Fundación (Día 0)

Antes de implementar funcionalidades de negocio, define la base visual y estructural junto a tu agente de IA:

1. **Identidad visual y Design Tokens (`docs/design/tokens-and-themes.md`):** Pide al agente definir paleta claro/oscuro, tipografías, espaciado, radios y variables CSS/Tailwind evitando valores arbitrarios.
2. **Arquitectura inicial (`docs/technical/routing-and-rendering.md` y `docs/technical/component-hierarchy.md`):** Define rutas raíz, layouts, Error Boundaries y estrategia CSR/SSR/SSG.
3. **Primer requerimiento fundacional (`REQ-UI-CORE-001`):**
   - Crea primero el flujo base (ej. `docs/functional/user-flows/UF-CORE-001-app-shell.md` siguiendo `.spec/templates/_template_user_flow.md`).
   - Registra el requerimiento en `docs/backlog/pending.md`:
     ```bash
     fspec req:new "Fundacion de tokens, App Shell y configuracion de pruebas" --domain CORE --impact MINOR --uf docs/functional/user-flows/UF-CORE-001-app-shell.md
     ```
4. **Planificación, ejecución y cierre:**
   - Revisa y aprueba el plan en el chat del agente (`/ui-plan` en Claude/Cursor/Windsurf o `/plan` en Antigravity).
   - Implementa los tokens y el App Shell reemplazando la vista de ejemplo del scaffold, añadiendo la configuración base de tests unitarios (`axe-core`) y E2E.
   - Valida y cierra el requerimiento:
     ```bash
     fspec check
     fspec resolve REQ-UI-CORE-001 --bump
     ```

---

<a id="escenario-b-repositorio-totalmente-vacio"></a>
## Escenario B: Repositorio Totalmente Vacío

Usa este flujo solo si deseas diseñar flujos de usuario, tokens y arquitectura **antes** de decidir o instalar el boilerplate Node/JavaScript.

### Paso 1: Inicialización interactiva (`-i`)

En una carpeta vacía (o recién creada con `git init`), usa el modo interactivo para indicar el ecosistema objetivo, esquema de versionamiento y versión inicial:

```bash
mkdir mi-app-web && cd mi-app-web
git init
fspec init --dir . -i --harness all
```

Durante el asistente interactivo podrás seleccionar el perfil objetivo (`Next.js`, `Nuxt`, `SvelteKit`, `Astro`, `Angular`, `Vue + Vite` o `React + Vite`), el esquema (`semver`, `calver` o `sequential`) y la versión inicial (por defecto `0.1.0`).

### Paso 2: Diseño Spec-First sin código fuente

En esta etapa aún no existe `src/` ni `package.json`:

1. Trabaja con el agente (`/ui-grill` o `/grill-me`) para redactar los primeros flujos UX en `docs/functional/user-flows/UF-*.md`.
2. Define la identidad visual en `docs/design/tokens-and-themes.md` y los contratos base en `docs/technical/` (opcionalmente respaldados con sidecars `.spec/specs/*.json` validados contra `schemas/`).
3. Registra `REQ-UI-CORE-001` en `docs/backlog/pending.md` declarando en **Fronteras y Artefactos** la creación del proyecto base (`package.json`, configuración del framework, tokens y App Shell) y aprueba el plan antes de generar código.

### Paso 3: Materialización del scaffold y alineación del stack

1. Crea los archivos del proyecto Node dentro del directorio (o genera el scaffold en una carpeta temporal y mueve `package.json`, `src/`, etc. respetando `.spec/`, `docs/` y `.gitignore`).
2. Revisa `.spec/config.yaml` y `docs/technical/tech-stack.md` para asegurar que `language` (`TypeScript`/`JavaScript`), `styling`, `routes_dir` y `test_pattern` coincidan con los paquetes reales instalados.
3. Verifica que toda la documentación, sidecars y código staged cumplan los contratos:
   ```bash
   fspec sync
   fspec check --staged
   ```

---

## Siguiente Paso

- Continúa la operación diaria en [Guía 03: Flujo de Trabajo Diario (Dos Velocidades y Multi-Harness)](03-daily-workflow-two-speeds.md).
- Vuelve al índice principal en [README.md](../README.md).
