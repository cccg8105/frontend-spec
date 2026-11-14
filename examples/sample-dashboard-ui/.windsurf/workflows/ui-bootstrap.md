---
description: "Adopcion Brownfield en 4 fases (.spec/bootstrap-report.md) para proyectos frontend existentes."
---

# /ui-bootstrap — Adopcion Brownfield Frontend (Windsurf)

1. **Fase 1 (Diagnostico y Linea Base):**
   - Inspecciona `package.json`, configuracion de framework/bundler (`vite.config.*`, `next.config.*`, `nuxt.config.*`, `svelte.config.*`, `astro.config.*`, `angular.json`), CSS/Tailwind y cobertura de tests (`test_baseline`).
   - Actualiza `.spec/config.yaml` y `docs/technical/tech-stack.md`; crea `.spec/bootstrap-report.md`.
2. **Fase 2 (Extraccion As-Is por Bloques):**
   - Documenta un bloque por turno marcando `[x]` en `.spec/bootstrap-report.md` al terminar cada uno: `tokens-and-themes.md`, `routing-and-rendering.md`, `component-hierarchy.md`, `data-fetching-and-state.md` y `deployment-strategy.md`.
3. **Fase 3 (Alcance Full vs. Progresivo):**
   - Detente con opciones `A) Modo Progresivo (Recomendado)` vs `B) Modo Completo` para que el usuario decida cuantos flujos `UF-*` documentar inicialmente frente a `Módulos / Rutas Legadas Detectadas`.
4. **Fase 4 (Triage de Deuda y Cierre):**
   - Registra hallazgos `[AUDIT-UI-DOMINIO-NUM]` con evidencia `archivo:linea` en `docs/backlog/audit-proposals.md` sin editar `src/`, marca completada la Fase 4 y reporta el resultado.
