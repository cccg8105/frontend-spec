---
name: webapp-testing
description: "Protocolo de verificación multi-nivel frontend (Unit/Component + axe-core y Playwright E2E + Responsive + Modo Oscuro) bajo el patrón Reconnaissance-Then-Action."
---

# webapp-testing Skill

Esta skill guía la validación automatizada de interfaces, máquinas de estado e invariantes UI en `frontend-spec` combinando pruebas rápidas de componente y verificación E2E en navegador real.

## Niveles de Verificación
1. **Nivel 1 — Componente / Unidad (`.spec/templates/_template_ui_test.md`):**
   - Vitest/Jest + Testing Library adaptado al framework (React, Vue, Svelte o Angular) + `vitest-axe`.
   - Verifica estados `Loading`, `Empty`, `Error RFC 7807`, interacción real con `userEvent` e invariantes (`NoDoubleSubmit`, `PreserveDraftOnError`, `FocusRestoration`).
2. **Nivel 2 — E2E, Responsive y WCAG Real (`.spec/templates/_template_e2e_test.md`):**
   - Playwright + `@axe-core/playwright` obligatorio para flujos `UF-*` críticos (autenticación, rutas protegidas, formularios multi-paso o checkout).
   - Comprueba explícitamente `prefers-color-scheme: dark` y los viewports `390x844` (móvil), `768x1024` (tablet) y `1280x800` (desktop) validando ausencia de desbordamiento horizontal.

## Protocolo Reconnaissance-Then-Action
1. **Carga y Asentamiento:** Espera que hidratación y peticiones asíncronas (MSW o API) concluyan antes de interactuar.
2. **Selectores Accesibles Primero:** Consulta elementos por rol y etiqueta visible (`getByRole`, `getByLabel`) antes de recurrir a `data-testid` o selectores CSS frágiles.
3. **Verificación de Trazabilidad:** Incluye etiquetas `@spec`, `@req` e `@invariant` vinculando cada suite con `docs/functional/user-flows/` y `docs/backlog/pending.md`.
4. **Protocolo en `PATCH` Fast-Track:** Reproduce el bug visual o de estado con un test mínimo en rojo (`/diagnose`) antes de modificar el código fuente.
5. **Auditoría de Dependencias y Dependabot (`gh` CLI):** Si el cambio atiende vulnerabilidades o actualiza dependencias, verifica `gh auth status`, diagnostica alertas en GitHub (`gh api "repos/{owner}/{repo}/dependabot/alerts?state=open"` y `gh pr list --author "app/dependabot"`), ejecuta el auditor local del gestor de paquetes (`npm audit` / `pnpm audit`), valida con `fspec check --security` y verifica la suite de regresión antes de cerrar el `REQ-UI-SEC-*`.
