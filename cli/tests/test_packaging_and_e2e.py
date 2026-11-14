import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLI_MAIN = REPO_ROOT / "cli" / "main.py"
if str(REPO_ROOT / "cli") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "cli"))

from frontend_spec import __version__
from frontend_spec.commands.check_cmd import run_check


class TestPackagingAndE2E(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_cli_subprocess_exit_codes_and_version(self):
        ver = subprocess.run(
            [sys.executable, str(CLI_MAIN), "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(ver.returncode, 0)
        self.assertIn(__version__, ver.stdout)

        # check sin init -> exit code 1
        fail_chk = subprocess.run(
            [sys.executable, str(CLI_MAIN), "check", "--dir", str(self.tmp)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(fail_chk.returncode, 1)

        # init -> req:new sin titulo -> resolve inexistente
        ok_init = subprocess.run(
            [sys.executable, str(CLI_MAIN), "init", "--dir", str(self.tmp), "--harness", "antigravity"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(ok_init.returncode, 0)

        bad_req = subprocess.run(
            [sys.executable, str(CLI_MAIN), "req:new", "--dir", str(self.tmp)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(bad_req.returncode, 1)

        bad_res = subprocess.run(
            [sys.executable, str(CLI_MAIN), "resolve", "REQ-UI-NONE-999", "--dir", str(self.tmp)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(bad_res.returncode, 1)

    def test_pilot_project_sample_dashboard_ui_passes_check(self):
        pilot_dir = REPO_ROOT / "examples" / "sample-dashboard-ui"
        self.assertTrue(pilot_dir.is_dir(), "Falta el proyecto piloto examples/sample-dashboard-ui")
        self.assertTrue((pilot_dir / ".spec" / "bootstrap-report.md").exists())
        self.assertTrue(run_check(pilot_dir))

    def test_installed_wheel_layout_resolves_bundled_assets(self):
        pkg_root = self.tmp / "site_pkg" / "frontend_spec"
        shutil.copytree(REPO_ROOT / "cli" / "frontend_spec", pkg_root)
        shutil.copytree(REPO_ROOT / "templates", pkg_root / "templates")
        shutil.copytree(REPO_ROOT / "harnesses", pkg_root / "harnesses")
        shutil.copytree(REPO_ROOT / "schemas", pkg_root / "schemas")

        target = self.tmp / "consumer"
        res = subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys; sys.path.insert(0, sys.argv[1]); from frontend_spec.__main__ import main; sys.argv=['frontend-spec', 'init', '--dir', sys.argv[2], '--harness', 'antigravity']; main()",
                str(self.tmp / "site_pkg"),
                str(target),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertTrue((target / ".spec" / "config.yaml").exists())
        self.assertTrue((target / ".gemini" / "skills" / "frontend-spec" / "SKILL.md").exists())
        self.assertTrue(run_check(target))


if __name__ == "__main__":
    unittest.main()
