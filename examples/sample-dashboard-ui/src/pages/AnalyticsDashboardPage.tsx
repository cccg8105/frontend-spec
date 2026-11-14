import React, { useState } from "react";
import { AnalyticsDataTable, AnalyticsRow } from "../features/analytics/AnalyticsDataTable";
import { ExportReportButton } from "../features/analytics/ExportReportButton";

const SAMPLE_ROWS: AnalyticsRow[] = [
  { id: "1", endpoint: "/api/v1/charges", status: "healthy", p95LatencyMs: 84, requests: 12450 },
  { id: "2", endpoint: "/api/v1/refunds", status: "degraded", p95LatencyMs: 312, requests: 940 },
];

export const AnalyticsDashboardPage: React.FC = () => {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [feedback, setFeedback] = useState<string | null>(null);

  const filtered = SAMPLE_ROWS.filter((row) =>
    row.endpoint.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <main className="min-h-screen bg-bgBase p-6 text-textMain">
      <header className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Analitica Operativa</h1>
          <p className="text-sm">Monitoreo en tiempo real de latencia y tasa de exito</p>
        </div>
        <ExportReportButton
          queryFilter={search}
          onExported={(id) => setFeedback(`Exportacion en cola: ${id}`)}
          onError={(detail) => setFeedback(detail)}
        />
      </header>

      <div className="mb-4">
        <label htmlFor="endpoint-filter" className="block text-sm font-medium mb-1">
          Filtrar por endpoint
        </label>
        <input
          id="endpoint-filter"
          type="search"
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
          placeholder="/api/v1/charges"
          className="w-full max-w-md rounded border border-border bg-surface px-3 py-2 text-sm"
        />
      </div>

      {feedback && (
        <div role="status" aria-live="polite" className="mb-4 rounded border border-border bg-surface p-3 text-sm">
          {feedback}
        </div>
      )}

      <AnalyticsDataTable
        rows={filtered}
        isLoading={false}
        page={page}
        totalPages={1}
        onPageChange={setPage}
        onRetry={() => setFeedback(null)}
        onClearFilters={() => {
          setSearch("");
          setPage(1);
        }}
      />
    </main>
  );
};
