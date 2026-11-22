---
name: frontend-deploy
description: "Gobierna pipelines CI/CD frontend, GitHub Environments (preview/staging/production), variables públicas por ambiente (.env.example + vars.*), caché/CSP, despliegues CDN/SSR/PaaS y corte de releases/tags."
---

# frontend-deploy Skill

Activa esta skill bajo demanda cuando una tarea cree o modifique pipelines CI/CD (`.github/workflows/`), variables públicas de build, cabeceras de caché o CSP, configuración de despliegue CDN/SSR/PaaS o prepare un release/tag.

---

## 1. Modelo de Ramas y Promoción
- **Estándar por defecto:** `PR -> CI (+ Preview opcional)`, `main -> Staging (GitHub Env: staging)`, `tag vX.Y.Z -> Producción (GitHub Env: production)`.
- **Excepción PaaS (Vercel, Netlify, Cloudflare Pages):** Si el proyecto utiliza previews nativos y despliegue directo desde rama en PaaS, documenta explícitamente ese flujo en `docs/technical/deployment-strategy.md` en lugar de duplicar deploys.
- **Excepción Monorepo:** Configura filtros `paths:` para el paquete web y utiliza tags prefijados (`web-vX.Y.Z`) para aislar despliegues respecto a servicios backend.

---

## 2. Contrato de Variables Públicas por Ambiente
1. **Regla estricta de cero secretos en el cliente:**
   - Toda variable empaquetada en el frontend debe llevar prefijo público (`VITE_*`, `NEXT_PUBLIC_*`, `NUXT_PUBLIC_*`, `PUBLIC_*`) y configurarse como **GitHub Environment Variable** (`${{ vars.NOMBRE }}`), nunca con claves privadas API, secrets OAuth ni llaves de firma.
   - Usa **GitHub Environment Secrets** (`${{ secrets.NOMBRE }}`) únicamente para tokens de despliegue del proveedor CI (ej. Vercel/Cloudflare/AWS OIDC) consumidos en el runner.
   - **Prohibido** versionar archivos `.env.staging` o `.env.production` con credenciales en Git.
2. **Sincronización obligatoria de 3 puntos:** Toda nueva variable de build debe quedar registrada bajo un `REQ-UI-*` activo en:
   - `docs/technical/deployment-strategy.md` (prefijo, propósito, `var`, ambientes y origen).
   - `.env.example` en la raíz del proyecto (ejemplo no sensible).
   - `.github/workflows/*.yml` (inyección por ambiente con `vars.*`).

---

## 3. Auditoría Pre-Despliegue con GitHub CLI (`gh`)
Antes de cortar un despliegue hacia `staging` o `production`, audita los ambientes configurados en GitHub sin exponer secretos:

```bash
gh auth status
gh variable list --env staging
gh secret list --env staging
gh variable list --env production
gh secret list --env production
```

Si falta alguna variable pública declarada en `docs/technical/deployment-strategy.md` / `.env.example`, detén el release y notifícalo al usuario.

---

## 4. Generación de CI/CD Frontend a Medida (Día 0 y Evolución)
Durante `REQ-UI-CORE-001` (o al modificar infraestructura en `02d_plan_ui_guarantees_and_deploy`):
1. Genera `ci.yml` / `cd.yml` adaptados al perfil del stack (`docs/technical/tech-stack.md`) sin sobrescribir `frontend-spec-check.yml` si conserva `# FRONTEND-SPEC-CI-MANAGED`.
2. Incluye gates de calidad frontend: typecheck, lint, unit + `axe-core`, comprobación de presupuesto de bundle (`<= 200 KB` gzip inicial) y Playwright E2E con viewports.
3. Verifica políticas de producción: `Cache-Control` inmutable en assets con hash (`/assets/*`, `/_next/static/*`), `no-cache, must-revalidate` en `index.html`, cabeceras CSP/seguridad y rollback instantáneo ante `ChunkLoadError` o degradación de Web Vitals.

---

## 5. Checklist de Corte de Release
- **Integración continua a `main` (`Staging`):** Cierra el requerimiento sin subir versión de `package.json` mientras continúe el hito:
  `fspec resolve <REQ-UI-ID>`
- **Promoción a `Producción` (`tag vX.Y.Z`):**
  1. Verifica `fspec check` (y `--strict-tokens` si aplica), unit + `axe-core` y Playwright E2E en verde.
  2. Cierra el requerimiento final del hito subiendo versión: `fspec resolve <REQ-UI-ID> --bump`.
  3. Audita variables/secretos con `gh variable list --env production` y `gh secret list --env production`.
  4. Crea tag anotado sobre `main`: `git tag -a vX.Y.Z -m "Release vX.Y.Z"` y publica con `git push origin main --follow-tags`.
