"""
Data loader module for Google Sheets integration
"""
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st

def load_google_sheets_data(sheet_name):
    """Load data and normalize column names"""
    try:
        # Define scope
        scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        
        # Load credentials
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope
        )
        
        client = gspread.authorize(credentials)
        spreadsheet_id = st.secrets["sheets"]["spreadsheet_id"]
        worksheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
        
        data = worksheet.get_all_values()
        if not data:
            return pd.DataFrame()
        
        # Create DataFrame
        headers = data[0]
        rows = data[1:]
        df = pd.DataFrame(rows, columns=headers)
        
        # --- FIX 1: Rename Columns to Match Code Expectations ---
        # Maps 'Total Earned' from Sheet -> 'Amount' for Python
        column_mapping = {
            'Total Earned': 'Amount',
            'Doctor / Location': 'Doctor',
            'Patients Seen / Type': 'Type'
        }
        df = df.rename(columns=column_mapping)
        
        # --- FIX 2: Clean Currency Strings ("$750.00" -> 750.00) ---
        if 'Amount' in df.columns:
            # Remove '$', ',', and empty strings
            df['Amount'] = df['Amount'].astype(str).str.replace('$', '', regex=False)
            df['Amount'] = df['Amount'].str.replace(',', '', regex=False)
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)

        # --- FIX 3: Flexible Date Parsing ---
        if 'Date' in df.columns:
            # Try ISO format first (YYYY-MM-DD), then DD/MM/YYYY
            df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
            
        return df
        
    except Exception as e:
        st.error(f"Error loading {sheet_name}: {str(e)}")
        return pd.DataFrame()
