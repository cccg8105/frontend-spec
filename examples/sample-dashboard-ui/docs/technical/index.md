# Índice de Documentación Técnica Frontend — sample-dashboard-ui

> **Instrucción para el Agente de IA:**
> Utiliza este índice O(1) para cargar **únicamente** los documentos técnicos relevantes para la tarea actual:
> - ¿Árbol de componentes, Props/Slots, FSM o accesibilidad ARIA? -> [`component-hierarchy.md`](./component-hierarchy.md)
> - ¿Rutas, layouts anidados, guardias RBAC, Error Boundaries, CSR/SSR/SSG o SEO? -> [`routing-and-rendering.md`](./routing-and-rendering.md)
> - ¿Estado servidor/cliente, formularios, errores RFC 7807, `Idempotency-Key` o mocks MSW? -> [`data-fetching-and-state.md`](./data-fetching-and-state.md)
> - ¿Stack (`React + Vite`), presupuestos Core Web Vitals, XSS/CSP, i18n o telemetría? -> [`tech-stack.md`](./tech-stack.md)
> - ¿CI/CD, variables públicas, Cache-Control o despliegue CDN/SSR? -> [`deployment-strategy.md`](./deployment-strategy.md)
> - Blueprints y moldes de pruebas (Unit/a11y + Playwright E2E): [`.spec/templates/`](../../.spec/templates/)

---

## Artefactos Técnicos del Sistema

| Artefacto | Archivo | Responsabilidad Clave |
| :--- | :--- | :--- |
| **Jerarquía de Componentes** | [component-hierarchy.md](./component-hierarchy.md) | Niveles atómicos, inventario de componentes `CMP-*`, Props/Slots y contratos FSM. |
| **Rutas y Renderizado** | [routing-and-rendering.md](./routing-and-rendering.md) | Mapa de URLs, layouts, auth/RBAC guards, Error Boundaries, CSR/SSR/SSG y SEO. |
| **Estado y Consumo de API** | [data-fetching-and-state.md](./data-fetching-and-state.md) | Fronteras de estado, puente RFC 7807 con backend, idempotencia UI, formularios y mocks MSW. |
| **Stack y Políticas RNFs** | [tech-stack.md](./tech-stack.md) | Ecosistema activo (`React + Vite`), nomenclatura, Web Vitals/bundle budgets, XSS/CSP e i18n. |
| **Estrategia de Despliegue** | [deployment-strategy.md](./deployment-strategy.md) | Pipeline CI/CD, variables públicas sin secretos, cabeceras de seguridad, caché y rollback. |

---

## Principios Técnicos Invariables
1. **Desacoplamiento Visual y Contractual:** Los componentes presentacionales (`Átomos` y `Moléculas`) no realizan fetching de red directo ni contienen secretos o lógica de enrutamiento acoplada.
2. **Cero Valores Quemados:** Todos los colores, tipografías, radios y capas `z-index` provienen de [`docs/design/tokens-and-themes.md`](../design/tokens-and-themes.md).
3. **Sincronía Viva:** Todo cambio en endpoints consumidos o payloads actualiza `data-fetching-and-state.md`; toda ruta o permiso nuevo actualiza `routing-and-rendering.md`.
