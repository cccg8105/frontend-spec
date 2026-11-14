# Comando: 03_create_requirement

> **Propósito:** Sintetizar las especificaciones en un requerimiento atómico en `docs/backlog/pending.md` con fronteras estrictas de archivos y scaffolding de pruebas.

## Instrucciones para el Agente:
1. Consulta `docs/backlog/versioning-strategy.md` para clasificar el impacto y el carril:
   - `MAJOR` / `MINOR` -> **Carril Completo** (exige flujo `UF-*`, revisión de tokens y referencias técnicas existentes).
   - `PATCH` -> **Carril Fast-Track** (permite `Referencia Funcional: N/A (PATCH / Fast-Track)` si no cambia rutas, props públicas ni contratos).
2. Asigna un ID único `REQ-UI-[DOMINIO]-[NUMERO]` verificando `docs/backlog/pending.md` y `docs/backlog/changelog.md`.
3. Registra el bloque en `docs/backlog/pending.md` respetando el formato canónico:
   - `### [REQ-UI-DOMINIO-NNN] Título`
   - `Prioridad:` `P1` | `P2` | `P3`
   - `Tipo:` `Feature (MINOR)` | `Breaking (MAJOR)` | `Hotfix / Fix (PATCH - Fast-Track)`
   - `Versión Objetivo:` milestone activo (ej. `v0.1.0`)
   - `Referencia Funcional:` ruta real `docs/functional/user-flows/UF-*.md` o `N/A (PATCH / Fast-Track)`
   - `Referencia Técnica:` rutas reales en `docs/technical/` y `docs/design/`
   - `Tokens Consumidos:` tokens semánticos autorizados
   - `Fronteras y Artefactos:` archivos exactos marcados `[NEW]`, `[MODIFY]` o `[DELETE]` + `Restricciones`
   - `Criterios de Aceptación:` casillas `- [ ]` verificables mediante tests automatizados.
4. **Scaffolding Spec-First o Diagnóstico `/diagnose`:**
   - En `MAJOR`/`MINOR`: crea el esqueleto inicial en rojo basado en `.spec/templates/_template_ui_test.md` (y `.spec/templates/_template_e2e_test.md` para flujos críticos multi-paso o de autenticación) con anotaciones `@spec`, `@req` e `@invariant`.
   - En `PATCH` (Fast-Track): aplica `/diagnose` (reproducción determinista -> caso mínimo -> hipótesis de causa raíz -> test automatizado de regresión en rojo antes del fix).
5. **Gatekeeper:** Presenta el plan acotado (`/plan` en carril completo o resumen de diagnóstico y test de regresión en `PATCH`) y **detén la ejecución** hasta recibir aprobación explícita del usuario.
