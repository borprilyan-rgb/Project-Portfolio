import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Complex Construction Calculator", layout="wide")

st.title("🏗️ Project Dimension Calculator")
st.markdown("---")

# --- STEP 1: INPUT BOXES (User Changeable) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📐 Area Metrics")
    land_area = st.number_input("Land Area (m²)", min_value=0.0, step=1.0)
    gba = st.number_input("GBA (Gross Building Area) (m²)", min_value=0.0, step=1.0)
    gfa = st.number_input("GFA (Gross Floor Area) (m²)", min_value=0.0, step=1.0)
    sgfa = st.number_input("SGFA (Semi-Gross Floor Area) (m²)", min_value=0.0, step=1.0)
    facade = st.number_input("Facade (m²)", min_value=0.0, step=1.0)

with col2:
    st.subheader("🚪 Units & Interior")
    rooms = st.number_input("Room (unit)", min_value=0, step=1)
    door_glass = st.number_input("Door Glass (unit)", min_value=0, step=1)
    pintu_kayu = st.number_input("Pintu Kayu (unit)", min_value=0, step=1)
    pintu_besi = st.number_input("Pintu Besi (unit)", min_value=0, step=1)
    lobby_interior = st.number_input("Lobby Interior (m²)", min_value=0.0, step=1.0)

with col3:
    st.subheader("🌳 External & Infrastructure")
    rooftop = st.number_input("Rooftop (m²)", min_value=0.0, step=1.0)
    facilities = st.number_input("Facilities (m²)", min_value=0.0, step=1.0)
    landscape = st.number_input("External/Landscape (m²)", min_value=0.0, step=1.0)
    boundary_wall = st.number_input("Boundary Wall & Gate (m')", min_value=0.0, step=1.0)
    access_road = st.number_input("Access Road (m')", min_value=0.0, step=1.0)

st.markdown("---")

st.markdown("---")

# --- STEP 2: UNIT RATES (Changeable Numbers) ---
st.subheader("💰 Unit Rates")
col_rate1, col_rate2 = st.columns(2)

with col_rate1:
    # This is the "changeable number" for Earthwork
    rate_earthwork = st.number_input("Earthwork Rate (per GBA m²)", min_value=0.0, value=100.0, step=1.0)

# --- STEP 3: CALCULATIONS ---
# Calculation for Earthwork: GBA (from Step 1) x Rate (from Step 2)
total_earthwork = gba * rate_earthwork

# --- STEP 4: HARD COST INFORMATION TABLE ---
st.header("📊 Hard Cost")

# We define the data, including our new Earthwork row
hard_cost_data = {
    "Description": ["1. Preliminary Works", "2. Earthwork"],
    "Basis": ["5% of Hard Cost", f"{gba} m² (GBA) x {rate_earthwork}"],
    "Amount": [0.0, total_earthwork] # Preliminary remains 0 until we have the full Hard Cost logic
}

df_hc = pd.DataFrame(hard_cost_data)

# Formatting for display
df_hc_display = df_hc.copy()
df_hc_display["Amount"] = df_hc_display["Amount"].map("{:,.2f}".format)

st.table(df_hc_display)

# --- STEP 2: HARD COST INFORMATION TABLE (Non-changeable) ---
st.header("📊 Hard Cost")

# Initializing the table with Preliminary Works
# 'Amount' is 0 for now as we don't have the other components to calculate the 5%
hard_cost_data = {
    "Description": ["1. Preliminary Works"],
    "Basis": ["5% of Hard Cost"],
    "Amount": [0.0] 
}

df_hc = pd.DataFrame(hard_cost_data)

# Displaying the information table
st.table(df_hc)

st.info("Preliminary Works added to the Hard Cost table. What is the next item?")
