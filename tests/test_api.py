from falcon import testing
import pytest

import application as api

DEFAULT_LANG = 'en_us'
DEFAULT_APP_ID = 'test_app_123-456'


@pytest.fixture()
def client():
    return testing.TestClient(api.initialize())


def test_liveness(client):
    result = client.simulate_get('/liveness')
    assert 'data' in result.json
    assert result.json['data']['type'] == 'liveness'
    assert result.json['data']['attributes']['id'] == 0
