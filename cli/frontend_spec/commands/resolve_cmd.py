import datetime
import re
import subprocess
from pathlib import Path

from frontend_spec.commands.sync_index_cmd import run_sync_index
from frontend_spec.common import read_config_settings
from frontend_spec.detector.version_extractor import (
    compare_versions,
    compute_next_milestone,
    extract_version,
    update_version,
)


def run_resolve(
    project_root: Path,
    req_id: str,
    auto_bump: bool = False,
    force_version: bool = False,
) -> bool:
    """Archiva un REQ-UI-* completado en changelog.md, sincroniza indices y opcionalmente hace bump."""
    project_root = Path(project_root).resolve()
    docs_dir = project_root / "docs"
    pending_file = docs_dir / "backlog" / "pending.md"
    changelog_file = docs_dir / "backlog" / "changelog.md"

    if not pending_file.exists() or not changelog_file.exists():
        print("[ERROR] docs/backlog/pending.md o changelog.md no encontrados.")
        return False

    pending_content = pending_file.read_text(encoding="utf-8")
    pattern = rf"(###\s*\[{re.escape(req_id)}\].*?)(?=###\s*\[REQ-|\n##\s+Milestone|\Z)"
    match = re.search(pattern, pending_content, re.DOTALL)
    if not match:
        print(f"[ERROR] Requerimiento {req_id} no encontrado en docs/backlog/pending.md.")
        return False

    req_block = re.sub(r"(?:\r?\n---\s*)+\Z", "", match.group(1).strip()).strip()
    v_match = re.search(r"-\s*\*\*Versión Objetivo:\*\*\s*`?([^\n`]+)`?", req_block)
    target_version = v_match.group(1).strip() if v_match else "v0.1.0"
    if not target_version.startswith("v"):
        target_version = f"v{target_version}"

    # 1. Retirar de pending.md y sincronizar indice
    new_pending = pending_content[: match.start()] + pending_content[match.end() :]
    new_pending = re.sub(r"\n{3,}", "\n\n", new_pending).rstrip() + "\n"
    pending_file.write_text(new_pending, encoding="utf-8")
    print(f"[OK] Requerimiento {req_id} retirado de docs/backlog/pending.md")
    run_sync_index(project_root)

    # 2. Registrar en changelog.md
    changelog_content = changelog_file.read_text(encoding="utf-8")
    today = datetime.date.today().isoformat()
    resolved_block = re.sub(r"-\s*\[ \]", "- [x]", req_block)
    lines = resolved_block.splitlines()
    if lines:
        lines.insert(1, f"- **Fecha de Resolución:** `{today}`")
        resolved_block = "\n".join(lines)

    version_header_regex = rf"^##\s+Release\s+{re.escape(target_version)}\b[^\n]*"
    header_match = re.search(version_header_regex, changelog_content, re.MULTILINE)
    if header_match:
        end_pos = header_match.end()
        updated_changelog = (
            changelog_content[:end_pos]
            + f"\n\n{resolved_block}\n"
            + changelog_content[end_pos:]
        )
    else:
        updated_changelog = (
            changelog_content.rstrip()
            + f"\n\n---\n\n## Release {target_version} (Actualizado: {today})\n\n{resolved_block}\n"
        )
    changelog_file.write_text(updated_changelog, encoding="utf-8")
    print(f"[OK] Requerimiento {req_id} archivado en docs/backlog/changelog.md")

    # 3. Auto-bump opcional en package.json + .spec/config.yaml
    if auto_bump:
        cfg = read_config_settings(project_root)
        manifest_path = project_root / cfg["manifest_path"]
        manifest_fmt = cfg["manifest_format"]
        scheme = cfg["versioning_scheme"]
        clean_ver = target_version.lstrip("vV")

        current_manifest_ver = extract_version(manifest_path, manifest_fmt)
        if (
            current_manifest_ver
            and compare_versions(clean_ver, current_manifest_ver) < 0
            and not force_version
        ):
            print(
                f"[WARN] Proteccion anti-downgrade: {clean_ver} < {current_manifest_ver} en "
                f"{manifest_path.name}. Usa --force-version para sobrescribir."
            )
        else:
            if (manifest_path.exists() or manifest_fmt == "plain") and update_version(
                manifest_path, manifest_fmt, clean_ver
            ):
                print(f"[OK] Manifiesto {manifest_path.name} actualizado a {clean_ver}")

            config_file = project_root / ".spec" / "config.yaml"
            if config_file.exists():
                next_ms = compute_next_milestone(clean_ver, scheme)
                cfg_txt = config_file.read_text(encoding="utf-8")
                cfg_txt = re.sub(
                    r'^current_version:\s*["\']?[^"\'\r\n]+["\']?',
                    f'current_version: "{clean_ver}"',
                    cfg_txt,
                    flags=re.MULTILINE,
                )
                cfg_txt = re.sub(
                    r'^current_milestone:\s*["\']?[^"\'\r\n]+["\']?',
                    f'current_milestone: "{next_ms}"',
                    cfg_txt,
                    flags=re.MULTILINE,
                )
                config_file.write_text(cfg_txt, encoding="utf-8")

    # 4. Actualizar grafo Graphify si existe
    if (project_root / "graphify-out").exists():
        try:
            res = subprocess.run(
                ["graphify", "update"],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
            if res.returncode == 0:
                print("[OK] Grafo Graphify actualizado (graphify update).")
        except Exception:
            pass

    return True
