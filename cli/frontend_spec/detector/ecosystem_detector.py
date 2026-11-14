import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ECOSYSTEM_PROFILES: List[Dict[str, str]] = [
    {
        "ecosystem": "nextjs",
        "runtime_label": "Next.js (React)",
        "framework": "React",
        "meta_framework": "Next.js",
        "manifest": "package.json",
        "version_file": "package.json",
        "format": "json",
        "field": "version",
        "src_ext": ".tsx",
        "src_dir": "src",
        "routes_dir": "src/app",
        "default_state_server": "TanStack Query / React Server Components",
        "default_testing_lib": "@testing-library/react",
        "test_pattern": "tests/unit/{slug}.test.tsx",
    },
    {
        "ecosystem": "remix",
        "runtime_label": "Remix (React Router v7)",
        "framework": "React",
        "meta_framework": "Remix",
        "manifest": "package.json",
        "version_file": "package.json",
        "format": "json",
        "field": "version",
        "src_ext": ".tsx",
        "src_dir": "app",
        "routes_dir": "app/routes",
        "default_state_server": "Remix loader()/action() / URL SearchParams",
        "default_testing_lib": "@testing-library/react",
        "test_pattern": "tests/unit/{slug}.test.tsx",
    },
    {
        "ecosystem": "nuxt",
        "runtime_label": "Nuxt (Vue)",
        "framework": "Vue",
        "meta_framework": "Nuxt",
        "manifest": "package.json",
        "version_file": "package.json",
        "format": "json",
        "field": "version",
        "src_ext": ".vue",
        "src_dir": "app",
        "routes_dir": "app/pages",
        "default_state_server": "Nuxt useFetch / Pinia",
        "default_testing_lib": "@testing-library/vue",
        "test_pattern": "tests/unit/{slug}.spec.ts",
    },
    {
        "ecosystem": "sveltekit",
        "runtime_label": "SvelteKit",
        "framework": "Svelte",
        "meta_framework": "SvelteKit",
        "manifest": "package.json",
        "version_file": "package.json",
        "format": "json",
        "field": "version",
        "src_ext": ".svelte",
        "src_dir": "src",
        "routes_dir": "src/routes",
        "default_state_server": "SvelteKit load() / Form Actions",
        "default_testing_lib": "@testing-library/svelte",
        "test_pattern": "tests/unit/{slug}.spec.ts",
    },
    {
        "ecosystem": "solid",
        "runtime_label": "SolidJS (SolidStart / Vite)",
        "framework": "SolidJS",
        "meta_framework": "SolidStart / Vite",
        "manifest": "package.json",
        "version_file": "package.json",
        "format": "json",
        "field": "version",
        "src_ext": ".tsx",
        "src_dir": "src",
        "routes_dir": "src/routes",
        "default_state_server": "Solid Signals / createResource",
        "default_testing_lib": "@solidjs/testing-library",
        "test_pattern": "tests/unit/{slug}.test.tsx",
    },
    {
        "ecosystem": "qwik",
        "runtime_label": "Qwik (Qwik City)",
        "framework": "Qwik",
        "meta_framework": "Qwik City",
        "manifest": "package.json",
        "version_file": "package.json",
        "format": "json",
        "field": "version",
        "src_ext": ".tsx",
        "src_dir": "src",
        "routes_dir": "src/routes",
        "default_state_server": "Qwik routeLoader$() / useSignal",
        "default_testing_lib": "@builder.io/qwik/testing",
        "test_pattern": "tests/unit/{slug}.test.tsx",
    },
    {
        "ecosystem": "astro",
        "runtime_label": "Astro",
        "framework": "Astro",
        "meta_framework": "Astro",
        "manifest": "package.json",
        "version_file": "package.json",
        "format": "json",
        "field": "version",
        "src_ext": ".astro",
        "src_dir": "src",
        "routes_dir": "src/pages",
        "default_state_server": "Astro Content Collections / fetch",
        "default_testing_lib": "Testing Library / Playwright",
        "test_pattern": "tests/unit/{slug}.spec.ts",
    },
    {
        "ecosystem": "angular",
        "runtime_label": "Angular",
        "framework": "Angular",
        "meta_framework": "Angular CLI",
        "manifest": "package.json",
        "version_file": "package.json",
        "format": "json",
        "field": "version",
        "src_ext": ".component.ts",
        "src_dir": "src",
        "routes_dir": "src/app",
        "default_state_server": "Angular HttpClient / RxJS Signals",
        "default_testing_lib": "@testing-library/angular",
        "test_pattern": "src/app/{domain}/{slug}.component.spec.ts",
    },
    {
        "ecosystem": "vue-vite",
        "runtime_label": "Vue + Vite",
        "framework": "Vue",
        "meta_framework": "Vite",
        "manifest": "package.json",
        "version_file": "package.json",
        "format": "json",
        "field": "version",
        "src_ext": ".vue",
        "src_dir": "src",
        "routes_dir": "src/pages",
        "default_state_server": "TanStack Vue Query / Pinia",
        "default_testing_lib": "@testing-library/vue",
        "test_pattern": "tests/unit/{slug}.spec.ts",
    },
    {
        "ecosystem": "react-vite",
        "runtime_label": "React + Vite",
        "framework": "React",
        "meta_framework": "Vite",
        "manifest": "package.json",
        "version_file": "package.json",
        "format": "json",
        "field": "version",
        "src_ext": ".tsx",
        "src_dir": "src",
        "routes_dir": "src/pages",
        "default_state_server": "TanStack Query",
        "default_testing_lib": "@testing-library/react",
        "test_pattern": "tests/unit/{slug}.test.tsx",
    },
]

