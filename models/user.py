from pydantic import BaseModel
from typing import List,Optional





class CreateUser(BaseModel):
   
    mailid: str
    password: str


class Address(BaseModel):
    first_line: str
    country: str
    state: str
    pincode: str

class InterviewScore(BaseModel):
    interview_type: str
    score: int

class CandidateSignup(BaseModel):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    job_role: Optional[str] = None
    company: Optional[str] = None
    experience: Optional[int] = None
    resume: Optional[str] = None
    photo: Optional[str] = None
    about_me: Optional[str] = None
    skills: Optional[str] = None
    interview_scores: Optional[str] = None
    
class CandidateLogin(BaseModel):
    email: str
    password: str
     
    
class Candidate(BaseModel):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    job_role: Optional[str] = None
    company: Optional[str] = None
    experience: Optional[int] = None
    resume: Optional[str] = None
    photo: Optional[str] = None
    about_me: Optional[str] = None
    skills: Optional[str] = None
    interview_scores: Optional[str] = None 


class GoogleUser(BaseModel):
    user_name: str
    user_mail: str
    profile_url: str
    first_name: str
    last_name: str
    country: str
    state: str
    city: str
    postal_code: str
    about: str
    address: str


class GetUser(BaseModel):
    user_name: str
    user_mail: str
    profile_url: str
    first_name: str
    last_name: str
    country: str
    state: str
    city: str
    postal_code: str
    about: str
    address: str

class UpdateUser(BaseModel):

    first_name: str
    last_name: str
    country: str
    state: str
    city: str
    postal_code: str
    about: str
    address: str


