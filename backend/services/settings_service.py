import os
from sqlalchemy.orm import Session

from models.setting import Setting

TENANT_ID = os.getenv("TENANT_ID", "prospector-qc")


def salvar(db: Session, request):
    existing = (
        db.query(Setting)
        .filter(Setting.chave == request.chave, Setting.tenant_id == TENANT_ID)
        .first()
    )

    if existing:
        existing.valor = request.valor
        db.commit()
        db.refresh(existing)
        return {"id": str(existing.id), "chave": existing.chave, "valor": existing.valor}

    model = Setting(
        tenant_id=TENANT_ID,
        chave=request.chave,
        valor=request.valor,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return {"id": str(model.id), "chave": model.chave, "valor": model.valor}


def buscar(db: Session, chave: str):
    model = (
        db.query(Setting)
        .filter(Setting.chave == chave, Setting.tenant_id == TENANT_ID)
        .first()
    )
    if not model:
        return None
    return {"id": str(model.id), "chave": model.chave, "valor": model.valor}


def listar(db: Session) -> list:
    items = (
        db.query(Setting)
        .filter(Setting.tenant_id == TENANT_ID)
        .all()
    )
    return [{"id": str(s.id), "chave": s.chave, "valor": s.valor} for s in items]
