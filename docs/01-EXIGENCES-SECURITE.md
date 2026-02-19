# 🔒 Exigences de Sécurité - SecureShare

**Document**: Spécifications des exigences de sécurité
**Version**: 1.0
**Date**: 2025-12-05
**Statut**: ✅ Approuvé

---

## 1. Introduction

### 1.1 Objectif du document

Ce document définit les exigences de sécurité pour la plateforme **SecureShare**, un service SaaS de partage de fichiers éphémères et sécurisés. Il établit les standards, contrôles et mesures de sécurité obligatoires pour garantir la confidentialité, l'intégrité et la disponibilité du service.

### 1.2 Périmètre

- Application web (frontend React)
- API backend (FastAPI)
- Infrastructure (containers, stockage, base de données)
- Pipeline CI/CD DevSecOps
- Gestion des données utilisateurs

### 1.3 Références normatives

- **OWASP Top 10** (2021)
- **OWASP ASVS** v4.0 (Application Security Verification Standard)
- **ISO/IEC 27001:2013** - Système de management de la sécurité de l'information
- **RGPD** (Règlement Général sur la Protection des Données)
- **ANSSI** - Recommandations de sécurité relatives à TLS
- **NIST Cybersecurity Framework**

---

## 2. Classification des Données

### 2.1 Types de données

| Catégorie | Description | Niveau de sensibilité | Durée de conservation |
|-----------|-------------|----------------------|----------------------|
| **Fichiers utilisateurs** | Fichiers uploadés temporairement | **CRITIQUE** | ≤ 48h ou 1 téléchargement |
| **Métadonnées** | Nom fichier, taille, date, IP hashée | **SENSIBLE** | 90 jours (audit) |
| **Logs d'audit** | Événements système, accès, erreurs | **SENSIBLE** | 1 an |
| **Clés de chiffrement** | Clés AES-256, secrets API | **CRITIQUE** | Rotation tous les 90 jours |
| **Tokens d'accès** | Liens de téléchargement à usage unique | **SENSIBLE** | TTL ≤ 48h |

### 2.2 Exigences par classification

#### Données CRITIQUES
- ✅ Chiffrement obligatoire (AES-256-GCM minimum)
- ✅ Accès strictement contrôlé (principe du moindre privilège)
- ✅ Journalisation complète de tous les accès
- ✅ Suppression sécurisée garantie (wiping)
- ✅ Sauvegarde chiffrée si applicable

#### Données SENSIBLES
- ✅ Chiffrement en transit (TLS 1.3)
- ✅ Hashage des identifiants personnels (IP, user-agent)
- ✅ Rétention limitée selon RGPD
- ✅ Accès audité

---

## 3. Exigences de Sécurité par Domaine

### 3.1 Authentification & Autorisation

#### 3.1.1 Authentification (si implémentée)

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **AUTH-01** | Authentification multi-facteurs (MFA) pour accès administrateur | **OBLIGATOIRE** | OWASP ASVS 2.1 |
| **AUTH-02** | Politique de mots de passe: min 12 caractères, complexité, pas de mots communs | **OBLIGATOIRE** | OWASP ASVS 2.1 |
| **AUTH-03** | Limitation des tentatives de connexion (5 max / 15 min) | **OBLIGATOIRE** | OWASP ASVS 2.2 |
| **AUTH-04** | Tokens de session avec expiration (30 min inactivité) | **OBLIGATOIRE** | OWASP ASVS 3.2 |
| **AUTH-05** | Stockage sécurisé des mots de passe (Argon2id ou bcrypt) | **OBLIGATOIRE** | OWASP ASVS 2.4 |

#### 3.1.2 Autorisation

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **AUTHZ-01** | Contrôle d'accès basé sur les tokens (RBAC) | **OBLIGATOIRE** | OWASP ASVS 4.1 |
| **AUTHZ-02** | Validation de tous les tokens côté serveur | **OBLIGATOIRE** | OWASP ASVS 4.2 |
| **AUTHZ-03** | Principe du moindre privilège (least privilege) | **OBLIGATOIRE** | ISO 27001 A.9.2 |
| **AUTHZ-04** | Tokens à usage unique (one-time download links) | **OBLIGATOIRE** | Requis métier |

### 3.2 Cryptographie

