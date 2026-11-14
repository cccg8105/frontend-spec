import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple

from frontend_spec.validator.schema_validator import (
    count_rolling_history_rows,
    extract_design_tokens_summary,
    extract_requirement_data,
    extract_user_flow_data,
    load_json_schema,
    parse_yaml_frontmatter,
    validate_against_schema,
)

FRONTEND_SOURCE_EXTENSIONS = {
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".mts",
    ".vue",
    ".svelte",
    ".astro",
    ".html",
    ".css",
    ".scss",
    ".sass",
    ".less",
}

NON_SOURCE_PREFIXES = (
    "docs/",
    ".spec/",
    "tests/",
    "test/",
    "e2e/",
    "playwright/",
    ".gemini/",
    ".cursor/",
    ".claude/",
    ".windsurf/",
    ".github/",
    "public/",
    "static/",
)

EXPECTED_TECHNICAL_DOCS: Tuple[Tuple[str, str, str], ...] = (
    ("component-hierarchy.md", "component-hierarchy", "technical/component-hierarchy.schema.json"),
    ("routing-and-rendering.md", "routing-and-rendering", "technical/routing-and-rendering.schema.json"),
    ("data-fetching-and-state.md", "data-fetching-and-state", "technical/data-fetching-and-state.schema.json"),
    ("tech-stack.md", "tech-stack", "technical/tech-stack.schema.json"),
    ("deployment-strategy.md", "deployment-strategy", "technical/deployment-strategy.schema.json"),
)

VALID_MERMAID_TYPES = (
    "flowchart",
    "sequenceDiagram",
    "classDiagram",
    "erDiagram",
    "stateDiagram",
    "graph",
    "gantt",
    "pie",
    "journey",
)


def _check_markdown_links(md_file: Path, errors: List[str]) -> None:
    content = md_file.read_text(encoding="utf-8")
    stripped = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    for label, raw_target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", stripped):
        target = raw_target.strip().split()[0]
        if not target or target.startswith(
            ("http://", "https://", "mailto:", "#", "file:", "conversation:", "sidecar:")
        ):
            continue
        clean_rel = target.split("#")[0]
        if not clean_rel or "[" in clean_rel or "{{" in clean_rel:
            continue
        resolved = (md_file.parent / clean_rel).resolve()
        if not resolved.exists():
            errors.append(
                f"Enlace roto en '{md_file.name}': [{label}]({raw_target}) -> no existe '{clean_rel}'"
            )


def _is_source_code_path(rel_posix: str) -> bool:
    if rel_posix.startswith(NON_SOURCE_PREFIXES):
        return False
    p = Path(rel_posix)
    if len(p.parts) == 1:
        return False
    return p.suffix.lower() in FRONTEND_SOURCE_EXTENSIONS


def _verify_staged_commits(
    project_root: Path,
    declared_artifacts: Set[str],
    has_active_reqs: bool,
    errors: List[str],
) -> None:
    try:
        res = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except Exception:
        return

    if res.returncode != 0:
        return

    staged_files = [
        line.strip().replace("\\", "/") for line in res.stdout.splitlines() if line.strip()
    ]
    if not staged_files:
        return

    staged_source = [f for f in staged_files if _is_source_code_path(f)]
    if not staged_source:
        return

    changelog_staged = "docs/backlog/changelog.md" in staged_files
    docs_staged = any(f.startswith("docs/") for f in staged_files)
    if changelog_staged:
        return

    if not has_active_reqs:
        errors.append(
            "Commit fantasma bloqueado: cambios en codigo frontend "
            f"({', '.join(staged_source[:5])}) sin ningun requerimiento activo en "
            "docs/backlog/pending.md ni cierre en changelog.md."
        )
        return

    undeclared = [f for f in staged_source if f not in declared_artifacts]
    if undeclared and not docs_staged:
        errors.append(
            "Violacion de fronteras (Commit fantasma parcial): los archivos en stage "
            f"({', '.join(undeclared[:5])}) no figuran en las 'Fronteras y Artefactos' de ningun "
            "REQ-UI-* activo en docs/backlog/pending.md."
        )


