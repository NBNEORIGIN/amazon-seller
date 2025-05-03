from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from pathlib import Path

def download_model():
    print("Setting up Llama 3.2 model...")
    
    # Create models directory
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)
    
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    output_dir = models_dir / "tinyllama-1.1b-chat"
    
    try:
        print(f"Downloading model {model_name}...")
        
        # Download tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(output_dir)
        print("Tokenizer downloaded successfully")
        
        # Download model
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            device_map="auto"
        )
        model.save_pretrained(output_dir)
        print("Model downloaded successfully")
        
        print("\nModel setup complete!")
        return True
    except Exception as e:
        print(f"Error during setup: {str(e)}")
        return False

if __name__ == "__main__":
    download_model()
