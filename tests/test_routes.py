"""Tests for DLX Solution website routes."""
import pytest

from app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Home page returns 200."""
    rv = client.get("/")
    assert rv.status_code == 200


def test_about_page(client):
    """About page returns 200."""
    rv = client.get("/about")
    assert rv.status_code == 200


def test_services_page(client):
    """Services page returns 200."""
    rv = client.get("/services")
    assert rv.status_code == 200


def test_contact_page(client):
    """Contact page returns 200."""
    rv = client.get("/contact")
    assert rv.status_code == 200


def test_login_page(client):
    """Login page returns 200 and links to Zoho."""
    rv = client.get("/login")
    assert rv.status_code == 200
    data = rv.get_data(as_text=True)
    assert "DLX Mail" in data


def test_language_switch(client):
    """Language query param works."""
    rv = client.get("/?lang=zh")
    assert rv.status_code == 200
    data = rv.get_data(as_text=True)
    assert "使命" in data or "首頁" in data or "我們的" in data


def test_french_language(client):
    """French language works."""
    rv = client.get("/?lang=fr")
    assert rv.status_code == 200
    data = rv.get_data(as_text=True)
    assert "Accueil" in data or "Contact" in data or "À propos" in data
