from pydantic import BaseModel
from typing import Optional


class BuscarSettingResponse(BaseModel):
    id: str
    chave: str
    valor: Optional[str] = None
