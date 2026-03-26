from models.prospection import Prospection

ENGINES_VALIDOS = ["claude_code", "ai_api"]
QUANTIDADE_MAX_LEADS = 50


def criar_prospection(titulo: str, segmento: str, localizacao: str | None,
                       quantidade_leads: int, prompt_customizado: str | None,
                       engine_tipo: str, tenant_id: str) -> Prospection:
    if not titulo or not titulo.strip():
        raise ValueError("Titulo e obrigatorio")

    if not segmento or not segmento.strip():
        raise ValueError("Segmento e obrigatorio")

    if engine_tipo not in ENGINES_VALIDOS:
        raise ValueError(f"Engine invalido. Validos: {ENGINES_VALIDOS}")

    if quantidade_leads < 1 or quantidade_leads > QUANTIDADE_MAX_LEADS:
        raise ValueError(f"Quantidade de leads deve ser entre 1 e {QUANTIDADE_MAX_LEADS}")

    return Prospection(
        tenant_id=tenant_id,
        titulo=titulo.strip(),
        segmento=segmento.strip(),
        localizacao=localizacao.strip() if localizacao else None,
        quantidade_leads=quantidade_leads,
        prompt_customizado=prompt_customizado,
        engine_tipo=engine_tipo,
        status="pendente",
    )


def montar_prompt_prospeccao(segmento: str, localizacao: str | None,
                              quantidade: int, customizado: str | None) -> str:
    prompt = (
        f'Voce e um especialista em prospeccao B2B. Encontre {quantidade} '
        f'empresas reais do segmento "{segmento}"'
    )

    if localizacao:
        prompt += f' localizadas em "{localizacao}"'

    prompt += """.

Para cada empresa, retorne um JSON array com objetos contendo:
- nome_empresa: nome completo da empresa
- segmento: segmento de atuacao
- website: URL do site oficial
- descricao: breve descricao da empresa (2-3 frases)
- score: nota de 0 a 10 indicando relevancia para prospeccao
- contatos: array com objetos contendo nome, cargo, email, telefone, linkedin (quando disponivel)

IMPORTANTE:
- Retorne APENAS o JSON array, sem texto adicional
- Use dados reais e verificaveis
- Priorize empresas de medio e grande porte
- Inclua pelo menos 1 contato por empresa quando possivel"""

    if customizado:
        prompt += f"\n\nInstrucoes adicionais: {customizado}"

    return prompt
