from pymongo import MongoClient
from db_utils.db_settings import CLIENT_URL

def create_collections(DATABASE_NAME):
    client = MongoClient(CLIENT_URL)
    db = client[DATABASE_NAME]
    collection_names = ["audio_files", "metrics" , "references", "transcriptions"]

    for collection_name in collection_names:
        if collection_name in db.list_collection_names():
            print(f"Collection '{collection_name}' already exist in '{DATABASE_NAME}'.")
        else:
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created in '{DATABASE_NAME}'.")

