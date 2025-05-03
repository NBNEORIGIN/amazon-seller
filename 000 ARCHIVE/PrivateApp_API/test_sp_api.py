from sp_api.api import Orders
from sp_api.base import Marketplaces, SellingApiException
import os
from dotenv import load_dotenv

# Load .env from the current directory
load_dotenv()

try:
    orders = Orders(
        marketplace=Marketplaces.UK,  # Change if you want another region
        refresh_token=os.getenv('REFRESH_TOKEN'),
        lwa_app_id=os.getenv('LWA_APP_ID'),
        lwa_client_secret=os.getenv('LWA_CLIENT_SECRET'),
        aws_secret_key=os.getenv('AWS_SECRET_KEY'),
        aws_access_key=os.getenv('AWS_ACCESS_KEY'),
        role_arn=os.getenv('ROLE_ARN')  # Only needed if using a role
    )
    result = orders.get_orders(CreatedAfter='2024-04-01T00:00:00Z')
    print(result.payload)
except SellingApiException as ex:
    print("API Exception:", ex)
except Exception as e:
    print("General Exception:", e)