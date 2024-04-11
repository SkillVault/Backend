import os
from models.questions import FetchQuestion
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient


app = APIRouter()
load_dotenv()  # Load environment variables from .env file
MONGODB_URI="mongodb+srv://bibinjose:bibinmongodb@cluster0.8cod5vz.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.react

@app.get("/",response_model=FetchQuestion)
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
