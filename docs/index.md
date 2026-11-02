# Apps Demo 2026 Ecosystem

Welcome to the **Apps Demo 2026** technical documentation on Backstage.

## Architecture & Microservices

The ecosystem consists of two reference microservices designed to validate enterprise platform requirements:

1. **Python 3.12 Flask Microservice (`python-app`):**
   - High-throughput asynchronous REST API running on Gunicorn with `gthread` workers.
   - Structured JSON logging (`timestamp`, `level`, `service`, `duration_ms`, `trace_id`).
   - Telemetry exposed on `/metrics` (Prometheus) and logs ingested into Grafana Loki.
   - Probes: `/healthz` (liveness) and `/ready` (readiness).

2. **.NET 8 C# Minimal API Microservice (`dotnet-csharp-app`):**
   - Modern, high-performance C# 12 Minimal API on Kestrel.
   - Native structured JSON logging compatible with Fluentd/Loki schema.
   - Built-in Prometheus metrics exposition at `/metrics`.
   - Probes: `/healthz` (liveness) and `/ready` (readiness).

## Infrastructure & Delivery

- **Kubernetes:** Amazon EKS 1.30 with automated Horizontal Pod Autoscaling.
- **GitOps:** Continuous synchronization via ArgoCD.
- **Networking:** AWS Classic LoadBalancer with Dual-Port (80 HTTP / 443 HTTPS TLS ACM) and Route 53 Dynamic DNS.
- **Observability:** Custom Golden Signals Dashboards provisioned as code in Grafana (`UID: python-demo-app-dashboard` and `UID: dotnet-csharp-demo-app-dashboard`).
- **Quality & Security:** Automated SonarQube Quality Gate scans on every pull request.
