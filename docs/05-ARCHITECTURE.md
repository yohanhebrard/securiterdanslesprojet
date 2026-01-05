# 🏗️ Architecture Technique Détaillée - SecureShare

**Document**: Spécifications d'architecture système
**Version**: 1.0
**Date**: 2025-12-05
**Statut**: ✅ Approuvé

---

## 1. Vue d'Ensemble

### 1.1 Architecture Globale

```
┌──────────────────────────────────────────────────────────────┐
│                      Internet / Clients                       │
└────────────────────────────┬─────────────────────────────────┘
                             │
                ┌────────────▼────────────┐
                │   CDN / WAF / DDoS      │
                │  (Cloudflare/AWS WAF)   │
                └────────────┬────────────┘
                             │
                ┌────────────▼────────────┐
                │   Load Balancer         │
                │   (Nginx / Traefik)     │
                │   - TLS Termination     │
                │   - Rate Limiting       │
                └────┬─────────────┬──────┘
                     │             │
        ┌────────────▼──┐      ┌──▼────────────┐
        │   Frontend    │      │   Backend API │
        │   (React SPA) │      │   (FastAPI)   │
        │   - Nginx     │      │   - Uvicorn   │
        │   - Static    │      │   - Workers   │
        └───────────────┘      └───┬───────────┘
                                   │
                   ┌───────────────┼───────────────┐
                   │               │               │
            ┌──────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
            │  PostgreSQL │ │   Redis    │ │   MinIO    │
            │  (Metadata) │ │  (Cache)   │ │ (Storage)  │
            └─────────────┘ └────────────┘ └────────────┘
                   │
            ┌──────▼──────┐
            │HashiCorp    │
            │   Vault     │
            │  (Secrets)  │
            └─────────────┘
```

---

## 2. Composants Détaillés

### 2.1 Frontend (React SPA)

#### Technologies
- **Framework** : React 18.2+ avec TypeScript
- **Build** : Vite (fast HMR, optimized builds)
- **State Management** : Context API + Custom Hooks
- **Routing** : React Router v6
- **Styling** : TailwindCSS
- **Cryptographie** : WebCrypto API (chiffrement E2EE)

#### Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── UploadForm.tsx          # Formulaire upload
│   │   ├── FileDropzone.tsx         # Drag & drop
│   │   ├── DownloadPage.tsx         # Page téléchargement
│   │   ├── ProgressBar.tsx          # Indicateur progression
│   │   └── SecurityBadge.tsx        # Badge "Scanné" / "Chiffré"
│   ├── services/
│   │   ├── api.ts                   # Client HTTP (Axios)
│   │   ├── crypto.ts                # WebCrypto wrapper
│   │   └── upload.ts                # Logique upload avec chiffrement
│   ├── hooks/
│   │   ├── useUpload.ts             # Hook upload
│   │   └── useCountdown.ts          # Timer expiration
│   ├── utils/
│   │   ├── validation.ts            # Validation fichiers
│   │   └── formatters.ts            # Formatage taille, dates
│   └── App.tsx
├── public/
│   └── favicon.ico
├── Dockerfile
├── nginx.conf                       # Config Nginx avec headers sécurité
├── package.json
└── vite.config.ts
```

#### Sécurité Frontend
- **CSP** : `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'`
- **SRI** : Subresource Integrity pour CDN
- **Headers** : X-Frame-Options, X-Content-Type-Options (via Nginx)
- **HTTPS Only** : Redirection automatique
- **Sanitization** : DOMPurify pour inputs utilisateur

---

### 2.2 Backend API (FastAPI)

#### Technologies
- **Framework** : FastAPI 0.104+ (Python 3.11)
- **Server ASGI** : Uvicorn avec workers Gunicorn
- **ORM** : SQLAlchemy 2.0 (async)
- **Validation** : Pydantic v2
- **Migration DB** : Alembic
- **Task Queue** : Celery + Redis (scan antivirus asynchrone)