_PROFILE_MAP: Dict[str, Dict[str, str]] = {
    p["ecosystem"]: p for p in ECOSYSTEM_PROFILES
}

IGNORED_SCAFFOLD_ENTRIES = {
    ".git",
    ".spec",
    "docs",
    "graphify-out",
    ".gitignore",
    ".graphifyignore",
    ".githooks",
    ".gemini",
    ".cursor",
    ".claude",
    ".windsurf",
    "CLAUDE.md",
    ".windsurfrules",
}

_SCAN_SKIP_DIRS = {
    ".git",
    ".spec",
    "docs",
    "node_modules",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".astro",
    ".angular",
    "dist",
    "build",
    "storybook-static",
    "coverage",
    ".gemini",
    ".cursor",
    ".claude",
    ".windsurf",
}
_UI_EXTS = {".tsx", ".jsx", ".vue", ".svelte", ".astro"}


def _is_fresh_scaffold(project_root: Path) -> bool:
    """Determina si el repo tiene un scaffold inicial minimo (<=2 vistas UI, sin features ni tests)."""
    if not (project_root / "package.json").is_file():
        return False
    ui_files = 0
    for item in project_root.rglob("*"):
        if any(part in _SCAN_SKIP_DIRS for part in item.parts) or not item.is_file():
            continue
        low_name = item.name.lower()
        rel_path = item.relative_to(project_root)
        rel = rel_path.as_posix().lower()
        if re.search(r"\.(test|spec)\.[a-z]+$", low_name) or rel.startswith(
            ("tests/", "test/", "e2e/", "playwright/", "cypress/")
        ):
            return False
        if rel.startswith(("src/features/", "src/modules/")) and len(rel_path.parts) >= 4:
            return False
        if item.suffix.lower() in _UI_EXTS or low_name.endswith(".component.ts"):
            ui_files += 1
            if ui_files > 2:
                return False
    return True


def _has_any_glob(root: Path, patterns: Tuple[str, ...]) -> bool:
    for pat in patterns:
        if any(root.glob(pat)):
            return True
    return False


def _read_package_deps(project_root: Path) -> Dict[str, str]:
    pkg = project_root / "package.json"
    if not pkg.is_file():
        return {}
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
        deps: Dict[str, str] = {}
        for section in ("dependencies", "devDependencies", "peerDependencies"):
            block = data.get(section)
            if isinstance(block, dict):
                for k, v in block.items():
                    deps[str(k)] = str(v)
        return deps
    except Exception:
        return {}


def _detect_ecosystem_key(project_root: Path, deps: Dict[str, str]) -> str:
    checks: Tuple[Tuple[str, Tuple[str, ...], Tuple[str, ...]], ...] = (
        ("angular", ("angular.json",), ("@angular/core",)),
        ("nuxt", ("nuxt.config.*",), ("nuxt", "nuxt3")),
        ("sveltekit", ("svelte.config.*",), ("@sveltejs/kit",)),
        ("astro", ("astro.config.*",), ("astro",)),
        ("nextjs", ("next.config.*",), ("next",)),
        ("qwik", (), ("@builder.io/qwik", "@builder.io/qwik-city")),
        ("solid", (), ("solid-js", "@solidjs/start")),
        ("remix", ("remix.config.*",), ("@remix-run/react", "@remix-run/node", "@react-router/dev")),
        ("vue-vite", (), ("vue",)),
        ("react-vite", ("vite.config.*",), ("react", "react-dom")),
    )
    for key, globs, pkg_names in checks:
        if any(p in deps for p in pkg_names):
            return key
        if globs and _has_any_glob(project_root, globs):
            if key == "react-vite" and "vue" in deps:
                return "vue-vite"
            return key
    return "react-vite"


