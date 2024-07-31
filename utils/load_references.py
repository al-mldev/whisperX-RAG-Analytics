import os
import re
from pymongo import MongoClient
from unidecode import unidecode


def load_reference_batch(audio_id, reference_dir):
  client = MongoClient('mongodb://localhost:27017/')
  db = client['whisperx']
  collection = db['references']
  if os.listdir(reference_dir):
    for file_name in os.listdir(reference_dir):
      if ([i for i in os.listdir(reference_dir) if i.startswith('R-') and i.endswith('.txt')]): 
        with open(reference_dir+file_name, 'r', encoding="utf-8") as file:
          reference_text = file.read()
          processed_text = reference_text.replace('\n', ' ').lower()
          processed_text = unidecode(processed_text)
          reference_list = re.findall(r'\b\w+\b', processed_text)            
          reference_document = {
                  'file_name': file_name,
                  'audio_id': audio_id,
                  'reference_list': reference_list
              }
          collection.insert_one(reference_document)
          print(f"File: {file_name} loaded successfully {'references'}.")
          file.close()
      elif not ([i for i in os.listdir(reference_dir) if i.startswith('R-') and i.endswith('.txt')]):   
        print(file_name[:-4]+"Error: File "+file_name+" has no reference format R-<filename>.txt")





