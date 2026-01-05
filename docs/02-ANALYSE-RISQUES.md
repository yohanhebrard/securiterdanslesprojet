# ⚠️ Analyse de Risques - SecureShare

**Document**: Analyse de risques de sécurité (méthode EBIOS adaptée)
**Version**: 1.0
**Date**: 2025-12-05
**Statut**: ✅ Approuvé

---

## 1. Contexte et Périmètre

### 1.1 Objectif de l'analyse

Identifier, évaluer et traiter les risques de sécurité liés à la plateforme **SecureShare**, un service de partage de fichiers éphémères et sécurisés.

### 1.2 Méthodologie

Approche hybride inspirée de :
- **EBIOS Risk Manager** (ANSSI)
- **ISO 27005** - Gestion des risques de sécurité de l'information
- **OWASP Risk Rating Methodology**

### 1.3 Périmètre

- Application web (frontend + backend API)
- Infrastructure (stockage, bases de données, containers)
- Données utilisateurs (fichiers, métadonnées, logs)
- Pipeline CI/CD DevSecOps

### 1.4 Actifs critiques à protéger

| Actif | Type | Valeur métier | Impact si compromis |
|-------|------|---------------|---------------------|
| **Fichiers utilisateurs** | Données | CRITIQUE | Perte de confidentialité, violation RGPD |
| **Clés de chiffrement** | Secrets | CRITIQUE | Compromission totale du système |
| **Base de données métadonnées** | Données | ÉLEVÉ | Fuite d'informations personnelles |
| **API Backend** | Service | ÉLEVÉ | Indisponibilité, compromission |
| **Pipeline CI/CD** | Infrastructure | MOYEN | Supply chain attack |

---

## 2. Échelle d'Évaluation

### 2.1 Gravité (Impact)

| Niveau | Valeur | Critères |
|--------|--------|----------|
| **CRITIQUE** | 5 | Compromission totale, violation RGPD majeure, arrêt de service > 24h |
| **ÉLEVÉ** | 4 | Perte de confidentialité significative, indisponibilité partielle |
| **MOYEN** | 3 | Fuite de métadonnées, dégradation de service |
| **FAIBLE** | 2 | Impact limité, pas de données sensibles exposées |
| **NÉGLIGEABLE** | 1 | Impact mineur, facilement réversible |

### 2.2 Vraisemblance (Probabilité)

| Niveau | Valeur | Critères |
|--------|--------|----------|
| **TRÈS ÉLEVÉE** | 5 | Attaque courante, exploitation facile, surface d'attaque large |
| **ÉLEVÉE** | 4 | Attaque connue, outils publics disponibles |
| **MOYENNE** | 3 | Nécessite compétences moyennes, opportunité régulière |
| **FAIBLE** | 2 | Nécessite compétences avancées, opportunité rare |
| **TRÈS FAIBLE** | 1 | Attaque très complexe, conditions très spécifiques |

### 2.3 Matrice de criticité

| Impact \ Probabilité | 1 (Très faible) | 2 (Faible) | 3 (Moyenne) | 4 (Élevée) | 5 (Très élevée) |
|---------------------|----------------|------------|-------------|-----------|----------------|
| **5 (CRITIQUE)** | MOYEN (5) | ÉLEVÉ (10) | ÉLEVÉ (15) | CRITIQUE (20) | CRITIQUE (25) |
| **4 (ÉLEVÉ)** | FAIBLE (4) | MOYEN (8) | ÉLEVÉ (12) | ÉLEVÉ (16) | CRITIQUE (20) |
| **3 (MOYEN)** | FAIBLE (3) | FAIBLE (6) | MOYEN (9) | ÉLEVÉ (12) | ÉLEVÉ (15) |
| **2 (FAIBLE)** | FAIBLE (2) | FAIBLE (4) | FAIBLE (6) | MOYEN (8) | MOYEN (10) |
| **1 (NÉGLIGEABLE)** | FAIBLE (1) | FAIBLE (2) | FAIBLE (3) | FAIBLE (4) | MOYEN (5) |

