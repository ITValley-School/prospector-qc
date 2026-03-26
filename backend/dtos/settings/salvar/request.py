from pydantic import BaseModel


class SalvarSettingRequest(BaseModel):
    chave: str
    valor: str
