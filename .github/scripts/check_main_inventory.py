"""Validate approved game files and preserve the supplied baseline payloads."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = root / "src"
expected = json.loads((root / "docs/main_pack_inventory.json").read_text())
actual = sorted(p.relative_to(source).as_posix() for p in source.rglob("*") if p.is_file())
if actual != sorted(expected) or len(expected) != len(set(expected)):
    raise SystemExit(f"Inventory mismatch: missing={sorted(set(expected)-set(actual))}; unexpected={sorted(set(actual)-set(expected))}")
baseline = json.loads((root / "baseline.json").read_text())
for entry in baseline["files"]:
    if hashlib.sha256((source / entry["path"]).read_bytes()).hexdigest() != entry["sha256"]:
        raise SystemExit(f"Supplied baseline payload changed: {entry['path']}")
print(f"PASS: {len(actual)} approved game files; {len(baseline['files'])} baseline payloads unchanged")
