import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="EMG Payment Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 EMG Payment Dashboard")
st.markdown("### Kitchener - Live Financial Overview")

# Sidebar
with st.sidebar:
    st.header("🎛️ Controls")
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    st.markdown("---")
    st.info(f"**Last Updated:**\n{datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Received", "$45,840")
col2.metric("⏳ Pending", "$3,200")
col3.metric("📊 Projected", "$15,400")
col4.metric("📈 Avg Payment", "$760")

# Sample data
st.subheader("Recent Payments")
sample_data = pd.DataFrame({
    'Date': ['18/11/2025', '11/11/2025', '05/11/2025'],
    'Sender': ['MILJAN TRIPIC', 'MILJAN TRIPIC', 'MILJAN TRIPIC'],
    'Amount': [770, 840, 840],
    'Doctor': ['Dr. Tripic', 'Dr. Tripic', 'Dr. Tripic']
})

st.dataframe(sample_data, use_container_width=True)

st.success("✅ Dashboard loaded successfully!")
