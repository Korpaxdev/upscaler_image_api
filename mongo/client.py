from os import getenv

import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_USERNAME = getenv("MONGO_USERNAME")
MONGO_USER_PASSWORD = getenv("MONGO_PASSWORD")
MONGO_HOST = getenv("MONGO_HOST")
DB_NAME = getenv("DB_NAME", "default")
FILES_COLLECTION = getenv("FILES_COLLECTION", "files")

client = pymongo.MongoClient(f"mongodb://{MONGO_USERNAME}:{MONGO_USER_PASSWORD}@{MONGO_HOST}/")
db = client[DB_NAME]
files_collection = db[FILES_COLLECTION]
