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
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.subheader("📅 Date Range")
    start_date = st.date_input("Start", datetime.now() - timedelta(days=90))
    end_date = st.date_input("End", datetime.now() + timedelta(days=180))
    
    st.markdown("---")
    st.info(f"**Last Updated:**\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Metrics Row
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Received", "$45,840", "+$2,500")
with col2:
    st.metric("⏳ Pending", "$3,200", "-$500")
with col3:
    st.metric("📊 Projected", "$15,400", "+$1,200")
with col4:
    st.metric("📈 Avg Payment", "$760", "+$50")

st.info("📝 **Setup Required**: Add Google Sheets credentials in Streamlit Cloud settings to enable live data.")

# Tabs
tab1, tab2, tab3 = st.tabs(["📅 Timeline", "💵 Payments", "📋 Work Log"])

with tab1:
    st.subheader("Payment Timeline - Past, Present & Future")
    st.info("Connect Google Sheets to see your complete payment timeline")
    
    # Sample chart placeholder
    sample_dates = pd.date_range(start='2024-10-01', end='2025-02-28', freq='W')
    sample_amounts = [840, 770, 660, 720, 840, 900, 780, 840, 770, 660, 600, 720, 840, 780, 660, 720, 840, 900, 780, 840]
    
    chart_data = pd.DataFrame({
        'Date': sample_dates[:len(sample_amounts)],
        'Amount': sample_amounts
    })
    st.line_chart(chart_data.set_index('Date'))

with tab2:
    st.subheader("Payment History")
    
    # Sample payment data
    sample_data = pd.DataFrame({
        'Date': ['18/11/2025', '11/11/2025', '05/11/2025', '28/10/2025', '21/10/2025'],
        'Sender': ['MILJAN TRIPIC', 'MILJAN TRIPIC', 'MILJAN TRIPIC', 'MILJAN TRIPIC', 'MILJAN TRIPIC'],
        'Amount': [770, 840, 840, 840, 840],
        'Doctor': ['Dr. Tripic', 'Dr. Tripic', 'Dr. Tripic', 'Dr. Tripic', 'Dr. Tripic'],
        'Status': ['Auto-Logged', 'Auto-Logged', 'Auto-Logged', 'Auto-Logged', 'Auto-Logged']
    })
    
    st.dataframe(sample_data, use_container_width=True, hide_index=True)
    
    st.download_button(
        label="📥 Download CSV",
        data=sample_data.to_csv(index=False),
        file_name="payments_export.csv",
        mime="text/csv"
    )

with tab3:
    st.subheader("Work Schedule & Payment Status")
    
    # Sample work log
    work_log = pd.DataFrame({
        'Date': ['26/11/2024', '03/12/2024', '10/12/2024', '17/12/2024'],
        'Doctor': ['Dr. Tripic', 'Dr. Tripic', 'Dr. Cartagena', 'Dr. Tripic'],
        'Type': ['Scheduled Work', 'Scheduled Work', 'Scheduled Work', 'Scheduled Work'],
        'Rate': ['Est. Lump Sum', 'Est. Lump Sum', 'Est. Lump Sum', 'Est. Lump Sum'],
        'Amount': [720, 660, 900, 720],
        'Status': ['✓ Paid', '⏳ Pending', '📊 Projected', '📊 Projected']
    })
    
    st.dataframe(work_log, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("🔗 Data will sync with Google Sheets once credentials are configured • Built with Streamlit")
