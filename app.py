import streamlit as st

# Page configuration
st.set_page_config(page_title="Complex Construction Calculator", layout="wide")

st.title("🏗️ Project Dimension Calculator")
st.markdown("---")

# Using columns to organize the input fields
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

# Creating a dictionary to store data for the next steps
project_data = {
    "Land Area": land_area,
    "GBA": gba,
    "GFA": gfa,
    "SGFA": sgfa,
    "Facade": facade,
    "Rooms": rooms,
    "Rooftop": rooftop,
    "Lobby": lobby_interior,
    "Glass Doors": door_glass,
    "Wooden Doors": pintu_kayu,
    "Steel Doors": pintu_besi,
    "Facilities": facilities,
    "Landscape": landscape,
    "Boundary": boundary_wall,
    "Road": access_road
}

# Display a summary table (optional, for verification)
if st.checkbox("Show Data Summary"):
    st.table([project_data])

st.info("Inputs captured. Please provide the next set of instructions or calculation logic!")


import streamlit as st
import pandas as pd

# Page configuration
st.set_config(page_title="Complex Construction Calculator", layout="wide")

st.title("🏗️ Project Dimension & Cost Calculator")
st.markdown("---")

# --- STEP 1: INPUT BOXES ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📐 Area Metrics")
    land_area = st.number_input("Land Area (m²)", min_value=0.0, value=1000.0)
    gba = st.number_input("GBA (Gross Building Area) (m²)", min_value=0.0, value=500.0)
    gfa = st.number_input("GFA (Gross Floor Area) (m²)", min_value=0.0, value=450.0)
    sgfa = st.number_input("SGFA (Semi-Gross Floor Area) (m²)", min_value=0.0, value=400.0)
    facade = st.number_input("Facade (m²)", min_value=0.0, value=200.0)

with col2:
    st.subheader("🚪 Units & Interior")
    rooms = st.number_input("Room (unit)", min_value=0, value=10)
    door_glass = st.number_input("Door Glass (unit)", min_value=0, value=5)
    pintu_kayu = st.number_input("Pintu Kayu (unit)", min_value=0, value=10)
    pintu_besi = st.number_input("Pintu Besi (unit)", min_value=0, value=2)
    lobby_interior = st.number_input("Lobby Interior (m²)", min_value=0.0, value=50.0)

with col3:
    st.subheader("🌳 External & Infrastructure")
    rooftop = st.number_input("Rooftop (m²)", min_value=0.0, value=100.0)
    facilities = st.number_input("Facilities (m²)", min_value=0.0, value=150.0)
    landscape = st.number_input("External/Landscape (m²)", min_value=0.0, value=300.0)
    boundary_wall = st.number_input("Boundary Wall & Gate (m')", min_value=0.0, value=50.0)
    access_road = st.number_input("Access Road (m')", min_value=0.0, value=20.0)

st.markdown("---")

# --- STEP 2: HARD COST PARAMETERS (Information Table) ---
st.header("📊 Hard Cost Calculation")

# For now, I'm setting placeholder unit rates since we haven't defined them yet.
# These will multiply with your inputs above.
unit_rates = {
    "GFA Cost": 5000000, 
    "Facade Cost": 1500000,
    "Landscape Cost": 500000,
    # ... we can add more as you provide them
}

# Calculation Logic
# Let's assume a basic subtotal of physical works first
physical_works_subtotal = (gfa * unit_rates["GFA Cost"]) + (facade * unit_rates["Facade Cost"]) + (landscape * unit_rates["Landscape Cost"])

# Applying your rule: Preliminary Works = 5% of Hard Cost
# Math: Hard Cost = Physical Works + (0.05 * Hard Cost)
# Therefore: Hard Cost = Physical Works / 0.95
total_hard_cost = physical_works_subtotal / 0.95
preliminary_works = total_hard_cost * 0.05

# --- STEP 3: DISPLAY INFORMATION TABLE ---
df_hard_cost = pd.DataFrame({
    "Description": ["Physical Construction Subtotal", "Preliminary Works (5%)"],
    "Percentage": ["95%", "5%"],
    "Total Amount": [f"Rp {physical_works_subtotal:,.2f}", f"Rp {preliminary_works:,.2f}"]
})

st.table(df_hard_cost)

st.metric(label="Total Hard Cost", value=f"Rp {total_hard_cost:,.2f}")

st.info("Preliminary works logic applied. What are the other components of the Hard Cost table?")
