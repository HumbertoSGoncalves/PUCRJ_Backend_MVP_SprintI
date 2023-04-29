from pydantic import BaseModel


# como uma nota é adicionada a um vinho
class NotaSchema(BaseModel):
    vinho_id: int = 1
    texto: str = "Notas a serem adicionadas."


# estrutura para retirada de nota de algum vinho
class NotaDelSchema(BaseModel):
    message: str
    vinho: str
