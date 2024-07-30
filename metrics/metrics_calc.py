from evaluate import load
from jiwer import cer
from utils.load_lists import load_transcription_text, load_reference_text
import librosa

#pending: set the functions outputs as inserts on the metrics collection, show the resulting object   

def whisperx_metrics_rtf(file_name, output_path, last_end):
  last_end = float(last_end)
  audio_duration = librosa.get_duration(filename=output_path)
  rtf_score = last_end/audio_duration
  print("-------------------------------------------------------------------")
  print("-------Transcription Name : "+str(file_name['filename'])+"--------------------")
  print("-------Transcription Time : "+str(round(last_end))+" (s)-----------------------------")
  print("-------------------Status : Complete ------------------------------------------")
  print("----Real Time Factor (RTF): "+str(round((rtf_score*100),2))+"%-----------------------")
  print("-------------------------------------------------------------------") 

def whisperx_metrics_wer(file_name, document_id):
  file_name=file_name.replace('.mp3', '.txt')
  reference_list = load_reference_text(file_name)
  transcription_list = load_transcription_text(document_id)
  ref_str = str(reference_list)
  tr_str = str(transcription_list)
  wer = load("wer")
  wer_score = wer.compute(predictions=[tr_str], references=[ref_str])
  if reference_list==None or transcription_list==None:
    print("-------Transcription Name: "+file_name+"-------------")
    print('Error: No data to calculate WER metrics')
  else:
    print("-------------------------------------------------------------------")
    print("-------Transcription Name: "+file_name+"-------------")
    print("-------------------------------------------------------------------")
    print("----Word Error Rate (WER): "+str(round((wer_score*100),2))+"%------------------------")
    print("-------------------------------------------------------------------")

def whisperx_metrics_cer(file_name, document_id):
  file_name=file_name.replace('.mp3', '.txt')
  reference_list = load_reference_text(file_name)
  transcription_list = load_transcription_text(document_id)
  ref_str = str(reference_list)
  tr_str = str(transcription_list)
  cer_score = cer(ref_str, tr_str)
  if reference_list==None or transcription_list==None:
    print("-------Transcription Name: "+file_name+"-------------")
    print('Error: No data to calculate CER metrics')
  else: 
    print("-------------------------------------------------------------------")
    print("-------Transcription Name: "+file_name+"--------------------------")  
    print("-------------------------------------------------------------------")
    print("-----Character Error Rate (CER): "+str(round((cer_score*100),2))+"%----------------------------------")
    print("-------------------------------------------------------------------")





