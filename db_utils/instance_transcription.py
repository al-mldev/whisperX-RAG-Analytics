from bson import Binary, UuidRepresentation
from db_utils.db_settings import CLIENT_URL, DATABASE_NAME
from utils.utils_settings import HF_TOKEN, DEVICE, BATCH_SIZE, COMPUTE_TYPE, LANGUAGE, WHISPER_FASTER_MODEL_DIR
from pymongo import MongoClient
from transcription.wx_transcribe import generate_transcription, show_output 
import uuid

def insert_transcription(audio_id, file_name, result_transcription):
  client = MongoClient(CLIENT_URL)  
  db = client[DATABASE_NAME]  
  collection = db['transcriptions'] 
  transcription_id = uuid.uuid4()
  bson_transcription_id = Binary.from_uuid(transcription_id, UuidRepresentation.STANDARD)
  result_transcription['transcription_id'] = bson_transcription_id
  document = {
      'transcription_id': bson_transcription_id,
      'audio_id': audio_id,
      'file_name': file_name,
      'result': result_transcription
  }    
  collection.insert_one(document)

def create_transcription_output(audio_id, output_path, file_name, whisper_faster_model_dir):
  result_transcription = generate_transcription(output_path, HF_TOKEN, DEVICE, BATCH_SIZE, COMPUTE_TYPE, WHISPER_FASTER_MODEL_DIR, LANGUAGE)
  insert_transcription(audio_id, file_name, result_transcription)
  show_output(result_transcription)
  return result_transcription
  