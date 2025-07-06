# 🌱 Crop Recommendation System - Streamlit & Google Cloud

This project implements an SVM model for crop recommendation based on soil and environmental characteristics, deployed using Streamlit and Google Cloud with a complete CI/CD pipeline.

## 📋 Project Overview

The system uses machine learning to recommend the best crop type based on:
- **Nitrogen** content in soil
- **Phosphorus** content in soil  
- **Potassium** content in soil
- **Temperature** conditions
- **Humidity** levels
- **pH** level of soil
- **Rainfall** amount

## 🚀 Quick Start

### Local Development

1. **Create Python environment:**
```bash
conda create -n crop-env python=3.7
conda activate crop-env
pip install -r requirements.txt
```

2. **Run the application:**
```bash
streamlit run app.py
```

### Docker (Production-like)

```bash
# Build Docker image
sudo docker build -t crop-streamlit-app .

# Run container
sudo docker run -p 8080:8080 -e PORT=8080 crop-streamlit-app
```

Access at: [http://localhost:8080](http://localhost:8080)

## 🏗️ Model Training

The SVM model was trained using the Jupyter notebook: [CropPrediction.ipynb](CropPrediction.ipynb)

### Training Process:
1. Load crop recommendation dataset
2. Split data into training/testing sets (80/20)
3. Train SVM model with linear kernel
4. Achieved 99.3% accuracy on test data
5. Save model as `pickle_model.pkl`

## 🚀 CI/CD Pipeline

This project includes a complete CI/CD pipeline with three environments:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   develop   │───▶│     qa      │───▶│    master   │
│   (DEV)     │    │    (QA)     │    │   (PROD)    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Environment Configuration

| Environment | RAM | CPU | Max Instances | Purpose |
|-------------|-----|-----|---------------|---------|
| **DEV**     | 512Mi | 1 | 2 | Development and testing |
| **QA**      | 1Gi | 1 | 3 | Integration testing |
| **PROD**    | 2Gi | 2 | 10 | Production |

### Deployment URLs

| Environment | URL Pattern |
|-------------|-------------|
| **DEV** | `https://streamlit-app-dev-[hash]-southamerica-east1.a.run.app` |
| **QA** | `https://streamlit-app-qa-[hash]-southamerica-east1.a.run.app` |
| **PROD** | `https://streamlit-app-prod-[hash]-southamerica-east1.a.run.app` |

## 🔄 Deployment Process

### 1. Development (DEV)
```bash
git checkout develop
git add . && git commit -m "feat: new feature"
git push origin develop
```
**✅ Automatically deploys to DEV**

### 2. Testing (QA)
```bash
git checkout qa
git merge develop
git push origin qa
```
**✅ Automatically deploys to QA**

### 3. Production (PROD)
```bash
git checkout master
git merge qa
git push origin master
```
**✅ Automatically deploys to PROD**

## 🛠️ Setup CI/CD

### 1. Run Setup Script
```bash
./setup-cicd.sh [YOUR_PROJECT_ID]
```

### 2. Configure GitHub
1. Create repository on GitHub
2. Create branches:
   ```bash
   git checkout -b develop
   git checkout -b qa
   git checkout main
   ```
3. Add GitHub Secrets:
   - `GCP_PROJECT_ID`: Your Google Cloud project ID
   - `GCP_SA_KEY`: Content of generated `cicd-key.json`

## 📊 Monitoring

### GitHub Actions
- Go to repository → Actions
- Monitor workflow execution
- Check logs for errors

### Google Cloud Console
- Cloud Build → History
- Cloud Run → Services
- Verify service status

### Logs
```bash
# Production logs
gcloud run services logs read streamlit-app-prod-[hash] --region=southamerica-east1

# Real-time logs
gcloud run services logs tail streamlit-app-prod-[hash] --region=southamerica-east1
```

## 🔄 Rollback Guide

### Quick Rollback
```bash
# Rollback to previous commit
git checkout [branch]
git reset --hard HEAD~1
git push --force origin [branch]
```

### Emergency Rollback
```bash
# For critical issues in PROD
git checkout master
git reset --hard HEAD~1
git push --force origin master
```

## 🚨 Troubleshooting

### Common Issues

**Build Failed:**
```bash
gcloud builds log [BUILD_ID]
```

**Deploy Failed:**
```bash
gcloud run services logs read [SERVICE_NAME] --region=southamerica-east1
```

**Permission Denied:**
- Verify GitHub Secrets configuration
- Check Service Account permissions

### Health Check Issues
- The app includes a health check endpoint at `/healthz`
- Health check logs are silenced to prevent spam
- Check `health_check.py` for configuration

## 📁 Project Structure

```
API_Gcloud_Streamlit/
├── app.py                 # Main Streamlit application
├── health_check.py        # Health check endpoint
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── models/
│   └── pickle_model.pkl  # Trained SVM model
├── .github/workflows/
│   └── ci-cd.yml         # GitHub Actions workflow
├── cloudbuild-dev.yaml   # DEV environment config
├── cloudbuild-qa.yaml    # QA environment config
├── cloudbuild-prod.yaml  # PROD environment config
└── CropPrediction.ipynb  # Model training notebook
```

## 🔧 Configuration Files

- `cloudbuild-dev.yaml` - Development environment
- `cloudbuild-qa.yaml` - QA environment  
- `cloudbuild-prod.yaml` - Production environment
- `.github/workflows/ci-cd.yml` - GitHub Actions workflow
- `Dockerfile` - Container configuration
- `nginx.conf` - Web server configuration

## ✅ Production Checklist

- [ ] Changes tested in DEV
- [ ] Changes tested in QA  
- [ ] CI/CD pipeline executed without errors
- [ ] Production service active
- [ ] Health check responding correctly
- [ ] Application working as expected

## 📞 Support

If you encounter issues:
1. Check GitHub Actions logs
2. Verify Cloud Run logs
3. Confirm GitHub Secrets configuration
4. Ensure PROJECT_ID is correct

## 🙏 Acknowledgments

- [Praneeth Kandula](https://medium.com/analytics-vidhya/deploying-streamlit-apps-to-google-app-engine-in-5-simple-steps-5e2e2bd5b172) - Original deployment guide
- Crop Recommendation Dataset from Kaggle
