import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

CLI_DIR = Path(__file__).resolve().parent.parent
if str(CLI_DIR) not in sys.path:
    sys.path.insert(0, str(CLI_DIR))

from frontend_spec.detector.ecosystem_detector import (
    build_profile_context,
    detect_frontend_ecosystem,
)


class TestEcosystemDetector(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_greenfield_detection(self):
        det = detect_frontend_ecosystem(self.tmp)
        self.assertEqual(det["mode"], "greenfield")
        self.assertEqual(det["project_state"], "empty")
        self.assertFalse(det["is_fresh_scaffold"])
        self.assertIsNone(det["detected"])
        empty_prof = build_profile_context(self.tmp, "nextjs")
        self.assertEqual(empty_prof["language"], "TypeScript")
        self.assertEqual(empty_prof["src_ext"], ".tsx")

    def test_fresh_scaffold_vs_real_brownfield(self):
        scaf = self.tmp / "fresh-vite"
        (scaf / "src").mkdir(parents=True)
        (scaf / "package.json").write_text(
            json.dumps({"name": "fresh-vite", "version": "0.0.0", "dependencies": {"react": "19.0.0"}, "devDependencies": {"vite": "6.0.0", "typescript": "5.7.0"}}),
            encoding="utf-8",
        )
        (scaf / "vite.config.ts").write_text("export default {};", encoding="utf-8")
        (scaf / "tsconfig.json").write_text("{}", encoding="utf-8")
        (scaf / "src" / "main.tsx").write_text("import './App';", encoding="utf-8")
        (scaf / "src" / "App.tsx").write_text("export function App() { return null; }", encoding="utf-8")

        det_scaf = detect_frontend_ecosystem(scaf)
        self.assertEqual(det_scaf["mode"], "brownfield")
        self.assertEqual(det_scaf["project_state"], "scaffold")
        self.assertTrue(det_scaf["is_fresh_scaffold"])
        self.assertEqual(det_scaf["detected"]["language"], "TypeScript")

        # Agregar carpeta de feature o test -> pasa a brownfield real
        (scaf / "src" / "features" / "billing").mkdir(parents=True)
        (scaf / "src" / "features" / "billing" / "InvoiceCard.tsx").write_text("export const InvoiceCard = () => null;", encoding="utf-8")
        det_real = detect_frontend_ecosystem(scaf)
        self.assertEqual(det_real["project_state"], "brownfield")
        self.assertFalse(det_real["is_fresh_scaffold"])

    def test_all_7_frontend_ecosystems(self):
        cases = [
            (
                "nextjs",
                {"dependencies": {"next": "15.0.0", "react": "19.0.0", "@tanstack/react-query": "5.0.0"}},
                ["next.config.mjs", "pnpm-lock.yaml", "components.json", "tsconfig.json", "tailwind.config.ts"],
                "pnpm",
                "TypeScript",
                "Tailwind CSS",
                "shadcn/ui + Radix",
                "TanStack Query",
            ),
            (
                "nuxt",
                {"dependencies": {"nuxt": "3.13.0", "vue": "3.5.0", "pinia": "2.2.0"}},
                ["nuxt.config.ts", "tsconfig.json"],
                "npm",
                "TypeScript",
                "CSS Custom Properties / CSS Modules",
                "Primitivas Nativas / HTML Semantico",
                "Nuxt useFetch / Pinia",
            ),
            (
                "sveltekit",
                {"devDependencies": {"@sveltejs/kit": "2.0.0", "vitest": "2.0.0"}},
                ["svelte.config.js", "bun.lockb"],
                "bun",
                "JavaScript",
                "CSS Custom Properties / CSS Modules",
                "Primitivas Nativas / HTML Semantico",
                "SvelteKit load() / Form Actions",
            ),
            (
                "astro",
                {"dependencies": {"astro": "4.15.0"}},
                ["astro.config.mjs", "yarn.lock", "tsconfig.json"],
                "yarn",
                "TypeScript",
                "CSS Custom Properties / CSS Modules",
                "Primitivas Nativas / HTML Semantico",
                "Astro Content Collections / fetch",
            ),
            (
                "angular",
                {"dependencies": {"@angular/core": "18.0.0", "@angular/material": "18.0.0"}},
                ["angular.json", "tsconfig.json"],
                "npm",
                "TypeScript",
                "CSS Custom Properties / CSS Modules",
                "Angular Material",
                "Angular HttpClient / RxJS Signals",
            ),
            (
                "vue-vite",
                {"dependencies": {"vue": "3.5.0"}, "devDependencies": {"vite": "5.4.0", "sass": "1.77.0"}},
                ["vite.config.ts", "tsconfig.json"],
                "npm",
                "TypeScript",
                "SCSS / CSS Modules",
                "Primitivas Nativas / HTML Semantico",
                "TanStack Vue Query / Pinia",
            ),
            (
                "react-vite",
                {"dependencies": {"react": "18.3.0"}, "devDependencies": {"vite": "5.4.0"}},
                ["vite.config.js"],
                "npm",
                "JavaScript",
                "CSS Custom Properties / CSS Modules",
                "Primitivas Nativas / HTML Semantico",
                "TanStack Query",
            ),
        ]

        for expected_eco, deps, files, exp_pm, exp_lang, exp_style, exp_ui, exp_state in cases:
            proj = self.tmp / expected_eco
            proj.mkdir()
            pkg = {"name": f"app-{expected_eco}", "version": "1.0.0", **deps}
            (proj / "package.json").write_text(json.dumps(pkg), encoding="utf-8")
            for fname in files:
                (proj / fname).write_text("", encoding="utf-8")

            det = detect_frontend_ecosystem(proj)
            self.assertEqual(det["mode"], "brownfield", expected_eco)
            prof = det["detected"]
            self.assertEqual(prof["ecosystem"], expected_eco)
            self.assertEqual(prof["package_manager"], exp_pm)
            self.assertEqual(prof["language"], exp_lang)
            self.assertEqual(prof["styling"], exp_style)
            self.assertEqual(prof["ui_primitives"], exp_ui)
            self.assertEqual(prof["state_server"], exp_state)

    def test_detect_new_ecosystems_remix_solid_qwik(self):
        extra_cases = [
            (
                "remix",
                {"dependencies": {"@remix-run/react": "2.14.0", "react": "18.3.0"}, "devDependencies": {"@storybook/react": "8.4.0"}},
                ["vite.config.ts", "tsconfig.json"],
                "Remix loader()/action() / URL SearchParams",
                True,
            ),
            (
                "solid",
                {"dependencies": {"solid-js": "1.9.0", "@solidjs/router": "0.14.0"}},
                ["vite.config.ts", "tsconfig.json"],
                "Solid Signals / createResource",
                False,
            ),
            (
                "qwik",
                {"dependencies": {"@builder.io/qwik": "1.9.0", "@builder.io/qwik-city": "1.9.0"}},
                ["vite.config.ts", "tsconfig.json"],
                "Qwik routeLoader$() / useSignal",
                False,
            ),
        ]

        for expected_eco, deps, files, exp_state, exp_storybook in extra_cases:
            proj = self.tmp / f"extra-{expected_eco}"
            proj.mkdir()
            pkg = {"name": f"app-{expected_eco}", "version": "1.0.0", **deps}
            (proj / "package.json").write_text(json.dumps(pkg), encoding="utf-8")
            for fname in files:
                (proj / fname).write_text("", encoding="utf-8")

            det = detect_frontend_ecosystem(proj)
            prof = det["detected"]
            self.assertEqual(prof["ecosystem"], expected_eco)
            self.assertEqual(prof["language"], "TypeScript")
            self.assertEqual(prof["state_server"], exp_state)
            self.assertEqual(prof["has_storybook"], exp_storybook)


if __name__ == "__main__":
    unittest.main()