def _validate_functional_docs(
    docs_dir: Path, uf_schema: Dict, errors: List[str], warnings: List[str]
) -> None:
    func_dir = docs_dir / "functional"
    func_index = func_dir / "index.md"
    uf_dir = func_dir / "user-flows"

    if not func_index.exists():
        errors.append("Falta el archivo obligatorio docs/functional/index.md")
        return

    _check_markdown_links(func_index, errors)
    index_content = func_index.read_text(encoding="utf-8")

    uf_candidates: List[Path] = []
    if uf_dir.exists():
        for uf_file in sorted(uf_dir.glob("*.md")):
            if not uf_file.name.startswith("_"):
                uf_candidates.append(uf_file)
                if uf_file.name not in index_content:
                    warnings.append(
                        f"El flujo '{uf_file.name}' no esta catalogado en docs/functional/index.md (ejecuta 'frontend-spec sync')"
                    )

    for domain_dir in sorted(func_dir.iterdir()):
        if domain_dir.is_dir() and domain_dir.name != "user-flows":
            domain_index = domain_dir / "index.md"
            if not domain_index.exists():
                warnings.append(
                    f"Sub-dominio '{domain_dir.name}' sin sub-indice docs/functional/{domain_dir.name}/index.md"
                )
            else:
                _check_markdown_links(domain_index, errors)
                dom_content = domain_index.read_text(encoding="utf-8")
                for uf in sorted(domain_dir.rglob("*.md")):
                    if uf.name != "index.md" and not uf.name.startswith("_"):
                        uf_candidates.append(uf)
                        if uf.name not in dom_content:
                            warnings.append(
                                f"El flujo '{uf.name}' no figura en el sub-indice de {domain_dir.name}"
                            )

    for uf_path in uf_candidates:
        _check_markdown_links(uf_path, errors)
        uf_data, has_fm = extract_user_flow_data(uf_path.read_text(encoding="utf-8"))
        if not has_fm:
            warnings.append(f"Flujo '{uf_path.name}': falta cabecera YAML Frontmatter")
        if uf_schema:
            errors.extend(validate_against_schema(uf_data, uf_schema, path=uf_path.name))


def _validate_design_and_technical_docs(
    docs_dir: Path, errors: List[str], warnings: List[str]
) -> None:
    design_dir = docs_dir / "design"
    design_index = design_dir / "index.md"
    tokens_file = design_dir / "tokens-and-themes.md"
    tokens_schema = load_json_schema("design/tokens-and-themes.schema.json")

    if not design_index.exists():
        errors.append("Falta el archivo obligatorio docs/design/index.md")
    else:
        _check_markdown_links(design_index, errors)

    if not tokens_file.exists():
        errors.append("Falta el documento obligatorio docs/design/tokens-and-themes.md")
    else:
        _check_markdown_links(tokens_file, errors)
        tok_info = extract_design_tokens_summary(tokens_file.read_text(encoding="utf-8"))
        if not tok_info["has_fm"] or tok_info["artifact_type"] != "design-tokens":
            errors.append(
                "docs/design/tokens-and-themes.md debe declarar YAML Frontmatter con artifact_type: design-tokens"
            )
        if tokens_schema:
            props = tokens_schema.get("properties", {})
            if tok_info["theme_modes"] and "theme_modes" in props:
                errors.extend(
                    validate_against_schema(
                        tok_info["theme_modes"],
                        props["theme_modes"],
                        path="tokens-and-themes.md#theme_modes",
                    )
                )
            if tok_info["semantic_colors"] and "semantic_colors" in props:
                errors.extend(
                    validate_against_schema(
                        tok_info["semantic_colors"],
                        props["semantic_colors"],
                        path="tokens-and-themes.md#semantic_colors",
                    )
                )

    tech_dir = docs_dir / "technical"
    tech_index = tech_dir / "index.md"
    if not tech_index.exists():
        errors.append("Falta el archivo obligatorio docs/technical/index.md")
        return

    _check_markdown_links(tech_index, errors)
    tech_index_content = tech_index.read_text(encoding="utf-8")

    for filename, expected_art_type, schema_rel in EXPECTED_TECHNICAL_DOCS:
        tf_path = tech_dir / filename
        if not tf_path.exists():
            errors.append(f"Falta el documento tecnico obligatorio: docs/technical/{filename}")
            continue

        _check_markdown_links(tf_path, errors)
        fm, _, has_fm = parse_yaml_frontmatter(tf_path.read_text(encoding="utf-8"))
        if not has_fm or fm.get("artifact_type") != expected_art_type:
            warnings.append(
                f"Documento '{filename}': se recomienda frontmatter 'artifact_type: {expected_art_type}'"
            )

        schema = load_json_schema(schema_rel)
        if schema:
            props = schema.get("properties", {})
            for scalar_key in ("ecosystem", "default_rendering_mode", "mock_strategy", "hosting_model"):
                if scalar_key in fm and scalar_key in props and "{{" not in str(fm[scalar_key]):
                    errors.extend(
                        validate_against_schema(
                            fm[scalar_key], props[scalar_key], path=f"{filename}#{scalar_key}"
                        )
                    )

        if filename not in tech_index_content:
            warnings.append(f"El documento tecnico '{filename}' no figura en docs/technical/index.md")


