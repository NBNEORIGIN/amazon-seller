from setuptools import setup, find_packages

setup(
    name='sp_api_client',
    version='1.0.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'requests>=2.25.1',
        'backoff>=2.2.1',
        'boto3>=1.26.0',
        'python-dotenv>=0.19.0'
    ],
    description='A Python SDK for Amazon Selling Partner API',
    long_description='A Python SDK for interacting with the Amazon Selling Partner API',
    long_description_content_type='text/markdown',
    url='https://github.com/amzn/selling-partner-api-models'
)
