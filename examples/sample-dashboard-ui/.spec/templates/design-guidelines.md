# Guías de Diseño Frontend (Anti-AI Slop & Alta Fidelidad)

> **Inspirado en la directiva canónica `frontend-design` de Anthropic.**
> Este documento rige la estética de cualquier componente generado en el framework.

---

## 1. Prohibiciones Estrictas (Eliminando el "AI Slop")
- **Degradados Púrpura/Índigo Genéricos:** Prohibido usar degradados estándar de fondo o texto (`from-indigo-500 to-purple-600`) sin una justificación de identidad de marca.
- **Tarjetas Blancas Idénticas:** No encierres cada sección de contenido en un contenedor blanco idéntico con bordes grises suaves y sombra difusa. Varía la densidad, el fondo y la separación mediante espacios en blanco y líneas divisorias sutiles.
- **Titulares con Palabras Teñidas:** Prohibido colorear arbitrariamente la última palabra de un titular en un tono llamativo por defecto.
- **Iconos Decorativos Sin Propósito:** Cada icono debe aportar significado operativo (acción o estado), no mero relleno visual.

---

## 2. Tipografía con Personalidad y Jerarquía
- Define roles tipográficos claros:
  - **Títulos y Display:** Tipografía con carácter y peso distintivo (ej. fuentes grotesk modernas, serif refinadas o monospace técnico según el dominio).
  - **Cuerpo y UI:** Tipografía con máxima legibilidad en tamaños pequeños (14px-16px) y espaciado entre letras equilibrado.
- Jerarquía estricta: escala visual evidente entre H1, H2, H3 y texto de soporte. Prohibido usar más de dos familias tipográficas por proyecto.

---

## 3. Paleta Cromática Deliberada (Regla de 4 a 6 Hex)
- Cada vista o componente debe ceñirse a una paleta restringida de **4 a 6 colores hexadecimales semánticos**:
  - `Background` (fondo principal)
  - `Surface` (superficie de contenido)
  - `Primary / Accent` (un único color de acento para acciones primarias)
  - `Text Primary` (alto contraste, mínimo 4.5:1 contra el fondo)
  - `Text Muted` (texto secundario legible)
  - `Border / Divider` (límites estructurales discretos)
- Soporte simétrico obligatorio para modo claro y modo oscuro.

---

## 4. Microcopy Directo y Humano
- Botones de acción claros y descriptivos: *"Guardar cambios"*, *"Crear cuenta"*, *"Exportar CSV"*.
- Prohibido el microcopy melodramático, vago o grandilocuente (evita *"Comienza tu viaje épico"* o *"Desata el poder de los datos"*).
- Mensajes de error que expliquen la causa y cómo solucionarlo en una sola línea.

---

## 5. Calidad de Interacción y Accesibilidad (a11y)
- **Foco por Teclado:** Todo elemento interactivo (`button`, `a`, `input`, `select`) debe contar con un anillo de foco visible (`focus-visible:ring-2 focus-visible:outline-none`).
- **Estados Interactivos Perceptibles:** Todo control debe definir estados claros para `hover`, `active`, `disabled` y `loading`.
- **Diseño Mobile-First:** El layout debe responder limpiamente a pantallas pequeñas sin desbordamiento horizontal (`overflow-x-hidden`).

---

## 6. Movimiento Intencional, Densidad e Internacionalización
- **Micro-interacciones Aceleradas y Respeto a `prefers-reduced-motion`:** Anima únicamente propiedades compuestas por GPU (`transform`, `opacity`). Respeta siempre `@media (prefers-reduced-motion: reduce)` reduciendo transiciones a `0ms`.
- **Asimetría y Jerarquía Espacial:** Prioriza el elemento operativo principal de la vista (ej. acción primaria, gráfico o tabla de trabajo) en lugar de rejillas simétricas monótonas de 3 tarjetas idénticas.
- **Externalización de Copy (i18n-ready):** Si el proyecto habilita soporte multi-idioma en `docs/technical/tech-stack.md`, prohíbe concatenar literales de interfaz dentro de componentes; usa claves semánticas de traducción.