#### Structure
```
backend/
├── app/
│   ├── main.py                      # Point d'entrée FastAPI
│   ├── api/
│   │   ├── v1/
│   │   │   ├── upload.py            # POST /upload
│   │   │   ├── download.py          # GET /download/{token}
│   │   │   ├── health.py            # GET /health
│   │   │   └── admin.py             # Endpoints admin
│   │   └── dependencies.py          # Injections de dépendances
│   ├── core/
│   │   ├── config.py                # Settings (Pydantic BaseSettings)
│   │   ├── security.py              # Rate limiting, CORS
│   │   └── logging.py               # Config logs structurés JSON
│   ├── models/
│   │   ├── file.py                  # SQLAlchemy File model
│   │   └── audit_log.py             # Modèle logs d'audit
│   ├── schemas/
│   │   ├── file_schema.py           # Pydantic schemas
│   │   └── response_schema.py       # Réponses API
│   ├── services/
│   │   ├── storage.py               # Interface S3/MinIO
│   │   ├── encryption.py            # Chiffrement AES-GCM
│   │   ├── token_service.py         # Génération/validation tokens
│   │   ├── antivirus.py             # Integration ClamAV
│   │   └── deletion.py              # Suppression atomique
│   ├── utils/
│   │   ├── validators.py            # Validation MIME, taille
│   │   └── crypto.py                # Utilitaires cryptographiques
│   └── middleware/
│       ├── rate_limiter.py          # Rate limiting (Redis)
│       ├── security_headers.py      # Headers HTTP sécurité
│       └── audit_logger.py          # Logs structurés événements
├── tests/
│   ├── unit/
│   ├── integration/
│   └── security/                    # Tests spécifiques sécurité
├── Dockerfile
├── requirements.txt
└── pyproject.toml
```

#### Endpoints API

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| **POST** | `/api/v1/upload` | Upload fichier + génération token | Public |
| **GET** | `/api/v1/download/{token}` | Download à usage unique | Public |
| **GET** | `/api/v1/info/{token}` | Métadonnées fichier (sans download) | Public |
| **GET** | `/health` | Health check (monitoring) | Public |
| **GET** | `/metrics` | Métriques Prometheus | Internal |
| **GET** | `/admin/stats` | Statistiques plateforme | Admin |
| **POST** | `/admin/cleanup` | Cleanup manuel | Admin |

---

### 2.3 Base de Données (PostgreSQL)

#### Schéma

```sql
-- Table files : métadonnées fichiers
CREATE TABLE files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token_hash VARCHAR(64) UNIQUE NOT NULL,  -- SHA-256(token)
    filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    file_size BIGINT NOT NULL,
    storage_key VARCHAR(255) UNIQUE NOT NULL, -- S3 key
    encryption_metadata JSONB,                -- IV, tag, KEK version
    ip_hash VARCHAR(64) NOT NULL,             -- SHA-256(IP + salt)
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    downloaded_at TIMESTAMPTZ,                -- NULL = pas encore téléchargé
    antivirus_status VARCHAR(20) DEFAULT 'pending', -- pending/clean/infected
    antivirus_scanned_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index pour performance
CREATE INDEX idx_files_token_hash ON files(token_hash);
CREATE INDEX idx_files_expires_at ON files(expires_at);
CREATE INDEX idx_files_ip_hash ON files(ip_hash);

-- Table audit_logs : journalisation événements
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,  -- upload, download, delete, error
    file_id UUID REFERENCES files(id) ON DELETE SET NULL,
    ip_hash VARCHAR(64) NOT NULL,
    user_agent_hash VARCHAR(64),
    metadata JSONB,                   -- Données contextuelles
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_event_type ON audit_logs(event_type);

-- Table rate_limits : tracking quotas (backup Redis)
CREATE TABLE rate_limits (
    id SERIAL PRIMARY KEY,
    ip_hash VARCHAR(64) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,  -- upload, download, global
    count INTEGER NOT NULL DEFAULT 1,
    window_start TIMESTAMPTZ NOT NULL,
    window_end TIMESTAMPTZ NOT NULL,
    UNIQUE(ip_hash, resource_type, window_start)
);
```

#### Sécurité Base de Données
- **Chiffrement au repos** : PostgreSQL transparent data encryption (TDE)
- **Connexions TLS** : SSL mode `require`
- **Principe moindre privilège** : Comptes dédiés (app, backup, admin)
- **Auditing** : pgAudit activé pour tracer les accès
- **Backups** : Chiffrés avec pgBackRest, rétention 30 jours

