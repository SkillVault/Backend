from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes import user,questions,company,checkAnswer
import bcrypt
import logging



# Ensure you import the function for database operations correctly
# from database import create_user, create_questions  # Assuming you'll add a new function for question insertion

origin = ['http://localhost:5173',
''
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
   
)

@app.get('/')
def read_root():
    return {"message": "Welcome to skillvault"}

app.include_router(user.app,prefix="/api/user")
app.include_router(questions.app,prefix="/api/questions")
app.include_router(company.app,prefix="/api/company_signup")
app.include_router(checkAnswer.app,prefix="/api/text-similarity")

