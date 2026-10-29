"""Build the supplied Empire Endures baseline plus independent Franz school."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'tools'))
from packfile import write_pack
from check_db_references import main as check_references
check_references()
root=Path(__file__).resolve().parent
files={p.relative_to(root/'src').as_posix():p.read_bytes() for p in (root/'src').rglob('*') if p.is_file()}
output=root/'dist/the_empire_endures.pack'
output.parent.mkdir(exist_ok=True)
write_pack(output,files)
print(f'Built {output.name}: {len(files)} entries')
