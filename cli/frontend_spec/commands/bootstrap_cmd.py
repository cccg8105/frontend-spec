import datetime
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from frontend_spec.commands.sync_index_cmd import _replace_sync_section, run_sync_index
from frontend_spec.common import build_doc_context, read_config_settings, render_placeholders
from frontend_spec.detector.ecosystem_detector import build_profile_context, detect_frontend_ecosystem
from frontend_spec.detector.version_extractor import extract_version
from frontend_spec.validator.schema_validator import locate_framework_asset

SKIP_DIRS = {
    ".git",
    ".spec",
    "docs",
    "node_modules",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".astro",
    ".angular",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    "storybook-static",
    "coverage",
    "playwright-report",
    "test-results",
    "graphify-out",
    ".gemini",
    ".cursor",
    ".claude",
    ".windsurf",
}

UI_COMPONENT_EXTS = {".tsx", ".jsx", ".vue", ".svelte", ".astro"}
GENERIC_UI_FOLDERS = {
    "components",
    "atoms",
    "molecules",
    "organisms",
    "layouts",
    "templates",
    "pages",
    "routes",
    "app",
    "src",
    "views",
    "features",
    "modules",
    "common",
    "shared",
    "utils",
    "helpers",
    "hooks",
    "composables",
    "stores",
    "store",
    "services",
    "styles",
    "assets",
    "types",
    "lib",
    "config",
    "core",
    "api",
    "ui",
    "__tests__",
    "__mocks__",
}


def _scan_frontend_inventory(project_root: Path) -> Dict[str, List[str]]:
    routes_and_pages: List[str] = []
    components: List[str] = []
    styles_and_tokens: List[str] = []
    state_and_mocks: List[str] = []
    unit_tests: List[str] = []
    e2e_tests: List[str] = []
    candidate_domains: Set[str] = set()

    for path in sorted(project_root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts) or not path.is_file():
            continue

        rel = path.relative_to(project_root).as_posix()
        low_rel = rel.lower()
        low_name = path.name.lower()
        is_test = bool(re.search(r"\.(test|spec)\.[a-z]+$", low_name))

        if is_test or low_rel.startswith(("tests/", "test/")):
            unit_tests.append(rel)
            continue

        if low_rel.startswith(("e2e/", "playwright/", "cypress/")):
            e2e_tests.append(rel)
            continue

        if re.search(r"\.stories\.(tsx|ts|jsx|js|mdx)$", low_name):
            continue

        if (
            any(seg in path.parts for seg in ("pages", "routes"))
            or any(k in low_name for k in ("+page.", "page.", "layout.", "router.", "routes.", "routing."))
        ) and path.suffix.lower() in (UI_COMPONENT_EXTS | {".ts", ".js", ".mdx"}):
            routes_and_pages.append(rel)

        if path.suffix.lower() in UI_COMPONENT_EXTS or low_name.endswith(".component.ts"):
            components.append(rel)

        if (
            path.suffix.lower() in (".css", ".scss", ".sass", ".less")
            or low_name == "components.json"
            or low_name.startswith("tailwind.config.")
            or "token" in low_name
            or "theme" in low_name
        ):
            styles_and_tokens.append(rel)

        if any(k in low_rel for k in ("msw", "handlers", "mock", "store", "query", "hooks/", "composables/")):
            state_and_mocks.append(rel)

        parts = Path(rel).parts
        if len(parts) >= 3 and parts[0] in ("src", "app", "pages", "routes", "features", "modules"):
            for seg in parts[1:-1]:
                clean_seg = re.sub(r"[^a-z0-9_-]", "", seg.lower())
                if clean_seg and clean_seg not in GENERIC_UI_FOLDERS and len(clean_seg) >= 3:
                    candidate_domains.add(clean_seg)

    return {
        "routes_and_pages": routes_and_pages[:30],
        "components": components[:40],
        "styles_and_tokens": styles_and_tokens[:25],
        "state_and_mocks": state_and_mocks[:25],
        "unit_tests": unit_tests,
        "e2e_tests": e2e_tests,
        "domains": sorted(candidate_domains)[:12] or ["core"],
    }


