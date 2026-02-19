# 📊 KPIs & KRIs - SecureShare

**Document**: Indicateurs de Performance et de Risque de Sécurité
**Version**: 1.0
**Date**: 2025-12-05
**Statut**: ✅ Actif

---

## 1. Introduction

### 1.1 Objectif

Ce document définit les **KPIs** (Key Performance Indicators) et **KRIs** (Key Risk Indicators) utilisés pour mesurer l'efficacité des mesures de sécurité de la plateforme SecureShare.

### 1.2 Différence KPI vs KRI

- **KPI (Performance)** : Mesure le bon fonctionnement des contrôles de sécurité
- **KRI (Risque)** : Détecte les signaux d'alarme indiquant un risque accru

---

## 2. KPIs Sécurité (Performance)

### 2.1 Disponibilité et Fiabilité

#### KPI-01 : Uptime du service
**Définition** : Pourcentage de temps où le service est disponible

- **Formule** : `(Temps total - Temps indisponibilité) / Temps total × 100`
- **Cible** : ≥ 99.5% (maximum 3h 39min d'indisponibilité/mois)
- **Fréquence** : Mesure continue, rapport mensuel
- **Source** : Monitoring (Prometheus/Grafana)
- **Responsable** : DevOps

**Seuils d'alerte** :
- 🟢 Vert : ≥ 99.5%
- 🟡 Jaune : 99.0-99.4% → Investigation
- 🔴 Rouge : < 99.0% → Incident majeur

---

#### KPI-02 : Taux de succès des uploads
**Définition** : Pourcentage d'uploads aboutissant avec succès (chiffrement + scan + stockage)

- **Formule** : `Uploads réussis / Tentatives totales × 100`
- **Cible** : ≥ 99%
- **Fréquence** : Temps réel, rapport quotidien
- **Source** : Logs applicatifs
- **Responsable** : Équipe backend

**Seuils** :
- 🟢 ≥ 99%
- 🟡 95-98% → Investigation (problème scan AV, chiffrement?)
- 🔴 < 95% → Incident

---

#### KPI-03 : Taux de suppression après téléchargement
**Définition** : Pourcentage de fichiers supprimés immédiatement après download

- **Formule** : `Fichiers supprimés après download / Downloads totaux × 100`
- **Cible** : 100% (aucun écart toléré)
- **Fréquence** : Temps réel, rapport quotidien
- **Source** : Logs de suppression + vérification S3
- **Responsable** : Équipe backend

**Seuils** :
- 🟢 100%
- 🟡 99.9-99.99% → Investigation urgente
- 🔴 < 99.9% → Incident critique RGPD

**Alerte** : Si 1 seul fichier non supprimé → escalade immédiate

---

#### KPI-04 : Temps de réponse API (p95)
**Définition** : 95e percentile du temps de réponse des endpoints API

- **Formule** : Temps de réponse au 95e percentile (ms)
- **Cible** : < 200ms (p95)
- **Fréquence** : Mesure continue
- **Source** : APM (Application Performance Monitoring)
- **Responsable** : Équipe backend

**Seuils** :
- 🟢 < 200ms
- 🟡 200-500ms → Optimisation requise
- 🔴 > 500ms → Dégradation UX

---

### 2.2 Efficacité des Contrôles de Sécurité

#### KPI-05 : Taux de détection malwares
**Définition** : Pourcentage de fichiers malveillants bloqués avant mise à disposition

- **Formule** : `Malwares bloqués / (Malwares bloqués + Malwares distribués) × 100`
- **Cible** : 100% (zéro malware distribué)
- **Fréquence** : Temps réel, rapport quotidien
- **Source** : Logs ClamAV + rapports incidents
- **Responsable** : Responsable sécurité

**Seuils** :
- 🟢 100%
- 🔴 < 100% → Incident critique + review urgente

**Note** : Tests réguliers avec EICAR et fichiers malveillants connus.

---

#### KPI-06 : Taux de blocage par rate limiting
**Définition** : Pourcentage de requêtes bloquées par le rate limiting

- **Formule** : `Requêtes bloquées (429) / Requêtes totales × 100`
- **Cible** : 0.5-2% (indique efficacité sans bloquer utilisateurs légitimes)
- **Fréquence** : Quotidienne
- **Source** : Logs rate limiting (Redis)
- **Responsable** : DevOps

**Seuils** :
- 🟢 0.5-2%
- 🟡 2-5% → Vérifier si abuse ou limite trop stricte
- 🔴 > 5% → Faux positifs possibles, ajuster

---

#### KPI-07 : Couverture des tests de sécurité
**Définition** : Pourcentage du code critique couvert par des tests

- **Formule** : `Lignes couvertes / Lignes totales × 100`
- **Cible** : ≥ 80% (code crypto, auth, upload/download)
- **Fréquence** : À chaque commit (CI/CD)
- **Source** : Coverage report (pytest-cov, Jest)
- **Responsable** : Équipe dev

**Seuils** :
- 🟢 ≥ 80%
- 🟡 70-79% → Amélioration nécessaire
- 🔴 < 70% → Blocage PR

---

#### KPI-08 : Temps moyen de correction des vulnérabilités critiques
**Définition** : Délai entre détection et patch en production

- **Formule** : `Somme(temps de correction) / Nombre de vulns critiques`
- **Cible** : < 24h pour CRITICAL, < 7 jours pour HIGH
- **Fréquence** : Mensuelle
- **Source** : Suivi Jira/GitHub Issues
- **Responsable** : Responsable sécurité

**Seuils** :
- 🟢 CRITICAL < 24h, HIGH < 7j
- 🟡 CRITICAL < 48h, HIGH < 14j
- 🔴 Au-delà → Escalade management

---

### 2.3 Conformité RGPD

#### KPI-09 : Taux de traitement des demandes RGPD
**Définition** : Demandes d'accès/suppression traitées dans le délai légal (72h)

- **Formule** : `Demandes traitées < 72h / Demandes totales × 100`
- **Cible** : 100%
- **Fréquence** : Mensuelle
- **Source** : Registre RGPD
- **Responsable** : DPO

**Seuils** :
- 🟢 100%
- 🔴 < 100% → Non-conformité légale

---

#### KPI-10 : Durée moyenne de conservation des fichiers
**Définition** : Temps moyen entre upload et suppression définitive

- **Formule** : `Somme(durées de vie) / Nombre de fichiers`
- **Cible** : < 24h (indication bonne utilisation éphémère)
- **Fréquence** : Hebdomadaire
- **Source** : Métadonnées DB
- **Responsable** : Product Owner

---

## 3. KRIs Sécurité (Risques)

### 3.1 Indicateurs d'Attaque

#### KRI-01 : Tentatives d'accès invalides
**Définition** : Nombre de tentatives de download avec token invalide

- **Formule** : Nombre de HTTP 404/403 sur `/download/{token}`
- **Seuil d'alerte** : > 100/heure
- **Fréquence** : Temps réel
- **Source** : Logs applicatifs + WAF
- **Responsable** : SOC/DevOps

**Actions** :
- > 100/h → Alerte Slack
- > 500/h → Investigation (brute force?)
- > 1000/h → Blacklist IP automatique

---

#### KRI-02 : Pics de requêtes anormaux
**Définition** : Écart soudain du volume de requêtes par rapport à la baseline

- **Formule** : `(Requêtes actuelles - Moyenne glissante 24h) / Écart-type`
- **Seuil d'alerte** : > 3 écarts-types (indicateur statistique DDoS)
- **Fréquence** : Temps réel (fenêtre 5 min)
- **Source** : Métriques serveur (Prometheus)
- **Responsable** : DevOps

**Actions** :
- Z-score > 3 → Alerte investigation
- Z-score > 5 → Activation protection DDoS (Cloudflare, rate limit agressif)

---

#### KRI-03 : Uploads bloqués par type MIME suspect
**Définition** : Tentatives d'upload de fichiers exécutables/scripts

- **Formule** : Nombre de rejets pour MIME non autorisé
- **Seuil d'alerte** : > 50/jour
- **Fréquence** : Quotidienne
- **Source** : Logs validation fichiers
- **Responsable** : Responsable sécurité

**Actions** :
- > 50/jour → Analyse manuelle (campagne d'attaque?)
- Même IP > 10 tentatives → Blacklist

---

#### KRI-04 : Échecs scan antivirus
**Définition** : Fichiers détectés comme malveillants

- **Formule** : Nombre de malwares détectés
- **Seuil d'alerte** : > 0
- **Fréquence** : Temps réel
- **Source** : ClamAV logs
- **Responsable** : Responsable sécurité

**Actions** :
- 1 détection → Log + alerte + blocage lien
- > 5/jour → Investigation approfondie (campagne?)

---

### 3.2 Indicateurs Opérationnels de Risque

#### KRI-05 : Vulnérabilités non patchées (dépendances)
**Définition** : Nombre de CVE critiques/hautes dans les dépendances

- **Formule** : Nombre de CVE CRITICAL + HIGH non résolues
- **Seuil d'alerte** : > 0 CRITICAL, > 5 HIGH
- **Fréquence** : Quotidienne (scan SCA automatique)
- **Source** : Snyk / Safety / npm audit
- **Responsable** : Équipe dev

**Actions** :
- CRITICAL > 0 → Blocage déploiement
- HIGH > 5 → Plan de patch < 7 jours

---

#### KRI-06 : Échecs pipeline DevSecOps
**Définition** : Nombre de builds échouant aux tests de sécurité

- **Formule** : Nombre de builds bloqués par SAST/DAST/SCA
- **Seuil d'alerte** : > 10% des builds
- **Fréquence** : Hebdomadaire
- **Source** : GitHub Actions / GitLab CI
- **Responsable** : Tech Lead

**Actions** :
- > 10% → Formation équipe + revue des règles
- Trend croissant → Audit qualité code

---

#### KRI-07 : Temps moyen de détection des incidents (MTTD)
**Définition** : Délai entre début d'incident et détection

- **Formule** : `Somme(temps de détection) / Nombre d'incidents`
- **Cible** : < 15 minutes
- **Fréquence** : Trimestrielle (post-incident)
- **Source** : Post-mortem incidents
- **Responsable** : Responsable sécurité

**Actions** :
- > 15 min → Amélioration monitoring
- > 1h → Revue complète alertes

---

#### KRI-08 : Certificats SSL expirant
**Définition** : Nombre de certificats expirant dans < 30 jours

- **Formule** : Nombre de certs avec validité < 30 jours
- **Seuil d'alerte** : > 0
- **Fréquence** : Quotidienne
- **Source** : Script de vérification certs
- **Responsable** : DevOps

**Actions** :
- < 30 jours → Alerte
- < 7 jours → Escalade urgente
- Expiré → Incident majeur

---

### 3.3 Indicateurs Conformité et Gouvernance

#### KRI-09 : Logs non conformes RGPD
**Définition** : Détection de données personnelles en clair dans les logs

- **Formule** : Nombre d'occurrences (emails, IPs non hashées, noms)
- **Seuil d'alerte** : > 0
- **Fréquence** : Hebdomadaire (scan automatisé)
- **Source** : Script de parsing logs
- **Responsable** : DPO

**Actions** :
- > 0 → Investigation + correction code
- Récurrence → Audit RGPD complet

---

#### KRI-10 : Fichiers "fantômes" (non supprimés)
**Définition** : Fichiers présents sur S3 mais absents de la DB (incohérence)

- **Formule** : `COUNT(S3 objects) - COUNT(DB records)`
- **Seuil d'alerte** : > 10
- **Fréquence** : Quotidienne (cron reconciliation)
- **Source** : Script de reconciliation S3 ↔ DB
- **Responsable** : Équipe backend

**Actions** :
- > 10 → Investigation + cleanup manuel
- Trend croissant → Bug critique suppression

---

## 4. Dashboard et Visualisation

### 4.1 Dashboard Temps Réel (Grafana)

**Panneaux recommandés** :

1. **Vue d'ensemble Sécurité**
   - KPI-03 : Taux suppression (gauge)
   - KRI-01 : Tentatives invalides (graph temps réel)
   - KRI-04 : Malwares détectés (counter)
   - KRI-05 : Vulnérabilités critiques (badge)

2. **Performance**
   - KPI-01 : Uptime (ligne 30j)
   - KPI-04 : Latence p95 (heatmap)
   - KPI-02 : Taux succès uploads (gauge)

3. **Abuse & Anomalies**
   - KRI-02 : Volume requêtes (graph avec baseline)
   - KPI-06 : Taux rate limiting (ligne)
   - KRI-03 : Uploads suspects (bar chart par type)

4. **Conformité**
   - KPI-09 : Demandes RGPD (table)
   - KRI-10 : Fichiers fantômes (counter)
   - KPI-10 : Durée moyenne conservation (gauge)

---

### 4.2 Alertes Automatisées

| Indicateur | Canal | Sévérité | Destinataire |
|------------|-------|----------|--------------|
| KPI-03 < 100% | Slack + Email | CRITICAL | Toute l'équipe |
| KRI-01 > 500/h | Slack | HIGH | DevOps + Sécu |
| KRI-04 > 0 | Slack + Ticket | HIGH | Responsable sécu |
| KRI-05 (CRITICAL) > 0 | Email | CRITICAL | Tech Lead + DevOps |
| KRI-08 < 7j | Email | HIGH | DevOps |
| KRI-10 > 50 | Ticket | MEDIUM | Backend team |

---

## 5. Rapports Périodiques

### 5.1 Rapport Quotidien Automatisé

**Envoi** : Email @ 9h00 (lun-ven)
**Destinataires** : Équipe projet

**Contenu** :
- ✅ Uptime 24h (KPI-01)
- ✅ Uploads/downloads 24h avec taux succès (KPI-02)
- ✅ Incidents sécurité (KRI-04, KRI-01)
- ✅ Vulnérabilités nouvelles (KRI-05)
- ✅ Top 5 IPs par volume de requêtes

---

### 5.2 Rapport Hebdomadaire

**Envoi** : Lundi matin
**Destinataires** : Management + équipe

**Contenu** :
- 📊 KPIs principaux (tendances 7j vs semaine précédente)
- 📊 KRIs : nombre d'alertes déclenchées
- 📊 Incidents résolus et en cours
- 📊 Progression backlog sécurité
- 📊 Recommandations actions prioritaires

---

### 5.3 Rapport Mensuel Exécutif

**Envoi** : 1er jour du mois
**Destinataires** : Direction + stakeholders

**Contenu** :
- 🎯 Synthèse exécutive (1 page)
- 🎯 KPIs vs objectifs
- 🎯 Incidents majeurs du mois
- 🎯 Conformité RGPD (KPI-09)
- 🎯 Investissements sécurité recommandés
- 🎯 Évolution des risques (tendances)

---

## 6. Revue et Amélioration Continue

### 6.1 Cadence de Revue

- **Mensuel** : Revue KPIs/KRIs avec équipe, ajustement seuils
- **Trimestriel** : Revue stratégique, ajout/suppression indicateurs
- **Annuel** : Benchmarking externe, audit complet

### 6.2 Critères d'Ajustement des Seuils

Les seuils sont ajustés si :
- Trop d'alertes (faux positifs > 20%)
- Pas assez d'alertes (incidents non détectés)
- Évolution de la menace (nouvelles attaques)
- Changement d'architecture

---

## 7. Outils et Intégrations

| Catégorie | Outil | KPIs/KRIs mesurés |
|-----------|-------|-------------------|
| **Monitoring** | Prometheus + Grafana | KPI-01, KPI-04, KRI-02 |
| **Logs** | ELK Stack / Loki | KPI-02, KPI-03, KRI-01, KRI-04 |
| **APM** | Datadog / New Relic | KPI-04, KRI-07 |
| **Security Scanning** | Snyk / Trivy | KRI-05 |
| **Alerting** | PagerDuty / Opsgenie | Tous les KRIs |
| **RGPD** | Custom DB | KPI-09, KPI-10 |

---

## 8. Exemple de Scorecard Mensuel

| Indicateur | Cible | Jan 2025 | Fév 2025 | Tendance | Statut |
|------------|-------|----------|----------|----------|--------|
| **KPI-01** Uptime | ≥99.5% | 99.8% | 99.7% | ➡️ Stable | 🟢 |
| **KPI-02** Uploads réussis | ≥99% | 99.4% | 99.6% | ⬆️ Amélioration | 🟢 |
| **KPI-03** Suppression | 100% | 100% | 100% | ➡️ Parfait | 🟢 |
| **KPI-04** Latence p95 | <200ms | 145ms | 160ms | ⬇️ Dégradation | 🟢 |
| **KPI-05** Malwares bloqués | 100% | 100% | 100% | ➡️ Parfait | 🟢 |
| **KPI-07** Coverage tests | ≥80% | 82% | 85% | ⬆️ Amélioration | 🟢 |
| **KRI-01** Accès invalides | <100/h | 45/h | 52/h | ⬆️ Augmentation | 🟢 |
| **KRI-04** Malwares détectés | - | 3 | 7 | ⬆️ Campagne? | 🟡 |
| **KRI-05** Vulns CRITICAL | 0 | 0 | 0 | ➡️ Bon | 🟢 |
| **KRI-10** Fichiers fantômes | <10 | 2 | 1 | ⬇️ Amélioration | 🟢 |

**Score global** : 9/10 🟢 (1 indicateur en surveillance)

---

## 9. Responsabilités

| Rôle | Responsabilités KPIs/KRIs |
|------|---------------------------|
| **Responsable sécurité** | Définition, suivi, rapports, escalade |
| **DevOps** | Configuration monitoring, alertes, disponibilité |
| **Développeurs** | Implémentation instrumentation, correction anomalies |
| **Product Owner** | Arbitrage objectifs, priorisation actions |
| **DPO** | KPIs/KRIs RGPD, audits |

