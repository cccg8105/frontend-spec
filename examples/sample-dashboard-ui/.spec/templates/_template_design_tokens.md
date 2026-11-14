---
artifact_type: design-tokens
theme_modes:
  - light
  - dark
---

# Blueprint: Design Tokens y Temas Ejecutables

> **Inspirado en `theme-factory` de Anthropic.**
> Define variables semánticas portables entre Tailwind CSS (`@theme`), `shadcn-ui`, CSS Modules, PrimeVue, Angular Material o CSS estándar con simetría obligatoria claro/oscuro.

---

## 1. Paleta Cromática Semántica (4-6 Hex Base + Estados)

| Token Semántico | Rol de Uso | Modo Claro (Hex) | Modo Oscuro (Hex) | Contraste Mínimo |
| :--- | :--- | :--- | :--- | :--- |
| `color-bg-base` | Fondo principal del viewport | `#F8F9FA` | `#0D1117` | Base |
| `color-surface` | Superficies elevadas, paneles y cards | `#FFFFFF` | `#161B22` | > 1.2:1 vs Base |
| `color-primary` | Acciones primarias y estado activo | `#0F52BA` | `#388BFD` | >= 4.5:1 vs texto |
| `color-primary-hover` | Interacción hover de acción primaria | `#0C4196` | `#58A6FF` | Perceptible |
| `color-text-main` | Texto principal de lectura y títulos | `#1A202C` | `#F0F6FC` | >= 7:1 vs Surface |
| `color-text-muted` | Subtítulos, labels y metadata | `#526071` | `#9CA3AF` | >= 4.5:1 vs Surface |
| `color-border` | Divisores y bordes de controles | `#E2E8F0` | `#30363D` | >= 3:1 en inputs |
| `color-danger` | Errores de validación y acciones destructivas | `#DC2626` | `#F85149` | >= 4.5:1 |

---

## 2. Tipografía, Espaciado, Elevación, Z-Index y Breakpoints

```css
:root {
  /* Colores Base */
  --color-bg-base: #F8F9FA;
  --color-surface: #FFFFFF;
  --color-primary: #0F52BA;
  --color-primary-hover: #0C4196;
  --color-text-main: #1A202C;
  --color-text-muted: #526071;
  --color-border: #E2E8F0;
  --color-danger: #DC2626;

  /* Tipografía (máximo 2 familias) */
  --font-display: "Plus Jakarta Sans", -apple-system, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Espaciado Modular (base 4px) */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2.5rem;

  /* Radios y Elevación */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.06);
  --shadow-md: 0 4px 12px rgba(15, 23, 42, 0.08);

  /* Z-Index */
  --z-base: 0;
  --z-sticky: 20;
  --z-overlay: 40;
  --z-modal: 50;
  --z-toast: 60;

  /* Movimiento */
  --duration-fast: 150ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
}

.dark {
  --color-bg-base: #0D1117;
  --color-surface: #161B22;
  --color-primary: #388BFD;
  --color-primary-hover: #58A6FF;
  --color-text-main: #F0F6FC;
  --color-text-muted: #9CA3AF;
  --color-border: #30363D;
  --color-danger: #F85149;
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0ms;
  }
}
```

### Breakpoints Oficiales:
- `sm`: `640px` | `md`: `768px` | `lg`: `1024px` | `xl`: `1280px`

---

## 3. Mapeo a Librerías y Motores CSS

| Token Semántico | Tailwind v4 (`@theme`) / `shadcn-ui` | CSS Modules / Vanilla / Angular / Vue |
| :--- | :--- | :--- |
| `color-bg-base` | `--background` / `bg-bg-base` | `var(--color-bg-base)` |
| `color-surface` | `--card` / `bg-surface` | `var(--color-surface)` |
| `color-primary` | `--primary` / `bg-primary` | `var(--color-primary)` |
| `color-text-main` | `--foreground` / `text-main` | `var(--color-text-main)` |
| `color-border` | `--border` / `border-border` | `var(--color-border)` |
| `color-danger` | `--destructive` / `text-danger` | `var(--color-danger)` |

---

## Historial de Revisiones (Últimos Cambios)

| Versión | Fecha | Requerimiento | Resumen del Cambio |
| :--- | :--- | :--- | :--- |
| `v0.1.0` | YYYY-MM-DD | `INIT` | Definición inicial de tokens y mapeo multi-stack. |

> *Nota: Esta tabla mantiene una ventana deslizante de los últimos 3 cambios. Para el historial completo, consultar `docs/backlog/changelog.md`.*
