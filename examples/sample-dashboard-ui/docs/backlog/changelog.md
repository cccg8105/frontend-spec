# Historial de Requerimientos y Releases Frontend — sample-dashboard-ui

> Este documento contiene el registro inmutable de requerimientos completados y liberados en cada versión del proyecto.

---

## Release v1.0.0 - Línea Base de Especificaciones
*Fecha de inicialización: 2026-11-14*

- **`[INIT]` Adopción de `frontend-spec` v1.0.0**
  - Configuración inicial de flujos UX, design tokens claro/oscuro, arquitectura técnica multi-ecosistema y gobernanza de backlog (`SemVer 2.0.0`).

---

## Release v1.1.0 (Actualizado: 2026-11-14)

### [REQ-UI-ANALYTICS-001] Anuncio accesible de paginacion en AnalyticsDataTable
- **Fecha de Resolución:** `2026-11-14`
- **Prioridad:** P1
- **Tipo:** Hotfix / Fix (PATCH - Fast-Track)
- **Versión Objetivo:** `v1.1.0`
- **Referencia Funcional:** `N/A (PATCH / Fast-Track)`
- **Referencia Técnica:** `docs/design/tokens-and-themes.md`, `docs/technical/component-hierarchy.md`
- **Tokens Consumidos:** `color-surface`, `color-primary`, `color-text-main`

#### Fronteras y Artefactos:
- **Artefactos a Modificar / Crear:**
  - `src/features/analytics/AnalyticsDataTable.tsx` [MODIFY]
  - `tests/unit/anuncio-accesible-de-paginacion-en-analy.test.tsx` [NEW]
- **Restricciones:**
  - Carril Fast-Track (`PATCH`): prohibido romper rutas, props publicas, contratos RFC 7807 o quemar valores CSS fuera de tokens.

#### Criterios de Aceptación:
- [x] Reproducir el defecto con `/diagnose` mediante test automatizado de regresion en rojo antes del fix.
- [x] Aplicar correccion minima verificando tests unitarios + `axe-core` al 100%.


### [REQ-UI-DASH-001] Tabla analitica paginada y exportacion idempotente
- **Fecha de Resolución:** `2026-11-14`
- **Prioridad:** P1
- **Tipo:** Feature (MINOR)
- **Versión Objetivo:** `v1.1.0`
- **Referencia Funcional:** `docs/functional/user-flows/UF-DASH-001-analytics-datatable.md`
- **Referencia Técnica:** `docs/design/tokens-and-themes.md`, `docs/technical/component-hierarchy.md`, `docs/technical/routing-and-rendering.md`
- **Tokens Consumidos:** `color-surface`, `color-primary`, `color-text-main`

#### Fronteras y Artefactos:
- **Artefactos a Modificar / Crear:**
  - `src/features/dash/TablaAnaliticaPaginadaYExportacionI.tsx` [NEW]
  - `tests/unit/tabla-analitica-paginada-y-exportacion-i.test.tsx` [NEW]
- **Restricciones:**
  - Cumplir directivas Anti-AI Slop, simetria claro/oscuro, FSM e invariantes verificables y cero secretos en cliente.

#### Criterios de Aceptación:
- [x] Implementar flujo UX y estados borde (`Loading`, `Empty`, `Error` RFC 7807) consumiendo solo semantic design tokens.
- [x] Pruebas unitarias (`axe-core`) y E2E Playwright en viewports pasando al 100%.
