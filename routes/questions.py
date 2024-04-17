import os
from models.questions import FetchQuestion
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient



load_dotenv()  # Load environment variables from .env file
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.react

router = APIRouter()

@router.get("/",response_model=FetchQuestion)
async def get_question(QNo: int,Level: int):
    try:
        question_document = await collection.find_one({"QNo": QNo,"Level": Level})
        if question_document:
            return FetchQuestion(**question_document)
        else:
            raise HTTPException(status_code=404, detail="Question not found")
    except ValueError as e:  # If Q_No is not an integer
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:  # Catch all other exceptions
        return JSONResponse(
            status_code=500,
            content={"message": "An error occurred", "error": str(e)},
        )
