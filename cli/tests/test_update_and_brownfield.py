import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

CLI_DIR = Path(__file__).resolve().parent.parent
if str(CLI_DIR) not in sys.path:
    sys.path.insert(0, str(CLI_DIR))

from frontend_spec.commands.bootstrap_cmd import run_bootstrap
from frontend_spec.commands.check_cmd import run_check
from frontend_spec.commands.init_cmd import run_init
from frontend_spec.commands.new_req_cmd import run_new_req
from frontend_spec.commands.update_cmd import run_update


class TestUpdateAndBrownfield(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_brownfield_bootstrap_gps_reset_and_audit_promotion(self):
        proj = self.tmp / "vue-legacy"
        (proj / "src" / "pages").mkdir(parents=True)
        (proj / "src" / "features" / "checkout").mkdir(parents=True)
        (proj / "src" / "styles").mkdir(parents=True)
        (proj / "tests" / "unit").mkdir(parents=True)
        (proj / "graphify-out").mkdir(parents=True)

        (proj / "package.json").write_text(
            json.dumps({"name": "vue-legacy", "version": "0.5.0", "dependencies": {"vue": "3.4.0"}, "devDependencies": {"vite": "5.0.0"}}),
            encoding="utf-8",
        )
        (proj / "src" / "pages" / "BillingPage.vue").write_text("<template><div/></template>", encoding="utf-8")
        (proj / "src" / "features" / "checkout" / "CheckoutForm.vue").write_text("<template><form/></template>", encoding="utf-8")
        (proj / "src" / "styles" / "tokens.css").write_text(":root {}", encoding="utf-8")
        (proj / "tests" / "unit" / "checkout.spec.ts").write_text("test('ok', () => {})", encoding="utf-8")
        (proj / "graphify-out" / "graph.json").write_text(
            json.dumps(
                {
                    "nodes": [{"id": "n1", "label": "CheckoutForm.vue"}, {"id": "n2", "label": "BillingPage.vue"}],
                    "links": [{"source": "n1", "target": "n2"}],
                }
            ),
            encoding="utf-8",
        )

        run_init(proj, harness="claude")
        report_path = run_bootstrap(proj, mode="auto")
        report_txt = report_path.read_text(encoding="utf-8")
        self.assertIn("Vue + Vite", report_txt)
        self.assertIn("CheckoutForm.vue", report_txt)
        self.assertIn("`checkout`", (proj / "docs" / "functional" / "index.md").read_text(encoding="utf-8"))

        # Preservar casilla marcada y limpiar con --reset
        checked = report_txt.replace(
            "- [ ] Documentar paleta real claro/oscuro, tipografias y Tailwind/CSS en docs/design/tokens-and-themes.md",
            "- [x] Documentar paleta real claro/oscuro, tipografias y Tailwind/CSS en docs/design/tokens-and-themes.md",
        )
        report_path.write_text(checked, encoding="utf-8")
        run_bootstrap(proj, mode="auto", reset=False)
        self.assertIn(
            "- [x] Documentar paleta real claro/oscuro, tipografias y Tailwind/CSS en docs/design/tokens-and-themes.md",
            report_path.read_text(encoding="utf-8"),
        )
        run_bootstrap(proj, mode="auto", reset=True)
        self.assertNotIn(
            "- [x] Documentar paleta real claro/oscuro, tipografias y Tailwind/CSS en docs/design/tokens-and-themes.md",
            report_path.read_text(encoding="utf-8"),
        )

        # Promocion valida y error ante AUDIT inexistente
        self.assertIsNone(run_new_req(proj, from_audit="AUDIT-UI-NO-EXISTE"))

        audit_file = proj / "docs" / "backlog" / "audit-proposals.md"
        audit_file.write_text(
            audit_file.read_text(encoding="utf-8")
            + """

### [AUDIT-UI-CHECKOUT-001] Contraste insuficiente en boton de pago
- **Dominio:** `checkout`
- **Categoría:** Accesibilidad (WCAG)
- **Severidad Sugerida:** P1
- **Impacto Estimado:** PATCH
- **Evidencia en Código:** `src/features/checkout/CheckoutForm.vue:12`
- **Estado:** Propuesto
""",
            encoding="utf-8",
        )
        promoted_id = run_new_req(proj, from_audit="AUDIT-UI-CHECKOUT-001")
        self.assertEqual(promoted_id, "REQ-UI-CHECKOUT-001")
        self.assertIn("`src/features/checkout/CheckoutForm.vue` [MODIFY]", (proj / "docs" / "backlog" / "pending.md").read_text(encoding="utf-8"))
        self.assertIn("Promovido a REQ-UI-CHECKOUT-001", audit_file.read_text(encoding="utf-8"))

    def test_monorepo_coexistence_update_protects_live_docs_and_dry_run(self):
        proj = self.tmp / "monorepo"
        (proj / ".git" / "hooks").mkdir(parents=True)
        (proj / ".claude" / "commands").mkdir(parents=True)
        (proj / "CLAUDE.md").write_text(
            "<!-- BACKEND-SPEC:START -->\n# Backend Rules\n<!-- BACKEND-SPEC:END -->\n",
            encoding="utf-8",
        )
        (proj / ".windsurfrules").write_text(
            "<!-- BACKEND-SPEC:START -->\n# Backend Windsurf\n<!-- BACKEND-SPEC:END -->\n",
            encoding="utf-8",
        )
        (proj / ".claude" / "commands" / "spec-plan.md").write_text("# Backend Plan", encoding="utf-8")
        (proj / ".git" / "hooks" / "pre-commit").write_text(
            "#!/usr/bin/env sh\n# BACKEND-SPEC:START\necho backend\n# BACKEND-SPEC:END\nexit 0\n",
            encoding="utf-8",
        )

        run_init(proj, harness="all")

        # Personalizar doc vivo y desactualizar plantilla en .spec/templates/
        custom_comp_doc = "---\nartifact_type: component-hierarchy\n---\n# Catalogo Custom Vivo\n"
        comp_path = proj / "docs" / "technical" / "component-hierarchy.md"
        comp_path.write_text(custom_comp_doc, encoding="utf-8")
        bp_path = proj / ".spec" / "templates" / "_template_user_flow.md"
        bp_path.write_text("# Plantilla obsoleta", encoding="utf-8")

        claude_txt = (proj / "CLAUDE.md").read_text(encoding="utf-8")
        (proj / "CLAUDE.md").write_text(claude_txt + "\n# My Custom Note\n", encoding="utf-8")
        before = (proj / "CLAUDE.md").read_text(encoding="utf-8")

        # Dry run no escribe en disco
        self.assertTrue(run_update(proj, harness="claude", dry_run=True))
        self.assertEqual((proj / "CLAUDE.md").read_text(encoding="utf-8"), before)
        self.assertEqual(bp_path.read_text(encoding="utf-8"), "# Plantilla obsoleta")

        # Update real refresca blueprints y bloques sin tocar docs/ existentes
        self.assertTrue(run_update(proj, harness="claude", dry_run=False))
        self.assertEqual(comp_path.read_text(encoding="utf-8"), custom_comp_doc)
        self.assertIn("UF-[DOMINIO]-[NUM]", bp_path.read_text(encoding="utf-8"))

        after = (proj / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("# My Custom Note", after)
        self.assertIn("<!-- BACKEND-SPEC:START -->", after)
        self.assertIn("<!-- FRONTEND-SPEC:START -->", after)
        self.assertTrue((proj / ".claude" / "commands" / "spec-plan.md").exists())
        self.assertTrue((proj / ".claude" / "commands" / "ui-plan.md").exists())
        self.assertTrue(run_check(proj))


if __name__ == "__main__":
    unittest.main()
