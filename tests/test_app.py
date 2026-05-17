import io
from unittest.mock import patch, MagicMock
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ── Page load ──────────────────────────────────────────────────────────────

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Text to Speech' in response.data


def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_404_error(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404


# ── /synthesize — input validation (no network calls needed) ───────────────

def test_synthesize_no_input_returns_400(client):
    """Empty form should be rejected."""
    response = client.post('/synthesize', data={})
    assert response.status_code == 400
    assert b'No text provided' in response.data


def test_synthesize_empty_text_returns_400(client):
    response = client.post('/synthesize', data={'text': '   '})
    assert response.status_code == 400
    assert b'No text provided' in response.data


def test_synthesize_text_too_long_returns_400(client):
    response = client.post('/synthesize', data={'text': 'a' * 5001})
    assert response.status_code == 400
    assert b'character limit' in response.data


def test_synthesize_non_txt_file_returns_400(client):
    data = {'file': (io.BytesIO(b'hello'), 'audio.mp3')}
    response = client.post('/synthesize', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'.txt' in response.data


def test_synthesize_non_ascii_file_returns_400(client):
    data = {'file': (io.BytesIO('héllo'.encode('utf-8')), 'note.txt')}
    response = client.post('/synthesize', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'ASCII' in response.data


# ── /synthesize — successful conversion (gTTS mocked) ─────────────────────

def _mock_tts():
    """Return a mock gTTS that writes a minimal MP3-like byte sequence."""
    mock = MagicMock()
    mock.write_to_fp.side_effect = lambda fp: fp.write(b'\xff\xfb' + b'\x00' * 128)
    return mock


def test_synthesize_text_returns_audio(client):
    with patch('app.gTTS', return_value=_mock_tts()):
        response = client.post('/synthesize', data={'text': 'Hello world'})
    assert response.status_code == 200
    assert response.content_type == 'audio/mpeg'


def test_synthesize_txt_file_returns_audio(client):
    data = {'file': (io.BytesIO(b'Hello from a file'), 'sample.txt')}
    with patch('app.gTTS', return_value=_mock_tts()):
        response = client.post('/synthesize', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.content_type == 'audio/mpeg'
