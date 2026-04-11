"""
test_api_openai.py - Test de la connexion à l'API OpenAI
Vérifie que la clé API est configurée et que la connexion fonctionne
"""
import os
import pytest

# NOTE: Do NOT call load_dotenv() here! It would override test environment
# conftest.py will handle loading .env in the right context


class TestOpenAIConnection:
    """Tests de connexion à l'API OpenAI"""
    
    @pytest.mark.api
    def test_api_key_exists(self):
        """Vérifier que la clé API est définie"""
        api_key = os.getenv("OPEN_API_KEY")
        if not api_key:
            pytest.skip("API key not configured")
        assert api_key.startswith("sk-"), "Clé API invalide (doit commencer par sk-)"
    
    def test_openai_import(self):
        """Vérifier que openai peut être importé"""
        from openai import OpenAI
        assert OpenAI is not None
    
    @pytest.mark.api
    def test_openai_client_initialization(self):
        """Vérifier que le client OpenAI peut être initialisé"""
        api_key = os.getenv("OPEN_API_KEY")
        if not api_key:
            pytest.skip("API key not configured")
        
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        assert client is not None
    
    @pytest.mark.api
    @pytest.mark.slow
    def test_openai_api_call(self):
        """Test d'appel réel à l'API OpenAI"""
        api_key = os.getenv("OPEN_API_KEY")
        if not api_key:
            pytest.skip("API key not configured")
        
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un expert en sécurité routière."},
                {"role": "user", "content": "Qu'est-ce qu'un feu tricolore ?"}
            ],
            temperature=0.7,
            max_tokens=50
        )
        
        assert response is not None
        assert response.choices is not None
        assert len(response.choices) > 0
        assert response.choices[0].message.content is not None
        assert response.usage.total_tokens > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
