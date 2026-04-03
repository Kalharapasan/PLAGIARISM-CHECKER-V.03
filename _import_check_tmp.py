import importlib
import sys
modules = [
    "ui.basic_gui",
    "ui.advanced_gui",
    "ui.ultimate_gui",
    "ui.cli_interface",
    "core.batch_processor",
    "api.server",
]
failed = []
for m in modules:
    try:
        importlib.import_module(m)
        print(f"OK {m}")
    except Exception as e:
        failed.append((m, e))
        print(f"FAIL {m}: {type(e).__name__}: {e}")
if failed:
    sys.exit(1)