---

### 2.4 Cache & Queue (Redis)

#### Utilisation

```
Redis Cluster (3 nodes)
├── DB 0 : Rate Limiting
│   ├── rate:ip:{ip_hash}:upload -> counter TTL 1h
│   ├── rate:ip:{ip_hash}:download -> counter TTL 1h
│   └── rate:ip:{ip_hash}:global -> counter TTL 1min
│
├── DB 1 : Token Status (one-time download)
│   ├── token:{token_hash}:status -> "active" | "downloaded"
│   └── token:{token_hash}:lock -> distributed lock
│
├── DB 2 : Quotas Storage
│   └── quota:ip:{ip_hash}:storage -> total bytes TTL sync with files
│
└── DB 3 : Celery Queue (task broker)
    └── celery:tasks:*
```

#### Sécurité Redis
- **Auth** : Mot de passe complexe (via Vault)
- **TLS** : Connexions chiffrées
- **Bind** : Interface privée uniquement
- **Désactivation commandes dangereuses** : FLUSHALL, CONFIG, etc.

---

### 2.5 Stockage (MinIO / AWS S3)

#### Organisation

```
Bucket: secureshare-files (private)
├── prod/
│   └── {YYYY}/{MM}/{DD}/{uuid}.enc    # Fichiers chiffrés
├── quarantine/                         # Fichiers malware détectés
│   └── {YYYY}/{MM}/{DD}/{uuid}.enc
└── (lifecycle auto-delete après expiration)
```

#### Sécurité Stockage
- **Access** : Privé, pas de public read
- **Chiffrement** : Server-side avec KMS (SSE-KMS)
- **Versioning** : Désactivé (pas de rétention après suppression)
- **Lifecycle** : Suppression automatique objets > 48h
- **Access Logs** : Activés et archivés
- **Bucket Policy** : Deny all par défaut, allow depuis backend uniquement

---

### 2.6 Gestion Secrets (HashiCorp Vault)

#### Configuration

```
Vault Cluster (HA)
├── KV Secrets Engine v2
│   ├── secret/backend/db-credentials
│   ├── secret/backend/s3-credentials
│   ├── secret/backend/redis-password
│   └── secret/antivirus/api-key
│
├── Transit Secrets Engine (encryption-as-a-service)
│   └── transit/keys/file-encryption  # KEK pour chiffrement fichiers
│
└── PKI Secrets Engine
    └── pki/issue/api-cert            # Certificats internes
```

#### Policies

```hcl
# Policy pour backend API
path "secret/data/backend/*" {
  capabilities = ["read"]
}

path "transit/encrypt/file-encryption" {
  capabilities = ["update"]
}

path "transit/decrypt/file-encryption" {
  capabilities = ["update"]
}
```

---

### 2.7 Scan Antivirus (ClamAV)

#### Architecture

```
ClamAV Service
├── Daemon : clamd (écoute port 3310)
├── Updater : freshclam (MàJ quotidiennes signatures)
└── Queue : Celery tasks asynchrones
```

#### Workflow Scan

```
1. Upload fichier → Stockage temporaire (non chiffré)
2. Celery task : scan ClamAV
3. Si clean → Chiffrement + déplacement S3 prod + génération lien
4. Si infected → Déplacement S3 quarantine + alerte + blocage lien
5. Suppression fichier temporaire
```

---

## 3. Flux de Données Sécurisés

### 3.1 Flux Upload

