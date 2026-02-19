# 🔐 SecureShare - Plateforme de Partage de Fichiers Éphémères Sécurisée

## 📋 Description du Projet

**SecureShare** est un micro-projet SaaS développé dans le cadre d'un projet fil rouge axé sur la sécurité.

L'objectif est de créer une plateforme simple mais robuste permettant le partage de fichiers sensibles avec :
- ✅ Chiffrement de bout en bout
- ✅ Liens à usage unique et expiration automatique
- ✅ Suppression sécurisée après téléchargement
- ✅ Protection contre les abus (rate limiting, antivirus, CAPTCHA)
- ✅ Journalisation et audit complets
- ✅ Pipeline DevSecOps intégré

## 🎯 Objectifs Pédagogiques

Ce projet démontre l'intégration de la sécurité à chaque étape du cycle de développement :
1. **Analyse de risques** - Identification et mitigation des menaces
2. **Secure by Design** - Architecture sécurisée dès la conception
3. **DevSecOps** - Pipeline CI/CD avec tests de sécurité automatisés
4. **Conformité** - RGPD, OWASP Top 10, bonnes pratiques cryptographiques

## 🏗️ Architecture

### Stack Technique

**Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- TailwindCSS
- WebCrypto API (chiffrement client)

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL (métadonnées)
- Redis (cache, tokens éphémères)
- MinIO (stockage S3-compatible)
- HashiCorp Vault (gestion des secrets)

**DevSecOps:**
- GitHub Actions / GitLab CI
- SAST: Bandit, Semgrep, ESLint Security
- DAST: OWASP ZAP
- SCA: Safety, Snyk, Trivy
- Container scanning: Trivy

### Diagramme d'Architecture

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │ HTTPS/TLS
       │
┌──────▼──────────────────────────────────────┐
│         Load Balancer / WAF                  │
└──────┬──────────────────────────────────────┘
       │
┌──────▼──────────┐
│  React Frontend │
│   (Static SPA)  │
└──────┬──────────┘
       │ API Calls
┌──────▼──────────┐
│  FastAPI Backend│◄─────┐
│   + Rate Limit  │      │
└──┬───┬───┬───┬──┘      │
   │   │   │   │         │
   │   │   │   │    ┌────▼────┐
   │   │   │   │    │  Redis  │
   │   │   │   │    │ (Cache) │
   │   │   │   │    └─────────┘
   │   │   │   │
   │   │   │   │    ┌──────────┐
   │   │   │   └────►PostgreSQL│
   │   │   │        │   (DB)   │
   │   │   │        └──────────┘
   │   │   │
   │   │   │        ┌──────────┐
   │   │   └────────►  MinIO   │
   │   │            │ (Storage)│
   │   │            └──────────┘
   │   │
   │   │            ┌──────────┐
   │   └────────────►  Vault   │
   │                │ (Secrets)│
   │                └──────────┘
   │
   │                ┌──────────┐
   └────────────────► ClamAV   │
                    │(Antivirus)│
                    └──────────┘
```

## 📁 Structure du Projet

```
secureshare/
├── docs/                           # Documentation professionnelle
│   ├── 01-EXIGENCES-SECURITE.md   # Exigences de sécurité
│   ├── 02-ANALYSE-RISQUES.md      # Analyse de risques EBIOS
│   ├── 03-BACKLOG-SECURITE.md     # Backlog sécurité priorisé
│   ├── 04-KPIS-KRIS.md            # Indicateurs de sécurité
│   ├── 05-ARCHITECTURE.md         # Architecture détaillée
│   └── 06-MANUEL-DEPLOIEMENT.md   # Guide de déploiement
│
├── backend/                        # API FastAPI
│   ├── app/
│   │   ├── api/                   # Endpoints API
│   │   ├── core/                  # Configuration, sécurité
│   │   ├── models/                # Modèles SQLAlchemy
│   │   ├── schemas/               # Schémas Pydantic
│   │   ├── services/              # Logique métier
│   │   └── utils/                 # Utilitaires
│   ├── tests/                     # Tests unitaires et intégration
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/                       # Application React
│   ├── src/
│   │   ├── components/            # Composants React
│   │   ├── services/              # API client, crypto
│   │   ├── hooks/                 # Custom hooks
│   │   ├── pages/                 # Pages/routes
│   │   └── utils/                 # Utilitaires
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
│
├── infrastructure/                 # Infrastructure as Code
│   ├── docker/                    # Docker configs
│   │   ├── docker-compose.yml
│   │   └── docker-compose.prod.yml
│   ├── kubernetes/                # K8s manifests
│   └── terraform/                 # Terraform configs
│
├── .github/                       # CI/CD Pipeline
│   └── workflows/
│       ├── ci.yml                 # Tests + SAST
│       ├── security-scan.yml      # Scans de sécurité
│       └── deploy.yml             # Déploiement
│
└── scripts/                       # Scripts utilitaires
    ├── setup-dev.sh
    └── run-security-tests.sh
