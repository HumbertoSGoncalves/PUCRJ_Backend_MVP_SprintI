from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Nota

# Implicit association of wines and notes.
class Vinho(Base):
    __tablename__ = 'vinho'

    id = Column("pk_vinho", Integer, primary_key=True)
    vinho = Column(String(140), unique=True)
    uva = Column(String(140))
    ano = Column(Integer)
    categoria = Column(String(140))
    fabricante = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())
    notas = relationship("Nota")


    def __init__(self, vinho:str, uva:str, ano:int, categoria:str, fabricante:str,
                data_insercao:Union[DateTime, None] = None):
        self.vinho = vinho
        self.uva = uva
        self.ano = ano
        self.categoria = categoria
        self.fabricante = fabricante

        if data_insercao:
            self.data_insercao = data_insercao
        
        # To add wines to the cellar:
        #    vinho: name according to the wine label.
        #    uva: type of grape used in wine production (e.g., Cabernet Sauvignon, Tannat, Merlot).
        #    ano: the year of the wine's production.
        #    categoria: category of the wine, such as Fine, Reserved, Table, etc.
        #    fabricante: identification of the wine producer.
        #    data_insercao: the date when the wine was added to the cellar (added automatically).


    #adding notes to the wines of the cellar.
    def adiciona_nota(self, nota:Nota):
        self.notas.append(nota)
