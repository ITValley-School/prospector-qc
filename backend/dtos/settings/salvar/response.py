from pydantic import BaseModel


class SalvarSettingResponse(BaseModel):
    id: str
    chave: str
    valor: str