```

## 🚀 Démarrage Rapide

### Prérequis

- Docker & Docker Compose
- Node.js 18+ (pour développement frontend local)
- Python 3.11+ (pour développement backend local)

### Installation

```bash
# Cloner le repository
git clone <repo-url>
cd secureshare

# Copier les variables d'environnement
cp .env.example .env

# Démarrer tous les services
docker-compose up -d

# Initialiser la base de données
docker-compose exec backend alembic upgrade head

# Accéder à l'application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🔒 Fonctionnalités de Sécurité

### ✅ Chiffrement
- **En transit**: TLS 1.3, HSTS, certificate pinning
- **Au repos**: AES-256-GCM via HashiCorp Vault KMS
- **Option E2EE**: Chiffrement client avec WebCrypto API

### ✅ Protection contre les abus
- Rate limiting (Redis)
- CAPTCHA (hCaptcha/reCAPTCHA)
- Scan antivirus (ClamAV)
- Validation MIME type stricte
- Limite de taille fichiers

### ✅ Confidentialité & Conformité
- Suppression sécurisée après téléchargement
- Expiration automatique (TTL configurable)
- Tokens à usage unique (hachés en base)
- Journalisation RGPD-compliant
- Pas de tracking utilisateur

### ✅ Audit & Monitoring
- Logs structurés (JSON)
- Événements tracés (upload, download, delete)
- Alertes sur comportements anormaux
- Dashboard de métriques de sécurité

## 📊 KPIs / KRIs

| Indicateur | Type | Seuil | Fréquence |
|------------|------|-------|-----------|
| Taux de suppression après ouverture | KPI | > 99% | Quotidien |
| Tentatives de téléchargement invalides | KRI | < 5% | Temps réel |
| Détections antivirus | KRI | 0 fichiers malveillants distribués | Temps réel |
| Temps de réponse API | KPI | < 200ms (p95) | Continu |
| Certificats SSL expirés | KRI | 0 | Hebdomadaire |

## 🧪 Tests de Sécurité

```bash
# SAST (Static Application Security Testing)
./scripts/run-sast.sh

# DAST (Dynamic Application Security Testing)
./scripts/run-dast.sh

# Dependency scanning
./scripts/run-dependency-scan.sh

# Tests unitaires avec coverage
docker-compose exec backend pytest --cov

# Tests d'intégration
docker-compose exec backend pytest tests/integration/
```

## 📚 Documentation

Consultez le dossier [`docs/`](docs/) pour :
- [Exigences de sécurité](docs/01-EXIGENCES-SECURITE.md)
- [Analyse de risques](docs/02-ANALYSE-RISQUES.md)
- [Backlog sécurité](docs/03-BACKLOG-SECURITE.md)
- [KPIs/KRIs détaillés](docs/04-KPIS-KRIS.md)
- [Architecture technique](docs/05-ARCHITECTURE.md)
- [Manuel de déploiement](docs/06-MANUEL-DEPLOIEMENT.md)
- [**Dossier final**](docs/07-DOSSIER-FINAL.md)

## 👥 Équipe

- **Chef de projet**: [Nom]
- **Développeurs**: [Noms]
- **Responsable sécurité**: [Nom]

## 📝 Licence

Projet éducatif - Tous droits réservés

## 🙏 Remerciements

Projet réalisé dans le cadre du fil rouge "Sécurité intégrée dans les projets".
