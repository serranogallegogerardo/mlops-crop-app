#!/bin/bash

# Script para configurar CI/CD con Google Cloud Build
# Uso: ./setup-cicd.sh [PROJECT_ID]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Configurando CI/CD Pipeline para Google Cloud${NC}"

# Verificar si se proporcionó PROJECT_ID
if [ -z "$1" ]; then
    echo -e "${YELLOW}⚠️  No se proporcionó PROJECT_ID${NC}"
    echo "Uso: $0 [PROJECT_ID]"
    echo "Ejemplo: $0 mi-proyecto-123"
    exit 1
fi

PROJECT_ID=$1
REGION="southamerica-east1"

echo -e "${GREEN}📋 Configurando proyecto: $PROJECT_ID${NC}"

# 1. Configurar proyecto
echo -e "${YELLOW}1. Configurando proyecto...${NC}"
gcloud config set project $PROJECT_ID

# 2. Habilitar APIs necesarias
echo -e "${YELLOW}2. Habilitando APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 3. Configurar Cloud Build
echo -e "${YELLOW}3. Configurando Cloud Build...${NC}"
gcloud config set builds/region $REGION

# 4. Crear Service Account para CI/CD
echo -e "${YELLOW}4. Creando Service Account...${NC}"
SA_NAME="cicd-service-account"
SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

# Crear service account si no existe
gcloud iam service-accounts create $SA_NAME \
    --display-name="CI/CD Service Account" \
    --description="Service account for CI/CD pipeline" || echo "Service account ya existe"

# 5. Asignar roles necesarios
echo -e "${YELLOW}5. Asignando roles...${NC}"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/cloudbuild.builds.builder"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/iam.serviceAccountUser"

# 6. Crear y descargar la clave del service account
echo -e "${YELLOW}6. Creando clave del Service Account...${NC}"
gcloud iam service-accounts keys create cicd-key.json \
    --iam-account=$SA_EMAIL

echo -e "${GREEN}✅ Configuración completada!${NC}"
echo ""
echo -e "${YELLOW}📝 Próximos pasos:${NC}"
echo "1. Sube tu código a GitHub"
echo "2. Crea las ramas: develop, qa, main"
echo "3. En GitHub, ve a Settings > Secrets and variables > Actions"
echo "4. Agrega estos secrets:"
echo "   - GCP_PROJECT_ID: $PROJECT_ID"
echo "   - GCP_SA_KEY: (contenido del archivo cicd-key.json)"
echo ""
echo -e "${YELLOW}🔗 URLs de los ambientes:${NC}"
echo "DEV: https://streamlit-app-dev-[hash]-$REGION.a.run.app"
echo "QA:  https://streamlit-app-qa-[hash]-$REGION.a.run.app"
echo "PROD: https://streamlit-app-prod-[hash]-$REGION.a.run.app"
echo ""
echo -e "${RED}⚠️  IMPORTANTE: Guarda el archivo cicd-key.json de forma segura!${NC}" 