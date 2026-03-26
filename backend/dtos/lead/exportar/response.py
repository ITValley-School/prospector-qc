from pydantic import BaseModel


class ExportarLeadsResponse(BaseModel):
    url: str
    formato: str
    total_leads: int
