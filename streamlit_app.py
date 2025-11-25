import streamlit as st
import pandas as pd
from utils.data_loader import load_google_sheets_data
from utils.calculations import calculate_metrics
from utils.charts import create_payment_timeline, create_income_breakdown

st.set_page_config(page_title="EMG Payment Dashboard", page_icon="🏥", layout="wide")

st.title("🏥 EMG Payment Dashboard")

# 1. Load Real Data
with st.spinner('Fetching latest data from Google Sheets...'):
    # Load 'Master_Income' for the timeline/projections
    master_df = load_google_sheets_data("Master_Income")
    
    # Load 'Payments' for the confirmed money
    payments_df = load_google_sheets_data("Payments")

if not master_df.empty:
    # 2. Calculate Real Metrics
    # Filter Master DF into 'Pending' and 'Projected' for the metrics
    metrics = calculate_metrics(payments_df, master_df, master_df)
    
    # 3. Display Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Received", f"${metrics['total_received']:,.0f}")
    col2.metric("⏳ Pending (Tugalov)", f"${metrics['pending']:,.0f}")
    col3.metric("📊 Projected (Kitchener)", f"${metrics['projected']:,.0f}")
    col4.metric("📈 Avg Payment", f"${metrics['avg_payment']:,.0f}")

    # 4. Charts
    st.markdown("---")
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("Payment Timeline (Past & Future)")
        # Pass master_df as 'work_df' because it contains the schedule
        timeline_fig = create_payment_timeline(payments_df, master_df)
        st.plotly_chart(timeline_fig, use_container_width=True)
        
    with col_chart2:
        st.subheader("Income by Doctor")
        pie_fig = create_income_breakdown(payments_df)
        st.plotly_chart(pie_fig, use_container_width=True)

    # 5. Recent Data Table
    st.subheader("📋 Detailed Master Log")
    # Show the cleaned master list
    st.dataframe(
        master_df[['Date', 'Doctor', 'Type', 'Amount', 'Status']].sort_values('Date', ascending=False),
        use_container_width=True,
        hide_index=True
    )

else:
    st.error("Could not load data. Check your secrets.toml and Sheet Name.")
