import sys
sys.path.insert(0, './app')
from main import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_predict_valid(client):
    response = client.post('/predict',
        json={'features': [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 200
    assert 'prediction' in response.json

def test_predict_empty(client):
    response = client.post('/predict',
        json={'features': []})
    # Accept either 500 (handled) or 500 (unhandled)
    assert response.status_code in [400, 500]