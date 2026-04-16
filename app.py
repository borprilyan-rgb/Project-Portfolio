import streamlit as st
import pandas as pd

# 1. MUST BE FIRST: Page configuration
st.set_page_config(page_title="Complex Construction Calculator", layout="wide")

st.title("Project Dimension and Cost Calculator")
st.markdown("---")

# --- STEP 1: INPUT BOXES (Area Metrics) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Area Metrics")
    land_area = st.number_input("Land Area (m2)", min_value=0.0, format="%.2f")
    gba = st.number_input("GBA (Gross Building Area) (m2)", min_value=0.0, format="%.2f")
    gfa = st.number_input("GFA (Gross Floor Area) (m2)", min_value=0.0, format="%.2f")
    sgfa = st.number_input("SGFA (Semi-Gross Floor Area) (m2)", min_value=0.0, format="%.2f")
    facade = st.number_input("Facade (m2)", min_value=0.0, format="%.2f")

with col2:
    st.subheader("Units and Interior")
    rooms = st.number_input("Room (unit)", min_value=0, format="%d")
    glass_door = st.number_input("Glass Door (unit)", min_value=0, format="%d")
    wooden_door = st.number_input("Wooden Door (unit)", min_value=0, format="%d")
    steel_door = st.number_input("Steel Door (unit)", min_value=0, format="%d")
    lobby_interior = st.number_input("Lobby Interior (m2)", min_value=0.0, format="%.2f")

with col3:
    st.subheader("External & Infrastructure")
    rooftop = st.number_input("Rooftop (m2)", min_value=0.0, format="%.2f")
    facilities = st.number_input("Facilities (m2)", min_value=0.0, format="%.2f")
    landscape = st.number_input("External/Landscape (m2)", min_value=0.0, format="%.2f")
    boundary_wall = st.number_input("Boundary Wall & Gate (m')", min_value=0.0, format="%.2f")
    access_road = st.number_input("Access Road (m')", min_value=0.0, format="%.2f")
    
st.markdown("---")

# --- STEP 2: UNIT RATES ---
st.subheader("Unit Rates and Estimations")
col_rate1, col_rate2, col_rate3 = st.columns(3)

with col_rate1:
    rate_earthwork = st.number_input("Earthwork Rate (per GBA m2)", min_value=0.0, value=0.0)
    rate_foundation = st.number_input("Foundation Rate (per GBA m2)", min_value=0.0, value=0.0)

with col_rate2:
    rate_structural = st.number_input("Structural Work Rate (per GBA m2)", min_value=0.0, value=0.0)

with col_rate3:
    project_type = st.selectbox("Project Type", ["Hotel", "Retail", "Apartment", "Parking"])
    rate_architecture = st.number_input("Architecture Rate (per GFA m2)", min_value=0.0, value=0.0)

# --- SUB-SECTION: FACADE ---
st.markdown("#### Facade Breakdown")
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

# --- SUB-SECTION: PROJECT SPECIFIC DOORS ---
st.markdown(f"#### {project_type} Door Rates")
col_spec1, col_spec2, col_spec3 = st.columns(3)

with col_spec1:
    rate_wooden_door = st.number_input(f"Wooden Door Rate ({project_type})", min_value=0.0, value=0.0, format="%.2f")

with col_spec2:
    rate_glass_door = st.number_input(f"Glass Door Rate ({project_type})", min_value=0.0, value=0.0, format="%.2f")

with col_spec3:
    rate_steel_door = st.number_input(f"Steel Door Rate ({project_type})", min_value=0.0, value=0.0, format="%.2f")

st.markdown("---")

# --- STEP 3: CALCULATIONS ---
total_earthwork = gba * rate_earthwork
total_foundation = gba * rate_foundation
total_structural = gba * rate_structural
total_architecture = gfa * rate_architecture
total_precast = facade * (precast_p / 100) * rate_precast
total_window = facade * (window_p / 100) * rate_window
total_double_skin = facade * (double_p / 100) * rate_double

total_wooden_doors = wooden_door * rate_wooden_door
total_glass_doors = glass_door * rate_glass_door
total_steel_doors = steel_door * rate_steel_door

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
        "8. Facade - Double Skin",
        f"9. Wooden Doors ({project_type})",
        f"10. Glass Doors ({project_type})",
        f"11. Steel Doors ({project_type})"
    ],
    "Basis": [
        "5% of Hard Cost", 
        f"{gba:,.2f} m2 (GBA) x {rate_earthwork:,.2f}", 
        f"{gba:,.2f} m2 (GBA) x {rate_foundation:,.2f}",
        f"{gba:,.2f} m2 (GBA) x {rate_structural:,.2f}",
        f"{gfa:,.2f} m2 (GFA) x {rate_architecture:,.2f}",
        f"{facade * (precast_p/100):,.2f} m2 x {rate_precast:,.2f}",
        f"{facade * (window_p/100):,.2f} m2 x {rate_window:,.2f}",
        f"{facade * (double_p/100):,.2f} m2 x {rate_double:,.2f}",
        f"{wooden_door} units x {rate_wooden_door:,.2f}",
        f"{glass_door} units x {rate_glass_door:,.2f}",
        f"{steel_door} units x {rate_steel_door:,.2f}"
    ],
    "Amount": [
        0.0, 
        total_earthwork, 
        total_foundation,
        total_structural,
        total_architecture,
        total_precast,
        total_window,
        total_double_skin,
        total_wooden_doors,
        total_glass_doors,
        total_steel_doors
    ]
}

df_hc = pd.DataFrame(hard_cost_data)

st.dataframe(
    df_hc.style.format({"Amount": "{:,.2f}"}),
    use_container_width=True,
    hide_index=True
)
