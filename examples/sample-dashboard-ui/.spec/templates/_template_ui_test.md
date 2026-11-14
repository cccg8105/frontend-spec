# Blueprint: Pruebas Unitarias, de Interacción y Accesibilidad (Multi-Ecosistema)

> **Inspirado en `webapp-testing` de Anthropic y alineado con el patrón Spec-First.**
> Todo requerimiento `MAJOR`/`MINOR` genera su scaffolding antes de codificar; todo `PATCH` Fast-Track crea primero su test de regresión en rojo.

---

## 1. Estructura Obligatoria (*Reconnaissance-Then-Action*)
1. **Trazabilidad:** Etiquetas `@spec UF-[DOMINIO]-[ID]` (o `CMP-[DOMINIO]-[ID]`), `@req REQ-UI-[DOMINIO]-[ID]` e `@invariant`.
2. **Renderizado e Hidratación:** Confirmar estado inicial y consumo correcto de roles semánticos.
3. **Interacción Real (`userEvent`):** Clics, teclado (`Tab`, `Enter`, `Escape`), validación de formularios y verificación anti-doble envío (`NoDoubleSubmit`).
4. **Estados Borde:** Loading (`aria-busy="true"`), Empty State (`CTA` visible) y Error RFC 7807 preservando inputs.
5. **Accesibilidad Automática (`axe`):** Cero violaciones críticas o serias de WCAG 2.1 AA.

---

## 2. Plantilla Vitest + `@testing-library/react` + `vitest-axe`

```typescript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { axe } from "vitest-axe";
import { describe, it, expect, vi } from "vitest";
import { TargetComponent } from "./TargetComponent";

/**
 * @spec UF-[DOMINIO]-[ID]
 * @req REQ-UI-[DOMINIO]-[ID]
 */
describe("CMP-[DOMINIO]-[ID]: TargetComponent", () => {
  it("renderiza estado inicial y cumple WCAG AA automático", async () => {
    const { container } = render(<TargetComponent title="Resumen" />);
    expect(screen.getByRole("heading", { name: /resumen/i })).toBeInTheDocument();
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  /** @invariant NoDoubleSubmit */
  it("evita doble envío durante estado Submitting y maneja interacción de usuario", async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn().mockImplementation(() => new Promise(() => {}));
    render(<TargetComponent onSubmit={onSubmit} />);

    const btn = screen.getByRole("button", { name: /guardar cambios/i });
    await user.dblClick(btn);

    expect(onSubmit).toHaveBeenCalledTimes(1);
    expect(btn).toBeDisabled();
  });

  it("renderiza indicadores accesibles de carga y error preservando borrador", () => {
    render(<TargetComponent isLoading={true} errorMessage="Error de red" />);
    expect(screen.getByRole("status")).toHaveAttribute("aria-busy", "true");
    expect(screen.getByRole("alert")).toHaveTextContent(/error de red/i);
  });
});
```

---

## 3. Adaptación para Otros Ecosistemas Soportados

- **Vue / Nuxt (`@testing-library/vue` + `vitest-axe`):** Sustituir `render(<TargetComponent ... />)` por `render(TargetComponent, { props: { ... } })`; mantener intactas las consultas `screen.getByRole`, `userEvent` y `await axe(container)`.
- **Svelte / SvelteKit (`@testing-library/svelte` + `vitest-axe`):** Usar `render(TargetComponent, { props: { ... } })` junto con `userEvent` y aserciones ARIA idénticas.
- **Angular (`@testing-library/angular` + `jest-axe`/`vitest-axe`):** Usar `await render(TargetComponent, { componentInputs: { ... } })` y consultar el DOM renderizado mediante `screen.getByRole` / `userEvent`.
