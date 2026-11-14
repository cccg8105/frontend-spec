import { http, HttpResponse } from "msw";

export const analyticsHandlers = [
  http.get("/api/v1/analytics/metrics", ({ request }) => {
    const url = new URL(request.url);
    const q = url.searchParams.get("q") ?? "";
    if (q === "force-500") {
      return HttpResponse.json(
        {
          type: "https://api.example.com/problems/internal-error",
          title: "Service Unavailable",
          status: 500,
          detail: "No fue posible consultar las metricas en este momento.",
        },
        { status: 500, headers: { "Content-Type": "application/problem+json" } }
      );
    }
    return HttpResponse.json({
      items: [
        { id: "1", endpoint: "/api/v1/charges", status: "healthy", p95LatencyMs: 84, requests: 12450 },
      ],
      totalPages: 1,
    });
  }),

  http.post("/api/v1/analytics/exports", ({ request }) => {
    if (!request.headers.get("Idempotency-Key")) {
      return HttpResponse.json(
        {
          type: "https://api.example.com/problems/missing-idempotency-key",
          title: "Missing Idempotency-Key",
          status: 422,
          detail: "La cabecera Idempotency-Key es obligatoria para exportaciones.",
        },
        { status: 422, headers: { "Content-Type": "application/problem+json" } }
      );
    }
    return HttpResponse.json({ exportId: "exp_001" }, { status: 201 });
  }),
];
