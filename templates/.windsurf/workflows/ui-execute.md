---
description: "Implementa un REQ-UI-* aprobado en docs/backlog/pending.md respetando fronteras, tokens simetricos, FSM y tests a11y/E2E."
---

# /ui-execute — Implementacion de Requerimiento UI Aprobado (Windsurf)

1. **Validacion de Gatekeeper:**
   - Verifica que el `REQ-UI-*` exista en `docs/backlog/pending.md`, este aprobado y declare **Fronteras y Artefactos** (`[NEW]`, `[MODIFY]`, `[DELETE]`). Si falta especificacion o aprobacion, detente y ejecuta `/ui-plan`.
   - Prohibido modificar archivos fuera de fronteras o editar `docs/backlog/audit-proposals.md`.
2. **Test Spec-First en Rojo:**
   - Implementa o actualiza primero el test unitario (`testing-library` + `axe-core` + mocks MSW) y/o Playwright E2E definido en la especificacion.
3. **Implementacion UI Estricta:**
   - Usa exclusivamente semantic design tokens de `docs/design/tokens-and-themes.md` (modo claro y oscuro).
   - Respeta FSM e invariantes, mapeo RFC 7807, cabecera `Idempotency-Key` en mutaciones criticas, prevencion XSS y restauracion de foco.
4. **Verificacion y Cierre:**
   - Ejecuta lint, typecheck, tests unitarios + `axe-core` y Playwright E2E (`390x844`, `1440x900`) cuando corresponda. Si el requerimiento cubre dependencias o Dependabot (`REQ-UI-SEC-*`), valida auditor local y `fspec check --security`.
   - Marca `[x]` los criterios, mueve el `REQ-UI-*` a `docs/backlog/changelog.md`, actualiza indices/*Rolling Window* (maximo 3 filas) y ejecuta `graphify update`.
