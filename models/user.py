from pydantic import BaseModel




class CreateUser(BaseModel):
   
    mail_id: str
    user_name: str
    password: str


class GoogleUser(BaseModel):
    user_name: str
    user_mail: str
    profile_url: str
    user_sub: str
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
    user_sub: str
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


