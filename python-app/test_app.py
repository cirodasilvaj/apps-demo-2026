import socket
from app import app


def test_healthz():
    client = app.test_client()
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_ready():
    client = app.test_client()
    res = client.get("/ready")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ready"


def test_prometheus_metrics():
    client = app.test_client()
    res = client.get("/metrics")
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    assert "app_http_requests_total" in body
    assert "app_uptime_seconds" in body


def test_api_info_with_forwarded_ip():
    client = app.test_client()
    res = client.get("/api/info", headers={"X-Forwarded-For": "198.51.100.77"})
    assert res.status_code == 200
    body = res.get_json()
    assert body["language"] == "Python"
    assert body["client_ip"] == "198.51.100.77"
    assert body["hostname"] == socket.gethostname()
    assert "version" in body


def test_html_index_renders():
    client = app.test_client()
    res = client.get("/", headers={"X-Forwarded-For": "198.51.100.77"})
    assert res.status_code == 200
    text = res.get_data(as_text=True)
    assert "Python" in text
    assert "198.51.100.77" in text
