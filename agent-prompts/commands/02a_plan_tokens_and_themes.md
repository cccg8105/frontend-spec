# Comando: 02a_plan_tokens_and_themes

> **Propósito:** Definir o extender los tokens semánticos de diseño y su mapeo técnico (Etapa 2A).

## Instrucciones para el Agente:
1. Revisa `docs/design/tokens-and-themes.md`, `.spec/templates/_template_design_tokens.md` y `.spec/templates/design-guidelines.md`.
2. Evalúa si los tokens vigentes cubren el requerimiento; evita proliferar nuevos colores sin justificación semántica (mantén paleta restringida de 4-6 hex base + estados).
3. Si se requieren nuevos tokens:
   - Define equivalentes simétricos para modo **claro** y modo **oscuro**.
   - Verifica contraste WCAG AA (`>= 4.5:1` texto normal, `>= 3:1` texto grande y bordes interactivos).
   - Documenta el mapeo hacia variables CSS (`:root` / `.dark`), Tailwind `@theme` / `shadcn-ui`, o el adaptador del stack configurado en `.spec/config.yaml`.
4. Registra elevaciones, capas `z-index`, breakpoints y política `prefers-reduced-motion` si introducen overlays, modales o animaciones.
5. Actualiza `Historial de Revisiones` (máx. 3 filas) en `docs/design/tokens-and-themes.md` y el resumen en `docs/design/index.md`.
