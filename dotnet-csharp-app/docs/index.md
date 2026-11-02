# .NET 8 C# Minimal API Microservice (`dotnet-csharp-demo-app`)

Welcome to the **.NET 8 C# Minimal API Demo Microservice** technical documentation!

## Architecture & Overview
* **Runtime:** .NET 8 (ASP.NET Core Minimal API)
* **Observability:**
  - **Metrics:** `/metrics` endpoint exposed in Prometheus format.
  - **Logs:** Structured JSON sent directly to `stdout` and collected by Fluentd into Grafana Loki.
  - **Probes:** `/healthz` (liveness) and `/ready` (readiness).
* **Quality & Security:** SonarQube Quality Gate with automated SAST scanning and build validation.
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
