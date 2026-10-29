import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("check_db_references", ROOT / "tools/check_db_references.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class ReferenceTests(unittest.TestCase):
    def test_corrected_references_resolve(self):
        checker.main()

    def test_original_crash_is_rejected_for_all_three_charge_groups(self):
        blocks = json.loads((ROOT / "db_rows.json").read_text())
        contract = json.loads((ROOT / "docs/db_reference_contract.json").read_text())
        for ability in ("bjuna_bombard", "purple_eclipse", "spirit_barrage"):
            with self.subTest(ability=ability):
                broken = copy.deepcopy(blocks)
                block = next(b for b in broken if b["table"] == "campaign_group_members_tables")
                row = next(r for r in block["rows"] if r[1].endswith(ability + "_1-3"))
                row[0] = row[1]
                errors = checker.reference_errors(broken, contract)
                self.assertTrue(any(row[1] in error and ".group:" in error for error in errors))
