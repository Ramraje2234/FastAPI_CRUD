# import pymongo
#
#
# # MongoDB Atlas connection
# def get_database():
#     client = pymongo.MongoClient("mongodb://localhost:27017/")
#     db = client['crud_app']
#     return db


from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
import os

# MongoDB Atlas connection URI (Make sure to replace with your credentials)
MONGODB_URI = os.getenv("MONGODB_URI",
                        "mongodb+srv://chiragramraje7741:x2EAgX75b2f0X9t1@cluster0.c354n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Database name (replace 'my_database' with your actual database name)
DATABASE_NAME = "Crud_App"

# Create a global client to reuse connections
client = AsyncIOMotorClient(MONGODB_URI)


def get_database() -> Database:
    """
    Returns the MongoDB database instance.
    Ensures reuse of the client connection.
    """
    return client[DATABASE_NAME]


