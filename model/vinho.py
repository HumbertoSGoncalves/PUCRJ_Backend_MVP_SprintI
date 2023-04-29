from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Nota

# associação implícita de vinhos e notas
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
        
        #Para adicionar vinhos na adega.
        #Descrição dos argumentos da função:
        #    vinho: nome de acordo com o rotulo do vinho.
        #    uva: tipo de uva utilizada na producao do vinho (Cabernet Sauvignon, Tannah, Merlot, etc).
        #    ano: ano de producao do vinho.
        #    categoria: a categoria do vinho, se se trata de vinho Fino, Reservado, de Mesa, etc.
        #   fabricante: identificacao do produtor do vinho.
        #    data_insercao: data de quando o vinho foi adicionado à adega (adicionada automaticamente).


    #adição de notas aos vinhos da adega.
    def adiciona_nota(self, nota:Nota):
        self.notas.append(nota)
