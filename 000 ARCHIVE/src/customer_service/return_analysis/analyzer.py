import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ReturnMetrics:
    return_rate: float
    total_returns: int
    total_orders: int
    top_reasons: List[Tuple[str, int]]
    cost_impact: float

class ReturnAnalyzer:
    def __init__(self, report_path: str):
        self.report_path = Path(report_path)
        self.data = None

    def load_data(self):
        """Load return report data from CSV/Excel file"""
        if self.report_path.suffix.lower() == '.csv':
            self.data = pd.read_csv(self.report_path)
        else:
            self.data = pd.read_excel(self.report_path)
        
    def calculate_metrics(self, product_id: str = None) -> ReturnMetrics:
        """Calculate return metrics for overall or specific product"""
        if self.data is None:
            self.load_data()
            
        df = self.data if product_id is None else self.data[self.data['product_id'] == product_id]
        
        total_returns = len(df)
        total_orders = df['total_orders'].sum() if 'total_orders' in df.columns else 0
        return_rate = (total_returns / total_orders * 100) if total_orders > 0 else 0
        
        # Analyze return reasons
        reasons = df['return_reason'].value_counts().head(5)
        top_reasons = [(reason, count) for reason, count in reasons.items()]
        
        # Calculate cost impact
        cost_impact = df['refund_amount'].sum() if 'refund_amount' in df.columns else 0
        
        return ReturnMetrics(
            return_rate=return_rate,
            total_returns=total_returns,
            total_orders=total_orders,
            top_reasons=top_reasons,
            cost_impact=cost_impact
        )
    
    def identify_high_risk_products(self, threshold: float = 10.0) -> List[Dict]:
        """Identify products with return rates above threshold"""
        if self.data is None:
            self.load_data()
            
        products = []
        for product_id in self.data['product_id'].unique():
            metrics = self.calculate_metrics(product_id)
            if metrics.return_rate > threshold:
                products.append({
                    'product_id': product_id,
                    'return_rate': metrics.return_rate,
                    'total_returns': metrics.total_returns,
                    'top_reasons': metrics.top_reasons,
                    'cost_impact': metrics.cost_impact
                })
        
        return sorted(products, key=lambda x: x['return_rate'], reverse=True)

    def generate_recommendations(self, product_id: str = None) -> List[str]:
        """Generate actionable recommendations based on return patterns"""
        metrics = self.calculate_metrics(product_id)
        recommendations = []
        
        # Return rate based recommendations
        if metrics.return_rate > 20:
            recommendations.append("CRITICAL: Return rate is extremely high. Consider temporary pause in sales.")
        elif metrics.return_rate > 10:
            recommendations.append("WARNING: Return rate above acceptable threshold. Review product details and listings.")
        
        # Analyze return reasons and provide specific recommendations
        for reason, count in metrics.top_reasons:
            if 'size' in reason.lower():
                recommendations.append("Update size charts and add more detailed measurements")
            elif 'quality' in reason.lower():
                recommendations.append("Review product quality control process and supplier relationship")
            elif 'not as described' in reason.lower():
                recommendations.append("Audit product listings for accuracy and add more detailed photos")
            elif 'damaged' in reason.lower():
                recommendations.append("Review packaging and shipping methods")
                
        return recommendations
