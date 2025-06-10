import os
import sys
from pathlib import Path

def setup_model():
    print("Setting up Llama 3.2 model...")

    # Create models directory if it doesn't exist
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)

    # Run llama CLI commands
    try:
        # List available models
        os.system('llama model list --show-all')

        # Download the 3B-Instruct model
        print("\nDownloading Llama-3.2-3B-Instruct model...")
        os.system('llama model download --source meta --model-id Llama-3.2-3B-Instruct')

        print("\nSetup complete! The model should now be downloaded.")
        return True
    except Exception as e:
        print(f"Error during setup: {str(e)}")
        return False

if __name__ == "__main__":
    setup_model()
