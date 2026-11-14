---
artifact_type: data-fetching-and-state
server_state_tool: "TanStack Query"
mock_strategy: msw
---

# Contratos de Consumo de API, Formularios y Gestión de Estado — sample-dashboard-ui

## 1. Separación Estricta de Estado
- **Estado de Servidor:** Gestionado mediante `TanStack Query` (TanStack Query / SWR / `useFetch` Nuxt / `load` SvelteKit / Angular `HttpClient` + `Resource`), nunca replicado manualmente en stores globales.
- **Estado de URL:** Filtros, paginación, búsqueda y pestañas persistidas en query params.
- **Estado de Cliente / UI Local:** Context / Store ligero para preferencias transversales (tema, layout) y estado local de componentes para FSM reactivas.

---

## 2. Integración Contractual con Backend (`api-contracts.md` / RFC 7807)
- **Errores RFC 7807 (`application/problem+json`):** Los errores `400`/`422` se asignan a campos específicos del formulario; `401` activa refresh único o redirección a login; `403` muestra vista controlada sin reintento; `409` alerta conflicto de versión; `429` respeta `Retry-After`; `5xx` conserva el borrador del usuario con opción de reintento.
- **Idempotencia en Mutaciones Críticas:** Las acciones financieras o de creación crítica generan un UUID v4 por intención y lo envían en la cabecera `Idempotency-Key`, bloqueando el botón mientras la mutación está pendiente.
- **Mocks Deterministas (MSW):** Los handlers de Mock Service Worker deben reflejar exactamente los contratos HTTP de backend (incluyendo casos de error `4xx`/`5xx`) para pruebas locales y E2E reproducibles.

---

## Historial de Revisiones (Últimos Cambios)

| Versión | Fecha | Requerimiento | Resumen del Cambio |
| :--- | :--- | :--- | :--- |
| `v1.0.0` | 2026-11-14 | `INIT` | Contrato de fronteras de estado, mapeo RFC 7807, idempotencia y MSW. |

> *Nota: Esta tabla mantiene una ventana deslizante de los últimos 3 cambios. Para el historial completo, consultar [`docs/backlog/changelog.md`](../backlog/changelog.md).*
