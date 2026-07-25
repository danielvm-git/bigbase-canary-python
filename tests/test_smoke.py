# story: e01s01
# scenario: SC-e01s01-P0-01
from bigbase_canary_python.app import create_app


def test_footer_contains_version():
    client = create_app().test_client()
    resp = client.get("/")
    assert b"0.1.0" in resp.data
