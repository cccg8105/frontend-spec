---
description: "Planifica un requerimiento UI siguiendo frontend-spec (Dos Velocidades) y deteniendose para aprobacion antes de implementar."
---

# /ui-plan — Planificacion Spec-Driven UI (Windsurf)

1. **Contexto Selectivo O(1):**
   - Lee `docs/functional/index.md`, `docs/design/index.md` y `docs/technical/index.md` (y consulta `graphify-out/graph.json` si existe) antes de explorar multiples archivos fuente.
   - Si toca rutas en `Módulos / Rutas Legadas Detectadas`, documenta primero el flujo *As-Is*.
2. **Clasificacion de Impacto (`docs/backlog/versioning-strategy.md`):**
   - **`MAJOR` / `MINOR` (Carril Completo):** Ejecuta `/ui-grill` si hay decisiones abiertas sobre FSM, estados borde, rutas/RBAC o tokens. Luego redacta o actualiza `UF-*`, diagrama/invariantes FSM (`ui-contracts-guidelines.md`), tokens claro/oscuro, rutas, componentes, estado y el test *Spec-First*.
   - **`PATCH` (Fast-Track):** Para ajustes con tokens existentes, fixes a11y, bugs locales o parches Dependabot compatibles (`REQ-UI-SEC-*` verificados via `gh api "repos/{owner}/{repo}/dependabot/alerts?state=open"` y auditor local) sin cambiar rutas/props/API. Usa `Referencia Funcional: N/A (PATCH / Fast-Track)` y prepara test de regresion en rojo (upgrades `MAJOR` con impacto en `src/` pasan a Carril Completo).
3. **Registro en `docs/backlog/pending.md`:**
   - Crea la entrada `REQ-UI-*` declarando rutas exactas (`[NEW]`, `[MODIFY]`, `[DELETE]`) y criterios de aceptacion.
4. **Gatekeeper Obligatorio:**
   - Detente sin modificar codigo fuente y presenta el resumen al usuario. Una vez aprobado, ejecuta `/ui-execute`.
