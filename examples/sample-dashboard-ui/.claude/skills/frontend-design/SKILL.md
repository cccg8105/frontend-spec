---
name: frontend-design
description: "Directivas Anti-AI Slop para construir interfaces web de alta fidelidad en cualquier stack (React, Next.js, Vue/Nuxt, SvelteKit, Astro, Angular) con tipografía intencional, paleta restringida y WCAG AA."
---

# frontend-design Skill

Esta skill rige la calidad visual, ergonómica y de accesibilidad de toda interfaz producida bajo `frontend-spec`, eliminando patrones genéricos de IA ("AI slop").

## Directivas Esenciales
1. **Prohibiciones Anti-AI Slop:**
   - Cero degradados púrpura/índigo por defecto (`from-indigo-500 to-purple-600`).
   - Prohibido envolver cada bloque en tarjetas blancas idénticas con sombra difusa uniforme; usa densidad variable, jerarquía espacial y separadores sutiles.
   - Prohibido teñir la última palabra de los titulares arbitrariamente o añadir iconos decorativos sin significado operativo.
2. **Tipografía con Carácter y Escala Clara:** Usa un máximo de 2 familias definidas en `docs/design/tokens-and-themes.md` con jerarquía evidente entre títulos, lectura (`14px-16px`) y datos monoespaciados.
3. **Paleta Restringida y Tokens Obligatorios:** Cíñete a los 4-6 hex base + estados de `docs/design/tokens-and-themes.md` con soporte simétrico claro/oscuro. Prohibido quemar colores hex, `px` o `z-index` ad-hoc.
4. **Microcopy Directo e i18n:** Etiquetas precisas orientadas a acción (*"Guardar cambios"*, *"Reintentar envío"*); errores de una línea explicando causa y recuperación. Respeta claves i18n si `docs/technical/tech-stack.md` lo exige.
5. **Accesibilidad y Rendimiento Visual:**
   - Anillos `focus-visible` claros en todo elemento interactivo y navegación completa por teclado.
   - Todos los estados completos (`hover`, `active`, `focus-visible`, `disabled`, `loading`, `empty`, `error`).
   - Diseño *mobile-first* sin `overflow-x` horizontal; animaciones solo en `transform`/`opacity` respetando `prefers-reduced-motion`.