def _scan_legacy_docs(project_root: Path) -> List[Dict[str, str]]:
    legacy_docs: List[Dict[str, str]] = []
    latest_src_mtime = 0.0

    for path in project_root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts) or not path.is_file():
            continue
        if path.suffix.lower() in (UI_COMPONENT_EXTS | {".ts", ".js", ".css", ".scss"}):
            try:
                latest_src_mtime = max(latest_src_mtime, path.stat().st_mtime)
            except Exception:
                pass

    for path in project_root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts) or not path.is_file():
            continue
        rel = path.relative_to(project_root).as_posix()
        low_name = path.name.lower()
        if rel.startswith("docs/"):
            continue
        if low_name in ("readme.md", "architecture.md", "design.md", "storybook.md") or "storybook" in low_name:
            try:
                drift = (
                    "Posible desfase (anterior a cambios de UI)"
                    if latest_src_mtime > 0 and (latest_src_mtime - path.stat().st_mtime) > 86400 * 7
                    else "Reciente / Coincidente"
                )
            except Exception:
                drift = "No determinado"
            legacy_docs.append({"path": rel, "drift": drift})

    return legacy_docs[:15]


def _scan_stories(project_root: Path) -> List[str]:
    """Inventaria archivos de historias Storybook (*.stories.*)."""
    stories: List[str] = []
    for path in sorted(project_root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts) or not path.is_file():
            continue
        if re.search(r"\.stories\.(tsx|ts|jsx|js|mdx)$", path.name.lower()):
            stories.append(path.relative_to(project_root).as_posix())
    return stories


def _read_graphify_summary(project_root: Path) -> List[str]:
    graph_json = project_root / "graphify-out" / "graph.json"
    if not graph_json.exists():
        return []
    try:
        payload = json.loads(graph_json.read_text(encoding="utf-8"))
        nodes = payload.get("nodes", [])
        links = payload.get("links") or payload.get("edges") or []
        degree: Dict[str, int] = {}
        labels: Dict[str, str] = {}
        for n in nodes:
            nid = str(n.get("id", ""))
            labels[nid] = str(n.get("label") or n.get("name") or nid)
            degree[nid] = 0
        for edge in links:
            src = str(edge.get("source", ""))
            tgt = str(edge.get("target", ""))
            degree[src] = degree.get(src, 0) + 1
            degree[tgt] = degree.get(tgt, 0) + 1
        top = sorted(degree.items(), key=lambda kv: kv[1], reverse=True)[:8]
        return [f"`{labels.get(nid, nid)}` ({deg} conexiones)" for nid, deg in top if deg > 0]
    except Exception:
        return []


def _extract_previous_checkbox_state(report_path: Path) -> Tuple[Dict[str, bool], str]:
    state: Dict[str, bool] = {}
    mode = "progressive"
    if not report_path.exists():
        return state, mode
    try:
        text = report_path.read_text(encoding="utf-8")
        m_mode = re.search(r"onboarding_mode:\s*([a-zA-Z0-9_-]+)", text)
        if m_mode:
            mode = m_mode.group(1).strip()
        for line in text.splitlines():
            m_cb = re.search(r"-\s*\[([ xX])\]\s*(.+)", line)
            if m_cb:
                state[m_cb.group(2).strip()] = m_cb.group(1).lower() == "x"
    except Exception:
        pass
    return state, mode


def _update_tech_stack_sync(
    docs_dir: Path, profile: Dict[str, Any], version: str
) -> None:
    tech_stack_file = docs_dir / "technical" / "tech-stack.md"
    if not tech_stack_file.exists():
        return
    storybook_row = (
        "\n| **Catálogo Visual** | `Storybook` (`@storybook/*`) | Historias CSF 3.0 + `@storybook/addon-a11y` |"
        if profile.get("has_storybook")
        else ""
    )
    table_block = (
        "| Capa | Tecnología Activa | Notas de Configuración |\n"
        "| :--- | :--- | :--- |\n"
        f"| **Ecosistema / Meta-Framework** | `{profile['runtime_label']}` (`{profile['ecosystem']}`) | Manifiesto `{profile['version_file']}` (`v{version}`) |\n"
        f"| **Lenguaje** | `{profile['language']}` | Tipado estricto en Props, contratos API y Stores |\n"
        f"| **Estilos y Primitivas** | `{profile['styling']}` + `{profile['ui_primitives']}` | Consumo estricto de `docs/design/tokens-and-themes.md` |\n"
        f"| **Estado Remoto y Mocks** | `{profile['state_server']}` + MSW | Caché declarativa y contratos HTTP simulados |\n"
        f"| **Testing y a11y** | `{profile['unit_test_runner']}` + `{profile['testing_library']}` + `axe-core` + `{profile['e2e_runner']}` | Cobertura unitaria, WCAG 2.1 AA y E2E responsive |{storybook_row}"
    )
    updated = _replace_sync_section(
        tech_stack_file.read_text(encoding="utf-8"),
        "TECH_STACK",
        r"##\s*(?:1\.\s*)?Núcleo Tecnológico[^\n]*",
        table_block,
    )
    tech_stack_file.write_text(updated, encoding="utf-8")


