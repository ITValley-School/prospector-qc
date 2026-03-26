from pydantic import BaseModel
from typing import Optional


class ConfigurarEngineRequest(BaseModel):
    engine_tipo: str
    provider: Optional[str] = None
    modelo: Optional[str] = None
    api_key_ref: Optional[str] = None
    config_json: Optional[str] = None
