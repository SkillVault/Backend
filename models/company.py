from pydantic import BaseModel

class CompanysignUp(BaseModel):
    company_name : str
    company_email : str
    company_website : str
    password : str