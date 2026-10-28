"""Small uncompressed PFH5 reader/writer for campaign script packs."""
from pathlib import Path
import struct


def read_pack(path):
    with Path(path).open('rb') as f:
        header = f.read(28)
        magic, flags, deps, dep_size, count, index_size, timestamp = struct.unpack('<4s6I', header)
        if magic != b'PFH5' or flags & ~0x3F:
            raise ValueError(f'Unsupported pack header: {path}')
        # Extended headers are not needed for the local CA PFH5 packs.
        if flags & 0x100:
            raise ValueError('Extended header unsupported')
        f.seek(dep_size, 1)
        index = f.read(index_size)
        data_start = f.tell()
        pos = 0
        offset = data_start
        entries = {}
        for _ in range(count):
            size, compressed = struct.unpack_from('<IB', index, pos)
            pos += 5
            end = index.index(0, pos)
            name = index[pos:end].decode('utf-8').replace('\\', '/')
            entries[name] = (offset, size, compressed)
            offset += size
            pos = end + 1
        if pos != len(index):
            raise ValueError(f'Index length mismatch: {path}')
    return entries


def extract(path, entry, entries=None):
    entries = entries if entries is not None else read_pack(path)
    offset, size, compressed = entries[entry]
    if compressed:
        raise ValueError(f'Compressed entry unsupported: {entry}')
    with Path(path).open('rb') as f:
        f.seek(offset)
        return f.read(size)


def write_pack(path, files):
    files = sorted(files.items())
    index = b''.join(struct.pack('<IB', len(data), 0) + name.replace('/', '\\').encode() + b'\0'
                     for name, data in files)
    header = struct.pack('<4s6I', b'PFH5', 3, 0, 0, len(files), len(index), 0)
    Path(path).write_bytes(header + index + b''.join(data for _, data in files))
    entries = read_pack(path)
    assert set(entries) == {name for name, _ in files}
    for name, data in files:
        assert extract(path, name, entries) == data
