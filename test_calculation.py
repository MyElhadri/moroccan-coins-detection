import sys
import os

# Ajouter le répertoire racine au PATH pour des imports sécurisés
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.detector import COIN_VALUES

def test_calculation():
    # Liste de détections simulées (ex: sortie de YOLO)
    mock_detections_classes = ["coin_1dh", "coin_1dh", "coin_1dh", "coin_2dh", "coin_10dh"]
    
    # Créer le format de dictionnaire attendu par notre logique
    detections = [{"class_name": cls} for cls in mock_detections_classes]
    
    # Calcul comme dans detector.py
    counts = {cls: 0 for cls in COIN_VALUES.keys()}
    total_amount = 0.0
    
    for det in detections:
        cls_name = det["class_name"]
        if cls_name in counts:
            counts[cls_name] += 1
            total_amount += COIN_VALUES[cls_name]
            
    # Affichage des résultats
    print("Résultat du test :")
    for cls, count in counts.items():
        if count > 0:
            print(f"{cls}: {count}")
    print(f"Total: {int(total_amount)} DH")
    
if __name__ == "__main__":
    test_calculation()
