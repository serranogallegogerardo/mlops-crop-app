# 🔄 Guía de Rollback para Cloud Run

## 📋 Resumen

Esta guía te permite hacer rollback de tu aplicación en cualquiera de los tres ambientes: **DEV**, **QA** y **PROD** en caso de problemas después de un despliegue.

## 🚨 Cuándo hacer Rollback

- ❌ La aplicación no inicia correctamente
- ❌ Errores críticos en producción
- ❌ Problemas de rendimiento severos
- ❌ Bugs que afectan funcionalidad core
- ❌ Problemas de seguridad

## 🔄 Métodos de Rollback

### **Método 1: Rollback por Git (Recomendado)**

#### **Rollback a un commit anterior específico:**

```bash
# 1. Ver el historial de commits
git log --oneline -10

# 2. Identificar el commit al que quieres hacer rollback
# Ejemplo: a1b2c3d (commit anterior estable)

# 3. Para DEV
git checkout develop
git reset --hard a1b2c3d
git push --force origin develop

# 4. Para QA
git checkout qa
git reset --hard a1b2c3d
git push --force origin qa

# 5. Para PROD
git checkout master
git reset --hard a1b2c3d
git push --force origin master
```

#### **Rollback al commit anterior:**

```bash
# Rollback al commit anterior (HEAD~1)
git checkout [rama]
git reset --hard HEAD~1
git push --force origin [rama]
```

### **Método 2: Rollback por Cloud Run (Directo)**

#### **Ver revisiones disponibles:**
```bash
# Listar revisiones de un servicio
gcloud run revisions list --service=streamlit-app-dev-[hash] --region=southamerica-east1
gcloud run revisions list --service=streamlit-app-qa-[hash] --region=southamerica-east1
gcloud run revisions list --service=streamlit-app-prod-[hash] --region=southamerica-east1
```

#### **Hacer rollback a una revisión específica:**
```bash
# Rollback a revisión anterior
gcloud run services update-traffic streamlit-app-dev-[hash] \
  --to-revisions=REVISION_NAME=100 \
  --region=southamerica-east1
```

### **Método 3: Rollback por Cloud Build (Reconstruir versión anterior)**

```bash
# Reconstruir y desplegar versión anterior
gcloud builds submit \
  --config cloudbuild-dev.yaml \
  --substitutions=_ENV=dev \
  --source=git://github.com/USER/REPO.git#COMMIT_HASH \
  .
```

## 🎯 Rollback por Ambiente

### **DEV (Desarrollo)**
```bash
# Rollback rápido para DEV
git checkout develop
git reset --hard HEAD~1
git push --force origin develop
```

### **QA (Testing)**
```bash
# Rollback para QA
git checkout qa
git reset --hard HEAD~1
git push --force origin qa
```

### **PROD (Producción)**
```bash
# Rollback crítico para PROD
git checkout master
git reset --hard HEAD~1
git push --force origin master
```

## 🔍 Verificación del Rollback

### **1. Verificar el despliegue:**
```bash
# Ver estado de los servicios
gcloud run services list --region=southamerica-east1

# Ver logs del servicio
gcloud run services logs read streamlit-app-[env]-[hash] --region=southamerica-east1 --limit=50
```

### **2. Verificar la aplicación:**
- Acceder a la URL del ambiente
- Probar funcionalidad crítica
- Verificar que no hay errores en consola

### **3. Verificar en GitHub Actions:**
- Ir a Actions en tu repositorio
- Verificar que el rollback se desplegó correctamente
- Revisar logs si hay errores

## 🚨 Rollback de Emergencia

### **Para problemas críticos en PROD:**

```bash
# 1. Rollback inmediato
git checkout master
git reset --hard HEAD~1
git push --force origin master

# 2. Verificar despliegue
gcloud run services list --region=southamerica-east1

# 3. Notificar al equipo
# Enviar mensaje al equipo sobre el rollback
```

### **Para problemas en todos los ambientes:**

```bash
# Rollback masivo a un commit estable
STABLE_COMMIT="a1b2c3d"

git checkout develop
git reset --hard $STABLE_COMMIT
git push --force origin develop

git checkout qa
git reset --hard $STABLE_COMMIT
git push --force origin qa

git checkout master
git reset --hard $STABLE_COMMIT
git push --force origin master
```

## 📊 Monitoreo Post-Rollback

### **1. Logs de aplicación:**
```bash
# Monitorear logs en tiempo real
gcloud run services logs tail streamlit-app-[env]-[hash] --region=southamerica-east1
```

### **2. Métricas de Cloud Run:**
- Ve a Cloud Run → Services → [Tu servicio]
- Revisa métricas de requests, errores, latencia
- Verifica que no hay picos de errores

### **3. Health checks:**
- Verificar que la aplicación responde correctamente
- Confirmar que no hay errores 500
- Validar funcionalidad core

## 🔧 Comandos Útiles

### **Ver historial de commits:**
```bash
git log --oneline -10
git log --graph --oneline --all
```

### **Ver diferencias entre commits:**
```bash
git diff HEAD~1 HEAD
git diff a1b2c3d HEAD
```

### **Ver estado de ramas:**
```bash
git branch -v
git status
```

### **Ver servicios de Cloud Run:**
```bash
gcloud run services list --region=southamerica-east1
gcloud run services describe streamlit-app-[env]-[hash] --region=southamerica-east1
```

## ✅ Checklist de Rollback

- [ ] Identificar el problema
- [ ] Decidir si hacer rollback
- [ ] Elegir el método de rollback
- [ ] Ejecutar el rollback
- [ ] Verificar el despliegue
- [ ] Probar la aplicación
- [ ] Notificar al equipo
- [ ] Documentar el incidente
- [ ] Planificar la corrección

## 📝 Documentación del Incidente

Después de un rollback, documenta:

1. **Fecha y hora del incidente**
2. **Problema identificado**
3. **Método de rollback usado**
4. **Tiempo de resolución**
5. **Impacto en usuarios**
6. **Acciones correctivas futuras**

## 🆘 Contactos de Emergencia

- **DevOps Team**: [Contacto]
- **On-Call Engineer**: [Contacto]
- **Product Owner**: [Contacto]

## 📞 Soporte

Si tienes problemas con el rollback:
1. Revisa los logs de Cloud Build
2. Verifica los logs de Cloud Run
3. Confirma que los permisos están correctos
4. Contacta al equipo de DevOps 