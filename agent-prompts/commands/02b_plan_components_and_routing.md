# Comando: 02b_plan_components_and_routing

> **Propósito:** Diseñar la jerarquía de componentes UI, contratos Props/Slots/FSM y arquitectura de rutas/renderizado (Etapa 2B).

## Instrucciones para el Agente:
1. Abre `docs/technical/component-hierarchy.md` y consulta `.spec/templates/_template_ui_component.md`.
2. Clasifica los nuevos componentes según Atomic Design (`atom`, `molecule`, `organism`, `template`, `page`) respetando la regla de dependencias hacia abajo.
3. Para cada componente complejo (`fsm_required: true` según `.spec/templates/ui-contracts-guidelines.md`):
   - Define el contrato tipado agnóstico (Props/Inputs, Callbacks/Emits y Slots).
   - Traza la máquina de estados `stateDiagram-v2` indicando transiciones prohibidas.
   - Especifica tabla de roles ARIA, atajos y restauración de foco.
4. Abre `docs/technical/routing-and-rendering.md` (molde `.spec/templates/_template_routing.md`):
   - Registra nuevas rutas, layout padre, modo de renderizado (`CSR`/`SSR`/`SSG`/`RSC`), guardia de autenticación/RBAC (`NoPrivilegedFlash`), Error Boundary asignado y metadatos SEO si es ruta pública.
5. Actualiza `Historial de Revisiones` (máx. 3 filas) en ambos documentos.
