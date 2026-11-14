# Índice de Documentación Funcional y Flujos UX — sample-dashboard-ui

> **Instrucción para el Agente de IA:**
> Este catálogo contiene la lista de flujos de usuario (`UF-*`) e interacciones activas del proyecto.
> - Antes de planificar cambios visuales o de interacción, identifica aquí el flujo afectado.
> - **No leas todos los flujos simultáneamente**; carga únicamente el archivo vinculado a la tarea en curso.
> - Plantilla canónica: [`.spec/templates/_template_user_flow.md`](../../.spec/templates/_template_user_flow.md) y guía heurística FSM en [`.spec/templates/ui-contracts-guidelines.md`](../../.spec/templates/ui-contracts-guidelines.md).

---

## Catálogo de Flujos de Usuario

<!-- SYNC:USER_FLOWS_CATALOG:START -->
| ID Flujo | Título | Ruta | Dominio | FSM | Estado | Documento |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `UF-DASH-001` | Consulta paginada y exportacion de analitica operativa | `/dashboard/analytics` | `analytics` | Si | Activo | [UF-DASH-001-analytics-datatable.md](./user-flows/UF-DASH-001-analytics-datatable.md) |
<!-- SYNC:USER_FLOWS_CATALOG:END -->

---

## Módulos / Rutas Legadas Detectadas (Modo Progresivo — Pendientes As-Is)

<!-- SYNC:PENDING_DOMAINS:START -->
| Dominio / Ruta Legada | Estado | Accion Recomendada (Just-In-Time) |
| :--- | :--- | :--- |
| `mocks` | Pendiente As-Is | Ejecutar `/ui-bootstrap` o documentar `UF-MOCKS-001` al tocar el modulo |
<!-- SYNC:PENDING_DOMAINS:END -->

---

## Convenciones de Flujos UX
1. Todo flujo nuevo debe residir en `docs/functional/user-flows/UF-[DOMINIO]-[NUMERO]-[slug].md` con YAML Frontmatter válido (`id`, `title`, `domain`, `actor`, `route`, `status`).
2. Debe incluir diagrama Mermaid, tabla de estados visuales (`Loading`, `Empty`, `Error`), criterios WCAG 2.1 AA e invariantes FSM cuando aplique la Matriz Heurística.
