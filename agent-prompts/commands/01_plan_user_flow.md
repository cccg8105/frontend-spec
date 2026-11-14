# Comando: 01_plan_user_flow

> **Propósito:** Redactar o actualizar formalmente un flujo de usuario UX en Etapa 1 (Carril Completo `MAJOR` / `MINOR`).

## Instrucciones para el Agente:
1. Analiza la experiencia de usuario y las interacciones de negocio de forma agnóstica al framework JS/CSS concreto.
2. Identifica el dominio (ej. `auth`, `dashboard`, `billing`, `core`) y asigna el siguiente ID secuencial (`UF-[DOMINIO]-[NUM]-[slug].md`).
3. Crea o actualiza `docs/functional/user-flows/UF-[DOMINIO]-[NUM]-[slug].md` tomando como molde `.spec/templates/_template_user_flow.md`.
4. Incluye obligatoriamente:
   - Cabecera YAML Frontmatter (`id`, `title`, `domain`, `actor`, `route`, `status`, `fsm_required`, `viewports`).
   - Diagrama Mermaid del flujo completo (`flowchart TD` o `sequenceDiagram`).
   - Tablas de Entradas/Eventos del usuario y Salidas Visuales esperadas.
   - Matriz completa de estados UI (`Loading`, `Empty`, `Error de Red / 5xx`, `Error 403/404`).
   - Cláusulas formales de invariantes UI cuando aplique la Matriz Heurística (`.spec/templates/ui-contracts-guidelines.md`).
   - Requisitos de foco inicial, teclado (`Tab`, `Enter`, `Escape`), roles ARIA y viewports responsive.
   - Tabla `Historial de Revisiones` (máx. 3 filas).
5. Actualiza la entrada correspondiente en `docs/functional/index.md` dentro de `<!-- SYNC:USER_FLOWS_CATALOG:START/END -->`.
