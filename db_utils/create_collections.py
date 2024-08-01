from pymongo import MongoClient

def create_collections(database_name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client[database_name]
    collection_names = ["audio_files", "metrics" , "references", "transcriptions"]

    for collection_name in collection_names:
      
        if collection_name in db.list_collection_names():
            print(f"Collection '{collection_name}' already exist in '{database_name}'.")
        else:
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created in '{database_name}'.")

