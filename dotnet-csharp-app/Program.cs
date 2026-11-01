using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text.Json;
using Microsoft.AspNetCore.HttpOverrides;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<ForwardedHeadersOptions>(options =>
{
    options.ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto;
    options.KnownNetworks.Clear();
    options.KnownProxies.Clear();
});

var app = builder.Build();
app.UseForwardedHeaders();

var startTime = DateTime.UtcNow;
const string LanguageName = "C# (.NET)";
var languageVersion = $"{RuntimeInformation.FrameworkDescription} (C# 12 / {RuntimeInformation.OSArchitecture})";
var appVersion = Environment.GetEnvironmentVariable("APP_VERSION") ?? "1.0.0";
var fluentdHost = Environment.GetEnvironmentVariable("FLUENTD_HOST") ?? "fluentd.logging.svc.cluster.local";
var fluentdPort = Environment.GetEnvironmentVariable("FLUENTD_PORT") ?? "24224";

long requestsRoot = 0;
long requestsApiInfo = 0;
long requestsHealthz = 0;
long requestsMetrics = 0;

void EmitFluentdLog(string eventName, string path, string clientIp)
{
    var logRecord = new
    {
        time = DateTime.UtcNow.ToString("O"),
        app = "dotnet-csharp-app",
        language = LanguageName,
        @event = eventName,
        path,
        client_ip = clientIp,
        hostname = Dns.GetHostName(),
        fluentd_target = $"{fluentdHost}:{fluentdPort}"
    };
    Console.WriteLine(JsonSerializer.Serialize(logRecord));
}

static string GetClientIp(HttpContext context)
{
    if (context.Request.Headers.TryGetValue("X-Forwarded-For", out var forwardedFor) &&
        !string.IsNullOrWhiteSpace(forwardedFor))
    {
        return forwardedFor.ToString().Split(',')[0].Trim();
    }

    if (context.Request.Headers.TryGetValue("X-Real-IP", out var realIp) &&
        !string.IsNullOrWhiteSpace(realIp))
    {
        return realIp.ToString().Trim();
    }

    return context.Connection.RemoteIpAddress?.ToString() ?? "unknown";
}

static string GetLocalIp(string hostname)
{
    try
    {
        var addresses = Dns.GetHostAddresses(hostname);
        var ipv4 = addresses.FirstOrDefault(ip => ip.AddressFamily == AddressFamily.InterNetwork);
        return ipv4?.ToString() ?? addresses.FirstOrDefault()?.ToString() ?? "127.0.0.1";
    }
    catch
    {
        return "127.0.0.1";
    }
}

object BuildPayload(HttpContext context)
{
    var hostname = Dns.GetHostName();
    return new
    {
        language = LanguageName,
        version = languageVersion,
        app_version = appVersion,
        client_ip = GetClientIp(context),
        hostname = hostname,
        local_ip = GetLocalIp(hostname),
        timestamp = DateTime.UtcNow.ToString("O")
    };
}

app.MapGet("/", (HttpContext context) =>
{
    var hostname = Dns.GetHostName();
    var localIp = GetLocalIp(hostname);
    var clientIp = GetClientIp(context);
    var timestamp = DateTime.UtcNow.ToString("O");

    if (context.Request.Query["format"] == "json" ||
        context.Request.Headers.Accept.ToString().Contains("application/json", StringComparison.OrdinalIgnoreCase))
    {
        return Results.Json(BuildPayload(context));
    }

    var html = $$"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Apps Demo 2026 - {{LanguageName}}</title>
      <style>
        :root {
          --bg: #0f172a;
          --card: #1e293b;
          --accent: #a855f7;
          --badge: #c084fc;
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
          background: rgba(168, 85, 247, 0.15);
          color: var(--badge);
          border: 1px solid rgba(168, 85, 247, 0.4);
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
          <span class="badge">💜 {{LanguageName}}</span>
        </div>
        <div class="grid">
          <div class="item">
            <div class="label">Linguagem</div>
            <div class="value">{{LanguageName}}</div>
          </div>
          <div class="item">
            <div class="label">Versão da Linguagem / Runtime</div>
            <div class="value">{{languageVersion}}</div>
          </div>
          <div class="item">
            <div class="label">IP do Solicitante (Client IP)</div>
            <div class="value">{{clientIp}}</div>
          </div>
          <div class="item">
            <div class="label">Hostname Local (Container / Pod)</div>
            <div class="value">{{hostname}} ({{localIp}})</div>
          </div>
        </div>
        <div class="footer">
          <span>Timestamp (UTC): {{timestamp}}</span>
          <span><a href="/api/info">JSON (/api/info)</a> | <a href="/healthz">Health (/healthz)</a></span>
        </div>
      </div>
    </body>
    </html>
    """;

    return Results.Content(html, "text/html; charset=utf-8");
});

app.MapGet("/api/info", (HttpContext context) =>
{
    Interlocked.Increment(ref requestsApiInfo);
    EmitFluentdLog("api_info_request", "/api/info", GetClientIp(context));
    return Results.Json(BuildPayload(context));
});

app.MapGet("/metrics", () =>
{
    Interlocked.Increment(ref requestsMetrics);
    var uptime = (DateTime.UtcNow - startTime).TotalSeconds;
    var body = string.Join("\n", new[]
    {
        "# HELP app_http_requests_total Total HTTP requests handled by the application",
        "# TYPE app_http_requests_total counter",
        $"app_http_requests_total{{app=\"dotnet-csharp-app\",language=\"CSharp\",endpoint=\"/\"}} {Interlocked.Read(ref requestsRoot)}",
        $"app_http_requests_total{{app=\"dotnet-csharp-app\",language=\"CSharp\",endpoint=\"/api/info\"}} {Interlocked.Read(ref requestsApiInfo)}",
        $"app_http_requests_total{{app=\"dotnet-csharp-app\",language=\"CSharp\",endpoint=\"/healthz\"}} {Interlocked.Read(ref requestsHealthz)}",
        $"app_http_requests_total{{app=\"dotnet-csharp-app\",language=\"CSharp\",endpoint=\"/metrics\"}} {Interlocked.Read(ref requestsMetrics)}",
        "# HELP app_uptime_seconds Application uptime in seconds",
        "# TYPE app_uptime_seconds gauge",
        $"app_uptime_seconds{{app=\"dotnet-csharp-app\",language=\"CSharp\"}} {uptime:F2}",
        ""
    });
    return Results.Text(body, "text/plain; version=0.0.4");
});

app.MapGet("/healthz", () =>
{
    Interlocked.Increment(ref requestsHealthz);
    return Results.Json(new
    {
        status = "ok",
        language = LanguageName,
        hostname = Dns.GetHostName()
    });
});

var port = Environment.GetEnvironmentVariable("PORT") ?? "8080";
app.Run($"http://0.0.0.0:{port}");
