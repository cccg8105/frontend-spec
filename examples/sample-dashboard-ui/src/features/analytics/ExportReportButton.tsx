import React, { useState } from "react";

export interface ExportReportButtonProps {
  queryFilter: string;
  onExported?: (reportId: string) => void;
  onError?: (problemDetail: string) => void;
}

export const ExportReportButton: React.FC<ExportReportButtonProps> = ({
  queryFilter,
  onExported,
  onError,
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleExport = async () => {
    if (isSubmitting) {
      return;
    }
    setIsSubmitting(true);
    try {
      const idempotencyKey = crypto.randomUUID();
      const response = await fetch("/api/v1/analytics/exports", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Idempotency-Key": idempotencyKey,
        },
        body: JSON.stringify({ filter: queryFilter }),
      });
      if (!response.ok) {
        const problem = await response.json().catch(() => ({ detail: "Error inesperado" }));
        onError?.(problem.detail ?? `HTTP ${response.status}`);
        return;
      }
      const data = await response.json();
      onExported?.(data.exportId);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <button
      type="button"
      disabled={isSubmitting}
      aria-busy={isSubmitting}
      onClick={handleExport}
      className="rounded bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
    >
      {isSubmitting ? "Exportando..." : "Exportar CSV"}
    </button>
  );
};
