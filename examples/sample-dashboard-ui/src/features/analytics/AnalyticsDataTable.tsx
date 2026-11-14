import React from "react";

export interface AnalyticsRow {
  id: string;
  endpoint: string;
  status: "healthy" | "degraded";
  p95LatencyMs: number;
  requests: number;
}

export interface AnalyticsDataTableProps {
  rows: AnalyticsRow[];
  isLoading: boolean;
  errorMessage?: string | null;
  page: number;
  totalPages: number;
  onPageChange: (nextPage: number) => void;
  onRetry: () => void;
  onClearFilters: () => void;
}

export const AnalyticsDataTable: React.FC<AnalyticsDataTableProps> = ({
  rows,
  isLoading,
  errorMessage,
  page,
  totalPages,
  onPageChange,
  onRetry,
  onClearFilters,
}) => {
  if (isLoading) {
    return (
      <div aria-busy="true" aria-label="Cargando metricas" className="rounded-lg border border-border bg-surface p-4">
        <div className="h-6 w-1/3 animate-pulse rounded bg-border mb-3" />
        <div className="h-24 w-full animate-pulse rounded bg-border" />
      </div>
    );
  }

  if (errorMessage) {
    return (
      <div role="alert" className="rounded-lg border border-danger bg-surface p-4 text-textMain">
        <p className="font-semibold text-danger">Error al consultar metricas</p>
        <p className="text-sm mt-1">{errorMessage}</p>
        <button
          type="button"
          onClick={onRetry}
          className="mt-3 rounded bg-primary px-3 py-1.5 text-sm text-white"
        >
          Reintentar
        </button>
      </div>
    );
  }

  if (rows.length === 0) {
    return (
      <div className="rounded-lg border border-border bg-surface p-6 text-center text-textMain">
        <p className="font-medium">No hay registros para los filtros seleccionados.</p>
        <button
          type="button"
          onClick={onClearFilters}
          className="mt-3 rounded bg-primary px-4 py-2 text-sm text-white"
        >
          Limpiar filtros
        </button>
      </div>
    );
  }

  return (
    <section aria-label="Tabla de metricas operativas" className="rounded-lg border border-border bg-surface">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-textMain">
          <thead className="border-b border-border">
            <tr>
              <th scope="col" className="p-3">Endpoint</th>
              <th scope="col" className="p-3">Estado</th>
              <th scope="col" className="p-3">P95 (ms)</th>
              <th scope="col" className="p-3">Peticiones</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id} className="border-b border-border last:border-b-0">
                <td className="p-3 font-mono">{row.endpoint}</td>
                <td className="p-3">{row.status}</td>
                <td className="p-3">{row.p95LatencyMs}</td>
                <td className="p-3">{row.requests}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <nav aria-label="Paginacion" className="flex items-center justify-between p-3 border-t border-border">
        <span aria-live="polite" className="text-xs">
          Pagina {page} de {totalPages}
        </span>
        <div className="flex gap-2">
          <button
            type="button"
            disabled={page <= 1}
            onClick={() => onPageChange(page - 1)}
            className="rounded border border-border px-3 py-1 text-xs disabled:opacity-50"
          >
            Anterior
          </button>
          <button
            type="button"
            disabled={page >= totalPages}
            onClick={() => onPageChange(page + 1)}
            className="rounded border border-border px-3 py-1 text-xs disabled:opacity-50"
          >
            Siguiente
          </button>
        </div>
      </nav>
    </section>
  );
};
