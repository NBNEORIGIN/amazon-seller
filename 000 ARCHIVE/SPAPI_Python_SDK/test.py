from sp_api.api import Orders
from sp_api.base import SellingApiException, Marketplaces
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

def main():
    # Load environment variables
    load_dotenv()
    
    # Debug environment variables
    print("\nEnvironment variables:")
    print(f"AWS_ACCESS_KEY: {os.environ.get('AWS_ACCESS_KEY')}")
    print(f"AWS_SECRET_KEY: {os.environ.get('AWS_SECRET_KEY')}")
    print(f"SP_API_CLIENT_ID: {os.environ.get('SP_API_CLIENT_ID')}")
    print(f"SP_API_CLIENT_SECRET: {os.environ.get('SP_API_CLIENT_SECRET')}")
    
    try:
        # Initialize the Orders API client
        print("\nInitializing SP-API client...")
        orders_api = Orders(
            marketplace=Marketplaces.UK,  # UK marketplace
            refresh_token=os.getenv('SP_API_REFRESH_TOKEN'),
            credentials={
                'aws_access_key': os.getenv('AWS_ACCESS_KEY'),
                'aws_secret_key': os.getenv('AWS_SECRET_KEY'),
                'role_arn': os.getenv('ROLE_ARN')
            }
        )
        
        # Get orders from the last 7 days
        print("\nFetching orders...")
        created_after = (datetime.now() - timedelta(days=7)).isoformat()
        
        orders_response = orders_api.get_orders(
            CreatedAfter=created_after,
            MarketplaceIds=[Marketplaces.UK.marketplace_id]
        )
        
        print("\nOrders API Response:")
        print(orders_response.payload)
        
    except SellingApiException as e:
        print(f"\nAPI Error: {str(e)}")
        print(f"Error Code: {e.code}")
        print(f"Error Details: {e.message}")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
