from pydantic import BaseModel


# error message.
class ErrorSchema(BaseModel):
    message: str
