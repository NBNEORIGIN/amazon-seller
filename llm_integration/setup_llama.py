import os
import sys
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def setup_llama():
    print("Setting up Llama-2-7B-Chat...")
    
    # Create model directory
    os.makedirs("models", exist_ok=True)
    
    # Download the model
    model_id = "meta-llama/Llama-2-7b-chat-hf"
    
    try:
        # First, try to load the tokenizer
        print("Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        tokenizer.save_pretrained("models/llama-2-7b-chat")
        
        print("Downloading model...")
        # Download the model with 4-bit quantization
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            load_in_4bit=True,
            device_map="auto"
        )
        model.save_pretrained("models/llama-2-7b-chat")
        
        print("Model setup complete!")
        return True
        
    except Exception as e:
        print(f"Error setting up model: {str(e)}")
        return False

if __name__ == "__main__":
    setup_llama()
