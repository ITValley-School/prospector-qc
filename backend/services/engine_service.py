import os
from sqlalchemy.orm import Session

from models.engine_config import EngineConfig
from mappers.engine_mapper import para_dto, para_configurar_response

TENANT_ID = os.getenv("TENANT_ID", "prospector-qc")


def listar(db: Session) -> list:
    items = (
        db.query(EngineConfig)
        .filter(EngineConfig.tenant_id == TENANT_ID)
        .all()
    )
    return [para_dto(item) for item in items]


def configurar(db: Session, request):
    existing = (
        db.query(EngineConfig)
        .filter(
            EngineConfig.engine_tipo == request.engine_tipo,
            EngineConfig.tenant_id == TENANT_ID,
        )
        .first()
    )

    if existing:
        existing.provider = request.provider
        existing.modelo = request.modelo
        existing.api_key_ref = request.api_key_ref
        existing.config_json = request.config_json
        existing.ativo = True
        db.commit()
        db.refresh(existing)
        return para_configurar_response(existing)

    model = EngineConfig(
        tenant_id=TENANT_ID,
        engine_tipo=request.engine_tipo,
        provider=request.provider,
        modelo=request.modelo,
        api_key_ref=request.api_key_ref,
        config_json=request.config_json,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return para_configurar_response(model)
