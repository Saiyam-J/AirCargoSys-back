import time, uuid
from contextlib import contextmanager
from app.extensions import redis_client

# Atomic unlock script to ensure we only release our own lock
_RELEASE_LUA = """
if redis.call("GET", KEYS[1]) == ARGV[1] then
  return redis.call("DEL", KEYS[1])
else
  return 0
end
"""

@contextmanager
def redis_lock(key: str, ttl_ms: int = 8000, wait_ms: int = 3000, poll_ms: int = 100):
    """
    Acquire a distributed lock:
      key      -> lock key string (e.g., lock:booking:<ref_id>)
      ttl_ms   -> lock auto-expiry (avoid deadlocks)
      wait_ms  -> how long to wait to acquire before failing
      poll_ms  -> backoff between retries
    """
    if redis_client is None:
        # If Redis isn’t configured, the context still runs but provides no locking
        yield None
        return

    token = str(uuid.uuid4())
    deadline = time.time() + (wait_ms / 1000.0)
    acquired = False

    while time.time() < deadline:
        # SET NX PX -> acquire if not exists with TTL
        if redis_client.set(name=key, value=token, nx=True, px=ttl_ms):
            acquired = True
            break
        time.sleep(poll_ms / 1000.0)

    if not acquired:
        raise TimeoutError(f"Could not acquire lock for {key}")

    try:
        yield token
    finally:
        try:
            redis_client.eval(_RELEASE_LUA, 1, key, token)
        except Exception:
            pass
