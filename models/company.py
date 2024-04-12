from pydantic import BaseModel

class CompanysignUp(BaseModel):
    companyName : str
    email : str
    website : str
    password : str

class CompanyInfo(BaseModel):
    companyName : str
    email : str
    website : str



class AddJob(BaseModel):
    job_title : str
    category : str
    location : str
    skillRequired: str
    openings : str
    salary : str

class GetJob(BaseModel):
    job_title : str
    category : str
    location : str
    skillRequired: str
    openings : str
    salary : str
    

class CompanyLogin(BaseModel):
    email : str
    password : str