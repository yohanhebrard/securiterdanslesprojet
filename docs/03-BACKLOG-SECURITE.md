# 📋 Backlog Sécurité - SecureShare

**Document**: Product backlog avec user stories sécurité
**Version**: 1.0
**Date**: 2025-12-05
**Statut**: ✅ Prêt pour sprint planning

---

## 1. Organisation du Backlog

### 1.1 Structure

Ce backlog est organisé par **épics sécurité**, chacune contenant des **user stories** priorisées selon la méthode **MoSCoW** :

- **MUST** (P0) : Blocant pour mise en production
- **SHOULD** (P1) : Requis pour beta publique
- **COULD** (P2) : Nice-to-have, amélioration continue
- **WON'T** (Hors scope MVP)

### 1.2 Estimation

Utilisation de **story points** (Fibonacci) :
- **1 pt** : < 2h (trivial)
- **2 pts** : 2-4h (simple)
- **3 pts** : 4-8h (moyen)
- **5 pts** : 1-2 jours (complexe)
- **8 pts** : 2-4 jours (très complexe)
- **13 pts** : > 4 jours (à découper)

### 1.3 Definition of Done (DoD) Sécurité

Pour qu'une user story soit considérée comme **Done** :

- ✅ Code implémenté et fonctionnel
- ✅ Tests unitaires écrits (coverage > 80%)
- ✅ Tests de sécurité spécifiques passés
- ✅ Code review sécurité approuvée
- ✅ SAST/DAST/SCA passés sans vulnérabilités critiques
- ✅ Documentation technique à jour
- ✅ Déployé en environnement de test

---

## 2. EPIC 1 : Chiffrement et Protection des Données

**Objectif** : Garantir la confidentialité des fichiers au repos et en transit

### US-CRYPTO-001 : Chiffrement serveur AES-256-GCM
**Priorité** : MUST (P0)
**Story points** : 5
**Risque associé** : R-02

**En tant que** utilisateur,
**Je veux que** mes fichiers soient chiffrés de manière sécurisée sur le serveur,
**Afin de** protéger leur confidentialité même en cas de compromission du stockage.

**Critères d'acceptation** :
- [ ] Tous les fichiers uploadés sont chiffrés avec AES-256-GCM avant stockage
- [ ] Clés de chiffrement uniques par fichier (DEK - Data Encryption Key)
- [ ] DEK chiffrées avec KEK (Key Encryption Key) gérée par Vault/KMS
- [ ] Métadonnées de chiffrement stockées de manière sécurisée
- [ ] Tests de chiffrement/déchiffrement passés (round-trip)

**Tests de sécurité** :
- Vérifier que fichiers sur S3 sont bien chiffrés (impossible de lire en clair)
- Tester la rotation de KEK sans perte de données
- Vérifier l'impossibilité de déchiffrer sans la clé

**Tâches techniques** :
- [ ] Intégrer bibliothèque cryptographique (cryptography.io Python)
- [ ] Configurer HashiCorp Vault ou AWS KMS
- [ ] Implémenter service de chiffrement/déchiffrement
- [ ] Ajouter middleware de chiffrement sur upload
- [ ] Tester la performance (latence < 100ms pour 10MB)

---

### US-CRYPTO-002 : TLS 1.3 obligatoire avec HSTS
**Priorité** : MUST (P0)
**Story points** : 3
**Risque associé** : R-07

**En tant que** utilisateur,
**Je veux que** toutes mes communications soient chiffrées avec TLS moderne,
**Afin de** prévenir l'interception de mes fichiers et tokens.

