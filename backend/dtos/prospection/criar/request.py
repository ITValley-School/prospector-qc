from pydantic import BaseModel
from typing import Optional


class CriarProspectionRequest(BaseModel):
    titulo: str
    segmento: str
    localizacao: Optional[str] = None
    quantidade_leads: int = 10
    prompt_customizado: Optional[str] = None
    engine_tipo: str = "claude_code"
