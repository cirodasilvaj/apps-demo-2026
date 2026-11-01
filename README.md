# 🚀 Apps Demo 2026 (`cirodasilvaj/apps-demo-2026`)

Sample web applications built in **different programming languages**, all performing the exact same function when accessed:

- **Programming Language** used by the application
- **Language / Runtime Version** currently executing
- **Requester IP Address (Client IP)** (`X-Forwarded-For`, `X-Real-IP`, or `RemoteAddr`)
- **Local Hostname** (container / Kubernetes pod hostname and IP)

---

## 📦 Available Applications

| App | Directory | Language / Stack | Container Port | Docker Compose Port |
| :--- | :--- | :--- | :---: | :---: |
| **Python App** | [`python-app/`](./python-app) | Python 3.12 + Flask + Gunicorn | `8080` | `8081` |
| **.NET C# App** | [`dotnet-csharp-app/`](./dotnet-csharp-app) | C# 12 + .NET 8 Minimal API | `8080` | `8082` |

---

## 🌐 Standardized Endpoints

Every application exposes the same standardized endpoints:

- **`GET /`** — Styled HTML Web UI displaying **Language**, **Version**, **Client IP**, and **Local Hostname** (or returns JSON when queried with `?format=json` or `Accept: application/json`).
- **`GET /api/info`** — Returns the metadata payload in JSON format:
  ```json
  {
    "language": "Python",
    "version": "Python 3.12.9 (CPython)",
    "app_version": "1.0.0",
    "client_ip": "203.0.113.42",
    "hostname": "python-app-6d8f9b7c4-x9k2p",
    "local_ip": "10.0.1.45",
    "timestamp": "2026-10-31T20:55:00.000000+00:00"
  }
  ```
- **`GET /healthz`** — Health check endpoint for Kubernetes `readiness` and `liveness` probes.

---

## 🐳 Run Locally with Docker Compose

```bash
docker compose up --build -d
```

- **Python App**: [http://localhost:8081](http://localhost:8081) (`curl http://localhost:8081/api/info`)
- **.NET C# App**: [http://localhost:8082](http://localhost:8082) (`curl http://localhost:8082/api/info`)

---

## ☸️ Deploy to Kubernetes (EKS / ArgoCD)

```bash
kubectl apply -f k8s/apps-demo.yaml
kubectl get pods,svc -n apps-demo
```

To register in the **Backstage Catalog**, import the URL:
```text
https://github.com/cirodasilvaj/apps-demo-2026/blob/main/catalog-info.yaml
```
