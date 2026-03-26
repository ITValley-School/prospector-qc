import uuid
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from data.connections.database import Base


class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = {"schema": "prospector"}

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="prospector-qc")
    prospection_id = Column(UNIQUEIDENTIFIER, ForeignKey("prospector.prospections.id"), nullable=False)
    nome_empresa = Column(String(300), nullable=False)
    segmento = Column(String(200))
    website = Column(String(500))
    descricao = Column(Text)
    score = Column(Float, default=0)
    status = Column(String(50), nullable=False, default="novo")
    criado_em = Column(DateTime, nullable=False, server_default=func.now())
