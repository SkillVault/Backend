import os
from typing import List
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from models.company import CompanysignUp,AddJob,GetJob
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter,HTTPException,Body
from typing import List
import logging
from database.company_data import signup,login
import jwt
import bcrypt
from datetime import datetime, timedelta




load_dotenv()  # Load environment variables from .env file
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.jobposts
router = APIRouter()


SALT = bcrypt.gensalt(10)
SECRET_KEY = "g5iv0jd5hi4hkf5iu8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


@router.post("/login", response_model=dict)
async def company_login(company_email: str = Body(...), password: str = Body(...)) -> dict:
    try:
        login_info = await login(company_email)
        stored_password_hash = login_info["password"].encode()
        entered_password = password.encode()

        if not bcrypt.checkpw(entered_password, stored_password_hash):
            raise HTTPException(status_code=401, detail="Incorrect password")
        else:
            access_token = create_access_token(data={"email": company_email})
            return {"access_token": access_token, "token_type": "bearer"}
    except KeyError:
        raise HTTPException(status_code=404, detail="Candidate not found")
    except Exception as e:
        logging.error(f"An error occurred during candidate login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
 
 
    
@router.post("/signup", response_model=dict)
async def candidate_signup(company_data: CompanysignUp) ->dict :
    try:
        byte_password = bcrypt.hashpw(company_data.password.encode(), SALT)
        hashed_password = byte_password.decode()
        print("before signup\n")
        result = await signup(company_data.company_name, company_data.company_email, company_data.company_website, hashed_password)
        return result   
    except Exception as e:
        logging.error(f"An error occurred during candidate signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/add_job", response_model=AddJob)
async def postjob(add_job: AddJob):
    # Insert user_info into the MongoDB collection
    await collection.insert_one(add_job.dict())
    return add_job

@router.get("/get_job", response_model=List[GetJob])
async def get_job():
    try:
        job_cursor = collection.find()
        jobs_list = await job_cursor.to_list(length=None)  # Retrieves all documents as a list
        if jobs_list:
            # Remove _id field from each document
            for job in jobs_list:
                job.pop("_id", None)
            # Return list of job documents
            return jobs_list
        else:
            # If the list is empty, there are no jobs
            raise HTTPException(status_code=404, detail="No jobs found")
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred", "error": str(e)},
        )
