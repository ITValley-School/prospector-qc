import os
from sqlalchemy.orm import Session

from models.prospection import Prospection
from models.lead import Lead
from models.lead_contact import LeadContact
from factories.prospection_factory import criar_prospection, montar_prompt_prospeccao
from factories.lead_factory import parsear_resultado_ia, criar_lead_from_dict, criar_contatos_from_dict
from mappers.prospection_mapper import para_criar_response, para_resumo, para_detalhe

TENANT_ID = os.getenv("TENANT_ID", "prospector-qc")


def criar(db: Session, request) -> dict:
    model = criar_prospection(
        titulo=request.titulo,
        segmento=request.segmento,
        localizacao=request.localizacao,
        quantidade_leads=request.quantidade_leads,
        prompt_customizado=request.prompt_customizado,
        engine_tipo=request.engine_tipo,
        tenant_id=TENANT_ID,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return para_criar_response(model)


def listar(db: Session) -> list:
    items = (
        db.query(Prospection)
        .filter(Prospection.tenant_id == TENANT_ID)
        .order_by(Prospection.criado_em.desc())
        .all()
    )
    return [para_resumo(item) for item in items]


def buscar(db: Session, prospection_id: str):
    model = (
        db.query(Prospection)
        .filter(Prospection.id == prospection_id, Prospection.tenant_id == TENANT_ID)
        .first()
    )
    if not model:
        return None

    leads = (
        db.query(Lead)
        .filter(Lead.prospection_id == prospection_id, Lead.tenant_id == TENANT_ID)
        .order_by(Lead.score.desc())
        .all()
    )
    return para_detalhe(model, leads)


def buscar_model(db: Session, prospection_id: str):
    return (
        db.query(Prospection)
        .filter(Prospection.id == prospection_id, Prospection.tenant_id == TENANT_ID)
        .first()
    )


def atualizar_status(db: Session, prospection_id: str, status: str, **kwargs):
    model = buscar_model(db, prospection_id)
    if not model:
        return None
    model.status = status
    for key, value in kwargs.items():
        if hasattr(model, key):
            setattr(model, key, value)
    db.commit()
    db.refresh(model)
    return model


def processar_resultado(db: Session, prospection_id: str, resultado_raw: str):
    """Parseia resultado da IA, cria leads e contatos no banco."""
    model = buscar_model(db, prospection_id)
    if not model:
        raise ValueError("Prospection nao encontrada")

    dados = parsear_resultado_ia(resultado_raw, prospection_id, TENANT_ID)

    leads_criados = 0
    for item in dados:
        lead = criar_lead_from_dict(item, model.id, TENANT_ID)
        db.add(lead)
        db.flush()

        contatos_data = item.get("contatos", [])
        if contatos_data:
            contatos = criar_contatos_from_dict(contatos_data, lead.id, TENANT_ID)
            db.add_all(contatos)

        leads_criados += 1

    model.resultado_raw = resultado_raw
    model.total_leads_encontrados = leads_criados
    model.status = "concluido"
    db.commit()

    return leads_criados


def deletar(db: Session, prospection_id: str) -> bool:
    model = buscar_model(db, prospection_id)
    if not model:
        return False
    db.delete(model)
    db.commit()
    return True
