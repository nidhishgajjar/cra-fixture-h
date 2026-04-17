import time

_buckets = {}  # user_id -> list of timestamps


def check(user_id, limit=10, window=60):
    """Return True if user_id is within the rate limit, else False."""
    now = time.time()
    hits = _buckets.get(user_id, [])
    hits = [t for t in hits if t > now - window]
    if len(hits) >= limit:
        return False
    hits.append(now)
    _buckets[user_id] = hits
    return True
