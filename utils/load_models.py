from huggingface_hub import login
from transformers import WhisperForConditionalGeneration, WhisperTokenizer
import os
import shutil
import subprocess

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True)
        print("ffmpeg setup correctly")
    except FileNotFoundError:
        print("ffmpeg error setup")

def load_whisper_model(hf_token, model_name, whisper_model_dir):
    login(hf_token)
    os.makedirs(whisper_model_dir, exist_ok=True)
    model = WhisperForConditionalGeneration.from_pretrained(model_name, token=True)
    tokenizer = WhisperTokenizer.from_pretrained(model_name, token=True)
    model.save_pretrained(whisper_model_dir)
    tokenizer.save_pretrained(whisper_model_dir)
    print(f"Whisper model loaded, stored in: {whisper_model_dir}")

def load_whisper_faster_model(whisper_model_dir, whisper_faster_model_dir):
    os.makedirs(whisper_faster_model_dir, exist_ok=True)
    model = WhisperForConditionalGeneration.from_pretrained(whisper_model_dir)
    tokenizer = WhisperTokenizer.from_pretrained(whisper_model_dir)
    temp_model_dir = "temp_model"
    os.makedirs(temp_model_dir, exist_ok=True)
    model.save_pretrained(temp_model_dir)
    tokenizer.save_pretrained(temp_model_dir)
    command = [
        "ct2-transformers-converter",
        "--model", temp_model_dir,
        "--output_dir", whisper_faster_model_dir,
        "--force",
        "--quantization", "float16"
    ]
    subprocess.run(command, check=True)
    shutil.rmtree(temp_model_dir)
    print(f"Model transformed to Whisper faster format, stored in: {whisper_faster_model_dir}")
