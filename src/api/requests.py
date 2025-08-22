from flask import request
from typing import Optional, Tuple

def get_str_arg(name: str, default: Optional[str] = None, trim=True) -> Optional[str]:
    v = request.args.get(name, default)
    if v is None:
        return default
    return v.strip() if trim else v

def get_int_arg(name: str, default: Optional[int] = None) -> Optional[int]:
    try:
        return request.args.get(name, type=int) if name in request.args else default
    except Exception:
        return default

def get_bool_arg(name: str, default: Optional[bool] = None) -> Optional[bool]:
    raw = request.args.get(name)
    if raw is None:
        return default
    return raw.lower() in ("1", "true", "yes", "y", "on")

def get_pagination(default_page=1, default_size=50, max_size=200) -> Tuple[int, int, int, int]:
    page = get_int_arg("page", default_page) or default_page
    size = get_int_arg("page_size", default_size) or default_size
    if page < 1: page = 1
    if size < 1: size = default_size
    if size > max_size: size = max_size
    offset = (page - 1) * size
    limit = size
    return page, size, offset, limit

def get_sort(default: Optional[str] = None, allowed: set[str] | None = None) -> list[tuple[str, str]]:
    """
    sort=field1:asc,field2:desc
    """
    s = get_str_arg("sort", default)
    if not s:
        return []
    parts = []
    for token in s.split(","):
        field, _, direction = token.partition(":")
        field = field.strip()
        direction = (direction or "asc").lower()
        if allowed and field not in allowed:
            continue
        if direction not in ("asc", "desc"):
            direction = "asc"
        parts.append((field, direction))
    return parts
