from pydantic import BaseModel


# How a note is added to a wine.
class NotaSchema(BaseModel):
    vinho_id: int = 1
    texto: str = "Notas a serem adicionadas."


# Structure for retrieving a note from a wine.
class NotaDelSchema(BaseModel):
    message: str
    vinho: str
