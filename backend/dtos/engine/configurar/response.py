from pydantic import BaseModel
from typing import Optional


class ConfigurarEngineResponse(BaseModel):
    id: str
    engine_tipo: str
    provider: Optional[str] = None
    modelo: Optional[str] = None
    ativo: bool = True
