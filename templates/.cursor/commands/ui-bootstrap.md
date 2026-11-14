---
description: "Onboarding Brownfield en 4 fases (.spec/bootstrap-report.md) para adoptar frontend-spec en proyectos existentes."
---

# /ui-bootstrap — Adopcion Brownfield Frontend (Cursor)

Objetivo: Incorporar `frontend-spec` sobre un repositorio web existente mediante las 4 fases definidas en `.spec/skills/frontend-bootstrap/SKILL.md`.

## Fases de Ejecucion

1. **Fase 1 (Diagnostico y Linea Base):**
   - Analiza `package.json`, configuracion del framework (`vite.config.*`, `next.config.*`, `nuxt.config.*`, `svelte.config.*`, `astro.config.*`, `angular.json`), CSS/tokens y cobertura previa (`test_baseline`).
   - Actualiza `.spec/config.yaml` y `docs/technical/tech-stack.md`, e inicializa `.spec/bootstrap-report.md` como checklist GPS.
2. **Fase 2 (Extraccion As-Is — El Codigo Manda):**
   - Documenta un bloque por turno marcando `[x]` en `.spec/bootstrap-report.md` al completar: `tokens-and-themes.md`, `routing-and-rendering.md`, `component-hierarchy.md`, `data-fetching-and-state.md` y `deployment-strategy.md`.
3. **Fase 3 (Seleccion Full vs. Progresivo):**
   - Consulta al usuario mediante `AskQuestion` si prefiere **Modo Progresivo (Recommended)** (1-2 flujos criticos + inventario legado `Pendiente As-Is` en `docs/functional/index.md`) o **Modo Completo**.
4. **Fase 4 (Triage de Deuda sin Modificar `src/`):**
   - Registra hallazgos `[AUDIT-UI-DOMINIO-NUM]` con evidencia `archivo:linea` en `docs/backlog/audit-proposals.md` (hex quemados, fallos WCAG, XSS, rutas sin test/MSW) sin editar codigo fuente. Cierra Fase 4 en `.spec/bootstrap-report.md`.
