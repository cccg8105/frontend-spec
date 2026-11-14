---
name: theme-factory
description: "Metodología para modelar, mapear y gobernar Design Tokens semánticos portables (Tailwind @theme, shadcn-ui, CSS Modules, PrimeVue, Angular Material) con simetría claro/oscuro y contraste WCAG."
---

# theme-factory Skill

Esta skill gobierna el sistema de diseño basado en tokens de `frontend-spec`, asegurando portabilidad entre frameworks CSS y cero valores visuales hardcodeados.

## Reglas Operativas de Tokens
1. **Nombres Semánticos Únicos:** Emplea tokens basados en intención y rol (`color-bg-base`, `color-surface`, `color-primary`, `color-text-main`, `color-text-muted`, `color-border`, `color-danger`), nunca nombres literales de color (`blue-500`, `gray-200`).
2. **Dualidad Simétrica Claro / Oscuro:** Todo token de superficie, texto, borde o estado debe definir simultáneamente su valor para modo claro (`:root`) y modo oscuro (`.dark`), validando contraste mínimo WCAG AA (`>= 4.5:1` texto normal, `>= 3:1` bordes/controles).
3. **Mapeo Ejecutable al Stack:** Traduce los tokens documentados en `docs/design/tokens-and-themes.md` hacia las variables CSS reales del proyecto (`@theme` de Tailwind v4, variables CSS de `shadcn-ui`, CSS Modules, PrimeVue o Angular Material) según `docs/technical/tech-stack.md`.
4. **Escalas Completas:** Mantén centralizados no solo colores, sino espaciado modular, radios, sombras/elevación, capas `z-index`, breakpoints y duraciones de transición con soporte `prefers-reduced-motion`.
5. **Cero Valores Quemados:** Ningún componente en `src/` debe declarar colores hex/rgb ni `z-index` arbitrarios fuera del sistema de tokens; cualquier hallazgo en código legado se reporta en `docs/backlog/audit-proposals.md`.
