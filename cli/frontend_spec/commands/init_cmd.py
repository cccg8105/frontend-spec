import datetime
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from frontend_spec import __version__
from frontend_spec.commands.update_cmd import (
    install_or_update_harness,
    update_github_ci_workflow,
    update_pre_commit_hook,
)
from frontend_spec.common import HARNESS_NAMES, SCHEME_LABELS, build_doc_context, render_placeholders
from frontend_spec.detector.ecosystem_detector import (
    ECOSYSTEM_PROFILES,
    build_profile_context,
    detect_frontend_ecosystem,
)
from frontend_spec.detector.version_extractor import compute_next_milestone, extract_version
from frontend_spec.validator.schema_validator import locate_framework_asset


def _prompt_interactive_options(
    detection: Dict,
    profile: Dict[str, str],
    versioning: str,
    current_version: str,
    target_dir: Path,
    ecosystem_explicit: bool = False,
    ci: str = "none",
) -> Dict[str, str]:
    selected = profile
    if not ecosystem_explicit and (detection["mode"] == "greenfield" or not detection["detected"]):
        print("\nConfiguracion de ecosistema frontend:")
        for idx, prof in enumerate(ECOSYSTEM_PROFILES, 1):
            print(f"  {idx}. {prof['runtime_label']} ({prof['ecosystem']})")
        try:
            choice = input(f"Selecciona ecosistema (1-{len(ECOSYSTEM_PROFILES)}) [1]: ").strip()
            sel_idx = int(choice) - 1 if choice else len(ECOSYSTEM_PROFILES) - 1
            if 0 <= sel_idx < len(ECOSYSTEM_PROFILES):
                selected = build_profile_context(target_dir, ECOSYSTEM_PROFILES[sel_idx]["ecosystem"])
        except Exception:
            pass

    try:
        scheme_in = input(
            f"Esquema de versionamiento (semver/calver/sequential) [{versioning}]: "
        ).strip().lower()
        if scheme_in in SCHEME_LABELS:
            versioning = scheme_in
        ver_in = input(f"Version inicial [{current_version}]: ").strip()
        if ver_in:
            current_version = ver_in.lstrip("vV")
        if ci == "none":
            ci_in = input(
                "Instalar guardrail CI de GitHub Actions (.github/workflows/frontend-spec-check.yml)? (s/N) [n]: "
            ).strip().lower()
            if ci_in in ("s", "si", "y", "yes"):
                ci = "github"
    except Exception:
        pass

    return {
        "versioning": versioning,
        "current_version": current_version,
        "ci": ci,
        "_profile": selected,  # type: ignore[dict-item]
    }


def _render_config_yaml(
    templates_root: Path,
    ctx: Dict[str, str],
    harnesses_to_install: List[str],
) -> str:
    cfg_template = templates_root / ".spec" / "config.yaml"
    harnesses_block = "harnesses:\n" + "\n".join(f"  - {h}" for h in harnesses_to_install)

    if cfg_template.exists():
        raw = render_placeholders(cfg_template.read_text(encoding="utf-8"), ctx)
        raw = re.sub(
            r'^version:\s*["\'][^"\'\r\n]+["\']',
            f'version: "{__version__}"',
            raw,
            count=1,
            flags=re.MULTILINE,
        )
        raw = re.sub(
            r"^harnesses:\s*\r?\n(?:\s+-\s+.+\r?\n?)*",
            harnesses_block + "\n",
            raw,
            count=1,
            flags=re.MULTILINE,
        )
        return raw

    return (
        f'framework: frontend-spec\nversion: "{__version__}"\nproject_name: "{ctx["PROJECT_NAME"]}"\n'
        f'versioning_scheme: "{ctx["VERSIONING_SCHEME"]}"\ncurrent_version: "{ctx["CURRENT_VERSION"]}"\n'
        f'current_milestone: "{ctx["MILESTONE_VERSION"]}"\n{harnesses_block}\n'
    )


