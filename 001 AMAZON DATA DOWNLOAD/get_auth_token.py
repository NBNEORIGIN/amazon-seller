from sp_api.auth import AuthorizationCode
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
    client_secret = os.getenv('SP_API_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        logger.error("Missing client ID or secret in .env file")
        return
        
    auth = AuthorizationCode(
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Define the scopes we need
    scopes = [
        "sellingpartnerapi:orders_read",
        "sellingpartnerapi:orders_write",
        "sellingpartnerapi:reports_read",
        "sellingpartnerapi:reports_write",
        "sellingpartnerapi:catalogs_read",
        "sellingpartnerapi:inventory_read"
    ]
    
    # Get the authorization URL
    auth_url = auth.get_authorization_url(
        scopes=scopes,
        state="State123",  # Can be any random string
        redirect_uri="https://example.com/callback"  # This is just a placeholder
    )
    
    print("\nFollow these steps:")
    print("1. Copy and paste this URL into your browser:")
    print(f"\n{auth_url}\n")
    print("2. Log in to Seller Central if needed")
    print("3. You'll be redirected to example.com with an error (this is expected)")
    print("4. Copy the ENTIRE URL from your browser's address bar")
    print("5. Paste it here and press Enter:")
    
    redirect_url = input("\nPaste the redirect URL here: ").strip()
    
    try:
        # Exchange the authorization code for tokens
        tokens = auth.get_tokens_from_code(redirect_url)
        
        print("\nGot tokens successfully!")
        print(f"Refresh Token: {tokens['refresh_token']}")
        
        # Update the .env file
        with open(env_path, 'r') as f:
            lines = f.readlines()
            
        with open(env_path, 'w') as f:
            for line in lines:
                if line.startswith('SP_API_REFRESH_TOKEN='):
                    f.write(f'SP_API_REFRESH_TOKEN={tokens["refresh_token"]}\n')
                else:
                    f.write(line)
                    
        print("\nUpdated .env file with new refresh token")
        print("You can now run test_api.py again")
        
    except Exception as e:
        print(f"\nError getting tokens: {str(e)}")

if __name__ == "__main__":
    main()
