from pymongo import MongoClient
from transcription.wx_transcribe import generate_transcription, show_output 

hf_token = "<your_created_huggingface_token>"
model_name= "openai/whisper-tiny.en" 

device = "cuda"
batch_size = 16
compute_type = "float16"
language = "en"

reference_dir = './local_input_batch/reference_batch/'
audio_dir = './local_input_batch/audio_batch'
whisper_faster_model_dir = "../models/whisper_faster_model/"

def insert_transcription(audio_id, file_name, result_transcription):
  client = MongoClient('mongodb://localhost:27017/')  
  db = client['whisperx']  
  collection = db['transcriptions'] 
  document = {
      'file_name': file_name,
      'audio_id': audio_id,
      'result': result_transcription
  }    
  collection.insert_one(document)

def create_transcription_output(audio_id, output_path, file_name):
  result_transcription = generate_transcription(output_path, hf_token, device, batch_size, compute_type, whisper_faster_model_dir, language)
  insert_transcription(audio_id, file_name, result_transcription)
  show_output(result_transcription)
  return result_transcription
  