import whisperx
from transcription.wx_align import align_text
from transcription.wx_diarize import generate_diarization

def generate_transcription(output_path, hf_token, device, batch_size, compute_type, whisper_faster_model_dir, language):
  model = whisperx.load_model(whisper_faster_model_dir, device, compute_type=compute_type, language=language) 
  audio = whisperx.load_audio(output_path)
  result = model.transcribe(audio, batch_size=batch_size)
  result = align_text(audio, device, result)
  generate_diarization(hf_token, device, audio, result)
  return result 

def show_output(result_transcription):
  for seg, segment in enumerate(result_transcription["segments"]):      
    print(f"Segment {seg + 1}:")
    print(f"Start time: {segment['start']:.2f}")
    print(f"End time: {segment['end']:.2f}")
    print(f"{segment['speaker']}")
    print(f"{segment['text']}")
    print("")






