import pytest
from flask import g
from ratelimitpy import app
from ratelimitpy.ratelimit import TokenBucket, limit
from werkzeug.exceptions import TooManyRequests


@pytest.fixture
def bucket(monkeypatch):
    # Set starting time at 10
    monkeypatch.setattr("time.time", lambda: 10.0)
    # 2 requests every 10 seconds, ban for 30 seconds
    bucket = TokenBucket(2, 10, 30)
    return bucket


def test_first_allowed(bucket):
    assert bucket.allow()


def test_second_allowed(bucket):
    bucket.allow()
    assert bucket.allow()


def test_third_not_allowed(bucket):
    bucket.allow()
    bucket.allow()
    assert not bucket.allow()


def test_fourth_not_allowed(bucket):
    bucket.allow()
    bucket.allow()
    bucket.allow()
    assert not bucket.allow()


def test_fourth_allowed_after_30s(bucket, monkeypatch):
    bucket.allow()
    bucket.allow()
    bucket.allow()
    monkeypatch.setattr("time.time", lambda: 40.0)
    assert bucket.allow()


def test_fifth_allowed_after_30s_fourth_dont_ban_again(bucket, monkeypatch):
    bucket.allow()
    bucket.allow()
    bucket.allow()
    monkeypatch.setattr("time.time", lambda: 20.0)
    bucket.allow()
    monkeypatch.setattr("time.time", lambda: 40.0)
    assert bucket.allow()


def test_third_allowed_after_10s(bucket, monkeypatch):
    bucket.allow()
    bucket.allow()
    monkeypatch.setattr("time.time", lambda: 20.0)
    assert bucket.allow()


def test_fourth_allowed_after_10s(bucket, monkeypatch):
    bucket.allow()
    bucket.allow()
    monkeypatch.setattr("time.time", lambda: 20.0)
    bucket.allow()
    assert bucket.allow()

def test_tokens_should_be_1_or_more():
    with pytest.raises(RuntimeError):
        TokenBucket(0, 2, 2)

def test_per_seconds_shoul_be_ge_1():
    with pytest.raises(RuntimeError):
        TokenBucket(1, 0, 2)

def test_ban_shoul_be_ge_than_per_seconds():
    with pytest.raises(RuntimeError):
        TokenBucket(1, 10, 2)


def test_ban_None_then_as_per_seconds(monkeypatch):
    # Set starting time at 10
    monkeypatch.setattr("time.time", lambda: 10.0)
    # 2 requests every 10 seconds, ban for 30 seconds
    bucket = TokenBucket(2, 10)

    bucket.allow()
    bucket.allow()
    bucket.allow()
    monkeypatch.setattr("time.time", lambda: 20.0)
    assert bucket.allow()


# Test ratelimit decorator
def test_ratelimit_aborts_429(monkeypatch):
    @limit(1, 10, 60)
    def nothing():
        pass

    class MyBucket:
        def __init__(self, tokens, per_seconds, ban):
            pass
        def allow(self):
            return False

    bucket_allow_result = True
    monkeypatch.setattr("ratelimitpy.ratelimit.TokenBucket", MyBucket)

    with app.app_context():
        g.api_key = "test"
        with pytest.raises(TooManyRequests):
            nothing()


def test_ratelimit_runs(monkeypatch):
    @limit(1, 10, 60)
    def nothing():
        return True

    class MyBucket:
        def __init__(self, tokens, per_seconds, ban):
            pass
        def allow(self):
            return True

    monkeypatch.setattr(
            "ratelimitpy.ratelimit.TokenBucket", MyBucket)
    with app.app_context():
        g.api_key = "test"
        assert nothing()


def test_ratelimit_reuses_existing_bucket(monkeypatch):
    counter = {"times": 0}
    @limit(1, 10, 60)
    def nothing():
        return True

    class MyBucket:
        def __init__(self, tokens, per_seconds, ban):
            counter["times"] += 1
            pass
        def allow(self):
            return True

    monkeypatch.setattr(
            "ratelimitpy.ratelimit.TokenBucket", MyBucket)
    with app.app_context():
        g.api_key = "test"
        nothing()
        nothing()
        assert counter["times"] == 1


def test_ratelimit_uses_config(monkeypatch):
    @limit(1, 10, 60)
    def nothing():
        return True

    params = {}
    class MyBucket:
        def __init__(self, tokens, per_seconds, ban):
            params['tokens'] = tokens
            params['per_seconds'] = per_seconds
            params['ban'] = ban
        def allow(self):
            return True

    monkeypatch.setattr("ratelimitpy.ratelimit.TokenBucket", MyBucket)
    with app.app_context() as ctx:
        ctx.app.config['RATE_LIMITS']['test'] = dict(
                requests=42, per_seconds=43, ban=44)
        g.api_key = "test"
        nothing()
        assert params == dict(tokens=42, per_seconds=43, ban=44)
