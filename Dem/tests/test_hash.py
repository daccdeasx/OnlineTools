import pytest


def test_compute_hash_sha256(client):
    resp = client.post("/api/tools/hash/compute", json={
        "text": "hello world",
        "algorithm": "sha256",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["algorithm"] == "sha256"
    assert len(data["data"]["hash"]) == 64


def test_compute_hash_md5(client):
    resp = client.post("/api/tools/hash/compute", json={
        "text": "hello",
        "algorithm": "md5",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert data["data"]["algorithm"] == "md5"
    assert len(data["data"]["hash"]) == 32


def test_compute_hash_unsupported(client):
    resp = client.post("/api/tools/hash/compute", json={
        "text": "test",
        "algorithm": "sha99",
    })
    assert resp.status_code == 422


def test_compute_hash_empty_text(client):
    resp = client.post("/api/tools/hash/compute", json={
        "text": "",
        "algorithm": "sha256",
    })
    assert resp.status_code == 422