**Critères d'acceptation** :
- [ ] TLS 1.3 activé, TLS < 1.2 désactivé
- [ ] HSTS configuré (max-age=31536000; includeSubDomains; preload)
- [ ] Cipher suites modernes uniquement (ECDHE-AESGCM, ChaCha20-Poly1305)
- [ ] Certificat SSL valide (Let's Encrypt ou CA commerciale)
- [ ] Redirection HTTP → HTTPS automatique

**Tests de sécurité** :
- SSL Labs test : score A+ minimum
- Tester connexion TLS 1.0/1.1 (doit être rejetée)
- Vérifier HSTS header présent
- Tester downgrade attack (doit échouer)

---

### US-CRYPTO-003 : Rotation automatique des clés de chiffrement
**Priorité** : SHOULD (P1)
**Story points** : 5
**Risque associé** : R-02

**En tant qu'** administrateur système,
**Je veux** une rotation automatique des clés de chiffrement,
**Afin de** limiter l'impact d'une compromission de clé.

**Critères d'acceptation** :
- [ ] Rotation de la KEK tous les 90 jours
- [ ] Réencryption des DEK avec la nouvelle KEK
- [ ] Pas d'interruption de service pendant la rotation
- [ ] Logs d'audit de rotation
- [ ] Alerte si rotation échoue

---

### US-CRYPTO-004 : Option chiffrement côté client (E2EE)
**Priorité** : COULD (P2)
**Story points** : 8
**Risque associé** : R-02

**En tant qu'** utilisateur avancé,
**Je veux** chiffrer mes fichiers côté client avant upload,
**Afin que** le serveur ne puisse jamais accéder au contenu en clair.

**Critères d'acceptation** :
- [ ] Utilisation de WebCrypto API (AES-GCM)
- [ ] Génération de clé aléatoire dans le navigateur
- [ ] Clé incluse dans le token de partage (#fragment)
- [ ] Serveur stocke blob chiffré sans connaître la clé
- [ ] UX claire : badge "Chiffré de bout en bout"

**Limitations** :
- Pas de scan antivirus possible (blob chiffré opaque)
- Perte de clé = perte de fichier (pas de récupération)

---

## 3. EPIC 2 : Gestion Sécurisée des Tokens

**Objectif** : Empêcher l'accès non autorisé via brute force ou vol de tokens

### US-TOKEN-001 : Tokens cryptographiquement sécurisés
**Priorité** : MUST (P0)
**Story points** : 3
**Risque associé** : R-01

**En tant que** développeur,
**Je veux** générer des tokens impossibles à deviner,
**Afin de** protéger les fichiers contre le brute force.

**Critères d'acceptation** :
- [ ] Tokens de 32+ caractères (256 bits aléatoires)
- [ ] Génération avec `secrets.token_urlsafe()` (Python) ou équivalent
- [ ] Format base64url (compatible URLs)
- [ ] Stockage en base : hash SHA-256 uniquement (jamais en clair)
- [ ] Entropie vérifiée : minimum 256 bits

**Tests de sécurité** :
- Générer 10 000 tokens et vérifier unicité
- Vérifier impossibilité de retrouver le token depuis le hash
- Tester collisions (probabilité négligeable)

---

### US-TOKEN-002 : Tokens à usage unique (one-time download)
**Priorité** : MUST (P0)
**Story points** : 5
**Risque associé** : R-01

**En tant qu'** utilisateur,
**Je veux que** mon lien de partage soit invalide après le premier téléchargement,
**Afin de** garantir que le fichier ne sera vu qu'une seule fois.

**Critères d'acceptation** :
- [ ] Vérification atomique en Redis : `GETDEL` ou transaction Lua
- [ ] Invalidation du token immédiate après download
- [ ] Message clair : "Ce lien a déjà été utilisé" si réutilisation
- [ ] Logs d'audit : qui/quand a téléchargé
- [ ] Tests de concurrence : 2 downloads simultanés → 1 seul réussit

**Tâches techniques** :
- [ ] Implémenter transaction Redis avec flag "downloaded"
- [ ] Middleware de vérification pré-download
- [ ] Tests de race conditions (10 threads simultanés)

---

### US-TOKEN-003 : Expiration automatique (TTL)
**Priorité** : MUST (P0)
**Story points** : 2
**Risque associé** : R-01

**En tant qu'** utilisateur,
**Je veux que** mes liens expirent automatiquement après 24-48h,
**Afin de** limiter la fenêtre d'exposition.

**Critères d'acceptation** :
- [ ] TTL configurable par upload (défaut: 24h, max: 48h)
- [ ] Expiration gérée par Redis (EXPIRE) + cron DB cleanup
- [ ] Message clair : "Ce lien a expiré le [date]"
- [ ] Suppression automatique du fichier à expiration
- [ ] Indicateur visuel : "Expire dans 3h 25min"

---

### US-TOKEN-004 : Rate limiting sur accès aux tokens
**Priorité** : MUST (P0)
**Story points** : 3
**Risque associé** : R-01

**En tant que** système,
**Je veux** limiter le nombre de tentatives d'accès par IP,
**Afin de** bloquer les attaques par brute force.

**Critères d'acceptation** :
- [ ] Limite : 10 tentatives de download par heure par IP
- [ ] Limite : 50 vérifications de token par heure par IP
- [ ] CAPTCHA après 3 tentatives échouées
- [ ] Blacklist automatique si > 100 tentatives/heure
- [ ] Logs des IPs bloquées

**Tests de sécurité** :
- Simuler 100 requêtes en 1 min → blocage après 10
- Vérifier déblocage automatique après 1h

---

## 4. EPIC 3 : Protection contre les Malwares et Contenus Malveillants

**Objectif** : Empêcher l'upload et la distribution de fichiers dangereux

### US-MALWARE-001 : Scan antivirus obligatoire
**Priorité** : MUST (P0)
**Story points** : 5
**Risque associé** : R-03

**En tant que** téléchargeur,
**Je veux que** les fichiers soient scannés avant mise à disposition,
**Afin de** ne pas être infecté par un malware.

**Critères d'acceptation** :
- [ ] Intégration ClamAV (ou API VirusTotal en backup)
- [ ] Scan automatique après upload, avant génération du lien
- [ ] Quarantaine si fichier suspect (pas de lien généré)
- [ ] Alerte automatique à l'admin si détection
- [ ] Badge "Fichier scanné" visible sur page de download

**Tâches techniques** :
- [ ] Installer ClamAV dans container dédié
- [ ] API REST pour scan (POST /scan)
- [ ] Timeout: 60s max par fichier
- [ ] Mise à jour quotidienne des signatures virales

**Tests de sécurité** :
- Tester avec EICAR test file (doit être bloqué)
- Vérifier détection de ransomware connu
- Tester fichier légitime (doit passer)

---

### US-MALWARE-002 : Validation stricte des types MIME
**Priorité** : MUST (P0)
**Story points** : 2
**Risque associé** : R-03

**En tant que** système,
**Je veux** n'accepter que des types de fichiers autorisés,
**Afin de** réduire la surface d'attaque.

**Critères d'acceptation** :
- [ ] Whitelist MIME types : PDF, images (JPEG, PNG), documents Office, ZIP
- [ ] Vérification MIME via magic bytes (pas seulement extension)
- [ ] Rejet des exécutables (.exe, .sh, .bat, .ps1)
- [ ] Message clair : "Type de fichier non autorisé"

**Tests de sécurité** :
- Tester upload .exe → rejeté
- Tester .exe renommé en .pdf → détecté et rejeté (magic bytes)
- Tester .pdf légitime → accepté

---

### US-MALWARE-003 : Limite de taille par fichier
**Priorité** : MUST (P0)
**Story points** : 1
**Risque associé** : R-04

**En tant que** système,
**Je veux** limiter la taille des fichiers uploadés,
**Afin de** prévenir la saturation du stockage.

**Critères d'acceptation** :
- [ ] Limite : 100 MB par fichier
- [ ] Vérification côté client (JS) + serveur (obligatoire)
- [ ] Message d'erreur clair avec taille max
- [ ] Compteur visuel : "45 MB / 100 MB"

---

## 5. EPIC 4 : Suppression Sécurisée et Garantie d'Effacement

**Objectif** : Garantir la suppression effective des fichiers

### US-DELETE-001 : Suppression atomique après téléchargement
**Priorité** : MUST (P0)
**Story points** : 5
**Risque associé** : R-06

**En tant qu'** utilisateur,
**Je veux que** mon fichier soit supprimé immédiatement après téléchargement,
**Afin de** garantir qu'il n'existe plus sur le serveur.

**Critères d'acceptation** :
- [ ] Transaction atomique : invalidation token Redis + suppression S3 + suppression DB
- [ ] Vérification post-suppression (S3 HEAD → 404)
- [ ] Rollback si une étape échoue
- [ ] Log d'audit de suppression avec timestamp
- [ ] Tests de race conditions

**Tâches techniques** :
- [ ] Implémenter pattern Saga ou 2PC (Two-Phase Commit)
- [ ] Service de suppression avec retry logic
- [ ] Monitoring des échecs de suppression

**Tests de sécurité** :
- Télécharger fichier → vérifier suppression S3
- Simuler échec S3 → vérifier rollback
- Tester 10 downloads concurrents → 1 seul réussit, fichier supprimé

---

### US-DELETE-002 : Cleanup automatique des fichiers expirés
**Priorité** : MUST (P0)
**Story points** : 3
**Risque associé** : R-06

**En tant que** système,
**Je veux** supprimer automatiquement les fichiers expirés,
**Afin de** respecter le TTL promis.

**Critères d'acceptation** :
- [ ] Cron job toutes les heures : scan des fichiers expirés
- [ ] Suppression S3 + DB + Redis
- [ ] Logs : nombre de fichiers supprimés
- [ ] Alerte si échec de cleanup

---

### US-DELETE-003 : Documentation des limites de suppression
**Priorité** : MUST (P0)
**Story points** : 1
**Risque associé** : R-06, R-09 (RGPD)

**En tant qu'** utilisateur,
**Je veux** comprendre les limites de la suppression,
**Afin d'** avoir des attentes réalistes.

**Critères d'acceptation** :
- [ ] Page "Politique de confidentialité" avec section "Suppression des données"
- [ ] Mention explicite : backups provider, snapshots S3, logs
- [ ] Durée de rétention des backups (si applicable)
- [ ] Procédure de demande de suppression définitive

---

## 6. EPIC 5 : Protection contre les Abus (Rate Limiting, Quotas)

**Objectif** : Empêcher les attaques DoS et l'usage abusif

### US-ABUSE-001 : Rate limiting global
**Priorité** : MUST (P0)
**Story points** : 3
**Risque associé** : R-04

**En tant que** système,
**Je veux** limiter le nombre de requêtes par IP,
**Afin de** prévenir les attaques DDoS.

**Critères d'acceptation** :
- [ ] Limite : 100 requêtes/minute par IP (global)
- [ ] Limite upload : 10 fichiers/heure par IP
- [ ] Limite download : 50 tentatives/heure par IP
- [ ] Réponse HTTP 429 avec header Retry-After
- [ ] Implémentation via Redis (sliding window)

**Tâches techniques** :
- [ ] Middleware FastAPI de rate limiting
- [ ] Utiliser slowapi ou custom Redis counter

---

### US-ABUSE-002 : CAPTCHA après tentatives échouées
**Priorité** : MUST (P0)
**Story points** : 3
**Risque associé** : R-01, R-04

**En tant que** système,
**Je veux** déclencher un CAPTCHA après des tentatives d'accès suspectes,
**Afin de** bloquer les bots.

**Critères d'acceptation** :
- [ ] CAPTCHA (hCaptcha ou reCAPTCHA v3) après 3 tentatives échouées
- [ ] Intégration frontend + validation backend
- [ ] Pas de CAPTCHA pour accès normal (UX)
- [ ] Compteur reset après 1h

---

### US-ABUSE-003 : Quota de stockage par IP
**Priorité** : SHOULD (P1)
**Story points** : 3
**Risque associé** : R-04

**En tant que** système,
**Je veux** limiter le stockage total par IP,
**Afin de** prévenir la saturation.

**Critères d'acceptation** :
- [ ] Limite : 1 GB total par IP (tous fichiers actifs)
- [ ] Compteur en Redis (incrémentation/décrémentation)
- [ ] Message : "Quota dépassé, supprimez d'anciens fichiers"
- [ ] Dashboard admin : IPs avec plus haut usage

---

### US-ABUSE-004 : Blacklist automatique des IPs abusives
**Priorité** : SHOULD (P1)
**Story points** : 3
**Risque associé** : R-04

**En tant que** système,
**Je veux** blacklister automatiquement les IPs qui abusent,
**Afin de** protéger le service.

**Critères d'acceptation** :
- [ ] Blacklist si > 1000 requêtes/heure
- [ ] Blacklist si > 50 fichiers/jour
- [ ] Durée : 24h (puis déblocage automatique)
- [ ] Possibilité de whitelist manuelle (admin)

---

## 7. EPIC 6 : Journalisation et Audit (RGPD-compliant)

**Objectif** : Traçabilité des événements sans compromettre la vie privée

### US-AUDIT-001 : Logs structurés JSON
**Priorité** : MUST (P0)
**Story points** : 2
**Risque associé** : R-09

**En tant qu'** administrateur,
**Je veux** des logs structurés et faciles à analyser,
**Afin de** détecter les incidents de sécurité.

**Critères d'acceptation** :
- [ ] Format JSON avec champs : timestamp, level, event_type, user_id, ip_hash, metadata
- [ ] Horodatage UTC avec précision à la milliseconde
- [ ] Pas de données sensibles en clair (fichiers, tokens)
- [ ] Agrégation dans ELK ou solution cloud

---

### US-AUDIT-002 : Hashage des IPs utilisateurs
**Priorité** : MUST (P0)
**Story points** : 2
**Risque associé** : R-09 (RGPD)

**En tant que** système,
**Je veux** hasher les IPs avant logging,
**Afin de** minimiser les données personnelles.

**Critères d'acceptation** :
- [ ] Hachage SHA-256 avec salt quotidien
- [ ] Impossible de retrouver l'IP depuis le hash
- [ ] Salt rotatif (nouveau chaque jour)
- [ ] Logs conservent hash pour corrélation dans la journée

---

### US-AUDIT-003 : Journalisation des événements critiques
**Priorité** : MUST (P0)
**Story points** : 2
**Risque associé** : Tous

**En tant qu'** auditeur,
**Je veux** avoir une trace de tous les événements de sécurité,
**Afin de** pouvoir investiguer les incidents.

**Critères d'acceptation** :
- [ ] Événements : upload, download, suppression, erreurs 4xx/5xx, abus
- [ ] Logs immuables (append-only, pas de modification)
- [ ] Rétention : 1 an minimum
- [ ] Accès restreint aux logs (RBAC)

---

## 8. EPIC 7 : DevSecOps et Pipeline CI/CD

**Objectif** : Intégrer la sécurité dans le cycle de développement

### US-DEVSEC-001 : SAST automatisé (Bandit, Semgrep)
**Priorité** : MUST (P0)
**Story points** : 3
**Risque associé** : R-05, R-08

**En tant que** développeur,
**Je veux** que le code soit scanné automatiquement,
**Afin de** détecter les vulnérabilités avant production.

**Critères d'acceptation** :
- [ ] Scan Bandit (Python) + Semgrep à chaque commit
- [ ] Scan ESLint Security Plugin (React) à chaque commit
- [ ] Blocage du merge si vulnérabilités critiques
- [ ] Rapport intégré dans PR GitHub/GitLab
- [ ] Baseline : pas de régression sur les vulnérabilités

---

### US-DEVSEC-002 : Dependency scanning (SCA)
**Priorité** : MUST (P0)
**Story points** : 2
**Risque associé** : R-08

**En tant que** développeur,
**Je veux** être alerté des dépendances vulnérables,
**Afin de** les patcher rapidement.

**Critères d'acceptation** :
- [ ] Scan Safety (Python) + npm audit (Node) à chaque commit
- [ ] Blocage si vulnérabilités critiques (CVSS ≥ 9.0)
- [ ] Rapport avec CVE et patch recommandé
- [ ] Mise à jour automatique des dépendances (Dependabot)

---

### US-DEVSEC-003 : Secret scanning
**Priorité** : MUST (P0)
**Story points** : 2
**Risque associé** : R-02

**En tant que** développeur,
**Je veux** être alerté si je commite un secret,
**Afin de** prévenir les fuites.

**Critères d'acceptation** :
- [ ] Scan TruffleHog ou detect-secrets dans CI/CD
- [ ] Pre-commit hook local (optionnel mais recommandé)
- [ ] Blocage du commit si secret détecté
- [ ] Patterns : API keys, mots de passe, tokens JWT, clés privées

---

### US-DEVSEC-004 : Container scanning (Trivy)
**Priorité** : MUST (P0)
**Story points** : 2
**Risque associé** : R-08

**En tant que** DevOps,
**Je veux** scanner les images Docker,
**Afin de** détecter les CVE dans les dépendances système.

**Critères d'acceptation** :
- [ ] Scan Trivy avant push du container
- [ ] Blocage si vulnerabilités critiques ou élevées
- [ ] Rapport avec recommandations de patch
- [ ] Images basées sur Alpine ou Distroless (minimales)

---

### US-DEVSEC-005 : DAST en pré-production (OWASP ZAP)
**Priorité** : SHOULD (P1)
**Story points** : 5
**Risque associé** : R-10, R-05

**En tant que** QA sécurité,
**Je veux** tester l'application en conditions réelles,
**Afin de** détecter les vulnérabilités runtime.

**Critères d'acceptation** :
- [ ] Scan OWASP ZAP automatisé en environnement staging
- [ ] Tests : injection SQL, XSS, CSRF, SSRF, etc.
- [ ] Rapport avec PoC (Proof of Concept)
- [ ] Exécution hebdomadaire + avant chaque release majeure

---

## 9. EPIC 8 : Conformité RGPD

**Objectif** : Respecter les droits des utilisateurs et la réglementation

### US-RGPD-001 : Politique de confidentialité claire
**Priorité** : MUST (P0)
**Story points** : 2
**Risque associé** : R-09

**En tant qu'** utilisateur,
**Je veux** comprendre comment mes données sont traitées,
**Afin de** donner mon consentement éclairé.

**Critères d'acceptation** :
- [ ] Page dédiée "Politique de confidentialité"
- [ ] Sections : données collectées, finalité, durée, droits, contact DPO
- [ ] Langage clair (pas de jargon juridique)
- [ ] Lien visible dans le footer

---

### US-RGPD-002 : Minimisation des données collectées
**Priorité** : MUST (P0)
**Story points** : 1
**Risque associé** : R-09

**En tant que** système,
**Je veux** ne collecter que les données strictement nécessaires,
**Afin de** respecter le principe de minimisation.

**Critères d'acceptation** :
- [ ] Pas de tracking (Google Analytics, etc.)
- [ ] Pas de cookies non essentiels
- [ ] Métadonnées minimales : taille fichier, date upload, hash IP
- [ ] Pas de nom d'utilisateur, email (sauf si authentification)

---

### US-RGPD-003 : DPIA (Data Protection Impact Assessment)
**Priorité** : MUST (P0)
**Story points** : 3
**Risque associé** : R-09

**En tant que** DPO (Data Protection Officer),
**Je veux** une analyse d'impact documentée,
**Afin de** démontrer la conformité RGPD.

**Critères d'acceptation** :
- [ ] Document DPIA complété (template CNIL)
- [ ] Identification des traitements à risque
- [ ] Mesures de protection mises en place
- [ ] Validation par responsable sécurité

---

### US-RGPD-004 : Procédure de suppression des données
**Priorité** : MUST (P0)
**Story points** : 2
**Risque associé** : R-09

**En tant qu'** utilisateur,
**Je veux** pouvoir demander la suppression de mes données,
**Afin de** exercer mon droit à l'oubli.

**Critères d'acceptation** :
- [ ] Formulaire de contact "Demande de suppression"
- [ ] Traitement sous 72h
- [ ] Confirmation par email
- [ ] Suppression effective : fichiers + logs + métadonnées

---

## 10. Sprints Planning (Exemple)

### Sprint 1 (2 semaines) : Fondations sécurisées
**Objectif** : MVP fonctionnel avec sécurité de base

| US | Titre | Points | Statut |
|----|-------|--------|--------|
| US-CRYPTO-001 | Chiffrement AES-256 | 5 | 🔵 To Do |
| US-CRYPTO-002 | TLS 1.3 + HSTS | 3 | 🔵 To Do |
| US-TOKEN-001 | Tokens sécurisés | 3 | 🔵 To Do |
| US-TOKEN-002 | Usage unique | 5 | 🔵 To Do |
| US-TOKEN-003 | Expiration TTL | 2 | 🔵 To Do |
| US-MALWARE-002 | Validation MIME | 2 | 🔵 To Do |
| US-MALWARE-003 | Limite taille | 1 | 🔵 To Do |
| **TOTAL** | | **21 pts** | |

---

### Sprint 2 (2 semaines) : Protection avancée
**Objectif** : Anti-abuse + malware protection

| US | Titre | Points | Statut |
|----|-------|--------|--------|
| US-MALWARE-001 | Scan antivirus | 5 | 🔵 To Do |
| US-TOKEN-004 | Rate limiting tokens | 3 | 🔵 To Do |
| US-ABUSE-001 | Rate limiting global | 3 | 🔵 To Do |
| US-ABUSE-002 | CAPTCHA | 3 | 🔵 To Do |
| US-DELETE-001 | Suppression atomique | 5 | 🔵 To Do |
| US-DELETE-002 | Cleanup auto | 3 | 🔵 To Do |
| **TOTAL** | | **22 pts** | |

---

### Sprint 3 (2 semaines) : DevSecOps + Conformité
**Objectif** : Pipeline sécurisé + RGPD

| US | Titre | Points | Statut |
|----|-------|--------|--------|
| US-DEVSEC-001 | SAST | 3 | 🔵 To Do |
| US-DEVSEC-002 | Dependency scan | 2 | 🔵 To Do |
| US-DEVSEC-003 | Secret scan | 2 | 🔵 To Do |
| US-DEVSEC-004 | Container scan | 2 | 🔵 To Do |
| US-AUDIT-001 | Logs JSON | 2 | 🔵 To Do |
| US-AUDIT-002 | Hash IPs | 2 | 🔵 To Do |
| US-AUDIT-003 | Logs événements | 2 | 🔵 To Do |
| US-RGPD-001 | Politique confidentialité | 2 | 🔵 To Do |
| US-RGPD-003 | DPIA | 3 | 🔵 To Do |
| **TOTAL** | | **20 pts** | |

---

## 11. Backlog Complet Priorisé

| Priorité | Epic | US ID | Titre | Points | Sprint |
|----------|------|-------|-------|--------|--------|
| **MUST** | Crypto | US-CRYPTO-001 | Chiffrement AES-256 | 5 | 1 |
| **MUST** | Crypto | US-CRYPTO-002 | TLS 1.3 | 3 | 1 |
| **MUST** | Token | US-TOKEN-001 | Tokens sécurisés | 3 | 1 |
| **MUST** | Token | US-TOKEN-002 | Usage unique | 5 | 1 |
| **MUST** | Token | US-TOKEN-003 | Expiration TTL | 2 | 1 |
| **MUST** | Token | US-TOKEN-004 | Rate limit tokens | 3 | 2 |
| **MUST** | Malware | US-MALWARE-001 | Scan antivirus | 5 | 2 |
| **MUST** | Malware | US-MALWARE-002 | Validation MIME | 2 | 1 |
| **MUST** | Malware | US-MALWARE-003 | Limite taille | 1 | 1 |
| **MUST** | Delete | US-DELETE-001 | Suppression atomique | 5 | 2 |
| **MUST** | Delete | US-DELETE-002 | Cleanup auto | 3 | 2 |
| **MUST** | Delete | US-DELETE-003 | Doc limites | 1 | 2 |
| **MUST** | Abuse | US-ABUSE-001 | Rate limit global | 3 | 2 |
| **MUST** | Abuse | US-ABUSE-002 | CAPTCHA | 3 | 2 |
| **MUST** | Audit | US-AUDIT-001 | Logs JSON | 2 | 3 |
| **MUST** | Audit | US-AUDIT-002 | Hash IPs | 2 | 3 |
| **MUST** | Audit | US-AUDIT-003 | Logs événements | 2 | 3 |
| **MUST** | DevSecOps | US-DEVSEC-001 | SAST | 3 | 3 |
| **MUST** | DevSecOps | US-DEVSEC-002 | Dependency scan | 2 | 3 |
| **MUST** | DevSecOps | US-DEVSEC-003 | Secret scan | 2 | 3 |
| **MUST** | DevSecOps | US-DEVSEC-004 | Container scan | 2 | 3 |
| **MUST** | RGPD | US-RGPD-001 | Politique confidentialité | 2 | 3 |
| **MUST** | RGPD | US-RGPD-002 | Minimisation données | 1 | 1 |
| **MUST** | RGPD | US-RGPD-003 | DPIA | 3 | 3 |
| **MUST** | RGPD | US-RGPD-004 | Proc. suppression | 2 | 3 |
| | | **TOTAL MUST** | | **66 pts** | |
| **SHOULD** | Crypto | US-CRYPTO-003 | Rotation clés | 5 | 4 |
| **SHOULD** | Abuse | US-ABUSE-003 | Quota stockage | 3 | 4 |
| **SHOULD** | Abuse | US-ABUSE-004 | Blacklist auto | 3 | 4 |
| **SHOULD** | DevSecOps | US-DEVSEC-005 | DAST (ZAP) | 5 | 4 |
| **COULD** | Crypto | US-CRYPTO-004 | E2EE client | 8 | Backlog |

---

## 12. Métriques de Suivi

### Velocity par sprint
- **Sprint 1** : 21 pts
- **Sprint 2** : 22 pts
- **Sprint 3** : 20 pts
- **Moyenne** : ~21 pts/sprint

### Burndown chart
À suivre dans outil de gestion (Jira, GitHub Projects, etc.)

### Tests de sécurité
- **Coverage cible** : > 80% pour code critique (crypto, auth, upload)
- **Vulnérabilités max** : 0 critiques, 0 élevées en production

---

**📋 Document vivant - Mise à jour à chaque sprint planning**
