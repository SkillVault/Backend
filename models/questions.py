from pydantic import BaseModel


class FetchQuestion(BaseModel):
    
    QNo: int 
    Question: str
    Answer: str
    Level: int