import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

cli_dir = Path(__file__).resolve().parent
if str(cli_dir) not in sys.path:
    sys.path.insert(0, str(cli_dir))

from frontend_spec.__main__ import main

if __name__ == "__main__":
    main()
