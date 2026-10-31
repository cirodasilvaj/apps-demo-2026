FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
WORKDIR /src

COPY DotnetDemoApp.csproj .
RUN dotnet restore "DotnetDemoApp.csproj"

COPY Program.cs .
RUN dotnet publish "DotnetDemoApp.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS final
LABEL org.opencontainers.image.source="https://github.com/cirodasilvaj/apps-demo-2026"
WORKDIR /app

ENV ASPNETCORE_URLS=http://+:8080 \
    PORT=8080

COPY --from=build /app/publish .

USER $APP_UID
EXPOSE 8080

ENTRYPOINT ["dotnet", "DotnetDemoApp.dll"]
