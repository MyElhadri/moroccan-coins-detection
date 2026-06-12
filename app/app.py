import os
import sys
import streamlit as st
from PIL import Image

# Ajouter le répertoire racine au PATH pour des imports sécurisés
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from detector import CoinsDetector
from utils import draw_beautiful_detections, format_currency, save_prediction

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Détection de Pièces Marocaines",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd

# Initialisation du détecteur (chargement du modèle)
@st.cache_resource
def get_detector():
    return CoinsDetector(model_path="models/best.pt")

detector = get_detector()

# --- HEADER DE L'APPLICATION ---
st.title("🪙 Moroccan Coins Detection & Amount Calculator")
st.markdown("**Projet Académique • Traitement d'Images & Deep Learning YOLOv8**")

# --- SIDEBAR (PANNEAU LATÉRAL) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/120/morocco.png", width=70)
    st.markdown("### 🇲🇦 Projet Universitaire")
    st.markdown("""
    **Intitulé :**  
    *Moroccan Coins Detection and Total Amount Calculation*
    
    **Classes Cibles :**  
    Uniquement les pièces de monnaie courantes :
    - 1 DH, 2 DH, 5 DH, 10 DH.
    """)
    
    # Indicateur d'état du modèle
    st.markdown("---")
    st.markdown("### ⚙️ État du Système")
    
    if detector.model_loaded:
        st.success("**✓ YOLOv8 Actif**\n\nModèle de production (best.pt) chargé et opérationnel.")
    else:
        st.warning("**⚠️ Mode Simulation**\n\nFichier `models/best.pt` manquant. Détections simulées activées pour démonstration.")
        
    st.markdown("---")
    st.markdown("### 📘 Guide des Pièces")
    st.markdown("""
    * **1 DH** : Argentée, Cupro-Nickel.
    * **2 DH** : Argentée, Cupro-Nickel (plus grande).
    * **5 DH** : Bicolore (cœur doré, anneau argenté).
    * **10 DH** : Bicolore (cœur argenté, anneau doré).
    """)
    
    st.info("**Fiche Projet :**\n\n• Annotation : Roboflow\n\n• Entraînement : Google Colab\n\n• Détecteur : YOLOv8")

# --- MAIN PANEL (PANNEAU PRINCIPAL) ---
tab_detect, tab_about = st.tabs(["🔍 Détection de Monnaie", "📖 À propos du projet"])

