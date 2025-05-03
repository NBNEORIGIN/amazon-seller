import os
import json
import torch
from pathlib import Path
from transformers import LlamaConfig, LlamaForCausalLM, LlamaTokenizer

def convert_llama_to_hf(llama_dir):
    """Convert Llama model to Hugging Face format"""
    llama_dir = Path(llama_dir)
    hf_dir = llama_dir.parent / f"{llama_dir.name}-hf"
    
    # Load params
    with open(llama_dir / "params.json", "r") as f:
        params = json.load(f)
    
    # Create config
    config = LlamaConfig(
        vocab_size=32000,  # Standard for Llama
        hidden_size=4096,
        intermediate_size=11008,
        num_hidden_layers=32,
        num_attention_heads=32,
        max_position_embeddings=4096,
        rms_norm_eps=1e-6,
        pad_token_id=0,
        bos_token_id=1,
        eos_token_id=2,
    )
    
    # Save config
    os.makedirs(hf_dir, exist_ok=True)
    config.save_pretrained(hf_dir)
    
    # Load and convert model weights
    state_dict = torch.load(llama_dir / "consolidated.00.pth", map_location="cpu")
    
    # Create model
    model = LlamaForCausalLM(config)
    model.load_state_dict(state_dict, strict=False)
    
    # Save model
    model.save_pretrained(hf_dir)
    
    # Copy tokenizer
    tokenizer = LlamaTokenizer.from_pretrained(llama_dir)
    tokenizer.save_pretrained(hf_dir)
    
    print(f"Model converted and saved to {hf_dir}")

if __name__ == "__main__":
    llama_dir = os.path.expanduser("~/.llama/checkpoints/Llama3.2-3B-Instruct")
    convert_llama_to_hf(llama_dir)
