import whisperx

def generate_diarization(hf_token, device, audio, result):
  diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token, device=device)
  diarize_segments = diarize_model(audio)
  diarize_model(audio, min_speakers=1, max_speakers=2)
  result = whisperx.assign_word_speakers(diarize_segments, result)
  return result