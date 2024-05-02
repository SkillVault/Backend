import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from models.questions import FetchQuestion
from fastapi.responses import JSONResponse
from typing import List
from random import choice
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()  # Load environment variables from .env file
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault


router = APIRouter()

@router.get("/", response_model=FetchQuestion)
async def get_question(subject : str ,Level: int):
    try:
        collection = db[subject]
        questions_list = []
        async for question_document in collection.find({"Level": Level}):
            questions_list.append(FetchQuestion(**question_document))

        if questions_list:
            random_question = choice(questions_list)
            return  random_question
        else:
            raise HTTPException(status_code=404, detail="Questions not found for the specified level")
    except ValueError as e:  # If Level is not an integer
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:  # Catch all other exceptions
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred", "error": str(e)},
        )