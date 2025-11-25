"""
Data loader module for Google Sheets integration
"""
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st

def load_google_sheets_data(sheet_name):
    """
    Load data from Google Sheets using service account credentials
    
    Args:
        sheet_name (str): Name of the worksheet tab
    
    Returns:
        pd.DataFrame: Data from the specified sheet
    """
    try:
        # Define scope
        scope = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        # Load credentials from Streamlit secrets
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope
        )
        
        # Authorize and open spreadsheet
        client = gspread.authorize(credentials)
        spreadsheet_id = st.secrets["sheets"]["spreadsheet_id"]
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)
        
        # Get all values and convert to DataFrame
        data = worksheet.get_all_values()
        if not data:
            return pd.DataFrame()
        
        headers = data[0]
        rows = data[1:]
        df = pd.DataFrame(rows, columns=headers)
        
        # Type conversions
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
        
        if 'Amount' in df.columns:
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        
        return df
        
    except Exception as e:
        st.error(f"Error loading {sheet_name}: {str(e)}")
        return pd.DataFrame()

def get_spreadsheet_info():
    """Get basic info about the connected spreadsheet"""
    try:
        scope = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope
        )
        
        client = gspread.authorize(credentials)
        spreadsheet_id = st.secrets["sheets"]["spreadsheet_id"]
        spreadsheet = client.open_by_key(spreadsheet_id)
        
        return {
            'title': spreadsheet.title,
            'url': spreadsheet.url,
            'sheets': [ws.title for ws in spreadsheet.worksheets()]
        }
    except:
        return None
