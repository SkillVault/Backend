from fastapi import APIRouter, HTTPException
from models.user import Candidate, GoogleUser, Login,UpdateUser,ApplyJob
from database.candidate_data import login, signup, fetchUserDetails, checkUserExist, updateUserDetails
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import bcrypt
from datetime import datetime, timedelta
import jwt

load_dotenv()  # Load environment variables from .env file
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.candidates
collection1 = db.appliedjobs

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
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/candidate_login", response_model=dict)
async def candidate_login(candidate: Login) -> dict:
    try:
        login_info = await login(candidate.email)
        stored_password_hash = login_info["password"].encode()
        entered_password = candidate.password.encode()

        if not bcrypt.checkpw(entered_password, stored_password_hash):
            raise HTTPException(status_code=401, detail="Incorrect password")
        else:
            # Generate JWT token
            access_token = create_access_token(data={"email": candidate.email})
            return {"access_token": access_token, "token_type": "bearer"}

    except KeyError:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    except Exception as e:
        logging.error(f"An error occurred during candidate login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    

@router.post("/candidate_signup", response_model=dict)
async def candidate_signup(candidate: Candidate) -> dict:
    try:
        byte_password = bcrypt.hashpw(candidate.password.encode(), SALT)
        hashed_password = byte_password.decode()
        result = await signup(candidate.username, candidate.email, hashed_password)
        return result
    
    except Exception as e:
        logging.error(f"An error occurred during candidate signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@router.post("/create_google_user", response_model=GoogleUser)
async def create_google_user(user_info: GoogleUser):
    await collection.insert_one(user_info.dict())
    return user_info



@router.get("/get_user")
async def fetch_google_user(email: str):
    existing_user = await fetchUserDetails(email)
    
    if existing_user:
        return existing_user
    else: 
        return False

@router.get("/get_profile")
async def fetchProfile(username:str):
    # Attempt to find the user in the database
    existing_user = await collection.find_one({"username": username})
    
    if existing_user:
        candidate_dict = dict(existing_user)
        candidate_dict.pop('_id', None)
        return candidate_dict

@router.put("/update_candidate", response_model=dict)
async def update_google_user(email: str, user_data: UpdateUser):
    existing_user = await checkUserExist(email)
    if existing_user:
        result = await updateUserDetails(email, user_data)
        return result
    else:
        return {"ERROR": "user not found"}


@router.post('/apply_job',response_model=ApplyJob)
async def applyJob(applyJob:ApplyJob):
    await collection1.insert_one(applyJob.dict())
    return applyJob

@router.put('/skill_update')
async def updateSkill(email: str, skill: dict):
    existing_user = await checkUserExist(email)
    if existing_user:
        result = collection.update_one(
            {"email": email},
            {"$set": {"skills": skill}}
        )
        return {"success": "Successfully updated"}
    return {"success": False}