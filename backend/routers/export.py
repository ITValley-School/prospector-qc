from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from data.connections.database import get_db
from services.export_service import exportar_leads
from services.prospection_service import atualizar_status

router = APIRouter(prefix="/api/export", tags=["export"])


@router.post("/{prospection_id}")
def exportar(prospection_id: str,
             formato: str = Query("csv", regex="^(csv|json)$"),
             db: Session = Depends(get_db)):
    try:
        result = exportar_leads(db, prospection_id, formato)
        atualizar_status(db, prospection_id, arquivo_export_url=result["url"],
                         status="exportado")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
