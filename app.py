import streamlit as st
import pandas as pd

# 1. MUST BE FIRST: Page configuration
st.set_page_config(page_title="Complex Construction Calculator", layout="wide")

st.title("Project Dimension and Cost Calculator")
st.markdown("---")

# --- STEP 1: INPUT BOXES (Area Metrics) ---
col1, col2, col3 = st.columns(3)

def clean_num_input(label, default="0.0"):
    # Using text_input removes the +/- buttons entirely
    val = st.text_input(label, value=default)
    try:
        return float(val)
    except ValueError:
        return 0.0

with col1:
    st.subheader("Area Metrics")
    land_area = clean_num_input("Land Area (m2)")
    gba = clean_num_input("GBA (Gross Building Area) (m2)")
    gfa = clean_num_input("GFA (Gross Floor Area) (m2)")
    sgfa = clean_num_input("SGFA (Semi-Gross Floor Area) (m2)")
    facade = clean_num_input("Facade (m2)")

with col2:
    st.subheader("Units and Interior")
    rooms = clean_num_input("Room (unit)", default="0")
    door_glass = clean_num_input("Door Glass (unit)", default="0")
    pintu_kayu = clean_num_input("Pintu Kayu (unit)", default="0")
    pintu_besi = clean_num_input("Pintu Besi (unit)", default="0")
    lobby_interior = clean_num_input("Lobby Interior (m2)")

with col3:
    st.subheader("External and Infrastructure")
    rooftop = clean_num_input("Rooftop (m2)")
    facilities = clean_num_input("Facilities (m2)")
    landscape = clean_num_input("External/Landscape (m2)")
    boundary_wall = clean_num_input("Boundary Wall & Gate (m')")
    access_road = clean_num_input("Access Road (m')")

st.markdown("---")

# --- STEP 2: UNIT RATES ---
st.subheader("Unit Rates and Estimations")
col_rate1, col_rate2, col_rate3 = st.columns(3)

with col_rate1:
    rate_earthwork = st.number_input("Earthwork Rate (per GBA m2)", min_value=0.0, value=0.0)
    rate_foundation = st.number_input("Foundation Rate (per GBA m2)", min_value=0.0, value=0.0)

with col_rate2:
    rate_structural = st.number_input("Structural Work Rate (per GBA m2)", min_value=0.0, value=0.0)
    st.write("") 

with col_rate3:
    project_type = st.selectbox("Project Type", ["Hotel", "Retail", "Apartment", "Parking"])
    rate_architecture = st.number_input("Architecture Rate (per GFA m2)", min_value=0.0, value=0.0)

# --- SUB-SECTION: FACADE ---
st.markdown("#### Facade Breakdown")
st.caption("Adjust percentages to split the total Facade area (Total must be 100%)")

col_fac1, col_fac2, col_fac3 = st.columns(3)

with col_fac1:
    precast_p = st.number_input("Precast (%)", min_value=0.0, max_value=100.0, value=0.0, key="fac_pre")
    rate_precast = st.number_input("Precast Rate (per m2)", min_value=0.0, value=0.0, key="rate_pre")

with col_fac2:
    window_p = st.number_input("Window Wall (%)", min_value=0.0, max_value=100.0, value=0.0, key="fac_win")
    rate_window = st.number_input("Window Wall Rate (per m2)", min_value=0.0, value=0.0, key="rate_win")

with col_fac3:
    double_p = st.number_input("Double Skin (%)", min_value=0.0, max_value=100.0, value=0.0, key="fac_double_display")
    rate_double = st.number_input("Double Skin Rate (per m2)", min_value=0.0, value=0.0, key="rate_double")

st.markdown("---")

# --- STEP 3: CALCULATIONS ---
total_earthwork = gba * rate_earthwork
total_foundation = gba * rate_foundation
total_structural = gba * rate_structural
total_architecture = gfa * rate_architecture
total_precast = facade * (precast_p / 100) * rate_precast
total_window = facade * (window_p / 100) * rate_window
total_double_skin = facade * (double_p / 100) * rate_double

# --- STEP 4: HARD COST INFORMATION TABLE ---
st.header("Hard Cost Table")

hard_cost_data = {
    "Description": [
        "1. Preliminary Works", 
        "2. Earthwork", 
        "3. Foundation",
        "4. Structural Work",
        f"5. Basic Architecture ({project_type})",
        "6. Facade - Precast",
        "7. Facade - Window Wall",
        "8. Facade - Double Skin"
    ],
    "Basis": [
        "5% of Hard Cost", 
        f"{gba:,.2f} m2 (GBA) x {rate_earthwork:,.2f}", 
        f"{gba:,.2f} m2 (GBA) x {rate_foundation:,.2f}",
        f"{gba:,.2f} m2 (GBA) x {rate_structural:,.2f}",
        f"{gfa:,.2f} m2 (GFA) x {rate_architecture:,.2f}",
        f"{facade * (precast_p/100):,.2f} m2 ({precast_p}%) x {rate_precast:,.2f}",
        f"{facade * (window_p/100):,.2f} m2 ({window_p}%) x {rate_window:,.2f}",
        f"{facade * (double_p/100):,.2f} m2 ({double_p}%) x {rate_double:,.2f}"
    ],
    "Amount": [
        0.0, 
        total_earthwork, 
        total_foundation,
        total_structural,
        total_architecture,
        total_precast,
        total_window,
        total_double_skin
    ]
}

df_hc = pd.DataFrame(hard_cost_data)
st.table(df_hc.style.format({"Amount": "{:,.2f}"}))