#### 3.2.1 Chiffrement en transit

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **CRYPTO-01** | TLS 1.3 obligatoire (désactivation TLS < 1.2) | **OBLIGATOIRE** | ANSSI TLS |
| **CRYPTO-02** | HSTS activé (max-age=31536000; includeSubDomains; preload) | **OBLIGATOIRE** | OWASP ASVS 9.2 |
| **CRYPTO-03** | Cipher suites modernes uniquement (ECDHE, AEAD) | **OBLIGATOIRE** | ANSSI TLS |
| **CRYPTO-04** | Certificate pinning pour API mobile (si applicable) | **RECOMMANDÉ** | OWASP MASTG |

#### 3.2.2 Chiffrement au repos

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **CRYPTO-05** | Chiffrement AES-256-GCM pour tous les fichiers stockés | **OBLIGATOIRE** | OWASP ASVS 6.2 |
| **CRYPTO-06** | Gestion des clés via KMS dédié (Vault, AWS KMS) | **OBLIGATOIRE** | OWASP ASVS 6.1 |
| **CRYPTO-07** | Rotation des clés de chiffrement tous les 90 jours | **OBLIGATOIRE** | NIST SP 800-57 |
| **CRYPTO-08** | Chiffrement de la base de données au repos | **OBLIGATOIRE** | ISO 27001 A.10.1 |
| **CRYPTO-09** | Option E2EE côté client (WebCrypto API) | **RECOMMANDÉ** | Requis métier |

#### 3.2.3 Hachage et intégrité

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **CRYPTO-10** | Hachage SHA-256 minimum pour vérification d'intégrité | **OBLIGATOIRE** | OWASP ASVS 6.2 |
| **CRYPTO-11** | Hachage des tokens (ne jamais stocker en clair) | **OBLIGATOIRE** | OWASP ASVS 3.5 |
| **CRYPTO-12** | HMAC pour signatures de messages critiques | **OBLIGATOIRE** | OWASP ASVS 6.2 |

### 3.3 Sécurité des Données

#### 3.3.1 Protection des fichiers

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **DATA-01** | Validation stricte du type MIME (whitelist) | **OBLIGATOIRE** | OWASP Top 10 A03 |
| **DATA-02** | Limite de taille par fichier (max 100 MB) | **OBLIGATOIRE** | Requis métier |
| **DATA-03** | Scan antivirus obligatoire avant mise à disposition | **OBLIGATOIRE** | OWASP ASVS 12.1 |
| **DATA-04** | Suppression atomique et immédiate après téléchargement | **OBLIGATOIRE** | Requis métier |
| **DATA-05** | Expiration automatique (TTL max 48h) | **OBLIGATOIRE** | Requis métier |
| **DATA-06** | Isolation des fichiers par token (pas de listing) | **OBLIGATOIRE** | OWASP ASVS 4.1 |

#### 3.3.2 Suppression sécurisée

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **DATA-07** | Suppression physique du blob S3 immédiate | **OBLIGATOIRE** | Requis métier |
| **DATA-08** | Suppression des métadonnées en base de données | **OBLIGATOIRE** | RGPD Art. 17 |
| **DATA-09** | Invalidation du token dans Redis | **OBLIGATOIRE** | Requis métier |
| **DATA-10** | Journalisation de la suppression (audit trail) | **OBLIGATOIRE** | ISO 27001 A.12.4 |
| **DATA-11** | Documentation des limites (backups, snapshots) | **OBLIGATOIRE** | RGPD Transparence |

### 3.4 Sécurité Applicative

#### 3.4.1 Protection contre OWASP Top 10

| ID | Exigence | Menace OWASP | Niveau |
|----|----------|--------------|--------|
| **APP-01** | Validation et sanitization de toutes les entrées | A03 - Injection | **OBLIGATOIRE** |
| **APP-02** | Requêtes SQL paramétrées (ORM uniquement) | A03 - Injection | **OBLIGATOIRE** |
| **APP-03** | Content Security Policy (CSP) stricte | A03 - Injection | **OBLIGATOIRE** |
| **APP-04** | Protection CSRF avec tokens uniques | A01 - Broken Access | **OBLIGATOIRE** |
| **APP-05** | Headers de sécurité (X-Frame-Options, X-Content-Type-Options) | A05 - Security Misconfig | **OBLIGATOIRE** |
| **APP-06** | Désactivation de la mise en cache pour contenu sensible | A01 - Broken Access | **OBLIGATOIRE** |
| **APP-07** | Gestion sécurisée des erreurs (pas de stack trace en prod) | A05 - Security Misconfig | **OBLIGATOIRE** |
| **APP-08** | Désactivation des méthodes HTTP non utilisées (TRACE, OPTIONS) | A05 - Security Misconfig | **OBLIGATOIRE** |

