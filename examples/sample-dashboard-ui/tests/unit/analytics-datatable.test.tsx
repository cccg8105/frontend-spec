import { describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { axe } from "vitest-axe";
import { AnalyticsDataTable } from "../../src/features/analytics/AnalyticsDataTable";
import { AnalyticsDashboardPage } from "../../src/pages/AnalyticsDashboardPage";

describe("AnalyticsDataTable y AnalyticsDashboardPage", () => {
  it("renderiza filas y cumple WCAG 2.1 AA sin violaciones", async () => {
    const { container } = render(<AnalyticsDashboardPage />);
    expect(screen.getByText("/api/v1/charges")).toBeTruthy();
    const results = await axe(container);
    expect(results.violations).toHaveLength(0);
  });

  it("muestra estado de error con boton de reintento accesible", () => {
    const onRetry = vi.fn();
    render(
      <AnalyticsDataTable
        rows={[]}
        isLoading={false}
        errorMessage="Fallo temporal 500"
        page={1}
        totalPages={1}
        onPageChange={vi.fn()}
        onRetry={onRetry}
        onClearFilters={vi.fn()}
      />
    );
    expect(screen.getByRole("alert")).toBeTruthy();
    screen.getByRole("button", { name: "Reintentar" }).click();
    expect(onRetry).toHaveBeenCalledTimes(1);
  });
});
