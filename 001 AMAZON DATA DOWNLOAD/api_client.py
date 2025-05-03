from sp_api.api import Orders, Reports, Tokens
from sp_api.base import Marketplaces, SellingApiException
from sp_api.base.reportTypes import ReportType
from datetime import datetime, timedelta
import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AmazonOrdersAPI:
    def __init__(self):
        # Get the absolute path to the .env file
        env_path = Path(__file__).parent / '.env'
        logger.info(f"Loading .env file from: {env_path}")
        
        # Load .env file
        load_dotenv(env_path)
        
        # Load and validate credentials
        credentials = {
            'refresh_token': os.getenv('SP_API_REFRESH_TOKEN'),
            'lwa_app_id': os.getenv('SP_API_CLIENT_ID'),
            'lwa_client_secret': os.getenv('SP_API_CLIENT_SECRET'),
            'aws_access_key': os.getenv('AWS_ACCESS_KEY'),
            'aws_secret_key': os.getenv('AWS_SECRET_KEY'),
            'role_arn': os.getenv('ROLE_ARN'),
        }
        
        # Debug log to check credentials
        logger.info("Checking credentials:")
        for key, value in credentials.items():
            if value:
                prefix = value[:15] if len(value) > 15 else value
                logger.info(f"{key} starts with: {prefix}...")
            else:
                logger.error(f"{key} is not set!")

        # Validate credential formats
        if not credentials['lwa_app_id'].startswith('amzn1.application-oa2-client.'):
            logger.error("Invalid lwa_app_id format. Should start with 'amzn1.application-oa2-client.'")
            
        if not credentials['lwa_client_secret'].startswith('amzn1.oa2-cs.v1.'):
            logger.error("Invalid client secret format. Should start with 'amzn1.oa2-cs.v1.'")
            
        if not credentials['aws_access_key'].startswith('AKIA'):
            logger.error("AWS access key should start with 'AKIA'")
            
        if not credentials['role_arn'].startswith('arn:aws:iam::'):
            logger.error("Role ARN should start with 'arn:aws:iam::'")
        
        # Store credentials for use in API calls
        self.credentials = credentials
        
        # Get access token for self-authorization
        # Set up environment variables for SP-API
        os.environ['LWA_APP_ID'] = credentials['lwa_app_id']
        os.environ['LWA_CLIENT_SECRET'] = credentials['lwa_client_secret']
        os.environ['AWS_ACCESS_KEY_ID'] = credentials['aws_access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['aws_secret_key']
        os.environ['SP_API_ROLE_ARN'] = credentials['role_arn']
        
        # Get a new refresh token using self-authorization
        try:
            tokens_api = Tokens(credentials={
                'lwa_app_id': credentials['lwa_app_id'],
                'lwa_client_secret': credentials['lwa_client_secret'],
                'aws_access_key': credentials['aws_access_key'],
                'aws_secret_key': credentials['aws_secret_key'],
                'role_arn': credentials['role_arn']
            })
            
            # Request a new token with specific data elements
            token_response = tokens_api.create_restricted_data_token(
                restricted_resources=[
                    {
                        "method": "GET",
                        "path": "/orders/v0/orders",
                        "dataElements": ["buyerInfo", "shippingAddress"]
                    },
                    {
                        "method": "GET",
                        "path": "/reports/2020-09-04/reports",
                        "dataElements": ["reportDocumentId"]
                    }
                ]
            )
            logger.info(f"Got new token response: {token_response}")
            
            # Use the new token
            os.environ['SP_API_REFRESH_TOKEN'] = token_response['restrictedDataToken']
            self.credentials['refresh_token'] = token_response['restrictedDataToken']
        except Exception as e:
            logger.error(f"Error getting token: {str(e)}")
        
        # Set up marketplace
        self.marketplace = Marketplaces.US  # Can be changed based on need
        
    def get_orders(self, created_after: datetime = None, created_before: datetime = None):
        """Get orders from Amazon SP-API"""
        if not created_after:
            created_after = datetime.now() - timedelta(days=30)
        if not created_before:
            created_before = datetime.now()
            
        try:
            logger.info(f"Getting orders from {created_after} to {created_before}")
            
            # Create client
            orders_client = Orders(
                credentials=self.credentials,
                marketplace=Marketplaces.US
            )
            
            # Get orders
            response = orders_client.get_orders(
                CreatedAfter=created_after.isoformat(),
                CreatedBefore=created_before.isoformat(),
                MarketplaceIds=['ATVPDKIKX0DER']  # US marketplace ID
            )
            
            logger.info(f"Retrieved {len(response.payload.get('Orders', []))} orders")
            return response.payload
            
        except SellingApiException as e:
            logger.error(f"Error getting orders: {e}")
            logger.error(f"Full error details: {str(e)}")
            raise
            
    def request_order_report(self, start_date: datetime = None, end_date: datetime = None):
        """Request an order report from Amazon SP-API"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()
            
        try:
            logger.info(f"Requesting order report from {start_date} to {end_date}")
            
            # Create client
            report_client = Reports(
                credentials=self.credentials,
                marketplace=Marketplaces.US
            )
            
            # Request report
            response = report_client.create_report(
                reportType=ReportType.GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_GENERAL,
                dataStartTime=start_date.isoformat(),
                dataEndTime=end_date.isoformat(),
                marketplaceIds=['ATVPDKIKX0DER']  # US marketplace ID
            )
            
            logger.info(f"Report requested successfully. Report ID: {response.payload.get('reportId')}")
            return response.payload
            
        except SellingApiException as e:
            logger.error(f"Error requesting report: {e}")
            logger.error(f"Full error details: {str(e)}")
            raise
            
    def get_report(self, report_id: str):
        """Get a report by its ID"""
        try:
            logger.info(f"Getting report {report_id}")
            
            # Create client
            report_client = Reports(
                credentials=self.credentials,
                marketplace=Marketplaces.US
            )
            
            # Get report
            response = report_client.get_report(report_id)
            
            logger.info(f"Report retrieved successfully")
            return response.payload
            
        except SellingApiException as e:
            logger.error(f"Error getting report: {e}")
            logger.error(f"Full error details: {str(e)}")
            raise
            
    def get_report_document(self, report_document_id: str):
        """Get a report document by its ID"""
        try:
            logger.info(f"Getting report document {report_document_id}")
            
            # Create client
            report_client = Reports(
                credentials=self.credentials,
                marketplace=Marketplaces.US
            )
            
            # Get report document
            response = report_client.get_report_document(report_document_id)
            
            logger.info(f"Report document retrieved successfully")
            return response.payload
            
        except SellingApiException as e:
            logger.error(f"Error getting report document: {e}")
            logger.error(f"Full error details: {str(e)}")
            raise
