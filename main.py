from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import router as user_router  # Import the router from user.py
from routes.questions import router as questions_router  # Import the router from questions.py
from routes.company import router as company_router  # Import the router from company.py
from routes.checkAnswer import router as check_answer_router  # Import the router from checkAnswer.py

# Ensure you import the function for database operations correctly
# from database import create_user, create_questions  # Assuming you'll add a new function for question insertion

origin = ['http://localhost:5173', 'https://skillvault-backend.onrender.com']

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

app.include_router(user_router, prefix="/api/user")  # Use the imported router
app.include_router(questions_router, prefix="/api/questions")  # Use the imported router
app.include_router(company_router, prefix="/api/company")  # Use the imported router
app.include_router(check_answer_router, prefix="/api/text-similarity")  # Use the imported router
