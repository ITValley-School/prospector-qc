import uuid
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from data.connections.database import Base


class Enrichment(Base):
    __tablename__ = "enrichments"
    __table_args__ = {"schema": "prospector"}

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="prospector-qc")
    lead_id = Column(UNIQUEIDENTIFIER, ForeignKey("prospector.leads.id"), nullable=False)
    fonte = Column(String(100), nullable=False)
    dados = Column(Text)
    status = Column(String(50), nullable=False, default="pendente")
    criado_em = Column(DateTime, nullable=False, server_default=func.now())
