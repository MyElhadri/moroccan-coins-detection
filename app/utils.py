import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Palette de couleurs élégantes pour les pièces marocaines (RGB)
CLASS_COLORS = {
    "coin_1dh": (205, 127, 50),     # Bronze / Cuivré
    "coin_2dh": (170, 180, 190),    # Argenté / Gris (Pièce de 2 DH)
    "coin_5dh": (212, 175, 55),     # Doré / Or (Pièce bicolore 5 DH)
    "coin_10dh": (230, 140, 10)     # Cuivré vif / Bicolore (Pièce bicolore 10 DH)
}

def get_color(class_name):
    """
    Retourne la couleur RGB associée à la classe de la pièce.
    """
    return CLASS_COLORS.get(class_name, (128, 128, 128))

def format_currency(amount):
    """
    Formate un montant numérique en Dirham Marocain (DH / MAD).
    """
    if amount % 1 == 0:
        return f"{int(amount)} DH"
    return f"{amount:.2f} DH"

def draw_beautiful_detections(image_pil, detections):
    """
    Dessine des boîtes englobantes et des étiquettes stylisées sur une image PIL.
    Calcule dynamiquement la taille de la police et l'épaisseur des lignes en fonction des dimensions.
    
    Args:
        image_pil (PIL.Image): L'image originale.
        detections (list): Liste de dictionnaires contenant:
            - "box": [x1, y1, x2, y2]
            - "class_name": nom de la classe (ex: 'coin_1dh')
            - "confidence": score de confiance (0.0 à 1.0)
    
    Returns:
        PIL.Image: L'image annotée de manière haut de gamme.
    """
    # Copier l'image pour préserver l'originale
    annotated_image = image_pil.copy()
    draw = ImageDraw.Draw(annotated_image)
    width, height = annotated_image.size
    
    # Calcul dynamique de l'échelle des annotations selon la résolution
    scale = max(1, int(min(width, height) / 800))
    line_thickness = max(2, int(3 * scale))
    font_size = max(11, int(15 * scale))
    
    # Recherche d'une police TrueType système lisible, sinon fallback par défaut
    font = None
    font_names = ["arial.ttf", "calibri.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
    for font_name in font_names:
        try:
            font = ImageFont.truetype(font_name, font_size)
            break
        except IOError:
            continue
            
    if font is None:
        font = ImageFont.load_default()
            
    for det in detections:
        box = det["box"]
        class_name = det["class_name"]
        conf = det["confidence"]
        
        # Coordonnées entières
        x1, y1, x2, y2 = [max(0, int(coord)) for coord in box]
        
        # Obtenir la couleur associée à la classe
        color = get_color(class_name)
        
        # Dessiner le rectangle extérieur (boîte englobante de la pièce)
        draw.rectangle([x1, y1, x2, y2], outline=color, width=line_thickness)
        
        # Préparer le texte (ex: 5DH 98%)
        coin_label = class_name.replace("coin_", "").upper()
        text = f"{coin_label} ({conf:.0%})"
        
        # Récupération de la boîte de texte pour dessiner un arrière-plan à l'étiquette
        try:
            # Pillow >= 8.0.0
            text_bbox = draw.textbbox((x1, y1), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        except AttributeError:
            # Fallback pour anciennes versions de Pillow
            text_width, text_height = draw.textsize(text, font=font)
            
        # Éviter que le label sorte de l'image (si la boîte commence tout en haut)
        label_y = max(y1 - text_height - 6, 0)
        label_x = x1
        
        # Fond de couleur pour le label textuel
        draw.rectangle(
            [label_x, label_y, label_x + text_width + 8, label_y + text_height + 6], 
            fill=color
        )
        
        # Couleur du texte optimisée pour la lisibilité
        text_color = (255, 255, 255)
        if class_name == "coin_2dh": # Gris clair, texte noir préférable
            text_color = (0, 0, 0)
            
        # Écrire le texte
        draw.text((label_x + 4, label_y + 2), text, fill=text_color, font=font)
        
    return annotated_image

def save_prediction(image_pil, predictions_dir="results/predictions"):
    """
    Sauvegarde l'image annotée dans le dossier de prédictions avec un nom unique horodaté.
    
    Args:
        image_pil (PIL.Image): L'image annotée.
        predictions_dir (str): Chemin du répertoire de sauvegarde.
        
    Returns:
        str: Chemin relatif final du fichier sauvegardé.
    """
    if not os.path.exists(predictions_dir):
        os.makedirs(predictions_dir, exist_ok=True)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prediction_{timestamp}.png"
    filepath = os.path.join(predictions_dir, filename)
    image_pil.save(filepath)
    # Retourner en chemin relatif propre pour affichage ou référencement
    return os.path.normpath(os.path.join(predictions_dir, filename))
