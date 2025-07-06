# 🚀 Guía de Despliegue a Producción

## 📋 Resumen del Pipeline CI/CD

Tu proyecto tiene configurado un pipeline automático con **3 ambientes**:
- **DEV** (rama `develop`) → Desarrollo
- **QA** (rama `qa`) → Testing  
- **PROD** (rama `master`) → Producción

## 🔄 Flujo de Despliegue

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   develop   │───▶│     qa      │───▶│    master   │
│   (DEV)     │    │    (QA)     │    │   (PROD)    │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🚀 Pasos para Subir a Producción

### 1. **Verificar cambios locales**
```bash
# Ver el estado actual
git status

# Ver los cambios realizados
git diff
```

### 2. **Hacer commit de los cambios**
```bash
# Agregar todos los cambios
git add .

# Hacer commit con mensaje descriptivo
git commit -m "fix: deshabilitar health check spam en Cloud Run"
```

### 3. **Subir a la rama develop (DEV)**
```bash
# Cambiar a rama develop
git checkout develop

# Subir cambios
git push origin develop
```

**✅ Automáticamente se desplegará a DEV**

### 4. **Probar en DEV**
- Ve a la URL de DEV en Cloud Run
- Verifica que la aplicación funcione correctamente
- Confirma que el spam al health check se haya reducido

### 5. **Subir a la rama qa (QA)**
```bash
# Cambiar a rama qa
git checkout qa

# Merge de develop a qa
git merge develop

# Subir cambios
git push origin qa
```

**✅ Automáticamente se desplegará a QA**

### 6. **Probar en QA**
- Ve a la URL de QA en Cloud Run
- Realiza pruebas de integración
- Verifica que todo funcione como esperado

### 7. **Subir a la rama master (PRODUCCIÓN)**
```bash
# Cambiar a rama master
git checkout master

# Merge de qa a master
git merge qa

# Subir a producción
git push origin master
```

**✅ Automáticamente se desplegará a PRODUCCIÓN**

## 📊 URLs de los Ambientes

| Ambiente | URL |
|----------|-----|
| **DEV** | `https://streamlit-app-dev-[hash]-southamerica-east1.a.run.app` |
| **QA** | `https://streamlit-app-qa-[hash]-southamerica-east1.a.run.app` |
| **PROD** | `https://streamlit-app-prod-[hash]-southamerica-east1.a.run.app` |

## 🔍 Monitoreo del Despliegue

### 1. **GitHub Actions**
- Ve a tu repositorio → Actions
- Verifica que los workflows se ejecuten correctamente
- Revisa los logs si hay errores

### 2. **Google Cloud Console**
- Ve a Cloud Build → History
- Ve a Cloud Run → Services
- Verifica que los servicios estén activos

### 3. **Logs de Cloud Run**
```bash
# Ver logs de producción
gcloud run services logs read streamlit-app-prod-[hash] --region=southamerica-east1

# Ver logs en tiempo real
gcloud run services logs tail streamlit-app-prod-[hash] --region=southamerica-east1
```

## 🚨 Troubleshooting

### Error: "Build failed"
```bash
# Ver logs del build
gcloud builds log [BUILD_ID]
```

### Error: "Deploy failed"
```bash
# Ver logs del servicio
gcloud run services logs read [SERVICE_NAME] --region=southamerica-east1
```

### Error: "Permission denied"
- Verifica que los GitHub Secrets estén configurados correctamente
- Confirma que el Service Account tenga los permisos necesarios

## ⚡ Comandos Rápidos

### Despliegue completo (desde develop)
```bash
git checkout develop
git add . && git commit -m "fix: health check spam"
git push origin develop

git checkout qa
git merge develop
git push origin qa

git checkout master
git merge qa
git push origin master
```

### Verificar estado de servicios
```bash
gcloud run services list --region=southamerica-east1
```

### Ver logs de producción
```bash
gcloud run services logs read streamlit-app-prod-[hash] --region=southamerica-east1 --limit=50
```

## ✅ Checklist de Producción

- [ ] Cambios probados en DEV
- [ ] Cambios probados en QA  
- [ ] Pipeline de CI/CD ejecutado sin errores
- [ ] Servicio de producción activo
- [ ] Health check spam reducido
- [ ] Aplicación funcionando correctamente

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en GitHub Actions
2. Verifica los logs en Cloud Run
3. Confirma que los GitHub Secrets estén configurados
4. Asegúrate de que el PROJECT_ID sea correcto 