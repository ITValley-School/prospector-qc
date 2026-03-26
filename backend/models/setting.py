import uuid
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from data.connections.database import Base


class Setting(Base):
    __tablename__ = "settings"
    __table_args__ = {"schema": "prospector"}

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="prospector-qc")
    chave = Column(String(200), nullable=False)
    valor = Column(Text)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())
    atualizado_em = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
