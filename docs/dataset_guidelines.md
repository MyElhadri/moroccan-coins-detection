# Guide de Collecte du Dataset de Pièces Marocaines

La qualité des prédictions d'un modèle YOLOv8 dépend directement de la diversité et de la qualité des images fournies lors de son entraînement. Ce guide détaille les meilleures pratiques pour photographier vos pièces de monnaie afin de constituer un dataset robuste et académique.

---

## 1. Directives de Prise de Vue

### 📸 A. Arrière-plans & Contextes
*   **Variété des supports :** Prenez des photos sur différents types de tables, bureaux, nappes, tissus, tapis ou sols (bois, marbre, plastique, papier blanc/quadrillé).
*   **Contrastes :** Variez la couleur des surfaces (supports clairs, sombres, texturés) pour forcer le modèle à reconnaître la forme de la pièce et non son fond.
*   **Surfaces réalistes :** Incluez quelques photos des pièces tenues dans la main, posées sur un porte-feuille, ou éparpillées sur un comptoir pour simuler des scénarios réels.

### ☀️ B. Éclairage & Ombres
*   **Lumière naturelle vs. artificielle :** Prenez des photos en extérieur, sous lumière directe du soleil, à l'ombre, ou en intérieur sous lampe jaune/blanche.
*   **Gestion des reflets :** Les pièces métalliques brillent et créent des reflets. Variez l'orientation de votre source de lumière pour avoir des pièces mates, d'autres brillantes et d'autres partiellement ombragées.
*   **Ombres portées :** Ne masquez pas artificiellement toutes les ombres. Les ombres nettes autour des pièces aident le modèle à comprendre le relief et la profondeur.

### 📐 C. Angles & Distances de caméra
*   **Vue plongeante (Orthogonale) :** C'est l'angle principal (vue de dessus à 90°).
*   **Vue inclinée (Perspective) :** Prenez 30% d'images avec un angle incliné (45° à 75°) car dans la réalité, l'utilisateur prend rarement sa photo parfaitement de dessus.
*   **Distance (Échelle) :** 
    *   Prenez des photos de très près (les pièces occupent 40% de l'image).
    *   Prenez des photos de plus loin (les pièces occupent 5% de l'image, au milieu d'un grand décor).
    *   Le modèle apprendra ainsi à détecter les pièces peu importe leur taille relative à l'image.

### 🪙 D. Composition & Dispositions
*   **Pièces isolées :** Une seule pièce sur l'image.
*   **Groupes de pièces séparées :** Plusieurs pièces distinctes n'ayant aucun contact physique.
*   **Pièces accolées ou superposées :** Pièces qui se touchent ou se recouvrent légèrement (ex: une pièce de 1 DH couvrant à 15% une pièce de 10 DH). Cela aide le modèle à résoudre les occultations partielles.

---

## 2. Recommandations Techniques

*   **Format d'image :** Privilégiez les formats standard `JPG` ou `PNG`.
*   **Résolution :** Une résolution de **640x640 pixels** ou supérieure est idéale. YOLOv8 redimensionne les images en 640x640 par défaut. Inutile de prendre des photos de 108 Megapixels qui ralentiront le téléversement et l'annotation. Des photos d'environ 1920x1080 (HD) ou de téléphones portables standard conviennent parfaitement.
*   **Volume cible :** 
    *   **Minimum absolu :** 50 photos par classe (soit ~200 photos au total).
    *   **Recommandé pour un projet académique correct :** 100 à 150 photos par classe (soit ~500 images au total).

---

## 3. Organisation Locale des Fichiers

Avant d'importer vos images sur la plateforme d'annotation **Roboflow**, triez-les localement dans le dossier suivant de votre projet pour garder une trace de vos images brutes non-annotées :

```
data/
└── raw_images/
    ├── coin_1dh/     <-- Placez ici vos photos brutes de 1 Dirham
    ├── coin_2dh/     <-- Placez ici vos photos brutes de 2 Dirhams
    ├── coin_5dh/     <-- Placez ici vos photos brutes de 5 Dirhams
    ├── coin_10dh/    <-- Placez ici vos photos brutes de 10 Dirhams
    └── mixed_coins/  <-- Placez ici vos photos contenant plusieurs pièces ensemble
```

*(Note : les sous-dossiers locaux contiennent un fichier `.gitkeep` pour conserver la structure dans Git, mais vos images réelles ne doivent pas être poussées sur GitHub pour respecter les limites de taille de fichiers. Elles sont déjà exclues dans le `.gitignore` du projet).*
