import json

from models.lead import Lead
from models.lead_contact import LeadContact


def parsear_resultado_ia(resultado_raw: str, prospection_id, tenant_id: str) -> list[dict]:
    """Parseia o resultado raw da IA e retorna lista de dicts com lead + contatos."""
    texto = resultado_raw.strip()

    # Tenta extrair JSON de dentro de markdown code blocks
    if "```json" in texto:
        texto = texto.split("```json")[1].split("```")[0].strip()
    elif "```" in texto:
        texto = texto.split("```")[1].split("```")[0].strip()

    # Tenta encontrar o array JSON
    inicio = texto.find("[")
    fim = texto.rfind("]")
    if inicio == -1 or fim == -1:
        raise ValueError("Resultado da IA nao contem um JSON array valido")

    texto_json = texto[inicio:fim + 1]
    dados = json.loads(texto_json)

    if not isinstance(dados, list):
        raise ValueError("Resultado da IA nao e um array")

    return dados


def criar_lead_from_dict(data: dict, prospection_id, tenant_id: str) -> Lead:
    return Lead(
        tenant_id=tenant_id,
        prospection_id=prospection_id,
        nome_empresa=data.get("nome_empresa", "Sem nome"),
        segmento=data.get("segmento"),
        website=data.get("website"),
        descricao=data.get("descricao"),
        score=float(data.get("score", 0)),
        status="novo",
    )


def criar_contatos_from_dict(contatos_data: list[dict], lead_id, tenant_id: str) -> list[LeadContact]:
    contatos = []
    for c in contatos_data:
        contato = LeadContact(
            tenant_id=tenant_id,
            lead_id=lead_id,
            nome=c.get("nome"),
            cargo=c.get("cargo"),
            email=c.get("email"),
            telefone=c.get("telefone"),
            linkedin=c.get("linkedin"),
        )
        contatos.append(contato)
    return contatos
