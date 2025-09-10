from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

MONGOBD_URI = os.getenv("MONGOBD_URI")

client = MongoClient(MONGOBD_URI, server_api=ServerApi("1"))

db = client.todo_app_db
collection = db["todos"]
