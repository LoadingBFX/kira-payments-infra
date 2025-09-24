import pytest, httpx

BASE = "http://localhost:8000"

def test_health():
    r = httpx.get(f"{BASE}/healthz", timeout=5.0)
    assert r.status_code == 200

def test_transfer_success_vendorA():
    r = httpx.post(f"{BASE}/transfer", json={"amount":100,"vendor":"vendorA","txhash":"0xabc"}, timeout=5.0)
    assert r.status_code == 200
    assert r.json()["status"] in ("success","pending")

def test_transfer_not_found_tx():
    r = httpx.post(f"{BASE}/transfer", json={"amount":50,"vendor":"vendorA","txhash":"bad"}, timeout=5.0)
    assert r.status_code == 404