def _detect_storybook(project_root: Path, deps: Dict[str, str]) -> bool:
    """Detecta si el proyecto utiliza Storybook por dependencias @storybook/* o carpeta .storybook/."""
    return (
        any(k == "storybook" or k.startswith("@storybook/") for k in deps)
        or (project_root / ".storybook").is_dir()
    )


def _detect_package_manager(project_root: Path) -> str:
    if (project_root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (project_root / "bun.lockb").exists() or (project_root / "bun.lock").exists():
        return "bun"
    if (project_root / "yarn.lock").exists():
        return "yarn"
    return "npm"


def _detect_styling_and_ui(project_root: Path, deps: Dict[str, str]) -> Tuple[str, str]:
    if _has_any_glob(project_root, ("tailwind.config.*",)) or "tailwindcss" in deps:
        styling = "Tailwind CSS"
    elif "@vanilla-extract/css" in deps:
        styling = "Vanilla Extract"
    elif "sass" in deps or "sass-embedded" in deps:
        styling = "SCSS / CSS Modules"
    else:
        styling = "CSS Custom Properties / CSS Modules"

    if (project_root / "components.json").exists():
        ui_primitives = "shadcn/ui + Radix"
    elif any(k.startswith("@radix-ui/") for k in deps):
        ui_primitives = "Radix UI"
    elif any(k.startswith("@headlessui/") for k in deps):
        ui_primitives = "Headless UI"
    elif "@angular/material" in deps:
        ui_primitives = "Angular Material"
    elif any(k.startswith("@chakra-ui/") for k in deps):
        ui_primitives = "Chakra UI"
    elif "primevue" in deps:
        ui_primitives = "PrimeVue"
    else:
        ui_primitives = "Primitivas Nativas / HTML Semantico"

    return styling, ui_primitives


def _detect_state_and_tests(
    project_root: Path, deps: Dict[str, str], profile: Dict[str, str]
) -> Dict[str, str]:
    if any(
        k in deps
        for k in (
            "@tanstack/react-query",
            "@tanstack/vue-query",
            "@tanstack/svelte-query",
            "@tanstack/angular-query-experimental",
        )
    ):
        state_server = "TanStack Query"
    elif "swr" in deps:
        state_server = "SWR"
    elif "@reduxjs/toolkit" in deps:
        state_server = "RTK Query / Redux Toolkit"
    else:
        state_server = profile["default_state_server"]

    if "vitest" in deps or _has_any_glob(project_root, ("vitest.config.*",)):
        unit_runner = "Vitest"
    elif "jest" in deps or _has_any_glob(project_root, ("jest.config.*",)):
        unit_runner = "Jest"
    elif profile["ecosystem"] == "angular" and (
        "karma" in deps or "jasmine-core" in deps
    ):
        unit_runner = "Jasmine / Karma"
    else:
        unit_runner = "Vitest"

    testing_lib = profile["default_testing_lib"]
    for lib_pkg in (
        "@testing-library/react",
        "@testing-library/vue",
        "@testing-library/svelte",
        "@testing-library/angular",
        "@solidjs/testing-library",
    ):
        if lib_pkg in deps:
            testing_lib = lib_pkg
            break

    if "@playwright/test" in deps or _has_any_glob(project_root, ("playwright.config.*",)):
        e2e_runner = "Playwright"
    elif "cypress" in deps or _has_any_glob(project_root, ("cypress.config.*",)):
        e2e_runner = "Cypress"
    else:
        e2e_runner = "Playwright"

    return {
        "state_server": state_server,
        "unit_test_runner": unit_runner,
        "testing_library": testing_lib,
        "e2e_runner": e2e_runner,
    }


def _detect_directories(project_root: Path, profile: Dict[str, str]) -> Tuple[str, str]:
    src_dir = "src" if (project_root / "src").is_dir() else profile["src_dir"]
    if not (project_root / src_dir).is_dir() and (project_root / "app").is_dir():
        src_dir = "app"

    candidates_by_eco: Dict[str, Tuple[str, ...]] = {
        "nextjs": ("src/app", "app", "src/pages", "pages"),
        "remix": ("app/routes", "src/routes"),
        "nuxt": ("app/pages", "pages"),
        "sveltekit": ("src/routes",),
        "solid": ("src/routes", "src/pages"),
        "qwik": ("src/routes",),
        "astro": ("src/pages",),
        "angular": ("src/app",),
        "vue-vite": ("src/router", "src/pages", "src/views"),
        "react-vite": ("src/pages", "src/routes", "src/app"),
    }
    routes_dir = profile["routes_dir"]
    for cand in candidates_by_eco.get(profile["ecosystem"], ()):
        if (project_root / cand).is_dir():
            routes_dir = cand
            break

    return src_dir, routes_dir


def build_profile_context(project_root: Path, ecosystem_key: Optional[str] = None) -> Dict[str, Any]:
    """Construye el perfil tecnico completo combinando heuristica del ecosistema y dependencias."""
    deps = _read_package_deps(project_root)
    resolved_key = ecosystem_key or _detect_ecosystem_key(project_root, deps)
    base = dict(_PROFILE_MAP.get(resolved_key, _PROFILE_MAP["react-vite"]))

    has_pkg = (project_root / "package.json").exists()
    has_js_only_marker = _has_any_glob(
        project_root, ("*.config.js", "*.config.mjs", "jsconfig.json")
    )
    has_ts = (
        (project_root / "tsconfig.json").exists()
        or "typescript" in deps
        or (not has_pkg and not has_js_only_marker)
    )
    language = "TypeScript" if has_ts else "JavaScript"
    src_ext = base["src_ext"]
    if not has_ts and src_ext == ".tsx":
        src_ext = ".jsx"
    elif not has_ts and src_ext == ".ts":
        src_ext = ".js"

    src_dir, routes_dir = _detect_directories(project_root, base)
    styling, ui_primitives = _detect_styling_and_ui(project_root, deps)
    state_and_tests = _detect_state_and_tests(project_root, deps, base)
    pkg_manager = _detect_package_manager(project_root)
    has_storybook = _detect_storybook(project_root, deps)

    test_pattern = base["test_pattern"]
    if not has_ts and test_pattern.endswith(".tsx"):
        test_pattern = test_pattern[:-4] + ".jsx"
    elif not has_ts and test_pattern.endswith(".ts"):
        test_pattern = test_pattern[:-3] + ".js"

    return {
        "ecosystem": base["ecosystem"],
        "runtime_label": base["runtime_label"],
        "framework": base["framework"],
        "meta_framework": base["meta_framework"],
        "language": language,
        "package_manager": pkg_manager,
        "styling": styling,
        "ui_primitives": ui_primitives,
        "state_server": state_and_tests["state_server"],
        "unit_test_runner": state_and_tests["unit_test_runner"],
        "testing_library": state_and_tests["testing_library"],
        "e2e_runner": state_and_tests["e2e_runner"],
        "has_storybook": has_storybook,
        "manifest": "package.json",
        "version_file": "package.json" if (project_root / "package.json").exists() or not (project_root / "VERSION").exists() else "VERSION",
        "format": "json" if (project_root / "package.json").exists() or not (project_root / "VERSION").exists() else "plain",
        "field": "version",
        "src_ext": src_ext,
        "src_dir": src_dir,
        "routes_dir": routes_dir,
        "test_pattern": test_pattern,
    }


def detect_frontend_ecosystem(project_root: Path) -> Dict[str, Any]:
    """Detecta modo Greenfield vs Brownfield e identifica el stack frontend activo."""
    project_root = Path(project_root).resolve()

    existing_files = [
        f for f in project_root.iterdir() if f.name not in IGNORED_SCAFFOLD_ENTRIES
    ]
    if not existing_files:
        return {
            "mode": "greenfield",
            "project_state": "empty",
            "is_fresh_scaffold": False,
            "detected": None,
            "message": "Directorio vacio o proyecto nuevo. Modo Greenfield activado.",
        }

    profile = build_profile_context(project_root)
    version_path = project_root / profile["version_file"]
    manifest_path = project_root / profile["manifest"]
    fresh_scaffold = _is_fresh_scaffold(project_root)
    project_state = "scaffold" if fresh_scaffold else "brownfield"

    return {
        "mode": "brownfield",
        "project_state": project_state,
        "is_fresh_scaffold": fresh_scaffold,
        "detected": profile,
        "manifest_path": manifest_path,
        "version_path": version_path,
        "message": (
            f"Ecosistema detectado: {profile['runtime_label']} "
            f"({profile['ecosystem']} / {profile['language']} / {profile['styling']})"
        ),
    }
