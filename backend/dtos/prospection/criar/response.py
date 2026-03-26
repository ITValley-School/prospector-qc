from pydantic import BaseModel
from datetime import datetime


class CriarProspectionResponse(BaseModel):
    id: str
    titulo: str
    segmento: str
    engine_tipo: str
    status: str
    criado_em: datetime
