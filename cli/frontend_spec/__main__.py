import argparse
import sys
from pathlib import Path

from frontend_spec import __version__
from frontend_spec.commands.bootstrap_cmd import run_bootstrap
from frontend_spec.commands.check_cmd import run_check
from frontend_spec.commands.init_cmd import run_init
from frontend_spec.commands.new_req_cmd import run_new_req
from frontend_spec.commands.resolve_cmd import run_resolve
from frontend_spec.commands.sync_index_cmd import run_sync_index
from frontend_spec.commands.update_cmd import run_update
from frontend_spec.detector.ecosystem_detector import ECOSYSTEM_PROFILES


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="frontend-spec",
        description=f"Framework y CLI v{__version__} para ingenieria frontend Spec-Driven con agentes de IA",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    init_p = subparsers.add_parser("init", help="Inicializa frontend-spec en el proyecto destino")
    init_p.add_argument(
        "--harness",
        choices=["all", "antigravity", "cursor", "claude", "windsurf"],
        default="all",
        help="Harness de IA a configurar",
    )
    init_p.add_argument(
        "--versioning",
        choices=["semver", "calver", "sequential"],
        default="semver",
        help="Estrategia de versionamiento",
    )
    init_p.add_argument("-i", "--interactive", action="store_true", help="Modo interactivo")
    init_p.add_argument("-f", "--force", action="store_true", help="Sobrescribir archivos existentes")
    init_p.add_argument(
        "--ecosystem",
        choices=[p["ecosystem"] for p in ECOSYSTEM_PROFILES],
        default=None,
        help="Perfil de ecosistema objetivo (ideal en proyectos vacios)",
    )
    init_p.add_argument(
        "--mode",
        choices=["auto", "greenfield", "brownfield"],
        default="auto",
        help="Fuerza deteccion Greenfield o Brownfield (por defecto auto)",
    )
    init_p.add_argument("--dir", default=".", help="Directorio destino")

    upd_p = subparsers.add_parser(
        "update",
        help="Actualiza blueprints, skills, reglas gestionadas y hook pre-commit sin sobrescribir docs/",
    )
    upd_p.add_argument(
        "--harness",
        choices=["all", "antigravity", "cursor", "claude", "windsurf"],
        default=None,
        help="Harness a actualizar o agregar (por defecto auto-detecta)",
    )
    upd_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula los cambios sin modificar el disco",
    )
    upd_p.add_argument(
        "--refresh-stack",
        action="store_true",
        help="Re-detecta package.json/stack y sincroniza .spec/config.yaml y tech-stack.md sin destruir docs/",
    )
    upd_p.add_argument("--dir", default=".", help="Directorio del proyecto")

    boot_p = subparsers.add_parser(
        "bootstrap",
        help="Escanea un proyecto frontend existente (Brownfield) y genera .spec/bootstrap-report.md",
    )
    boot_p.add_argument(
        "--mode",
        choices=["auto", "full", "progressive"],
        default="auto",
        help="Alcance del levantamiento UX inicial",
    )
    boot_p.add_argument(
        "--reset",
        action="store_true",
        help="Reinicia las casillas de verificacion en .spec/bootstrap-report.md",
    )
    boot_p.add_argument("--dir", default=".", help="Directorio del proyecto")

    req_p = subparsers.add_parser("req:new", help="Crea un nuevo requerimiento REQ-UI-* en pending.md")
    req_p.add_argument("title", nargs="?", default=None, help="Titulo del requerimiento")
    req_p.add_argument("--domain", default="core", help="Dominio funcional/UI (ej. auth, checkout)")
    req_p.add_argument("--priority", choices=["P1", "P2", "P3"], default="P2", help="Prioridad")
    req_p.add_argument(
        "--impact",
        choices=["MAJOR", "MINOR", "PATCH"],
        default="MINOR",
        help="Impacto SemVer (PATCH activa Fast-Track)",
    )
    req_p.add_argument("--version", dest="target_version", default=None, help="Version objetivo")
    req_p.add_argument("--uf", dest="uf_ref", default=None, help="Ruta al flujo UX UF-*.md vinculado")
    req_p.add_argument("--tokens", default=None, help="Tokens semanticos consumidos separados por coma")
    req_p.add_argument("--fast-track", action="store_true", help="Fuerza carril ligero PATCH/Micro-Spec")
    req_p.add_argument("--from-audit", dest="from_audit", default=None, help="ID AUDIT-UI-* a promover")
    req_p.add_argument("--dir", default=".", help="Directorio del proyecto")

    sync_p = subparsers.add_parser(
        "sync", help="Sincroniza docs/backlog/index.md, docs/functional/index.md y docs/design/index.md"
    )
    sync_p.add_argument(
        "--export-tokens",
        action="store_true",
        help="Exporta docs/design/tokens-and-themes.md a .spec/specs/design.tokens.json (formato W3C DTCG)",
    )
    sync_p.add_argument("--dir", default=".", help="Directorio del proyecto")

    chk_p = subparsers.add_parser(
        "check", help="Valida enlaces, esquemas JSON Draft-07, Mermaid, Rolling Window y commits staged"
    )
    chk_p.add_argument(
        "--staged",
        action="store_true",
        help="Valida git diff --cached bloqueando commits fantasma sin REQ-UI-*",
    )
    chk_p.add_argument(
        "--strict-tokens",
        action="store_true",
        help="Detecta colores hexadecimales quemados (#RRGGBB) en componentes UI fuera de tokens",
    )
    chk_p.add_argument(
        "--security",
        action="store_true",
        help="Consulta alertas abiertas de Dependabot en GitHub mediante GitHub CLI (gh)",
    )
    chk_p.add_argument("--dir", default=".", help="Directorio del proyecto")

    res_p = subparsers.add_parser(
        "resolve", help="Archiva un REQ-UI-* en changelog.md y opcionalmente actualiza version"
    )
    res_p.add_argument("req_id", help="Identificador del requerimiento (ej. REQ-UI-AUTH-001)")
    res_p.add_argument(
        "--bump",
        action="store_true",
        help="Actualiza la version en package.json y .spec/config.yaml",
    )
    res_p.add_argument(
        "--force-version",
        action="store_true",
        help="Permite forzar version inferior a la actual en el manifiesto",
    )
    res_p.add_argument("--dir", default=".", help="Directorio del proyecto")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    project_dir = Path(getattr(args, "dir", ".")).resolve()

    if args.command == "init":
        run_init(
            target_dir=project_dir,
            harness=args.harness,
            versioning=args.versioning,
            interactive=args.interactive,
            force=args.force,
            ecosystem=args.ecosystem,
            mode=args.mode,
        )
    elif args.command == "update":
        ok = run_update(
            target_dir=project_dir,
            harness=args.harness,
            dry_run=args.dry_run,
            refresh_stack=args.refresh_stack,
        )
        sys.exit(0 if ok else 1)
    elif args.command == "bootstrap":
        run_bootstrap(project_root=project_dir, mode=args.mode, reset=args.reset)
    elif args.command == "req:new":
        req_id = run_new_req(
            project_root=project_dir,
            title=args.title,
            domain=args.domain,
            priority=args.priority,
            impact=args.impact,
            target_version=args.target_version,
            uf_ref=args.uf_ref,
            tokens=args.tokens,
            fast_track=args.fast_track,
            from_audit=args.from_audit,
        )
        sys.exit(0 if req_id else 1)
    elif args.command == "sync":
        run_sync_index(project_root=project_dir, export_tokens=args.export_tokens)
    elif args.command == "check":
        ok = run_check(
            project_root=project_dir,
            check_staged=args.staged,
            strict_tokens=args.strict_tokens,
            check_security=args.security,
        )
        sys.exit(0 if ok else 1)
    elif args.command == "resolve":
        ok = run_resolve(
            project_root=project_dir,
            req_id=args.req_id,
            auto_bump=args.bump,
            force_version=args.force_version,
        )
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
