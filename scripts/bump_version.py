#!/usr/bin/env python3
"""Valida y actualiza la versión SemVer de frontend-spec de forma atómica."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-(?:alpha|beta|rc)\.\d+)?$")
VER_CAPTURE = r"(\d+\.\d+\.\d+(?:-(?:alpha|beta|rc)\.\d+)?)"


class VersionRule(NamedTuple):
    """Regla declarativa para extraer o reemplazar una versión en un archivo."""

    rel_path: str
    pattern: re.Pattern[str]
    replacement: str
    expected_count: int = 1


RULES: tuple[VersionRule, ...] = (
    VersionRule(
        "pyproject.toml",
        re.compile(rf'(?m)^(version\s*=\s*"){VER_CAPTURE}(")$'),
        r"\g<1>{version}\g<3>",
    ),
    VersionRule(
        "cli/frontend_spec/__init__.py",
        re.compile(rf'(?m)^(__version__\s*=\s*"){VER_CAPTURE}(")$'),
        r"\g<1>{version}\g<3>",
    ),
    VersionRule(
        "README.md",
        re.compile(rf"(?m)^(# frontend-spec v){VER_CAPTURE}$"),
        r"\g<1>{version}",
    ),
    VersionRule(
        "README.md",
        re.compile(rf"(`v0\.1\.0` -> `v){VER_CAPTURE}(`)"),
        r"\g<1>{version}\g<3>",
    ),
    VersionRule(
        "agent-prompts/AGENTS.md",
        re.compile(rf"(?m)^(# Instrucciones Canónicas para Agentes de IA \(`frontend-spec` v){VER_CAPTURE}(\))$"),
        r"\g<1>{version}\g<3>",
    ),
    VersionRule(
        "agent-prompts/AGENTS.md",
        re.compile(rf"(\*\*`frontend-spec` v){VER_CAPTURE}(\*\*)"),
        r"\g<1>{version}\g<3>",
    ),
    VersionRule(
        "templates/.githooks/pre-commit",
        re.compile(rf"(?m)^(# frontend-spec v){VER_CAPTURE}( - Pre-commit Hook.*)$"),
        r"\g<1>{version}\g<3>",
    ),
    VersionRule(
        "templates/.spec/config.yaml",
        re.compile(rf"(?m)^(# frontend-spec v){VER_CAPTURE}( - .*)$"),
        r"\g<1>{version}\g<3>",
    ),
    VersionRule(
        "templates/.spec/config.yaml",
        re.compile(rf'(?m)^(version:\s*"){VER_CAPTURE}(")$'),
        r"\g<1>{version}\g<3>",
    ),
    VersionRule(
        "templates/.spec/docs/backlog/changelog.md",
        re.compile(rf"(?m)^(- \*\*`\[INIT\]` Adopción de `frontend-spec` v){VER_CAPTURE}(\*\*)$"),
        r"\g<1>{version}\g<3>",
    ),
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_versions() -> tuple[list[tuple[str, str]], list[str]]:
    found: list[tuple[str, str]] = []
    errors: list[str] = []
    for rule in RULES:
        target = ROOT / rule.rel_path
        if not target.is_file():
            errors.append(f"Archivo faltante: {rule.rel_path}")
            continue
        matches = rule.pattern.findall(_read_text(target))
        if len(matches) != rule.expected_count:
            errors.append(
                f"{rule.rel_path}: se esperaban {rule.expected_count} coincidencia(s) "
                f"para '{rule.pattern.pattern}', encontradas {len(matches)}"
            )
            continue
        for match in matches:
            version = match[1] if isinstance(match, tuple) else match
            found.append((rule.rel_path, version))
    return found, errors


def check_versions() -> int:
    """Verifica que todos los archivos declarados compartan la misma versión."""
    found, errors = _extract_versions()
    if errors:
        for err in errors:
            print(f"[ERROR] {err}", file=sys.stderr)
        return 1

    unique_versions = {ver for _, ver in found}
    if len(unique_versions) != 1:
        print("[ERROR] Versiones desincronizadas:", file=sys.stderr)
        for rel_path, ver in found:
            print(f"  - {rel_path}: {ver}", file=sys.stderr)
        return 1

    current = next(iter(unique_versions))
    print(f"[OK] Todas las referencias coinciden en v{current} ({len(found)} ubicaciones).")
    return 0


def _changelog_has_section(version: str) -> bool:
    changelog = ROOT / "CHANGELOG.md"
    if not changelog.is_file():
        return False
    pattern = re.compile(rf"(?m)^## \[{re.escape(version)}\](?:\s|$)")
    return bool(pattern.search(_read_text(changelog)))


def bump_version(target_version: str, dry_run: bool, create_tag: bool) -> int:
    """Actualiza la versión en todos los archivos objetivo y opcionalmente crea commit y tag."""
    if not SEMVER_RE.match(target_version):
        print(
            f"[ERROR] Versión '{target_version}' inválida. Usa MAJOR.MINOR.PATCH "
            "(o con sufijo -alpha.N / -beta.N / -rc.N).",
            file=sys.stderr,
        )
        return 1

    _, errors = _extract_versions()
    if errors:
        for err in errors:
            print(f"[ERROR] {err}", file=sys.stderr)
        return 1

    if create_tag and not _changelog_has_section(target_version):
        print(
            f"[ERROR] CHANGELOG.md no contiene la sección '## [{target_version}]'. "
            "Agrégala antes de crear el tag.",
            file=sys.stderr,
        )
        return 1

    grouped_rules: dict[str, list[VersionRule]] = {}
    for rule in RULES:
        grouped_rules.setdefault(rule.rel_path, []).append(rule)

    touched_files: list[str] = []
    for rel_path, file_rules in grouped_rules.items():
        path = ROOT / rel_path
        original = _read_text(path)
        updated = original
        for rule in file_rules:
            updated = rule.pattern.sub(rule.replacement.format(version=target_version), updated)
        if updated != original:
            touched_files.append(rel_path)
            if not dry_run:
                path.write_text(updated, encoding="utf-8")

    prefix = "[DRY-RUN] " if dry_run else "[OK] "
    print(f"{prefix}Versión objetivo: v{target_version}")
    for rel_path in touched_files:
        print(f"  - {rel_path}")

    if dry_run or not create_tag:
        return 0

    test_cmd = [sys.executable, "-m", "unittest", "discover", "-s", "cli/tests", "-v"]
    if subprocess.run(test_cmd, cwd=ROOT).returncode != 0:
        print("[ERROR] Las pruebas unitarias fallaron; se cancela el commit/tag.", file=sys.stderr)
        return 1

    files_to_stage = sorted(set(touched_files))
    subprocess.run(["git", "add", *files_to_stage], cwd=ROOT, check=True)
    subprocess.run(["git", "commit", "-m", f"chore(release): v{target_version}"], cwd=ROOT, check=True)
    subprocess.run(
        ["git", "tag", "-a", f"v{target_version}", "-m", f"Release v{target_version}"],
        cwd=ROOT,
        check=True,
    )
    print(f"[OK] Commit y tag v{target_version} creados. Ejecuta: git push origin main --follow-tags")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida o actualiza la versión de frontend-spec.")
    parser.add_argument("version", nargs="?", help="Nueva versión SemVer (ej. 1.3.1)")
    parser.add_argument("--check", action="store_true", help="Verifica coherencia sin modificar archivos")
    parser.add_argument("--dry-run", action="store_true", help="Muestra archivos que cambiarían sin escribir")
    parser.add_argument("--tag", action="store_true", help="Ejecuta tests, hace commit y crea tag anotado")
    args = parser.parse_args()

    if args.check:
        return check_versions()
    if not args.version:
        parser.error("Debes indicar una versión o usar --check.")
    return bump_version(args.version, dry_run=args.dry_run, create_tag=args.tag)


if __name__ == "__main__":
    raise SystemExit(main())