def _update_config_domains(spec_dir: Path, domains: List[str]) -> None:
    cfg_path = spec_dir / "config.yaml"
    if not cfg_path.exists() or not domains:
        return
    raw = cfg_path.read_text(encoding="utf-8")
    dom_block = "domains:\n" + "\n".join(f"  - {d}" for d in domains)
    if re.search(r"^domains:\s*\r?\n(?:\s+-\s+.+\r?\n?)*", raw, re.MULTILINE):
        updated = re.sub(
            r"^domains:\s*\r?\n(?:\s+-\s+.+\r?\n?)*",
            dom_block + "\n",
            raw,
            count=1,
            flags=re.MULTILINE,
        )
        cfg_path.write_text(updated, encoding="utf-8")


def run_bootstrap(
    project_root: Path,
    mode: str = "auto",
    reset: bool = False,
) -> Path:
    """Escanea un repo frontend existente (Brownfield), pre-puebla tech-stack y .spec/bootstrap-report.md."""
    project_root = Path(project_root).resolve()
    spec_dir = project_root / ".spec"
    docs_dir = project_root / "docs"

    if not docs_dir.exists() or not spec_dir.exists():
        raise RuntimeError(
            "El proyecto aun no tiene estructura frontend-spec. Ejecuta 'frontend-spec init' primero."
        )

    print(f"\n[INFO] Ejecutando Brownfield Bootstrap Frontend en: {project_root}")

    detection = detect_frontend_ecosystem(project_root)
    profile = detection.get("detected") or build_profile_context(project_root)
    ver_path = detection.get("version_path")
    detected_ver = (
        extract_version(ver_path, profile["format"]) if ver_path else None
    ) or "0.1.0"

    inventory = _scan_frontend_inventory(project_root)
    stories = _scan_stories(project_root)
    legacy_docs = _scan_legacy_docs(project_root)
    god_nodes = _read_graphify_summary(project_root)
    today = datetime.date.today().isoformat()

    total_tests = len(inventory["unit_tests"]) + len(inventory["e2e_tests"])
    route_count = len(inventory["routes_and_pages"])
    if total_tests == 0:
        test_baseline = "none (0 tests unitarios/E2E detectados: priorizar caracterizacion + axe)"
    elif len(inventory["e2e_tests"]) > 0 or total_tests >= max(2, route_count):
        test_baseline = f"solid ({len(inventory['unit_tests'])} unit, {len(inventory['e2e_tests'])} E2E)"
    else:
        test_baseline = f"partial ({len(inventory['unit_tests'])} unit, {len(inventory['e2e_tests'])} E2E)"

    report_path = spec_dir / "bootstrap-report.md"
    prev_state, prev_mode = ({}, "progressive") if reset else _extract_previous_checkbox_state(report_path)
    resolved_mode = (
        ("progressive" if len(inventory["routes_and_pages"]) > 4 or len(inventory["components"]) > 10 else "full")
        if mode == "auto"
        else mode
    )
    if mode == "auto" and prev_state and not reset:
        resolved_mode = prev_mode

    def cb(label: str, auto_checked: bool = False) -> str:
        checked = prev_state.get(label, auto_checked)
        return f"- [{'x' if checked else ' '}] {label}"

    _update_tech_stack_sync(docs_dir, profile, detected_ver)
    _update_config_domains(spec_dir, inventory["domains"])

    audit_file = docs_dir / "backlog" / "audit-proposals.md"
    if not audit_file.exists():
        templates_root = locate_framework_asset("templates")
        audit_src = templates_root / ".spec" / "docs" / "backlog" / "audit-proposals.md" if templates_root else None
        if audit_src and audit_src.exists():
            cfg = read_config_settings(project_root)
            ctx = build_doc_context(
                project_root.name,
                profile,
                detected_ver,
                cfg["current_milestone"],
                cfg["versioning_scheme"],
                today,
            )
            audit_file.parent.mkdir(parents=True, exist_ok=True)
            audit_file.write_text(
                render_placeholders(audit_src.read_text(encoding="utf-8"), ctx),
                encoding="utf-8",
            )

    domains_md = ", ".join(f"`{d}`" for d in inventory["domains"])
    routes_md = "\n".join(f"- `{p}`" for p in inventory["routes_and_pages"]) or "- *(Sin rutas/paginas detectadas automaticamente)*"
    comps_md = "\n".join(f"- `{c}`" for c in inventory["components"][:15]) or "- *(Sin componentes detectados automaticamente)*"
    styles_md = "\n".join(f"- `{s}`" for s in inventory["styles_and_tokens"][:15]) or "- *(Sin archivos CSS/tokens detectados)*"
    god_md = "\n".join(f"- {g}" for g in god_nodes) or "- *(Sin grafo Graphify detectado: recomienda ejecutar `graphify` respetando `.graphifyignore`)*"
    legacy_md = "\n".join(f"- `{d['path']}` — {d['drift']}" for d in legacy_docs) or "- *(Sin documentacion previa conflictiva detectada)*"

    has_storybook = bool(profile.get("has_storybook")) or bool(stories)
    storybook_meta = (
        f"\n- **Storybook:** Detectado ({len(stories)} archivos `*.stories.*`)"
        if has_storybook
        else ""
    )
    if has_storybook:
        stories_lines = "\n".join(f"- `{s}`" for s in stories[:25]) or (
            "- *(Dependencia `@storybook/*` o `.storybook/` detectada sin archivos `*.stories.*` creados aun)*"
        )
        storybook_section = f"\n\n### Catalogo Visual Storybook ({len(stories)})\n{stories_lines}"
    else:
        storybook_section = ""

    report_md = f"""---
artifact_type: bootstrap-report
onboarding_mode: {resolved_mode}
ecosystem: {profile['ecosystem']}
test_baseline: "{test_baseline}"
generated_at: "{today}"
---

# Reporte de Adopcion Brownfield Frontend — {project_root.name}

- **Modo Seleccionado:** `{resolved_mode}`
- **Stack Detectado:** `{profile['runtime_label']}` (`{profile['language']}`, `{profile['styling']}`, `{profile['ui_primitives']}`)
- **Estado / Mocks:** `{profile['state_server']}` | **Tests:** `{profile['unit_test_runner']}` / `{profile['e2e_runner']}`{storybook_meta}
- **Linea Base de Pruebas:** `{test_baseline}`
- **Dominios UI Sugeridos:** {domains_md}

---

## Checklist GPS de Ingenieria Inversa Frontend

### Fase 1: Linea Base e Infraestructura
{cb("Validar docs/technical/tech-stack.md y .spec/config.yaml con el ecosistema real", True)}
{cb("Revisar package.json, variables publicas y pipeline CI en deployment-strategy.md")}

### Fase 2: Extraccion Tecnica e Identidad Visual (El Codigo Manda)
{cb("Documentar paleta real claro/oscuro, tipografias y Tailwind/CSS en docs/design/tokens-and-themes.md")}
{cb("Inventariar rutas activas, layouts y guardias RBAC en docs/technical/routing-and-rendering.md")}
{cb("Catalogar componentes clave (CMP-*) y jerarquia atomica en docs/technical/component-hierarchy.md")}
{cb("Mapear estado remoto, manejo RFC 7807 y mocks MSW en docs/technical/data-fetching-and-state.md")}

### Fase 3: Flujos UX (UF-*)
{cb("Documentar flujos criticos iniciales en docs/functional/user-flows/UF-*.md")}
{cb("Verificar modulos legados pendientes (Just-In-Time) en docs/functional/index.md")}

### Fase 4: Triage de Deuda Visual, a11y y Cierre
{cb("Registrar hex quemados, fallos WCAG o riesgos XSS como AUDIT-UI-* en docs/backlog/audit-proposals.md")}

---

## Inventario Tecnico Detectado

### Rutas y Paginas ({len(inventory['routes_and_pages'])})
{routes_md}

### Muestra de Componentes UI ({len(inventory['components'])})
{comps_md}

### Hojas de Estilo, Tailwind y Tokens ({len(inventory['styles_and_tokens'])})
{styles_md}

### Documentacion Previa / Posible Doc Drift
{legacy_md}

### Graphify God Nodes
{god_md}{storybook_section}
"""
    report_path.write_text(report_md, encoding="utf-8")
    run_sync_index(project_root)

    print(f"[OK] Reporte Brownfield generado: {report_path.relative_to(project_root).as_posix()}")
    print(f"[OK] Tech stack actualizado en docs/technical/tech-stack.md ({profile['runtime_label']})")
    return report_path
