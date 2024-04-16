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

    
class Login(BaseModel):
    email: str
    password: str


class GoogleUser(BaseModel):
    username: str
    email: str
    profile_url: str
    experience: int
    skills:str
    resume:str
    first_name: str
    last_name: str
    country: str
    state: str
    city: str
    pincode: str
    about_me: str
    address: str


class GetUser(BaseModel):
    username: str
    email: str
    skills:str
    resume:str
    photo: str
    first_name: str
    last_name: str
    experience: int
    country: str
    state: str
    city: str
    pincode: str
    about_me: str
    address: str

class UpdateGoogleUser(BaseModel):
    
    username : str
    experience: int
    resume:str
    skills:str
    photo:str
    first_name: str
    last_name: str
    country: str
    state: str
    city: str
    pincode: str
    about_me: str
    address: str


