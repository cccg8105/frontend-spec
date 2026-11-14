---
name: frontend-bootstrap
description: "Guía el onboarding asistido de proyectos frontend existentes (Brownfield) en 4 fases mediante ingeniería inversa estructurada y checklist persistente en .spec/bootstrap-report.md."
---

# frontend-bootstrap Skill

Esta skill guía al agente en la adopción ordenada de `frontend-spec` sobre repositorios web existentes (React, Next.js, Vue, Nuxt, SvelteKit, Astro o Angular) con estilos ad-hoc, deuda de accesibilidad o documentación desfasada.

## Regla de Oro Anti-Pérdida de Contexto
1. **Memoria en Disco (`.spec/bootstrap-report.md`):** Registra y consulta el avance en una lista de verificación GPS (`- [ ]` / `- [x]`) dividida por dominios y documentos técnicos.
2. **Un Bloque por Turno:** Documenta un artefacto o flujo a la vez y marca `[x]` inmediatamente tras completarlo para sobrevivir compactaciones de contexto.

---

## Flujo Operativo en 4 Fases

### Fase 1: Diagnóstico del Ecosistema y Línea Base
1. Inspecciona `package.json`, archivos de configuración (`vite.config.*`, `next.config.*`, `nuxt.config.*`, `svelte.config.*`, `astro.config.*`, `angular.json`, `tailwind.config.*`, `components.json`) y actualiza `docs/technical/tech-stack.md` y `.spec/config.yaml`.
2. Evalúa cobertura previa (`test_baseline`: `none`, `partial`, `solid`) en tests unitarios y Playwright/Cypress.
3. Si existe `graphify-out/graph.json`, analiza *God Nodes* y comunidades; si no existe, sugiere generar el grafo respetando `.graphifyignore`.

### Fase 2: Extracción Técnica e Identidad As-Is
**Regla de Verdad:** *El código fuente y las hojas CSS reales mandan sobre cualquier documentación antigua.*
1. **Design Tokens As-Is (`docs/design/tokens-and-themes.md`):** Extrae paleta actual, fuentes, variables CSS/Tailwind reales y documenta si falta soporte oscuro.
2. **Rutas y Renderizado (`docs/technical/routing-and-rendering.md`):** Inventaría rutas reales, layouts, guardias de sesión y modo CSR/SSR/SSG.
3. **Componentes y Estado (`component-hierarchy.md`, `data-fetching-and-state.md`):** Mapea componentes activos, librerías de fetch/stores y mocks existentes, filtrando archivos huérfanos o código muerto.
4. **Despliegue (`deployment-strategy.md`):** Inventaría variables públicas (`VITE_*`/`NEXT_PUBLIC_*`/etc.) y pipeline CI existente.

### Fase 3: Selección Full vs. Progresivo (Strangler / Just-In-Time)
Pregunta al usuario (Pregunta de 2 a 4 decisiones por ronda en el chat colocando primero la opcion recomendada con trade-offs claros) si desea:
- **Modo Completo (`full`):** Documentar flujos `UF-*` para todas las vistas/dominios detectados ahora.
- **Modo Progresivo (`progressive`):** Documentar solo los 1 o 2 flujos críticos y registrar el resto en `docs/functional/index.md` bajo `Módulos / Rutas Legadas Detectadas` (`status: Pendiente As-Is`).

### Fase 4: Triage de Deuda Visual, a11y y Cierre
1. Si hay ambigüedad sobre si un comportamiento heredado es intencional (*As-Is*) o un defecto, resuélvelo con `/grill-me`. Registra en `docs/backlog/audit-proposals.md` (sin alterar `src/`) los hallazgos con formato `[AUDIT-UI-DOMINIO-NUM]` y evidencia `archivo:L10-L25`:
   - Colores hex o píxeles quemados fuera de tokens (*AI slop* o CSS legacy).
   - Fallos WCAG (falta de `focus-visible`, contraste < 4.5:1, botones sin label).
   - Riesgos XSS (`dangerouslySetInnerHTML`/`v-html`), secretos en cliente o `doc drift`.
   - Rutas sin tests ni mocks MSW.
2. Marca completada la Fase 4 en `.spec/bootstrap-report.md` e informa al usuario.
