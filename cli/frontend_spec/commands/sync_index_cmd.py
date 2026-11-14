import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

from frontend_spec.validator.schema_validator import (
    export_w3c_design_tokens,
    extract_design_tokens_summary,
    extract_requirement_data,
    extract_user_flow_data,
)


def _replace_sync_section(
    doc_text: str, marker: str, fallback_heading_regex: str, new_block: str
) -> str:
    start_tag = f"<!-- SYNC:{marker}:START -->"
    end_tag = f"<!-- SYNC:{marker}:END -->"

    if start_tag in doc_text and end_tag in doc_text:
        pattern = re.compile(rf"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
        replacement = f"{start_tag}\n{new_block.strip()}\n{end_tag}"
        return pattern.sub(lambda _: replacement, doc_text, count=1)

    heading_match = re.search(fallback_heading_regex, doc_text)
    if heading_match:
        insert_start = heading_match.end()
        next_sec = re.search(r"\n---\s*\n|\n##\s+", doc_text[insert_start:])
        if next_sec:
            end_pos = insert_start + next_sec.start()
            return (
                doc_text[:insert_start]
                + f"\n\n{start_tag}\n{new_block.strip()}\n{end_tag}\n"
                + doc_text[end_pos:]
            )
        return doc_text[:insert_start].rstrip() + f"\n\n{start_tag}\n{new_block.strip()}\n{end_tag}\n"

    return doc_text.rstrip() + f"\n\n{start_tag}\n{new_block.strip()}\n{end_tag}\n"


def _discover_user_flow_files(func_dir: Path) -> List[Path]:
    files: List[Path] = []
    flat_dir = func_dir / "user-flows"
    if flat_dir.exists():
        for md in sorted(flat_dir.glob("*.md")):
            if not md.name.startswith("_") and md.name != "index.md":
                files.append(md)

    for sub in sorted(func_dir.iterdir()):
        if sub.is_dir() and sub.name != "user-flows":
            for md in sorted(sub.rglob("*.md")):
                if not md.name.startswith("_") and md.name != "index.md":
                    files.append(md)
    return files


def _read_detected_domains(project_root: Path) -> List[str]:
    report_file = project_root / ".spec" / "bootstrap-report.md"
    config_file = project_root / ".spec" / "config.yaml"
    domains: Set[str] = set()

    if report_file.exists():
        try:
            text = report_file.read_text(encoding="utf-8")
            m = re.search(r"-\s*\*\*Dominios(?:\s+UI)?\s+Sugeridos:\*\*\s*(.+)", text)
            if m:
                domains.update(re.findall(r"`([a-zA-Z0-9_-]+)`", m.group(1)))
        except Exception:
            pass

    if not domains and config_file.exists():
        try:
            cfg_text = config_file.read_text(encoding="utf-8")
            sec_m = re.search(r"^domains:\s*\r?\n((?:\s+-\s+.+\r?\n?)*)", cfg_text, re.MULTILINE)
            if sec_m:
                for item in re.findall(r"^\s+-\s+([a-zA-Z0-9_-]+)", sec_m.group(1), re.MULTILINE):
                    domains.add(item.strip())
        except Exception:
            pass

    return sorted(domains)


def _sync_backlog_index(docs_dir: Path) -> int:
    pending_file = docs_dir / "backlog" / "pending.md"
    backlog_index = docs_dir / "backlog" / "index.md"
    if not (pending_file.exists() and backlog_index.exists()):
        return 0

    pending_content = pending_file.read_text(encoding="utf-8")
    req_blocks = re.findall(
        r"(###\s*\[REQ-[A-Z0-9-]+\].*?)(?=###\s*\[REQ-|\n##\s+Milestone|\Z)",
        pending_content,
        re.DOTALL,
    )

    rows: List[str] = []
    for raw_block in req_blocks:
        req_data = extract_requirement_data(raw_block)
        req_id = req_data["id"]
        if not req_id:
            continue
        criteria = req_data["acceptance_criteria"]
        if criteria and all(c["completed"] for c in criteria):
            status = "Completado"
        elif any(c["completed"] for c in criteria):
            status = "En Progreso"
        else:
            status = "Pendiente"

        func_ref = req_data["references"]["functional"] or "N/A"
        tech_refs = ", ".join(f"`{t}`" for t in req_data["references"]["technical"]) or "N/A"
        func_disp = f"`{func_ref}`" if not func_ref.startswith("`") else func_ref
        rows.append(
            f"| `{req_id}` | {req_data['title']} | `{req_data['impact_type'] or 'MINOR'}` | "
            f"`{req_data['priority'] or 'P2'}` | {status} | {func_disp} | {tech_refs} |"
        )

    if rows:
        table_md = (
            "| ID Requerimiento | Título | Impacto | Prioridad | Estado | Ref. Funcional | Ref. Técnica |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            + "\n".join(rows)
        )
    else:
        table_md = "_Sin requerimientos pendientes en el milestone actual._"

    updated = _replace_sync_section(
        backlog_index.read_text(encoding="utf-8"),
        "BACKLOG_TABLE",
        r"##\s*Resumen del Milestone Activo[^\n]*",
        table_md,
    )
    backlog_index.write_text(updated, encoding="utf-8")
    return len(rows)


def _sync_functional_index(project_root: Path, docs_dir: Path) -> Tuple[int, Set[str]]:
    func_dir = docs_dir / "functional"
    func_index = func_dir / "index.md"
    if not func_index.exists():
        return 0, set()

    uf_files = _discover_user_flow_files(func_dir)
    uf_rows: List[str] = []
    documented_domains: Set[str] = set()

    for uf_path in uf_files:
        uf_data, _ = extract_user_flow_data(uf_path.read_text(encoding="utf-8"))
        uf_id = uf_data.get("id") or uf_path.stem
        title = uf_data.get("title") or uf_path.stem
        domain = (uf_data.get("domain") or "core").lower()
        route = uf_data.get("route") or "/"
        status = uf_data.get("status") or "Activo"
        fsm_flag = "Si" if uf_data.get("fsm_required") else "No"
        documented_domains.add(domain)

        rel_link = uf_path.relative_to(func_dir).as_posix()
        uf_rows.append(
            f"| `{uf_id}` | {title} | `{route}` | `{domain}` | {fsm_flag} | {status} | [{uf_path.name}](./{rel_link}) |"
        )

    if uf_rows:
        uf_block = (
            "| ID Flujo | Título | Ruta | Dominio | FSM | Estado | Documento |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            + "\n".join(uf_rows)
        )
    else:
        uf_block = "_Aún no hay flujos de usuario registrados. Se agregarán al formalizar requerimientos `MAJOR` o `MINOR` en `docs/functional/user-flows/`._"

    updated_func = _replace_sync_section(
        func_index.read_text(encoding="utf-8"),
        "USER_FLOWS_CATALOG",
        r"##\s*Catálogo de Flujos de Usuario[^\n]*",
        uf_block,
    )

    candidate_domains = _read_detected_domains(project_root)
    pending_domains = [
        d for d in candidate_domains if d != "core" and d.lower() not in documented_domains
    ]
    if pending_domains:
        pending_rows = "\n".join(
            f"| `{d}` | Pendiente As-Is | Ejecutar `/ui-bootstrap` o documentar `UF-{d.upper()}-001` al tocar el modulo |"
            for d in pending_domains
        )
        pending_block = (
            "| Dominio / Ruta Legada | Estado | Accion Recomendada (Just-In-Time) |\n"
            "| :--- | :--- | :--- |\n"
            + pending_rows
        )
    else:
        pending_block = "_Sin rutas o módulos UI legados pendientes de levantamiento._"

    updated_func = _replace_sync_section(
        updated_func,
        "PENDING_DOMAINS",
        r"##\s*Módulos / Rutas Legadas Detectadas[^\n]*",
        pending_block,
    )
    func_index.write_text(updated_func, encoding="utf-8")
    return len(uf_rows), documented_domains


def _sync_design_index(docs_dir: Path) -> None:
    design_dir = docs_dir / "design"
    design_index = design_dir / "index.md"
    tokens_file = design_dir / "tokens-and-themes.md"
    if not (design_index.exists() and tokens_file.exists()):
        return

    summary = extract_design_tokens_summary(tokens_file.read_text(encoding="utf-8"))
    modes = ", ".join(f"`{m}`" for m in summary["theme_modes"]) or "`light`, `dark`"
    color_count = len(summary["semantic_colors"])
    disp = summary["display_font"] or "Sin especificar"
    mono = summary["mono_font"] or "Sin especificar"

    summary_block = (
        f"- **Modos activos:** {modes} ({color_count} tokens cromáticos semánticos).\n"
        f"- **Tipografías:** {disp} (display/UI) y {mono} (monoespacio).\n"
        "- **Regla estricta:** Prohibido quemar colores hex, tamaños arbitrarios o `z-index` fuera del catálogo semántico en [`tokens-and-themes.md`](./tokens-and-themes.md)."
    )
    updated = _replace_sync_section(
        design_index.read_text(encoding="utf-8"),
        "DESIGN_TOKENS_SUMMARY",
        r"##\s*Resumen de Tokens Activos[^\n]*",
        summary_block,
    )
    design_index.write_text(updated, encoding="utf-8")


def _export_w3c_tokens_file(project_root: Path, docs_dir: Path) -> bool:
    tokens_md = docs_dir / "design" / "tokens-and-themes.md"
    if not tokens_md.exists():
        print("[WARN] No se encontro docs/design/tokens-and-themes.md para exportar tokens W3C.")
        return False

    payload = export_w3c_design_tokens(tokens_md.read_text(encoding="utf-8"))
    out_file = project_root / ".spec" / "specs" / "design.tokens.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    color_count = len(payload.get("color", {}))
    print(f"[OK] Design tokens W3C DTCG exportados en .spec/specs/design.tokens.json ({color_count} colores)")
    return True


def run_sync_index(project_root: Path, export_tokens: bool = False) -> Tuple[int, int]:
    """Sincroniza en disco docs/backlog/index.md, docs/functional/index.md y docs/design/index.md."""
    project_root = Path(project_root).resolve()
    docs_dir = project_root / "docs"
    if not docs_dir.exists():
        print("[ERROR] Directorio docs/ no encontrado.")
        return 0, 0

    print("\n[INFO] Sincronizando catalogos index.md en disco...")
    synced_reqs = _sync_backlog_index(docs_dir)
    synced_ufs, _ = _sync_functional_index(project_root, docs_dir)
    _sync_design_index(docs_dir)

    if export_tokens:
        _export_w3c_tokens_file(project_root, docs_dir)

    print(
        f"[OK] Indices sincronizados: {synced_reqs} req(s) en backlog/index.md y "
        f"{synced_ufs} flujo(s) en functional/index.md."
    )
    return synced_reqs, synced_ufs
