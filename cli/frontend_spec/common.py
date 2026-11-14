import re
from pathlib import Path
from typing import Any, Dict, Tuple

HARNESS_NAMES: Tuple[str, ...] = ("antigravity", "cursor", "claude", "windsurf")

SCHEME_LABELS: Dict[str, str] = {
    "semver": "SemVer 2.0.0",
    "calver": "CalVer (YYYY.MM.MICRO)",
    "sequential": "Sequential Versioning",
}


def slugify(text: str) -> str:
    """Convierte un titulo libre en un slug ASCII compacto para rutas y archivos."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return slug[:40] if slug else "feature"


def render_placeholders(text: str, context: Dict[str, str]) -> str:
    """Sustituye placeholders {{KEY}} dentro de una plantilla sin requerir dependencias."""
    rendered = text
    for key, val in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", val)
    return rendered


def build_doc_context(
    project_name: str,
    profile: Dict[str, Any],
    current_version: str,
    milestone_version: str,
    versioning: str,
    today_iso: str,
    harness: str = "all",
) -> Dict[str, str]:
    """Construye el diccionario completo de placeholders para docs/ y .spec/config.yaml."""
    if harness == "antigravity":
        interview_trigger = "/grill-me"
    elif harness in ("claude", "cursor", "windsurf"):
        interview_trigger = "/ui-grill"
    else:
        interview_trigger = "/grill-me / /ui-grill"

    return {
        "PROJECT_NAME": project_name,
        "CURRENT_VERSION": current_version.lstrip("vV"),
        "MILESTONE_VERSION": milestone_version,
        "TODAY": today_iso,
        "ECOSYSTEM_NAME": profile.get("ecosystem", "react-vite"),
        "FRAMEWORK_NAME": profile.get("framework", "React"),
        "META_FRAMEWORK": profile.get("meta_framework", "Vite"),
        "LANGUAGE_NAME": profile.get("language", "TypeScript"),
        "RUNTIME_LABEL": profile.get("runtime_label", "React + Vite"),
        "PACKAGE_MANAGER": profile.get("package_manager", "npm"),
        "STYLING": profile.get("styling", "Tailwind CSS"),
        "UI_PRIMITIVES": profile.get("ui_primitives", "Primitivas Nativas / HTML Semantico"),
        "STATE_SERVER": profile.get("state_server", "TanStack Query"),
        "UNIT_TEST_RUNNER": profile.get("unit_test_runner", "Vitest"),
        "TESTING_LIBRARY": profile.get("testing_library", "@testing-library/react"),
        "E2E_RUNNER": profile.get("e2e_runner", "Playwright"),
        "SRC_DIR": profile.get("src_dir", "src"),
        "ROUTES_DIR": profile.get("routes_dir", "src/pages"),
        "TEST_PATTERN": profile.get("test_pattern", "tests/unit/{slug}.test.tsx"),
        "VERSIONING_SCHEME": versioning,
        "VERSIONING_SCHEME_LABEL": SCHEME_LABELS.get(versioning, versioning),
        "MANIFEST_FILE": profile.get("version_file", "package.json"),
        "HARNESS_INTERVIEW_TRIGGER": interview_trigger,
    }


def read_config_settings(project_root: Path) -> Dict[str, str]:
    """Lee campos clave desde .spec/config.yaml usando defaults seguros."""
    settings = {
        "ecosystem": "react-vite",
        "runtime_label": "React + Vite",
        "src_ext": ".tsx",
        "src_dir": "src",
        "routes_dir": "src/pages",
        "test_pattern": "tests/unit/{slug}.test.tsx",
        "current_version": "0.1.0",
        "current_milestone": "v0.2.0",
        "versioning_scheme": "semver",
        "manifest_path": "package.json",
        "manifest_format": "json",
    }
    cfg = project_root / ".spec" / "config.yaml"
    if not cfg.exists():
        return settings

    raw = cfg.read_text(encoding="utf-8")

    # Claves planas simples
    flat_map = (
        ("src_dir", "src_dir"),
        ("routes_dir", "routes_dir"),
        ("test_pattern", "test_pattern"),
        ("current_version", "current_version"),
        ("current_milestone", "current_milestone"),
        ("versioning_scheme", "versioning_scheme"),
    )
    for yaml_key, dst_key in flat_map:
        m = re.search(rf"^\s*{yaml_key}:\s*[\"']?([^\"'\r\n#]+)", raw, re.MULTILINE)
        if m:
            settings[dst_key] = m.group(1).strip().strip("\"'")

    # ecosystem.name y version_file.path / format
    m_eco = re.search(
        r"ecosystem:\s*(?:\r?\n\s+name:\s*[\"']?([^\"'\r\n#]+)|[\"']([^\"'\r\n#]+)[\"'])",
        raw,
    )
    if m_eco:
        val = (m_eco.group(1) or m_eco.group(2) or "").strip()
        if val and "{{" not in val:
            settings["ecosystem"] = val

    m_path = re.search(r"^\s*path:\s*[\"']?([^\"'\r\n#]+)", raw, re.MULTILINE)
    if m_path:
        settings["manifest_path"] = m_path.group(1).strip().strip("\"'")

    m_fmt = re.search(r"^\s*format:\s*[\"']?([^\"'\r\n#]+)", raw, re.MULTILINE)
    if m_fmt:
        settings["manifest_format"] = m_fmt.group(1).strip().strip("\"'")

    return settings
