"""
test_formatter.py - Tests du ResponseFormatter
Teste le parsing et le formatage des réponses du LLM
"""
import pytest
from llm_agent.formatter import ResponseFormatter


class TestResponseFormatterExtraction:
    """Tests d'extraction des sections de réponse"""
    
    def test_extract_resume(self):
        """Tester l'extraction du résumé"""
        text = """RÉSUMÉ: Ceci est un résumé de test.
RISQUES: Voici les risques
RECOMMANDATIONS: Voici les recommandations"""
        
        resume = ResponseFormatter.extract_resume(text)
        assert resume is not None
        assert "résumé" in resume.lower()
    
    def test_extract_risks(self):
        """Tester l'extraction des risques"""
        text = """RÉSUMÉ: Test
RISQUES: 
- Risque 1
- Risque 2
- Risque 3
RECOMMANDATIONS: Test"""
        
        risks = ResponseFormatter.extract_risks(text)
        assert len(risks) >= 1
    
    def test_extract_recommendations(self):
        """Tester l'extraction des recommandations"""
        text = """RÉSUMÉ: Test
RISQUES: Risques
RECOMMANDATIONS: 
- Recommandation 1
- Recommandation 2
- Recommandation 3"""
        
        recs = ResponseFormatter.extract_recommendations(text)
        assert len(recs) >= 1
    
    def test_extract_with_missing_sections(self):
        """Tester l'extraction quand des sections manquent"""
        text = "Réponse incomplète sans sections structurées"
        
        resume = ResponseFormatter.extract_resume(text)
        risks = ResponseFormatter.extract_risks(text)
        recs = ResponseFormatter.extract_recommendations(text)
        
        assert resume is not None
        assert isinstance(risks, list)
        assert isinstance(recs, list)


class TestResponseFormatterRiskInference:
    """Tests d'inférence du niveau de risque"""
    
    def test_infer_critical_risk(self):
        """Tester l'inférence d'un risque CRITIQUE"""
        text = "Situation critique ! Danger immédiat ! 🚨"
        level = ResponseFormatter.infer_risk_level(text)
        assert level == "CRITIQUE"
    
    def test_infer_high_risk(self):
        """Tester l'inférence d'un risque ÉLEVÉ"""
        text = "Situation avec des risques élevés. Urgent de réduire la vitesse."
        level = ResponseFormatter.infer_risk_level(text)
        assert level == "ÉLEVÉ"
    
    def test_infer_medium_risk(self):
        """Tester l'inférence d'un risque MOYEN"""
        text = "Situation normale avec vigilance requise."
        level = ResponseFormatter.infer_risk_level(text)
        assert level == "MOYEN"
    
    def test_infer_low_risk(self):
        """Tester l'inférence d'un risque FAIBLE"""
        text = "Route dégagée, aucun objet détecté."
        level = ResponseFormatter.infer_risk_level(text)
        assert level == "FAIBLE"


class TestResponseFormatterFormatting:
    """Tests de formatage de réponses complet"""
    
    def test_format_llm_response(self):
        """Tester le formatage complet d'une réponse LLM"""
        text = """RÉSUMÉ: Scène routière dégagée
RISQUES:
- Aucun risque majeur
RECOMMANDATIONS:
- Continuer votre route"""
        
        result = ResponseFormatter.format_llm_response(text)
        
        assert result is not None
        assert result.resume is not None
        assert result.recommandations is not None
        assert result.risque_eval is not None
    
    def test_format_for_display(self):
        """Tester le formatage pour affichage"""
        from pipeline.schema import AnalyseResultat, RisqueEvaluation
        
        analyse = AnalyseResultat(
            resume="Test",
            recommandations=["Rec 1", "Rec 2"],
            risque_eval=RisqueEvaluation(risque_level="MOYEN")
        )
        
        display_format = ResponseFormatter.format_for_display(analyse)
        
        assert display_format is not None
        assert "résumé" in display_format
        assert "niveau_risque" in display_format
        assert "recommandations" in display_format


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
