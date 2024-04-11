import os
from models.user import CandidateLogin,CandidateSignup,Candidate
from fastapi import HTTPException 
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter


load_dotenv()
MONGODB_URI="mongodb+srv://bibinjose:bibinmongodb@cluster0.8cod5vz.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.candidates
app = APIRouter()

async def signup(username: str, email: str, password: str ) -> CandidateLogin:
    candidate_data = CandidateLogin(
        username=username,
        password=password,
        email=email,
    )
    result = await collection.insert_one(candidate_data.dict())

    if result.inserted_id:
        return {"message" : "Candidate sign up successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to sign up candidate")
    


async def login(email: str) -> dict:
    candidate_data = await collection.find_one({"email": email})

    if candidate_data:
        return {
            "password": candidate_data["password"],
        }
    else:
        raise HTTPException(status_code=404, detail="Candidate not found")    
    
async def fetchUserDetails(email: str) ->Candidate:
    candidate_data = await collection.find_one({"email": email})
    if candidate_data:
        return candidate_data
    else:
        raise HTTPException(status_code=404, detail="Candidate not found")


    