import os
from typing import List
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from models.company import CompanysignUp,AddJob,GetJob
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter,HTTPException
from typing import List



load_dotenv()  # Load environment variables from .env file
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.jobposts
router = APIRouter()

@router.post("/signup", response_model= CompanysignUp)
async def add_company_data(company_info: CompanysignUp):
    # Insert user_info into the MongoDB collection
    await collection.insert_one(company_info.dict())
    return company_info

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
