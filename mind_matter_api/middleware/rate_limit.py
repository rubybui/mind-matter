import time
from flask import request, jsonify
from mind_matter_api.extensions import cache
from mind_matter_api.utils.auth import get_user_id_from_token  # assume this exists

def get_rate_limit_identity():
    # 1. Check for Device ID header (mobile apps)
    device_id = request.headers.get("X-Device-ID")
    if device_id:
        return f"device:{device_id}"

    # 2. Check for authenticated user (e.g. JWT bearer)
    auth_header = request.headers.get("Authorization")
    if auth_header and " " in auth_header:
        token_type, token = auth_header.split(" ", 1)
        if token_type.lower() == "bearer":
            try:
                user_id = get_user_id_from_token(token)
                if user_id:
                    return f"user:{user_id}"
            except Exception:
                pass

    # 3. Fallback to IP address
    return f"ip:{request.remote_addr or 'unknown'}"


def rate_limit_middleware(limit: int, window: int, exclude_paths=None, exclude_methods=None):
    exclude_paths = exclude_paths or []
    exclude_methods = exclude_methods or []

    def middleware():
        if request.path in exclude_paths or request.method in exclude_methods:
            return

        identity = get_rate_limit_identity()
        key = f"rate-limit:{identity}:{request.endpoint}"
        now = time.time()

        record = cache.get(key)

        if record:
            count, first_time = record
            if now - first_time < window:
                if count >= limit:
                    retry_after = int(window - (now - first_time) + 1)
                    response = jsonify({
                        "error": "Rate limit exceeded",
                        "retry_after_seconds": retry_after
                    })
                    response.headers["Retry-After"] = str(retry_after)
                    return response, 429
                cache.set(key, (count + 1, first_time), timeout=window * 2)
            else:
                cache.set(key, (1, now), timeout=window * 2)
        else:
            cache.set(key, (1, now), timeout=window * 2)

    return middleware