**Légende** :
- **CRITIQUE** (≥ 15) : Action immédiate requise, blocage déploiement
- **ÉLEVÉ** (10-14) : Traitement prioritaire < 30 jours
- **MOYEN** (5-9) : Traitement planifié < 90 jours
- **FAIBLE** (1-4) : Surveillance, amélioration continue

---

## 3. Identification des Menaces

### 3.1 Menaces par catégorie

#### 3.1.1 Menaces sur la confidentialité

| ID | Menace | Source | Vecteur d'attaque |
|----|--------|--------|------------------|
| **T-CONF-01** | Accès non autorisé aux fichiers stockés | Attaquant externe | Brute force des tokens |
| **T-CONF-02** | Interception des fichiers en transit | Attaquant MitM | Absence/faiblesse TLS |
| **T-CONF-03** | Exposition des clés de chiffrement | Attaquant interne/externe | Mauvaise gestion des secrets |
| **T-CONF-04** | Accès aux fichiers après suppression | Attaquant/enquêteur | Suppression non effective |
| **T-CONF-05** | Fuite de métadonnées utilisateurs | Attaquant | Logs non sécurisés, IDOR |

#### 3.1.2 Menaces sur l'intégrité

| ID | Menace | Source | Vecteur d'attaque |
|----|--------|--------|------------------|
| **T-INT-01** | Modification malveillante de fichiers | Attaquant | Injection pendant upload/download |
| **T-INT-02** | Upload de malware/ransomware | Utilisateur malveillant | Absence de scan antivirus |
| **T-INT-03** | Injection SQL/NoSQL | Attaquant | Input non validée |
| **T-INT-04** | Modification des métadonnées | Attaquant | Absence de contrôle d'intégrité |
| **T-INT-05** | Supply chain attack (dépendances) | Attaquant externe | Packages compromis |

#### 3.1.3 Menaces sur la disponibilité

| ID | Menace | Source | Vecteur d'attaque |
|----|--------|--------|------------------|
| **T-DISP-01** | Déni de service (DoS/DDoS) | Attaquant | Flood de requêtes |
| **T-DISP-02** | Épuisement du stockage | Utilisateur malveillant | Upload massif de fichiers |
| **T-DISP-03** | Crash applicatif | Bug/attaquant | Exploitation de vulnérabilités |
| **T-DISP-04** | Compromission de l'infrastructure | Attaquant APT | Exploitation de 0-day |
| **T-DISP-05** | Perte de données (backup) | Catastrophe/erreur | Absence de backup ou corruption |

#### 3.1.4 Menaces juridiques et conformité

| ID | Menace | Source | Vecteur d'attaque |
|----|--------|--------|------------------|
| **T-LEG-01** | Non-conformité RGPD | Audit/plainte | Mauvaise gestion des données personnelles |
| **T-LEG-02** | Utilisation pour activités illégales | Utilisateur malveillant | Partage de contenu illicite |
| **T-LEG-03** | Réquisition judiciaire impossible | Autorités | Absence de logs/traçabilité |
| **T-LEG-04** | Responsabilité du contenu partagé | Victime | Absence de modération |

---

## 4. Analyse Détaillée des Risques

### 4.1 Risques CRITIQUES

#### Risque R-01 : Compromission des fichiers par brute force des tokens

**Menace** : T-CONF-01
**Actif** : Fichiers utilisateurs

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| **Impact** | 5 (CRITIQUE) | Violation RGPD, perte totale de confidentialité |
| **Probabilité** | 4 (ÉLEVÉE) | Tokens courts/prévisibles, outils de brute force disponibles |
| **Risque brut** | **20 (CRITIQUE)** | - |

**Scénario d'attaque** :
1. Attaquant collecte plusieurs tokens valides
2. Analyse du format/longueur des tokens
3. Brute force avec dictionnaire ou force brute pure
4. Accès aux fichiers confidentiels

**Mesures de sécurité existantes** : Aucune (MVP)

**Mesures d'atténuation proposées** :
- **M-01.1** : Tokens de 32+ caractères (256 bits aléatoires encodés en base64url)
- **M-01.2** : Hachage SHA-256 des tokens en base de données (stockage sécurisé)
- **M-01.3** : Rate limiting strict : 10 tentatives/heure par IP
- **M-01.4** : CAPTCHA après 3 tentatives échouées
- **M-01.5** : Expiration courte (TTL 24-48h max)
- **M-01.6** : Monitoring des tentatives d'accès en masse

