from sqlalchemy import Column, Integer, String, Text, Float
from app.core.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    empresa = Column(String(100))
    whatsapp = Column(String(30))
    dor_principal = Column(Text)
    interesse = Column(Text)
    lead_score = Column(Float)
    status = Column(String(20))
    resumo_ia = Column(Text)
    origem = Column(String(50))
