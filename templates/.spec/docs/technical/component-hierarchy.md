---
artifact_type: component-hierarchy
---

# Jerarquía y Arquitectura de Componentes — {{PROJECT_NAME}}

## 1. Niveles de Composición (Atomic Design)
1. **Átomos (`atoms/`):** Primitivas puras sin acceso a red ni stores globales (ej. `Button`, `Input`, `Badge`, `Spinner`).
2. **Moléculas (`molecules/`):** Combinación funcional acotada con estado local de interacción (ej. `FormField`, `SearchInput`, `EmptyState`).
3. **Organismos (`organisms/`):** Secciones con lógica de dominio UI, máquinas de estado FSM y consumo opcional de hooks/composables (ej. `DataTable`, `UserProfileCard`, `CheckoutSummary`).
4. **Plantillas y Vistas (`layouts/` y `pages/`):** Composición de página conectada a rutas, guardias de sesión y estado remoto.

### Regla de Dirección de Dependencias:
- `Pages / Templates` -> `Organisms` -> `Molecules` -> `Atoms` -> `Design Tokens`.
- Prohibido que un Átomo o Molécula importe Organismos, Stores globales o clientes HTTP.

---

## 2. Catálogo de Componentes Documentados

<!-- SYNC:COMPONENT_CATALOG:START -->
_Aún no hay componentes `CMP-*` catalogados. Utiliza `.spec/templates/_template_ui_component.md` al formalizar requerimientos `MAJOR` o `MINOR`._
<!-- SYNC:COMPONENT_CATALOG:END -->

---

## Historial de Revisiones (Últimos Cambios)

| Versión | Fecha | Requerimiento | Resumen del Cambio |
| :--- | :--- | :--- | :--- |
| `v{{CURRENT_VERSION}}` | {{TODAY}} | `INIT` | Definición de niveles atómicos, regla de dependencias y catálogo base. |

> *Nota: Esta tabla mantiene una ventana deslizante de los últimos 3 cambios. Para el historial completo, consultar [`docs/backlog/changelog.md`](../backlog/changelog.md).*
