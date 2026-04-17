import os
import pathlib


class UnsafePath(Exception):
    pass


def safe_join(base, *parts):
    base_p = pathlib.Path(base).resolve()
    candidate = (base_p / pathlib.Path(*parts)).resolve()
    try:
        candidate.relative_to(base_p)
    except ValueError:
        raise UnsafePath(f"{candidate} escapes {base_p}")
    if any(p == ".." for p in parts):
        raise UnsafePath(f"'..' not allowed in parts")
    return candidate
