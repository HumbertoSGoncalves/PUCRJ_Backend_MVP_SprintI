from pydantic import BaseModel
from typing import List
from model.vinho import Vinho
from schemas import NotaSchema

# How a new wine should be added to the cellar.
class VinhoSchema(BaseModel):
    vinho: str = "Cristatus"
    uva: str = "Cabernet Sauvignon"
    ano: int = 2021
    categoria: str = "Fino tinto seco"
    fabricante: str = "SUR ANDINO"


# The structure that will be used for searching for specific wines in the cellar.
class VinhoBuscaSchema(BaseModel):
    vinho: str = "vinho"


# retrieves all wines from the cellar.
class ListagemVinhosSchema(BaseModel):
    vinhos:List[VinhoSchema]


# Returns information about the wine through different routes.
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


# All information about the wine, including data from both tables.
class VinhoViewSchema(BaseModel):
    id: int = 1
    vinho: str = "Cristatus"
    uva: str = "Cabernet Sauvignon"
    ano: int = 2021
    categoria: str = "Fino tinto seco"
    fabricante: str = "SUR ANDINO"
    total_notas: int = 1
    notas:List[NotaSchema]


# Structure returned when a wine is removed from the cellar.
class VinhoDelSchema(BaseModel):
    message: str
    vinho: str


# Returns the wine will all notes included.
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
