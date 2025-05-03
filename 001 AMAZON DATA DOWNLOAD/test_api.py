from api_client import AmazonOrdersAPI
from datetime import datetime, timedelta

def main():
    # Create API client
    api = AmazonOrdersAPI()
    
    # Test getting orders
    try:
        # Get orders from the last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        print("\nTesting get_orders...")
        orders = api.get_orders(created_after=start_date, created_before=end_date)
        print(f"Retrieved {len(orders.get('Orders', []))} orders")
        
        # Print first order details
        if orders.get('Orders'):
            first_order = orders['Orders'][0]
            print("\nFirst order details:")
            print(f"Order ID: {first_order.get('AmazonOrderId')}")
            print(f"Order Status: {first_order.get('OrderStatus')}")
            print(f"Purchase Date: {first_order.get('PurchaseDate')}")
            
        # Test requesting a report
        print("\nTesting request_order_report...")
        report_response = api.request_order_report(start_date=start_date, end_date=end_date)
        report_id = report_response.get('reportId')
        print(f"Report ID: {report_id}")
        
        if report_id:
            # Get report status
            print("\nGetting report status...")
            report = api.get_report(report_id)
            print(f"Report Status: {report.get('processingStatus')}")
            
            # If report is done, get the document
            if report.get('processingStatus') == 'DONE':
                report_doc_id = report.get('reportDocumentId')
                if report_doc_id:
                    print("\nGetting report document...")
                    doc = api.get_report_document(report_doc_id)
                    print("Report document retrieved successfully")
                    print(f"Document URL: {doc.get('url')}")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
