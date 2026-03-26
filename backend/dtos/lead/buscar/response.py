from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ContatoDTO(BaseModel):
    id: str
    nome: Optional[str] = None
    cargo: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    linkedin: Optional[str] = None


class BuscarLeadResponse(BaseModel):
    id: str
    prospection_id: str
    nome_empresa: str
    segmento: Optional[str] = None
    website: Optional[str] = None
    descricao: Optional[str] = None
    score: float = 0
    status: str = "novo"
    contatos: List[ContatoDTO] = []
    criado_em: datetime
