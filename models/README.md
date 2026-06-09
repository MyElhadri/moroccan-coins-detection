# Dossier Modèles (YOLOv8 Weights)

Ce dossier est destiné à héberger les fichiers de poids issus de l'entraînement du modèle YOLOv8 sur Google Colab.

## Instructions pour le déploiement du modèle

Une fois l'entraînement terminé dans Google Colab :
1. Téléchargez le fichier de poids optimaux, nommé par défaut `best.pt`.
2. Déplacez ce fichier dans ce dossier (`models/`).
3. Relancez l'application Streamlit ou rafraîchissez la page. L'application détectera automatiquement la présence de `models/best.pt` et basculera du **Mode Simulation** au **Mode Détection Réelle** (YOLOv8).

## Fichiers attendus après l'entraînement

*   `models/best.pt` : Le fichier de poids principal utilisé par l'application (les meilleurs poids d'époque).
*   `models/last.pt` (optionnel) : Les poids de la toute dernière époque d'entraînement.

> **Note académique :** Le fichier de poids `best.pt` est configuré dans le `.gitignore` pour éviter d'encombrer le dépôt Git avec des fichiers binaires volumineux. Assurez-vous de le copier localement lors du déploiement de l'application.
