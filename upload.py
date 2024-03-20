import pandas as pd
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()  # Load environment variables from .env file
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.skillvault
collection = db.react
# Step 1: Read Excel file
excel_file_path = "C:/Users/bibin/OneDrive/Desktop/react1.xlsx"
df = pd.read_excel(excel_file_path)



# Step 3: Insert data into MongoDB collection
# Convert DataFrame to dictionary (orient='records' converts it to a list of dicts)
data_dict = df.to_dict(orient='records')

# Insert documents into the collection
collection.insert_many(data_dict)

print(f"Inserted {len(data_dict)} documents into MongoDB.")
