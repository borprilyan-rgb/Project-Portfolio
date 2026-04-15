import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Pro Calculator", layout="wide")

# --- CONNECTION ---
# This looks for credentials in your Streamlit Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SIDEBAR: SHEET MANAGEMENT ---
st.sidebar.title("📁 Project Management")

# Let users define the sheet name
sheet_name = st.sidebar.text_input("Project/Sheet Name", value="General_Calculations")
st.sidebar.info("If the sheet name doesn't exist, it will be created on save.")

# --- CALCULATOR LOGIC ---
st.title("🔢 Advanced Calculator")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Inputs")
    val_a = st.number_input("Value A", value=0.0)
    val_b = st.number_input("Value B", value=0.0)
    operation = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])
    
    # Simple calculation logic
    if operation == "Add":
        res = val_a + val_b
    elif operation == "Subtract":
        res = val_a - val_b
    elif operation == "Multiply":
        res = val_a * val_b
    else:
        res = val_a / val_b if val_b != 0 else "Error (Div by 0)"

    st.metric("Result", res)

    # SAVE BUTTON
    if st.button("💾 Save Calculation to Sheet"):
        # Prepare the data
        new_row = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Project": sheet_name,
            "Value_A": val_a,
            "Operation": operation,
            "Value_B": val_b,
            "Result": res
        }])
        
        try:
            # Read existing data from that specific worksheet
            existing_data = conn.read(worksheet=sheet_name)
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        except:
            # If sheet doesn't exist, this is the first row
            updated_df = new_row
            
        # Write back to Google Sheets
        conn.update(worksheet=sheet_name, data=updated_df)
        st.success(f"Successfully saved to '{sheet_name}'!")

with col2:
    st.subheader("Sheet History")
    # Refresh button to pull latest data
    if st.button("🔄 Refresh History"):
        try:
            df = conn.read(worksheet=sheet_name)
            st.dataframe(df, use_container_width=True)
            
            # Download as CSV option for colleagues
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download this Sheet", data=csv, file_name=f"{sheet_name}.csv")
        except:
            st.warning("No data found in this project yet.")

# --- DELETE FUNCTION ---
st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Current Sheet"):
    # In GSheets, we 'clear' by writing an empty header-only dataframe
    empty_df = pd.DataFrame(columns=["Timestamp", "Project", "Value_A", "Operation", "Value_B", "Result"])
    conn.update(worksheet=sheet_name, data=empty_df)
    st.sidebar.success(f"Cleared {sheet_name}")