**Risque résiduel** : 6 (MOYEN) - Probabilité réduite à 2 (FAIBLE)

---

#### Risque R-02 : Exposition des clés de chiffrement

**Menace** : T-CONF-03
**Actif** : Clés de chiffrement

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| **Impact** | 5 (CRITIQUE) | Déchiffrement de tous les fichiers historiques |
| **Probabilité** | 3 (MOYENNE) | Erreur de configuration, commit accidentel |
| **Risque brut** | **15 (CRITIQUE)** | - |

**Scénario d'attaque** :
1. Clés stockées en clair dans .env ou code source
2. Commit accidentel sur repository public
3. Scan automatique par bots (GitGuardian, etc.)
4. Attaquant récupère les clés et accède au stockage

**Mesures d'atténuation proposées** :
- **M-02.1** : HashiCorp Vault ou AWS KMS pour gestion des clés
- **M-02.2** : Rotation automatique des clés tous les 90 jours
- **M-02.3** : Secret scanning dans CI/CD (TruffleHog, GitGuardian)
- **M-02.4** : `.gitignore` strict + pre-commit hooks
- **M-02.5** : Clés différentes par environnement (dev/staging/prod)
- **M-02.6** : Audit des accès aux secrets (Vault logs)

**Risque résiduel** : 5 (MOYEN) - Probabilité réduite à 1 (TRÈS FAIBLE)

---

#### Risque R-03 : Upload et distribution de malware

**Menace** : T-INT-02
**Actif** : Réputation, utilisateurs, infrastructure

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| **Impact** | 4 (ÉLEVÉ) | Infection des téléchargeurs, blacklist, responsabilité légale |
| **Probabilité** | 4 (ÉLEVÉE) | Facile à exploiter sans scan antivirus |
| **Risque brut** | **16 (ÉLEVÉ)** | - |

**Scénario d'attaque** :
1. Attaquant upload un ransomware déguisé en document PDF
2. Victime télécharge et exécute le fichier
3. Infection de la machine, propagation réseau
4. Plainte contre la plateforme pour hébergement de malware

**Mesures d'atténuation proposées** :
- **M-03.1** : Scan antivirus obligatoire (ClamAV) avant mise à disposition
- **M-03.2** : Quarantaine automatique des fichiers suspects
- **M-03.3** : Validation stricte des MIME types (whitelist)
- **M-03.4** : Sandboxing pour analyse comportementale (optionnel)
- **M-03.5** : Alerte automatique si détection + blocage du lien
- **M-03.6** : Disclaimer visible : "Fichier non vérifié par l'expéditeur"

**Risque résiduel** : 6 (FAIBLE) - Probabilité réduite à 2 (FAIBLE)

---

#### Risque R-04 : Déni de service par upload massif

**Menace** : T-DISP-02
**Actif** : Stockage, disponibilité du service

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| **Impact** | 4 (ÉLEVÉ) | Saturation du stockage, coût financier élevé, indisponibilité |
| **Probabilité** | 4 (ÉLEVÉE) | Pas de limite de quota par défaut |
| **Risque brut** | **16 (ÉLEVÉ)** | - |

**Scénario d'attaque** :
1. Attaquant upload 10 000 fichiers de 100 MB en parallèle
2. Saturation du stockage S3/MinIO (1 TB en quelques heures)
3. Dépassement de budget, crash du service
4. Indisponibilité pour les utilisateurs légitimes

**Mesures d'atténuation proposées** :
- **M-04.1** : Limite stricte par fichier (100 MB max)
- **M-04.2** : Quota par IP : 10 fichiers/heure, 1 GB total
- **M-04.3** : Rate limiting upload : 10 req/heure par IP
- **M-04.4** : CAPTCHA obligatoire après 3 uploads
- **M-04.5** : Monitoring en temps réel du stockage avec alertes
- **M-04.6** : Auto-scaling avec limite de coût (cloud provider)

**Risque résiduel** : 6 (FAIBLE) - Probabilité réduite à 2 (FAIBLE)

---

### 4.2 Risques ÉLEVÉS

#### Risque R-05 : Injection SQL/NoSQL

