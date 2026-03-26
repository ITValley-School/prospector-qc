import uuid
from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from data.connections.database import Base


class Prospection(Base):
    __tablename__ = "prospections"
    __table_args__ = {"schema": "prospector"}

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="prospector-qc")
    titulo = Column(String(200), nullable=False)
    segmento = Column(String(200), nullable=False)
    localizacao = Column(String(200))
    quantidade_leads = Column(Integer, nullable=False, default=10)
    prompt_customizado = Column(Text)
    engine_tipo = Column(String(50), nullable=False, default="claude_code")
    status = Column(String(50), nullable=False, default="pendente")
    resultado_raw = Column(Text)
    total_leads_encontrados = Column(Integer, default=0)
    erro = Column(Text)
    arquivo_export_url = Column(String(500))
    criado_em = Column(DateTime, nullable=False, server_default=func.now())
    atualizado_em = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
