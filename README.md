# 🪙 Moroccan Coins Detection & Real-Time Amount Calculation

> **Computer Vision system for automated detection of Moroccan metallic currency (1 DH, 2 DH, 5 DH, 10 DH) and instantaneous total sum calculation using YOLOv8 and Streamlit.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=flat&logo=yolo&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Image_Processing-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![Roboflow](https://img.shields.io/badge/Roboflow-Annotation-6706CE?style=flat&logo=roboflow&logoColor=white)](https://roboflow.com/)

---

## 📌 Aperçu du Projet

Ce projet académique (ENSA Tanger, 2025/2026) implémente une solution de vision par ordinateur pour :
1. **Détecter et classifier** les pièces de monnaie marocaines métalliques : **1 DH, 2 DH, 5 DH, et 10 DH**.
2. **Calculer automatiquement la somme totale** présente sur l'image après détection.
3. Offrir une **interface web interactive (Streamlit)** pour tester des images réelles ou utiliser un mode simulation.

| Métrique / Caractéristique | Spécification |
|:---|:---|
| **Modèle Backbone** | YOLOv8 (Ultralytics) |
| **Précision globale** | **98.6% mAP@50** sur les données de validation |
| **Classes Détectées** | 4 coupures (1 DH, 2 DH, 5 DH, 10 DH) |
| **Interface** | Streamlit avec drag-and-drop & visualisation comparative |
| **Supervision** | Pr. Abdelmonaime Lachkar · ENSA Tanger |

---

## 🌟 Fonctionnalités Clés

- **Détection Multi-pièces Précise :** Détection d'objets rapide et robuste sur des pièces isolées ou multiples.
- **Calculateur de Somme Automatisé :** Pipeline de post-traitement comptabilisant chaque pièce détectée par sa valeur faciale pour afficher la somme instantanément.
- **Interface Utilisateur Moderne :** Drag-and-drop, affichage côte à côte (originale vs annotée) et tableau récapitulatif détaillé avec les scores de confiance.
- **Mode Démo & Simulation :** Permet d'évaluer la chaîne de traitement même en l'absence temporaire des poids finaux du modèle.
- **Export & Historique :** Sauvegarde horodatée des prédictions dans `results/predictions/` avec option de téléchargement.

---

## 🛠️ Architecture du Projet

```
moroccan-coins-detection/
├── app/                        # Application Streamlit
│   ├── app.py                  # Interface web principale
│   ├── detector.py             # Pipeline d'inférence YOLOv8 & Simulateur
│   └── utils.py                # Utilitaires de rendu et d'annotation
├── data/                       # Structure des datasets
│   ├── dataset_yolo/           # Données labellisées (train, valid, test)
│   │   └── data.yaml           # Définition des classes YOLO
│   └── test_images/            # Échantillons de test
├── docs/                       # Documentation méthodologique
│   ├── annotation_guidelines.md# Protocole d'annotation Roboflow
│   ├── dataset_guidelines.md   # Spécifications de prise de vue
│   └── project_plan.md         # Planification du projet
├── models/                     # Poids du modèle (best.pt)
├── notebooks/                  # Notebooks d'entraînement
│   └── train_yolo_colab.ipynb  # Entraînement GPU sur Google Colab
├── results/                    # Sorties graphiques et prédictions
├── requirements.txt            # Dépendances Python
└── run_app.bat                 # Script de démarrage rapide sous Windows
```

---

## 🚀 Installation et Lancement

### 1. Prérequis
- Python 3.8 ou supérieur installé
- Git

### 2. Cloner et installer les dépendances
```bash
git clone https://github.com/MyElhadri/moroccan-coins-detection.git
cd moroccan-coins-detection

# Créer un environnement virtuel (recommandé)
python -m venv .venv
source .venv/bin/activate    # Linux / macOS
# .venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Démarrer l'application
- **Sous Windows :** Double-cliquez sur `run_app.bat`
- **En ligne de commande :**
```bash
streamlit run app/app.py
```
L'application est accessible à l'adresse : `http://localhost:8501`.

---

## 🔬 Entraînement (Google Colab)

1. Ouvrez le notebook `notebooks/train_yolo_colab.ipynb` dans Google Colab.
2. Connectez le GPU Colab (T4 recommandé).
3. Importez vos données depuis Roboflow en suivant les instructions du notebook.
4. Lancez l'entraînement YOLOv8. Une fois terminé, téléchargez le fichier `best.pt` et placez-le dans le dossier `models/`.

---

## 👥 Auteurs & Encadrement

- **Mohamed Yassine EL HADRI** ([@MyElhadri](https://github.com/MyElhadri))
- **Mosab BENABDELLAH**
- **Encadrant :** Pr. Abdelmonaime Lachkar
- **Institution :** École Nationale des Sciences Appliquées de Tanger (ENSA Tanger), Année 2025/2026
