from api_client import AmazonReturnsAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_api_connection():
    try:
        api = AmazonReturnsAPI()
        # Try to get return data for the last 30 days
        response = api.request_return_report()
        logger.info("Successfully requested return report!")
        logger.info(f"Response: {response}")
        return True
    except Exception as e:
        logger.error(f"Error testing API connection: {e}")
        return False

if __name__ == "__main__":
    test_api_connection()
