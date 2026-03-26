import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from factories.prospection_factory import criar_prospection, montar_prompt_prospeccao
from factories.lead_factory import parsear_resultado_ia, criar_lead_from_dict


class TestProspectionFactory:
    def test_criar_prospection_valida(self):
        model = criar_prospection(
            titulo="Test",
            segmento="Tech",
            localizacao="SP",
            quantidade_leads=10,
            prompt_customizado=None,
            engine_tipo="claude_code",
            tenant_id="test",
        )
        assert model.titulo == "Test"
        assert model.segmento == "Tech"
        assert model.status == "pendente"

    def test_criar_prospection_titulo_vazio(self):
        with pytest.raises(ValueError, match="Titulo"):
            criar_prospection("", "Tech", "SP", 10, None, "claude_code", "test")

    def test_criar_prospection_segmento_vazio(self):
        with pytest.raises(ValueError, match="Segmento"):
            criar_prospection("Test", "", "SP", 10, None, "claude_code", "test")

    def test_criar_prospection_engine_invalido(self):
        with pytest.raises(ValueError, match="Engine"):
            criar_prospection("Test", "Tech", "SP", 10, None, "invalido", "test")

    def test_criar_prospection_quantidade_invalida(self):
        with pytest.raises(ValueError, match="Quantidade"):
            criar_prospection("Test", "Tech", "SP", 0, None, "claude_code", "test")

        with pytest.raises(ValueError, match="Quantidade"):
            criar_prospection("Test", "Tech", "SP", 100, None, "claude_code", "test")

    def test_montar_prompt_basico(self):
        prompt = montar_prompt_prospeccao("Tech", None, 5, None)
        assert "5" in prompt
        assert "Tech" in prompt
        assert "JSON" in prompt

    def test_montar_prompt_com_localizacao(self):
        prompt = montar_prompt_prospeccao("Tech", "SP", 10, None)
        assert "SP" in prompt

    def test_montar_prompt_com_customizado(self):
        prompt = montar_prompt_prospeccao("Tech", None, 5, "Apenas empresas grandes")
        assert "Apenas empresas grandes" in prompt


class TestLeadFactory:
    def test_parsear_resultado_json_simples(self):
        raw = '[{"nome_empresa": "Test Corp", "segmento": "Tech"}]'
        dados = parsear_resultado_ia(raw, "abc", "test")
        assert len(dados) == 1
        assert dados[0]["nome_empresa"] == "Test Corp"

    def test_parsear_resultado_com_markdown(self):
        raw = '```json\n[{"nome_empresa": "Test Corp"}]\n```'
        dados = parsear_resultado_ia(raw, "abc", "test")
        assert len(dados) == 1

    def test_parsear_resultado_invalido(self):
        with pytest.raises(ValueError):
            parsear_resultado_ia("texto sem json", "abc", "test")

    def test_criar_lead_from_dict(self):
        data = {
            "nome_empresa": "Test Corp",
            "segmento": "Tech",
            "website": "https://test.com",
            "score": 8.5,
        }
        lead = criar_lead_from_dict(data, "abc-123", "test")
        assert lead.nome_empresa == "Test Corp"
        assert lead.score == 8.5
        assert lead.status == "novo"
