# 🚀 Apps Demo 2026 (`cirodasilvaj/apps-demo-2026`)

Repositório de aplicações Web de exemplo construídas em **diferentes linguagens de programação**, todas executando exatamente a mesma função ao serem acessadas:

- **Linguagem** utilizada pela aplicação
- **Versão da Linguagem / Runtime** em execução
- **IP do Solicitante (Client IP)** (`X-Forwarded-For`, `X-Real-IP` ou `RemoteAddr`)
- **Hostname Local** (nome e IP do container / pod Kubernetes)

---

## 📦 Aplicações Disponíveis

| App | Diretório | Linguagem / Stack | Porta Container | Porta Docker Compose |
| :--- | :--- | :--- | :---: | :---: |
| **Python App** | [`python-app/`](./python-app) | Python 3.12 + Flask + Gunicorn | `8080` | `8081` |
| **.NET C# App** | [`dotnet-csharp-app/`](./dotnet-csharp-app) | C# 12 + .NET 8 Minimal API | `8080` | `8082` |

---

## 🌐 Endpoints de Cada Aplicação

Todas as aplicações expõem os mesmos endpoints padronizados:

- **`GET /`** — Interface Web HTML estilizada mostrando **Linguagem**, **Versão**, **IP do Solicitante** e **Hostname Local** (ou retorna JSON se enviado `?format=json` ou header `Accept: application/json`).
- **`GET /api/info`** — Retorna os dados em formato JSON:
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
- **`GET /healthz`** — Health check para probes de `readiness` e `liveness` do Kubernetes.

---

## 🐳 Como Executar Localmente com Docker Compose

```bash
docker compose up --build -d
```

- **Python App**: [http://localhost:8081](http://localhost:8081) (`curl http://localhost:8081/api/info`)
- **.NET C# App**: [http://localhost:8082](http://localhost:8082) (`curl http://localhost:8082/api/info`)

---

## ☸️ Como Fazer Deploy no Kubernetes (EKS / ArgoCD)

```bash
kubectl apply -f k8s/apps-demo.yaml
kubectl get pods,svc -n apps-demo
```

E para registrar no **Backstage Catalog**, importe a URL:
```text
https://github.com/cirodasilvaj/apps-demo-2026/blob/main/catalog-info.yaml
```
