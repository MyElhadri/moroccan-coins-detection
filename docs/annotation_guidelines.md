# Guide d'Annotation des Pièces sur Roboflow

L'annotation consiste à dessiner des boîtes englobantes (*bounding boxes*) autour de chaque pièce de monnaie et à lui attribuer son étiquette de classe correcte. Pour ce projet, nous utilisons **Roboflow**, un outil en ligne gratuit et performant pour préparer les données pour YOLOv8.

---

## 1. Création du Projet sur Roboflow

1.  Rendez-vous sur [Roboflow](https://roboflow.com/) et créez un compte gratuit.
2.  Cliquez sur **"Create New Project"**.
3.  Configurez le projet avec les paramètres suivants :
    *   **Project Type :** Object Detection (Bounding Boxes)
    *   **What are you detecting? :** `Moroccan Coins`
    *   **License :** Private ou Public (selon vos préférences académiques)
4.  Ajoutez vos classes cibles exactes (dans le bon ordre) :
    *   `coin_1dh`
    *   `coin_2dh`
    *   `coin_5dh`
    *   `coin_10dh`

---

## 2. Règles d'Or pour le Tracé des Boîtes

Pour obtenir des détections ultra-précises du modèle, respectez scrupuleusement ces règles lors du dessin des rectangles sur Roboflow :

### 🎯 A. Ajustement des Boîtes (Tight Bounding Boxes)
*   **Pas trop grand :** Le rectangle doit épouser parfaitement le contour extérieur de la pièce. Ne laissez pas de marges vides inutiles autour de la pièce (cela apprendrait au modèle que le fond fait partie de l'objet).
*   **Pas trop petit :** Ne coupez pas les bords de la pièce. La boîte doit englober 100% du disque de la pièce.

### 🧩 B. Gestion des Superpositions (Occlusion)
*   Lorsque deux pièces se chevauchent légèrement :
    *   Dessinez une boîte complète pour la pièce de devant (100% visible).
    *   Dessinez également une boîte pour la pièce de derrière, même si elle est en partie masquée. Estimez où se trouvent ses bords réels.
    *   *Règle académique :* N'annotez une pièce partiellement masquée que si elle reste identifiable à l'œil nu (au moins 50% de la pièce visible).

### ✂️ C. Pièces coupées aux bords de l'image
*   Si une pièce se trouve sur la bordure de votre photo et qu'elle est coupée en deux par le cadre :
    *   Dessinez la boîte uniquement sur la partie visible dans l'image.
    *   N'annotez la pièce que si vous pouvez l'identifier sans ambiguïté (ex: on distingue clairement les détails d'une pièce de 10 DH bien qu'elle soit coupée à 30%).

---

## 3. Partitionnement des Données (Dataset Split)

Roboflow gère automatiquement ou manuellement le partitionnement de votre dataset. Conservez les proportions standard recommandées pour l'apprentissage profond :

*   **Train Set (Entraînement) : 70%** - Données sur lesquelles le modèle apprend à reconnaître les motifs.
*   **Validation Set (Validation) : 20%** - Données utilisées pendant l'entraînement pour mesurer l'apprentissage et ajuster les hyperparamètres (éviter le surapprentissage).
*   **Test Set (Test) : 10%** - Données de contrôle final, jamais vues par le modèle, pour simuler des prédictions réelles.

---

## 4. Augmentation de Données Recommandée

Dans Roboflow, lors de l'étape **"Generate"**, vous pouvez appliquer des augmentations pour multiplier artificiellement le nombre de vos images et rendre votre modèle plus robuste.

### Augmentations conseillées pour les pièces de monnaie :
1.  **Rotation (90° Rotation, Rotation libre -15° à +15°) :** Les pièces n'ont pas de sens haut/bas fixe. La rotation les présente sous tous les angles.
2.  **Luminosité (Brightness -15% à +15%) :** Simule des conditions d'éclairage variables (nuageux, ensoleillé).
3.  **Flou (Blur jusqu'à 1.5px) :** Simule des photos légèrement floues prises à main levée par un smartphone.
4.  **Bruit (Noise jusqu'à 5%) :** Simule le grain des capteurs de caméra en basse luminosité.

> ⚠️ **Attention :** N'utilisez pas l'augmentation **Flip vertical/horizontal** sans précaution si des inscriptions textuelles asymétriques sur les pièces sont cruciales (bien que YOLOv8 gère généralement très bien cela pour les disques). N'utilisez pas de déformation géométrique agressive (type shear/perspective trop fort) qui déformerait le cercle des pièces en ellipses trop aplaties.

---

## 5. Exportation vers Google Colab

Une fois le dataset généré sur Roboflow :
1.  Cliquez sur **"Export Dataset"**.
2.  Sélectionnez le format **YOLOv8**.
3.  Choisissez l'option **"show download code"** (code de téléchargement).
4.  Copiez le script Python contenant votre clé API unique. Vous collerez ce code directement dans la cellule correspondante de votre notebook Colab [train_yolo_colab.ipynb](file:///c:/Users/Yassine/Desktop/info2/s2/traitement_image/notebooks/train_yolo_colab.ipynb).
