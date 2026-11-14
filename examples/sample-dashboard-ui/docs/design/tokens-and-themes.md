---
artifact_type: design-tokens
theme_modes:
  - light
  - dark
---

# Sistema de Tokens y Temas — sample-dashboard-ui

> **Catálogo canónico de tokens semánticos para consumo en componentes y utilidades CSS.**

---

## 1. Colores Semánticos (Simetría Claro / Oscuro)

| Token | Modo Claro | Modo Oscuro | Rol de Uso |
| :--- | :--- | :--- | :--- |
| `color-bg-base` | `#F8F9FA` | `#0D1117` | Fondo principal |
| `color-surface` | `#FFFFFF` | `#161B22` | Tarjetas, paneles y modales |
| `color-primary` | `#0F52BA` | `#388BFD` | Acción primaria y acento |
| `color-primary-hover` | `#0C4196` | `#58A6FF` | Estado hover de acción primaria |
| `color-text-main` | `#1A202C` | `#F0F6FC` | Texto principal de lectura (>= 7:1) |
| `color-text-muted` | `#526071` | `#9CA3AF` | Etiquetas y texto auxiliar (>= 4.5:1) |
| `color-border` | `#E2E8F0` | `#30363D` | Límites y divisores |
| `color-danger` | `#DC2626` | `#F85149` | Errores y acciones destructivas |

---

## 2. Tipografía, Escala Modular, Elevación y Breakpoints

- **Display / UI:** `"Plus Jakarta Sans", -apple-system, sans-serif`
- **Monospace:** `"JetBrains Mono", monospace`
- **Espaciado:** `xs: 4px`, `sm: 8px`, `md: 16px`, `lg: 24px`, `xl: 40px`
- **Radios:** `sm: 4px`, `md: 8px`, `lg: 12px`
- **Z-Index:** `base: 0`, `sticky: 20`, `overlay: 40`, `modal: 50`, `toast: 60`
- **Breakpoints:** `sm: 640px`, `md: 768px`, `lg: 1024px`, `xl: 1280px`
- **Movimiento:** `150ms` estándar, reducido automáticamente a `0ms` con `prefers-reduced-motion: reduce`.

---

## 3. Mapeo Técnico Portable

Los tokens semánticos se exponen mediante variables CSS (`:root` / `.dark`) y deben mapearse a `--background`, `--foreground`, `--primary`, `--border` y `--destructive` según el adaptador CSS de [`docs/technical/tech-stack.md`](../technical/tech-stack.md).

---

## Historial de Revisiones (Últimos Cambios)

| Versión | Fecha | Requerimiento | Resumen del Cambio |
| :--- | :--- | :--- | :--- |
| `v1.0.0` | 2026-11-14 | `INIT` | Catálogo inicial simétrico claro/oscuro, tipografía, z-index y breakpoints. |

> *Nota: Esta tabla mantiene una ventana deslizante de los últimos 3 cambios. Para el historial completo, consultar [`docs/backlog/changelog.md`](../backlog/changelog.md).*
