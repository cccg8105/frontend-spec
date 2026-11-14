# Guía 02: Adopción en Repositorios Existentes (Brownfield)

Cuando introduces `frontend-spec` en una aplicación en desarrollo o producción, la documentación debe reflejar primero **el estado real del código (*As-Is*)** y aislar la deuda técnica antes de planificar nuevas funcionalidades (*To-Be*). El proceso combina comandos deterministas del CLI con descubrimiento asistido en 4 fases.

---

## Paso 1: Inicialización No Destructiva (`fspec init`)

Desde la raíz de tu repositorio existente:

```bash
fspec init --dir . --harness all --versioning semver
```

### Garantías sobre archivos existentes
- Si ya tienes `package.json`, el CLI autodetecta tu framework (`Next.js`, `React + Vite`, `Nuxt`, `Vue + Vite`, `SvelteKit`, `Astro` o `Angular`), lenguaje, sistema de estilos, librerías de estado/mocks, runners de pruebas y versión actual.
- En reglas ya existentes como `CLAUDE.md` o `.windsurfrules`, inserta únicamente el bloque delimitado `<!-- FRONTEND-SPEC:START -->`..`<!-- FRONTEND-SPEC:END -->` sin sobrescribir tus reglas previas (lo que permite convivir en monorepos junto a `backend-spec`).
- Si ya existe `.git/hooks/pre-commit`, añade su bloque gestionado `# FRONTEND-SPEC:START`..`# FRONTEND-SPEC:END` preservando hooks previos del equipo.
- Si ya existe `.gitignore`, no lo sobrescribe.

---

## Paso 2: Inventario Automático y Memoria GPS (`fspec bootstrap`)

Ejecuta el comando `bootstrap` para escanear rutas, páginas, componentes UI, hojas CSS/Tailwind, archivos de estado/mocks MSW, suites Unit/E2E y documentación previa con posible desfase (*doc drift*):

```bash
# Modo recomendado para aplicaciones medianas/grandes (estrategia Strangler / Just-In-Time)
fspec bootstrap --dir . --mode progressive

# Alternativa para repositorios pequeños donde deseas documentar todas las vistas de una vez
fspec bootstrap --dir . --mode full
```

Si en algún momento necesitas reiniciar las casillas de seguimiento del onboarding, usa `fspec bootstrap --dir . --reset`.

### Qué genera `fspec bootstrap`
1. Actualiza automáticamente el perfil real detectado en `docs/technical/tech-stack.md` y los dominios sugeridos en `.spec/config.yaml`.
2. Crea `.spec/bootstrap-report.md` con una checklist persistente GPS (`- [ ]` / `- [x]`) dividida en 4 fases para que el agente pueda avanzar por bloques sin perder progreso aunque cambie o se compacte la sesión.
3. Si existe un grafo previo de conocimiento en `graphify-out/graph.json`, incorpora el resumen de *God Nodes* detectados.

---

## Paso 3: Onboarding Asistido en 4 Fases (`/ui-bootstrap`)

Una vez generado `.spec/bootstrap-report.md`, inicia al agente con `/ui-bootstrap` (en **Claude Code**, **Cursor** o **Windsurf**) o invoca la skill `frontend-bootstrap` (en **Antigravity**). El agente ejecutará cuatro fases ordenadas bajo la regla **El código fuente y los estilos reales mandan**:

1. **Fase 1 — Línea Base e Infraestructura:** Valida `docs/technical/tech-stack.md`, `.spec/config.yaml`, cobertura previa de pruebas (`test_baseline`: `none`, `partial` o `solid`) y variables/CI en `docs/technical/deployment-strategy.md`.
2. **Fase 2 — Extracción *As-Is* por bloques:** Documenta uno a uno (marcando `[x]` tras cada entrega):
   - Paleta real claro/oscuro, fuentes y variables en `docs/design/tokens-and-themes.md`.
   - Rutas reales, layouts, guardias RBAC y modo CSR/SSR/SSG en `docs/technical/routing-and-rendering.md`.
   - Componentes activos y jerarquía atómica en `docs/technical/component-hierarchy.md`.
   - Estado servidor/cliente, manejo de errores y mocks existentes en `docs/technical/data-fetching-and-state.md`.
3. **Fase 3 — Alcance `progressive` vs. `full`:**
   - En **Modo Progresivo**, documenta solo los 1 o 2 flujos críticos (`UF-*.md`) y registra el resto de vistas detectadas en `docs/functional/index.md` bajo `Módulos / Rutas Legadas Detectadas` (`Pendiente As-Is`).
   - En **Modo Completo**, documenta flujos `UF-*` para todas las rutas/dominios activos.
4. **Fase 4 — Triage de deuda sin modificar código (`src/`):**
   - Toda deuda encontrada (hexadecimales quemados fuera de tokens, fallos WCAG de foco/contraste, riesgos XSS o rutas sin test ni MSW) se registra **exclusivamente** en `docs/backlog/audit-proposals.md` con formato `[AUDIT-UI-DOMINIO-NUM]` y evidencia `archivo:linea`.

---

## Paso 4: Expansión Progresiva (*Just-In-Time*) y Promoción de Deuda

Con el bootstrap completado, el repositorio entra en operación normal evitando documentar áreas que nadie está tocando:

- **Cuando una nueva petición toca un módulo listado como `Pendiente As-Is`:** El agente documenta primero su flujo actual (`status: "As-Is (Brownfield)"`) antes de diseñar la evolución *To-Be*.
- **Cuando el equipo decide resolver un hallazgo de auditoría (`docs/backlog/audit-proposals.md`):** Nunca se codifica directamente desde el buzón de auditoría. Se promueve explícitamente a requerimiento activo mediante el CLI:

```bash
fspec req:new --from-audit AUDIT-UI-CORE-001
```

Este comando lee el dominio, prioridad, impacto estimado y evidencia del archivo de auditoría, crea el `REQ-UI-*` en `docs/backlog/pending.md`, marca la propuesta como promovida en `audit-proposals.md` y sincroniza `docs/backlog/index.md`.

---

## Siguiente Paso

- Revisa cómo trabajar cada cambio día a día en [Guía 03: Flujo de Trabajo Diario (Dos Velocidades y Multi-Harness)](03-daily-workflow-two-speeds.md).
- Consulta detalles del CLI y validación en [Guía 04: Referencia de CLI, Harnesses, Estructura y Contratos](04-cli-harnesses-and-contracts.md).
- Vuelve al índice principal en [README.md](../README.md).
