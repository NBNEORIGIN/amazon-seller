import os
from dotenv import load_dotenv
import requests

# 1. Load environment variables from .env file first
load_dotenv()

# 2. Now retrieve the variables from the environment
LWA_APP_ID = os.getenv('LWA_CLIENT_ID')
LWA_CLIENT_SECRET = os.getenv('LWA_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')

# 3. Print them for debugging
print("LWA_CLIENT_ID:", LWA_APP_ID)
print("LWA_CLIENT_SECRET:", "SET" if LWA_CLIENT_SECRET else "NOT SET")
print("REFRESH_TOKEN:", "SET" if REFRESH_TOKEN else "NOT SET")

def get_lwa_access_token():
    response = requests.post(
        "https://api.amazon.com/auth/o2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
            "client_id": LWA_APP_ID,
            "client_secret": LWA_CLIENT_SECRET
        }
    )
    print("LWA Token Response:", response.status_code, response.text)
    response.raise_for_status()
    return response.json()['access_token']

if not all([LWA_APP_ID, LWA_CLIENT_SECRET, REFRESH_TOKEN]):
    print("ERROR: One or more environment variables are missing.")
    print("Please check your .env file and variable names.")
else:
    access_token = get_lwa_access_token()
    print("Access Token:", access_token)