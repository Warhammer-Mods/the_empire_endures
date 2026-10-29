"""Check added native rows and their reference contract against reviewed vanilla keys."""
from pathlib import Path
import json
import struct

ROOT = Path(__file__).resolve().parents[1]

def encode(field, value):
    kind = field["field_type"]
    prefix = b""
    if kind.startswith("Optional"):
        if value == "":
            return b"\0"
        prefix, kind = b"\1", kind[8:]
    if kind in ("StringU8", "StringU16"):
        data = value.encode("utf-16le" if kind == "StringU16" else "utf8")
        return prefix + struct.pack("<H", len(data) // (2 if kind == "StringU16" else 1)) + data
    if kind == "Boolean":
        return prefix + bytes([int(value)])
    return prefix + struct.pack("<" + {"I16":"h", "I32":"i", "I64":"q", "F32":"f", "F64":"d"}[kind], value)

def reference_errors(blocks, contract):
    keys = {k: set(v) for k, v in contract["vanilla_keys"].items()}
    for block in blocks:
        table = block["table"].removesuffix("_tables")
        for i, name in enumerate(block["fields"]):
            keys.setdefault(table + "." + name, set()).update(row[i] for row in block["rows"])
    errors = []
    for block in blocks:
        for i, field in enumerate(contract["fields"][block["table"]]):
            ref = field.get("is_reference")
            if not ref:
                continue
            valid = keys.get(".".join(ref), set())
            for row in block["rows"]:
                if row[i] != "" and row[i] not in valid:
                    errors.append(f"{block['table']}.{field['name']}: missing {ref}: {row[i]}")
    return errors

def main():
    blocks = json.loads((ROOT / "db_rows.json").read_text())
    contract = json.loads((ROOT / "docs/db_reference_contract.json").read_text())
    for block in blocks:
        fields = contract["fields"][block["table"]]
        if block["fields"] != [f["name"] for f in fields]:
            raise SystemExit("Documented fields differ from native schema")
        data = (ROOT / "src/db" / block["table"] / "ss_franz_gunnery").read_bytes()
        pos = 0
        if data[:4] == b"\xfd\xfe\xfc\xff":
            pos = 6 + struct.unpack_from("<H", data, 4)[0] * 2
        if data[pos:pos+4] == b"\xfc\xfd\xfe\xff":
            pos += 8
        if data[pos] not in (0, 1):
            raise SystemExit("Invalid native DB header")
        expected = struct.pack("<I", len(block["rows"])) + b"".join(
            encode(f, v) for row in block["rows"] for f, v in zip(fields, row))
        if data[pos+1:] != expected:
            raise SystemExit(f"Native DB differs from reviewed rows: {block['table']}")
    errors = reference_errors(blocks, contract)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(blocks)} added native tables match reviewed rows; all references resolve")

if __name__ == "__main__":
    main()
