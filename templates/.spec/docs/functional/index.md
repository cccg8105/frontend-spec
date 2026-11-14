# Índice de Documentación Funcional y Flujos UX — {{PROJECT_NAME}}

> **Instrucción para el Agente de IA:**
> Este catálogo contiene la lista de flujos de usuario (`UF-*`) e interacciones activas del proyecto.
> - Antes de planificar cambios visuales o de interacción, identifica aquí el flujo afectado.
> - **No leas todos los flujos simultáneamente**; carga únicamente el archivo vinculado a la tarea en curso.
> - Plantilla canónica: [`.spec/templates/_template_user_flow.md`](../../.spec/templates/_template_user_flow.md) y guía heurística FSM en [`.spec/templates/ui-contracts-guidelines.md`](../../.spec/templates/ui-contracts-guidelines.md).

---

## Catálogo de Flujos de Usuario

<!-- SYNC:USER_FLOWS_CATALOG:START -->
_Aún no hay flujos de usuario registrados. Se agregarán al formalizar requerimientos `MAJOR` o `MINOR` en `docs/functional/user-flows/`._
<!-- SYNC:USER_FLOWS_CATALOG:END -->

---

## Módulos / Rutas Legadas Detectadas (Modo Progresivo — Pendientes As-Is)

<!-- SYNC:PENDING_DOMAINS:START -->
_Sin rutas o módulos UI legados pendientes de levantamiento._
<!-- SYNC:PENDING_DOMAINS:END -->

---

## Convenciones de Flujos UX
1. Todo flujo nuevo debe residir en `docs/functional/user-flows/UF-[DOMINIO]-[NUMERO]-[slug].md` con YAML Frontmatter válido (`id`, `title`, `domain`, `actor`, `route`, `status`).
2. Debe incluir diagrama Mermaid, tabla de estados visuales (`Loading`, `Empty`, `Error`), criterios WCAG 2.1 AA e invariantes FSM cuando aplique la Matriz Heurística.
