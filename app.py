import streamlit as st
import pandas as pd

# Page configuration - Must be the first streamlit command
st.set_page_config(page_title="Complex Construction Calculator", layout="wide")

st.title("🏗️ Project Dimension & Cost Calculator")
st.markdown("---")

# --- STEP 1: INPUT BOXES (Project Dimensions) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📐 Area Metrics")
    land_area = st.number_input("Land Area (m²)", min_value=0.0, value=0.0, step=1.0)
    gba = st.number_input("GBA (Gross Building Area) (m²)", min_value=0.0, value=0.0, step=1.0)
    gfa = st.number_input("GFA (Gross Floor Area) (m²)", min_value=0.0, value=0.0, step=1.0)
    sgfa = st.number_input("SGFA (Semi-Gross Floor Area) (m²)", min_value=0.0, value=0.0, step=1.0)
    facade = st.number_input("Facade (m²)", min_value=0.0, value=0.0, step=1.0)

with col2:
    st.subheader("🚪 Units & Interior")
    rooms = st.number_input("Room (unit)", min_value=0, value=0, step=1)
    door_glass = st.number_input("Door Glass (unit)", min_value=0, value=0, step=1)
    pintu_kayu = st.number_input("Pintu Kayu (unit)", min_value=0, value=0, step=1)
    pintu_besi = st.number_input("Pintu Besi (unit)", min_value=0, value=0, step=1)
    lobby_interior = st.number_input("Lobby Interior (m²)", min_value=0.0, value=0.0, step=1.0)

with col3:
    st.subheader("🌳 External & Infrastructure")
    rooftop = st.number_input("Rooftop (m²)", min_value=0.0, value=0.0, step=1.0)
    facilities = st.number_input("Facilities (m²)", min_value=0.0, value=0.0, step=1.0)
    landscape = st.number_input("External/Landscape (m²)", min_value=0.0, value=0.0, step=1.0)
    boundary_wall = st.number_input("Boundary Wall & Gate (m')", min_value=0.0, value=0.0, step=1.0)
    access_road = st.number_input("Access Road (m')", min_value=0.0, value=0.0, step=1.0)

st.markdown("---")

# --- STEP 2: CALCULATIONS ---

# 1. Preliminary Works Logic
# Preliminary Works = 5% of Hard Cost.
# Hard Cost = (Sum of all construction items) + Preliminary Works
# Hard Cost = Sum / 0.95

# For now, we will sum the physical items. (As you give me more rates, we add them here)
# Example: Using 0 as default until you provide the unit prices
construction_subtotal = 0.0 

# Formula based on your rule:
total_hard_cost = construction_subtotal / 0.95
preliminary_works_val = total_hard_cost * 0.05

# --- STEP 3: HARD COST INFORMATION TABLE ---
st.header("📊 Hard Cost")

# This table will grow as you add more items
hard_cost_data = [
    {"Description": "Preliminary Works", "Percentage": "5.00%", "Amount": preliminary_works_val},
    {"Description": "Construction Physical Works", "Percentage": "95.00%", "Amount": construction_subtotal}
]

df_hc = pd.DataFrame(hard_cost_data)

# Formatting for display
df_hc_display = df_hc.copy()
df_hc_display["Amount"] = df_hc_display["Amount"].map("Rp {:,.2f}".format)

st.table(df_hc_display)

st.metric(label="Total Estimated Hard Cost", value=f"Rp {total_hard_cost:,.2f}")

st.info("Preliminary works set to 5% of Hard Cost. Ready for the next item in the Hard Cost table.")
