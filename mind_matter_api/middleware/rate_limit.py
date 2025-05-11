import time
from flask import request, jsonify
from mind_matter_api.extensions import cache   
def rate_limit_middleware(limit: int, window: int):
    def middleware():
        ip = request.remote_addr or "global"
        key = f"rate-limit:{ip}:{request.endpoint}"
        now = time.time()

        record = cache.get(key)

        if record:
            count, first_time = record
            if now - first_time < window:
                if count >= limit:
                    return jsonify({"error": "Rate limit exceeded"}), 429
                cache.set(key, (count + 1, first_time))
            else:
                cache.set(key, (1, now))
        else:
            cache.set(key, (1, now))
    return middleware
