import datetime
import re
import shutil
import stat
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from frontend_spec import __version__
from frontend_spec.commands.bootstrap_cmd import _update_tech_stack_sync
from frontend_spec.commands.check_cmd import run_check
from frontend_spec.commands.sync_index_cmd import run_sync_index
from frontend_spec.common import (
    HARNESS_NAMES,
    build_doc_context,
    read_config_settings,
    render_placeholders,
)
from frontend_spec.detector.ecosystem_detector import build_profile_context
from frontend_spec.detector.version_extractor import compute_next_milestone, extract_version
from frontend_spec.validator.schema_validator import locate_framework_asset

HARNESS_DETECTION_PATHS: Dict[str, List[Path]] = {
    "antigravity": [
        Path(".gemini/rules/frontend-spec.md"),
        Path(".gemini/skills/frontend-spec"),
    ],
    "cursor": [
        Path(".cursor/rules/frontend-spec.mdc"),
        Path(".cursor/commands/ui-plan.md"),
        Path(".cursor/skills/frontend-spec"),
    ],
    "claude": [
        Path(".claude/commands/ui-plan.md"),
        Path(".claude/skills/frontend-spec"),
    ],
    "windsurf": [
        Path(".windsurf/workflows/ui-plan.md"),
        Path(".windsurf/skills/frontend-spec"),
    ],
}


def detect_installed_harnesses(target_dir: Path) -> List[str]:
    """Detecta que harnesses ya tienen configuracion frontend-spec en el repo."""
    detected: List[str] = []
    for h_name in HARNESS_NAMES:
        paths = HARNESS_DETECTION_PATHS[h_name]
        if any((target_dir / p).exists() for p in paths):
            detected.append(h_name)
            continue
        if h_name == "claude" and (target_dir / "CLAUDE.md").exists():
            txt = (target_dir / "CLAUDE.md").read_text(encoding="utf-8", errors="ignore")
            if "FRONTEND-SPEC:START" in txt or "frontend-spec" in txt:
                detected.append(h_name)
        elif h_name == "windsurf" and (target_dir / ".windsurfrules").exists():
            txt = (target_dir / ".windsurfrules").read_text(encoding="utf-8", errors="ignore")
            if "FRONTEND-SPEC:START" in txt or "frontend-spec" in txt:
                detected.append(h_name)
    return detected


def update_managed_markdown(dest_path: Path, template_path: Path, dry_run: bool = False) -> str:
    """Inserta o actualiza el bloque <!-- FRONTEND-SPEC:START/END --> preservando BACKEND-SPEC y reglas propias."""
    template_content = template_path.read_text(encoding="utf-8")
    tmpl_match = re.search(
        r"<!-- FRONTEND-SPEC:START -->(.*?)<!-- FRONTEND-SPEC:END -->",
        template_content,
        re.DOTALL,
    )
    new_block = tmpl_match.group(1).strip() if tmpl_match else template_content.strip()
    full_managed = f"<!-- FRONTEND-SPEC:START -->\n{new_block}\n<!-- FRONTEND-SPEC:END -->"

    if not dest_path.exists():
        if not dry_run:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_text(template_content, encoding="utf-8")
        return "CREATED"

    dest_content = dest_path.read_text(encoding="utf-8")
    dest_match = re.search(
        r"<!-- FRONTEND-SPEC:START -->.*?<!-- FRONTEND-SPEC:END -->",
        dest_content,
        re.DOTALL,
    )
    if dest_match:
        updated = (
            dest_content[: dest_match.start()]
            + full_managed
            + dest_content[dest_match.end() :]
        )
        if not dry_run:
            dest_path.write_text(updated, encoding="utf-8")
        return "UPDATED_BLOCK"

    fm_match = re.match(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)", dest_content, re.DOTALL)
    if fm_match:
        rest = dest_content[fm_match.end() :].strip()
        updated = f"{dest_content[: fm_match.end()]}\n{full_managed}\n\n{rest}\n"
    elif "BACKEND-SPEC:START" in dest_content:
        updated = f"{dest_content.rstrip()}\n\n{full_managed}\n"
    else:
        updated = f"{full_managed}\n\n<!-- Custom Project Rules -->\n{dest_content.strip()}\n"

    if not dry_run:
        dest_path.write_text(updated, encoding="utf-8")
    return "MERGED_PRESERVING_USER_CONTENT"


