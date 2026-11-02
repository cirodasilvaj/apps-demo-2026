# Python 3.12 Flask Microservice (`python-demo-app`)

Welcome to the **Python 3.12 Flask Demo Microservice** technical documentation!

## Architecture & Overview
* **Runtime:** Python 3.12 (Flask)
* **Observability:**
  - **Metrics:** `/metrics` endpoint exposed in Prometheus format.
  - **Logs:** Structured JSON sent directly to `stdout` and collected by Fluentd into Grafana Loki.
  - **Probes:** `/healthz` (liveness) and `/ready` (readiness).
* **Quality & Security:** SonarQube Quality Gate with automated SAST scanning and test coverage.
* **Continuous Delivery:** GitOps deployment managed by ArgoCD on Amazon EKS.
* **Networking:** LoadBalancer with AWS Route 53 dynamic DNS and AWS ACM Wildcard HTTPS termination.

## Endpoints
| Route | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | HTML status dashboard & JSON info |
| `/api/info` | `GET` | JSON payload with runtime, host, and client IP |
| `/metrics` | `GET` | Prometheus telemetry metrics |
| `/healthz` | `GET` | Kubernetes Liveness Probe |
| `/ready` | `GET` | Kubernetes Readiness Probe |
