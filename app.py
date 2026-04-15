import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import gspread

# --- APP CONFIG ---
st.set_page_config(page_title="Pro Calculator", layout="wide")

# --- CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIDEBAR: SHEET MANAGEMENT ---
st.sidebar.title("Project Management")
sheet_name = st.sidebar.text_input("Project/Sheet Name", value="General_Calculations")

# --- CALCULATOR LOGIC ---
st.title("Advanced Calculator")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Inputs")
    val_a = st.number_input("Value A", value=0.0)
    val_b = st.number_input("Value B", value=0.0)
    operation = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])
    
    if operation == "Add":
        res = val_a + val_b
    elif operation == "Subtract":
        res = val_a - val_b
    elif operation == "Multiply":
        res = val_a * val_b
    else:
        res = val_a / val_b if val_b != 0 else 0.0

    st.metric("Result", res)

# --- SAVE LOGIC ---
    if st.button("Save Calculation to Sheet"):
        new_data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Project": sheet_name,
            "Value_A": val_a,
            "Operation": operation,
            "Value_B": val_b,
            "Result": res
        }
        
        try:
            # Reaching one level deeper to get the actual gspread client
            # Try this first:
            client = conn.client._client 
            
            # If that fails with an error, try this instead:
            # client = conn._client._client
            
            sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
            ss = client.open_by_url(sheet_url)
            
            try:
                ws = ss.worksheet(sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                ws = ss.add_worksheet(title=sheet_name, rows="100", cols="20")
                ws.append_row(list(new_data.keys())) 
                st.toast(f"New sheet '{sheet_name}' created!")

            ws.append_row(list(new_data.values()))
            st.success(f"Saved to {sheet_name}!")
            st.cache_data.clear() 
            
        except Exception as e:
            st.error(f"Error: {e}")

            # 3. Append the data
            ws.append_row(list(new_data.values()))
            st.success(f"Saved to {sheet_name}!")
            st.cache_data.clear() 
            
        except Exception as e:
            st.error(f"Error saving to Google Sheets: {e}")
            # If '.client' failed again, try '._client' below:
            # client = conn._client

# --- VIEW & DELETE ---
with col2:
    st.subheader("Sheet History")
    # Wrap this in a button or auto-refresh
    if st.button("Refresh Data"):
        st.cache_data.clear()

    try:
        # We use ttl=0 or clear cache to ensure colleagues see each other's updates
        df = conn.read(worksheet=sheet_name, ttl=0)
        st.dataframe(df, use_container_width=True)
    except:
        st.info("No data in this sheet yet. Save a calculation to begin!")

st.sidebar.markdown("---")
if st.sidebar.button("Clear Current Sheet"):
    try:
        # 1. Use the working client path
        # Note: If this line errors, try conn._client._client
        raw_client = conn.client._client 
        
        # 2. Open spreadsheet
        sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        ss = raw_client.open_by_url(sheet_url)
        
        # 3. Try to find the tab
        try:
            ws = ss.worksheet(sheet_name)
            # 4. Clear and reset headers
            ws.clear()
            ws.append_row(["Timestamp", "Project", "Value_A", "Operation", "Value_B", "Result"])
            
            # 5. Reset app state
            st.cache_data.clear()
            st.sidebar.success(f"Cleared {sheet_name}")
            st.rerun()
        except gspread.exceptions.WorksheetNotFound:
            st.sidebar.error("Cannot clear: This project tab does not exist yet.")
            
    except Exception as e:
        st.sidebar.error(f"System Error: {e}")
