#!/usr/bin/env bash
# ==============================================================================
# Sincronizador de DNS Route 53 para Apps Demo (Python & .NET C#)
# ==============================================================================
set -euo pipefail

echo "🔍 Buscando Hosted Zone pública (*realhandsonlabs.net) no Route 53..."
ZONE_INFO=$(aws route53 list-hosted-zones --query "HostedZones[?contains(Name, 'realhandsonlabs.net') && !Config.PrivateZone] | [0]" --output json 2>/dev/null || true)

if [ "$ZONE_INFO" = "null" ] || [ -z "$ZONE_INFO" ]; then
  echo "⚠️ Nenhuma Hosted Zone pública terminando com 'realhandsonlabs.net' encontrada na conta AWS atual."
  exit 0
fi

ZONE_ID=$(echo "$ZONE_INFO" | jq -r '.Id' | sed 's|/hostedzone/||')
ZONE_NAME=$(echo "$ZONE_INFO" | jq -r '.Name' | sed 's/\.$//')

echo "✅ Zona Route 53 encontrada: ${ZONE_NAME} (ID: ${ZONE_ID})"

# Mapeamento dos microserviços para os Services no EKS (subdominio:namespace:service_name)
APPS=(
  "python:apps-demo:python-app"
  "dotnet:apps-demo:dotnet-csharp-app"
)

CHANGES=()
LIVE_URLS=()

for item in "${APPS[@]}"; do
  IFS=":" read -r SUBDOMAIN NAMESPACE SVC_NAME <<< "$item"

  # Espera até 60s pelo hostname do LoadBalancer se estiver provisionando
  ELB_HOSTNAME=""
  for i in $(seq 1 12); do
    ELB_HOSTNAME=$(kubectl get svc "$SVC_NAME" -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null || true)
    if [ -n "$ELB_HOSTNAME" ]; then
      break
    fi
    sleep 5
  done

  if [ -n "$ELB_HOSTNAME" ]; then
    FQDN="${SUBDOMAIN}.${ZONE_NAME}"
    echo "🔗 Associando ${FQDN} -> ${ELB_HOSTNAME}"
    CHANGES+=("{\"Action\":\"UPSERT\",\"ResourceRecordSet\":{\"Name\":\"${FQDN}\",\"Type\":\"CNAME\",\"TTL\":60,\"ResourceRecords\":[{\"Value\":\"${ELB_HOSTNAME}\"}]}}")
    LIVE_URLS+=("${SUBDOMAIN}: http://${FQDN}")
  else
    echo "⏳ Serviço '${SVC_NAME}' no namespace '${NAMESPACE}' ainda não possui LoadBalancer atribuído no EKS."
  fi
done

if [ ${#CHANGES[@]} -gt 0 ]; then
  CHANGES_JSON=$(IFS=,; echo "${CHANGES[*]}")
  BATCH_JSON="{\"Comment\":\"Auto-sync Apps Demo endpoints to Route 53\",\"Changes\":[${CHANGES_JSON}]}"

  aws route53 change-resource-record-sets \
    --hosted-zone-id "$ZONE_ID" \
    --change-batch "$BATCH_JSON" >/dev/null

  echo ""
  echo "=============================================================================="
  echo "🎉 Apps Demo registrados no Route 53 com sucesso!"
  echo "=============================================================================="
  for url in "${LIVE_URLS[@]}"; do
    echo " 👉 ${url}"
  done
  echo "=============================================================================="
fi
