import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def locate_framework_asset(relative_path: str) -> Optional[Path]:
    """Localiza templates/, harnesses/ o schemas/ tanto en repo editable como en wheel instalado."""
    pkg_dir = Path(__file__).resolve().parent.parent
    candidates = [
        pkg_dir / relative_path,
        pkg_dir.parent.parent / relative_path,
    ]
    for cand in candidates:
        if cand.exists():
            return cand
    return None


def load_json_schema(schema_rel_path: str) -> Optional[Dict[str, Any]]:
    schemas_dir = locate_framework_asset("schemas")
    if not schemas_dir:
        return None
    target = schemas_dir / schema_rel_path
    if not target.exists():
        return None
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except Exception:
        return None


def _parse_scalar(raw: str) -> Any:
    val = raw.strip()
    if " #" in val and not (val.startswith('"') or val.startswith("'")):
        val = val.split(" #", 1)[0].strip()
    if (val.startswith('"') and val.endswith('"')) or (
        val.startswith("'") and val.endswith("'")
    ):
        return val[1:-1]
    low = val.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "~", ""):
        return None
    if re.fullmatch(r"-?\d+", val):
        return int(val)
    if re.fullmatch(r"-?\d+\.\d+", val):
        return float(val)
    return val


def parse_yaml_frontmatter(md_text: str) -> Tuple[Dict[str, Any], str, bool]:
    """Parsea cabecera YAML Frontmatter al inicio de un documento sin PyYAML."""
    clean_text = md_text.lstrip("\ufeff")
    match = re.match(
        r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|$)(.*)", clean_text, re.DOTALL
    )
    if not match:
        return {}, clean_text, False

    raw_yaml = match.group(1)
    body = match.group(2)
    data: Dict[str, Any] = {}
    current_key: Optional[str] = None
    current_type: Optional[str] = None

    for line in raw_yaml.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        list_match = re.match(r"^\s+-\s+(.+)$", line)
        if list_match and current_key and current_type == "list":
            data[current_key].append(_parse_scalar(list_match.group(1)))
            continue

        nested_kv = re.match(r"^\s{2,}([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if nested_kv and current_key and current_type == "dict":
            n_key = nested_kv.group(1)
            n_val = nested_kv.group(2).strip()
            data[current_key][n_key] = _parse_scalar(n_val) if n_val else ""
            continue

        kv_match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if kv_match:
            key = kv_match.group(1)
            val_part = kv_match.group(2).strip()
            if val_part == "":
                current_key = key
                current_type = None
                data[key] = []
            elif val_part.startswith("[") and val_part.endswith("]"):
                inner = val_part[1:-1].strip()
                data[key] = (
                    [_parse_scalar(x) for x in inner.split(",") if x.strip()]
                    if inner
                    else []
                )
                current_key = key
                current_type = "list"
            else:
                data[key] = _parse_scalar(val_part)
                current_key = key
                current_type = None
            continue

        if current_key and current_type is None and line.startswith("  "):
            if line.lstrip().startswith("- "):
                current_type = "list"
                data[current_key] = [_parse_scalar(line.lstrip()[2:])]
            elif ":" in line:
                current_type = "dict"
                data[current_key] = {}
                n_k, _, n_v = line.strip().partition(":")
                data[current_key][n_k.strip()] = _parse_scalar(n_v) if n_v.strip() else ""

    return data, body, True


def _check_json_type(val: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(val, dict)
    if expected_type == "array":
        return isinstance(val, list)
    if expected_type == "string":
        return isinstance(val, str)
    if expected_type == "boolean":
        return isinstance(val, bool)
    if expected_type == "integer":
        return isinstance(val, int) and not isinstance(val, bool)
    if expected_type == "number":
        return isinstance(val, (int, float)) and not isinstance(val, bool)
    return True


def validate_against_schema(
    data: Any, schema: Dict[str, Any], path: str = "$"
) -> List[str]:
    """Validador JSON Schema Draft-07 sin dependencias externas."""
    errors: List[str] = []

    expected_type = schema.get("type")
    if expected_type and not _check_json_type(data, expected_type):
        errors.append(
            f"{path}: se esperaba tipo '{expected_type}', se obtuvo '{type(data).__name__}'"
        )
        return errors

    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{path}: valor '{data}' no permitido; valores validos: {schema['enum']}")

    if isinstance(data, str):
        min_len = schema.get("minLength")
        if min_len is not None and len(data.strip()) < min_len:
            errors.append(f"{path}: longitud minima requerida {min_len} caracteres (actual: {len(data.strip())})")
        pat = schema.get("pattern")
        if pat and not re.search(pat, data):
            errors.append(f"{path}: '{data}' no cumple patron '{pat}'")

    if isinstance(data, dict):
        for req_key in schema.get("required", []):
            if req_key not in data or data[req_key] in (None, ""):
                errors.append(f"{path}.{req_key}: campo obligatorio ausente o vacio")

        props = schema.get("properties", {})
        for k, subschema in props.items():
            if k in data and data[k] is not None:
                errors.extend(validate_against_schema(data[k], subschema, f"{path}.{k}"))

    if isinstance(data, list) and "items" in schema:
        item_schema = schema["items"]
        for idx, item in enumerate(data):
            errors.extend(validate_against_schema(item, item_schema, f"{path}[{idx}]"))

    return errors


def _extract_markdown_table_rows(section_text: str) -> List[List[str]]:
    rows: List[List[str]] = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows[1:] if len(rows) > 1 else []


def extract_user_flow_data(md_text: str) -> Tuple[Dict[str, Any], bool]:
    """Extrae metadatos y secciones de un archivo UF-*.md para validar user-flow.schema.json."""
    fm, body, has_fm = parse_yaml_frontmatter(md_text)

    h1_match = re.search(r"^#\s+(UF-[A-Z0-9]+-[0-9]+)\s*:\s*(.+)$", body, re.MULTILINE)
    uf_id = fm.get("id") or (h1_match.group(1).strip() if h1_match else "")
    title = fm.get("title") or (h1_match.group(2).strip() if h1_match else "")

    dom_match = re.search(r"-\s*\*\*Dominio:\*\*\s*`?([^\n`]+)`?", body)
    actor_match = re.search(r"-\s*\*\*Actor Principal:\*\*\s*`?([^\n`]+)`?", body)
    route_match = re.search(r"-\s*\*\*Ruta de Entrada:\*\*\s*(?:`?(?:GET\s+)?(/[^`\s\n]+)`?)", body)
    mermaid_match = re.search(r"```mermaid\s*\r?\n(.*?)\r?\n```", body, re.DOTALL)

    inputs_list: List[Dict[str, Any]] = []
    inputs_sec = re.search(
        r"###\s*Eventos\s*/\s*Entradas del Usuario:(.*?)(?=###|\n---|\Z)",
        body,
        re.DOTALL,
    )
    if inputs_sec:
        for row in _extract_markdown_table_rows(inputs_sec.group(1)):
            if len(row) >= 3:
                req_flag = row[2].strip().lower() in ("sí", "si", "yes", "true")
                inputs_list.append(
                    {
                        "name": row[0].strip("` "),
                        "type": row[1].strip("` "),
                        "required": req_flag,
                        "validation": row[3].strip() if len(row) >= 4 else "",
                    }
                )

    outputs_list: List[Dict[str, str]] = []
    outputs_sec = re.search(
        r"###\s*Salidas Visuales y Efectos:(.*?)(?=###|\n---|\n##|\Z)",
        body,
        re.DOTALL,
    )
    if outputs_sec:
        for row in _extract_markdown_table_rows(outputs_sec.group(1)):
            if len(row) >= 3:
                outputs_list.append(
                    {
                        "element": row[0].strip("` "),
                        "condition": row[1].strip("` "),
                        "behavior": row[2].strip(),
                    }
                )

    states_list: List[Dict[str, str]] = []
    states_sec = re.search(
        r"##\s*(?:4\.\s*)?Matriz de Estados de Interfaz[^\n]*\n(.*?)(?=\n---|\n##|\Z)",
        body,
        re.DOTALL,
    )
    if states_sec:
        for row in _extract_markdown_table_rows(states_sec.group(1)):
            if len(row) >= 3:
                states_list.append(
                    {
                        "state": row[0].strip("*` "),
                        "trigger": row[1].strip(),
                        "feedback": row[2].strip(),
                        "recovery": row[3].strip() if len(row) >= 4 else "",
                    }
                )

    fm_a11y = fm.get("accessibility") if isinstance(fm.get("accessibility"), dict) else {}
    focus_m = re.search(r"-\s*\*\*Foco Inicial[^:]*:\*\*\s*(.+)", body)
    roles_m = re.search(r"-\s*\*\*Roles Semánticos:\*\*\s*(.+)", body)
    resp_m = re.search(r"-\s*\*\*Responsive:\*\*\s*(.+)", body)

    accessibility: Dict[str, str] = {
        "focus_management": str(
            fm_a11y.get("focus_management") or (focus_m.group(1).strip() if focus_m else "")
        ),
        "semantic_roles": str(
            fm_a11y.get("semantic_roles") or (roles_m.group(1).strip() if roles_m else "")
        ),
    }
    resp_val = fm_a11y.get("responsive_rules") or (resp_m.group(1).strip() if resp_m else "")
    if resp_val:
        accessibility["responsive_rules"] = str(resp_val)

    data: Dict[str, Any] = {
        "id": str(uf_id),
        "title": str(title),
        "domain": str(fm.get("domain") or (dom_match.group(1).strip() if dom_match else "")),
        "actor": str(fm.get("actor") or (actor_match.group(1).strip() if actor_match else "")),
        "route": str(fm.get("route") or (route_match.group(1).strip() if route_match else "")),
        "status": str(fm.get("status", "Activo")),
        "flow_diagram_mermaid": mermaid_match.group(1).strip() if mermaid_match else "",
        "ui_states": states_list,
        "accessibility": accessibility,
    }
    if "auth_required" in fm:
        data["auth_required"] = fm["auth_required"]
    if "fsm_required" in fm:
        data["fsm_required"] = fm["fsm_required"]
    if isinstance(fm.get("viewports"), list):
        data["viewports"] = [str(v) for v in fm["viewports"]]
    if inputs_list:
        data["user_inputs"] = inputs_list
    if outputs_list:
        data["visual_outputs"] = outputs_list

    return data, has_fm


def extract_requirement_data(full_req_block: str) -> Dict[str, Any]:
    """Convierte un bloque ### [REQ-UI-...] de pending.md al formato de requirement.schema.json."""
    header_match = re.search(r"###\s*\[(REQ-[^\]]+)\]\s*(.+)", full_req_block)
    req_id = header_match.group(1).strip() if header_match else ""
    title = header_match.group(2).strip() if header_match else ""

    prio_match = re.search(r"-\s*\*\*Prioridad:\*\*\s*(P[123])\b", full_req_block)
    priority = prio_match.group(1).strip() if prio_match else ""

    impact_match = re.search(r"-\s*\*\*Tipo:\*\*\s*([^\n]+)", full_req_block)
    raw_impact = impact_match.group(1).strip() if impact_match else ""
    imp_token = re.search(r"\b(MAJOR|MINOR|PATCH)\b", raw_impact)
    impact_type = imp_token.group(1).strip() if imp_token else ""
    track = "FAST_TRACK" if ("fast-track" in raw_impact.lower() or impact_type == "PATCH") else "FULL"

    ver_match = re.search(r"-\s*\*\*Versión Objetivo:\*\*\s*`?([^\n`]+)`?", full_req_block)
    target_version = ver_match.group(1).strip() if ver_match else ""

    func_ref_match = re.search(r"-\s*\*\*Referencia Funcional:\*\*\s*(.+)", full_req_block)
    func_ref = func_ref_match.group(1).strip().strip("` ") if func_ref_match else ""

    tech_ref_match = re.search(r"-\s*\*\*Referencia Técnica:\*\*\s*(.+)", full_req_block)
    tech_refs: List[str] = []
    if tech_ref_match:
        raw_tech = tech_ref_match.group(1)
        code_spans = re.findall(r"`([^`]+)`", raw_tech)
        if code_spans:
            tech_refs = [c.strip() for c in code_spans if c.strip()]
        else:
            tech_refs = [p.strip() for p in raw_tech.split(",") if p.strip()]

    tokens_consumed: List[str] = []
    tokens_match = re.search(r"-\s*\*\*Tokens Consumidos:\*\*\s*(.+)", full_req_block)
    if tokens_match:
        raw_tok = tokens_match.group(1).strip()
        spans = re.findall(r"`([^`]+)`", raw_tok)
        if spans:
            tokens_consumed = [s.strip() for s in spans if s.strip() and not s.strip().upper().startswith("N/A")]
        elif not raw_tok.upper().startswith("N/A"):
            tokens_consumed = [t.strip() for t in raw_tok.split(",") if t.strip()]

    artifacts: List[Dict[str, str]] = []
    for path_str, action_str in re.findall(
        r"-\s*`([^`]+)`\s*\[(NEW|MODIFY|DELETE)\]", full_req_block
    ):
        artifacts.append({"path": path_str.strip(), "action": action_str.strip()})

    restrictions: List[str] = []
    rest_sec = re.search(r"-\s*\*\*Restricciones:\*\*(.*?)(?=####|\Z)", full_req_block, re.DOTALL)
    if rest_sec:
        for line in rest_sec.group(1).splitlines():
            cleaned = line.strip()
            if cleaned.startswith("- "):
                restrictions.append(cleaned[2:].strip())
            elif cleaned:
                restrictions.append(cleaned)

    criteria: List[Dict[str, Any]] = []
    crit_sec = re.search(r"####\s*Criterios de Aceptación:(.*)", full_req_block, re.DOTALL)
    if crit_sec:
        for state_char, desc in re.findall(r"-\s*\[([ xX])\]\s*(.+)", crit_sec.group(1)):
            criteria.append(
                {
                    "description": desc.strip(),
                    "completed": state_char.lower() == "x",
                }
            )

    payload: Dict[str, Any] = {
        "id": req_id,
        "title": title,
        "priority": priority,
        "impact_type": impact_type,
        "track": track,
        "target_version": target_version,
        "references": {
            "functional": func_ref,
            "technical": tech_refs,
        },
        "boundaries": {
            "artifacts": artifacts,
            "restrictions": restrictions,
        },
        "acceptance_criteria": criteria,
    }
    if tokens_consumed:
        payload["tokens_consumed"] = tokens_consumed
    return payload


def extract_design_tokens_summary(md_text: str) -> Dict[str, Any]:
    """Extrae frontmatter y tabla de colores semanticos de tokens-and-themes.md."""
    fm, body, has_fm = parse_yaml_frontmatter(md_text)
    colors: List[Dict[str, str]] = []
    color_sec = re.search(
        r"##\s*(?:1\.\s*)?Colores Semánticos[^\n]*\n(.*?)(?=\n---|\n##|\Z)",
        body,
        re.DOTALL,
    )
    if color_sec:
        for row in _extract_markdown_table_rows(color_sec.group(1)):
            if len(row) >= 4:
                colors.append(
                    {
                        "token": row[0].strip("` "),
                        "light_hex": row[1].strip("` "),
                        "dark_hex": row[2].strip("` "),
                        "role": row[3].strip(),
                    }
                )

    disp_m = re.search(r"-\s*\*\*Display\s*/\s*UI:\*\*\s*(.+)", body)
    mono_m = re.search(r"-\s*\*\*Monospace:\*\*\s*(.+)", body)
    return {
        "has_fm": has_fm,
        "artifact_type": str(fm.get("artifact_type", "")),
        "theme_modes": fm.get("theme_modes") if isinstance(fm.get("theme_modes"), list) else [],
        "semantic_colors": colors,
        "display_font": disp_m.group(1).strip() if disp_m else "",
        "mono_font": mono_m.group(1).strip() if mono_m else "",
    }


def count_rolling_history_rows(md_text: str) -> int:
    """Cuenta las filas de datos en '## Historial de Revisiones' (limite Rolling Window: 3)."""
    match = re.search(
        r"##\s*Historial de Revisiones.*?\n(.*?)(?=\n##\s|\n>\s*\*Nota:|\Z)",
        md_text,
        re.DOTALL,
    )
    if not match:
        return 0
    return len(_extract_markdown_table_rows(match.group(1)))
