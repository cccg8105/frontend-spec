# Guía 01: Proyectos Nuevos (Con Scaffold vs. Repositorio Vacío)

En ingeniería frontend moderna existen dos maneras de comenzar un proyecto nuevo con `frontend-spec`. Elegir el orden correcto evita bloqueos del hook `pre-commit` y falsos diagnósticos de código legado (*Brownfield*).

| Aspecto | Escenario A: Nuevo con Scaffold *(Recomendado)* | Escenario B: Totalmente Vacío (*Zero-File Spec-First*) |
| :--- | :--- | :--- |
| **Punto de partida** | Ya creaste la base con `create-vite`, `create-next-app`, `nuxi` o `ng new`. | Carpeta vacía (`0` archivos o solo `.git`), sin `package.json`. |
| **Autodetección CLI** | Detecta framework, `TypeScript`, Tailwind y runner de tests desde `package.json`. | Sin manifiesto: asume `TypeScript` por defecto y permite `--ecosystem <perfil>` o `-i`. |
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
# Si ya añadiste archivos extra antes de inicializar, puedes forzar el flujo nuevo con:
# fspec init --dir . --mode greenfield --harness all
```

El CLI creará `.spec/`, `docs/`, las reglas de harness (Antigravity, Claude Code, Cursor, Windsurf) y el hook `pre-commit`, pre-poblando `docs/technical/tech-stack.md` con tu framework, gestor de paquetes, librerías CSS y runners detectados.

> **Detección inteligente de Scaffold (`v1.1.0+`):** Cuando existe `package.json` con un boilerplate mínimo (`<= 2` archivos UI y sin carpetas `features/` ni tests propios), `fspec init` clasifica automáticamente el repositorio como *Fresh Scaffold* y te guía hacia la Ceremonia de Fundación (`REQ-UI-CORE-001`) en lugar de sugerir `fspec bootstrap`.

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

### Paso 1: Inicialización directa (`--ecosystem`) o interactiva (`-i`)

En una carpeta vacía (o recién creada con `git init`), puedes fijar el perfil objetivo en un solo comando sin modo interactivo (asume `TypeScript` por defecto), o usar `-i` para elegir todo el asistente paso a paso:

```bash
mkdir mi-app-web && cd mi-app-web
git init

# Opción no interactiva (perfiles: nextjs, react-vite, nuxt, vue-vite, sveltekit, astro, angular)
fspec init --dir . --ecosystem nextjs --harness all --versioning semver

# Opción interactiva completa
# fspec init --dir . -i --harness all
```

### Paso 2: Diseño Spec-First sin código fuente

En esta etapa aún no existe `src/` ni `package.json`:

1. Trabaja con el agente (`/ui-grill` o `/grill-me`) para redactar los primeros flujos UX en `docs/functional/user-flows/UF-*.md`.
2. Define la identidad visual en `docs/design/tokens-and-themes.md` y los contratos base en `docs/technical/` (opcionalmente respaldados con sidecars `.spec/specs/*.json` validados contra `schemas/`).
3. Registra `REQ-UI-CORE-001` en `docs/backlog/pending.md` declarando en **Fronteras y Artefactos** la creación del proyecto base (`package.json`, configuración del framework, tokens y App Shell) y aprueba el plan antes de generar código.

### Paso 3: Materialización del scaffold y sincronización del stack

1. Crea los archivos del proyecto Node dentro del directorio (o genera el scaffold en una carpeta temporal y mueve `package.json`, `src/`, etc. respetando `.spec/`, `docs/` y `.gitignore`).
2. Re-detecta automáticamente el `package.json` instalado y sincroniza `.spec/config.yaml` junto con `docs/technical/tech-stack.md` sin sobrescribir tus especificaciones vivas:
   ```bash
   # Previsualiza el stack detectado o aplícalo directamente
   fspec update --dir . --refresh-stack --dry-run
   fspec update --dir . --refresh-stack
   ```
3. Verifica que toda la documentación, sidecars y código staged cumplan los contratos:
   ```bash
   fspec sync
   fspec check --staged
   ```

---

## Siguiente Paso

- Continúa la operación diaria en [Guía 03: Flujo de Trabajo Diario (Dos Velocidades y Multi-Harness)](03-daily-workflow-two-speeds.md).
- Vuelve al índice principal en [README.md](../README.md).
