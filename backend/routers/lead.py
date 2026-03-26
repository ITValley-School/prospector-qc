from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from data.connections.database import get_db
from services.lead_service import listar_por_prospection, buscar

router = APIRouter(prefix="/api/leads", tags=["leads"])


@router.get("/prospection/{prospection_id}")
def listar_leads(prospection_id: str, db: Session = Depends(get_db)):
    return listar_por_prospection(db, prospection_id)


@router.get("/{lead_id}")
def buscar_lead(lead_id: str, db: Session = Depends(get_db)):
    result = buscar(db, lead_id)
    if not result:
        raise HTTPException(status_code=404, detail="Lead nao encontrado")
    return result
