# 🚀 Guide de Démarrage Rapide - SecureShare

Bienvenue dans votre projet fil rouge **SecureShare** !

Ce guide vous permettra de démarrer rapidement avec l'environnement de développement.

---

## ⚡ Démarrage Express (5 minutes)

### Prérequis

```bash
✅ Docker Desktop installé et lancé
✅ Git installé
✅ Un éditeur de code (VS Code recommandé)
```

### Étapes

```bash
# 1. Cloner le projet (si ce n'est pas déjà fait)
git clone <votre-repo>
cd securiterdanslesprojet

# 2. Copier le fichier d'environnement
cp .env.example .env

# 3. Démarrer tous les services
docker-compose up -d

# 4. Attendre que les services démarrent (1-2 minutes)
docker-compose logs -f backend

# 5. Vérifier que tout fonctionne
curl http://localhost:8000/health
# Réponse attendue: {"status":"healthy"}
```

### Accès aux Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | [http://localhost:3000](http://localhost:3000) | - |
| **Backend API** | [http://localhost:8000](http://localhost:8000) | - |
| **API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | - |
| **MinIO Console** | [http://localhost:9001](http://localhost:9001) | minioadmin / minioadmin123 |
| **Grafana** | [http://localhost:3001](http://localhost:3001) | admin / admin |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | - |

---

## 📚 Structure du Projet

```
securiterdanslesprojet/
│
├── 📖 docs/                            # Documentation professionnelle
│   ├── 01-EXIGENCES-SECURITE.md       # ⭐ Exigences sécurité (OWASP, RGPD)
│   ├── 02-ANALYSE-RISQUES.md          # ⭐ Analyse de risques (EBIOS)
│   ├── 03-BACKLOG-SECURITE.md         # ⭐ User stories sécurité
│   ├── 04-KPIS-KRIS.md                # ⭐ Indicateurs de sécurité
│   ├── 05-ARCHITECTURE.md             # Architecture technique
│   └── 06-MANUEL-DEPLOIEMENT.md       # Guide déploiement
│
├── 🔧 backend/                         # API FastAPI
│   ├── app/
│   │   ├── api/                       # Endpoints
│   │   ├── core/                      # Configuration
│   │   ├── models/                    # Modèles DB
│   │   ├── services/                  # Logique métier
│   │   └── middleware/                # Sécurité, logs
│   ├── Dockerfile
│   └── requirements.txt
│
├── 🎨 frontend/                        # Application React
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── pages/
│   ├── Dockerfile
│   └── package.json
│
├── 🏗️ infrastructure/                  # Infrastructure as Code
│   ├── docker/
│   ├── kubernetes/
│   ├── prometheus/
│   └── grafana/
│
├── 🔄 .github/workflows/               # CI/CD Pipeline
│   └── ci.yml                         # Tests sécurité automatisés
│
├── 🐳 docker-compose.yml               # Environnement complet
├── 📄 .env.example                     # Template configuration
└── 📖 README.md                        # Vue d'ensemble
```

---

## 🎯 Checklist du Projet Fil Rouge

### Phase 1 : Fondations (Sprint 1) ✅

- [x] ✅ **Livrables professionnels créés**
  - [x] Exigences de sécurité (52 exigences critiques)
  - [x] Analyse de risques (10 risques analysés)
  - [x] Backlog sécurité (25 user stories)
  - [x] KPIs/KRIs (10 indicateurs)
  - [x] Architecture détaillée
  - [x] Manuel de déploiement

- [x] ✅ **Infrastructure DevSecOps configurée**
  - [x] Docker Compose multi-services
  - [x] Pipeline CI/CD GitHub Actions
  - [x] SAST (Bandit, ESLint)
  - [x] SCA (Safety, npm audit)
  - [x] Secret scanning (TruffleHog)
  - [x] Container scanning (Trivy)

- [x] ✅ **Structure projet créée**
  - [x] Backend (FastAPI)
  - [x] Frontend (React)
  - [x] Base de données (PostgreSQL)
  - [x] Cache (Redis)
  - [x] Stockage (MinIO)
  - [x] Secrets (Vault)
  - [x] Antivirus (ClamAV)

### Phase 2 : Implémentation Backend (Sprint 2) 🔄

- [ ] **Endpoints API**
  - [ ] POST /api/v1/upload
  - [ ] GET /api/v1/download/{token}
  - [ ] GET /api/v1/info/{token}
  - [ ] GET /health

- [ ] **Services sécurité**
  - [ ] Service de chiffrement AES-256-GCM
  - [ ] Génération tokens sécurisés
  - [ ] Intégration ClamAV
  - [ ] Suppression atomique
  - [ ] Rate limiting

- [ ] **Base de données**
  - [ ] Modèles SQLAlchemy
  - [ ] Migrations Alembic
  - [ ] Seed data (tests)

### Phase 3 : Implémentation Frontend (Sprint 3) 🔄

- [ ] **Pages**
  - [ ] Page d'upload
  - [ ] Page de téléchargement
  - [ ] Page RGPD / Confidentialité

- [ ] **Composants**
  - [ ] Formulaire upload (drag & drop)
  - [ ] Barre de progression
  - [ ] Badges sécurité
  - [ ] Timer expiration

- [ ] **Sécurité frontend**
  - [ ] WebCrypto API (E2EE optionnel)
  - [ ] Validation fichiers
  - [ ] CSP headers

### Phase 4 : Tests & Sécurité (Sprint 4) 🔄

- [ ] **Tests unitaires**
  - [ ] Backend (coverage > 80%)
  - [ ] Frontend (coverage > 80%)

- [ ] **Tests de sécurité**
  - [ ] DAST (OWASP ZAP)
  - [ ] Tests de pénétration manuels
  - [ ] Tests de contournement (rate limiting, etc.)

### Phase 5 : Documentation & Présentation (Sprint 5) 🔄

- [ ] **Documentation finale**
  - [ ] README complet
  - [ ] Guide utilisateur
  - [ ] Guide administrateur
  - [ ] Rapport de sécurité

- [ ] **Préparation démo**
  - [ ] Slides de présentation
  - [ ] Scénarios de démonstration
  - [ ] Vidéo de présentation

---

## 💡 Commandes Utiles

### Développement

```bash
# Démarrer les services
docker-compose up -d

# Voir les logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Redémarrer un service
docker-compose restart backend

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes (réinitialisation complète)
docker-compose down -v
```

### Base de Données

```bash
# Créer une migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Appliquer les migrations
docker-compose exec backend alembic upgrade head

# Annuler la dernière migration
docker-compose exec backend alembic downgrade -1

# Shell PostgreSQL
docker-compose exec postgres psql -U secureshare
```

### Tests

```bash
# Tests backend
docker-compose exec backend pytest -v

# Tests avec coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Tests frontend
docker-compose exec frontend npm test
```

### Sécurité

```bash
# Scan SAST (Bandit)
cd backend && bandit -r app/ -ll

# Scan dépendances (Safety)
cd backend && safety check

# Scan containers (Trivy)
trivy image secureshare-backend:latest

# Scan secrets (TruffleHog)
trufflehog filesystem . --json
```

---

## 🔍 Debugging

### Le backend ne démarre pas

```bash
# Vérifier les logs
docker-compose logs backend

# Erreurs fréquentes:
# - Database connection: vérifier DATABASE_URL dans .env
# - Vault unreachable: vérifier que vault est démarré
# - Port déjà utilisé: changer le port dans docker-compose.yml
```

### Les migrations échouent

```bash
# Vérifier l'état
docker-compose exec backend alembic current

# Forcer la version
docker-compose exec backend alembic stamp head

# Réinitialiser la base (⚠️ supprime toutes les données)
docker-compose down -v postgres
docker-compose up -d postgres
docker-compose exec backend alembic upgrade head
```

### ClamAV ne fonctionne pas

```bash
# Vérifier les logs
docker-compose logs clamav

# Mettre à jour les signatures (peut prendre 5-10 min)
docker-compose exec clamav freshclam

# Redémarrer
docker-compose restart clamav
```

---

## 📖 Ressources

### Documentation

- [README.md](README.md) - Vue d'ensemble
- [docs/01-EXIGENCES-SECURITE.md](docs/01-EXIGENCES-SECURITE.md) - Exigences sécurité
- [docs/02-ANALYSE-RISQUES.md](docs/02-ANALYSE-RISQUES.md) - Analyse de risques
- [docs/03-BACKLOG-SECURITE.md](docs/03-BACKLOG-SECURITE.md) - Backlog
- [docs/06-MANUEL-DEPLOIEMENT.md](docs/06-MANUEL-DEPLOIEMENT.md) - Déploiement

### Références Techniques

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [ANSSI - Sécurité TLS](https://www.ssi.gouv.fr/guide/recommandations-de-securite-relatives-a-tls/)

---

## 🎓 Objectifs Pédagogiques

### Compétences Développées

✅ **Sécurité** :
- Analyse de risques méthodique
- Implémentation de contrôles de sécurité
- Tests de sécurité automatisés (SAST, DAST, SCA)
- Conformité RGPD

✅ **DevSecOps** :
- Pipeline CI/CD sécurisé
- Infrastructure as Code
- Containerisation (Docker, Kubernetes)
- Monitoring et alerting

✅ **Architecture** :
- Microservices
- Chiffrement E2E
- Gestion des secrets (Vault)
- Haute disponibilité

✅ **Développement** :
- Backend API (FastAPI, Python)
- Frontend moderne (React, TypeScript)
- Base de données (PostgreSQL)
- Tests automatisés

---

## 🤝 Contribution

Ce projet est un projet fil rouge pédagogique.

Pour toute question ou problème, consultez les **Issues** GitHub ou contactez votre enseignant.

---

## 📝 Licence

Projet éducatif - Tous droits réservés

---

**Bon courage pour votre projet fil rouge ! 🚀**

*Projet généré avec [Claude Code](https://claude.com/claude-code)*
