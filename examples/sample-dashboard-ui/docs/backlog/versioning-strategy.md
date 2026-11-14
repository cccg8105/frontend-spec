# Estrategia y Gobernanza de Versionamiento — sample-dashboard-ui

> **Instrucción para el Agente de IA:**
> Clasifica toda solicitud del usuario mediante esta guía antes de abrir un requerimiento `REQ-UI-*` en `docs/backlog/pending.md`.

---

## 1. Esquema Activo: `SemVer 2.0.0` (`semver`)
- **Archivo Manifiesto Sincronizado:** `package.json`
- **Versión Base:** `v1.0.0`
- **Milestone Activo:** `v1.1.0`

---

## 2. Clasificación de Impacto y Dos Velocidades

### A. `MAJOR` — Cambio Incompatible (Carril Completo)
- Rediseño integral de layouts raíz o eliminación/cambio incompatible de rutas públicas.
- Cambio incompatible en tokens base o contratos públicos de componentes compartidos/design system.
- **Ceremonia exigida:** Entrevista `/grill-me / /ui-grill` -> Flujo UX (`UF-*`) -> FSM/Invariantes según matriz -> Tokens/Rutas/Componentes/Estado -> Tests Unit (`axe`) + Playwright E2E -> `pending.md` -> Gatekeeper `/plan`.

### B. `MINOR` — Nueva Capacidad UI Retrocompatible (Carril Completo)
- Nuevas vistas, rutas, componentes complejos (`DataTable`, formularios con API), nuevos tokens semánticos o soporte de estado.
- **Ceremonia exigida:** Entrevista `/grill-me / /ui-grill` -> Flujo UX (`UF-*`) -> FSM/Invariantes según matriz heurística -> Documentación técnica afectada -> Test *Spec-First* -> `pending.md` -> Gatekeeper `/plan`.

### C. `PATCH` — Fix Visual, de Estado o Accesibilidad (**Carril Fast-Track / Micro-Spec**)
- Ajustes de alineación/espaciado con tokens existentes, corrección de bugs de estado local, corrección de `aria-*`/contraste o refactor interno sin cambiar rutas, contratos API ni props públicas.
- **Ceremonia reducida (*Fast-Track*):**
  1. **Omite** crear nuevos flujos UX (`Referencia Funcional: N/A (PATCH / Fast-Track)` o referencia al `UF-*` corregido).
  2. Registra bloque compacto en `pending.md` declarando fronteras exactas de archivos.
  3. Aplica protocolo `/diagnose` + escribe primero el test de regresión en rojo -> confirmación breve -> aplica el fix mínimo.

---

## 3. Reglas por Esquema Soportado
- **`semver`:** `MAJOR.MINOR.PATCH` (incremento en `package.json` + `.spec/config.yaml`).
- **`calver`:** `YYYY.MM.MICRO` para aplicaciones de despliegue continuo por ciclo calendario.
- **`sequential`:** Incremento secuencial de release (`v1`, `v2`).
