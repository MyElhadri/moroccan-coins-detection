# Fiche de Révision & Notes de Présentation pour la Soutenance

Ce guide récapitule les points essentiels à maîtriser pour présenter avec succès votre projet **"Moroccan Coins Detection and Total Amount Calculation"** devant le jury académique.

---

## 1. Pitch d'Introduction (L'accroche - 1 minute)

> *"Monsieur le Président, Messieurs les membres du jury, bonjour. Dans le cadre de nos travaux pratiques en traitement d'images, nous nous sommes penchés sur un problème du quotidien : la comptabilisation automatique d'argent liquide. 
> Notre projet s'intitule 'Détection de Pièces Marocaines et Calcul du Montant Total'. À l'aide de l'algorithme de Deep Learning de pointe YOLOv8 et d'une interface Streamlit interactive, nous avons conçu un système capable de détecter individuellement les pièces de 1, 2, 5 et 10 DH sur une simple photo et de calculer instantanément le montant total représenté. 
> Voici la méthodologie que nous avons suivie et les résultats que nous avons obtenus..."*

---

## 2. Structure Recommandée du Diaporama (Soutenance de 10-15 min)

1.  **Introduction & Problématique :** Importance de la vision par ordinateur, limitations des méthodes traditionnelles de traitement d'images pour les pièces (ombres, reflets, textures).
2.  **Objectifs du Projet :** Périmètre limité aux 4 pièces marocaines courantes (1, 2, 5, 10 DH) excluant les centimes et billets.
3.  **Constitution du Dataset :** Collecte des images, diversité des arrière-plans et conditions d'éclairage. Rôle de la plateforme Roboflow pour l'annotation.
4.  **Méthodologie & Entraînement :** Pourquoi YOLOv8 ? Description de l'architecture, processus d'entraînement sur Google Colab (loss curves, nombre d'époques).
5.  **Analyse des Résultats :** Présentation des métriques de validation (Courbe de précision, de rappel, mAP50, Matrice de confusion).
6.  **Démonstration (Live Demo) :** Présentation en temps réel de l'application web Streamlit (téléversement d'image, détection, calcul de la somme).
7.  **Perspectives & Conclusion :** Améliorations futures (gestion des centimes, détection de faux billets, intégration sur application mobile).

---

## 3. Justification des Choix Techniques (Arguments Clés)

*   **Pourquoi YOLOv8 (Ultralytics) ?**
    *   *Vitesse et Précision :* YOLO (You Only Look Once) est l'état de l'art en détection d'objets en temps réel. Sa version 8 offre le meilleur compromis entre vitesse d'inférence (pour un déploiement embarqué ou mobile futur) et précision de localisation.
    *   *Détection de bout en bout (End-to-End) :* Contrairement aux approches classiques qui séparent la localisation (ex: trouver les cercles) de la classification (ex: reconnaître la pièce), YOLO effectue les deux tâches simultanément en une seule passe réseau.
*   **Pourquoi Streamlit pour l'interface ?**
    *   *Simplicité Python :* Streamlit permet de créer des applications web interactives esthétiques en pur Python en quelques lignes de code, facilitant le prototypage et la démonstration sans nécessiter de compétences approfondies en HTML/CSS/JS.

---

## 4. Questions Typiques du Jury & Réponses Préparées

### ❓ Q1. Pourquoi ne pas avoir utilisé la méthode classique de détection de cercles de OpenCV (Transformée de Hough Circle) ?
*   **Réponse :** *"La Transformée de Hough pour les cercles est très sensible au bruit et aux variations géométriques. Si la photo est prise avec un angle incliné, les pièces de monnaie apparaissent sous forme d'ellipses et non de cercles parfaits, ce qui fait échouer Hough. De plus, Hough ne fait que localiser les cercles, il ne permet pas de classifier les pièces (différencier 5 DH de 10 DH par exemple). YOLOv8, quant à lui, apprend les textures, les reliefs et les motifs bicolores des pièces, ce qui le rend robuste aux reflets, aux angles de prise de vue et aux occultations partielles."*

### ❓ Q2. Comment votre modèle gère-t-il les pièces qui se chevauchent ou se superposent ?
*   **Réponse :** *"Grâce à l'étape d'annotation sur Roboflow, nous avons inclus des exemples de pièces se chevauchant partiellement. L'algorithme YOLOv8 apprend à détecter des motifs partiels. Lors de l'inférence, le mécanisme de suppression non maximale (NMS) permet de conserver une boîte englobante par objet distinct détecté, même s'ils sont très proches ou superposés."*

### ❓ Q3. Pourquoi avoir exclu les centimes et les billets ?
*   **Réponse :** *"Pour garantir une haute précision dans le cadre de ce projet académique, nous avons choisi de nous concentrer sur les objets métalliques circulaires à forte valeur faciale (1 DH à 10 DH). L'inclusion des centimes (jaunes en cuivre ou petits formats) et des billets (qui nécessitent une détection de formes rectangulaires souples et pliées) aurait grandement complexifié le dataset. C'est une extension naturelle que nous envisageons pour la version 2.0 du projet."*

### ❓ Q4. Quelles sont les limites actuelles de votre application ?
*   **Réponse :** *"Les limites principales résident dans les conditions extrêmes de luminosité (reflets trop intenses masquant les détails de la gravure) et la présence d'objets circulaires non-monétaires (comme des capsules de bouteille) qui pourraient être faussement détectés comme des pièces. Pour y pallier, nous pourrions enrichir le dataset avec des exemples négatifs (background images sans pièces contenant des capsules) pour apprendre au modèle à les ignorer."*

---

## 5. Conseils pour la Démonstration (Live Demo)

1.  **Préparez des images de test à l'avance :** Ne cherchez pas une image sur internet le jour J. Mettez 3-4 images typiques dans `data/test_images/` (une simple avec 3 pièces claires, une plus complexe avec des superpositions, et une sous éclairage faible).
2.  **Montrez la flexibilité du système :** Téléversez une image, cliquez sur "Détecter", montrez le montant calculé et le tableau de comptage.
3.  **Présentez le Mode Simulation comme un atout d'ingénierie :** Si le jury pose des questions sur l'état d'avancement de l'entraînement, expliquez que l'architecture logicielle a été conçue pour être modulaire (grâce au mode simulation), permettant de valider l'interface utilisateur et la logique métier de calcul en parallèle de la collecte et de l'entraînement IA.
