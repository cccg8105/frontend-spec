# Comando: 02d_plan_ui_guarantees_and_deploy

> **Propósito:** Auditar requisitos no funcionales frontend (Web Vitals, seguridad XSS/CSP, i18n, telemetría) y estrategia de build/despliegue (Etapa 2D).

## Instrucciones para el Agente:
1. Consulta `docs/technical/tech-stack.md` y `.spec/templates/_template_tech_stack.md`:
   - Evalúa impacto en presupuestos **Core Web Vitals** (`LCP <= 2.5s`, `INP <= 200ms`, `CLS <= 0.1`) y tamaño de bundle JS inicial (`<= 200 KB` gzip / lazy loading para librerías pesadas).
   - Verifica prevención XSS (sin HTML sin sanitizar ni esquemas URL inseguros), almacenamiento seguro de sesión y reglas i18n.
2. Consulta `docs/technical/deployment-strategy.md` y `.spec/templates/_template_deployment.md`:
   - Si introduce nuevas variables de entorno cliente, regístralas con su prefijo público explícito (`VITE_*`, `NEXT_PUBLIC_*`, `NUXT_PUBLIC_*`, `PUBLIC_*`) confirmando que no contienen secretos.
   - Verifica cambios en directivas CSP (`connect-src`, `img-src`, `script-src`), cabeceras de caché o checkpoints del pipeline CI/CD (Unit + `axe` + Playwright E2E).
3. Actualiza `Historial de Revisiones` manteniendo máximo 3 filas.