def merge_graphifyignore(dest_path: Path, template_path: Path, dry_run: bool = False) -> int:
    if not dest_path.exists():
        if not dry_run:
            dest_path.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
        return -1

    existing_lines = dest_path.read_text(encoding="utf-8").splitlines()
    existing_set = {ln.strip() for ln in existing_lines if ln.strip() and not ln.strip().startswith("#")}

    added: List[str] = []
    for ln in template_path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s and not s.startswith("#") and s not in existing_set:
            added.append(ln)
            existing_set.add(s)

    if added and not dry_run:
        new_txt = (
            dest_path.read_text(encoding="utf-8").rstrip()
            + "\n\n# frontend-spec additions\n"
            + "\n".join(added)
            + "\n"
        )
        dest_path.write_text(new_txt, encoding="utf-8")
    return len(added)


def update_pre_commit_hook(target_dir: Path, hook_src: Path, dry_run: bool = False) -> str:
    git_dir = target_dir / ".git"
    if not git_dir.exists() or not git_dir.is_dir():
        return "NO_GIT"

    hooks_dir = git_dir / "hooks"
    hook_dest = hooks_dir / "pre-commit"
    hook_src_content = hook_src.read_text(encoding="utf-8")

    tmpl_match = re.search(
        r"# FRONTEND-SPEC:START(.*?)# FRONTEND-SPEC:END", hook_src_content, re.DOTALL
    )
    managed_block = tmpl_match.group(1).strip() if tmpl_match else hook_src_content.strip()
    full_managed = f"# FRONTEND-SPEC:START\n{managed_block}\n# FRONTEND-SPEC:END"

    if not hook_dest.exists():
        if not dry_run:
            hooks_dir.mkdir(parents=True, exist_ok=True)
            hook_dest.write_text(hook_src_content, encoding="utf-8")
            try:
                hook_dest.chmod(hook_dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            except Exception:
                pass
        return "CREATED"

    current_dest = hook_dest.read_text(encoding="utf-8", errors="ignore")
    if "# FRONTEND-SPEC:START" in current_dest and "# FRONTEND-SPEC:END" in current_dest:
        dest_match = re.search(
            r"# FRONTEND-SPEC:START.*?# FRONTEND-SPEC:END", current_dest, re.DOTALL
        )
        updated = (
            current_dest[: dest_match.start()]
            + full_managed
            + current_dest[dest_match.end() :]
        )
        if not dry_run:
            hook_dest.write_text(updated, encoding="utf-8")
        return "UPDATED_BLOCK"

    exit_match = re.search(r"(?m)^\s*exit\s+0\s*$", current_dest)
    if exit_match:
        updated = (
            current_dest[: exit_match.start()]
            + f"\n{full_managed}\n\n"
            + current_dest[exit_match.start() :]
        )
    else:
        updated = current_dest.rstrip() + f"\n\n{full_managed}\n"

    if not dry_run:
        hook_dest.write_text(updated, encoding="utf-8")
        try:
            hook_dest.chmod(hook_dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except Exception:
            pass
    return "INJECTED_INTO_EXISTING"


def update_github_ci_workflow(
    target_dir: Path,
    templates_root: Path,
    ci: Optional[str] = None,
    force: bool = False,
    dry_run: bool = False,
) -> str:
    """Instala o actualiza el workflow gestionado .github/workflows/frontend-spec-check.yml."""
    if ci == "none":
        return "SKIPPED"

    src_wf = templates_root / ".github" / "workflows" / "frontend-spec-check.yml"
    if not src_wf.exists():
        return "MISSING_TEMPLATE"

    rendered = src_wf.read_text(encoding="utf-8").replace("{{FRAMEWORK_VERSION}}", __version__)
    dest_wf = target_dir / ".github" / "workflows" / "frontend-spec-check.yml"

    if not dest_wf.exists():
        if ci != "github":
            return "NOT_INSTALLED"
        if not dry_run:
            dest_wf.parent.mkdir(parents=True, exist_ok=True)
            dest_wf.write_text(rendered, encoding="utf-8")
        return "CREATED"

    existing = dest_wf.read_text(encoding="utf-8", errors="ignore")
    if "# FRONTEND-SPEC-CI-MANAGED" in existing or force:
        if not dry_run:
            dest_wf.write_text(rendered, encoding="utf-8")
        return "UPDATED"

    return "SKIPPED_CUSTOM"


def install_harness_skills(
    target_dir: Path,
    templates_root: Path,
    harness: str,
    dry_run: bool = False,
) -> List[str]:
    """Instala skills por harness resolviendo triggers y estrategias de entrevista."""
    installed_items: List[str] = []
    skills_src = templates_root / ".spec" / "skills"
    if not skills_src.exists():
        return installed_items

    interview_trigger = "/grill-me" if harness == "antigravity" else "/ui-grill"
    question_strategies = {
        "antigravity": "Pregunta de 2 a 4 decisiones por ronda en el chat colocando primero la opcion recomendada con trade-offs claros",
        "claude": "Utiliza `AskUserQuestion` (2 a 4 decisiones por ronda, opcion `(Recommended)` primero y trade-offs concisos)",
        "cursor": "Utiliza `AskQuestion` por tarjeta interactiva (2 a 4 decisiones por ronda, opcion `(Recommended)` primero)",
        "windsurf": "Presenta de 2 a 4 decisiones con formato `A) (Recomendado) / B) / C)` y detente en pausa estructurada esperando respuesta",
    }
    ctx = {
        "HARNESS_INTERVIEW_TRIGGER": interview_trigger,
        "HARNESS_QUESTION_STRATEGY": question_strategies.get(
            harness, "Formula de 2 a 4 decisiones ordenadas con opcion recomendada primero"
        ),
    }

    dest_map = {
        "antigravity": target_dir / ".gemini" / "skills",
        "cursor": target_dir / ".cursor" / "skills",
        "claude": target_dir / ".claude" / "skills",
        "windsurf": target_dir / ".windsurf" / "skills",
    }
    skills_by_harness = {
        "antigravity": (
            "frontend-spec",
            "frontend-bootstrap",
            "frontend-deploy",
            "frontend-design",
            "theme-factory",
            "webapp-testing",
        ),
        "claude": (
            "frontend-spec",
            "frontend-bootstrap",
            "frontend-deploy",
            "ui-grill",
            "frontend-design",
            "theme-factory",
            "webapp-testing",
        ),
        "cursor": (
            "frontend-spec",
            "frontend-bootstrap",
            "frontend-deploy",
            "ui-grill",
            "frontend-design",
            "theme-factory",
            "webapp-testing",
        ),
        "windsurf": (
            "frontend-spec",
            "frontend-bootstrap",
            "frontend-deploy",
            "ui-grill",
            "frontend-design",
            "theme-factory",
            "webapp-testing",
        ),
    }

    skills_dest = dest_map.get(harness)
    if not skills_dest:
        return installed_items

    for sk in skills_by_harness.get(harness, ()):
        src_file = skills_src / sk / "SKILL.md"
        if not src_file.exists():
            continue
        dest_file = skills_dest / sk / "SKILL.md"
        if not dry_run:
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            dest_file.write_text(
                render_placeholders(src_file.read_text(encoding="utf-8"), ctx),
                encoding="utf-8",
            )
        installed_items.append(dest_file.relative_to(target_dir).as_posix())

    return installed_items


def install_or_update_harness(
    target_dir: Path,
    templates_root: Path,
    harnesses_root: Path,
    h_name: str,
    dry_run: bool,
) -> List[str]:
    logs: List[str] = []

    rule_specs: Dict[str, Tuple[Path, Path]] = {
        "antigravity": (
            harnesses_root / "antigravity" / "rules" / "frontend-spec.md",
            target_dir / ".gemini" / "rules" / "frontend-spec.md",
        ),
        "cursor": (
            harnesses_root / "cursor" / "rules" / "frontend-spec.mdc",
            target_dir / ".cursor" / "rules" / "frontend-spec.mdc",
        ),
        "claude": (
            harnesses_root / "claude" / "CLAUDE.md",
            target_dir / "CLAUDE.md",
        ),
        "windsurf": (
            harnesses_root / "windsurf" / ".windsurfrules",
            target_dir / ".windsurfrules",
        ),
    }

    if h_name in rule_specs:
        src_rule, dest_rule = rule_specs[h_name]
        if src_rule.exists():
            status = update_managed_markdown(dest_rule, src_rule, dry_run=dry_run)
            logs.append(f"Regla {h_name} ({dest_rule.relative_to(target_dir).as_posix()}): {status}")

    cmd_dirs = {
        "cursor": (templates_root / ".cursor" / "commands", target_dir / ".cursor" / "commands"),
        "claude": (templates_root / ".claude" / "commands", target_dir / ".claude" / "commands"),
        "windsurf": (templates_root / ".windsurf" / "workflows", target_dir / ".windsurf" / "workflows"),
    }
    if h_name in cmd_dirs:
        src_cmd_dir, dest_cmd_dir = cmd_dirs[h_name]
        if src_cmd_dir.exists():
            if not dry_run:
                dest_cmd_dir.mkdir(parents=True, exist_ok=True)
            for f in sorted(src_cmd_dir.glob("*.md")):
                dest_cmd = dest_cmd_dir / f.name
                if not dry_run:
                    shutil.copy2(f, dest_cmd)
                logs.append(f"Comando {h_name}: {dest_cmd.relative_to(target_dir).as_posix()}")

    skills = install_harness_skills(target_dir, templates_root, h_name, dry_run=dry_run)
    if skills:
        logs.append(f"Skills {h_name}: {', '.join(skills)}")
    return logs


def _ensure_missing_docs_non_destructive(
    target_dir: Path, templates_root: Path, dry_run: bool, harness: str = "all"
) -> List[str]:
    created: List[str] = []
    cfg = read_config_settings(target_dir)
    profile = build_profile_context(target_dir, ecosystem_key=cfg["ecosystem"])
    ctx = build_doc_context(
        project_name=target_dir.name,
        profile=profile,
        current_version=cfg["current_version"],
        milestone_version=cfg["current_milestone"],
        versioning=cfg["versioning_scheme"],
        today_iso=datetime.date.today().isoformat(),
        harness=harness,
    )

    clean_docs = templates_root / ".spec" / "docs"
    for comp in ("functional", "design", "technical", "backlog"):
        src_comp = clean_docs / comp
        dest_comp = target_dir / "docs" / comp
        if not src_comp.exists():
            continue
        for src_md in sorted(src_comp.rglob("*.md")):
            dest_md = dest_comp / src_md.relative_to(src_comp)
            if not dest_md.exists():
                created.append(dest_md.relative_to(target_dir).as_posix())
                if not dry_run:
                    dest_md.parent.mkdir(parents=True, exist_ok=True)
                    dest_md.write_text(
                        render_placeholders(src_md.read_text(encoding="utf-8"), ctx),
                        encoding="utf-8",
                    )
    return created


def _update_indented_yaml_block(raw: str, section: str, values: Dict[str, str]) -> str:
    block_pat = re.compile(
        rf"(^{re.escape(section)}:\s*\r?\n)((?:[ \t]+[^\r\n]*\r?\n?)*)",
        re.MULTILINE,
    )
    m = block_pat.search(raw)
    if not m:
        return raw
    block_body = m.group(2)
    for k, v in values.items():
        key_pat = re.compile(
            rf"^([ \t]+{re.escape(k)}:\s*)([\"']?[^\"'\r\n#]+[\"']?)([ \t]*(?:#.*)?)$",
            re.MULTILINE,
        )
        block_body = key_pat.sub(
            lambda km, val=v: f'{km.group(1)}"{val}"{km.group(3)}',
            block_body,
            count=1,
        )
    return raw[: m.start(2)] + block_body + raw[m.end(2) :]


def _refresh_detected_stack(target_dir: Path, dry_run: bool = False) -> str:
    """Re-detecta package.json/stack real y sincroniza .spec/config.yaml y docs/technical/tech-stack.md."""
    profile = build_profile_context(target_dir)
    cfg = read_config_settings(target_dir)

    ver_file = target_dir / profile["version_file"]
    detected_ver = (
        extract_version(ver_file, profile["format"]) if ver_file.is_file() else None
    )
    effective_ver = detected_ver or cfg["current_version"]

    if not dry_run:
        cfg_path = target_dir / ".spec" / "config.yaml"
        if cfg_path.exists():
            raw = cfg_path.read_text(encoding="utf-8")
            raw = _update_indented_yaml_block(
                raw,
                "ecosystem",
                {
                    "name": profile["ecosystem"],
                    "framework": profile["framework"],
                    "meta_framework": profile["meta_framework"],
                    "language": profile["language"],
                    "package_manager": profile["package_manager"],
                    "styling": profile["styling"],
                    "ui_primitives": profile["ui_primitives"],
                    "state_server": profile["state_server"],
                    "unit_test_runner": profile["unit_test_runner"],
                    "testing_library": profile["testing_library"],
                    "e2e_runner": profile["e2e_runner"],
                    "src_dir": profile["src_dir"],
                    "routes_dir": profile["routes_dir"],
                    "test_pattern": profile["test_pattern"],
                },
            )
            raw = _update_indented_yaml_block(
                raw,
                "version_file",
                {
                    "path": profile["version_file"],
                    "format": profile["format"],
                    "field": profile["field"],
                },
            )
            if detected_ver and cfg["current_version"] == "0.1.0" and detected_ver != "0.1.0":
                next_ms = compute_next_milestone(detected_ver, cfg["versioning_scheme"])
                raw = re.sub(
                    r'^current_version:\s*["\']?[^"\'\r\n]+["\']?',
                    f'current_version: "{detected_ver}"',
                    raw,
                    count=1,
                    flags=re.MULTILINE,
                )
                raw = re.sub(
                    r'^current_milestone:\s*["\']?[^"\'\r\n]+["\']?',
                    f'current_milestone: "{next_ms}"',
                    raw,
                    count=1,
                    flags=re.MULTILINE,
                )
            cfg_path.write_text(raw, encoding="utf-8")

        _update_tech_stack_sync(target_dir / "docs", profile, effective_ver)

    return (
        f"{profile['runtime_label']} "
        f"({profile['ecosystem']} / {profile['language']} / {profile['styling']} / v{effective_ver})"
    )


def run_update(
    target_dir: Path,
    harness: Optional[str] = None,
    dry_run: bool = False,
    refresh_stack: bool = False,
    ci: Optional[str] = None,
) -> bool:
    """Actualiza plantillas, skills, reglas gestionadas y hook pre-commit sin tocar docs/ existentes."""
    target_dir = Path(target_dir).resolve()
    spec_dir = target_dir / ".spec"
    docs_dir = target_dir / "docs"

    if not spec_dir.exists() or not docs_dir.exists():
        print("[ERROR] El proyecto no tiene .spec/ y docs/. Ejecuta 'frontend-spec init' primero.")
        return False

    templates_root = locate_framework_asset("templates")
    harnesses_root = locate_framework_asset("harnesses")
    if not templates_root or not harnesses_root:
        print("[ERROR] No se localizaron los activos base de frontend-spec (templates/ y harnesses/).")
        return False

    mode_label = "[DRY-RUN] " if dry_run else ""
    print(f"\n[INFO] {mode_label}Actualizando frontend-spec en: {target_dir}")

    if refresh_stack:
        stack_summary = _refresh_detected_stack(target_dir, dry_run=dry_run)
        print(f"[OK] {mode_label}Stack sincronizado en .spec/config.yaml y tech-stack.md: {stack_summary}")

    # 1. Blueprints .spec/templates/
    bp_src = templates_root / ".spec" / "templates"
    bp_dest = spec_dir / "templates"
    updated_bps = 0
    if bp_src.exists():
        if not dry_run:
            bp_dest.mkdir(parents=True, exist_ok=True)
        for bp in sorted(bp_src.glob("*.md")):
            updated_bps += 1
            if not dry_run:
                shutil.copy2(bp, bp_dest / bp.name)
    print(f"[OK] {mode_label}Blueprints actualizados en .spec/templates/: {updated_bps}")

    # 2. Harnesses objetivo y docs faltantes no destructivos
    if harness == "all":
        target_harnesses = list(HARNESS_NAMES)
    elif harness in HARNESS_NAMES:
        target_harnesses = [harness]
    else:
        target_harnesses = detect_installed_harnesses(target_dir) or ["antigravity"]

    effective_harness = target_harnesses[0] if len(target_harnesses) == 1 else "all"
    created_docs = _ensure_missing_docs_non_destructive(
        target_dir, templates_root, dry_run=dry_run, harness=effective_harness
    )
    if created_docs:
        print(f"[OK] {mode_label}Documentos base faltantes creados: {', '.join(created_docs)}")

    # 3. Harnesses
    for h in target_harnesses:
        for line in install_or_update_harness(target_dir, templates_root, harnesses_root, h, dry_run=dry_run):
            print(f"[OK] {mode_label}{line}")

    # 4. .graphifyignore
    gi_src = templates_root / ".graphifyignore"
    if gi_src.exists():
        gi_added = merge_graphifyignore(target_dir / ".graphifyignore", gi_src, dry_run=dry_run)
        if gi_added == -1:
            print(f"[OK] {mode_label}.graphifyignore creado")
        elif gi_added > 0:
            print(f"[OK] {mode_label}.graphifyignore ampliado con {gi_added} exclusiones nuevas")

    # 5. Pre-commit hook
    hook_src = templates_root / ".githooks" / "pre-commit"
    if hook_src.exists():
        hook_res = update_pre_commit_hook(target_dir, hook_src, dry_run=dry_run)
        if hook_res != "NO_GIT":
            print(f"[OK] {mode_label}.git/hooks/pre-commit: {hook_res}")

    # 5b. Guardrail CI GitHub Actions opt-in
    ci_res = update_github_ci_workflow(
        target_dir, templates_root, ci=ci, force=False, dry_run=dry_run
    )
    if ci_res in ("CREATED", "UPDATED"):
        print(f"[OK] {mode_label}.github/workflows/frontend-spec-check.yml: {ci_res}")
    elif ci_res == "SKIPPED_CUSTOM":
        print(
            f"[INFO] {mode_label}.github/workflows/frontend-spec-check.yml personalizado detectado "
            "(conservado sin sobrescribir)"
        )

    # 6. Sincronizar e inspeccionar
    if not dry_run:
        run_sync_index(target_dir)
        return run_check(target_dir)

    print("[INFO] Simulacion --dry-run finalizada sin escribir archivos.")
    return True
