# story: e01s01
# scenario: SC-e01s01-P0-01
from pathlib import Path

from bigbase_canary_python.app import create_app


def test_footer_contains_version():
    client = create_app().test_client()
    resp = client.get("/")
    version = Path("VERSION").read_text().strip()
    assert version.encode() in resp.data


def test_no_raw_placeholder():
    client = create_app().test_client()
    resp = client.get("/")
    assert b"{{VERSION}}" not in resp.data
