import os
from cv_module.infer import run_inference

# Ce fichier permet de tester le module d'inférence sur plusieurs images afin de vérifier que les détections sont bien retournées au format attendu

folder = "cv_module/test_images"

for img in sorted(os.listdir(folder)):
    if img.endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(folder, img)
        print(f"\n--- {img} ---")
        print(run_inference(path))
