from fastapi import APIRouter, Form
from models.user import CreateUser,GoogleUser,UpdateUser
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient



load_dotenv()  # Load environment variables from .env file
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault

collection = db.candidates
app = APIRouter()


@app.post("/", response_model=CreateUser)
async def add_user_data(user_info: CreateUser):
    # Insert user_info into the MongoDB collection
    await collection.insert_one(user_info.dict())
    return user_info


@app.post("/create_google_user", response_model=GoogleUser)
async def createGoogleUser(user_info: GoogleUser):
  
        await collection.insert_one(user_info.dict())
        # Return the new user data
        return user_info



@app.get("/get_user")
async def fetchGoogleUser(user_sub:str):
    # Attempt to find the user in the database
    existing_user = await collection.find_one({"user_sub": user_sub})
    
    if existing_user:
        # If the user exists, convert the MongoDB document to a GoogleUser model and return
        return GoogleUser(**existing_user)
   
@app.put("/update_user",response_model=UpdateUser)
async def update_google_user(user_sub: str, user_data: UpdateUser):
    # Check if the user exists
    existing_user = await collection.find_one({"user_sub": user_sub})
    if existing_user:
        # Update the user's about field
        result = await collection.update_one(
            {"user_sub": user_sub},  # Filter criteria
            {"$set": {
              
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "country": user_data.country,
                "state": user_data.state,
                "city": user_data.city,
                "postal_code": user_data.postal_code,
                "about": user_data.about,
                "address": user_data.address
            
            }}  # Update operation using $set
        )
        if result.modified_count == 1:
            return user_data
        else:
            raise HTTPException(status_code=500, detail="Failed to update user")
    else:
        raise HTTPException(status_code=404, detail="User not found")
