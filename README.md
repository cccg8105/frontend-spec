# frontend-spec v1.1.0

> **Framework y CLI de Especificación Viva para Ingeniería Frontend Multi-Ecosistema asistida por Agentes de IA (Spec-Driven Frontend)**

`frontend-spec` es la contraparte frontend de `backend-spec`. Estructura la colaboración entre desarrolladores y agentes de IA en aplicaciones web (**React/Vite, Next.js, Vue/Nuxt, SvelteKit, Astro y Angular**) para erradicar el *"vibe coding"* mediante cinco pilares:

1. **Multi-Ecosistema con Abstracción Única:** Contratos portables de flujos, componentes (`Props`/Slots/FSM), rutas y testing.
2. **Diseño Intencional Anti-AI Slop:** Tipografía con carácter, paleta acotada, asimetría espacial y respeto a `prefers-reduced-motion`.
3. **Tokens Ejecutables Claro/Oscuro:** Paleta simétrica, contraste WCAG y variables CSS/Tailwind sin valores quemados.
4. **Contratos Draft-07 y Puente Backend:** Validación sin dependencias (`schemas/`) para flujos UX, estado servidor, RFC 7807, `Idempotency-Key`, MSW, Web Vitals y XSS/CSP.
5. **Gatekeeper de Dos Velocidades:** Rigor completo para cambios `MAJOR`/`MINOR` y carril ligero *Fast-Track* para `PATCH`.

---

## Instalación Rápida

Requiere únicamente Python `>=3.9` (sin dependencias externas en tiempo de ejecución):

```bash
uv tool install git+https://github.com/cccg8105/frontend-spec.git
```

Consulta [`guides/04-cli-harnesses-and-contracts.md`](guides/04-cli-harnesses-and-contracts.md) para opciones con `pipx`/`uvx`, actualización con `fspec update` o instalación local editable.

---

## Guías por Escenario de Uso

Elige la guía operativa según el estado actual de tu repositorio:

| Escenario | Punto de Partida | Guía Paso a Paso |
| :--- | :--- | :--- |
| **1. Proyecto Nuevo con Scaffold** *(Recomendado)* | Acabas de crear la app con `create-vite`, `create-next-app`, `nuxi` o `ng new`. | [Guía 01 — Sección A: Nuevo con Scaffold](guides/01-new-projects-greenfield.md#escenario-a-repositorio-nuevo-con-scaffold) |
| **2. Repositorio Totalmente Vacío** (*Zero-File*) | Carpeta vacía donde diseñas flujos UX, tokens y contratos antes de instalar código. | [Guía 01 — Sección B: Repositorio Vacío](guides/01-new-projects-greenfield.md#escenario-b-repositorio-totalmente-vacio) |
| **3. Repositorio Existente (*Brownfield*)** | Aplicación en desarrollo o producción que adoptará el framework con `fspec bootstrap`. | [Guía 02 — Adopción en Repositorios Existentes](guides/02-existing-projects-brownfield.md) |
| **4. Flujo de Trabajo Diario** | Operación cotidiana del Carril Completo (`MAJOR`/`MINOR`), Fast-Track (`PATCH`) y harnesses. | [Guía 03 — Flujo Diario de Dos Velocidades](guides/03-daily-workflow-two-speeds.md) |

---

## Referencia Técnica y Recursos

* **[Guía 04: CLI, Harnesses, Estructura y Contratos (`v1.0.0+`)](guides/04-cli-harnesses-and-contracts.md):** Catálogo de los 7 subcomandos (`init`, `update`, `bootstrap`, `req:new`, `sync`, `check`, `resolve`), estructura del repositorio y del proyecto consumidor, coexistencia en monorepos (`FRONTEND-SPEC:START/END`), los 8 JSON Schemas Draft-07 y contratos congelados.
* **[Proyecto Piloto (`examples/sample-dashboard-ui/`)](examples/sample-dashboard-ui/):** Referencia completa en React + Vite + TypeScript + Tailwind CSS + TanStack Query + MSW + Vitest + Playwright validada sin advertencias con `fspec check`.
* **[Historial de Versiones (`CHANGELOG.md`)](CHANGELOG.md):** Registro SemVer 2.0.0 del framework (`v0.1.0` -> `v1.1.0`).
