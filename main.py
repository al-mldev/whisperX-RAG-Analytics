from db_utils.create_collections import create_collections
from db_utils.instance_faiss import add_transcription_to_faiss, search_in_faiss 
from db_utils.instance_metrics import calculate_error_rates
from db_utils.instance_transcription import create_transcription_output
from db_utils.db_settings import CLIENT_URL, DATABASE_NAME
from huggingface_hub import login
from llm_api.mistral7b_api_call import generate_response
from transcription.wx_transcribe import extract_raw_text
from pymongo import MongoClient
from utils.load_audios import load_mp3_batch
from utils.load_models import check_ffmpeg, load_whisper_model, load_whisper_faster_model
from utils.load_references import load_reference_batch
from utils.utils_settings  import HF_TOKEN, WHISPER_FASTER_MODEL_DIR, MODEL_NAME, WHISPER_MODEL_DIR, AUDIO_DIR, REFERENCE_DIR
import gridfs
import os
import tempfile

login(HF_TOKEN)

def main(database_name):
  client = MongoClient(CLIENT_URL)  
  db = client[database_name]
  audio_collection = db['audio_files']
  transcription_collection = db['transcriptions']
  fs = gridfs.GridFS(db)
  audio_cursor = audio_collection.find()  
  if audio_cursor:
    for doc in audio_cursor:
      file_name = doc.get('filename')
      audio_id = doc.get('audio_id')
      file_id = doc.get('file_id')
      mp3_data = fs.get(file_id).read()
      with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, file_name)
        output_path = output_path.replace("\\", "/")
        with open(output_path, 'wb') as f:
          f.write(mp3_data)
          result_transcription = create_transcription_output(audio_id,output_path, file_name, WHISPER_FASTER_MODEL_DIR)
          raw_text = "\n".join([segment['text'] for segment in result_transcription["segments"]])          
          transcription_cursor = transcription_collection.find()
          transcription_id = result_transcription['transcription_id'] 
          add_transcription_to_faiss(raw_text, transcription_id)
          for transcription in transcription_cursor:
            if transcription['transcription_id'] == transcription_id: 
              last_end = transcription['result']['segments'][-1]['end']
              document_id = transcription['_id']  
              file_name = str(file_name)
              calculate_error_rates(audio_id, 'R-'+file_name, last_end, document_id)
              extract_raw_text(result_transcription)
              document = search_in_faiss(transcription_id)
              document_id = str(document_id)
              document = str(document)
              document = document_id+document
              print("ID: "+document)   
  else: 
     print("Error: no audio files loaded in database")
    
if __name__ == "__main__":
    while True:

      print("---------------------------------------------------------\n",
            "------------------Whisperx Metrics Menu------------------\n"
            "---------------------------------------------------------\n"
            "-----------------1) Create Collections-------------------\n"
            "-----------------2) Load Models--------------------------\n"
            "-----------------3) Load Audios--------------------------\n"
            "-----------------4) Load References----------------------\n"
            "-----------------5) Run Transcriptions-------------------\n"
            "-----------------6) Analyze Transcription with LLM-------\n"
            "-----------------0) Exit---------------------------------\n"
            "---------------------------------------------------------")
      option =input("Enter an option: ")
      
      if option == '0':
        print("Menu Ended")
        break

      if option in '123456':
        option=int(option)
        if option >=1 and option <=6:
            if option == 1:
              create_collections(DATABASE_NAME)
            elif option == 2:
              print("Downloading model from huggingface")
              load_whisper_model(HF_TOKEN, MODEL_NAME, WHISPER_MODEL_DIR)
              print("Transforming whisper model into whisper faster format")
              load_whisper_faster_model(WHISPER_MODEL_DIR, WHISPER_FASTER_MODEL_DIR)
            elif option == 3:
              print("Loading audio files batch from local directory")
              load_mp3_batch(AUDIO_DIR)
            elif option == 4: 
              audio_id = input("Set the audio_id for the reference file: ")
              load_reference_batch(audio_id, REFERENCE_DIR)           
            elif option == 5:
              print("Checking ffmpeg")
              check_ffmpeg()
              print("Running transcriptions")
              main(DATABASE_NAME)
            elif option == 6:
              transcription_id = input("Insert Transcription ID: ")
              document=search_in_faiss(transcription_id)
              instruction=input("Insert Instruction For LLM: ")
              document = str(document)
              prompt = instruction+' :'+document
              generate_response(prompt)             
      else:
        ("Error: insert a value between 1 and 6")
      