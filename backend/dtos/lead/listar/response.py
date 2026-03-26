from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LeadListItem(BaseModel):
    id: str
    prospection_id: str
    nome_empresa: str
    segmento: Optional[str] = None
    website: Optional[str] = None
    score: float = 0
    status: str = "novo"
    criado_em: datetime
