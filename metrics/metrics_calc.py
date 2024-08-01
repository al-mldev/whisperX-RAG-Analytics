from evaluate import load
from jiwer import cer
from pymongo import MongoClient
from utils.load_lists import load_transcription_text, load_reference_text
import gridfs
import os
import librosa
import tempfile

def whisperx_metrics_rtf(audio_id, file_name, last_end):
  last_end = float(last_end)
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
    audio_duration = librosa.get_duration(filename=output_path)
    rtf_score = last_end/audio_duration
  return rtf_score
  
def whisperx_metrics_wer(file_name, document_id):
  file_name=file_name.replace('.mp3', '.txt')
  reference_list = load_reference_text(file_name)
  transcription_list = load_transcription_text(document_id)
  if reference_list==None or transcription_list==None:
    print("-------Transcription Name: "+file_name+"-------------\n"
          "Error: No data to calculate WER metrics")
  else:
    ref_str = str(reference_list)
    tr_str = str(transcription_list)
    wer = load("wer")
    wer_score = wer.compute(predictions=[tr_str], references=[ref_str])
    return wer_score

def whisperx_metrics_cer(file_name, document_id):
  file_name=file_name.replace('.mp3', '.txt')
  reference_list = load_reference_text(file_name)
  transcription_list = load_transcription_text(document_id)
  if reference_list==None or transcription_list==None:
    print("-------Transcription Name: "+file_name+"-------------")
    print('Error: No data to calculate CER metrics')  
  else:
    ref_str = str(reference_list)
    tr_str = str(transcription_list)
    cer_score = cer(ref_str, tr_str)
    return cer_score

def show_error_rates(audio_id, file_name, last_end, document_id):
  w_rate = whisperx_metrics_wer(file_name, document_id)
  c_rate = whisperx_metrics_cer(file_name, document_id)
  rtf_rate = whisperx_metrics_rtf(audio_id, file_name, last_end)
  client = MongoClient('mongodb://localhost:27017/')  
  db = client['whisperx']  
  collection = db['metrics'] 
  document = {
      'file_name': file_name,
      'audio_id': audio_id,
      'rtf_score': rtf_rate,
      'wer_score': w_rate,
      'cer_score': c_rate
  }    
  collection.insert_one(document)
  rtf_rate = float(rtf_rate)
  c_rate = float(c_rate)
  w_rate = float(w_rate)

  print("-------------------------------------------------------------------\n"  
        "-------Transcription Name : "+str(document['file_name'])+"---------------------\n"
        "-------------------------------------------------------------------\n"
        "-------------------Status : Complete ------------------------------\n"
        "-------------------------------------------------------------------\n"
        "-----Real Time Factor (RTF): "+str(round((rtf_rate*100),2))+"%--------------------------------\n"
        "-------------------------------------------------------------------\n"
        "-----Word Error Rate (WER): "+str(round((w_rate*100),2))+"%----------------------------------\n"
        "-------------------------------------------------------------------\n"
        "-----Character Error Rate (CER): "+str(round((c_rate*100),2))+"%-----------------------------\n"
        "-------------------------------------------------------------------")





