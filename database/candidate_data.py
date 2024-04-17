import os
from models.user import Candidate, UpdateUser
from fastapi import HTTPException 
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.candidates
app = APIRouter()


######################  SIGN UP ########################

async def signup(username: str, email: str, password: str) -> dict:
    candidate_data = Candidate(
        username=username,
        password=password,
        email=email,
    )
    result = await collection.insert_one(candidate_data.dict())

    if result.inserted_id:
        return {"message": "Candidate sign up successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to sign up candidate")
    
    
####################  LOGIN #################################

async def login(email: str) -> dict:
    candidate_data = await collection.find_one({"email": email})

    if candidate_data:
        return {
            "password": candidate_data["password"],
        }
    else:
        raise HTTPException(status_code=404, detail="Candidate not found")    
    
####################  FETCH USERS #################################

async def fetchUserDetails(email: str) -> Candidate:
    candidate_data = await collection.find_one({"email": email})
    if candidate_data:
        candidate_dict = dict(candidate_data)
        candidate_dict.pop('_id', None)
        return candidate_dict
    else:
        return False
    
    
####################  CHECK USERS#################################

async def checkUserExist(email: str) -> bool:
    candidate_data = await collection.find_one({"email": email})
    if candidate_data:
        return True
    else:
        return False
    
    
 ####################  UPDATE USERS #################################

async def updateUserDetails(email: str, profileData: UpdateUser) -> dict:
    try:
        if await checkUserExist(email):
            update_data = {}
            if hasattr(profileData, 'username'):
                update_data['username'] = profileData.username
            if hasattr(profileData, 'email'):
                update_data['email'] = profileData.email
            if hasattr(profileData, 'first_name'):
                update_data['first_name'] = profileData.first_name
            if hasattr(profileData, 'last_name'):
                update_data['last_name'] = profileData.last_name
            if hasattr(profileData, 'address'):
                if profileData.address is not None:
                    if isinstance(profileData.address, dict):
                        address_data = profileData.address
                    else:
                        address_data = profileData.address.dict()
                else:
                    address_data = None
                update_data['address'] = address_data
            if hasattr(profileData, 'phone_number'):
                update_data['phone_number'] = profileData.phone_number
            if hasattr(profileData, 'job_role'):
                update_data['job_role'] = profileData.job_role
            if hasattr(profileData, 'company'):
                update_data['company'] = profileData.company
            if hasattr(profileData, 'experience'):
                update_data['experience'] = profileData.experience
            if hasattr(profileData, 'resume'):
                update_data['resume'] = profileData.resume
            if hasattr(profileData, 'photo'):
                update_data['photo'] = profileData.photo
            if hasattr(profileData, 'about_me'):
                update_data['about_me'] = profileData.about_me

            # Remove any keys with None values from the update_data dictionary
            update_data = {k: v for k, v in update_data.items() if v is not None}

            result = await collection.update_one({"email": email}, {"$set": update_data})

            if result.modified_count == 1:
                return {"message": "User details updated successfully"}
            else:
                return {"error": "Failed to update user details. No documents modified."}
        else:
            return {"error": "Candidate NOT FOUND"}
    except Exception as e:
        return {"error": f"Failed to update user details. {str(e)}"}
