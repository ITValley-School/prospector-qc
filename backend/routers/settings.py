from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from data.connections.database import get_db
from dtos.settings.salvar.request import SalvarSettingRequest
from services.settings_service import salvar, buscar, listar

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("")
def listar_settings(db: Session = Depends(get_db)):
    return listar(db)


@router.post("")
def salvar_setting(request: SalvarSettingRequest, db: Session = Depends(get_db)):
    return salvar(db, request)


@router.get("/{chave}")
def buscar_setting(chave: str, db: Session = Depends(get_db)):
    result = buscar(db, chave)
    if not result:
        raise HTTPException(status_code=404, detail="Setting nao encontrada")
    return result
