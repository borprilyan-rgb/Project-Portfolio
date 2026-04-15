import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import gspread  # Moved to top

# --- APP CONFIG ---
st.set_page_config(page_title="Pro Calculator", layout="wide")

# --- CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIDEBAR: SHEET MANAGEMENT ---
st.sidebar.title("📁 Project Management")
sheet_name = st.sidebar.text_input("Project/Sheet Name", value="General_Calculations")

# --- CALCULATOR LOGIC ---
st.title("🔢 Advanced Calculator")

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
        new_data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Project": sheet_name,
            "Value_A": val_a,
            "Operation": operation,
            "Value_B": val_b,
            "Result": res
        }
        
        # Access the raw client to handle worksheet creation
        client = conn.client.client
        ss = client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
        
        try:
            # Check if tab exists
            ws = ss.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            # Create it if it doesn't
            ws = ss.add_worksheet(title=sheet_name, rows="100", cols="20")
            ws.append_row(list(new_data.keys())) # Add headers
            st.toast(f"New sheet '{sheet_name}' created!")

        # Append the new row
        ws.append_row(list(new_data.values()))
        st.success(f"Saved to {sheet_name}!")

# --- VIEW & DELETE ---
with col2:
    st.subheader("Sheet History")
    try:
        df = conn.read(worksheet=sheet_name)
        st.dataframe(df, use_container_width=True)
    except:
        st.info("No data in this sheet yet.")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Current Sheet"):
    try:
        client = conn.client.client
        ss = client.open_by_url(st.secrets["connections"]["gsheets"]["spreadsheet"])
        ws = ss.worksheet(sheet_name)
        # Clear everything but the header
        ws.clear()
        ws.append_row(["Timestamp", "Project", "Value_A", "Operation", "Value_B", "Result"])
        st.sidebar.success(f"Cleared {sheet_name}")
        st.rerun()
    except Exception as e:
        st.sidebar.error("Could not clear sheet.")
