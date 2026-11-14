import re
from pathlib import Path
from typing import Dict, Optional

from frontend_spec.commands.sync_index_cmd import run_sync_index
from frontend_spec.common import read_config_settings, slugify
from frontend_spec.detector.ecosystem_detector import build_profile_context


def _find_audit_proposal(project_root: Path, audit_id: str) -> Optional[Dict[str, str]]:
    audit_file = project_root / "docs" / "backlog" / "audit-proposals.md"
    if not audit_file.exists():
        return None
    content = audit_file.read_text(encoding="utf-8")
    clean_id = audit_id.strip("[]")
    pattern = rf"###\s*\[{re.escape(clean_id)}\]\s*([^\n\r]+)(.*?)(?=###\s*\[|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return None

    title = match.group(1).strip()
    body = match.group(2)

    m_dom = re.search(r"-\s*\*\*Dominio:\*\*\s*`?([a-zA-Z0-9_-]+)`?", body)
    m_imp = re.search(
        r"-\s*\*\*Impacto Estimado:\*\*\s*`?(MAJOR|MINOR|PATCH)`?", body, re.IGNORECASE
    )
    m_sev = re.search(r"-\s*\*\*Severidad Sugerida:\*\*\s*`?(P[123])`?", body, re.IGNORECASE)
    m_evid = re.search(r"-\s*\*\*Evidencia en Código:\*\*\s*`?([^`\n\r]+)`?", body)

    return {
        "id": clean_id,
        "title": title,
        "domain": m_dom.group(1).strip() if m_dom else "core",
        "impact": m_imp.group(1).strip().upper() if m_imp else "PATCH",
        "priority": m_sev.group(1).strip().upper() if m_sev else "P2",
        "evidence": m_evid.group(1).strip() if m_evid else "",
    }


def _mark_audit_promoted(project_root: Path, audit_id: str, req_id: str) -> bool:
    audit_file = project_root / "docs" / "backlog" / "audit-proposals.md"
    if not audit_file.exists():
        return False
    content = audit_file.read_text(encoding="utf-8")
    clean_id = audit_id.strip("[]")
    pattern = rf"(###\s*\[{re.escape(clean_id)}\][^\n\r]*\n.*?-\s*\*\*Estado:\*\*\s*)([^\n\r]+)"
    updated, count = re.subn(
        pattern, rf"\1Promovido a {req_id}", content, count=1, flags=re.DOTALL
    )
    if count > 0:
        audit_file.write_text(updated, encoding="utf-8")
        return True
    return False


def _resolve_component_artifact(
    src_dir: str, ecosystem: str, domain: str, slug: str, slug_pascal: str
) -> str:
    dom = domain.lower()
    if ecosystem == "angular":
        return f"{src_dir}/app/{dom}/{slug}/{slug}.component.ts"
    if ecosystem in ("vue-vite", "nuxt"):
        return f"{src_dir}/features/{dom}/{slug_pascal}.vue"
    if ecosystem == "sveltekit":
        return f"{src_dir}/lib/components/{dom}/{slug_pascal}.svelte"
    if ecosystem == "astro":
        return f"{src_dir}/components/{dom}/{slug_pascal}.astro"
    return f"{src_dir}/features/{dom}/{slug_pascal}.tsx"


