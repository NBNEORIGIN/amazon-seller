import os
import sys
from huggingface_hub import HfFolder, login

def setup_token():
    print("Setting up Hugging Face token...")
    token = input("Please enter your Hugging Face token: ")
    
    # Save the token
    try:
        login(token=token)
        print("Token configured successfully!")
        print("You can now run setup_llama.py to download the model.")
    except Exception as e:
        print(f"Error configuring token: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    setup_token()
