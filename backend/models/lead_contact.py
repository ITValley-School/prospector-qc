import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from data.connections.database import Base


class LeadContact(Base):
    __tablename__ = "lead_contacts"
    __table_args__ = {"schema": "prospector"}

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="prospector-qc")
    lead_id = Column(UNIQUEIDENTIFIER, ForeignKey("prospector.leads.id"), nullable=False)
    nome = Column(String(200))
    cargo = Column(String(200))
    email = Column(String(300))
    telefone = Column(String(50))
    linkedin = Column(String(500))
    criado_em = Column(DateTime, nullable=False, server_default=func.now())
