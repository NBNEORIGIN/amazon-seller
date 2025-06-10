from llama_cpp.convert import convert_model
import os

def convert_to_gguf():
    """Convert Llama model to GGUF format"""
    input_dir = os.path.expanduser("~/.llama/checkpoints/Llama3.2-1B")
    input_file = os.path.join(input_dir, "consolidated.00.pth")
    output_file = os.path.join(input_dir, "model.gguf")

    try:
        print(f"Converting model from {input_file} to {output_file}...")
        convert_model(
            input_file,
            output_file,
            vocab_size=32000,
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
        print("Model conversion complete!")
        return True
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return False

if __name__ == "__main__":
    convert_to_gguf()
