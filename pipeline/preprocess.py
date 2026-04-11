

"""
Pretraitement des images:
Minimal
-Vérifie qu'elles soient ok
"""

def preprocess_image(image):
    image_traitée = image
    
    # Vérifier que l'image est valide
    if image_traitée is None:
        raise ValueError("Image is None")
    
    return image_traitée