---
description: "Implementa un requerimiento REQ-UI-* aprobado de docs/backlog/pending.md respetando fronteras, tokens, FSM y verificacion a11y/E2E."
---

# /ui-resolve — Ejecucion de Requerimiento UI Aprobado

Objetivo: Implementar el requerimiento `$ARGUMENTS` previamente aprobado en `docs/backlog/pending.md`.

## Guardias Previas a Codificar

1. Verifica que el `REQ-UI-*` exista en `docs/backlog/pending.md`, este aprobado por el usuario y enumere explicitamente **Fronteras y Artefactos** (`[NEW]`, `[MODIFY]`, `[DELETE]`). Si no existe o faltan artefactos (`UF-*` para `MAJOR`/`MINOR`), detente y ejecuta `/ui-plan`.
2. **PROHIBIDO** modificar archivos fuera de las fronteras declaradas en el requerimiento o alterar `docs/backlog/audit-proposals.md`.

## Flujo de Implementacion y Verificacion

1. **Test Spec-First en Rojo:** Crea o actualiza el test unitario (`testing-library` + `axe-core` + mocks MSW) y/o E2E Playwright segun lo planificado y confirma su estado inicial antes o durante la implementacion.
2. **Implementacion UI Estricta:**
   - Consume unicamente semantic design tokens de `docs/design/tokens-and-themes.md` (cero valores CSS quemados, soporte modo claro y oscuro).
   - Implementa la maquina de estados (FSM), manejo de errores RFC 7807 (`400`/`401`/`403`/`409`/`422`/`429`/`5xx`), `Idempotency-Key` en mutaciones criticas, proteccion XSS y restauracion de foco.
3. **Verificacion Multi-Nivel:**
   - Ejecuta typecheck, lint, tests unitarios + auditoria `axe-core` (0 violaciones WCAG AA) y E2E Playwright en `390x844` y `1440x900` cuando aplique. Si se modificaron dependencias o alertas de Dependabot (`REQ-UI-SEC-*`), valida auditor local + `fspec check --security`.
4. **Cierre Documental y Grafo:**
   - Marca `[x]` los criterios de aceptacion, archiva el `REQ-UI-*` en `docs/backlog/changelog.md`, actualiza indices y tablas *Rolling Window* (maximo 3 filas) y corre `graphify update` si existe `graphify-out/`.
