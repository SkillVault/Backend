from pydantic import BaseModel
from typing import Optional


class CompanysignUp(BaseModel):
    company_name : str
    company_email : str
    company_website : str
    password : str

class CompanyDetails(BaseModel):
    company_name: str
    company_email: str
    company_website: str


class AddJob(BaseModel):
    job_title : str
    skills: str
    category : str
    location : str
    openings : str
    salary : str
    companyname: str
    website: str
    companyemail: str
    closingDate: str
    
class GetJob(BaseModel):
    job_title : Optional[str] = None
    jobid: Optional[str] = None
    category : Optional[str] = None
    location : Optional[str] = None
    skills: Optional[str] = None
    openings : Optional[str] = None
    salary : Optional[str] = None
    companyname: str
    website: str
    closingDate: str


class Responses(BaseModel):
    userName: str
    job_title : str
    link: str
    companyName: str
    jobid: str