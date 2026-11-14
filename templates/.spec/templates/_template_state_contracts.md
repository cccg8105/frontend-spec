---
artifact_type: data-fetching-and-state
server_state_tool: tanstack-query # tanstack-query | swr | nuxt-usefetch | sveltekit-load | angular-http
mock_strategy: msw
---

# Blueprint: Contratos de Estado, Formularios y Consumo de API

## 1. Taxonomía y Fronteras de Estado

| Tipo de Estado | Dónde Vive | Herramienta Recomendada (por Stack) | Regla de Uso |
| :--- | :--- | :--- | :--- |
| **Estado de Servidor (Remoto)** | Caché asíncrona declarativa | TanStack Query / SWR / `useFetch` (Nuxt) / Loaders (SvelteKit) / Resource API (Angular) | Prohibido duplicar respuestas HTTP en stores globales manuales |
| **Estado de URL (Compartible)** | Query params y path params | Router nativo / `nuqs` | Filtros, paginación, pestaña activa y búsqueda |
| **Estado de Cliente Compartido** | Store ligero | Context / Zustand / Pinia / Svelte Stores / Angular Signals | Preferencias UI (tema, sidebar colapsado), estado efímero de sesión |
| **Estado Local de Componente** | Estado interno / máquina FSM | `useState`/`useReducer` / `ref`/`reactive` / `$state` / `signal` | Inputs no confirmados, hover, apertura de popover |

---

## 2. Puente Contractual con Backend (`api-contracts.md` / OpenAPI)

### A. Mapeo Estándar de Errores HTTP y RFC 7807 (`application/problem+json`)
| Código HTTP | Significado Backend | Comportamiento Obligatorio en UI |
| :--- | :--- | :--- |
| `400` / `422` | Validación / regla de negocio | Mapear `errors[]` o `detail` a errores por campo o banner sin limpiar el formulario |
| `401` | Token expirado / ausente | Intentar refresh único; si falla, limpiar sesión y redirigir a `/login` |
| `403` | Violación RBAC / anti-IDOR | Mostrar vista o estado `403` sin reintentos automáticos |
| `409` | Conflicto de concurrencia o idempotencia | Notificar desactualización de recurso y ofrecer recargar datos vigentes |
| `429` | Rate Limit excedido | Deshabilitar reintento automático inmediato y mostrar tiempo de espera (`Retry-After`) |
| `5xx` / Red | Fallo transitorio | Conservar borrador del usuario y mostrar botón "Reintentar" |

### B. Idempotencia en Mutaciones Críticas
- Toda mutación `POST`/`PATCH` no naturalmente idempotente (pagos, creación de órdenes, envíos únicos) genera un UUID v4 único por intento de intención de usuario y lo envía en la cabecera `Idempotency-Key`, manteniendo el botón bloqueado mientras `isPending === true`.

### C. Política de Caché, Invalidación y Actualizaciones Optimistas
- Definir explícitamente `queryKey` jerárquicos (ej. `["transactions", { page, filter }]`), `staleTime` acorde a volatilidad y qué keys invalidar en `onSuccess`.
- Si se usa actualización optimista, guardar snapshot previo en `onMutate` y ejecutar rollback determinista en `onError`.

---

## 3. Contratos de Formularios y Mocks (MSW)
- **Validación Cliente:** Esquema tipado compartido o alineado con `api-contracts.md` (Zod / Valibot / ArkType) validando antes de enviar y reflejando restricciones exactas de backend.
- **Mock Service Worker (MSW):** Los handlers de desarrollo y pruebas deben respetar exactamente el contrato HTTP (rutas, cabeceras `Idempotency-Key`, payloads RFC 7807 para escenarios `4xx`/`5xx`) para evitar falsos positivos antes de integrar con backend real.

---

## Historial de Revisiones (Últimos Cambios)

| Versión | Fecha | Requerimiento | Resumen del Cambio |
| :--- | :--- | :--- | :--- |
| `v0.1.0` | YYYY-MM-DD | `INIT` | Definición base de fronteras de estado, RFC 7807, idempotencia y MSW. |

> *Nota: Esta tabla mantiene una ventana deslizante de los últimos 3 cambios. Para el historial completo, consultar `docs/backlog/changelog.md`.*
