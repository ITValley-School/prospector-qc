import os
from sqlalchemy.orm import Session

from models.lead import Lead
from models.lead_contact import LeadContact
from mappers.lead_mapper import para_list_item, para_detalhe

TENANT_ID = os.getenv("TENANT_ID", "prospector-qc")


def listar_por_prospection(db: Session, prospection_id: str) -> list:
    items = (
        db.query(Lead)
        .filter(Lead.prospection_id == prospection_id, Lead.tenant_id == TENANT_ID)
        .order_by(Lead.score.desc())
        .all()
    )
    return [para_list_item(item) for item in items]


def buscar(db: Session, lead_id: str):
    model = (
        db.query(Lead)
        .filter(Lead.id == lead_id, Lead.tenant_id == TENANT_ID)
        .first()
    )
    if not model:
        return None

    contatos = (
        db.query(LeadContact)
        .filter(LeadContact.lead_id == lead_id, LeadContact.tenant_id == TENANT_ID)
        .all()
    )
    return para_detalhe(model, contatos)
