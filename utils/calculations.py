"""
Financial calculations and metrics
"""
import pandas as pd
from datetime import datetime, timedelta

def calculate_metrics(payments_df, work_df, income_df):
    """Calculate key financial metrics"""
    
    metrics = {}
    
    # Total received
    metrics['total_received'] = payments_df['Amount'].sum() if not payments_df.empty else 0
    
    # This month received
    current_month = datetime.now().month
    current_year = datetime.now().year
    this_month = payments_df[
        (payments_df['Date'].dt.month == current_month) &
        (payments_df['Date'].dt.year == current_year)
    ]
    metrics['month_received'] = this_month['Amount'].sum() if not this_month.empty else 0
    
    # Pending payments
    pending = work_df[work_df['Status'] == 'Pending']
    metrics['pending'] = pending['Amount'].sum() if not pending.empty else 0
    
    # Projected income
    projected = work_df[work_df['Status'] == 'Projected']
    metrics['projected'] = projected['Amount'].sum() if not projected.empty else 0
    
    # Average payment
    metrics['avg_payment'] = payments_df['Amount'].mean() if not payments_df.empty else 0
    
    # Payment count
    metrics['payment_count'] = len(payments_df)
    
    return metrics

def forecast_next_month(payments_df):
    """Forecast next month's income based on historical average"""
    if payments_df.empty:
        return 0
    
    # Get last 3 months average
    three_months_ago = datetime.now() - timedelta(days=90)
    recent = payments_df[payments_df['Date'] >= three_months_ago]
    
    if recent.empty:
        return 0
    
    avg_daily = recent['Amount'].sum() / 90
    return avg_daily * 30

def identify_pending_payments(work_df, days_threshold=30):
    """Identify payments pending over threshold days"""
    if work_df.empty:
        return pd.DataFrame()
    
    pending = work_df[work_df['Status'] == 'Pending'].copy()
    
    if pending.empty:
        return pd.DataFrame()
    
    pending['days_pending'] = (datetime.now() - pending['Date']).dt.days
    overdue = pending[pending['days_pending'] > days_threshold]
    
    return overdue.sort_values('days_pending', ascending=False)
