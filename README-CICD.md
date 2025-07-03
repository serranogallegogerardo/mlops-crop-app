# 🚀 CI/CD Pipeline with Google Cloud Build (English Quick Start)

This project includes a complete CI/CD pipeline with three environments: **DEV**, **QA**, and **PROD**.

## ⚡ How to Run the App Locally

### 1. Run with Docker (Production-like)

Build the Docker image locally:
```bash
sudo docker build -t crop-streamlit-app .
```

Run the app in a Docker container:
```bash
sudo docker run -p 8080:8080 -e PORT=8080 crop-streamlit-app
```
- Access your app at: [http://localhost:8080](http://localhost:8080)
- This method replicates the production environment and is ideal for testing how your app will behave in Google Cloud Run.

### 2. Run Natively (Local Development)

You can also run the app directly on your machine, without Docker.

For example, to run both Jupyter Notebook and Streamlit locally:
```bash
# Activate your Python environment first, if needed
source crop-env/bin/activate

# Start Jupyter Notebook
jupyter notebook

# In another terminal, start Streamlit
streamlit run app.py
```
- This method is useful for rapid development and debugging.

---

## 🚦 How to Test the CI/CD Flow

1. **Push to `develop` branch** → Deploys automatically to DEV environment.
2. **Push to `qa` branch** → Deploys automatically to QA environment.
3. **Push to `master` branch** → Deploys automatically to PROD environment.

You can monitor the deployment status in the **Actions** tab of your GitHub repository. Each environment will have its own Google Cloud Run service and URL.

---

# 🚀 CI/CD Pipeline con Google Cloud Build

Este proyecto incluye un pipeline CI/CD completo con tres ambientes: **DEV**, **QA** y **PROD**.

## 📋 Estructura del Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   develop   │───▶│     qa      │───▶│    main     │
│   (DEV)     │    │    (QA)     │    │   (PROD)    │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🛠️ Configuración Automática

### 1. Ejecutar el script de configuración

```bash
./setup-cicd.sh [TU_PROJECT_ID]
```

Ejemplo:
```bash
./setup-cicd.sh mi-proyecto-123
```

### 2. Configurar GitHub

1. **Crear repositorio en GitHub**
2. **Crear las ramas:**
   ```bash
   git checkout -b develop
   git checkout -b qa
   git checkout main
   ```

3. **Configurar Secrets en GitHub:**
   - Ve a tu repositorio → Settings → Secrets and variables → Actions
   - Agrega estos secrets:
     - `GCP_PROJECT_ID`: Tu ID de proyecto de Google Cloud
     - `GCP_SA_KEY`: Contenido del archivo `cicd-key.json` generado

## 🔄 Flujo de Trabajo

### Desarrollo (rama `develop`)
- **Trigger**: Push a `develop`
- **Deploy**: Automático a ambiente DEV
- **URL**: `https://streamlit-app-dev-[hash]-southamerica-east1.a.run.app`

### QA (rama `qa`)
- **Trigger**: Push a `qa`
- **Deploy**: Automático a ambiente QA
- **URL**: `https://streamlit-app-qa-[hash]-southamerica-east1.a.run.app`

### Producción (rama `main`)
- **Trigger**: Push a `main`
- **Deploy**: Automático a ambiente PROD
- **URL**: `https://streamlit-app-prod-[hash]-southamerica-east1.a.run.app`

## 📊 Configuración por Ambiente

| Ambiente | RAM | CPU | Max Instances | Propósito |
|----------|-----|-----|---------------|-----------|
| **DEV**  | 512Mi | 1 | 2 | Desarrollo y testing |
| **QA**   | 1Gi | 1 | 3 | Testing de integración |
| **PROD** | 2Gi | 2 | 10 | Producción |

## 🔧 Archivos de Configuración

- `cloudbuild-dev.yaml` - Configuración para DEV
- `cloudbuild-qa.yaml` - Configuración para QA  
- `cloudbuild-prod.yaml` - Configuración para PROD
- `.github/workflows/ci-cd.yml` - Workflow de GitHub Actions

## 🚨 Seguridad

- ✅ Service Account dedicado para CI/CD
- ✅ Permisos mínimos necesarios
- ✅ Autenticación segura con GitHub
- ✅ Variables de entorno en secrets

## 📝 Comandos Útiles

### Ver logs de Cloud Build
```bash
gcloud builds log [BUILD_ID]
```

### Ver servicios desplegados
```bash
gcloud run services list
```

### Ver logs de un servicio
```bash
gcloud run services logs read [SERVICE_NAME]
```

## 🆘 Troubleshooting

### Error: "Permission denied"
- Verifica que el Service Account tenga los permisos correctos
- Asegúrate de que las APIs estén habilitadas

### Error: "Build failed"
- Revisa los logs de Cloud Build
- Verifica que el Dockerfile sea correcto

### Error: "Deploy failed"
- Verifica que el proyecto tenga cuota disponible
- Revisa los logs de Cloud Run

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Google Cloud Console
2. Verifica la configuración de GitHub Secrets
3. Asegúrate de que el PROJECT_ID sea correcto 