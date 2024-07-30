import gridfs
import os
from pymongo import MongoClient

def load_mp3_batch(audio_dir):
    client = MongoClient('mongodb://localhost:27017/')  
    db = client['whisperx']
    fs = gridfs.GridFS(db)
    files = os.listdir(audio_dir)
    c=1

    for file_name in files:
        if file_name.endswith('.mp3'):
            file_path = os.path.join(audio_dir, file_name)
            with open(file_path, 'rb') as f:
                file_data = f.read()
            file_id = fs.put(file_data, filename=file_name)
            collection = db['audio_files']
            audio_id = f"T-{c}" 
            document = {
                'audio_id': audio_id,
                'filename': file_name, 
                'file_id': file_id 
            }
            collection.insert_one(document)
            print(f"File: {file_name} uploaded to mongodb ID: {file_id}")
            c+=1


    