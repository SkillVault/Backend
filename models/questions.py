from pydantic import BaseModel
from typing import Union

class FetchQuestion(BaseModel):
    QNo: int 
    Question: str
    # optionA: Union[int, str]
    # optionB: Union[int, str]
    # optionC: Union[int, str]
    Answer: Union[int, str]
    Level: int

class CheckAnswer(BaseModel):
    question: str
    answer: str
