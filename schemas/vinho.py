from pydantic import BaseModel
from typing import List
from model.vinho import Vinho
from schemas import NotaSchema

# como novo vinho deverá ser adicionado na adega
class VinhoSchema(BaseModel):
    vinho: str = "Cristatus"
    uva: str = "Cabernet Sauvignon"
    ano: int = 2021
    categoria: str = "Fino tinto seco"
    fabricante: str = "SUR ANDINO"


# estrutura que será utilizada na busca por vinhos específicos na adega
class VinhoBuscaSchema(BaseModel):
    vinho: str = "vinho"


#retorna todos os vinhos da adega
class ListagemVinhosSchema(BaseModel):
    vinhos:List[VinhoSchema]


# para que seja possível o retorno referente as informações do vinho em diferentes rotas
def apresenta_vinhos(vinhos: List[Vinho]):
    result = []
    for vinho in vinhos:
        result.append({
            "vinho": vinho.vinho,
            "uva": vinho.uva,
            "ano": vinho.ano,
            "categoria": vinho.categoria,
            "fabricante": vinho.fabricante,
        })
    return {"vinhos": result}


# todas as informações do vinho, incluindo dados de ambas tabelas
class VinhoViewSchema(BaseModel):
    id: int = 1
    vinho: str = "Cristatus"
    uva: str = "Cabernet Sauvignon"
    ano: int = 2021
    categoria: str = "Fino tinto seco"
    fabricante: str = "SUR ANDINO"
    total_notas: int = 1
    notas:List[NotaSchema]


# estrutura retornada quando um vinho é retirado da adega
class VinhoDelSchema(BaseModel):
    message: str
    vinho: str


# retorna o vinho com todas notas adicionadas
def apresenta_vinho(vinho: Vinho):
    return {
        "id": vinho.id,
        "vinho": vinho.vinho,
        "uva": vinho.uva,
        "ano": vinho.ano,
        "categoria": vinho.categoria,
        "fabricante": vinho.fabricante,
        "total_notas": len(vinho.notas),
        "notas": [{"texto": c.texto} for c in vinho.notas]
    }
