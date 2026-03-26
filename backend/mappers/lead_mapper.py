from dtos.lead.buscar.response import BuscarLeadResponse, ContatoDTO
from dtos.lead.listar.response import LeadListItem


def para_list_item(model) -> LeadListItem:
    return LeadListItem(
        id=str(model.id),
        prospection_id=str(model.prospection_id),
        nome_empresa=model.nome_empresa,
        segmento=model.segmento,
        website=model.website,
        score=model.score or 0,
        status=model.status,
        criado_em=model.criado_em,
    )


def para_detalhe(model, contatos=None) -> BuscarLeadResponse:
    contatos_dto = []
    if contatos:
        contatos_dto = [
            ContatoDTO(
                id=str(c.id),
                nome=c.nome,
                cargo=c.cargo,
                email=c.email,
                telefone=c.telefone,
                linkedin=c.linkedin,
            )
            for c in contatos
        ]

    return BuscarLeadResponse(
        id=str(model.id),
        prospection_id=str(model.prospection_id),
        nome_empresa=model.nome_empresa,
        segmento=model.segmento,
        website=model.website,
        descricao=model.descricao,
        score=model.score or 0,
        status=model.status,
        contatos=contatos_dto,
        criado_em=model.criado_em,
    )
