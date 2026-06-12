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

# Chargement du style CSS personnalisé pour une interface Premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Header Mosaic Style */
    .header-container {
        background: linear-gradient(135deg, #0f2b1d 0%, #1e5a38 100%);
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 25px;
        border-bottom: 5px solid #d4af37;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        color: white;
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 5px;
        color: #f7f7f7;
    }
    .header-subtitle {
        font-size: 1.1rem;
        color: #d4af37;
        font-weight: 300;
    }
    
    /* Premium Metric Card */
    .metric-card {
        background: radial-gradient(circle at top left, #23272a, #16181a);
        border: 2px solid #d4af37;
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .metric-value {
        font-size: 3.5rem;
        font-weight: 700;
        color: #e5c158;
        margin: 5px 0;
        text-shadow: 0 0 10px rgba(229, 193, 88, 0.3);
    }
    .metric-label {
        font-size: 0.9rem;
        color: #9e9e9e;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
    }
    
    /* Custom Alert */
    .custom-alert {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 5px solid;
    }
    .alert-warning {
        background-color: rgba(243, 156, 18, 0.15);
        border-left-color: #f39c12;
        color: #f39c12;
    }
    .alert-success {
        background-color: rgba(46, 204, 113, 0.15);
        border-left-color: #2ecc71;
        color: #2ecc71;
    }
    
    /* Coin Badges */
    .coin-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 12px;
        font-weight: bold;
        color: white;
        font-size: 0.85rem;
        text-align: center;
    }
    .badge-1dh { background-color: #cd7f32; }
    .badge-2dh { background-color: #a0acb9; color: #1a1a1a; }
    .badge-5dh { background-color: #d4af37; }
    .badge-10dh { background-color: #e08c44; }
    
    /* Table styles */
    .table-container {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }
    .table-container th {
        background-color: #1f2326;
        color: #d4af37;
        font-weight: 600;
        padding: 10px;
        border-bottom: 2px solid #2d3238;
        text-align: left;
    }
    .table-container td {
        padding: 12px 10px;
        border-bottom: 1px solid #2d3238;
    }
    
    /* Sidebar Details */
    .sidebar-info {
        background-color: #1f2326;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2d3238;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation du détecteur (chargement du modèle)
@st.cache_resource
def get_detector():
    return CoinsDetector(model_path="models/best.pt")

detector = get_detector()

# --- HEADER DE L'APPLICATION ---
st.markdown("""
    <div class="header-container">
        <div class="header-title">🪙 Moroccan Coins Detection & Amount Calculator</div>
        <div class="header-subtitle">Projet Académique • Traitement d'Images & Deep Learning YOLOv8</div>
    </div>
""", unsafe_allow_html=True)

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
        st.markdown("""
            <div class="custom-alert alert-success">
                <strong>✓ YOLOv8 Actif</strong><br>
                Modèle de production (best.pt) chargé et opérationnel.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="custom-alert alert-warning">
                <strong>⚠️ Mode Simulation</strong><br>
                Fichier <code>models/best.pt</code> manquant. Détections simulées activées pour démonstration.
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 📘 Guide des Pièces")
    st.markdown("""
    *   **1 DH** : <span class="coin-badge badge-1dh">1 DH</span> Argentée, Cupro-Nickel.
    *   **2 DH** : <span class="coin-badge badge-2dh">2 DH</span> Argentée, Cupro-Nickel (plus grande).
    *   **5 DH** : <span class="coin-badge badge-5dh">5 DH</span> Bicolore (cœur doré, anneau argenté).
    *   **10 DH** : <span class="coin-badge badge-10dh">10 DH</span> Bicolore (cœur argenté, anneau doré).
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-info">
        <strong>Fiche Projet :</strong><br>
        • Annotation : Roboflow<br>
        • Entraînement : Google Colab<br>
        • Détecteur : YOLOv8
    </div>
    """, unsafe_allow_html=True)

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
        
        with col_img:
            st.markdown("### 🖼️ Image Originale")
            st.image(image, use_container_width=True)
            
            # Bouton de lancement de la détection
            detect_btn = st.button("🚀 Détecter les pièces", use_container_width=True, type="primary")
            
        with col_stats:
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
                
            # Rafraîchir les colonnes avec les résultats
            with col_img:
                st.markdown("### 🎯 Image Annotée")
                st.image(annotated_image, use_container_width=True)
                
                # Bouton de téléchargement de l'image annotée
                # Convertir en bytes pour streamlit
                from io import BytesIO
                buffered = BytesIO()
                annotated_image.save(buffered, format="PNG")
                img_bytes = buffered.getvalue()
                
                st.download_button(
                    label="💾 Télécharger l'image annotée",
                    data=img_bytes,
                    file_name=f"detected_coins_{uploaded_file.name}",
                    mime="image/png",
                    use_container_width=True
                )
                
            with col_stats:
                st.markdown("### 📊 Résultats de l'Analyse")
                
                # Notification de simulation si applicable
                if is_mock:
                    st.warning("⚠️ **Mode Démo actif :** Les résultats ci-dessous sont simulés car aucun modèle réel n'est présent dans `models/best.pt`.")
                else:
                    st.success("✅ Détection effectuée avec succès avec le modèle YOLOv8 !")
                
                # Affichage du montant total dans la carte premium
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Montant Total Calculé</div>
                        <div class="metric-value">{format_currency(total)}</div>
                        <div class="metric-label">{len(detections)} pièces détectées au total</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Tableau récapitulatif détaillé des comptages
                st.markdown("#### Détail par type de pièce :")
                
                t_1 = counts["coin_1dh"]
                t_2 = counts["coin_2dh"]
                t_5 = counts["coin_5dh"]
                t_10 = counts["coin_10dh"]
                
                st.markdown(f"""
                    <table class="table-container">
                        <tr>
                            <th>Pièce</th>
                            <th>Description</th>
                            <th>Quantité</th>
                            <th>Sous-total</th>
                        </tr>
                        <tr>
                            <td><span class="coin-badge badge-1dh">1 DH</span></td>
                            <td>1 Dirham (Bronze)</td>
                            <td><strong>{t_1}</strong></td>
                            <td>{format_currency(t_1 * 1.0)}</td>
                        </tr>
                        <tr>
                            <td><span class="coin-badge badge-2dh">2 DH</span></td>
                            <td>2 Dirhams (Argenté)</td>
                            <td><strong>{t_2}</strong></td>
                            <td>{format_currency(t_2 * 2.0)}</td>
                        </tr>
                        <tr>
                            <td><span class="coin-badge badge-5dh">5 DH</span></td>
                            <td>5 Dirhams (Doré/Argenté)</td>
                            <td><strong>{t_5}</strong></td>
                            <td>{format_currency(t_5 * 5.0)}</td>
                        </tr>
                        <tr>
                            <td><span class="coin-badge badge-10dh">10 DH</span></td>
                            <td>10 Dirhams (Argenté/Doré)</td>
                            <td><strong>{t_10}</strong></td>
                            <td>{format_currency(t_10 * 10.0)}</td>
                        </tr>
                        <tr style="border-top: 2px solid #d4af37; background-color: rgba(212, 175, 55, 0.05);">
                            <td colspan="2"><strong>TOTAL</strong></td>
                            <td><strong>{len(detections)}</strong></td>
                            <td><strong>{format_currency(total)}</strong></td>
                        </tr>
                    </table>
                """, unsafe_allow_html=True)
                
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
