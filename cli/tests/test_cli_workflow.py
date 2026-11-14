import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI_DIR = Path(__file__).resolve().parent.parent
CLI_MAIN = CLI_DIR / "main.py"
if str(CLI_DIR) not in sys.path:
    sys.path.insert(0, str(CLI_DIR))

from frontend_spec.commands.check_cmd import run_check
from frontend_spec.commands.init_cmd import run_init
from frontend_spec.commands.new_req_cmd import run_new_req
from frontend_spec.commands.resolve_cmd import run_resolve
from frontend_spec.commands.sync_index_cmd import run_sync_index
from frontend_spec.detector.version_extractor import extract_version


class TestCLIWorkflow(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_full_lifecycle_and_harness_parity(self):
        proj = self.tmp / "next-shop"
        proj.mkdir()
        (proj / "package.json").write_text(
            json.dumps({"name": "next-shop", "version": "1.0.0", "dependencies": {"next": "15.0.0", "react": "19.0.0"}}),
            encoding="utf-8",
        )
        (proj / "tsconfig.json").write_text("{}", encoding="utf-8")
        (proj / "next.config.mjs").write_text("export default {};", encoding="utf-8")

        run_init(proj, harness="all", versioning="semver")

        # Cero placeholders residuales en docs, config.yaml ni skills instaladas
        check_files = [proj / ".spec" / "config.yaml", *(proj / "docs").rglob("*.md")]
        for sk_dir in (".gemini/skills", ".claude/skills", ".cursor/skills", ".windsurf/skills"):
            check_files.extend((proj / sk_dir).rglob("SKILL.md"))
        for p in check_files:
            txt = p.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"\{\{[A-Z0-9_]+\}\}", txt), f"Placeholder residual en {p}")

        # Paridad multi-harness: Antigravity omite ui-grill y usa /grill-me; los otros 3 instalan ui-grill
        self.assertFalse((proj / ".gemini" / "skills" / "ui-grill").exists())
        self.assertIn("/grill-me", (proj / ".gemini" / "skills" / "frontend-spec" / "SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("AskUserQuestion", (proj / ".claude" / "skills" / "ui-grill" / "SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("AskQuestion", (proj / ".cursor" / "skills" / "ui-grill" / "SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("A) (Recomendado)", (proj / ".windsurf" / "skills" / "ui-grill" / "SKILL.md").read_text(encoding="utf-8"))

        self.assertTrue(run_check(proj))

        # Fast-Track PATCH sin bump
        req1 = run_new_req(proj, title="Fix focus ring on search input", domain="core", impact="PATCH")
        self.assertEqual(req1, "REQ-UI-CORE-001")
        self.assertIn("`REQ-UI-CORE-001`", (proj / "docs" / "backlog" / "index.md").read_text(encoding="utf-8"))
        self.assertTrue(run_check(proj))
        self.assertTrue(run_resolve(proj, "REQ-UI-CORE-001", auto_bump=False))
        self.assertEqual(extract_version(proj / "package.json", "json"), "1.0.0")

        # Carril Completo MINOR: falla hasta crear UF-AUTH-001 valido
        req2 = run_new_req(
            proj,
            title="Login con validacion accesible",
            domain="auth",
            priority="P1",
            impact="MINOR",
            target_version="v1.1.0",
            uf_ref="docs/functional/user-flows/UF-AUTH-001-login.md",
            tokens="color-surface, color-primary",
        )
        self.assertEqual(req2, "REQ-UI-AUTH-001")
        self.assertFalse(run_check(proj))

        uf_path = proj / "docs" / "functional" / "user-flows" / "UF-AUTH-001-login.md"
        uf_path.write_text(
            """---
id: UF-AUTH-001
title: "Inicio de sesion accesible"
domain: "auth"
actor: "Usuario Final"
route: "/login"
status: "Activo"
auth_required: false
fsm_required: true
viewports:
  - mobile
  - desktop
---

# UF-AUTH-001: Inicio de sesion accesible

## 2. Diagrama del Flujo de Interaccion (Mermaid)
```mermaid
flowchart TD
    A --> B
```

## 4. Matriz de Estados de Interfaz y Casos Borde

| Estado UI | Condicion de Disparo | Que ve el usuario | Accion / Recuperacion |
| :--- | :--- | :--- | :--- |
| **Loading** | Submit | Spinner en boton | Esperar respuesta |

## 6. Accesibilidad (WCAG 2.1 AA) y Responsive
- **Foco Inicial y Teclado:** Foco automatico en campo email al montar vista.
- **Roles Semánticos:** Uso de main, form y role=alert en errores de validacion.
- **Responsive:** Formulario centrado a una columna en 390px sin overflow horizontal.
""",
            encoding="utf-8",
        )
        self.assertTrue(run_check(proj))
        self.assertTrue(run_resolve(proj, "REQ-UI-AUTH-001", auto_bump=True))
        self.assertEqual(extract_version(proj / "package.json", "json"), "1.1.0")
        reqs_count, ufs_count = run_sync_index(proj)
        self.assertEqual(reqs_count, 0)
        self.assertEqual(ufs_count, 1)

    def test_calver_and_sequential_init(self):
        cal_dir = self.tmp / "cal-app"
        run_init(cal_dir, harness="antigravity", versioning="calver")
        cfg_txt = (cal_dir / ".spec" / "config.yaml").read_text(encoding="utf-8")
        self.assertIn('versioning_scheme: "calver"', cfg_txt)
        self.assertTrue(run_check(cal_dir))

        seq_dir = self.tmp / "seq-app"
        run_init(seq_dir, harness="claude", versioning="sequential")
        seq_cfg = (seq_dir / ".spec" / "config.yaml").read_text(encoding="utf-8")
        self.assertIn('versioning_scheme: "sequential"', seq_cfg)
        self.assertTrue(run_check(seq_dir))

    def test_init_empty_with_ecosystem_and_mode_flags(self):
        svelte_dir = self.tmp / "empty-svelte"
        run_init(
            svelte_dir,
            harness="antigravity",
            ecosystem="sveltekit",
            mode="greenfield",
        )
        cfg_txt = (svelte_dir / ".spec" / "config.yaml").read_text(encoding="utf-8")
        self.assertIn('name: "sveltekit"', cfg_txt)
        self.assertIn('language: "TypeScript"', cfg_txt)
        self.assertIn('routes_dir: "src/routes"', cfg_txt)
        self.assertTrue(run_check(svelte_dir))

        # Ejecucion por subproceso con --ecosystem y --mode en directorio vacio
        astro_dir = self.tmp / "empty-astro"
        astro_dir.mkdir()
        proc = subprocess.run(
            [
                sys.executable,
                str(CLI_MAIN),
                "init",
                "--dir",
                str(astro_dir),
                "--ecosystem",
                "astro",
                "--mode",
                "greenfield",
                "--harness",
                "claude",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("--refresh-stack", proc.stdout)
        astro_cfg = (astro_dir / ".spec" / "config.yaml").read_text(encoding="utf-8")
        self.assertIn('name: "astro"', astro_cfg)
        self.assertIn('language: "TypeScript"', astro_cfg)

        # Scaffold inicial via subproceso sugiere Kickoff REQ-UI-CORE-001 y NO bootstrap
        scaf_dir = self.tmp / "vite-scaf"
        (scaf_dir / "src").mkdir(parents=True)
        (scaf_dir / "package.json").write_text(
            json.dumps({"name": "vite-scaf", "version": "0.0.0", "dependencies": {"react": "19.0.0"}}),
            encoding="utf-8",
        )
        (scaf_dir / "tsconfig.json").write_text("{}", encoding="utf-8")
        (scaf_dir / "vite.config.ts").write_text("export default {};", encoding="utf-8")
        (scaf_dir / "src" / "App.tsx").write_text("export default function App(){return null;}", encoding="utf-8")
        proc_scaf = subprocess.run(
            [sys.executable, str(CLI_MAIN), "init", "--dir", str(scaf_dir), "--harness", "antigravity"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc_scaf.returncode, 0, proc_scaf.stderr)
        self.assertIn("Scaffold inicial detectado", proc_scaf.stdout)
        self.assertNotIn("ejecuta 'frontend-spec bootstrap'", proc_scaf.stdout)


if __name__ == "__main__":
    unittest.main()
