import streamlit as st
import pandas as pd

# 1. MUST BE FIRST: Page configuration
st.set_page_config(page_title="Complex Construction Calculator", layout="wide")

st.title("🏗️ Project Dimension & Cost Calculator")
st.markdown("---")

# --- STEP 1: INPUT BOXES (Area Metrics) ---
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

# --- STEP 2: UNIT RATES (The Changeable Numbers) ---
st.subheader("💰 Unit Rates & Estimations")
col_rate1, col_rate2, col_rate3 = st.columns(3)

with col_rate1:
    rate_earthwork = st.number_input("Earthwork Rate (per GBA m²)", min_value=0.0, value=0.0)
    rate_foundation = st.number_input("Foundation Rate (per GBA m²)", min_value=0.0, value=0.0)

with col_rate2:
    rate_structural = st.number_input("Structural Work Rate (per GBA m²)", min_value=0.0, value=0.0)

with col_rate3:
    st.markdown("**Basic Architecture**")
    project_type = st.selectbox(
        "Project Type",
        ["Hotel", "Retail", "Apartment", "Parking"]
    )
    rate_architecture = st.number_input(f"Rate for {project_type} (per GFA m²)", min_value=0.0, value=0.0)

st.markdown("---")

# --- STEP 3: CALCULATIONS ---
total_earthwork = gba * rate_earthwork
total_foundation = gba * rate_foundation
total_structural = gba * rate_structural
total_architecture = gfa * rate_architecture

# --- STEP 4: HARD COST INFORMATION TABLE ---
st.header("📊 Hard Cost Table")

hard_cost_data = {
    "Description": [
        "1. Preliminary Works", 
        "2. Earthwork", 
        "3. Foundation",
        "4. Structural Work",
        f"5. Basic Architecture ({project_type})"
    ],
    "Basis": [
        "5% of Hard Cost", 
        f"{gba:,.2f} m² (GBA) x {rate_earthwork:,.2f}", 
        f"{gba:,.2f} m² (GBA) x {rate_foundation:,.2f}",
        f"{gba:,.2f} m² (GBA) x {rate_structural:,.2f}",
        f"{gfa:,.2f} m² (GFA) x {rate_architecture:,.2f}"
    ],
    "Amount": [
        0.0, # Placeholder for now
        total_earthwork, 
        total_foundation,
        total_structural,
        total_architecture
    ]
}

df_hc = pd.DataFrame(hard_cost_data)

# Show the table
st.table(df_hc.style.format({"Amount": "{:,.2f}"}))
