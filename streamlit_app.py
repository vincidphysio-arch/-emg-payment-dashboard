import streamlit as st
import pandas as pd
from utils.data_loader import load_google_sheets_data
from utils.calculations import calculate_metrics
from utils.charts import create_payment_timeline, create_income_breakdown
from datetime import datetime

# Page config
st.set_page_config(page_title="EMG Payment Dashboard", page_icon="💰", layout="wide")

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
    .card-orange {
        background: linear-gradient(135deg, #FF8C00, #FF6347);
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
    page = st.radio("", ["🏠 Home", "🏥 Kitchener Tracker", "🏛️ London Tracker", "💸 Expense Tracker", "📈 Future Income", "📊 Tax Center"], label_visibility="collapsed")

# Load data from both sheets
try:
    payments_df = load_google_sheets_data("Payments")
    master_df = load_google_sheets_data("Master_Income")
except Exception as e:
    st.error(f"Error loading data: {e}")
    payments_df = pd.DataFrame()
    master_df = pd.DataFrame()

# Define location filters
KITCHENER_DOCTORS = ['Dr. Tripic', 'Dr. Cartagena']
LONDON_DOCTORS = ['Dr. Tugalov']

# Filter data by location
def filter_by_location(df, doctors):
    if df.empty:
        return df
    return df[df['Doctor'].isin(doctors)] if 'Doctor' in df.columns else df

kitchener_payments = filter_by_location(payments_df, KITCHENER_DOCTORS)
london_payments = filter_by_location(payments_df, LONDON_DOCTORS)
kitchener_master = filter_by_location(master_df, KITCHENER_DOCTORS)
london_master = filter_by_location(master_df, LONDON_DOCTORS)

# Refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# Calculate metrics for each location
all_metrics = calculate_metrics(payments_df, master_df)
kitchener_metrics = calculate_metrics(kitchener_payments, kitchener_master)
london_metrics = calculate_metrics(london_payments, london_master)

if page == "🏠 Home":
    st.title("💰 EMG Payment Dashboard")
    st.markdown("### 📊 Combined Earnings Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card card-teal">
            <div class="card-title">💰 Total Earnings</div>
            <div class="card-value">${all_metrics['total_received']:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        quarter_amount = all_metrics['total_received'] * 0.25
        st.markdown(f'''
        <div class="metric-card card-purple">
            <div class="card-title">📅 This Quarter</div>
            <div class="card-value">${quarter_amount:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        year_amount = all_metrics['total_received'] * 0.85
        st.markdown(f'''
        <div class="metric-card card-blue">
            <div class="card-title">📅 This Year</div>
            <div class="card-value">${year_amount:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        month_amount = all_metrics.get('avg_payment', 0) * 4
        st.markdown(f'''
        <div class="metric-card card-pink">
            <div class="card-title">⭐ THIS MONTH</div>
            <div class="card-value">${month_amount:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Location Summary Cards
    st.markdown("### 📍 Income by Location")
    loc_col1, loc_col2 = st.columns(2)
    with loc_col1:
        st.markdown(f'''
        <div class="metric-card card-orange">
            <div class="card-title">🏥 Kitchener Total</div>
            <div class="card-value">${kitchener_metrics['total_received']:,.2f}</div>
            <div style="font-size: 12px; margin-top: 10px;">Dr. Tripic & Dr. Cartagena</div>
        </div>
        ''', unsafe_allow_html=True)
    with loc_col2:
        st.markdown(f'''
        <div class="metric-card card-purple">
            <div class="card-title">🏛️ London Total</div>
            <div class="card-value">${london_metrics['total_received']:,.2f}</div>
            <div style="font-size: 12px; margin-top: 10px;">Dr. Tugalov</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📈 Monthly Earnings Trend")
    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        timeline_fig = create_payment_timeline(payments_df, master_df)
        st.plotly_chart(timeline_fig, use_container_width=True)
    with col_chart2:
        st.subheader("Income by Doctor")
        pie_fig = create_income_breakdown(payments_df)
        st.plotly_chart(pie_fig, use_container_width=True)

elif page == "🏥 Kitchener Tracker":
    st.title("🏥 Kitchener Income Tracker")
    st.markdown("**Doctors:** Dr. Tripic & Dr. Cartagena")
    
    st.markdown("### 📊 Kitchener Earnings Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card card-teal">
            <div class="card-title">💰 Total Earnings</div>
            <div class="card-value">${kitchener_metrics['total_received']:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="metric-card card-purple">
            <div class="card-title">⏳ Pending</div>
            <div class="card-value">${kitchener_metrics.get('pending', 0):,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="metric-card card-blue">
            <div class="card-title">📊 Projected</div>
            <div class="card-value">${kitchener_metrics.get('projected', 0):,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
        <div class="metric-card card-pink">
            <div class="card-title">📈 Avg Payment</div>
            <div class="card-value">${kitchener_metrics.get('avg_payment', 0):,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📈 Kitchener Payment Timeline")
    if not kitchener_payments.empty:
        timeline_fig = create_payment_timeline(kitchener_payments, kitchener_master)
        st.plotly_chart(timeline_fig, use_container_width=True)
    
    col_chart1, col_chart2 = st.columns([1, 1])
    with col_chart1:
        st.subheader("Income by Doctor")
        if not kitchener_payments.empty:
            pie_fig = create_income_breakdown(kitchener_payments)
            st.plotly_chart(pie_fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📋 Kitchener Payment Log")
    if not kitchener_master.empty:
        st.dataframe(
            kitchener_master[['Date', 'Doctor', 'Type', 'Amount', 'Status']].sort_values('Date', ascending=False),
            use_container_width=True
        )
    elif not kitchener_payments.empty:
        st.dataframe(kitchener_payments, use_container_width=True)
    else:
        st.info("No Kitchener payment data available.")

elif page == "🏛️ London Tracker":
    st.title("🏛️ London Income Tracker")
    st.markdown("**Doctor:** Dr. Tugalov")
    
    st.markdown("### 📊 London Earnings Overview")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'''
        <div class="metric-card card-teal">
            <div class="card-title">💰 Total Earnings</div>
            <div class="card-value">${london_metrics['total_received']:,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="metric-card card-purple">
            <div class="card-title">⏳ Pending</div>
            <div class="card-value">${london_metrics.get('pending', 0):,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="metric-card card-blue">
            <div class="card-title">📊 Projected</div>
            <div class="card-value">${london_metrics.get('projected', 0):,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col4:
        st.markdown(f'''
        <div class="metric-card card-pink">
            <div class="card-title">📈 Avg Payment</div>
            <div class="card-value">${london_metrics.get('avg_payment', 0):,.2f}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📈 London Payment Timeline")
    if not london_payments.empty:
        timeline_fig = create_payment_timeline(london_payments, london_master)
        st.plotly_chart(timeline_fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📋 London Payment Log")
    if not london_master.empty:
        st.dataframe(
            london_master[['Date', 'Doctor', 'Type', 'Amount', 'Status']].sort_values('Date', ascending=False),
            use_container_width=True
        )
    elif not london_payments.empty:
        st.dataframe(london_payments, use_container_width=True)
    else:
        st.info("No London payment data available.")

elif page == "💸 Expense Tracker":
    st.title("💸 Expense Tracker")
    st.info("Expense tracking coming soon!")

elif page == "📈 Future Income":
    st.title("📈 Future Income Projections")
    st.info("Future income projections coming soon!")

elif page == "📊 Tax Center":
    st.title("📊 Tax Center")
    st.info("Tax calculations and reports coming soon!")
