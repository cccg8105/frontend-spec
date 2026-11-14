---
artifact_type: tech-stack
ecosystem: "{{ECOSYSTEM_NAME}}"
---

# Stack Tecnológico, Presupuestos y Políticas Transversales Frontend — {{PROJECT_NAME}}

## 1. Núcleo Tecnológico del Proyecto

<!-- SYNC:TECH_STACK:START -->
| Capa | Tecnología Activa | Notas de Configuración |
| :--- | :--- | :--- |
| **Ecosistema / Meta-Framework** | `{{RUNTIME_LABEL}}` (`{{ECOSYSTEM_NAME}}`) | Manifiesto `{{MANIFEST_FILE}}` (`v{{CURRENT_VERSION}}`) |
| **Lenguaje** | `{{LANGUAGE_NAME}}` | Tipado estricto en Props, contratos API y Stores |
| **Estilos y Primitivas** | `{{STYLING}}` + `{{UI_PRIMITIVES}}` | Consumo estricto de `docs/design/tokens-and-themes.md` |
| **Estado Remoto y Mocks** | `{{STATE_SERVER}}` + MSW | Caché declarativa y contratos HTTP simulados |
| **Testing y a11y** | `{{UNIT_TEST_RUNNER}}` + `{{TESTING_LIBRARY}}` + `axe-core` + `{{E2E_RUNNER}}` | Cobertura unitaria, WCAG 2.1 AA y E2E responsive |
<!-- SYNC:TECH_STACK:END -->

---

## 2. Presupuestos de Rendimiento (Core Web Vitals)
- **LCP:** `<= 2.5 s` (P75 móvil) | **INP:** `<= 200 ms` | **CLS:** `<= 0.1`
- **Bundle Inicial por Ruta:** `<= 200 KB` gzip mediante *code-splitting* por ruta y carga diferida de módulos pesados.

---

## 3. Políticas de Seguridad, i18n y Observabilidad
- **Prevención XSS:** Prohibido renderizar HTML sin sanitización previa (`DOMPurify`) o aceptar URLs `javascript:`.
- **Tokens y Sesión:** Priorizar cookies `HttpOnly; Secure; SameSite` para credenciales sensibles; nunca almacenar secretos en `localStorage`.
- **i18n:** Centralizar literales de usuario (claves de diccionario o módulo único de copy según necesidad de idiomas del producto).
- **Observabilidad:** Reportar fallos no capturados desde Error Boundaries sin registrar PII ni cabeceras de autorización.

---

## Historial de Revisiones (Últimos Cambios)

| Versión | Fecha | Requerimiento | Resumen del Cambio |
| :--- | :--- | :--- | :--- |
| `v{{CURRENT_VERSION}}` | {{TODAY}} | `INIT` | Configuración base para `{{RUNTIME_LABEL}}`, presupuestos Web Vitals y seguridad XSS. |

> *Nota: Esta tabla mantiene una ventana deslizante de los últimos 3 cambios. Para el historial completo, consultar [`docs/backlog/changelog.md`](../backlog/changelog.md).*
