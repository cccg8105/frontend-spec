import datetime
import json
import re
from pathlib import Path
from typing import Optional, Tuple


def extract_version(manifest_path: Path, file_format: str = "json") -> Optional[str]:
    """Extrae la version actual desde package.json o archivo plain VERSION."""
    if not manifest_path.exists() or not manifest_path.is_file():
        return None

    content = manifest_path.read_text(encoding="utf-8")

    if file_format == "plain":
        for line in content.splitlines():
            cleaned = line.strip()
            if cleaned and not cleaned.startswith("#"):
                return cleaned.lstrip("vV")
        return None

    if file_format == "json":
        try:
            data = json.loads(content)
            val = data.get("version")
            return str(val).strip().lstrip("vV") if val else None
        except Exception:
            pass

    generic = re.search(r'version["\']?\s*[:=]\s*["\']([^"\']+)["\']', content, re.IGNORECASE)
    return generic.group(1).strip().lstrip("vV") if generic else None


def update_version(manifest_path: Path, file_format: str, new_version: str) -> bool:
    """Actualiza la version en package.json o VERSION preservando el formato."""
    clean_ver = new_version.strip().lstrip("vV")

    if file_format == "plain":
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(f"{clean_ver}\n", encoding="utf-8")
        return True

    if not manifest_path.exists():
        return False

    content = manifest_path.read_text(encoding="utf-8")

    if file_format == "json":
        try:
            data = json.loads(content)
            data["version"] = clean_ver
            manifest_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            return True
        except Exception:
            pass

    fallback = r'(version["\']?\s*[:=]\s*["\'])[^"\']+(["\'])'
    if re.search(fallback, content, re.IGNORECASE):
        updated = re.sub(
            fallback, rf"\g<1>{clean_ver}\g<2>", content, count=1, flags=re.IGNORECASE
        )
        manifest_path.write_text(updated, encoding="utf-8")
        return True

    return False


def parse_version_tuple(version_str: str) -> Tuple[int, ...]:
    """Convierte 'v1.2.3-rc1', '2026.11.1' o '3' en tupla numerica comparable."""
    cleaned = version_str.strip().lstrip("vV")
    core = re.split(r"[-+]", cleaned)[0]
    nums = re.findall(r"\d+", core)
    return tuple(int(n) for n in nums) if nums else (0,)


def compare_versions(v_new: str, v_current: str) -> int:
    """Retorna 1 si v_new > v_current, 0 si iguales, -1 si v_new < v_current."""
    t_new = parse_version_tuple(v_new)
    t_cur = parse_version_tuple(v_current)
    max_len = max(len(t_new), len(t_cur))
    pad_new = t_new + (0,) * (max_len - len(t_new))
    pad_cur = t_cur + (0,) * (max_len - len(t_cur))
    if pad_new > pad_cur:
        return 1
    if pad_new < pad_cur:
        return -1
    return 0


def compute_next_milestone(current_version: str, scheme: str = "semver") -> str:
    """Calcula el siguiente milestone segun estrategia semver, calver o sequential."""
    parts = parse_version_tuple(current_version)

    if scheme == "calver":
        today = datetime.date.today()
        if len(parts) >= 3 and parts[0] >= 2000 and parts[0] == today.year and parts[1] == today.month:
            return f"v{today.year}.{today.month:02d}.{parts[2] + 1}"
        return f"v{today.year}.{today.month:02d}.1"

    if scheme == "sequential":
        last = parts[-1] + 1
        prefix = ".".join(str(p) for p in parts[:-1])
        return f"v{prefix}.{last}" if prefix else f"v{last}"

    major = parts[0] if len(parts) >= 1 else 0
    minor = parts[1] if len(parts) >= 2 else 1
    return f"v{major}.{minor + 1}.0"
