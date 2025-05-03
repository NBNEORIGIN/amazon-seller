import os
from pathlib import Path
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load environment variables
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
    
    # Get credentials
    client_id = os.getenv('SP_API_CLIENT_ID')
    if not client_id:
        logger.error("SP_API_CLIENT_ID not found in .env file")
        return
        
    # Define the scopes we need
    scopes = [
        "sellingpartnerapi::notifications",
        "sellingpartnerapi::migration",
        "sellingpartnerapi::orders:read",
        "sellingpartnerapi::orders:write",
        "sellingpartnerapi::reports:read",
        "sellingpartnerapi::reports:write",
        "sellingpartnerapi::catalogs:read",
        "sellingpartnerapi::inventory:read"
    ]
    
    # Construct the OAuth URL
    oauth_url = (
        "https://sellercentral.amazon.com/apps/authorize/consent?"
        f"application_id={client_id}&"
        f"version=beta&"
        f"state=State123&"  # State can be any random string
        f"scopes={','.join(scopes)}"
    )
    
    print("\nFollow these steps:")
    print("1. Copy and paste this URL into your browser:")
    print(f"\n{oauth_url}\n")
    print("2. Log in to Seller Central if needed")
    print("3. Review and accept the permissions")
    print("4. You'll be redirected to a page with a refresh token")
    print("5. Copy the refresh token and update it in your .env file")
    
    print("\nAfter getting the refresh token:")
    print("1. Open the .env file")
    print("2. Replace the SP_API_REFRESH_TOKEN value with your new token")
    print("3. Save the file and try running test_api.py again")

if __name__ == "__main__":
    main()
