"""
Chart creation utilities using Plotly
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

def create_payment_timeline(payments_df, work_df):
    """Create timeline chart showing past, present, and future"""
    fig = go.Figure()
    
    # Add payments (past)
    if not payments_df.empty:
        fig.add_trace(go.Scatter(
            x=payments_df['Date'],
            y=payments_df['Amount'],
            mode='markers+lines',
            name='Received',
            marker=dict(size=10, color='green'),
            line=dict(color='green', width=2)
        ))
    
    # Add pending (present)
    pending = work_df[work_df['Status'] == 'Pending']
    if not pending.empty:
        fig.add_trace(go.Scatter(
            x=pending['Date'],
            y=pending['Amount'],
            mode='markers',
            name='Pending',
            marker=dict(size=12, color='orange', symbol='diamond')
        ))
    
    # Add projected (future)
    projected = work_df[work_df['Status'] == 'Projected']
    if not projected.empty:
        fig.add_trace(go.Scatter(
            x=projected['Date'],
            y=projected['Amount'],
            mode='markers',
            name='Projected',
            marker=dict(size=10, color='blue', symbol='square')
        ))
    
    # Add today line
    try:  # Try to add vline, skip if data is malformed
        fig.add_vline(
            x=datetime.now(),
            line_dash="dash",
            line_color="red",
            annotation_text="Today"
        )
            except Exception:  # Skip vline if any error occurs
        pass
    
    fig.update_layout(
        title="Payment Timeline - Past, Present & Future",
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_income_breakdown(payments_df):
    """Create pie chart of income by doctor"""
    if payments_df.empty or 'Doctor' not in payments_df.columns:
        return go.Figure()
    
    doctor_totals = payments_df.groupby('Doctor')['Amount'].sum().reset_index()
    
    fig = px.pie(
        doctor_totals,
        values='Amount',
        names='Doctor',
        title='Income Breakdown by Doctor',
        color_discrete_sequence=['#0066CC', '#FF6B6B']
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_monthly_trend(payments_df):
    """Create line chart of monthly income trend"""
    if payments_df.empty:
        return go.Figure()
    
    payments_df['YearMonth'] = payments_df['Date'].dt.to_period('M').astype(str)
    monthly = payments_df.groupby('YearMonth')['Amount'].sum().reset_index()
    
    fig = px.line(
        monthly,
        x='YearMonth',
        y='Amount',
        title='Monthly Income Trend',
        markers=True
    )
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Amount ($)",
        height=400
    )
    
    return fig

def create_doctor_comparison(payments_df):
    """Create bar chart comparing doctors"""
    if payments_df.empty or 'Doctor' not in payments_df.columns:
        return go.Figure()
    
    doctor_stats = payments_df.groupby('Doctor').agg({
        'Amount': ['sum', 'mean', 'count']
    }).round(2)
    
    doctor_stats.columns = ['Total', 'Average', 'Count']
    doctor_stats = doctor_stats.reset_index()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Total Income', 'Average Payment')
    )
    
    fig.add_trace(
        go.Bar(x=doctor_stats['Doctor'], y=doctor_stats['Total'], name='Total'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=doctor_stats['Doctor'], y=doctor_stats['Average'], name='Average'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False)
    return fig
