from fastapi import APIRouter, Form,HTTPException
from models.user import CreateUser,GoogleUser,UpdateUser,CandidateLogin,CandidateSignup
from dotenv import load_dotenv
import os
from database.candidate_data import login, signup
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import bcrypt


load_dotenv()  # Load environment variables from .env file
MONGODB_URI="mongodb+srv://bibinjose:bibinmongodb@cluster0.8cod5vz.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault

collection = db.candidates
app = APIRouter()

SALT = bcrypt.gensalt(10)


@app.post("/candidate_login", response_model=dict)
async def candidate_login(candidate: CandidateLogin) -> dict:
    try:
        login_info = await login(candidate.email)
        stored_password_hash = login_info["password"].encode()
        entered_password = candidate.password.encode()

        if not bcrypt.checkpw(entered_password, stored_password_hash):
            raise HTTPException(status_code=401, detail="Incorrect password")
        else:
            return {"message": "Login successful"}

    except KeyError:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    except Exception as e:
        logging.error(f"An error occurred during candidate login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@app.post("/candidate_signup", response_model= dict)
async def candidate_signup(candidate: CandidateSignup) -> dict:
    try:
        byte_password = bcrypt.hashpw(candidate.password.encode(), SALT)
        hashed_password = byte_password.decode()
        result = await signup(candidate.username, candidate.email, hashed_password)
        return result
    
    except Exception as e:
        logging.error(f"An error occurred during candidate signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")




# google user

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
