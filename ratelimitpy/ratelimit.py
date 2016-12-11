import time
from functools import wraps
from threading import Lock
from flask import g, abort, current_app


class TokenBucket:
    def __init__(self, tokens, per_seconds, ban=None):
        if tokens < 1:
            raise RuntimeError("tokens should be 1 or more")
        if per_seconds < 1:
            raise RuntimeError("per_seconds should be 1 or more")
        if ban is None:
            ban = per_seconds
        if ban < per_seconds:
            raise RuntimeError("cannot ban for less time than per_seconds")
        self.__tokens = tokens
        self.__per_seconds = per_seconds
        self.__bucket = tokens
        self.__last = time.time()
        self.__lock = Lock()
        self.__ban = ban
        self.__banned = False

    def allow(self):
        with self.__lock:
            return self.__allow()

    def __allow(self):
        # Should we add tokens
        now = time.time()
        elapsed_token_periods = int((now - self.__last)) // self.__per_seconds
        tokens = self.__tokens * elapsed_token_periods

        #print("Elapsed: {0} Periods: {1} Extra:{2}, Current {3}".format(now - self.__last,
        #    elapsed_token_periods, tokens, self.__bucket))
        if tokens > 0:
            self.__bucket = min(self.__tokens, self.__bucket + tokens)
            if self.__bucket > 0:
                self.__banned = False
            # advance time
            self.__last += elapsed_token_periods * self.__per_seconds

        # check if can allow the request/tick/item
        if self.__bucket > 0:
            self.__bucket -= 1
            return True
        if self.__banned:
            # You're already banned:
            return False
        # Ban the bucket
        self.__bucket -= (self.__ban - self.__per_seconds) // self.__per_seconds
        self.__banned = True
        return False


def get_config(defaults, api_key):
    """Get rate limit config for a specific key or use defaults"""
    config = defaults.copy()
    extra = current_app.config['RATE_LIMITS'].get(api_key, {})
    config.update(extra)
    return dict(
            tokens=config['requests'],
            per_seconds=config['per_seconds'],
            ban=config['ban'])


def limit(requests, per_seconds, ban):
    """Rate limit decorator for flask view"""
    def decorator(original):
        defaults = dict(
                requests=requests, per_seconds=per_seconds, ban=ban)
        token_db = {}
        lock = Lock()
        @wraps(original)
        def wrapped(*args, **kwargs):
            with lock:
                bucket = token_db.get(g.api_key)
                if bucket is None:
                    bucket = TokenBucket(**get_config(defaults, g.api_key))
                    token_db[g.api_key] = bucket
            if bucket.allow():
                return original(*args, **kwargs)
            else:
                abort(429)
        return wrapped
    return decorator