**Menace** : T-INT-03
**Actif** : Base de données, intégrité des données

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| **Impact** | 4 (ÉLEVÉ) | Accès aux métadonnées, modification/suppression de données |
| **Probabilité** | 2 (FAIBLE) | ORM utilisé (SQLAlchemy), mais risque si requêtes brutes |
| **Risque brut** | **8 (MOYEN)** | - |

**Mesures d'atténuation proposées** :
- **M-05.1** : Utilisation exclusive de l'ORM (pas de requêtes SQL brutes)
- **M-05.2** : Validation stricte de toutes les entrées (Pydantic schemas)
- **M-05.3** : Principe du moindre privilège (compte DB read-only pour API)
- **M-05.4** : WAF avec règles anti-injection (ModSecurity)
- **M-05.5** : Tests SAST automatisés (Bandit, Semgrep)

**Risque résiduel** : 4 (FAIBLE)

---

#### Risque R-06 : Fichiers non supprimés après téléchargement

**Menace** : T-CONF-04
**Actif** : Fichiers utilisateurs, conformité RGPD

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| **Impact** | 4 (ÉLEVÉ) | Violation promesse de suppression, non-conformité RGPD |
| **Probabilité** | 3 (MOYENNE) | Erreur de logique, snapshots non gérés, backups |
| **Risque brut** | **12 (ÉLEVÉ)** | - |

**Scénario d'attaque/incident** :
1. Utilisateur partage document sensible avec "suppression après lecture"
2. Bug applicatif ou snapshot S3 conserve le fichier
3. Fichier accessible indéfiniment malgré la promesse de suppression
4. Plainte RGPD, perte de confiance

**Mesures d'atténuation proposées** :
- **M-06.1** : Transaction atomique (Redis + DB + S3) pour garantir la suppression
- **M-06.2** : Tests automatisés de suppression (end-to-end)
- **M-06.3** : Vérification post-suppression (S3 HEAD request)
- **M-06.4** : Désactivation du versioning S3 ou lifecycle automatique
- **M-06.5** : Documentation claire des limites (backups provider)
- **M-06.6** : Monitoring des fichiers "fantômes" (S3 vs DB reconciliation)

**Risque résiduel** : 6 (FAIBLE)

---

#### Risque R-07 : Interception Man-in-the-Middle (MitM)

**Menace** : T-CONF-02
**Actif** : Fichiers en transit, tokens

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| **Impact** | 4 (ÉLEVÉ) | Interception des fichiers et tokens |
| **Probabilité** | 2 (FAIBLE) | Nécessite position réseau privilégiée |
| **Risque brut** | **8 (MOYEN)** | - |

**Mesures d'atténuation proposées** :
- **M-07.1** : TLS 1.3 obligatoire (désactivation TLS < 1.2)
- **M-07.2** : HSTS avec preload (max-age=31536000)
- **M-07.3** : Cipher suites modernes uniquement (ECDHE, AEAD)
- **M-07.4** : Certificate pinning pour API mobile (si applicable)
- **M-07.5** : Monitoring des erreurs TLS (alertes sur downgrade)

**Risque résiduel** : 4 (FAIBLE)

---

### 4.3 Risques MOYENS

#### Risque R-08 : Supply Chain Attack (dépendances compromises)

**Menace** : T-INT-05
**Actif** : Code source, infrastructure, utilisateurs

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| **Impact** | 5 (CRITIQUE) | Backdoor dans l'application, accès total |
| **Probabilité** | 1 (TRÈS FAIBLE) | Rare mais possible (ex: event-stream npm) |
| **Risque brut** | **5 (MOYEN)** | - |

**Mesures d'atténuation proposées** :
- **M-08.1** : Dependency scanning automatisé (Snyk, Safety, npm audit)
- **M-08.2** : Lockfiles stricts (poetry.lock, package-lock.json)
- **M-08.3** : Vérification des signatures de packages
- **M-08.4** : Revue manuelle des dépendances critiques
- **M-08.5** : Utilisation de miroirs internes (artifactory, nexus)
- **M-08.6** : Blocage des mises à jour automatiques en production

**Risque résiduel** : 2 (FAIBLE)

---

#### Risque R-09 : Non-conformité RGPD

