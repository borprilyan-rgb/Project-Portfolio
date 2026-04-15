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
if st.button("💾 Save Calculation"):
    new_data = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        sheet_name,
        val_a,
        operation,
        val_b,
        res,
        "Active"  # <--- New 'Status' column
    ]
    
    client = conn.client._client
    ss = client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
    
    try:
        ws = ss.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        ws = ss.add_worksheet(title=sheet_name, rows="100", cols="20")
        ws.append_row(["Timestamp", "Project", "Value_A", "Operation", "Value_B", "Result", "Status"])
    
    ws.append_row(new_data)
    st.success("Saved!")
    st.cache_data.clear()

# --- 2. UPDATED VIEW & MARK AS "NOT FOR USE" ---
with col2:
    st.subheader("Sheet History")
    try:
        df = conn.read(worksheet=sheet_name, ttl=0)
        
        # Filter: Only show the "Active" ones to the user
        active_df = df[df['Status'] == 'Active'].copy()
        
        # Add the Row_ID for referencing
        active_df['Row_ID'] = active_df.index + 2
        
        # Show the filtered list
        st.dataframe(active_df, use_container_width=True)
        
        st.divider()
        row_to_archive = st.number_input("Enter Row_ID to mark as 'Not for Use'", min_value=2, step=1)
        
        if st.button("🚫 Mark as Not for Use"):
            client = conn.client._client
            ss = client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
            ws = ss.worksheet(sheet_name)
            
            # Find the column index for 'Status' (it's the 7th column)
            # update_cell(row, col, value)
            ws.update_cell(int(row_to_archive), 7, "Archived")
            
            st.cache_data.clear()
            st.warning(f"Row {row_to_archive} is now hidden.")
            st.rerun()

    except Exception as e:
        st.info("No active calculations found.")
