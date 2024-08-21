from pydantic import BaseModel

class SMS(BaseModel):
    sender: str
    receiver: str
    content: str