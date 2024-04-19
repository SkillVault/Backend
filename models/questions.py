from pydantic import BaseModel
from typing import Union

class FetchQuestion(BaseModel):
    QNo: int 
    Question: str
    optionA: Optional[Union[int, str]] = None
    optionB: Optional[Union[int, str]] = None
    optionC: Optional[Union[int, str]] = None
    Answer: Union[int, str]
    Level: int

class CheckAnswer(BaseModel):
    question: str
    answer: str
