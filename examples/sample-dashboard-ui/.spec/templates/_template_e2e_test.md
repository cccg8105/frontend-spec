# Blueprint: Pruebas E2E, Responsive, Modo Oscuro y Accesibilidad (Playwright)

> **Cobertura para `e2e_runner: playwright` en flujos críticos `UF-*` (`MAJOR` / `MINOR`).**
> Verifica la aplicación real en navegador (flujos de navegación, guardias de ruta, viewports responsive y escaneo WCAG automatizado).

---

## Plantilla Canónica Playwright + `@axe-core/playwright`

```typescript
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

/**
 * @spec UF-[DOMINIO]-[ID]
 * @req REQ-UI-[DOMINIO]-[ID]
 */
test.describe("UF-[DOMINIO]-[ID]: Flujo Crítico End-to-End", () => {
  test("completa el flujo feliz y supera auditoría WCAG 2.1 AA", async ({ page }) => {
    await test.step("1. Navegar y esperar hidratación / red asentada", async () => {
      await page.goto("/ruta-objetivo");
      await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    });

    await test.step("2. Ejecutar acción principal con selectores semánticos", async () => {
      await page.getByLabel(/correo electrónico/i).fill("usuario@empresa.com");
      await page.getByRole("button", { name: /guardar cambios/i }).click();
      await expect(page.getByRole("status")).toContainText(/guardado/i);
    });

    await test.step("3. Auditar accesibilidad WCAG AA", async () => {
      const scan = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
        .analyze();
      expect(scan.violations).toEqual([]);
    });
  });

  test("preserva layout sin desbordamiento horizontal en móvil y modo oscuro", async ({ page }) => {
    await page.emulateMedia({ colorScheme: "dark" });
    await page.setViewportSize({ width: 390, height: 844 }); // Mobile
    await page.goto("/ruta-objetivo");

    const hasHorizontalOverflow = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    expect(hasHorizontalOverflow).toBe(false);
  });
});
```

### Viewports Mínimos de Verificación Responsive:
- **Mobile:** `390 x 844`
- **Tablet:** `768 x 1024`
- **Desktop:** `1280 x 800`
