from dtos.prospection.criar.response import CriarProspectionResponse
from dtos.prospection.listar.response import ProspectionResumo
from dtos.prospection.buscar.response import BuscarProspectionResponse, LeadResumoDTO


def para_criar_response(model) -> CriarProspectionResponse:
    return CriarProspectionResponse(
        id=str(model.id),
        titulo=model.titulo,
        segmento=model.segmento,
        engine_tipo=model.engine_tipo,
        status=model.status,
        criado_em=model.criado_em,
    )


def para_resumo(model) -> ProspectionResumo:
    return ProspectionResumo(
        id=str(model.id),
        titulo=model.titulo,
        segmento=model.segmento,
        localizacao=model.localizacao,
        engine_tipo=model.engine_tipo,
        status=model.status,
        total_leads_encontrados=model.total_leads_encontrados or 0,
        criado_em=model.criado_em,
    )


def para_detalhe(model, leads=None) -> BuscarProspectionResponse:
    leads_dto = []
    if leads:
        leads_dto = [
            LeadResumoDTO(
                id=str(l.id),
                nome_empresa=l.nome_empresa,
                segmento=l.segmento,
                website=l.website,
                score=l.score or 0,
                status=l.status,
            )
            for l in leads
        ]

    return BuscarProspectionResponse(
        id=str(model.id),
        titulo=model.titulo,
        segmento=model.segmento,
        localizacao=model.localizacao,
        quantidade_leads=model.quantidade_leads,
        prompt_customizado=model.prompt_customizado,
        engine_tipo=model.engine_tipo,
        status=model.status,
        total_leads_encontrados=model.total_leads_encontrados or 0,
        erro=model.erro,
        arquivo_export_url=model.arquivo_export_url,
        leads=leads_dto,
        criado_em=model.criado_em,
        atualizado_em=model.atualizado_em,
    )
