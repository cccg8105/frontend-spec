---
artifact_type: routing-and-rendering
default_rendering_mode: hybrid
---

# Arquitectura de Rutas, Layouts y Renderizado — sample-dashboard-ui

## 1. Mapa Activo de Rutas

<!-- SYNC:ROUTES_TABLE:START -->
| Ruta | Flujo (`UF-*`) | Layout | Renderizado | Guardia (`Auth / RBAC`) | Fallback / Error |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/` | - | `PublicLayout` | `CSR` / `SSG` | Público | `GlobalErrorBoundary` |
| `*` | - | `PublicLayout` | Estático | Público | `NotFoundPage (404)` |
<!-- SYNC:ROUTES_TABLE:END -->

---

## 2. Reglas de Guardias, Error Boundaries y SEO
- **Guardias de Autenticación y RBAC:** Ninguna ruta protegida debe renderizar contenido privado mientras la sesión esté en estado `Loading` (`NoPrivilegedFlash`). Validar el parámetro `returnTo` para aceptar exclusivamente rutas internas relativas.
- **Manejo de Fallos por Segmento:** Cada sección de ruta crítica debe encapsularse en un Error Boundary que ofrezca recuperación no destructiva y registre el fallo sin exponer trazas internas al usuario.
- **Metadatos y SEO:** Las vistas públicas definen `<title>`, `<meta name="description">`, etiquetas OpenGraph y URL canónica según la API nativa del stack configurado.

---

## Historial de Revisiones (Últimos Cambios)

| Versión | Fecha | Requerimiento | Resumen del Cambio |
| :--- | :--- | :--- | :--- |
| `v1.0.0` | 2026-11-14 | `INIT` | Estructura base de rutas, guardias, Error Boundaries y política SEO. |

> *Nota: Esta tabla mantiene una ventana deslizante de los últimos 3 cambios. Para el historial completo, consultar [`docs/backlog/changelog.md`](../backlog/changelog.md).*
