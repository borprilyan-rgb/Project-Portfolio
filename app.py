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
    if st.button("💾 Save Calculation to Sheet"):
        # We prepare the data as a list for the .append_row function
        new_row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sheet_name,
            val_a,
            operation,
            val_b,
            res,
            "Active"  # The status column
        ]
        
        try:
            # Reaching into the gspread client
            client = conn.client._client 
            sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
            ss = client.open_by_url(sheet_url)
            
            try:
                ws = ss.worksheet(sheet_name)
            except gspread.exceptions.WorksheetNotFound:
                ws = ss.add_worksheet(title=sheet_name, rows="100", cols="20")
                # Add headers including the 'Status' column
                ws.append_row(["Timestamp", "Project", "Value_A", "Operation", "Value_B", "Result", "Status"])
                st.toast(f"New sheet '{sheet_name}' created!")

            ws.append_row(new_row)
            st.success(f"Saved to {sheet_name}!")
            st.cache_data.clear() 
            
        except Exception as e:
            st.error(f"Error saving to Google Sheets: {e}")

# --- VIEW & ARCHIVE LOGIC ---
with col2:
    st.subheader("Sheet History")
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()

    try:
        # Read the sheet data
        df = conn.read(worksheet=sheet_name, ttl=0)
        
        # Filter: Only show 'Active' rows
        if "Status" in df.columns:
            active_df = df[df['Status'] == 'Active'].copy()
            # Add Row_ID (Index + 2 to match Google Sheets row numbers)
            active_df['Row_ID'] = active_df.index + 2
            
            # Show the table
            st.dataframe(active_df, use_container_width=True)
            
            st.divider()
            
            # ARCHIVE SECTION
            row_to_archive = st.number_input("Enter Row_ID to hide (Not for Use)", min_value=2, step=1)
            
            if st.button("🚫 Mark as Not for Use"):
                client = conn.client._client
                sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
                ss = client.open_by_url(sheet_url)
                ws = ss.worksheet(sheet_name)
                
                # Column 7 is the 'Status' column
                ws.update_cell(int(row_to_archive), 7, "Archived")
                
                st.cache_data.clear()
                st.warning(f"Row {row_to_archive} is now hidden.")
                st.rerun()
        else:
            st.info("The sheet format is being updated. Please save a new calculation.")

    except Exception:
        st.info("No active calculations found in this project yet.")
