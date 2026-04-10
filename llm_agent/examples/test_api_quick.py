#!/usr/bin/env python3
"""
Test rapide de la connexion API OpenAI
"""
import os
import sys
from dotenv import load_dotenv

# Charger les variables d'env depuis .env
load_dotenv()

# Faire un test simple
print("\n" + "=" * 60)
print("🧪 TEST RAPIDE OPENAI")
print("=" * 60)

# Vérifier la clé
api_key = os.getenv("OPEN_API_KEY")  # Attention : c'est OPEN_API_KEY pas OPENAI_API_KEY

if not api_key:
    print("❌ ERREUR : Clé API non trouvée dans .env")
    print("   Assurez-vous que OPEN_API_KEY est défini")
    sys.exit(1)

print(f"✅ Clé trouvée : {api_key[:20]}...{api_key[-10:]}")

# Test d'import
try:
    from openai import OpenAI
    print("✅ Librairie OpenAI importée avec succès")
except ImportError as e:
    print(f"❌ Erreur d'import : {e}")
    sys.exit(1)

# Test de connexion
try:
    client = OpenAI(api_key=api_key)
    print("✅ Client OpenAI initialisé")
    
    # Appel simple
    print("\n⏳ Appel API en cours...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es un expert en sécurité routière."},
            {"role": "user", "content": "Qu'est-ce qu'un feu tricolore en une phrase ?"}
        ],
        temperature=0.7,
        max_tokens=50
    )
    
    print("✅ Réponse reçue !")
    print(f"\n📝 Réponse LLM :")
    print(f"   {response.choices[0].message.content}")
    print(f"\n📊 Stats :")
    print(f"   Tokens : {response.usage.total_tokens}")
    print(f"   Coût estimé : ${response.usage.total_tokens * 0.0000007:.6f}")
    
    print("\n" + "=" * 60)
    print("🎉 SUCCÈS ! L'API OpenAI fonctionne parfaitement !")
    print("=" * 60 + "\n")
    
except Exception as e:
    print(f"❌ Erreur lors de l'appel API : {e}")
    sys.exit(1)
