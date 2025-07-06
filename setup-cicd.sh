#!/bin/bash

# Script to configure CI/CD with Google Cloud Build
# Usage: ./setup-cicd.sh [PROJECT_ID]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Configuring CI/CD Pipeline for Google Cloud${NC}"

# Check if PROJECT_ID is provided
if [ -z "$1" ]; then
    echo -e "${YELLOW}⚠️  PROJECT_ID not provided${NC}"
    echo "Usage: $0 [PROJECT_ID]"
    echo "Example: $0 my-project-123"
    exit 1
fi

PROJECT_ID=$1
REGION="southamerica-east1"

echo -e "${GREEN}📋 Configuring project: $PROJECT_ID${NC}"

# 1. Configure project
echo -e "${YELLOW}1. Configuring project...${NC}"
gcloud config set project $PROJECT_ID

# 2. Enable necessary APIs
echo -e "${YELLOW}2. Enabling APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 3. Configure Cloud Build
echo -e "${YELLOW}3. Configuring Cloud Build...${NC}"
gcloud config set builds/region $REGION

# 4. Create Service Account for CI/CD
echo -e "${YELLOW}4. Creating Service Account...${NC}"
SA_NAME="cicd-service-account"
SA_EMAIL="$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com"

# Create service account if it doesn't exist
gcloud iam service-accounts create $SA_NAME \
    --display-name="CI/CD Service Account" \
    --description="Service account for CI/CD pipeline" || echo "Service account already exists"

# 5. Assign necessary roles
echo -e "${YELLOW}5. Assigning roles...${NC}"
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

# 6. Create and download service account key
echo -e "${YELLOW}6. Creating Service Account key...${NC}"
gcloud iam service-accounts keys create cicd-key.json \
    --iam-account=$SA_EMAIL

echo -e "${GREEN}✅ Configuration completed!${NC}"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Push your code to GitHub"
echo "2. Create branches: develop, qa, main"
echo "3. In GitHub, go to Settings > Secrets and variables > Actions"
echo "4. Add these secrets:"
echo "   - GCP_PROJECT_ID: $PROJECT_ID"
echo "   - GCP_SA_KEY: (content of cicd-key.json file)"
echo ""
echo -e "${YELLOW}🔗 Environment URLs:${NC}"
echo "DEV: https://streamlit-app-dev-[hash]-$REGION.a.run.app"
echo "QA:  https://streamlit-app-qa-[hash]-$REGION.a.run.app"
echo "PROD: https://streamlit-app-prod-[hash]-$REGION.a.run.app"
echo ""
echo -e "${RED}⚠️  IMPORTANT: Keep the cicd-key.json file secure!${NC}" 