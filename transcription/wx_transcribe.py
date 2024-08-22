import whisperx
from transcription.wx_align import align_text
from transcription.wx_diarize import generate_diarization

def generate_transcription(output_path, HF_TOKEN, DEVICE, BATCH_SIZE, COMPUTE_TYPE, WHISPER_FASTER_MODEL_DIR, LANGUAGE):
  model = whisperx.load_model(WHISPER_FASTER_MODEL_DIR, DEVICE, compute_type=COMPUTE_TYPE, language=LANGUAGE) 
  audio = whisperx.load_audio(output_path)
  result = model.transcribe(audio, batch_size=BATCH_SIZE)
  result = align_text(audio, DEVICE, result)
  generate_diarization(HF_TOKEN, DEVICE, audio, result)
  return result 

def extract_raw_text(result_transcription):
  raw_text = "\n".join([segment['text'] for segment in result_transcription["segments"]])
  print("------------------------------------------------------------------\n",
        "------------------------Raw Transcription-------------------------\n",
        "------------------------------------------------------------------\n",
        raw_text)
  
def show_output(result_transcription):
  for seg, segment in enumerate(result_transcription["segments"]):      
    print(f"Segment {seg + 1}:")
    print(f"Start time: {segment['start']:.2f}")
    print(f"End time: {segment['end']:.2f}")
    print(f"{segment['speaker']}")
    print(f"{segment['text']}")
    print("")


