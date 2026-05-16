import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Flask' in response.data


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}


def test_api_message(client):
    response = client.get('/api/message')
    assert response.status_code == 200
    assert 'message' in response.json
    assert response.json['message'] == 'Hello from Flask API!'


def test_404(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
