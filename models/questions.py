from pydantic import BaseModel
from typing import Union

class FetchQuestion(BaseModel):
    QNo: int 
    Question: str
    # optionA: Union[int, str]
    # optionB: Union[int, str]
    # optionC: Union[int, str]
    # Correct: Union[int, str]
    Level: int
    Answer: str

class CheckAnswer(BaseModel):
    question: str
    answer: str
