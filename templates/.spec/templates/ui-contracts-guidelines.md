# Guía de Contratos UI y Matriz Heurística de Complejidad (`frontend-spec`)

Este documento define el equivalente frontend a las cláusulas formales de dominio: establece cuándo un flujo o componente requiere especificar obligatoriamente una **Máquina de Estados Finita (FSM)** e **invariantes verificables de UI**, y cómo traducirlos a pruebas automatizadas en cualquier stack (React, Next.js, Vue, Nuxt, SvelteKit, Astro, Angular).

---

## 1. Matriz Heurística de Decisión FSM e Invariantes

| Escenario Detectado | Condición en el Requerimiento | Acción Exigida al Agente |
| :--- | :--- | :--- |
| **Mutaciones Críticas o Pagos** | Envío de dinero, checkout, borrado irreversible, cambios de permisos. | **OBLIGATORIO:** FSM `stateDiagram-v2`, invariante anti-doble envío (`NoDoubleSubmit`) y propagación de `Idempotency-Key`. |
| **Formularios Multi-Paso / Wizards** | Flujos de onboarding, checkout o registros con pasos secuenciales y validación dependiente. | **OBLIGATORIO:** FSM con transiciones permitidas/prohibidas y preservación de borrador ante errores transitorios. |
| **Widgets Interactivos Complejos** | `DataTable` con filtros/paginación/ordenamiento, combobox asíncrono, modales anidados, drag-and-drop. | **OBLIGATORIO:** FSM de interacción, sincronización de URL/estado y contrato estricto de foco por teclado. |
| **Flujos de Autenticación y Guardias** | Login, refresh de sesión, expiración de token, rutas protegidas por RBAC. | **OBLIGATORIO:** FSM de sesión y redirección limpia sin parpadeo de contenido privado. |
| **Componentes Presentacionales Puros** | Badges, botones básicos, tipografía, divisores o tarjetas estáticas sin efectos asíncronos. | **OMITIR FSM:** Declarar `fsm_required: false` en Frontmatter y documentar únicamente Props/Slots y estados CSS (`hover`/`focus`). |

---

## 2. Catálogo Estándar de Invariantes UI Verificables

Al redactar secciones `## Invariantes de UI` en flujos o componentes complejos, utiliza contratos concretos que se traduzcan directamente a aserciones en Vitest/Testing Library o Playwright:

1. **`NoDoubleSubmit`:** Mientras el estado sea `Submitting` o `Loading`, cualquier botón de confirmación debe estar deshabilitado (`disabled` / `aria-disabled="true"`) e ignorar clics o pulsaciones repetidas de `Enter`.
2. **`PreserveDraftOnError`:** Ante errores recuperables (`409`, `429`, `5xx`, timeout de red), los valores ingresados por el usuario deben permanecer intactos respecto al estado previo al envío.
3. **`FocusRestoration`:** Al cerrar un modal, diálogo o drawer (`Escape`, backdrop o botón cerrar), el foco del teclado debe regresar exactamente al elemento disparador original.
4. **`NoPrivilegedFlash`:** En rutas protegidas, mientras `authStatus === Unknown | Loading`, no se debe renderizar DOM perteneciente al área autenticada.
5. **`RollbackOnOptimisticFailure`:** Si se aplica actualización optimista en caché y la mutación remota falla, el estado visual debe revertirse exactamente al snapshot anterior y notificar el motivo.

---

## 3. Traducción Multi-Ecosistema hacia Pruebas Automatizadas

| Invariante | Traducción en Test Unitario (`Testing Library`) | Traducción en Test E2E (`Playwright`) |
| :--- | :--- | :--- |
| `NoDoubleSubmit` | `await user.dblClick(btn)` -> `expect(mutateSpy).toHaveBeenCalledTimes(1)` y `expect(btn).toBeDisabled()` | Interceptar request con delay; hacer doble clic y verificar `1` sola petición de red y botón `toBeDisabled()` |
| `PreserveDraftOnError` | Simular rechazo HTTP 500 -> `expect(input).toHaveValue("valor previo")` | `page.route(...)` abortando con 500 -> verificar contenido preservado en el input y presencia del `role="alert"` |
| `FocusRestoration` | Abrir diálogo -> `await user.keyboard("{Escape}")` -> `expect(triggerBtn).toHaveFocus()` | Pulsar `Escape` -> `await expect(triggerBtn).toBeFocused()` |