#### 3.4.2 Rate Limiting & Anti-Abuse

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **RATE-01** | Rate limiting global: 100 req/min par IP | **OBLIGATOIRE** | OWASP API Security |
| **RATE-02** | Rate limiting upload: 10 fichiers/heure par IP | **OBLIGATOIRE** | Requis métier |
| **RATE-03** | Rate limiting download: 50 tentatives/heure par IP | **OBLIGATOIRE** | Requis métier |
| **RATE-04** | CAPTCHA après 3 tentatives d'accès invalides | **OBLIGATOIRE** | OWASP ASVS 2.2 |
| **RATE-05** | Blacklist automatique des IPs abusives (> 1000 req/h) | **OBLIGATOIRE** | OWASP API Security |
| **RATE-06** | Quota de stockage par IP (max 1 GB) | **RECOMMANDÉ** | Requis métier |

### 3.5 Journalisation & Audit

#### 3.5.1 Événements à logger

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **LOG-01** | Logs structurés au format JSON | **OBLIGATOIRE** | OWASP Logging Cheat Sheet |
| **LOG-02** | Horodatage UTC avec précision à la seconde | **OBLIGATOIRE** | ISO 27001 A.12.4 |
| **LOG-03** | Événements : upload, download, suppression, erreurs, abus | **OBLIGATOIRE** | ISO 27001 A.12.4 |
| **LOG-04** | Logs immuables (append-only, pas de modification) | **OBLIGATOIRE** | ISO 27001 A.12.4 |
| **LOG-05** | Rétention des logs : 1 an minimum | **OBLIGATOIRE** | Conformité légale |

#### 3.5.2 Protection des logs

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **LOG-06** | Pas de données sensibles en clair (RGPD) | **OBLIGATOIRE** | RGPD Art. 5 |
| **LOG-07** | Hashage des IPs (SHA-256 avec salt quotidien) | **OBLIGATOIRE** | RGPD minimisation |
| **LOG-08** | Chiffrement des logs archivés | **OBLIGATOIRE** | ISO 27001 A.12.3 |
| **LOG-09** | Contrôle d'accès restreint aux logs (admin seul) | **OBLIGATOIRE** | ISO 27001 A.9.4 |

### 3.6 Sécurité Infrastructure

#### 3.6.1 Containers & Orchestration

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **INFRA-01** | Images Docker depuis registres officiels uniquement | **OBLIGATOIRE** | CIS Docker Benchmark |
| **INFRA-02** | Scan de vulnérabilités des images (Trivy, Snyk) | **OBLIGATOIRE** | OWASP DevSecOps |
| **INFRA-03** | Pas d'exécution en tant que root (USER non-root) | **OBLIGATOIRE** | CIS Docker Benchmark |
| **INFRA-04** | Secrets injectés via variables d'environnement ou Vault | **OBLIGATOIRE** | OWASP DevSecOps |
| **INFRA-05** | Network policies pour isolation des pods (K8s) | **OBLIGATOIRE** | CIS Kubernetes Benchmark |

#### 3.6.2 Base de données

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **DB-01** | Principe du moindre privilège (comptes dédiés par service) | **OBLIGATOIRE** | CIS PostgreSQL Benchmark |
| **DB-02** | Connexions chiffrées uniquement (TLS) | **OBLIGATOIRE** | OWASP ASVS 9.2 |
| **DB-03** | Mots de passe complexes et rotation tous les 90 jours | **OBLIGATOIRE** | ISO 27001 A.9.4 |
| **DB-04** | Sauvegardes chiffrées et testées mensuellement | **OBLIGATOIRE** | ISO 27001 A.12.3 |
| **DB-05** | Désactivation des comptes par défaut | **OBLIGATOIRE** | CIS PostgreSQL Benchmark |

