import pytest


def test_health_check(client):
    resp = client.get("/api/system/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["status"] == "healthy"
    assert "version" in data["data"]


def test_ping(client):
    resp = client.get("/api/system/ping")
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"] == "pong"
