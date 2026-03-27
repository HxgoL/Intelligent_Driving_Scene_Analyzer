# Analyseur Intelligent de Scènes de Conduite

## Description du projet

Ce projet s’inscrit dans le cadre d’un module d’Intelligence Artificielle.  
Il a pour objectif de développer un système capable d’analyser automatiquement des images issues de caméras embarquées (dashcam) afin d’évaluer des situations de conduite.

L’application combine plusieurs domaines de l’IA :
- Vision par ordinateur (détection d’objets)
- Traitement du langage naturel (LLM)
- Systèmes intelligents (agent d’analyse)

L’objectif final est de produire une **analyse complète d’une scène de conduite**, incluant :
- les éléments détectés
- une estimation du niveau de risque
- des recommandations de conduite

---

## Objectifs

Le projet vise à :

- Détecter automatiquement des objets dans une image (véhicules, piétons, panneaux, feux)
- Interpréter ces détections pour comprendre la scène
- Évaluer le niveau de danger (faible à critique)
- Générer un rapport en langage naturel
- Proposer une interface interactive permettant de visualiser les résultats

---

## Fonctionnalités principales

- Upload d’une image dashcam
- Détection automatique des objets présents dans la scène
- Évaluation du niveau de risque
- Génération d’un rapport détaillé en français
- Interface web simple et interactive

---

## Technologies utilisées

- Python
- YOLOv8 (détection d’objets)
- LLM (analyse et génération de texte)
- Streamlit (interface web)
- Jupyter Notebook (expérimentation et analyse)

---

## Données

Le projet utilise des datasets de conduite autonome, notamment :
- Images de dashcam
- Annotations d’objets (véhicules, piétons, etc.)
- Données contextuelles (météo, moment de la journée)

---

## Organisation de l’équipe

Le projet est réalisé en équipe avec une répartition des rôles :

- Vision par ordinateur : entraînement et utilisation du modèle de détection
- Données : préparation, nettoyage et évaluation
- Agent LLM : analyse intelligente et génération du rapport
- Intégration : développement de l’interface et connexion des modules
```bash
git clone <repo_url>
cd projet-ia-conduite
