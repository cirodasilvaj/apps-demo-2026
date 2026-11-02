import json
import os
import platform
import socket
import sys
import time
from datetime import datetime, timezone
from flask import Flask, Response, jsonify, render_template_string, request

app = Flask(__name__)
START_TIME = time.time()

APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
FLUENTD_HOST = os.environ.get("FLUENTD_HOST", "fluentd.logging.svc.cluster.local")
FLUENTD_PORT = os.environ.get("FLUENTD_PORT", "24224")
LANGUAGE_NAME = "Python"
LANGUAGE_VERSION = f"Python {platform.python_version()} ({platform.python_implementation()})"

METRICS_COUNTERS = {
    "/": 0,
    "/api/info": 0,
    "/healthz": 0,
    "/metrics": 0,
}


def emit_fluentd_log(event_type: str, path: str, client_ip: str, status_code: int = 200, duration_ms: float = 0.0) -> None:
    trace_id = "trace-default"
    method = "GET"
    if request:
        try:
            trace_id = request.headers.get("X-Trace-Id", request.headers.get("X-Request-Id", "trace-default"))
            method = request.method
        except RuntimeError:
            pass
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": "INFO" if status_code < 400 else "ERROR",
        "service": "python-app",
        "app": "python-app",
        "language": LANGUAGE_NAME,
        "event": event_type,
        "message": f"{method} {path} - {status_code} ({duration_ms:.2f}ms)",
        "http_method": method,
        "endpoint": path,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 2),
        "client_ip": client_ip,
        "hostname": socket.gethostname(),
        "trace_id": trace_id,
        "fluentd_target": f"{FLUENTD_HOST}:{FLUENTD_PORT}",
    }
    print(json.dumps(record), file=sys.stdout, flush=True)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Apps Demo 2026 - {{ info.language }}</title>
  <style>
    :root {
      --bg: #0f172a;
      --card: #1e293b;
      --accent: #38bdf8;
      --badge: #eab308;
      --text: #f8fafc;
      --muted: #94a3b8;
      --border: #334155;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .container {
      width: 100%;
      max-width: 680px;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
      padding-bottom: 20px;
      margin-bottom: 24px;
    }
    .title {
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--accent);
    }
    .badge {
      background: rgba(234, 179, 8, 0.15);
      color: var(--badge);
      border: 1px solid rgba(234, 179, 8, 0.4);
      padding: 6px 14px;
      border-radius: 9999px;
      font-weight: 600;
      font-size: 0.875rem;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
    }
    .item {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px 20px;
    }
    .label {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--muted);
      margin-bottom: 6px;
    }
    .value {
      font-family: 'JetBrains Mono', 'Fira Code', monospace;
      font-size: 1.125rem;
      font-weight: 600;
      color: var(--text);
      word-break: break-all;
    }
    .footer {
      margin-top: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.8rem;
      color: var(--muted);
    }
    .footer a {
      color: var(--accent);
      text-decoration: none;
    }
    .footer a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title">🚀 Apps Demo 2026</div>
      <span class="badge">🐍 {{ info.language }}</span>
    </div>
    <div class="grid">
      <div class="item">
        <div class="label">Linguagem</div>
        <div class="value">{{ info.language }}</div>
      </div>
      <div class="item">
        <div class="label">Versão da Linguagem / Runtime</div>
        <div class="value">{{ info.version }}</div>
      </div>
      <div class="item">
        <div class="label">IP do Solicitante (Client IP)</div>
        <div class="value">{{ info.client_ip }}</div>
      </div>
      <div class="item">
        <div class="label">Hostname Local (Container / Pod)</div>
        <div class="value">{{ info.hostname }} ({{ info.local_ip }})</div>
      </div>
    </div>
    <div class="footer">
      <span>Timestamp (UTC): {{ info.timestamp }}</span>
      <span><a href="/api/info">JSON (/api/info)</a> | <a href="/healthz">Health (/healthz)</a></span>
    </div>
  </div>
</body>
</html>
"""


def get_client_ip() -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip.strip()
    return request.remote_addr or "unknown"


def get_local_ip(hostname: str) -> str:
    try:
        return socket.gethostbyname(hostname)
    except Exception:
        return "127.0.0.1"


def build_payload() -> dict:
    hostname = socket.gethostname()
    return {
        "language": LANGUAGE_NAME,
        "version": LANGUAGE_VERSION,
        "app_version": APP_VERSION,
        "client_ip": get_client_ip(),
        "hostname": hostname,
        "local_ip": get_local_ip(hostname),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.route("/")
def index():
    METRICS_COUNTERS["/"] += 1
    info = build_payload()
    emit_fluentd_log("index_request", "/", info["client_ip"])
    if request.args.get("format") == "json" or "application/json" in request.headers.get("Accept", ""):
        return jsonify(info)
    return render_template_string(HTML_TEMPLATE, info=info)


@app.route("/api/info")
def api_info():
    METRICS_COUNTERS["/api/info"] += 1
    info = build_payload()
    emit_fluentd_log("api_info_request", "/api/info", info["client_ip"])
    return jsonify(info)


@app.route("/metrics")
def metrics():
    METRICS_COUNTERS["/metrics"] += 1
    uptime = max(0.0, time.time() - START_TIME)
    lines = [
        "# HELP app_http_requests_total Total HTTP requests handled by the application",
        "# TYPE app_http_requests_total counter",
    ]
    for endpoint, count in METRICS_COUNTERS.items():
        lines.append(
            f'app_http_requests_total{{app="python-app",language="Python",endpoint="{endpoint}"}} {count}'
        )
    lines.extend(
        [
            "# HELP app_uptime_seconds Application uptime in seconds",
            "# TYPE app_uptime_seconds gauge",
            f'app_uptime_seconds{{app="python-app",language="Python"}} {uptime:.2f}',
        ]
    )
    return Response("\n".join(lines) + "\n", mimetype="text/plain; version=0.0.4")


@app.route("/healthz")
def healthz():
    METRICS_COUNTERS["/healthz"] += 1
    return jsonify({"status": "ok", "language": LANGUAGE_NAME, "hostname": socket.gethostname()})


@app.route("/ready")
def ready():
    return jsonify({"status": "ready", "language": LANGUAGE_NAME, "hostname": socket.gethostname()})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
