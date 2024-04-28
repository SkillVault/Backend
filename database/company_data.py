import os
from models.company import CompanysignUp
from fastapi import HTTPException 
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter


load_dotenv()
MONGODB_URI="mongodb+srv://bibinjose:bibinmongodb@cluster0.8cod5vz.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.companies
app = APIRouter()

async def signup(companyName: str, email: str,website: str, password: str )->dict:
    print("inside 1\n\n")
    company_data = CompanysignUp(
        company_name=companyName,
        company_email=email,
        company_website=website,
        password=password,
    )
    print(company_data)
    result = await collection.insert_one(company_data.dict())

    if result.inserted_id:
        return {"message" : "Company sign up successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to sign up company")
    
async def login(email: str) -> dict:
    company_data = await collection.find_one({"company_email": email})
    if company_data:
        return {
            "password": company_data["password"],
        }
    else:
        raise HTTPException(status_code=404, detail="Candidate not found")