from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class LeadResumoDTO(BaseModel):
    id: str
    nome_empresa: str
    segmento: Optional[str] = None
    website: Optional[str] = None
    score: float = 0
    status: str = "novo"


class BuscarProspectionResponse(BaseModel):
    id: str
    titulo: str
    segmento: str
    localizacao: Optional[str] = None
    quantidade_leads: int
    prompt_customizado: Optional[str] = None
    engine_tipo: str
    status: str
    total_leads_encontrados: int = 0
    erro: Optional[str] = None
    arquivo_export_url: Optional[str] = None
    leads: List[LeadResumoDTO] = []
    criado_em: datetime
    atualizado_em: datetime
