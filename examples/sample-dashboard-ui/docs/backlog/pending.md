# Backlog de Requerimientos UI Activos — sample-dashboard-ui

> **Instrucción para el Agente de IA:**
> Organizado por milestones y prioridad (`P1` Alta, `P2` Media, `P3` Baja).
> 1. Modifica **únicamente** los archivos declarados en **Fronteras y Artefactos** (`[NEW]`, `[MODIFY]`, `[DELETE]`).
> 2. Verifica todos los criterios de aceptación (`[x]`) con pruebas unitarias/a11y y E2E cuando aplique.
> 3. Para ajustes internos o fixes visuales (`PATCH`), utiliza el carril *Fast-Track* con `Referencia Funcional: N/A (PATCH / Fast-Track)`.

---

## Milestone v1.2.0

### [REQ-UI-DASH-002] Preservar foco en boton de reintento tras error temporal
- **Prioridad:** P2
- **Tipo:** Hotfix / Fix (PATCH - Fast-Track)
- **Versión Objetivo:** `v1.2.0`
- **Referencia Funcional:** `N/A (PATCH / Fast-Track)`
- **Referencia Técnica:** `docs/design/tokens-and-themes.md`, `docs/technical/component-hierarchy.md`
- **Tokens Consumidos:** `color-primary`, `color-danger`

#### Fronteras y Artefactos:
- **Artefactos a Modificar / Crear:**
  - `src/features/analytics/AnalyticsDataTable.tsx` [MODIFY]
  - `tests/unit/analytics-datatable.test.tsx` [MODIFY]
- **Restricciones:**
  - Carril Fast-Track (`PATCH`): prohibido alterar contratos de props publicas o rutas.

#### Criterios de Aceptación:
- [ ] Reproducir perdida de foco en test de regresion antes de aplicar el fix.
- [ ] Aplicar correccion manteniendo 0 violaciones WCAG en `vitest-axe`.
