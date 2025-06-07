# tests/test_send_email_endpoint.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

#Class to help us to test sending emails (it's like SESMailer implementation). Instead of SESMailer we use DummyMailer
class DummyMailer:
    def send(self, to, subject, html_body, from_alias=None, cc=None, bcc=None, reply_to=None):
        return "dummy-message-id"

@pytest.fixture
def patch_mailer(monkeypatch):
    monkeypatch.setattr(
        "app.api.controllers._get_mailer",
        lambda: DummyMailer()
    )

#Dummy will help us to test the emails without sending real emails (we don't test SES)
def test_send_email_success_with_dummy(patch_mailer):
    client = TestClient(app)
    payload = {
        "to": ["test@test.com"],
        "template": "test_email",
        "language_code": "es"
    }
    response = client.post("/api/send-email", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "sent"
    assert data["message_id"] == "dummy-message-id"

def test_send_email_success_with_dummy_with_vars(patch_mailer):
    client = TestClient(app)
    payload = {
        "to": ["test@test.com"],
        "template": "test_email_with_vars",
        "language_code": "es",
        "title_variables": {
            "name": "Test",
            "surname": "Email"
        },
        "variables": {
            "name": "Test",
            "surname": "Email"
        }
    }
    response = client.post("/api/send-email", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "sent"
    assert data["message_id"] == "dummy-message-id"

@pytest.mark.integration
def test_send_email_success_realmailer():
    client = TestClient(app)
    payload = {
        "to": ["test@test.com"],
        "template": "test_email",
        "language_code": "es"
    }
    response = client.post("/api/send-email", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "sent"
    assert "message_id" in data

@pytest.mark.integration
def test_send_email_success_realmailer_with_vars():
    client = TestClient(app)
    payload = {
        "to": ["test@test.com"],
        "template": "test_email_with_vars",
        "language_code": "es",
        "title_variables": {
            "name": "Test",
            "surname": "Email"
        },
        "variables": {
            "name": "Test",
            "surname": "Email"
        }
    }
    response = client.post("/api/send-email", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "sent"
    assert "message_id" in data


def test_send_email_invalid_template():
    client = TestClient(app)
    payload = {
        "to": ["test@example.com"],
        "template": "dont_exist",
        "language_code": "en"
    }
    response = client.post("/api/send-email", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "error"
    assert "does not exist" in data["message"]
