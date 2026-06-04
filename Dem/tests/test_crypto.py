import base64
import pytest


def test_generate_aes_key(client):
    resp = client.post("/api/tools/crypto/aes/generate-key")
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert "key" in data["data"]
    assert "iv" in data["data"]
    key_bytes = base64.b64decode(data["data"]["key"])
    assert len(key_bytes) == 32


def test_aes_encrypt_decrypt_roundtrip(client):
    key_resp = client.post("/api/tools/crypto/aes/generate-key")
    key_data = key_resp.json()
    key = key_data["data"]["key"]

    enc_resp = client.post("/api/tools/crypto/aes/encrypt", json={
        "plaintext": "Hello, OnlineTools!",
        "key": key,
    })
    assert enc_resp.status_code == 200
    enc_data = enc_resp.json()
    assert enc_data["code"] == 0
    ciphertext = enc_data["data"]["ciphertext"]
    iv = enc_data["data"]["iv"]

    dec_resp = client.post("/api/tools/crypto/aes/decrypt", json={
        "ciphertext": ciphertext,
        "key": key,
        "iv": iv,
    })
    assert dec_resp.status_code == 200
    dec_data = dec_resp.json()
    assert dec_data["code"] == 0
    assert dec_data["data"]["plaintext"] == "Hello, OnlineTools!"