```
┌──────────┐
│ Client   │
└────┬─────┘
     │ 1. POST /upload (multipart/form-data)
     │    - File blob
     │    - TTL (optional, default 24h)
     ▼
┌────────────────┐
│ Load Balancer  │
│ - Rate limit   │ → 429 si dépassé
│ - TLS check    │
└────┬───────────┘
     │ 2. Validation initiale
     ▼
┌────────────────┐
│ FastAPI        │
│ - Validate MIME│ → 400 si invalide
│ - Validate size│ → 413 si > 100MB
│ - Hash IP      │
└────┬───────────┘
     │ 3. Stockage temporaire
     ▼
┌────────────────┐
│ Temp Storage   │ /tmp/{uuid}
└────┬───────────┘
     │ 4. Scan antivirus (async Celery)
     ▼
┌────────────────┐
│ ClamAV         │ → Si infected: quarantine + 403
└────┬───────────┘
     │ 5. Chiffrement
     ▼
┌────────────────┐
│ Encryption Svc │
│ - Gen DEK      │
│ - Encrypt DEK  │ ← Vault KEK
│ - AES-GCM file │
└────┬───────────┘
     │ 6. Upload S3
     ▼
┌────────────────┐
│ MinIO / S3     │ key: prod/{date}/{uuid}.enc
└────┬───────────┘
     │ 7. Enregistrement métadonnées
     ▼
┌────────────────┐
│ PostgreSQL     │
│ - token_hash   │
│ - storage_key  │
│ - expires_at   │
└────┬───────────┘
     │ 8. Génération token
     ▼
┌────────────────┐
│ Token Service  │
│ - 256-bit random│
│ - SHA-256 hash │
│ - Set Redis    │ token:*:status = "active"
└────┬───────────┘
     │ 9. Réponse
     ▼
┌──────────┐
│ Client   │ ← JSON: {"download_url": "https://.../download/{token}"}
└──────────┘
```

---

### 3.2 Flux Download (One-Time)

```
┌──────────┐
│ Client   │
└────┬─────┘
     │ 1. GET /download/{token}
     ▼
┌────────────────┐
│ FastAPI        │
│ - Hash token   │
│ - Check Redis  │ → 404 si déjà téléchargé
└────┬───────────┘
     │ 2. Distributed Lock (Redis)
     ▼
┌────────────────┐
│ Redis SETNX    │ token:{hash}:lock (TTL 30s)
└────┬───────────┘
     │ 3. Vérification atomique
     ▼
┌────────────────┐
│ PostgreSQL     │
│ - SELECT file  │ → 404 si expiré
│ - WHERE        │ → 410 si déjà downloaded
│   downloaded_at│
│   IS NULL      │
└────┬───────────┘
     │ 4. Récupération blob S3
     ▼
┌────────────────┐
│ MinIO / S3     │ GET prod/{storage_key}
└────┬───────────┘
     │ 5. Déchiffrement streaming
     ▼
┌────────────────┐
│ Encryption Svc │
│ - Decrypt DEK  │ ← Vault KEK
│ - Stream AES   │
└────┬───────────┘
     │ 6. Stream au client
     ▼
┌──────────┐
│ Client   │ ← Content-Disposition: attachment
└────┬─────┘
     │ 7. Après envoi complet
     ▼
┌────────────────┐
│ Deletion Svc   │
│ - Mark Redis   │ token:*:status = "downloaded"
│ - UPDATE files │ SET downloaded_at = NOW()
│ - DELETE S3    │
│ - Audit log    │
└────────────────┘
```

---

### 3.3 Flux Suppression Automatique (Expiration)

```
┌────────────────┐
│ Cron Job       │ (toutes les heures)
│ cleanup.py     │
└────┬───────────┘
     │ 1. SELECT files WHERE expires_at < NOW()
     ▼
┌────────────────┐
│ PostgreSQL     │ → Liste des fichiers expirés
└────┬───────────┘
     │ 2. Pour chaque fichier
     ▼
┌────────────────┐
│ Deletion Svc   │
│ - DELETE S3    │
│ - DELETE Redis │
│ - DELETE DB    │
│ - Audit log    │
└────────────────┘
```

---

## 4. Sécurité Réseau

### 4.1 Segmentation