def _validate_backlog(
    project_root: Path, docs_dir: Path, req_schema: Dict, errors: List[str]
) -> Tuple[Set[str], bool]:
    backlog_dir = docs_dir / "backlog"
    for name in ("index.md", "audit-proposals.md"):
        doc_p = backlog_dir / name
        if doc_p.exists():
            _check_markdown_links(doc_p, errors)

    pending_file = backlog_dir / "pending.md"
    declared_artifacts: Set[str] = set()
    has_active_reqs = False

    if not pending_file.exists():
        errors.append("Falta el archivo obligatorio docs/backlog/pending.md")
        return declared_artifacts, has_active_reqs

    content = pending_file.read_text(encoding="utf-8")
    raw_blocks = re.findall(
        r"(###\s*\[REQ-[^\]]+\].*?)(?=###\s*\[REQ-|\n##\s+Milestone|\Z)",
        content,
        re.DOTALL,
    )
    print(f"[INFO] Requerimientos activos analizados en backlog: {len(raw_blocks)}")
    has_active_reqs = len(raw_blocks) > 0

    for block in raw_blocks:
        req_data = extract_requirement_data(block)
        req_id = req_data["id"] or "REQ-UNKNOWN"

        if req_schema:
            errors.extend(validate_against_schema(req_data, req_schema, path=req_id))

        if not req_data["boundaries"]["artifacts"]:
            errors.append(
                f"{req_id}: debe declarar al menos un archivo en 'Fronteras y Artefactos'"
            )
        if not req_data["acceptance_criteria"]:
            errors.append(
                f"{req_id}: debe incluir al menos una casilla '- [ ]' en 'Criterios de Aceptacion'"
            )

        func_ref = req_data["references"]["functional"]
        is_patch = req_data["impact_type"] == "PATCH"
        if not func_ref:
            if not is_patch:
                errors.append(
                    f"{req_id}: todo requerimiento {req_data['impact_type']} debe declarar 'Referencia Funcional' (UF-*.md)"
                )
        elif func_ref.upper().startswith("N/A"):
            if not is_patch:
                errors.append(
                    f"{req_id}: solo requerimientos PATCH (Fast-Track) pueden omitir Referencia Funcional ('N/A')"
                )
        elif not (project_root / func_ref).exists():
            errors.append(
                f"{req_id}: la Referencia Funcional '{func_ref}' no existe en disco"
            )

        for t_ref in req_data["references"]["technical"]:
            if not t_ref.upper().startswith("N/A") and not (project_root / t_ref).exists():
                errors.append(
                    f"{req_id}: la Referencia Tecnica '{t_ref}' no existe en disco"
                )

        for art in req_data["boundaries"]["artifacts"]:
            norm_path = art["path"].replace("\\", "/").lstrip("./")
            declared_artifacts.add(norm_path)
            if art["action"] in ("MODIFY", "DELETE") and not (project_root / norm_path).exists():
                errors.append(
                    f"{req_id}: archivo '{norm_path}' marcado como [{art['action']}] no existe en disco"
                )

    return declared_artifacts, has_active_reqs


