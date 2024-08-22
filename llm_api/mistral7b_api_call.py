from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
from utils.utils_settings import HF_TOKEN

login(HF_TOKEN)

def generate_response(prompt):
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3", use_fast=False)
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
    max_length = 500

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=max_length, return_attention_mask=True)
    output = model.generate(**inputs, max_new_tokens=500, pad_token_id=tokenizer.eos_token_id)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print("Generated Response:", generated_text)