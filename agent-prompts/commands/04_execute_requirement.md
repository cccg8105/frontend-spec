# Comando: 04_execute_requirement

> **Propósito:** Ejecutar la implementación aprobada dentro de sus fronteras autorizadas aplicando diseño Anti-AI Slop, contratos FSM y verificación multi-nivel.

## Instrucciones para el Agente:
1. Lee únicamente el bloque `REQ-UI-*` activo en `docs/backlog/pending.md` y sus documentos referenciados.
2. **Descomposición e Implementación Acotada:**
   - Si el requerimiento involucra múltiples archivos, implementa primero tipos/contratos, esquemas de validación y handlers MSW antes que los componentes visuales dependientes.
   - Modifica **únicamente** los archivos listados en `Fronteras y Artefactos`.
   - Aplica `.spec/templates/design-guidelines.md` (paleta restringida de `tokens-and-themes.md`, cero valores CSS quemados, tipografía intencional, simetría claro/oscuro, `prefers-reduced-motion`).
   - Implementa todos los estados interactivos (`hover`, `active`, `focus-visible`, `disabled`, `loading`, `empty`, `error`) e invariantes FSM (`NoDoubleSubmit`, `PreserveDraftOnError`, `FocusRestoration`).
3. **Verificación Multi-Nivel:**
   - Ejecuta la suite unitaria/componente (Vitest/Jest + Testing Library + `axe-core`) hasta obtener 100% de éxito sin omisiones.
   - En flujos `MAJOR`/`MINOR` con navegación o responsive crítico, ejecuta la suite Playwright E2E verificando `@axe-core/playwright`, modo oscuro y viewports (`390x844`, `768x1024`, `1280x800`) sin `overflow-x`.
   - Realiza auditoría del diff (`/code-review`) comprobando ausencia de CSS quemado, code smells, fugas de estado servidor a stores globales o XSS.
4. **Cierre y Graphify:**
   - Marca `[x]` los criterios cumplidos en `docs/backlog/pending.md`, actualiza los catálogos afectados (`docs/functional/index.md`, `docs/technical/component-hierarchy.md`, `docs/technical/routing-and-rendering.md`) y registra la entrega en `docs/backlog/changelog.md`.
   - Si existe `graphify-out/`, ejecuta `graphify update` respetando `.graphifyignore`.
