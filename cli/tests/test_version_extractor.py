import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

CLI_DIR = Path(__file__).resolve().parent.parent
if str(CLI_DIR) not in sys.path:
    sys.path.insert(0, str(CLI_DIR))

from frontend_spec.commands.init_cmd import run_init
from frontend_spec.commands.new_req_cmd import run_new_req
from frontend_spec.commands.resolve_cmd import run_resolve
from frontend_spec.detector.version_extractor import (
    compare_versions,
    compute_next_milestone,
    extract_version,
    update_version,
)


class TestVersionExtractor(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_extract_compare_update_across_formats(self):
        pkg = self.tmp / "package.json"
        pkg.write_text('{\n  "name": "web-app",\n  "version": "1.2.0"\n}\n', encoding="utf-8")
        self.assertEqual(extract_version(pkg, "json"), "1.2.0")
        self.assertEqual(compare_versions("1.3.0", "1.2.0"), 1)
        self.assertEqual(compare_versions("1.1.9", "1.2.0"), -1)
        self.assertEqual(compare_versions("1.2.0", "1.2.0"), 0)
        self.assertTrue(update_version(pkg, "json", "1.3.0"))
        self.assertEqual(extract_version(pkg, "json"), "1.3.0")

        yaml_cfg = self.tmp / "config.yaml"
        yaml_cfg.write_text('current_version: "0.4.0"\n', encoding="utf-8")
        self.assertEqual(extract_version(yaml_cfg, "yaml"), "0.4.0")
        self.assertTrue(update_version(yaml_cfg, "yaml", "0.5.0"))
        self.assertEqual(extract_version(yaml_cfg, "yaml"), "0.5.0")

        plain_ver = self.tmp / "VERSION"
        plain_ver.write_text("v5\n", encoding="utf-8")
        self.assertEqual(extract_version(plain_ver, "plain"), "5")
        self.assertTrue(update_version(plain_ver, "plain", "6"))
        self.assertEqual(extract_version(plain_ver, "plain"), "6")

    def test_milestones_semver_calver_sequential(self):
        self.assertEqual(compute_next_milestone("1.3.0", "semver"), "v1.4.0")
        self.assertEqual(compute_next_milestone("5", "sequential"), "v6")
        cal = compute_next_milestone("0.1.0", "calver")
        self.assertRegex(cal, r"^v\d{4}\.\d{2}\.\d+$")

    def test_anti_downgrade_guard_and_force_override(self):
        (self.tmp / "package.json").write_text(
            json.dumps({"name": "shop", "version": "2.4.0"}),
            encoding="utf-8",
        )
        run_init(self.tmp, harness="antigravity")

        req_blocked = run_new_req(
            self.tmp,
            title="Hotfix de contraste menor",
            domain="core",
            impact="PATCH",
            target_version="v0.9.0",
        )
        self.assertTrue(run_resolve(self.tmp, req_blocked, auto_bump=True, force_version=False))
        self.assertEqual(extract_version(self.tmp / "package.json", "json"), "2.4.0")

        req_forced = run_new_req(
            self.tmp,
            title="Forzar rollback controlado",
            domain="core",
            impact="PATCH",
            target_version="v1.0.0",
        )
        self.assertTrue(run_resolve(self.tmp, req_forced, auto_bump=True, force_version=True))
        self.assertEqual(extract_version(self.tmp / "package.json", "json"), "1.0.0")


if __name__ == "__main__":
    unittest.main()
