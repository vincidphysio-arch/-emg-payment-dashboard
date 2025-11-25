import streamlit as st
import pandas as pd
from utils.data_loader import load_google_sheets_data
from utils.calculations import calculate_metrics
from utils.charts import create_payment_timeline, create_income_breakdown
from datetime import datetime

# Page config
st.set_page_config(page_title="EMG Payment Dashboard", page_icon="🏥", layout="wide")

# Custom CSS for colorful cards
st.markdown("""
<style>
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .card-teal {
        background: linear-gradient(135deg, #20B2AA, #008B8B);
    }
    .card-purple {
        background: linear-gradient(135deg, #9370DB, #6B48FF);
    }
    .card-blue {
        background: linear-gradient(135deg, #4169E1, #1E90FF);
    }
    .card-pink {
        background: linear-gradient(135deg, #FF1493, #C71585);
    }
    .card-title {
        font-size: 14px;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    .card-value {
        font-size: 32px;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background-color: #1a1a2e;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio("", ["🏠 Home", "📊 Kitchener Tracker", "💰 Expense Tracker", "📈 Future Income", "🧾 Tax Center"], label_visibility="collapsed")

# Main content
st.title("🏥 EMG Payment Dashboard")

# Refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# Load data
with st.spinner('Fetching latest data from Google Sheets...'):
    master_df = load_google_sheets_data("Master_Income")
    payments_df = load_google_sheets_data("Payments")

if not master_df.empty:
    metrics = calculate_metrics(payments_df, master_df, master_df)
    
    # Calculate time-based metrics
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    current_quarter = (current_month - 1) // 3 + 1
    
    # Earnings Overview section
    st.markdown("### 💵 Earnings Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card card-teal">
            <div class="card-title">💰 Total Earnings</div>
            <div class="card-value">${metrics['total_received']:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        quarter_amount = metrics['total_received'] * 0.25  # Placeholder
        st.markdown(f'''
        <div class="metric-card card-purple">
            <div class="card-title">📅 This Quarter</div>
            <div class="card-value">${quarter_amount:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        year_amount = metrics['total_received'] * 0.85  # Placeholder
        st.markdown(f'''
        <div class="metric-card card-blue">
            <div class="card-title">📆 This Year</div>
            <div class="card-value">${year_amount:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        month_amount = metrics.get('avg_payment', 0) * 4  # Approximate monthly
        st.markdown(f'''
        <div class="metric-card card-pink">
            <div class="card-title">⭐ THIS MONTH</div>
            <div class="card-value">${month_amount:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts section
    st.markdown("### 📈 Monthly Earnings Trend")
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        timeline_fig = create_payment_timeline(payments_df, master_df)
        st.plotly_chart(timeline_fig, use_container_width=True)
    
    with col_chart2:
        st.subheader("Income by Doctor")
        pie_fig = create_income_breakdown(payments_df)
        st.plotly_chart(pie_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed log
    st.subheader("📋 Detailed Master Log")
    st.dataframe(
        master_df[['Date', 'Doctor', 'Type', 'Amount', 'Status']].sort_values('Date', ascending=False),
        use_container_width=True
    )
else:
    st.error("Unable to load data from Google Sheets. Please check your connection.")
