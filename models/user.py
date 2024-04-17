from pydantic import BaseModel
from typing import List,Optional


class Address(BaseModel):
    first_line: str
    country: str
    state: str
    city: str
    pincode: int

class BaseUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[Address] = None
    job_role: Optional[str] = None
    company: Optional[str] = None
    experience: Optional[int] = None
    resume: Optional[str] = None
    photo: Optional[str] = None
    about_me: Optional[str] = None
    skills: Optional[str] = None
    interview_scores: Optional[str] = None


class UpdateUser(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[Address] = None
    phone_number: Optional[str] = None
    job_role: Optional[str] = None
    company: Optional[str] = None
    experience: Optional[int] = None
    resume: Optional[str] = None
    photo: Optional[str] = None
    about_me: Optional[str] = None

class Candidate(BaseUser):
    username: str
    email: str
    password: str

class GoogleUser(BaseUser):
    username: str
    email: str

    
class Login(BaseModel):
    email: str
    password: str