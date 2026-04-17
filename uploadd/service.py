import os
from uploadd.paths import safe_join, UnsafePath
from uploadd.io import atomic_write
from uploadd.limits import MAX_BYTES


UPLOAD_ROOT = os.environ.get("UPLOAD_ROOT", "./uploads")


def store(user_id, filename, data):
    if len(data) > MAX_BYTES:
        raise ValueError(f"file exceeds {MAX_BYTES} bytes")
    user_dir = safe_join(UPLOAD_ROOT, user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    target = safe_join(str(user_dir), filename)
    atomic_write(target, data)
    return str(target)


def retrieve(user_id, filename):
    target = safe_join(safe_join(UPLOAD_ROOT, user_id), filename)
    if not target.is_file():
        return None
    return target.read_bytes()
