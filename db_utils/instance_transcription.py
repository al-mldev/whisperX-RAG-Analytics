from pymongo import MongoClient
import gridfs
import os
import tempfile
from metrics.metrics_calc import whisperx_metrics_rtf
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

def insert_transcription(file_name, result_transcription):
  client = MongoClient('mongodb://localhost:27017/')  
  db = client['whisperx']  
  collection = db['transcriptions'] 
  document = {
      'file_name': file_name,
      'result': result_transcription
  }    
  collection.insert_one(document)

def create_transcription_output(output_path, file_name):
  result_transcription = generate_transcription(output_path, hf_token, device, batch_size, compute_type, whisper_faster_model_dir, language)
  insert_transcription(file_name, result_transcription)
  show_output(result_transcription)
  return result_transcription 

def create_transcription_object(file_name, audio_id):
  client = MongoClient('mongodb://localhost:27017/')  
  db = client['whisperx']
  fs = gridfs.GridFS(db)    
  collection = db['audio_files']
  file_name = collection.find_one({'audio_id': audio_id})
  file_id = file_name['file_id']
  mp3_data = fs.get(file_id).read()
  with tempfile.TemporaryDirectory() as temp_dir:
      output_path = os.path.join(temp_dir, file_name['filename'])
      output_path = output_path.replace("\\", "/")
      with open(output_path, 'wb') as f:
          f.write(mp3_data)
      transcription_object = create_transcription_output(output_path, file_name)
      last_end = transcription_object['segments'][-1]['end']
      whisperx_metrics_rtf(file_name, output_path, last_end)