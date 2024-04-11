import os
from dotenv import load_dotenv
from models.company import CompanysignUp,AddJob,GetJob,CompanyLogin
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter,HTTPException
import logging
from typing import List
import bcrypt
from database.company_data import login,signup


load_dotenv()  # Load environment variables from .env file
MONGODB_URI="mongodb+srv://bibinjose:bibinmongodb@cluster0.8cod5vz.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.jobposts
app = APIRouter()
SALT = bcrypt.gensalt(10)


@app.post("/login", response_model=dict)
async def company_login(company: CompanyLogin) -> dict:
    try:
        login_info = await login(company.email)
        stored_password_hash = login_info["password"].encode()
        entered_password = company.password.encode()

        if not bcrypt.checkpw(entered_password, stored_password_hash):
            raise HTTPException(status_code=401, detail="Incorrect password")
        else:
            return {"message": "Login successful"}

    except KeyError:
        raise HTTPException(status_code=404, detail="Company not found")
    
    except Exception as e:
        logging.error(f"An error occurred during company login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/signup", response_model= dict)
async def company_signup(company: CompanysignUp) -> dict:
    try:
        byte_password = bcrypt.hashpw(company.password.encode(), SALT)
        hashed_password = byte_password.decode()
        result = await signup(company.companyName, company.email, company.website, hashed_password)
        return result
    
    except Exception as e:
        logging.error(f"An error occurred during company signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")





@app.post("/add_job", response_model=AddJob)
async def postjob(add_job: AddJob):
    # Insert user_info into the MongoDB collection
    await collection.insert_one(add_job.dict())
    return add_job

@app.get("/get_job", response_model=List[GetJob])
async def get_job():
    try:
        # Using collection.find() instead of collection.find_one()
        job_cursor = collection.find()
        jobs_list = await job_cursor.to_list(length=None)  # Retrieves all documents as a list
        if jobs_list:
            # Return list of job documents
            return [GetJob(**job) for job in jobs_list]
        else:
            # If the list is empty, there are no jobs
            raise HTTPException(status_code=404, detail="No jobs found")
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred", "error": str(e)},
        )


