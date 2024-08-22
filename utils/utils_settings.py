#API 
HF_TOKEN = "created_huggingface_token"

#MODEL
MODEL_NAME = "openai/whisper-tiny.en" 
DEVICE = "cuda"
BATCH_SIZE = 16
COMPUTE_TYPE = "float16"
LANGUAGE = "en"

#TRANSCRIPTION
REFERENCE_DIR = './local_input_batch/reference_batch/'
AUDIO_DIR = './local_input_batch/audio_batch'
WHISPER_MODEL_DIR = "./models/whisper_model/"
WHISPER_FASTER_MODEL_DIR = "./models/whisper_faster_model/"