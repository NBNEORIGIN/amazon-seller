import pandas as pd
from pathlib import Path
from typing import List
from .models import ReturnRecord

class ReturnReportParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
    
    def parse(self) -> List[ReturnRecord]:
        """Parse Amazon return report into ReturnRecord objects"""
        if self.file_path.suffix.lower() == '.csv':
            df = pd.read_csv(self.file_path)
        else:
            df = pd.read_excel(self.file_path)
            
        records = []
        for _, row in df.iterrows():
            record = ReturnRecord(
                order_id=row.get('order_id'),
                product_id=row.get('product_id'),
                return_date=pd.to_datetime(row.get('return_date')),
                return_reason=row.get('return_reason'),
                refund_amount=float(row.get('refund_amount', 0)),
                customer_comments=row.get('customer_comments')
            )
            records.append(record)
            
        return records
