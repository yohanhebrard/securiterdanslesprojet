# 🚀 Manuel de Déploiement - SecureShare

**Document**: Guide d'installation et déploiement
**Version**: 1.0
**Date**: 2025-12-05
**Statut**: ✅ Opérationnel

---

## 1. Prérequis

### 1.1 Environnement de Développement

```bash
# Versions minimales requises
- Docker: 24.0+
- Docker Compose: 2.20+
- Node.js: 18 LTS
- Python: 3.11+
- Git: 2.40+
```

### 1.2 Environnement de Production

```bash
# Infrastructure
- Kubernetes: 1.27+
- Helm: 3.12+
- Cert-Manager: 1.12+
- Ingress Nginx: 1.8+

# Cloud Provider (optionnel)
- AWS / Azure / GCP
- Managed PostgreSQL (RDS / Azure DB / Cloud SQL)
- Managed Redis (ElastiCache / Azure Cache)
```

---

## 2. Installation Locale (Développement)

### 2.1 Clonage du Repository

```bash
git clone https://github.com/votre-org/secureshare.git
cd secureshare
```

### 2.2 Configuration des Variables d'Environnement

```bash
# Copier le template
cp .env.example .env

# Éditer avec vos valeurs
nano .env
```

**Contenu `.env` minimal** :

```bash
# Backend
DATABASE_URL=postgresql://secureshare:dev_password@postgres:5432/secureshare
REDIS_URL=redis://:dev_redis_password@redis:6379/0
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123

# Vault
VAULT_ADDR=http://vault:8200
VAULT_TOKEN=dev-root-token

# Security
SECRET_KEY=your-secret-key-here-min-32-chars
RATE_LIMIT_ENABLED=true
ANTIVIRUS_ENABLED=true

# Frontend
VITE_API_URL=http://localhost:8000
```

### 2.3 Démarrage avec Docker Compose

```bash
# Construction et démarrage de tous les services
docker-compose up --build -d

# Vérification des logs
docker-compose logs -f backend

# Services disponibles:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - MinIO Console: http://localhost:9001
# - Grafana: http://localhost:3001
```

### 2.4 Initialisation de la Base de Données

```bash
# Migrations Alembic
docker-compose exec backend alembic upgrade head

# Vérification
docker-compose exec backend alembic current
```

### 2.5 Initialisation de Vault

```bash
# Initialiser Vault (première fois uniquement)
docker-compose exec vault vault operator init

# Sauvegarder les unseal keys et root token (IMPORTANT!)
# Puis unseal (3 clés sur 5)
docker-compose exec vault vault operator unseal <key1>
docker-compose exec vault vault operator unseal <key2>
docker-compose exec vault vault operator unseal <key3>

# Activer secrets engine
docker-compose exec vault vault secrets enable -path=secret kv-v2
docker-compose exec vault vault secrets enable transit
docker-compose exec vault vault write -f transit/keys/file-encryption
```

### 2.6 Tests de Santé

```bash
# Health check API
curl http://localhost:8000/health

# Upload test
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@test.txt" \
  -F "ttl=3600"

# Vérifier logs
docker-compose logs backend | grep "Upload successful"
```

---

## 3. Configuration Avancée

### 3.1 Activation Scan Antivirus (ClamAV)

```bash
# Vérifier que ClamAV est démarré
docker-compose ps clamav

# Mise à jour des signatures (peut prendre 5-10 min)
docker-compose exec clamav freshclam

# Test de scan
docker-compose exec clamav clamdscan /tmp/eicar.txt
```

### 3.2 Configuration TLS/HTTPS (Développement)

```bash
# Générer certificat auto-signé
mkdir -p infrastructure/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout infrastructure/certs/key.pem \
  -out infrastructure/certs/cert.pem \
  -subj "/CN=localhost"

# Redémarrer nginx
docker-compose restart nginx
```

### 3.3 Configuration Monitoring

```bash
# Importer dashboards Grafana prédéfinis
docker-compose cp infrastructure/grafana/dashboards/ grafana:/etc/grafana/provisioning/dashboards/

# Redémarrer Grafana
docker-compose restart grafana

# Accéder : http://localhost:3001 (admin / admin)
```

---

## 4. Déploiement Production (Kubernetes)

### 4.1 Prérequis Production

```bash
# Créer namespace
kubectl create namespace secureshare-prod

# Créer secrets
kubectl create secret generic secureshare-secrets \
  --from-literal=database-password=<strong-password> \
  --from-literal=redis-password=<strong-password> \
  --from-literal=minio-access-key=<access-key> \
  --from-literal=minio-secret-key=<secret-key> \
  --from-literal=vault-token=<vault-token> \
  -n secureshare-prod
```

### 4.2 Installation avec Helm

```bash
# Ajouter le repository Helm
helm repo add secureshare ./infrastructure/helm

# Installer la release
helm install secureshare secureshare/secureshare \
  --namespace secureshare-prod \
  --values infrastructure/helm/values-production.yaml \
  --set image.tag=v1.0.0 \
  --set ingress.hostname=secureshare.example.com
```

### 4.3 Configuration Ingress avec Cert-Manager