**Menace** : T-LEG-01
**Actif** : Conformité légale, réputation

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| **Impact** | 4 (ÉLEVÉ) | Amendes CNIL (jusqu'à 4% CA), sanctions |
| **Probabilité** | 2 (FAIBLE) | Mesures de conformité mises en place |
| **Risque brut** | **8 (MOYEN)** | - |

**Mesures d'atténuation proposées** :
- **M-09.1** : DPIA (Data Protection Impact Assessment) documentée
- **M-09.2** : Minimisation des données (pas de collecte excessive)
- **M-09.3** : Durée de conservation limitée (TTL 48h max)
- **M-09.4** : Hashage des IPs dans les logs
- **M-09.5** : Politique de confidentialité claire et accessible
- **M-09.6** : Procédure de traitement des demandes d'accès/suppression

**Risque résiduel** : 4 (FAIBLE)

---

#### Risque R-10 : XSS (Cross-Site Scripting)

**Menace** : Injection de scripts malveillants
**Actif** : Utilisateurs, sessions

| Critère | Évaluation | Justification |
|---------|------------|---------------|
| **Impact** | 3 (MOYEN) | Vol de session, redirection malveillante |
| **Probabilité** | 2 (FAIBLE) | React échappe par défaut, mais risque si dangerouslySetInnerHTML |
| **Risque brut** | **6 (FAIBLE)** | - |

**Mesures d'atténuation proposées** :
- **M-10.1** : Content Security Policy (CSP) stricte
- **M-10.2** : Validation et sanitization de toutes les entrées
- **M-10.3** : Pas d'utilisation de dangerouslySetInnerHTML
- **M-10.4** : Headers de sécurité (X-XSS-Protection, X-Content-Type-Options)
- **M-10.5** : Tests DAST automatisés (OWASP ZAP)

**Risque résiduel** : 2 (FAIBLE)

---

## 5. Plan de Traitement des Risques

### 5.1 Synthèse des risques

| ID | Risque | Risque brut | Mesures | Risque résiduel | Priorité |
|----|--------|-------------|---------|----------------|----------|
| **R-01** | Brute force tokens | 20 (CRITIQUE) | M-01.1 à M-01.6 | 6 (MOYEN) | P0 |
| **R-02** | Exposition clés chiffrement | 15 (CRITIQUE) | M-02.1 à M-02.6 | 5 (MOYEN) | P0 |
| **R-03** | Upload malware | 16 (ÉLEVÉ) | M-03.1 à M-03.6 | 6 (FAIBLE) | P0 |
| **R-04** | DoS upload massif | 16 (ÉLEVÉ) | M-04.1 à M-04.6 | 6 (FAIBLE) | P0 |
| **R-05** | Injection SQL | 8 (MOYEN) | M-05.1 à M-05.5 | 4 (FAIBLE) | P1 |
| **R-06** | Suppression non effective | 12 (ÉLEVÉ) | M-06.1 à M-06.6 | 6 (FAIBLE) | P1 |
| **R-07** | MitM | 8 (MOYEN) | M-07.1 à M-07.5 | 4 (FAIBLE) | P1 |
| **R-08** | Supply chain | 5 (MOYEN) | M-08.1 à M-08.6 | 2 (FAIBLE) | P2 |
| **R-09** | Non-conformité RGPD | 8 (MOYEN) | M-09.1 à M-09.6 | 4 (FAIBLE) | P1 |
| **R-10** | XSS | 6 (FAIBLE) | M-10.1 à M-10.5 | 2 (FAIBLE) | P2 |

**Légende priorités** :
- **P0** : Blocant pour mise en production (≥ 15 risque brut)
- **P1** : Requis avant beta publique (8-14 risque brut)
- **P2** : Amélioration continue (< 8 risque brut)

### 5.2 Roadmap de traitement

#### Phase 1 : MVP Sécurisé (Sprint 1-2)
- ✅ R-01 : Tokens sécurisés + rate limiting
- ✅ R-02 : Intégration HashiCorp Vault
- ✅ R-03 : Scan antivirus ClamAV
- ✅ R-04 : Quotas et limites upload

#### Phase 2 : Hardening (Sprint 3)
- ✅ R-05 : Validation stricte + WAF
- ✅ R-06 : Tests de suppression garantie
- ✅ R-07 : Configuration TLS 1.3 + HSTS

#### Phase 3 : Conformité (Sprint 4)
- ✅ R-09 : DPIA + politique de confidentialité
- ✅ R-08 : Pipeline dependency scanning
- ✅ R-10 : CSP + headers de sécurité

---

## 6. Risques Résiduels Acceptés

### 6.1 Limitations techniques documentées

| Risque résiduel | Justification | Mesure compensatoire |
|----------------|---------------|---------------------|
| **Backups provider** | Snapshots S3/DB peuvent conserver des données | Documentation claire dans politique de confidentialité |
| **E2EE non implémenté (MVP)** | Complexité UX trop élevée pour v1 | Chiffrement serveur AES-256-GCM + KMS |
| **Sandboxing malware basique** | Analyse comportementale coûteuse | Scan antivirus signature + validation MIME stricte |

---

## 7. Indicateurs de Suivi (KRIs)

| KRI | Seuil d'alerte | Fréquence | Action si dépassé |
|-----|---------------|-----------|-------------------|
| Tentatives de brute force | > 100/jour | Temps réel | Blacklist IP automatique |
| Détections antivirus | > 0 fichiers distribués | Temps réel | Incident majeur + investigation |
| Erreurs TLS (downgrade) | > 0.1% requêtes | Journalier | Audit configuration |
| Fichiers non supprimés | > 0.1% fichiers | Quotidien | Investigation + correctif urgent |
| Vulnérabilités critiques (deps) | > 0 critiques | À chaque scan | Blocage déploiement |

---

## 8. Plan de Réponse aux Incidents

### 8.1 Classification des incidents

| Niveau | Critères | Temps de réponse | Responsable |
|--------|----------|------------------|-------------|
| **P0 - CRITIQUE** | Fuite de données, compromission totale | < 1h | Équipe complète + direction |
| **P1 - MAJEUR** | Indisponibilité > 1h, vulnérabilité exploitée | < 4h | Équipe technique + chef projet |
| **P2 - MINEUR** | Dégradation de service, anomalie sécurité | < 24h | Équipe technique |

### 8.2 Procédure de réponse (P0/P1)

1. **Détection** : Alertes automatiques (monitoring, WAF, IDS)
2. **Confinement** : Isolation du composant compromis
3. **Investigation** : Analyse des logs, forensics
4. **Éradication** : Correction de la faille, patch
5. **Récupération** : Restauration du service
6. **Post-mortem** : Rapport d'incident + mesures préventives

---

## 9. Validation et Approbation

### 9.1 Signatures

| Rôle | Nom | Signature | Date |
|------|-----|-----------|------|
| **Responsable sécurité** | [Nom] | ___________ | 2025-12-05 |
| **Chef de projet** | [Nom] | ___________ | 2025-12-05 |
| **Sponsor projet** | [Nom] | ___________ | 2025-12-05 |

### 9.2 Revue périodique

Ce document doit être revu :
- ✅ À chaque évolution majeure de l'application
- ✅ Après chaque incident de sécurité
- ✅ Minimum 1 fois par trimestre
- ✅ Avant mise en production

---

## 10. Annexes

### Annexe A : Cartographie des menaces STRIDE

| Menace | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Elevation |
|--------|----------|-----------|-------------|----------------|-----|-----------|
| **Frontend** | - | XSS | - | Logs client | Client crash | - |
| **API** | Token forgery | Injection SQL | Pas de logs | IDOR | Rate limit | Bypass authz |
| **Stockage** | - | File corruption | - | Bucket public | Quota | ACL bypass |
| **DB** | - | Injection | - | Dump | Resource exhaustion | Privilege escalation |

### Annexe B : Références

- **OWASP Risk Rating Methodology** : https://owasp.org/www-community/OWASP_Risk_Rating_Methodology
- **EBIOS Risk Manager (ANSSI)** : https://www.ssi.gouv.fr/guide/ebios-risk-manager-the-method/
- **ISO/IEC 27005:2018** : Gestion des risques de sécurité de l'information

---

**⚠️ Document confidentiel - Diffusion restreinte**