def _validate_spec_json_sidecars(
    project_root: Path, errors: List[str]
) -> None:
    specs_dir = project_root / ".spec" / "specs"
    if not specs_dir.is_dir():
        return
    schema_mapping = {
        "tokens-and-themes.json": "design/tokens-and-themes.schema.json",
        "component-hierarchy.json": "technical/component-hierarchy.schema.json",
        "routing-and-rendering.json": "technical/routing-and-rendering.schema.json",
        "data-fetching-and-state.json": "technical/data-fetching-and-state.schema.json",
        "tech-stack.json": "technical/tech-stack.schema.json",
        "deployment-strategy.json": "technical/deployment-strategy.schema.json",
    }
    for json_file in sorted(specs_dir.glob("*.json")):
        if json_file.name.startswith("user-flow"):
            schema_rel = "user-flow.schema.json"
        else:
            schema_rel = schema_mapping.get(json_file.name)
        if not schema_rel:
            errors.append(
                f".spec/specs/{json_file.name}: nombre de especificacion JSON no reconocido"
            )
            continue
        schema = load_json_schema(schema_rel)
        if not schema:
            continue
        try:
            payload = json.loads(json_file.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f".spec/specs/{json_file.name}: JSON invalido ({exc})")
            continue
        errors.extend(validate_against_schema(payload, schema, path=json_file.name))


def run_check(project_root: Path, check_staged: bool = False) -> bool:
    """Ejecuta auditoria integral de especificaciones, esquemas, enlaces y commits staged."""
    project_root = Path(project_root).resolve()
    docs_dir = project_root / "docs"
    print(f"\n[INFO] Ejecutando verificacion de integridad frontend-spec en: {docs_dir}")

    errors: List[str] = []
    warnings: List[str] = []

    if not docs_dir.exists():
        print("[ERROR] Directorio docs/ no encontrado. Ejecuta 'frontend-spec init'.")
        return False

    uf_schema = load_json_schema("user-flow.schema.json") or {}
    req_schema = load_json_schema("requirement.schema.json") or {}

    _validate_functional_docs(docs_dir, uf_schema, errors, warnings)
    _validate_design_and_technical_docs(docs_dir, errors, warnings)
    declared_artifacts, has_active_reqs = _validate_backlog(project_root, docs_dir, req_schema, errors)
    _validate_spec_json_sidecars(project_root, errors)

    for md_file in sorted(docs_dir.rglob("*.md")):
        md_text = md_file.read_text(encoding="utf-8")
        for block in re.findall(r"```mermaid\s*\r?\n(.*?)\r?\n```", md_text, re.DOTALL):
            first_line = block.strip().splitlines()[0].strip() if block.strip() else ""
            if not any(first_line.startswith(vt) for vt in VALID_MERMAID_TYPES):
                warnings.append(
                    f"Diagrama Mermaid sin encabezado estandar en {md_file.name}: '{first_line}'"
                )

        rev_rows = count_rolling_history_rows(md_text)
        if rev_rows > 3:
            warnings.append(
                f"Historial de Revisiones en '{md_file.relative_to(docs_dir).as_posix()}' tiene {rev_rows} filas (maximo Rolling Window: 3)"
            )

    if check_staged:
        _verify_staged_commits(project_root, declared_artifacts, has_active_reqs, errors)

    print("-" * 60)
    if warnings:
        print(f"[WARN] Advertencias encontradas ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("[OK] Cero advertencias de catalogo, Mermaid o Rolling Window.")

    if errors:
        print(f"\n[ERROR] Errores de integridad detectados ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        return False

    print("[OK] Todos los artefactos, enlaces y esquemas superaron la verificacion.")
    return True