def run_init(
    target_dir: Path,
    harness: str = "all",
    versioning: str = "semver",
    interactive: bool = False,
    force: bool = False,
    ecosystem: Optional[str] = None,
    mode: str = "auto",
    ci: str = "none",
) -> None:
    """Inicializa frontend-spec en un proyecto frontend Greenfield o Brownfield."""
    target_dir = Path(target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n[INFO] Inicializando frontend-spec v{__version__} en: {target_dir}")

    templates_root = locate_framework_asset("templates")
    harnesses_root = locate_framework_asset("harnesses")
    if not templates_root or not (templates_root / ".spec" / "docs").exists():
        raise RuntimeError(
            "No se encontraron las plantillas base de frontend-spec (templates/.spec/docs)."
        )

    detection = detect_frontend_ecosystem(target_dir)
    print(f"[INFO] {detection['message']}")

    if ecosystem:
        profile = build_profile_context(target_dir, ecosystem)
        print(
            f"[INFO] Perfil de ecosistema fijado por flag --ecosystem: "
            f"{profile['runtime_label']} ({profile['ecosystem']})"
        )
    else:
        profile = detection.get("detected") or build_profile_context(target_dir, "react-vite")

    if mode == "greenfield":
        effective_state = "scaffold" if (target_dir / "package.json").is_file() else "empty"
    elif mode == "brownfield":
        effective_state = "brownfield"
    else:
        effective_state = str(
            detection.get(
                "project_state",
                "empty" if detection["mode"] == "greenfield" else "brownfield",
            )
        )

    current_version = "0.1.0"

    if detection.get("version_path"):
        ver_path = detection["version_path"]
        extracted = extract_version(ver_path, profile["format"])
        if extracted:
            current_version = extracted
            print(f"[OK] Version actual detectada en {ver_path.name}: {current_version}")

    if interactive:
        res = _prompt_interactive_options(
            detection,
            profile,
            versioning,
            current_version,
            target_dir,
            ecosystem_explicit=bool(ecosystem),
            ci=ci,
        )
        versioning = res["versioning"]
        current_version = res["current_version"]
        ci = res.get("ci", ci)
        profile = res["_profile"]  # type: ignore[assignment]

    if current_version == "0.1.0" and versioning == "calver":
        today_dt = datetime.date.today()
        current_version = f"{today_dt.year}.{today_dt.month:02d}.0"

    milestone_version = compute_next_milestone(current_version, versioning)
    today_iso = datetime.date.today().isoformat()

    ctx = build_doc_context(
        project_name=target_dir.name,
        profile=profile,
        current_version=current_version,
        milestone_version=milestone_version,
        versioning=versioning,
        today_iso=today_iso,
        harness=harness,
    )

    docs_dir = target_dir / "docs"
    spec_dir = target_dir / ".spec"
    blueprints_dest = spec_dir / "templates"
    docs_dir.mkdir(parents=True, exist_ok=True)
    blueprints_dest.mkdir(parents=True, exist_ok=True)

    # 1. Blueprints canonicos
    blueprints_src = templates_root / ".spec" / "templates"
    if blueprints_src.exists():
        for bp_file in sorted(blueprints_src.glob("*.md")):
            dest_bp = blueprints_dest / bp_file.name
            if not dest_bp.exists() or force:
                shutil.copy2(bp_file, dest_bp)
        print("[OK] Blueprints instalados en: .spec/templates/")

    # 2. Docs base (4 pilares: functional, design, technical, backlog)
    clean_docs_src = templates_root / ".spec" / "docs"
    for comp in ("functional", "design", "technical", "backlog"):
        src_comp = clean_docs_src / comp
        dest_comp = docs_dir / comp
        dest_comp.mkdir(parents=True, exist_ok=True)
        for src_md in sorted(src_comp.rglob("*.md")):
            dest_md = dest_comp / src_md.relative_to(src_comp)
            dest_md.parent.mkdir(parents=True, exist_ok=True)
            if not dest_md.exists() or force:
                rendered = render_placeholders(src_md.read_text(encoding="utf-8"), ctx)
                dest_md.write_text(rendered, encoding="utf-8")
        print(f"[OK] Modulo documental inicializado: docs/{comp}")

    uf_dir = docs_dir / "functional" / "user-flows"
    uf_dir.mkdir(parents=True, exist_ok=True)
    gitkeep = uf_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")

    # 3. Harnesses y configuracion
    harnesses_to_install = [h for h in HARNESS_NAMES if harness in ("all", h)]
    config_content = _render_config_yaml(templates_root, ctx, harnesses_to_install)
    config_path = spec_dir / "config.yaml"
    if not config_path.exists() or force:
        config_path.write_text(config_content, encoding="utf-8")
        print("[OK] Configuracion generada: .spec/config.yaml")

    # 4. .graphifyignore y .gitignore
    gi_src = templates_root / ".graphifyignore"
    gi_dest = target_dir / ".graphifyignore"
    if gi_src.exists() and (not gi_dest.exists() or force):
        shutil.copy2(gi_src, gi_dest)
        print("[OK] Generado: .graphifyignore")

    gitignore_src = templates_root / ".gitignore"
    gitignore_dest = target_dir / ".gitignore"
    if gitignore_src.exists() and not gitignore_dest.exists():
        shutil.copy2(gitignore_src, gitignore_dest)
        print("[OK] Generado: .gitignore")

    # 5. Reglas, comandos /ui-* y skills por harness
    if harnesses_root and harnesses_root.exists():
        for h_name in harnesses_to_install:
            for msg in install_or_update_harness(
                target_dir, templates_root, harnesses_root, h_name, dry_run=False
            ):
                print(f"[OK] {msg}")

    # 6. Pre-commit hook
    hook_src = templates_root / ".githooks" / "pre-commit"
    if (target_dir / ".git").is_dir() and hook_src.exists():
        res_hook = update_pre_commit_hook(target_dir, hook_src, dry_run=False)
        if res_hook != "NO_GIT":
            print(f"[OK] Git Hook instalado en .git/hooks/pre-commit ({res_hook})")

    # 7. Guardrail CI GitHub Actions opt-in
    if ci == "github":
        ci_res = update_github_ci_workflow(
            target_dir, templates_root, ci="github", force=force, dry_run=False
        )
        if ci_res in ("CREATED", "UPDATED"):
            print(
                f"[OK] Guardrail CI instalado en .github/workflows/frontend-spec-check.yml ({ci_res})"
            )
        elif ci_res == "SKIPPED_CUSTOM":
            print(
                "[INFO] .github/workflows/frontend-spec-check.yml ya existe sin marcador gestionado "
                "(conservado sin sobrescribir)"
            )

    print(f"\n[OK] frontend-spec v{__version__} inicializado con exito.")
    if effective_state == "brownfield":
        print("[INFO] Proyecto existente detectado: ejecuta 'frontend-spec bootstrap' (o '/ui-bootstrap') para inventariar rutas, componentes y tokens.")
    elif effective_state == "scaffold":
        print("[INFO] Scaffold inicial detectado: define tokens en 'docs/design/tokens-and-themes.md' y registra 'REQ-UI-CORE-001' (no requiere 'fspec bootstrap').")
    else:
        print("[INFO] Proyecto vacio inicializado: tras generar el scaffold Node, ejecuta 'frontend-spec update --refresh-stack' para alinear .spec/config.yaml y tech-stack.md.")
    print("[INFO] Revisa 'docs/technical/index.md', 'docs/design/index.md' y 'docs/backlog/pending.md'.\n")
