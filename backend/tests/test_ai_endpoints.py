import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.main import app

client = TestClient(app)


def test_ai_health():
    r = client.get('/api/v1/ai/health')
    assert r.status_code == 200
    assert r.json().get('service')


@patch.dict(os.environ, {'OPENROUTER_API_KEY': ''})
def test_ai_summarize_with_content_mock():
    payload = [{
        "path": "maths.py",
        "content": "def add(a,b): return a+b",
        "encoding": "utf-8",
        "size": 24,
        "sha": "abc123"
    }]
    r = client.post('/api/v1/ai/summarize-tests-with-content?framework=pytest', json=payload)
    assert r.status_code == 200
    body = r.json()
    assert 'summaries' in body
    assert isinstance(body['summaries'], list)


