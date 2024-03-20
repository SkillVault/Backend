import os
from dotenv import load_dotenv
from models.company import CompanysignUp
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter


load_dotenv()  # Load environment variables from .env file
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.companies
app = APIRouter()

@app.post("/", response_model=CompanysignUp)
async def add_company_data(company_info: CompanysignUp):
    # Insert user_info into the MongoDB collection
    await collection.insert_one(company_info.dict())
    return company_info
