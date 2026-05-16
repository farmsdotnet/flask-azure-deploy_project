import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Flask' in response.data

def test_api_hello(client):
    """Test the API endpoint."""
    response = client.get('/api/hello')
    assert response.status_code == 200
    assert response.json['message'] == 'Hello from Flask API!'

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_404_error(client):
    """Test that invalid routes return 404."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
