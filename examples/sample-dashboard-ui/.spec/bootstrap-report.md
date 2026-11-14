---
artifact_type: bootstrap-report
onboarding_mode: full
ecosystem: react-vite
test_baseline: "solid (2 unit, 0 E2E)"
generated_at: "2026-11-14"
---

# Reporte de Adopcion Brownfield Frontend — sample-dashboard-ui

- **Modo Seleccionado:** `full`
- **Stack Detectado:** `React + Vite` (`TypeScript`, `Tailwind CSS`, `shadcn/ui + Radix`)
- **Estado / Mocks:** `TanStack Query` | **Tests:** `Vitest` / `Playwright`
- **Linea Base de Pruebas:** `solid (2 unit, 0 E2E)`
- **Dominios UI Sugeridos:** `analytics`, `mocks`

---

## Checklist GPS de Ingenieria Inversa Frontend

### Fase 1: Linea Base e Infraestructura
- [x] Validar docs/technical/tech-stack.md y .spec/config.yaml con el ecosistema real
- [x] Revisar package.json, variables publicas y pipeline CI en deployment-strategy.md

### Fase 2: Extraccion Tecnica e Identidad Visual (El Codigo Manda)
- [x] Documentar paleta real claro/oscuro, tipografias y Tailwind/CSS en docs/design/tokens-and-themes.md
- [x] Inventariar rutas activas, layouts y guardias RBAC en docs/technical/routing-and-rendering.md
- [x] Catalogar componentes clave (CMP-*) y jerarquia atomica en docs/technical/component-hierarchy.md
- [x] Mapear estado remoto, manejo RFC 7807 y mocks MSW en docs/technical/data-fetching-and-state.md

### Fase 3: Flujos UX (UF-*)
- [x] Documentar flujos criticos iniciales en docs/functional/user-flows/UF-*.md
- [x] Verificar modulos legados pendientes (Just-In-Time) en docs/functional/index.md

### Fase 4: Triage de Deuda Visual, a11y y Cierre
- [x] Registrar hex quemados, fallos WCAG o riesgos XSS como AUDIT-UI-* en docs/backlog/audit-proposals.md

---

## Inventario Tecnico Detectado

### Rutas y Paginas (1)
- `src/pages/AnalyticsDashboardPage.tsx`

### Muestra de Componentes UI (3)
- `src/features/analytics/AnalyticsDataTable.tsx`
- `src/features/analytics/ExportReportButton.tsx`
- `src/pages/AnalyticsDashboardPage.tsx`

### Hojas de Estilo, Tailwind y Tokens (3)
- `components.json`
- `src/styles/tokens.css`
- `tailwind.config.ts`

### Documentacion Previa / Posible Doc Drift
- *(Sin documentacion previa conflictiva detectada)*

### Graphify God Nodes
- *(Sin grafo Graphify detectado: recomienda ejecutar `graphify` respetando `.graphifyignore`)*
