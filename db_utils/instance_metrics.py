from metrics.metrics_calc import whisperx_metrics_cer, whisperx_metrics_rtf, whisperx_metrics_wer
from pymongo import MongoClient

def calculate_error_rates(audio_id, file_name, last_end, document_id):
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
  transcription_name = str(document['file_name'])
  transcription_name = transcription_name[2:-4]
  
  print("-------------------------------------------------------------------\n"  
        "-------Transcription Name : "+transcription_name+"---------------------\n"
        "-------------------------------------------------------------------\n"
        "-------------------Status : Complete ------------------------------\n"
        "-------------------------------------------------------------------\n"
        "-----Real Time Factor (RTF): "+str(round((rtf_rate*100),2))+"%--------------------------------\n"
        "-------------------------------------------------------------------\n"
        "-----Word Error Rate (WER): "+str(round((w_rate*100),2))+"%----------------------------------\n"
        "-------------------------------------------------------------------\n"
        "-----Character Error Rate (CER): "+str(round((c_rate*100),2))+"%-----------------------------\n"
        "-------------------------------------------------------------------")

