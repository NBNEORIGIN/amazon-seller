import os
import sys
import requests
from pathlib import Path
import subprocess

def download_model():
    print("Setting up Llama 3.2 model...")

    # Create models directory
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)

    # Meta's download URL (from your email)
    base_url = "https://llama3-2-lightweight.llamameta.net/*"
    policy = "eyJTdGF0ZW1lbnQiOlt7InVuaXF1ZV9oYXNoIjoiZ29sMHluZXhyNnh2bXZxNXFvejBxaDB5IiwiUmVzb3VyY2UiOiJodHRwczpcL1wvbGxhbWEzLTItbGlnaHR3ZWlnaHQubGxhbWFtZXRhLm5ldFwvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc0NjAzMTU4MX19fV19"
    signature = "E~Slp2DGK6XTg6tRbEgyrHrFIyamxIu7~XIQGiz~0CEowrjkA10~gd59zEj64uhQ-9d-4y~COMNS3jau~ccZsEg1KEsiE3nyy5OAcTDuKYl9X02TgHyKlbyJqNNyA-Y7qs4KWG6T9CkGUaMF2tnDKZoyJ7i-tl0uzDzHju8gySZ4dW5GQL57rT5y5DW7u5hoI7cNeO8KAGOh1ksIM-A0eJw9rhgRYBOR91iImLXxfVlDyijRoGCbepFbet05ALAkx5bENYRuO8g~3R1xaWy3o6yzLZqm4q-~RpgCgzfGOPhycK9pvQ1qP7tkLXo7-zFxl3jnfb3FHIDkxvygKvmZMA__"
    key_pair_id = "K15QRJLYKIFSLZ"
    request_id = "709140034807127"

    # Construct full URL
    download_url = f"{base_url}?Policy={policy}&Signature={signature}&Key-Pair-Id={key_pair_id}&Download-Request-ID={request_id}"

    # Download model files
    model_files = [
        "config.json",
        "tokenizer.model",
        "tokenizer_config.json",
        "special_tokens_map.json",
        "pytorch_model.bin"
    ]

    model_dir = models_dir / "llama-3.2-3b-instruct"
    model_dir.mkdir(exist_ok=True)

    print(f"Downloading model files to {model_dir}...")

    for file in model_files:
        file_url = download_url.replace("*", file)
        target_path = model_dir / file

        if not target_path.exists():
            print(f"Downloading {file}...")
            try:
                response = requests.get(file_url, stream=True)
                response.raise_for_status()

                with open(target_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Successfully downloaded {file}")
            except Exception as e:
                print(f"Error downloading {file}: {str(e)}")
                return False

    print("\nModel download complete!")
    return True

if __name__ == "__main__":
    download_model()
