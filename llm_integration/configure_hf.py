import os
from huggingface_hub import login
import sys

def setup_token(token=None):
    print("Setting up Hugging Face authentication...")
    
    # Get token from argument or environment
    token = token or os.environ.get("HF_TOKEN")
    if not token:
        print("No token provided. Please provide token as argument or set HF_TOKEN environment variable")
        print("Get your token from https://huggingface.co/settings/tokens")
        return False
    
    try:
        # Login with token
        login(token=token)
        print("\nSuccessfully logged in to Hugging Face!")
        return True
    except Exception as e:
        print(f"Error during login: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python configure_hf.py <huggingface_token>")
        sys.exit(1)
    setup_token(sys.argv[1])
