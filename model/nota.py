from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union
from  model import Base

# Relationship between notes and wines.
class Nota(Base):
    __tablename__ = 'nota'
    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())
    vinho = Column(Integer, ForeignKey("vinho.pk_vinho"), nullable=False)

    # Creates a note with the insertion date.
    def __init__(self, texto:str, data_insercao:Union[DateTime, None] = None):
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