with tab_detect:
    # Instructions initiales
    st.write("Téléversez une image contenant des pièces marocaines pour détecter leurs types et calculer instantanément le montant total.")
    
    # Zone de dépôt d'image
    uploaded_file = st.file_uploader(
        "Sélectionnez une image (JPG, JPEG, PNG)...", 
        type=["jpg", "jpeg", "png"],
        help="Glissez-déposez ou parcourez vos fichiers."
    )
    
    # Force simulation checkbox if developer wants to test it even when best.pt is present
    force_sim = False
    if detector.model_loaded:
        force_sim = st.checkbox("Forcer le mode simulation (pour tests/démonstration)", value=False)

    if uploaded_file is not None:
        # Charger l'image avec Pillow
        image = Image.open(uploaded_file).convert("RGB")
        
        # Diviser l'affichage en 2 colonnes
        col_img, col_stats = st.columns([3, 2])
        
        # Placeholders pour pouvoir écraser le contenu après le clic
        image_placeholder = col_img.empty()
        stats_placeholder = col_stats.empty()
        
        with image_placeholder.container():
            st.markdown("### 🖼️ Image Originale")
            st.image(image, use_container_width=True)
            
        with col_img:
            # Bouton de lancement de la détection
            detect_btn = st.button("🚀 Détecter les pièces", use_container_width=True, type="primary")
            download_placeholder = st.empty()
            
        with stats_placeholder.container():
            st.markdown("### 📊 Résultats de l'Analyse")
            st.info("Cliquez sur le bouton **Détecter les pièces** sous l'image pour lancer le traitement.")

        if detect_btn:
            with st.spinner("Analyse de l'image en cours par l'intelligence artificielle..."):
                # Effectuer la détection (réelle ou simulée)
                results = detector.detect(image, force_simulation=force_sim)
                detections = results["detections"]
                counts = results["counts"]
                total = results["total_amount"]
                is_mock = results["is_mock"]
                
                # Annoter l'image
                annotated_image = draw_beautiful_detections(image, detections)
                
                # Sauvegarder la prédiction localement
                saved_path = save_prediction(annotated_image)
                
            # Écraser l'image originale avec l'image annotée
            with image_placeholder.container():
                st.markdown("### 🎯 Image Annotée")
                st.image(annotated_image, use_container_width=True)
                
            # Ajouter le bouton de téléchargement
            from io import BytesIO
            buffered = BytesIO()
            annotated_image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
            with download_placeholder:
                st.download_button(
                    label="💾 Télécharger l'image annotée",
                    data=img_bytes,
                    file_name=f"detected_coins_{uploaded_file.name}",
                    mime="image/png",
                    use_container_width=True
                )
                
            # Écraser le texte d'info avec les résultats
            with stats_placeholder.container():
                st.markdown("### 📊 Résultats de l'Analyse")
                
                # Notification de simulation si applicable
                if is_mock:
                    st.warning("⚠️ **Mode Démo actif :** Les résultats ci-dessous sont simulés car aucun modèle réel n'est présent dans `models/best.pt`.")
                else:
                    st.success("✅ Détection effectuée avec succès avec le modèle YOLOv8 !")
                
                # Affichage du montant total de manière native
                st.metric(label="Montant Total Calculé", value=format_currency(total), delta=f"{len(detections)} pièces détectées", delta_color="off")
                
                # Tableau récapitulatif détaillé des comptages
                st.markdown("#### Détail par type de pièce :")
                
                t_1 = counts["coin_1dh"]
                t_2 = counts["coin_2dh"]
                t_5 = counts["coin_5dh"]
                t_10 = counts["coin_10dh"]
                
                df_data = {
                    "Pièce": ["1 DH", "2 DH", "5 DH", "10 DH", "TOTAL"],
                    "Description": ["1 Dirham (Bronze)", "2 Dirhams (Argenté)", "5 Dirhams (Doré/Argenté)", "10 Dirhams (Argenté/Doré)", "-"],
                    "Quantité": [t_1, t_2, t_5, t_10, len(detections)],
                    "Sous-total": [
                        format_currency(t_1 * 1.0),
                        format_currency(t_2 * 2.0),
                        format_currency(t_5 * 5.0),
                        format_currency(t_10 * 10.0),
                        format_currency(total)
                    ]
                }
                st.table(pd.DataFrame(df_data))
                
                # Emplacement de sauvegarde
                st.caption(f"Image sauvegardée localement dans : `{saved_path}`")

with tab_about:
    st.markdown("### 📝 Présentation du Projet Académique")
    st.markdown("""
    Ce projet s'inscrit dans le cadre du module académique de **Traitement d'Images**. Il met en pratique des techniques modernes d'apprentissage profond pour la détection d'objets en temps réel, appliquées à la monnaie fiduciaire marocaine (pièces de monnaie métalliques).
    
    #### ⚙️ Pipeline Technologique :
    1.  **Acquisition de données :** Photos réelles prises sous différents angles et conditions d'éclairage.
    2.  **Annotation :** Utilisation de la plateforme **Roboflow** pour tracer les boîtes englobantes (*bounding boxes*) autour de chaque pièce et leur associer l'une des 4 classes de pièces marocaines (`coin_1dh`, `coin_2dh`, `coin_5dh`, `coin_10dh`).
    3.  **Entraînement :** Réalisé avec l'algorithme de pointe **YOLOv8** d'Ultralytics sur un GPU hébergé par **Google Colab**.
    4.  **Interface Utilisateur :** Développée en **Streamlit** (Python) pour fournir un outil interactif, simple et instantané aux utilisateurs ou examinateurs du projet.
    5.  **Calculateur de total :** Algorithme de post-traitement en Python pour extraire les prédictions, compter les instances et multiplier chaque type par sa valeur faciale nominale afin d'afficher la somme cumulée.
    
    #### 🎓 Équipe & Encadrement :
    *   **Projet :** Moroccan Coins Detection and Total Amount Calculation
    *   **Technologie phare :** YOLOv8 (Deep Learning) & Streamlit (Web App)
    """)