def run_new_req(
    project_root: Path,
    title: Optional[str] = None,
    domain: str = "core",
    priority: str = "P2",
    impact: str = "MINOR",
    target_version: Optional[str] = None,
    uf_ref: Optional[str] = None,
    tokens: Optional[str] = None,
    fast_track: bool = False,
    from_audit: Optional[str] = None,
) -> Optional[str]:
    """Registra un requerimiento REQ-UI-* en docs/backlog/pending.md y sincroniza indices."""
    project_root = Path(project_root).resolve()
    pending_file = project_root / "docs" / "backlog" / "pending.md"
    changelog_file = project_root / "docs" / "backlog" / "changelog.md"

    if not pending_file.exists():
        print("[ERROR] docs/backlog/pending.md no encontrado. Ejecuta 'frontend-spec init' primero.")
        return None

    audit_info: Optional[Dict[str, str]] = None
    if from_audit:
        audit_info = _find_audit_proposal(project_root, from_audit)
        if not audit_info:
            print(f"[ERROR] Propuesta '{from_audit}' no encontrada en docs/backlog/audit-proposals.md.")
            return None
        title = title or audit_info["title"]
        domain = audit_info["domain"]
        impact = audit_info["impact"]
        priority = priority if priority != "P2" else audit_info["priority"]
        print(f"[INFO] Promoviendo [{audit_info['id']}]: '{title}' ({impact}, {priority})")
    elif not title:
        print("[ERROR] Debes indicar un titulo o usar --from-audit <ID>.")
        return None

    pending_content = pending_file.read_text(encoding="utf-8")
    changelog_content = changelog_file.read_text(encoding="utf-8") if changelog_file.exists() else ""

    domain_upper = re.sub(r"[^A-Z0-9]", "", domain.upper()) or "CORE"
    combined = pending_content + "\n" + changelog_content
    existing_ids = re.findall(rf"REQ-(?:UI-)?{domain_upper}-(\d+)", combined)
    next_num = max(int(i) for i in existing_ids) + 1 if existing_ids else 1
    req_id = f"REQ-UI-{domain_upper}-{next_num:03d}"

    cfg = read_config_settings(project_root)
    profile = build_profile_context(project_root, ecosystem_key=cfg["ecosystem"])

    if not target_version:
        v_match = re.search(r"##\s+Milestone\s+([^\s\n]+)", pending_content)
        target_version = v_match.group(1).strip() if v_match else cfg["current_milestone"]

    is_fast_track = fast_track or (impact.upper() == "PATCH")
    slug = slugify(title)
    slug_snake = slug.replace("-", "_")
    slug_pascal = "".join(p.capitalize() for p in slug.split("-"))

    src_artifact = _resolve_component_artifact(
        cfg["src_dir"], profile["ecosystem"], domain, slug, slug_pascal
    )
    test_artifact = (
        cfg["test_pattern"]
        .replace("{slug}", slug)
        .replace("{slug_snake}", slug_snake)
        .replace("{slug_pascal}", slug_pascal)
        .replace("{domain}", domain.lower())
    )

    if audit_info and audit_info.get("evidence"):
        clean_evid = audit_info["evidence"].split(":")[0].strip()
        if (project_root / clean_evid).exists():
            src_artifact = clean_evid

    action_src = "MODIFY" if (project_root / src_artifact).exists() else "NEW"
    token_line = tokens or "color-surface, color-primary, color-text-main"
    token_spans = ", ".join(
        f"`{t.strip('` ')}`" for t in token_line.split(",") if t.strip("` ")
    )

    if is_fast_track:
        resolved_uf = uf_ref or "N/A (PATCH / Fast-Track)"
        req_block = f"""
### [{req_id}] {title}
- **Prioridad:** {priority}
- **Tipo:** Hotfix / Fix (PATCH - Fast-Track)
- **Versión Objetivo:** `{target_version}`
- **Referencia Funcional:** `{resolved_uf}`
- **Referencia Técnica:** `docs/design/tokens-and-themes.md`, `docs/technical/component-hierarchy.md`
- **Tokens Consumidos:** {token_spans}

#### Fronteras y Artefactos:
- **Artefactos a Modificar / Crear:**
  - `{src_artifact}` [{action_src}]
  - `{test_artifact}` [NEW]
- **Restricciones:**
  - Carril Fast-Track (`PATCH`): prohibido romper rutas, props publicas, contratos RFC 7807 o quemar valores CSS fuera de tokens.

#### Criterios de Aceptación:
- [ ] Reproducir el defecto con `/diagnose` mediante test automatizado de regresion en rojo antes del fix.
- [ ] Aplicar correccion minima verificando tests unitarios + `axe-core` al 100%.
"""
    else:
        resolved_uf = uf_ref or f"docs/functional/user-flows/UF-{domain_upper}-{next_num:03d}-{slug}.md"
        req_block = f"""
### [{req_id}] {title}
- **Prioridad:** {priority}
- **Tipo:** Feature ({impact.upper()})
- **Versión Objetivo:** `{target_version}`
- **Referencia Funcional:** `{resolved_uf}`
- **Referencia Técnica:** `docs/design/tokens-and-themes.md`, `docs/technical/component-hierarchy.md`, `docs/technical/routing-and-rendering.md`
- **Tokens Consumidos:** {token_spans}

#### Fronteras y Artefactos:
- **Artefactos a Modificar / Crear:**
  - `{src_artifact}` [{action_src}]
  - `{test_artifact}` [NEW]
- **Restricciones:**
  - Cumplir directivas Anti-AI Slop, simetria claro/oscuro, FSM e invariantes verificables y cero secretos en cliente.

#### Criterios de Aceptación:
- [ ] Implementar flujo UX y estados borde (`Loading`, `Empty`, `Error` RFC 7807) consumiendo solo semantic design tokens.
- [ ] Pruebas unitarias (`axe-core`) y E2E Playwright en viewports pasando al 100%.
"""

    pending_file.write_text(pending_content.rstrip() + "\n" + req_block, encoding="utf-8")

    if from_audit and _mark_audit_promoted(project_root, from_audit, req_id):
        print(f"[OK] Estado actualizado en audit-proposals.md: Promovido a {req_id}")

    run_sync_index(project_root)
    print(f"[OK] Requerimiento creado: {req_id} en docs/backlog/pending.md")
    if not is_fast_track:
        print(f"[INFO] Crea/actualiza '{resolved_uf}' antes de ejecutar 'frontend-spec check'.")
    return req_id
