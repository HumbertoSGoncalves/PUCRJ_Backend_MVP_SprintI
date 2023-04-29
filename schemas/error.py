from pydantic import BaseModel


#mensagem de erro em caso de falhas.
class ErrorSchema(BaseModel):
    message: str
