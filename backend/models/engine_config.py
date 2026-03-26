import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from data.connections.database import Base


class EngineConfig(Base):
    __tablename__ = "engine_configs"
    __table_args__ = {"schema": "prospector"}

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(100), nullable=False, default="prospector-qc")
    engine_tipo = Column(String(50), nullable=False)
    provider = Column(String(50))
    modelo = Column(String(100))
    api_key_ref = Column(String(200))
    ativo = Column(Boolean, nullable=False, default=True)
    config_json = Column(Text)
    criado_em = Column(DateTime, nullable=False, server_default=func.now())