#### 3.6.3 Stockage (S3/MinIO)

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **STORAGE-01** | Buckets privés uniquement (pas de public access) | **OBLIGATOIRE** | AWS Security Best Practices |
| **STORAGE-02** | Versioning activé avec expiration automatique | **OBLIGATOIRE** | Requis métier |
| **STORAGE-03** | Access logs activés et monitored | **OBLIGATOIRE** | ISO 27001 A.12.4 |
| **STORAGE-04** | Chiffrement server-side (SSE-KMS) | **OBLIGATOIRE** | AWS Security Best Practices |
| **STORAGE-05** | Politique de lifecycle pour suppression automatique | **OBLIGATOIRE** | Requis métier |

### 3.7 DevSecOps & Pipeline CI/CD

#### 3.7.1 Tests de sécurité automatisés

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **CICD-01** | SAST obligatoire à chaque commit (Bandit, Semgrep) | **OBLIGATOIRE** | OWASP DevSecOps |
| **CICD-02** | Dependency scanning (Safety, Snyk, npm audit) | **OBLIGATOIRE** | OWASP DevSecOps |
| **CICD-03** | Secret scanning (GitGuardian, TruffleHog) | **OBLIGATOIRE** | OWASP DevSecOps |
| **CICD-04** | Container scanning (Trivy) | **OBLIGATOIRE** | OWASP DevSecOps |
| **CICD-05** | DAST en pré-production (OWASP ZAP) | **RECOMMANDÉ** | OWASP DevSecOps |
| **CICD-06** | Blocage du déploiement si vulnérabilités critiques | **OBLIGATOIRE** | OWASP DevSecOps |

#### 3.7.2 Gestion des secrets

| ID | Exigence | Niveau | Standard |
|----|----------|--------|----------|
| **SECRET-01** | Pas de secrets en clair dans le code source | **OBLIGATOIRE** | OWASP Top 10 A05 |
| **SECRET-02** | Utilisation d'un gestionnaire de secrets (Vault, AWS Secrets Manager) | **OBLIGATOIRE** | OWASP DevSecOps |
| **SECRET-03** | Rotation automatique des secrets tous les 90 jours | **OBLIGATOIRE** | NIST SP 800-57 |
| **SECRET-04** | Secrets uniques par environnement (dev/staging/prod) | **OBLIGATOIRE** | OWASP DevSecOps |

### 3.8 Conformité RGPD

#### 3.8.1 Principes de protection des données

| ID | Exigence | Article RGPD | Niveau |
|----|----------|--------------|--------|
| **RGPD-01** | Minimisation des données collectées | Art. 5(1)(c) | **OBLIGATOIRE** |
| **RGPD-02** | Finalité explicite et légitime | Art. 5(1)(b) | **OBLIGATOIRE** |
| **RGPD-03** | Limitation de la conservation (TTL max 48h) | Art. 5(1)(e) | **OBLIGATOIRE** |
| **RGPD-04** | Intégrité et confidentialité (chiffrement) | Art. 5(1)(f) | **OBLIGATOIRE** |
| **RGPD-05** | Transparence (politique de confidentialité claire) | Art. 12 | **OBLIGATOIRE** |

#### 3.8.2 Droits des personnes

| ID | Exigence | Article RGPD | Niveau |
|----|----------|--------------|--------|
| **RGPD-06** | Droit d'accès aux données personnelles | Art. 15 | **OBLIGATOIRE** |
| **RGPD-07** | Droit à l'effacement (suppression garantie) | Art. 17 | **OBLIGATOIRE** |
| **RGPD-08** | Information en cas de violation de données (< 72h) | Art. 33-34 | **OBLIGATOIRE** |
| **RGPD-09** | DPIA (Data Protection Impact Assessment) documentée | Art. 35 | **OBLIGATOIRE** |

---

## 4. Niveaux de Sécurité et Priorisation

### 4.1 Classification par criticité

| Niveau | Définition | Impact si non respecté | Action |
|--------|------------|------------------------|--------|
| **CRITIQUE** | Exigence obligatoire pour mise en production | Blocage déploiement | Correction immédiate |
| **ÉLEVÉ** | Exigence obligatoire mais dérogation possible | Risque juridique/réputationnel | Correction < 7 jours |
| **MOYEN** | Recommandé, bonne pratique | Risque opérationnel | Correction < 30 jours |
| **FAIBLE** | Nice-to-have, amélioration continue | Optimisation | Backlog |

