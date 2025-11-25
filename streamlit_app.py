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
    .metric-card { padding: 20px; border-radius: 10px; color: white; text-align: center; }
    .card-teal { background: linear-gradient(135deg, #15aea, #008b8b); }
    .card-purple { background: linear-gradient(135deg, #932ad, #6d28d9ff); }
    .card-blue { background: linear-gradient(135deg, #15aea, #1f85ff); }
    .card-pink { background: linear-gradient(135deg, #15aea, #ff1493); }
    .card-orange { background: linear-gradient(135deg, #ff6b00, #ff7547); }
    .card-title { font-size: 14px; opacity: 0.9; margin-bottom: 5px; }
    .card-value { font-size: 32px; font-weight: bold; }
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio("", ["🏠 Home", "🏥 Kitchener Tracker", "🏛️ London Tracker", "💸 Expense Tracker", "📈 Future Income", "📊 Tax Center"], label_visibility="collapsed")

# Cached data loading
@st.cache_data(ttl=300)
def get_all_data():
    try:
        payments = load_google_sheets_data("Payments")
        master = load_google_sheets_data("Master_Income")
        expenses = load_google_sheets_data("Expenses")
        return payments, master, expenses, None
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), str(e)

payments_df, master_df, expenses_df, load_error = get_all_data()

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

if load_error:
    st.error(f"Error loading data: {load_error}")
    st.stop()

# Location filters
KITCHENER_DOCTORS = ['Dr. Tripic', 'Dr. Cartagena']
LONDON_DOCTORS = ['Dr. Tugalov']

def filter_by_location(df, location):
    if location == "kitchener":
        if 'Doctor' in df.columns:
            return df[df['Doctor'].isin(KITCHENER_DOCTORS)]
    elif location == "london":
        if 'Doctor' in df.columns:
            return df[df['Doctor'].isin(LONDON_DOCTORS)]
    return df

def get_metrics(payments, master):
    try:
        total_received = payments['Amount'].sum() if 'Amount' in payments.columns else 0
        avg_payment = payments['Amount'].mean() if 'Amount' in payments.columns else 0
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        if 'Date' in payments.columns:
            payments['Date'] = pd.to_datetime(payments['Date'], errors='coerce')
            month_received = payments[(payments['Date'].dt.month == current_month) & (payments['Date'].dt.year == current_year)]['Amount'].sum()
        else:
            month_received = 0
        
        if 'Status' in master.columns and 'Amount' in master.columns:
            pending = master[master['Status'] == 'Pending']['Amount'].sum()
            projected = master[master['Status'] == 'Projected']['Amount'].sum()
        else:
            pending = projected = 0
        
        return {
            'total_received': total_received,
            'avg_payment': avg_payment,
            'month_received': month_received,
            'pending': pending,
            'projected': projected
        }
    except Exception as e:
        st.warning(f"Metrics calculation issue: {e}")
        return {'total_received': 0, 'avg_payment': 0, 'month_received': 0, 'pending': 0, 'projected': 0}

# PAGE: Home
if page == "🏠 Home":
    st.title("💰 EMG Payment Dashboard")
    
    all_metrics = get_metrics(payments_df, master_df)
    
    st.markdown("### 📊 Combined Earnings Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='metric-card card-teal'><div class='card-title'>Total Earnings</div><div class='card-value'>${all_metrics['total_received']:,.2f}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card card-purple'><div class='card-title'>Pending</div><div class='card-value'>${all_metrics['pending']:,.2f}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card card-blue'><div class='card-title'>Projected</div><div class='card-value'>${all_metrics['projected']:,.2f}</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='metric-card card-pink'><div class='card-title'>This Month</div><div class='card-value'>${all_metrics['month_received']:,.2f}</div></div>", unsafe_allow_html=True)
    
    st.markdown("### 💼 Income by Location")
    kit_payments = filter_by_location(payments_df, "kitchener")
    lon_payments = filter_by_location(payments_df, "london")
    
    col1, col2 = st.columns(2)
    col1.markdown(f"<div class='metric-card card-orange'><div class='card-title'>Kitchener Total</div><div class='card-value'>${kit_payments['Amount'].sum():,.2f}</div></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-card card-pink'><div class='card-title'>London Total</div><div class='card-value'>${lon_payments['Amount'].sum():,.2f}</div></div>", unsafe_allow_html=True)
    
    if not payments_df.empty:
        st.markdown("### 📈 Charts")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_payment_timeline(payments_df, use_container_width=True))
        with col2:
            st.subheader("Income by Doctor")
            st.plotly_chart(create_income_breakdown(payments_df, use_container_width=True))
        
        st.markdown("### 📋 Payment Log")
        if not payments_df.empty:
            st.dataframe(payments_df, use_container_width=True)

# PAGE: Kitchener Tracker
elif page == "🏥 Kitchener Tracker":
    st.title("🏥 Kitchener Income Tracker")
    st.markdown("**Doctors:** Dr. Tripic & Dr. Cartagena")
    
    kit_pay = filter_by_location(payments_df, "kitchener")
    kit_master = filter_by_location(master_df, "kitchener")
    kit_metrics = get_metrics(kit_pay, kit_master)
    
    st.markdown("### 📊 Kitchener Earnings Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='metric-card card-teal'><div class='card-title'>Total</div><div class='card-value'>${kit_metrics['total_received']:,.2f}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card card-purple'><div class='card-title'>Pending</div><div class='card-value'>${kit_metrics['pending']:,.2f}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card card-blue'><div class='card-title'>Projected</div><div class='card-value'>${kit_metrics['projected']:,.2f}</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='metric-card card-pink'><div class='card-title'>Avg/Payment</div><div class='card-value'>${kit_metrics['avg_payment']:,.2f}</div></div>", unsafe_allow_html=True)
    
    if not kit_pay.empty:
        st.markdown("### 💳 Kitchener Payment Log")
        st.dataframe(kit_pay, use_container_width=True)
    else:
        st.info("No Kitchener data available.")

# PAGE: London Tracker
elif page == "🏛️ London Tracker":
    st.title("🏛️ London Income Tracker")
    st.markdown("**Doctor:** Dr. Tugalov")
    
    lon_pay = filter_by_location(payments_df, "london")
    lon_master = filter_by_location(master_df, "london")
    lon_metrics = get_metrics(lon_pay, lon_master)
    
    st.markdown("### 📊 London Earnings Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='metric-card card-teal'><div class='card-title'>Total</div><div class='card-value'>${lon_metrics['total_received']:,.2f}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card card-purple'><div class='card-title'>Pending</div><div class='card-value'>${lon_metrics['pending']:,.2f}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card card-blue'><div class='card-title'>Projected</div><div class='card-value'>${lon_metrics['projected']:,.2f}</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='metric-card card-pink'><div class='card-title'>Avg/Payment</div><div class='card-value'>${lon_metrics['avg_payment']:,.2f}</div></div>", unsafe_allow_html=True)
    
    if not lon_pay.empty:
        st.markdown("### 💳 London Payment Log")
        st.dataframe(lon_pay, use_container_width=True)
    else:
        st.info("No London data available.")

# PAGE: Expense Tracker
elif page == "💸 Expense Tracker":
    st.title("💸 Expense Tracker")
    
    if not expenses_df.empty and 'Amount' in expenses_df.columns:
        total_expenses = expenses_df['Amount'].sum()
        monthly_avg = total_expenses / 12 if total_expenses > 0 else 0
        
        st.markdown("### 💰 Expense Summary")
        c1, c2 = st.columns(2)
        c1.markdown(f"<div class='metric-card card-orange'><div class='card-title'>Total Expenses</div><div class='card-value'>${total_expenses:,.2f}</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card card-purple'><div class='card-title'>Monthly Avg</div><div class='card-value'>${monthly_avg:,.2f}</div></div>", unsafe_allow_html=True)
        
        # Category breakdown
        if 'Category' in expenses_df.columns:
            st.markdown("### 📂 Expenses by Category")
            category_summary = expenses_df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
            st.bar_chart(category_summary)
        
        st.markdown("### 📋 Expense Details")
        st.dataframe(expenses_df.sort_values('Date', ascending=False) if 'Date' in expenses_df.columns else expenses_df, use_container_width=True)
    else:
        st.info("No expense data available.")

# PAGE: Future Income
elif page == "📈 Future Income":
    st.title("📈 Future Income Projections")
    
    if not master_df.empty:
        projected_df = master_df[master_df['Status'] == 'Projected'] if 'Status' in master_df.columns else master_df
        
        if not projected_df.empty and 'Amount' in projected_df.columns:
            total_projected = projected_df['Amount'].sum()
            count_projected = len(projected_df)
            
            st.markdown("### 📊 Projected Income Summary")
            c1, c2 = st.columns(2)
            c1.markdown(f"<div class='metric-card card-blue'><div class='card-title'>Total Projected</div><div class='card-value'>${total_projected:,.2f}</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card card-teal'><div class='card-title'>Upcoming Items</div><div class='card-value'>{count_projected}</div></div>", unsafe_allow_html=True)
            
            st.markdown("### 📅 Upcoming Income")
            st.dataframe(projected_df.sort_values('Date') if 'Date' in projected_df.columns else projected_df, use_container_width=True)
        else:
            st.info("No projected income data available.")
    else:
        st.info("No master income data available.")

# PAGE: Tax Center
elif page == "📊 Tax Center":
    st.title("📊 Tax Center")
    
    if not payments_df.empty:
        total_income = payments_df['Amount'].sum() if 'Amount' in payments_df.columns else 0
        total_expenses = expenses_df['Amount'].sum() if 'Amount' in expenses_df.columns else 0
        net_income = total_income - total_expenses
        estimated_tax_rate = 0.23  # Ontario self-employed ~23%
        estimated_tax = net_income * estimated_tax_rate
        
        st.markdown("### 💼 Income & Tax Summary")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='metric-card card-teal'><div class='card-title'>Gross Income</div><div class='card-value'>${total_income:,.2f}</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='metric-card card-orange'><div class='card-title'>Total Expenses</div><div class='card-value'>${total_expenses:,.2f}</div></div>", unsafe_allow_html=True)
        c3.markdown(f"
