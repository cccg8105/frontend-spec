---
artifact_type: tech-stack
---

# Blueprint: Stack Tecnológico, Presupuestos y Políticas Transversales Frontend

## 1. Matriz Multi-Ecosistema Soportada

| Capa | Opciones Oficiales del Framework |
| :--- | :--- |
| **Framework / Meta-Framework** | React + Vite \| Next.js \| Vue + Vite \| Nuxt \| SvelteKit \| Astro \| Angular |
| **Lenguaje** | TypeScript (`strict: true`) |
| **Estilos y Primitivas UI** | Tailwind CSS + `shadcn-ui` / Radix \| CSS Modules \| PrimeVue \| Melt UI \| Angular Material |
| **Estado Remoto y Mocks** | TanStack Query / SWR / Fetch nativo de meta-framework + MSW (Mock Service Worker) |
| **Testing y Accesibilidad** | Vitest o Jest + Testing Library + `axe-core` + Playwright |

---

## 2. Convenciones de Nomenclatura
- **Componentes UI:** `PascalCase` (`UserProfileCard.tsx`, `UserProfileCard.vue`, `UserProfileCard.svelte`) o `kebab-case` en Angular según convención del CLI (`user-profile-card.component.ts`).
- **Hooks / Composables / Stores:** `use*.ts` (React/Vue composables), `*.store.ts` / `*.svelte.ts`.
- **Variables Públicas de Entorno:** Únicamente con el prefijo explícito del bundler (`VITE_*`, `NEXT_PUBLIC_*`, `NUXT_PUBLIC_*`, `PUBLIC_*`).

---

## 3. Presupuestos de Rendimiento (Core Web Vitals y Bundle)

| Métrica / Presupuesto | Umbral Objetivo (P75 Móvil) | Estrategia de Cumplimiento |
| :--- | :--- | :--- |
| **LCP** (*Largest Contentful Paint*) | `<= 2.5 s` | Precarga de fuentes críticas, imágenes optimizadas (`width`/`height`, lazy fuera de fold), SSR/SSG cuando aplique |
| **INP** (*Interaction to Next Paint*) | `<= 200 ms` | Evitar renders síncronos costosos, virtualizar listas largas (`> 100` filas), debouncing en filtros |
| **CLS** (*Cumulative Layout Shift*) | `<= 0.1` | Skeletons con dimensiones fijas, reserva de espacio para alertas/imágenes |
| **JavaScript Inicial** | `<= 200 KB` gzip por ruta inicial | *Code-splitting* por ruta y carga diferida de gráficos/editores pesados |

---

## 4. Seguridad Frontend, i18n y Observabilidad

- **Prevención XSS:** Prohibido inyectar HTML crudo (`dangerouslySetInnerHTML`, `v-html`, `{@html}`, `[innerHTML]`) sin sanitización verificada (`DOMPurify`) y validación de esquemas URL (`https://` o ruta relativa; bloquear `javascript:`).
- **Almacenamiento de Credenciales:** Prohibido persistir secretos, refresh tokens o credenciales privilegiadas en `localStorage`/`sessionStorage` si el backend provee cookies `HttpOnly; Secure; SameSite`.
- **Content Security Policy (CSP):** Documentar orígenes permitidos de scripts, fuentes, imágenes y `connect-src`.
- **Internacionalización (i18n):** Definir explícitamente si el proyecto externaliza literales mediante diccionarios/claves (`react-i18next`, `vue-i18n`, `@inlang/paraglide-js`, Angular `@angular/localize`) o si opera en idioma único con microcopy centralizado.
- **Error Boundaries y Telemetría:** Toda sección crítica debe estar envuelta en un Error Boundary que reporte fallos estructurados sin incluir PII ni tokens en logs del cliente.

---

## Historial de Revisiones (Últimos Cambios)

| Versión | Fecha | Requerimiento | Resumen del Cambio |
| :--- | :--- | :--- | :--- |
| `v0.1.0` | YYYY-MM-DD | `INIT` | Plantilla base de stack multi-ecosistema y políticas RNFs frontend. |

> *Nota: Esta tabla mantiene una ventana deslizante de los últimos 3 cambios. Para el historial completo, consultar `docs/backlog/changelog.md`.*
