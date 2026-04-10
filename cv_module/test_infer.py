import os

# Ce fichier permet de tester le module d'inférence sur plusieurs images afin de vérifier que les détections sont bien retournées au format attendu

folder = "cv_module/test_images"


def main() -> None:
    # Evite une erreur si le dossier de test n'est pas present sur une autre machine ou en CI.
    if not os.path.isdir(folder):
        print(f"Dossier introuvable : {folder}")
        return

    from cv_module.infer import run_inference

    for img in sorted(os.listdir(folder)):
        if img.endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(folder, img)
            print(f"\n--- {img} ---")
            print(run_inference(path))


if __name__ == "__main__":
    main()