```yaml
# infrastructure/kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secureshare-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/hsts: "true"
    nginx.ingress.kubernetes.io/hsts-max-age: "31536000"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - secureshare.example.com
    secretName: secureshare-tls
  rules:
  - host: secureshare.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

```bash
kubectl apply -f infrastructure/kubernetes/ingress.yaml -n secureshare-prod
```

### 4.4 Vérification du Déploiement

```bash
# Status des pods
kubectl get pods -n secureshare-prod

# Logs backend
kubectl logs -f deployment/backend -n secureshare-prod

# Test health check
curl https://secureshare.example.com/health
```

---

## 5. Pipeline CI/CD

### 5.1 GitHub Actions (Exemple)

```yaml
# .github/workflows/deploy-prod.yml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: SAST - Bandit
        run: |
          pip install bandit
          bandit -r backend/ -f json -o bandit-report.json

      - name: SCA - Safety
        run: |
          pip install safety
          safety check --json > safety-report.json

      - name: Secret Scan - TruffleHog
        run: |
          docker run trufflesecurity/trufflehog:latest github --repo https://github.com/${{ github.repository }}

      - name: Container Scan - Trivy
        run: |
          docker build -t secureshare:${{ github.sha }} .
          trivy image --severity CRITICAL,HIGH --exit-code 1 secureshare:${{ github.sha }}

  build-and-push:
    needs: security-scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Backend
        run: docker build -t ghcr.io/${{ github.repository }}/backend:${{ github.ref_name }} backend/

      - name: Build Frontend
        run: docker build -t ghcr.io/${{ github.repository }}/frontend:${{ github.ref_name }} frontend/

      - name: Push to GHCR
        run: |
          echo ${{ secrets.GITHUB_TOKEN }} | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker push ghcr.io/${{ github.repository }}/backend:${{ github.ref_name }}
          docker push ghcr.io/${{ github.repository }}/frontend:${{ github.ref_name }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: |
          helm upgrade secureshare ./infrastructure/helm/secureshare \
            --namespace secureshare-prod \
            --set image.tag=${{ github.ref_name }} \
            --reuse-values
```

### 5.2 Stratégie de Déploiement

**Blue/Green Deployment** :

```bash
# Déployer nouvelle version (green)
helm install secureshare-green secureshare/secureshare \
  --namespace secureshare-prod \
  --set version=green \
  --set image.tag=v2.0.0

# Vérifications
kubectl run -it --rm test-pod --image=curlimages/curl -- curl http://backend-green:8000/health

# Switch du trafic (modifier Ingress)
kubectl patch ingress secureshare-ingress -p '{"spec":{"rules":[{"http":{"paths":[{"backend":{"serviceName":"backend-green"}}]}}]}}'

# Supprimer ancienne version après validation
helm uninstall secureshare-blue -n secureshare-prod
```

---

## 6. Maintenance

### 6.1 Backups

#### Base de Données

```bash
# Backup manuel
kubectl exec -it postgres-0 -n secureshare-prod -- \
  pg_dump -U secureshare -F c -b -v -f /backup/secureshare_$(date +%Y%m%d).dump secureshare

# Copier localement
kubectl cp secureshare-prod/postgres-0:/backup/secureshare_20250105.dump ./backup/

# Automatique avec CronJob Kubernetes
kubectl apply -f infrastructure/kubernetes/cronjob-backup.yaml
```

#### Vault

```bash
# Snapshot Vault
kubectl exec -it vault-0 -n secureshare-prod -- \
  vault operator raft snapshot save /vault/data/snapshot_$(date +%Y%m%d).snap

# Backup des unseal keys (OFFLINE, sécurisé)
# Stocker dans coffre-fort physique ou HSM
```

### 6.2 Restauration

#### Base de Données

```bash
# Arrêter backend
kubectl scale deployment backend --replicas=0 -n secureshare-prod

# Restaurer dump
kubectl exec -it postgres-0 -n secureshare-prod -- \
  pg_restore -U secureshare -d secureshare -v /backup/secureshare_20250105.dump

# Redémarrer backend
kubectl scale deployment backend --replicas=3 -n secureshare-prod
```

### 6.3 Mise à Jour des Dépendances

```bash
# Backend
cd backend
pip list --outdated
pip install -U <package>
pip freeze > requirements.txt

# Frontend
cd frontend
npm outdated
npm update
npm audit fix

# Tester
docker-compose up --build
pytest
npm test
```

### 6.4 Rotation des Secrets

```bash
# Rotation clé PostgreSQL
kubectl create secret generic secureshare-secrets-new \
  --from-literal=database-password=<new-strong-password> \
  -n secureshare-prod

# Mise à jour déploiement
helm upgrade secureshare secureshare/secureshare \
  --set secrets.name=secureshare-secrets-new \
  --reuse-values

# Supprimer ancien secret après validation
kubectl delete secret secureshare-secrets -n secureshare-prod
```

---

## 7. Troubleshooting

### 7.1 Problèmes Courants

#### Backend ne démarre pas

```bash
# Vérifier logs
docker-compose logs backend

# Erreurs courantes:
# - Database connection: vérifier DATABASE_URL
# - Vault unreachable: vérifier VAULT_ADDR et token
# - Migrations: alembic upgrade head
```

#### Scan antivirus échoue

```bash
# Vérifier ClamAV
docker-compose logs clamav

# Mettre à jour signatures
docker-compose exec clamav freshclam

# Redémarrer
docker-compose restart clamav
```

#### Rate limiting trop agressif

```bash
# Ajuster limites dans .env
RATE_LIMIT_UPLOAD_PER_HOUR=20  # Au lieu de 10
RATE_LIMIT_DOWNLOAD_PER_HOUR=100  # Au lieu de 50

# Redémarrer backend
docker-compose restart backend
```

#### Fichiers non supprimés

```bash
# Vérifier logs de suppression
docker-compose logs backend | grep "deletion"

# Reconciliation manuelle S3 ↔ DB
docker-compose exec backend python scripts/reconcile_storage.py

# Cleanup forcé
docker-compose exec backend python scripts/cleanup_expired.py --force
```

### 7.2 Debugging Avancé

```bash
# Shell interactif dans container backend
docker-compose exec backend /bin/bash

# Tester connexion DB
docker-compose exec backend python -c "from app.core.database import engine; print(engine.execute('SELECT 1').scalar())"

# Tester connexion Redis
docker-compose exec redis redis-cli -a dev_redis_password PING

# Tester connexion Vault
docker-compose exec backend python -c "import hvac; client = hvac.Client(url='http://vault:8200', token='dev-root-token'); print(client.is_authenticated())"
```

---

## 8. Sécurité Post-Déploiement

### 8.1 Hardening Checklist

- [ ] TLS 1.3 activé, TLS < 1.2 désactivé
- [ ] HSTS configuré avec preload
- [ ] CSP headers actifs
- [ ] Rate limiting fonctionnel
- [ ] Scan antivirus testé
- [ ] Backups automatiques configurés
- [ ] Monitoring et alertes actifs
- [ ] Firewall configuré (ports minimum)
- [ ] Secrets rotation planifiée (90 jours)
- [ ] Logs centralisés et sécurisés
- [ ] Audit RGPD complété
- [ ] Pentest interne réalisé

### 8.2 Tests de Sécurité Post-Déploiement

```bash
# SSL Labs test
curl https://www.ssllabs.com/ssltest/analyze.html?d=secureshare.example.com

# Security Headers test
curl https://securityheaders.com/?q=secureshare.example.com

# OWASP ZAP baseline scan
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://secureshare.example.com

# Nmap scan (ports ouverts)
nmap -sV -p- secureshare.example.com
```

---

## 9. Métriques de Production

### 9.1 Dashboards Grafana

Importer les dashboards prédéfinis :
- **Overview** : `infrastructure/grafana/dashboards/overview.json`
- **Security** : `infrastructure/grafana/dashboards/security.json`
- **Performance** : `infrastructure/grafana/dashboards/performance.json`

### 9.2 Alertes Critiques

```yaml
# Alertmanager config
groups:
  - name: secureshare-critical
    interval: 1m
    rules:
      - alert: HighErrorRate
        expr: rate(secureshare_errors_total[5m]) > 10
        annotations:
          summary: "High error rate detected"

      - alert: MalwareDetected
        expr: increase(secureshare_malware_detected_total[1h]) > 0
        annotations:
          summary: "Malware detected on platform"

      - alert: FilesNotDeleted
        expr: secureshare_deletion_failed_total > 0
        annotations:
          summary: "CRITICAL: Files not deleted after download"
```

---

## 10. Rollback Procédure

### 10.1 Rollback Application

```bash
# Via Helm
helm rollback secureshare -n secureshare-prod

# Via kubectl (si déploiement direct)
kubectl rollout undo deployment/backend -n secureshare-prod
kubectl rollout undo deployment/frontend -n secureshare-prod
```

### 10.2 Rollback Base de Données

```bash
# Restaurer backup précédent (voir section 6.2)
# ATTENTION: Perte de données entre backup et rollback

# Alternative: migration Alembic downgrade
kubectl exec -it backend-pod -n secureshare-prod -- \
  alembic downgrade -1
```

---

## 11. Documentation Complémentaire

- [README.md](../README.md) - Vue d'ensemble
- [01-EXIGENCES-SECURITE.md](01-EXIGENCES-SECURITE.md) - Exigences
- [02-ANALYSE-RISQUES.md](02-ANALYSE-RISQUES.md) - Risques
- [03-BACKLOG-SECURITE.md](03-BACKLOG-SECURITE.md) - User stories
- [04-KPIS-KRIS.md](04-KPIS-KRIS.md) - Indicateurs
- [05-ARCHITECTURE.md](05-ARCHITECTURE.md) - Architecture technique

---

## 12. Support

**En cas de problème critique** :
1. Consulter les logs : `kubectl logs -f deployment/backend -n secureshare-prod`
2. Vérifier le dashboard Grafana : https://grafana.example.com
3. Contacter l'équipe : security@example.com
4. Incident majeur : Activer procédure d'incident (PagerDuty)

---

**🚀 Bon déploiement !**
