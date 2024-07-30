from bson import ObjectId  
from pymongo import MongoClient
from unidecode import unidecode
import re

def load_reference_text(file_name):
  client = MongoClient('mongodb://localhost:27017/')
  db = client['whisperx']
  collection = db['references']
  reference_document = collection.find_one({'file_name': file_name})
  if reference_document:
    reference_document = str(reference_document) 
    processed_text = reference_document.replace('\n', ' ').lower()
    processed_text = unidecode(processed_text)
    reference_list = re.findall(r'\b\w+\b', processed_text)
    reference_list = reference_list[8:] 
    print(f"Reference document found for file: {file_name}")
    return reference_list  
  else:
      print(f"Warning: No reference document found for file: {file_name}")
      return None

def load_transcription_text(document_id):
  client = MongoClient('mongodb://localhost:27017/')
  db = client['whisperx']
  collection = db['transcriptions']
  transcription_document = collection.find_one({'_id': ObjectId(document_id)})
  transcription_list = []
  if transcription_document:
     segments = transcription_document.get('result',{}).get('segments',[])
     transcription_text = [segment.get('text', '') for segment in segments]
     transcription_text = str(transcription_text)
     processed_text = transcription_text.replace('\n', ' ').lower()
     processed_text = unidecode(processed_text)
     transcription_list = re.findall(r'\b\w+\b', processed_text)
     print(f"Transcription document found for file: {document_id}")
     return transcription_list
    
  else:
      print(f"Warning: No transcription document found for file: {document_id}")
      return None
