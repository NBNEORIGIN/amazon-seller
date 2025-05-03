class SPAPIConfig:
    def __init__(self, client_id, client_secret, refresh_token=None, region="EU", scope=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.region = region
        self.scope = scope
        
        # Map regions to endpoints
        region_endpoints = {
            'EU': 'sellingpartnerapi-eu.amazon.com',
            'NA': 'sellingpartnerapi-na.amazon.com',
            'FE': 'sellingpartnerapi-fe.amazon.com',
            'SANDBOX': 'sandbox.sellingpartnerapi-na.amazon.com'
        }
        
        # Set endpoint based on region
        if region.upper() not in region_endpoints:
            raise ValueError(f"Invalid region: {region}. Must be one of {list(region_endpoints.keys())}")
            
        self.endpoint = f"https://{region_endpoints[region.upper()]}"
