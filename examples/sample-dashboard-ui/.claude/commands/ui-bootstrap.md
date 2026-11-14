---
description: "Ejecuta el onboarding Brownfield en 4 fases (.spec/bootstrap-report.md) para proyectos frontend existentes."
---

# /ui-bootstrap — Adopcion Brownfield Frontend

Objetivo: Adoptar `frontend-spec` sobre el proyecto existente siguiendo las 4 fases de `.spec/skills/frontend-bootstrap/SKILL.md` sin perder contexto entre turnos.

## Protocolo en 4 Fases

1. **Fase 1 (Diagnostico y Linea Base):**
   - Inspecciona `package.json`, configuracion de bundler/framework (`vite.config.*`, `next.config.*`, `nuxt.config.*`, `svelte.config.*`, `astro.config.*`, `angular.json`), CSS/Tailwind y suite de tests (`test_baseline`).
   - Actualiza `.spec/config.yaml` y `docs/technical/tech-stack.md`. Crea o actualiza `.spec/bootstrap-report.md` con la checklist GPS.
2. **Fase 2 (Extraccion As-Is — El Codigo Manda):**
   - Documenta un bloque por turno y marca `[x]` en `.spec/bootstrap-report.md` al completar cada uno:
     - `docs/design/tokens-and-themes.md` (paleta real, fuentes, claro/oscuro faltante).
     - `docs/technical/routing-and-rendering.md` (rutas reales, layouts, guardias, CSR/SSR/SSG).
     - `docs/technical/component-hierarchy.md` y `docs/technical/data-fetching-and-state.md`.
     - `docs/technical/deployment-strategy.md` (variables publicas y CI).
3. **Fase 3 (Alcance Full vs. Progresivo):**
   - Usa `AskUserQuestion` para que el usuario elija entre **Modo Progresivo (Recommended)** (documentar 1-2 flujos criticos y listar modulos legados en `docs/functional/index.md` con `Pendiente As-Is`) o **Modo Completo**.
4. **Fase 4 (Triage de Deuda sin Alterar `src/`):**
   - Registra hallazgos `[AUDIT-UI-DOMINIO-NUM]` con evidencia `archivo:linea` en `docs/backlog/audit-proposals.md` (hex quemados, fallos WCAG, XSS, rutas sin test ni MSW) sin tocar codigo fuente. Marca Fase 4 completada e informa al usuario.
