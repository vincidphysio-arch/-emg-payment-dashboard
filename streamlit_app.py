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
    .card-teal { background: linear-gradient(135deg, #20B2AA, #008B8B); }
    .card-purple { background: linear-gradient(135deg, #9370DB, #6B48FF); }
    .card-blue { background: linear-gradient(135deg, #4169E1, #1E90FF); }
    .card-pink { background: linear-gradient(135deg, #FF1493, #C71585); }
    .card-orange { background: linear-gradient(135deg, #FF8C00, #FF6347); }
    .card-title { font-size: 14px; opacity: 0.9; margin-bottom: 5px; }
    .card-value { font-size: 32px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio("", ["🏠 Home", "🏥 Kitchener Tracker", "🏛️ London Tracker", "💸 Expense Tracker", "📈 Future Income", "📊 Tax Center"], label_visibility="collapsed")

# Cached data loading function
@st.cache_data(ttl=300)
def get_all_data():
    try:
        payments = load_google_sheets_data("Payments")
        master = load_google_sheets_data("Master_Income")
        return payments, master, None
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame(), str(e)

# Load data with caching
payments_df, master_df, load_error = get_all_data()

# Refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

if load_error:
    st.error(f"Error loading data: {load_error}")
    st.info("Please wait a moment and click Refresh Data to try again.")
    st.stop()

# Define location filters
KITCHENER_DOCTORS = ['Dr. Tripic', 'Dr. Cartagena']
LONDON_DOCTORS = ['Dr. Tugalov']

def filter_by_location(df, doctors):
    if df.empty: return df
    return df[df['Doctor'].isin(doctors)] if 'Doctor' in df.columns else df

def safe_metrics(payments, master):
    try:
        return calculate_metrics(payments, master)
    except:
        return {'total_received': 0, 'pending': 0, 'projected': 0, 'avg_payment': 0}

# Page Content
if page == "🏠 Home":
    st.title("💰 EMG Payment Dashboard")
    
    all_metrics = safe_metrics(payments_df, master_df)
    kit_pay = filter_by_location(payments_df, KITCHENER_DOCTORS)
    lon_pay = filter_by_location(payments_df, LONDON_DOCTORS)
    kit_metrics = safe_metrics(kit_pay, filter_by_location(master_df, KITCHENER_DOCTORS))
    lon_metrics = safe_metrics(lon_pay, filter_by_location(master_df, LONDON_DOCTORS))
    
    st.markdown("### 📊 Combined Earnings Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-card card-teal"><div class="card-title">💰 Total Earnings</div><div class="card-value">${all_metrics["total_received"]:,.2f}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card card-purple"><div class="card-title">📅 This Quarter</div><div class="card-value">${all_metrics["total_received"]*0.25:,.2f}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card card-blue"><div class="card-title">📅 This Year</div><div class="card-value">${all_metrics["total_received"]*0.85:,.2f}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card card-pink"><div class="card-title">⭐ THIS MONTH</div><div class="card-value">${all_metrics.get("avg_payment",0)*4:,.2f}</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📍 Income by Location")
    l1, l2 = st.columns(2)
    l1.markdown(f'<div class="metric-card card-orange"><div class="card-title">🏥 Kitchener Total</div><div class="card-value">${kit_metrics["total_received"]:,.2f}</div><div style="font-size:12px;margin-top:10px">Dr. Tripic & Dr. Cartagena</div></div>', unsafe_allow_html=True)
    l2.markdown(f'<div class="metric-card card-purple"><div class="card-title">🏛️ London Total</div><div class="card-value">${lon_metrics["total_received"]:,.2f}</div><div style="font-size:12px;margin-top:10px">Dr. Tugalov</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📈 Monthly Earnings Trend")
    ch1, ch2 = st.columns([2, 1])
    with ch1:
        st.plotly_chart(create_payment_timeline(payments_df, master_df), use_container_width=True)
    with ch2:
        st.subheader("Income by Doctor")
        st.plotly_chart(create_income_breakdown(payments_df), use_container_width=True)

elif page == "🏥 Kitchener Tracker":
    st.title("🏥 Kitchener Income Tracker")
    st.markdown("**Doctors:** Dr. Tripic & Dr. Cartagena")
    
    kit_pay = filter_by_location(payments_df, KITCHENER_DOCTORS)
    kit_master = filter_by_location(master_df, KITCHENER_DOCTORS)
    metrics = safe_metrics(kit_pay, kit_master)
    
    st.markdown("### 📊 Kitchener Earnings Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-card card-teal"><div class="card-title">💰 Total</div><div class="card-value">${metrics["total_received"]:,.2f}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card card-purple"><div class="card-title">⏳ Pending</div><div class="card-value">${metrics.get("pending",0):,.2f}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card card-blue"><div class="card-title">📊 Projected</div><div class="card-value">${metrics.get("projected",0):,.2f}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card card-pink"><div class="card-title">📈 Avg</div><div class="card-value">${metrics.get("avg_payment",0):,.2f}</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if not kit_pay.empty:
        st.markdown("### 📈 Payment Timeline")
        st.plotly_chart(create_payment_timeline(kit_pay, kit_master), use_container_width=True)
        st.subheader("Income by Doctor")
        st.plotly_chart(create_income_breakdown(kit_pay), use_container_width=True)
    
    st.markdown("---")
    st.subheader("📋 Kitchener Payment Log")
    if not kit_pay.empty:
        st.dataframe(kit_pay, use_container_width=True)
    else:
        st.info("No Kitchener payment data available.")

elif page == "🏛️ London Tracker":
    st.title("🏛️ London Income Tracker")
    st.markdown("**Doctor:** Dr. Tugalov")
    
    lon_pay = filter_by_location(payments_df, LONDON_DOCTORS)
    lon_master = filter_by_location(master_df, LONDON_DOCTORS)
    metrics = safe_metrics(lon_pay, lon_master)
    
    st.markdown("### 📊 London Earnings Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-card card-teal"><div class="card-title">💰 Total</div><div class="card-value">${metrics["total_received"]:,.2f}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card card-purple"><div class="card-title">⏳ Pending</div><div class="card-value">${metrics.get("pending",0):,.2f}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card card-blue"><div class="card-title">📊 Projected</div><div class="card-value">${metrics.get("projected",0):,.2f}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card card-pink"><div class="card-title">📈 Avg</div><div class="card-value">${metrics.get("avg_payment",0):,.2f}</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if not lon_pay.empty:
        st.markdown("### 📈 Payment Timeline")
        st.plotly_chart(create_payment_timeline(lon_pay, lon_master), use_container_width=True)
    
    st.markdown("---")
    st.subheader("📋 London Payment Log")
    if not lon_pay.empty:
        st.dataframe(lon_pay, use_container_width=True)
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
