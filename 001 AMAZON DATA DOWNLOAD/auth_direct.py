import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import requests
import base64
from urllib.parse import urlencode

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
        
    # Define the scopes we need
    scopes = [
        "orders:read",
        "orders:write",
        "reports:read",
        "reports:write",
        "catalog:read",
        "inventory:read"
    ]
    
    # Construct the authorization URL
    auth_params = {
        'application_id': 'amzn1.sp.solution.5bbdc64a-885f-43f7-ba9e-23b4a99dd87d',  # SP-API application ID
        'version': 'beta',
        'state': 'State123',  # Can be any random string
        'scopes': ','.join(scopes)
    }
    
    auth_url = f"https://sellercentral.amazon.com/apps/authorize/consent?{urlencode(auth_params)}"
    
    print("\nFollow these steps:")
    print("1. Copy and paste this URL into your browser:")
    print(f"\n{auth_url}\n")
    print("2. Log in to Seller Central if needed")
    print("3. You'll be redirected to example.com with an error (this is expected)")
    print("4. Copy the ENTIRE URL from your browser's address bar")
    print("5. Paste it here and press Enter:")
    
    redirect_url = input("\nPaste the redirect URL here: ").strip()
    
    try:
        # Extract the authorization code from the redirect URL
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(redirect_url)
        params = parse_qs(parsed.query)
        
        if 'spapi_oauth_code' in params:
            auth_code = params['spapi_oauth_code'][0]
        else:
            print("No authorization code found in URL. Available parameters:")
            for key, value in params.items():
                print(f"{key}: {value[0]}")
            return
        
        # Exchange the authorization code for tokens
        token_url = 'https://api.amazon.com/auth/o2/token'
        print(f"\nExchanging authorization code for tokens...")
        
        # Create basic auth header
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode('ascii')
        base64_auth = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {base64_auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': 'https://example.com/callback'
        }
        
        response = requests.post(token_url, headers=headers, data=data)
        tokens = response.json()
        
        if 'refresh_token' in tokens:
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
        else:
            print("\nError: No refresh token in response")
            print(f"Response: {tokens}")
        
    except Exception as e:
        print(f"\nError getting tokens: {str(e)}")

if __name__ == "__main__":
    main()