### 4.2 Matrice de priorisation

| Domaine | Exigences CRITIQUES | Exigences ÉLEVÉES | Exigences MOYENNES |
|---------|---------------------|-------------------|-------------------|
| **Cryptographie** | 8 | 2 | 3 |
| **Protection données** | 11 | 0 | 0 |
| **Application** | 8 | 0 | 0 |
| **Infrastructure** | 10 | 5 | 2 |
| **DevSecOps** | 6 | 1 | 0 |
| **RGPD** | 9 | 0 | 0 |
| **TOTAL** | **52** | **8** | **5** |

---

## 5. Validation et Vérification

### 5.1 Checklist de conformité

Avant chaque release, valider que **100% des exigences CRITIQUES** sont implémentées.

```
□ Tous les fichiers sont chiffrés (AES-256-GCM)
□ TLS 1.3 activé et testé
□ Rate limiting fonctionnel
□ Scan antivirus opérationnel
□ Suppression après téléchargement testée
□ Logs d'audit activés et conformes
□ Pipeline DevSecOps complet (SAST + SCA)
□ Tests de sécurité automatisés passés
□ DPIA documentée et approuvée
□ Politique de confidentialité publiée
```

### 5.2 Audits de sécurité

| Type d'audit | Fréquence | Responsable | Livrable |
|--------------|-----------|-------------|----------|
| **Code review sécurité** | Chaque PR | Équipe dev | Checklist OWASP |
| **Scan automatisé** | Chaque commit | CI/CD | Rapport Bandit/Trivy |
| **Pentest interne** | Mensuel | Responsable sécu | Rapport vulnérabilités |
| **Audit externe** | Avant mise en prod | Auditeur tiers | Rapport de conformité |

---

## 6. Gestion des Exceptions

### 6.1 Processus de dérogation

En cas d'impossibilité technique de respecter une exigence CRITIQUE :

1. **Documentation** : Justification détaillée de l'exception
2. **Analyse de risque** : Évaluation de l'impact résiduel
3. **Mesures compensatoires** : Contrôles alternatifs mis en place
4. **Approbation** : Validation par le responsable sécurité + chef de projet
5. **Traçabilité** : Enregistrement dans le registre des dérogations
6. **Revue** : Réévaluation trimestrielle

### 6.2 Registre des dérogations

| ID | Exigence | Justification | Mesure compensatoire | Date fin | Statut |
|----|----------|---------------|---------------------|----------|--------|
| _Exemple_ | CRYPTO-09 (E2EE) | Complexité UX trop élevée pour MVP | Chiffrement serveur renforcé + HSM | 2025-06-01 | Active |

---

## 7. Responsabilités

| Rôle | Responsabilités |
|------|----------------|
| **Chef de projet** | Validation des exigences, arbitrage des dérogations |
| **Responsable sécurité** | Définition des exigences, audits, conformité |
| **Développeurs** | Implémentation, tests unitaires sécurité, code review |
| **DevOps** | Pipeline CI/CD, infrastructure sécurisée, monitoring |
| **Auditeur externe** | Validation indépendante avant production |

---

## 8. Révisions du Document

| Version | Date | Auteur | Modifications |
|---------|------|--------|---------------|
| 1.0 | 2025-12-05 | Équipe projet | Version initiale |

---

## 9. Annexes

### Annexe A : Références OWASP Top 10 2021

- **A01** - Broken Access Control
- **A02** - Cryptographic Failures
- **A03** - Injection
- **A04** - Insecure Design
- **A05** - Security Misconfiguration
- **A06** - Vulnerable and Outdated Components
- **A07** - Identification and Authentication Failures
- **A08** - Software and Data Integrity Failures
- **A09** - Security Logging and Monitoring Failures
- **A10** - Server-Side Request Forgery (SSRF)

### Annexe B : Outils de sécurité recommandés

**SAST** : Bandit (Python), Semgrep, ESLint Security Plugin
**DAST** : OWASP ZAP, Burp Suite
**SCA** : Safety, Snyk, npm audit, Trivy
**Secret scanning** : GitGuardian, TruffleHog, detect-secrets
**Container scanning** : Trivy, Clair, Anchore
**Pentest** : Metasploit, Nmap, Nikto

