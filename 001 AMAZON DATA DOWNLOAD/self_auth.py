from sp_api.api import Orders, Reports
from sp_api.base import Marketplaces
from sp_api.auth import AccessTokenClient
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load environment variables
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
    
    # Set up environment variables for SP-API
    os.environ['LWA_APP_ID'] = os.getenv('SP_API_CLIENT_ID')
    os.environ['LWA_CLIENT_SECRET'] = os.getenv('SP_API_CLIENT_SECRET')
    os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY')
    os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_KEY')
    os.environ['SP_API_ROLE_ARN'] = os.getenv('ROLE_ARN')
    
    # Debug environment variables
    print("\nEnvironment variables:")
    print(f"LWA_APP_ID: {os.environ.get('LWA_APP_ID')}")
    print(f"LWA_CLIENT_SECRET: {os.environ.get('LWA_CLIENT_SECRET')}")
    print(f"AWS_ACCESS_KEY_ID: {os.environ.get('AWS_ACCESS_KEY_ID')}")
    print(f"AWS_SECRET_ACCESS_KEY: {os.environ.get('AWS_SECRET_ACCESS_KEY')}")
    print(f"SP_API_ROLE_ARN: {os.environ.get('SP_API_ROLE_ARN')}")
    
    try:
        print("\nGetting access token...")
        
        # Get access token
        access_token_client = AccessTokenClient()
        access_token = access_token_client.get_auth_token()
        print(f"Got access token: {access_token}")
        
        # Try to make a simple API call to test credentials
        print("\nTesting API access...")
        orders_api = Orders(
            marketplace=Marketplaces.US
        )
        
        # Get orders for the last 7 days
        response = orders_api.get_orders(
            CreatedAfter='2025-04-22T00:00:00Z',
            CreatedBefore='2025-04-29T00:00:00Z'
        )
        
        print("\nAPI call successful!")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"\nError testing API: {str(e)}")
        if hasattr(e, 'error_response'):
            print(f"Error response: {e.error_response}")

if __name__ == "__main__":
    main()
