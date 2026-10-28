"""Verify supplied baseline preservation and pack round-trip."""
from pathlib import Path
import sys, json, hashlib
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'tools'))
from packfile import read_pack, extract
pack=root/'dist/the_empire_endures.pack'
entries=read_pack(pack)
for p in (root/'src').rglob('*'):
 if p.is_file():
  key=p.relative_to(root/'src').as_posix()
  assert extract(pack,key,entries)==p.read_bytes(),key
for e in json.loads((root/'baseline.json').read_text())['files']:
 assert hashlib.sha256(extract(pack,e['path'],entries)).hexdigest()==e['sha256'],e['path']
print('PASS: pack contents and baseline payload hashes')
