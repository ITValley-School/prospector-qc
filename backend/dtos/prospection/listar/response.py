from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProspectionResumo(BaseModel):
    id: str
    titulo: str
    segmento: str
    localizacao: Optional[str] = None
    engine_tipo: str
    status: str
    total_leads_encontrados: int = 0
    criado_em: datetime
