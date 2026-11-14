# Comando: 02c_plan_state_and_api

> **Propósito:** Especificar las fronteras de estado, validación de formularios, mocks MSW y el puente contractual con backend (Etapa 2C).

## Instrucciones para el Agente:
1. Abre `docs/technical/data-fetching-and-state.md` y usa `.spec/templates/_template_state_contracts.md` como referencia.
2. Clasifica cada pieza de estado en su ámbito correcto:
   - **Estado de Servidor:** Query keys, `staleTime` e invalidaciones (TanStack Query / SWR / fetch nativo de Nuxt/SvelteKit / Angular HTTP).
   - **Estado de URL:** Filtros, paginación y pestañas compartibles.
   - **Estado de Cliente / Local:** Stores ligeros o FSM interna.
3. Sincroniza con contratos backend (`api-contracts.md` / `openapi.yaml` si existen):
   - Define mapeo de errores RFC 7807 (`400`/`422` por campo, `401`, `403`, `409`, `429`, `5xx`).
   - Exige generación y envío de `Idempotency-Key` en mutaciones críticas y política de rollback si hay *optimistic updates*.
   - Define el esquema de validación cliente para formularios y los handlers/fixtures MSW correspondientes (incluyendo casos de error).
4. Actualiza `Historial de Revisiones` manteniendo máximo 3 filas.
