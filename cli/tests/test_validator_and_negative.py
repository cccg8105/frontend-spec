import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI_DIR = Path(__file__).resolve().parent.parent
if str(CLI_DIR) not in sys.path:
    sys.path.insert(0, str(CLI_DIR))

from frontend_spec.commands.check_cmd import run_check
from frontend_spec.commands.init_cmd import run_init
from frontend_spec.commands.new_req_cmd import run_new_req
from frontend_spec.validator.schema_validator import count_rolling_history_rows


class TestValidatorAndNegative(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_broken_links_missing_modify_and_minor_missing_uf(self):
        run_init(self.tmp, harness="antigravity")

        # 1. Enlace roto
        tech_idx = self.tmp / "docs" / "technical" / "index.md"
        tech_idx.write_text(tech_idx.read_text(encoding="utf-8") + "\n- [Roto](./fantasma.md)\n", encoding="utf-8")
        self.assertFalse(run_check(self.tmp))

        # 2. [MODIFY] inexistente y MINOR sin Referencia Funcional
        run_init(self.tmp, harness="antigravity", force=True)
        pending = self.tmp / "docs" / "backlog" / "pending.md"
        pending.write_text(
            pending.read_text(encoding="utf-8")
            + """
### [REQ-UI-CORE-001] Cambiar modal sin flujo funcional ni archivo
- **Prioridad:** P1
- **Tipo:** Feature (MINOR)
- **Versión Objetivo:** `v0.2.0`
- **Referencia Técnica:** `docs/technical/component-hierarchy.md`

#### Fronteras y Artefactos:
- **Artefactos a Modificar / Crear:**
  - `src/features/core/MissingModal.tsx` [MODIFY]
- **Restricciones:**
  - Ninguna

#### Criterios de Aceptación:
- [ ] Completar modal
""",
            encoding="utf-8",
        )
        self.assertFalse(run_check(self.tmp))

    def test_invalid_tokens_and_invalid_user_flow(self):
        run_init(self.tmp, harness="antigravity")

        tok_file = self.tmp / "docs" / "design" / "tokens-and-themes.md"
        orig_tok = tok_file.read_text(encoding="utf-8")
        tok_file.write_text(orig_tok.replace("#0F52BA", "not-a-hex"), encoding="utf-8")
        self.assertFalse(run_check(self.tmp))
        tok_file.write_text(orig_tok, encoding="utf-8")

        bad_uf = self.tmp / "docs" / "functional" / "user-flows" / "UF-BAD.md"
        bad_uf.write_text("# Flujo invalido sin frontmatter ni mermaid ni a11y\n", encoding="utf-8")
        self.assertFalse(run_check(self.tmp))

    def test_spec_json_sidecars_positive_negative_and_unknown(self):
        run_init(self.tmp, harness="antigravity")
        specs_dir = self.tmp / ".spec" / "specs"
        specs_dir.mkdir(parents=True, exist_ok=True)

        valid_stack = {
            "artifact_type": "tech-stack",
            "ecosystem": "react-vite",
            "core": {"framework": "React", "language": "TypeScript", "styling": "Tailwind CSS", "testing_framework": "Vitest"},
            "performance_budgets": {"lcp": "<= 2.5s", "inp": "<= 200ms", "cls": "<= 0.1", "bundle_max_kb": 200},
            "security_policies": {
                "xss": "Sin dangerouslySetInnerHTML",
                "token_storage": "Cookies HttpOnly",
                "csp": "default-src self",
            },
        }
        stack_json = specs_dir / "tech-stack.json"
        stack_json.write_text(json.dumps(valid_stack), encoding="utf-8")
        self.assertTrue(run_check(self.tmp))

        # Ecosistema invalido debe fallar schema
        bad_stack = dict(valid_stack, ecosystem="jquery-legacy")
        stack_json.write_text(json.dumps(bad_stack), encoding="utf-8")
        self.assertFalse(run_check(self.tmp))
        stack_json.unlink()

        # Archivo desconocido debe fallar en .spec/specs/
        (specs_dir / "unknown-contract.json").write_text("{}", encoding="utf-8")
        self.assertFalse(run_check(self.tmp))

    def test_rolling_window_count(self):
        sample = """
## Historial de Revisiones (Últimos Cambios)

| Versión | Fecha | Requerimiento | Resumen del Cambio |
| :--- | :--- | :--- | :--- |
| `v0.1.0` | 2026-11-01 | `REQ-1` | Uno |
| `v0.2.0` | 2026-11-02 | `REQ-2` | Dos |
| `v0.3.0` | 2026-11-03 | `REQ-3` | Tres |
| `v0.4.0` | 2026-11-04 | `REQ-4` | Cuatro |

> *Nota: Esta tabla mantiene una ventana deslizante.*
"""
        self.assertEqual(count_rolling_history_rows(sample), 4)

    def test_staged_phantom_commit_matrix(self):
        proj = self.tmp / "git-guarded"
        proj.mkdir()
        subprocess.run(["git", "init"], cwd=str(proj), check=True, capture_output=True)
        run_init(proj, harness="antigravity")

        # 1. Config raiz suelta sin REQ-UI-* se permite
        (proj / "vite.config.ts").write_text("export default {};\n", encoding="utf-8")
        subprocess.run(["git", "add", "vite.config.ts"], cwd=str(proj), check=True)
        self.assertTrue(run_check(proj, check_staged=True))

        # 2. Codigo fuente en src/ sin REQ-UI-* se bloquea
        ghost = proj / "src" / "features" / "core" / "GhostModal.tsx"
        ghost.parent.mkdir(parents=True, exist_ok=True)
        ghost.write_text("export const GhostModal = () => null;\n", encoding="utf-8")
        subprocess.run(["git", "add", "src/features/core/GhostModal.tsx"], cwd=str(proj), check=True)
        self.assertFalse(run_check(proj, check_staged=True))

        # 3. Registrar REQ-UI-* con otro archivo en fronteras -> bloqueo parcial
        req_other = run_new_req(proj, title="Otra tarjeta", domain="billing", impact="PATCH")
        self.assertEqual(req_other, "REQ-UI-BILLING-001")
        self.assertFalse(run_check(proj, check_staged=True))

        # 4. Registrar REQ-UI-* cuyo archivo coincide con stage -> permitido
        req_core = run_new_req(proj, title="Ghost modal", domain="core", impact="PATCH")
        self.assertEqual(req_core, "REQ-UI-CORE-001")
        self.assertTrue(run_check(proj, check_staged=True))

        # 5. Si docs/backlog/changelog.md esta en stage (cierre) -> permitido incluso sin pending activo
        (proj / "docs" / "backlog" / "pending.md").write_text("# Backlog\n\n## Milestone v0.2.0\n", encoding="utf-8")
        subprocess.run(["git", "add", "docs/backlog/changelog.md"], cwd=str(proj), check=True)
        self.assertTrue(run_check(proj, check_staged=True))

    def test_check_strict_tokens_detects_burned_hex(self):
        proj = self.tmp / "strict-ui"
        run_init(proj, harness="antigravity", ecosystem="solid", mode="greenfield")

        comp = proj / "src" / "components" / "Button.tsx"
        comp.parent.mkdir(parents=True, exist_ok=True)
        comp.write_text(
            'export const Button = () => <button style={{ backgroundColor: "#FF5733" }}>Enviar</button>;\n',
            encoding="utf-8",
        )

        # En modo opt-in: check normal aprueba, check --strict-tokens rechaza hex quemado
        self.assertTrue(run_check(proj, strict_tokens=False))
        self.assertFalse(run_check(proj, strict_tokens=True))

        # Reemplazar por variable semantica CSS y verificar via CLI --strict-tokens
        comp.write_text(
            'export const Button = () => <button style={{ backgroundColor: "var(--color-primary)" }}>Enviar</button>;\n',
            encoding="utf-8",
        )
        cli_main = Path(__file__).resolve().parent.parent / "main.py"
        proc_ok = subprocess.run(
            [sys.executable, str(cli_main), "check", "--dir", str(proj), "--strict-tokens"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc_ok.returncode, 0, proc_ok.stderr)

        # Un sidecar *.tokens.json malformado debe fallar en run_check
        bad_tokens = proj / ".spec" / "specs" / "broken.tokens.json"
        bad_tokens.parent.mkdir(parents=True, exist_ok=True)
        bad_tokens.write_text(
            json.dumps({"color": {"primary": {"$type": "color", "$value": "not-a-hex"}}}),
            encoding="utf-8",
        )
        self.assertFalse(run_check(proj))


if __name__ == "__main__":
    unittest.main()
