import os
import requests
import backoff
from datetime import datetime, timezone
from requests_aws4auth import AWS4Auth
import boto3
import json

class SPAPIClient:
    def __init__(self, config):
        self.config = config
        self.access_token = None
        self.token_expiry = None
        
    def _get_lwa_access_token(self):
        """Get a Login with Amazon access token using client credentials"""
        url = 'https://api.amazon.com/auth/o2/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'scope': 'sellingpartnerapi::migration'
        }
            
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data['access_token']
        self.token_expiry = datetime.now(timezone.utc).timestamp() + token_data['expires_in']
        
        return self.access_token
        
    def _get_valid_token(self):
        """Get a valid access token, refreshing if necessary"""
        now = datetime.now(timezone.utc).timestamp()
        
        if not self.access_token or not self.token_expiry or now >= self.token_expiry:
            return self._get_lwa_access_token()
            
        return self.access_token
        
    def _get_aws_auth(self):
        """Get AWS authentication"""
        aws_access_key = os.environ.get('AWS_ACCESS_KEY')
        aws_secret_key = os.environ.get('AWS_SECRET_KEY')
        role_arn = os.environ.get('ROLE_ARN')
        
        if not aws_access_key or not aws_secret_key:
            raise ValueError("AWS credentials not found in environment variables")
            
        if not role_arn:
            raise ValueError("ROLE_ARN not found in environment variables")
            
        # Map SP-API regions to AWS regions
        region_map = {
            'EU': 'eu-west-1',
            'NA': 'us-east-1',
            'FE': 'us-west-2'
        }
        
        aws_region = region_map.get(self.config.region.upper(), 'us-east-1')
        
        # Create an STS client
        sts_client = boto3.client(
            'sts',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        
        # Assume the IAM role
        assumed_role = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName='sp_api_session'
        )
        
        # Get temporary credentials
        credentials = assumed_role['Credentials']
        
        return AWS4Auth(
            credentials['AccessKeyId'],
            credentials['SecretAccessKey'],
            self.config.region.lower(),
            'execute-api',
            session_token=credentials['SessionToken']
        )
        
    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=3)
    def _make_request(self, method, path, **kwargs):
        """Make a request to the SP-API with automatic retries"""
        url = f"{self.config.endpoint}{path}"
        
        # Get AWS auth
        auth = self._get_aws_auth()
        
        # Set up headers
        headers = kwargs.pop('headers', {})
        headers.update({
            'x-amz-access-token': self._get_valid_token(),
            'Content-Type': 'application/json'
        })
        
        try:
            response = requests.request(method, url, auth=auth, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response status: {e.response.status_code}")
                print(f"Response headers: {e.response.headers}")
                print(f"Response body: {e.response.text}")
            raise
        
    def get_orders(self, marketplace_ids, created_after=None, created_before=None):
        """Get orders from SP-API directly"""
        path = '/orders/v0/orders'
        params = {
            'MarketplaceIds': ','.join(marketplace_ids)
        }
        
        if created_after:
            params['CreatedAfter'] = created_after
        if created_before:
            params['CreatedBefore'] = created_before
            
        return self._make_request('GET', path, params=params)
