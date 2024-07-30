from db_utils.instance_transcription import create_transcription_object
from huggingface_hub import login
from metrics.metrics_calc import whisperx_metrics_wer, whisperx_metrics_cer
from pymongo import MongoClient
from utils.load_audios import load_mp3_batch
from utils.load_models import check_ffmpeg, load_whisper_model, load_whisper_faster_model
from utils.load_references import load_reference_batch

hf_token = "<your_created_huggingface_token>"
model_name= "openai/whisper-tiny.en" 

reference_dir = './local_input_batch/reference_batch/'
audio_dir = './local_input_batch/audio_batch'
whisper_model_dir = "./models/whisper_model/"
whisper_faster_model_dir = "./models/whisper_faster_model/"

login(hf_token)

def main():
  client = MongoClient('mongodb://localhost:27017/')  
  db = client['whisperx']
  audio_collection = db['audio_files']
  transcription_collection = db['transcriptions']
  audio_cursor = audio_collection.find()  
  if audio_cursor:
    for doc in audio_cursor:
      file_name = doc.get('filename')
      audio_id = doc.get('audio_id')
      create_transcription_object(file_name, audio_id)
      transcription_obj = transcription_collection.find_one({'file_name.audio_id': audio_id })
      document_id = transcription_obj.get('_id')
      whisperx_metrics_wer((str('R-'+file_name)), document_id)
      whisperx_metrics_cer((str('R-'+file_name)), document_id) 
  else: 
     print("Error: no audio files loaded in database")
    

if __name__ == "__main__":
    print("---------------------------------------------------------") 
    print("------------------Whisperx Metrics Menu------------------")
    print("---------------------------------------------------------")
    print("------------------1) Load Models--------------------------\n",
          "-----------------2) Load Audios--------------------------\n",
          "-----------------3) Load References----------------------\n",
          "-----------------4) Run Transcriptions-------------------")
    print("---------------------------------------------------------")
    option =input("Enter an option: ")
    if option in '1234':
       option=int(option)
       if option >=1 and option <=4:
          if option == 1:
            print("Downloading model from huggingface")
            load_whisper_model(hf_token, model_name, whisper_model_dir)
            print("Transforming whisper model into whisper faster format")
            load_whisper_faster_model(whisper_model_dir, whisper_faster_model_dir)
          elif option == 2:
            print("Loading audio files batch from local directory")
            load_mp3_batch(audio_dir)
          elif option == 3: 
            print("Loading reference files batch from local directory") 
            load_reference_batch(reference_dir)            
          elif option == 4:
            print("Checking ffmpeg")
            check_ffmpeg()
            print("Running transcriptions")
            main()
    else:
      ("Error: insert a value between 1 and 4")
    