import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import gspread

# --- APP CONFIG ---
st.set_page_config(page_title="Project Budget Estimator", layout="wide")

# --- CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIDEBAR: SHEET MANAGEMENT ---
st.sidebar.title("Project Management")
sheet_name = st.sidebar.text_input("Project/Sheet Name", value="RWI_PalmBeach_Budget")

# --- CALCULATOR LOGIC ---
st.title("🏗️ Project Budget Calculator")
st.markdown("Estimate and log Hard Costs and Soft Costs based on the master concept comparison.")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("Cost Item Input")
    
    # Adapted inputs based on the uploaded CSV structure
    category = st.selectbox("Cost Category", ["HARD COST", "SOFT COST"])
    
    # Pre-populated descriptions based on standard items in the CSV
    description_options = [
        "PRELIMINARIES WORKS", "EARTHWORKS", "FOUNDATIONS", "STRUCTURAL WORKS", 
        "ARCHITECTURAL WORKS", "F F & E", "M.E.P WORKS", "UTILITY CONNECTION", 
        "EXTERNAL WORKS", "FACILITY", "CONTINGENCIES", "CONSULTANCY SERVICES FEE", 
        "QS SERVICES", "PROJECT MANAGEMENT SERVICES", "INSURANCE COVERAGE", "Other (Custom)"
    ]
    description = st.selectbox("Description", description_options)
    
    if description == "Other (Custom)":
        description = st.text_input("Enter Custom Description")

    col1_a, col1_b = st.columns(2)
    with col1_a:
        qty = st.number_input("Quantity (QTY)", value=0.0, format="%.4f")
    with col1_b:
        # Pre-populated units based on the CSV
        unit = st.selectbox("Unit", ["m2 GBA", "m2 GFA", "m2", "unit", "bh", "Room", "%", "bln", "ls", "m'"])

    rate = st.number_input("Rate (IDR)", value=0.0, format="%.2f")
    
    # --- CALCULATION ---
    # Note: If using percentage (%), enter QTY as the percentage number (e.g., 5) and Rate as the base cost / 100.
    total_cost = qty * rate

    st.metric("Total Estimated Cost (IDR)", f"Rp {total_cost:,.2f}")

    # --- SAVE LOGIC ---
    if st.button("💾 Save Calculation to Sheet"):
        # Prepare the new 9-column row
        new_row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sheet_name,
            category,
            description,
            qty,
            unit,
            rate,
            total_cost,
            "Active"  # The status column is now at index 8 (9th column)
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
                # Updated headers to match the new construction variables
                ws.append_row(["Timestamp", "Project", "Category", "Description", "QTY", "Unit", "Rate", "Total_Cost", "Status"])
                st.toast(f"New sheet '{sheet_name}' created!")

            ws.append_row(new_row)
            st.success(f"Saved {description} to {sheet_name}!")
            st.cache_data.clear() 
            
        except Exception as e:
            st.error(f"Error saving to Google Sheets: {e}")

# --- VIEW & ARCHIVE LOGIC ---
with col2:
    st.subheader("Budget Sheet History")
    
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
            
            # Show the table with specific formatting for easier reading
            st.dataframe(
                active_df[['Row_ID', 'Category', 'Description', 'QTY', 'Unit', 'Rate', 'Total_Cost']], 
                use_container_width=True,
                hide_index=True
            )
            
            st.divider()
            
            # ARCHIVE SECTION
            row_to_archive = st.number_input("Enter Row_ID to hide (Not for Use)", min_value=2, step=1)
            
            if st.button("🚫 Mark as Not for Use"):
                client = conn.client._client
                sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
                ss = client.open_by_url(sheet_url)
                ws = ss.worksheet(sheet_name)
                
                # Column 9 is the new 'Status' column based on our new structure
                ws.update_cell(int(row_to_archive), 9, "Archived")
                
                st.cache_data.clear()
                st.warning(f"Row {row_to_archive} is now hidden.")
                st.rerun()
        else:
            st.info("The sheet format is being updated. Please save a new calculation.")

    except Exception:
        st.info("No active budget calculations found in this project yet.")