```
┌─────────────────────────────────────────────┐
│             DMZ (Zone Publique)             │
│  ┌──────────────┐      ┌──────────────┐    │
│  │ Load Balancer│      │   Frontend   │    │
│  │   (Public)   │      │   (Static)   │    │
│  └──────────────┘      └──────────────┘    │
└─────────────┬──────────────┬────────────────┘
              │              │
              Firewall (Allow HTTPS 443 only)
              │              │
┌─────────────▼──────────────▼────────────────┐
│          Zone Application                   │
│  ┌──────────────┐    ┌──────────────┐      │
│  │   Backend    │    │   ClamAV     │      │
│  │   (FastAPI)  │    │   (Scan)     │      │
│  └──────────────┘    └──────────────┘      │
└─────────────┬──────────────────────────────┘
              │
              Firewall (Allow Backend only)
              │
┌─────────────▼────────────────────────────────┐
│          Zone Données                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │PostgreSQL│  │  Redis  │  │  MinIO  │     │
│  └─────────┘  └─────────┘  └─────────┘     │
└──────────────────────────────────────────────┘
              │
              Firewall (No internet access)
              │
┌─────────────▼────────────────────────────────┐
│         Zone Secrets                         │
│  ┌───────────────────────────────┐           │
│  │      HashiCorp Vault          │           │
│  │    (Sealed, HA, Audit)        │           │
│  └───────────────────────────────┘           │
└──────────────────────────────────────────────┘
```

### 4.2 Règles Firewall

| Source | Destination | Port | Protocole | Action |
|--------|-------------|------|-----------|--------|
| Internet | Load Balancer | 443 | TCP | ALLOW |
| Load Balancer | Backend | 8000 | TCP | ALLOW |
| Backend | PostgreSQL | 5432 | TCP | ALLOW |
| Backend | Redis | 6379 | TCP | ALLOW |
| Backend | MinIO | 9000 | TCP | ALLOW |
| Backend | ClamAV | 3310 | TCP | ALLOW |
| Backend | Vault | 8200 | TCP | ALLOW |
| * | * | * | * | DENY |

---

## 5. Haute Disponibilité

### 5.1 Architecture HA

```
                    ┌─── Replica 1 ───┐
Load Balancer ──────┤                 │
(Active/Standby)    ├─── Replica 2 ───┤  Backend (3+ pods)
                    └─── Replica 3 ───┘

PostgreSQL: Primary + Standby (streaming replication)
Redis: Cluster 3 masters + 3 replicas
MinIO: Distributed mode (4+ nodes)
Vault: 3 nodes HA avec Raft storage
```

### 5.2 Objectifs

- **RTO** (Recovery Time Objective) : < 15 minutes
- **RPO** (Recovery Point Objective) : < 5 minutes
- **Uptime** : 99.5% (objectif)

---

## 6. Monitoring & Observabilité

### 6.1 Stack

- **Metrics** : Prometheus + Grafana
- **Logs** : ELK Stack (Elasticsearch, Logstash, Kibana) ou Loki
- **Traces** : Jaeger (OpenTelemetry)
- **Alerting** : Alertmanager → Slack/PagerDuty

### 6.2 Métriques Collectées

```python
# FastAPI custom metrics (Prometheus client)
- secureshare_uploads_total{status="success|failed"}
- secureshare_downloads_total{status="success|failed"}
- secureshare_malware_detected_total
- secureshare_file_size_bytes (histogram)
- secureshare_latency_seconds (histogram)
- secureshare_rate_limit_hits_total
```

---

## 7. Scalabilité

### 7.1 Scaling Horizontal

| Composant | Stratégie | Trigger |
|-----------|-----------|---------|
| **Backend** | Kubernetes HPA | CPU > 70% |
| **PostgreSQL** | Read replicas | Connexions > 80% |
| **Redis** | Cluster sharding | Memory > 75% |
| **MinIO** | Add nodes | Storage > 80% |

### 7.2 Limites Actuelles (MVP)

- **Uploads** : 10 req/s (100 MB/s throughput)
- **Downloads** : 50 req/s (500 MB/s throughput)
- **Storage** : 1 TB total
- **Concurrent users** : 1000

---

## 8. Disaster Recovery

### 8.1 Backups

| Composant | Fréquence | Rétention | Stockage |
|-----------|-----------|-----------|----------|
| PostgreSQL | Quotidien + WAL | 30 jours | S3 chiffré |
| Redis | Snapshot quotidien | 7 jours | S3 chiffré |
| MinIO | Pas de backup (fichiers éphémères) | - | - |
| Vault | Snapshot quotidien | 90 jours | S3 chiffré + offline |

### 8.2 Procédure de Restauration

Voir [06-MANUEL-DEPLOIEMENT.md](06-MANUEL-DEPLOIEMENT.md)

---

**🏗️ Document de référence technique - Révision à chaque changement architectural**
