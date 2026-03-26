from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from data.connections.database import get_db
from dtos.engine.configurar.request import ConfigurarEngineRequest
from services.engine_service import listar, configurar

router = APIRouter(prefix="/api/engines", tags=["engines"])


@router.get("")
def listar_engines(db: Session = Depends(get_db)):
    return listar(db)


@router.post("")
def configurar_engine(request: ConfigurarEngineRequest, db: Session = Depends(get_db)):
    return configurar(db, request)
