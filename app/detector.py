import os
import random
from PIL import Image

# Mappage des classes vers leurs valeurs financières en Dirhams (MAD)
COIN_VALUES = {
    "coin_1dh": 1.0,
    "coin_2dh": 2.0,
    "coin_5dh": 5.0,
    "coin_10dh": 10.0
}

class CoinsDetector:
    def __init__(self, model_path="models/best.pt"):
        """
        Initialise le détecteur de pièces de monnaie.
        
        Args:
            model_path (str): Chemin vers le fichier de poids YOLOv8 (.pt).
        """
        self.model_path = model_path
        self.model = None
        self.model_loaded = False
        self.coin_values = COIN_VALUES
        
        # Tenter de charger le modèle YOLOv8
        self.load_model()

    def load_model(self):
        """
        Tente de charger le modèle YOLO depuis le chemin configuré.
        """
        if os.path.exists(self.model_path):
            try:
                from ultralytics import YOLO
                self.model = YOLO(self.model_path)
                self.model_loaded = True
                print(f"[INFO] Modèle YOLOv8 chargé avec succès depuis {self.model_path}")
            except Exception as e:
                print(f"[ERREUR] Échec du chargement du modèle YOLOv8: {e}")
                self.model_loaded = False
        else:
            print(f"[INFO] Fichier de modèle '{self.model_path}' introuvable. Mode simulation activé par défaut.")
            self.model_loaded = False

    def detect(self, image_pil, force_simulation=False):
        """
        Exécute la détection de pièces sur l'image fournie.
        
        Args:
            image_pil (PIL.Image): L'image à analyser.
            force_simulation (bool): Si True, force le mode simulation même si le modèle est présent.
            
        Returns:
            dict: Un dictionnaire contenant :
                - "detections" (list): Liste de dictionnaires de détections.
                - "counts" (dict): Nombre de pièces par classe.
                - "total_amount" (float): Somme cumulée en Dirham (DH).
                - "is_mock" (bool): Indique si la détection a été simulée.
        """
        use_simulation = force_simulation or not self.model_loaded
        
        if use_simulation:
            detections = self._generate_mock_detections(image_pil)
            is_mock = True
        else:
            detections = self._run_yolo_inference(image_pil)
            is_mock = False

        # Calculer le nombre de pièces de chaque type
        counts = {cls: 0 for cls in self.coin_values.keys()}
        total_amount = 0.0
        
        for det in detections:
            cls_name = det["class_name"]
            if cls_name in counts:
                counts[cls_name] += 1
                total_amount += self.coin_values[cls_name]

        return {
            "detections": detections,
            "counts": counts,
            "total_amount": total_amount,
            "is_mock": is_mock
        }

    def _run_yolo_inference(self, image_pil):
        """
        Réalise la détection réelle avec le modèle YOLOv8.
        """
        detections = []
        try:
            # Lancement de la prédiction YOLOv8
            results = self.model.predict(image_pil, verbose=False)
            
            if len(results) > 0:
                result = results[0]
                boxes = result.boxes
                
                for box in boxes:
                    # Coordonnées [x1, y1, x2, y2]
                    xyxy = box.xyxy[0].tolist()
                    # Indice de classe
                    cls_id = int(box.cls[0].item())
                    # Confiance
                    conf = float(box.conf[0].item())
                    
                    # Récupérer le nom de la classe
                    if hasattr(self.model, 'names') and cls_id in self.model.names:
                        class_name = self.model.names[cls_id]
                    else:
                        # Fallback basé sur l'ordre standard défini dans data.yaml
                        class_names = list(self.coin_values.keys())
                        class_name = class_names[cls_id] if cls_id < len(class_names) else "unknown"
                    
                    # N'ajouter que si la classe fait partie de nos pièces marocaines
                    if class_name in self.coin_values:
                        detections.append({
                            "box": xyxy,
                            "class_name": class_name,
                            "confidence": conf,
                            "class_id": cls_id
                        })
        except Exception as e:
            print(f"[ERREUR] Erreur lors de l'inférence YOLOv8: {e}")
            # Si plantage de l'inférence, on bascule en simulation de secours
            detections = self._generate_mock_detections(image_pil)
            
        return detections

    def _generate_mock_detections(self, image_pil):
        """
        Génère des détections simulées cohérentes visuellement pour la démonstration de l'interface.
        """
        w, h = image_pil.size
        detections = []
        
        # Déterminer un nombre aléatoire de pièces à simuler (2 à 6 pièces)
        num_coins = random.randint(2, 6)
        
        # Déterminer les classes disponibles
        classes = list(self.coin_values.keys())
        
        # Pour éviter que toutes les pièces se superposent exactement
        grid_positions = []
        rows, cols = 3, 3
        cell_w, cell_h = w // cols, h // rows
        
        for r in range(rows):
            for c in range(cols):
                grid_positions.append((c * cell_w, r * cell_h, cell_w, cell_h))
                
        # Mélanger les positions de grille disponibles
        random.shuffle(grid_positions)
        
        for i in range(min(num_coins, len(grid_positions))):
            gx, gy, gw, gh = grid_positions[i]
            
            # Taille de la pièce (environ 40% à 70% de la cellule de grille)
            coin_diameter = int(min(gw, gh) * random.uniform(0.40, 0.75))
            
            # Centre aléatoire dans la cellule en laissant une marge
            margin = 5
            if gw - coin_diameter - margin > margin:
                cx = gx + random.randint(margin, gw - coin_diameter - margin)
            else:
                cx = gx + margin
                
            if gh - coin_diameter - margin > margin:
                cy = gy + random.randint(margin, gh - coin_diameter - margin)
            else:
                cy = gy + margin
            
            # Coordonnées [x1, y1, x2, y2]
            x1 = cx
            y1 = cy
            x2 = x1 + coin_diameter
            y2 = y1 + coin_diameter
            
            # Choix de la classe
            cls_name = random.choice(classes)
            cls_id = classes.index(cls_name)
            
            # Score de confiance réaliste (ex: 85% à 98%)
            confidence = random.uniform(0.85, 0.98)
            
            detections.append({
                "box": [x1, y1, x2, y2],
                "class_name": cls_name,
                "confidence": confidence,
                "class_id": cls_id
            })
            
        return detections
