# Índice del Sistema de Diseño — sample-dashboard-ui

> **Instrucción para el Agente de IA:**
> Toda decisión estética, cromática, tipográfica y de movimiento debe validarse contra estos artefactos antes de generar markup o estilos.
> - Reglas visuales Anti-AI Slop y WCAG: [`.spec/templates/design-guidelines.md`](../../.spec/templates/design-guidelines.md)
> - Catálogo activo de tokens claro/oscuro: [`tokens-and-themes.md`](./tokens-and-themes.md)
> - Molde ejecutable de referencia: [`.spec/templates/_template_design_tokens.md`](../../.spec/templates/_template_design_tokens.md)

---

## Artefactos de Identidad Visual

| Artefacto | Archivo | Responsabilidad |
| :--- | :--- | :--- |
| **Tokens y Temas** | [tokens-and-themes.md](./tokens-and-themes.md) | Paleta semántica (claro/oscuro), tipografía, espaciado, elevación, z-index, breakpoints y mapeo CSS/Tailwind. |
| **Guías Anti-AI Slop** | [design-guidelines.md](../../.spec/templates/design-guidelines.md) | Prohibiciones visuales, contraste, microcopy directo, foco por teclado y `prefers-reduced-motion`. |

---

## Resumen de Tokens Activos

<!-- SYNC:DESIGN_TOKENS_SUMMARY:START -->
- **Modos activos:** `light`, `dark` (8 tokens cromáticos semánticos).
- **Tipografías:** `"Plus Jakarta Sans", -apple-system, sans-serif` (display/UI) y `"JetBrains Mono", monospace` (monoespacio).
- **Regla estricta:** Prohibido quemar colores hex, tamaños arbitrarios o `z-index` fuera del catálogo semántico en [`tokens-and-themes.md`](./tokens-and-themes.md).
<!-- SYNC:DESIGN_TOKENS_SUMMARY:END -->
