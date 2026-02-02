# 📊 Tableau de Bord Investissements Hebdomadaire - NSIA VIE ASSURANCES

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

## 📋 Description

Application web interactive développée avec **Streamlit** pour le suivi et l'analyse hebdomadaire des investissements de **NSIA VIE ASSURANCES**. Cette solution offre une visualisation en temps réel des performances financières par classe d'actifs avec un suivi budgétaire détaillé.

### 🎯 Objectifs

- Centraliser le suivi des investissements hebdomadaires
- Comparer les réalisations aux budgets prévisionnels
- Analyser les taux de réalisation par classe d'actifs
- Faciliter les briefings hebdomadaires de la Direction des Investissements
- Maintenir un historique des performances

---

## ✨ Fonctionnalités Principales

### 📅 Gestion Temporelle
- **Filtre par période** : Sélection dynamique de la semaine analysée
- **Navigation historique** : Consultation des données des semaines précédentes
- **Semaine actuelle** : Bouton de retour rapide à la période en cours
- **Historique complet** : Stockage automatique de toutes les semaines saisies

### 💰 Gestion des Investissements
Suivi de **8 classes d'actifs** :
1. Obligations d'États
2. Obligations des sociétés commerciales
3. Actions des Sociétés Commerciales
4. Droits immobiliers
5. Prêts
6. Dépôts à terme
7. Autres investissements
8. Investissements d'exploitation (DRI)

### 📊 Indicateurs Clés de Performance (KPI)

#### KPI Hebdomadaire
- Réalisation de la semaine vs budget
- Taux de réalisation
- Écart en montant et en pourcentage

#### KPI Cumulé
- Réalisation cumulée depuis le début de l'année
- Progression par rapport au budget annuel ajusté
- Montant restant à réaliser

#### KPI Globaux
- Performance globale (nombre d'objectifs atteints)
- Taux de succès par classe d'actifs
- Badges de statut (Objectif atteint / En cours / En retard)

### 📈 Visualisations Interactives

1. **Budget vs Réalisation Hebdomadaire**
   - Graphique en barres groupées
   - Comparaison visuelle immédiate
   - Valeurs affichées sur les barres

2. **Taux de Réalisation par Actif**
   - Code couleur intelligent (vert/jaune/rouge)
   - Ligne de référence à 100%
   - Identification rapide des performances

3. **Réalisation Cumulée vs Budget**
   - Courbes d'évolution
   - Tendances par classe d'actifs
   - Analyse comparative

### 📋 Tableau Détaillé
- Vue complète de tous les indicateurs
- Format professionnel avec séparateurs de milliers
- Calculs automatiques (écarts, taux)
- Export possible des données

---

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt** (ou télécharger le fichier)
```bash
