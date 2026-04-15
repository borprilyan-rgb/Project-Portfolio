import streamlit as st
import pandas as pd

# Hardcoded data extracted from the document
raw_data = [
    {'cost_type': 'HARD COST', 'main_item': 'PRELIMINARIES WORKS', 'description': 'PRELIMINARIES WORKS', 'qty': 5.0, 'unit': '%', 'rate': 1549932414153.24},
    {'cost_type': 'HARD COST', 'main_item': 'EARTHWORKS', 'description': 'EARTHWORKS', 'qty': 179970.685, 'unit': 'm2 GBA', 'rate': 25000.0},
    {'cost_type': 'HARD COST', 'main_item': 'FOUNDATIONS', 'description': 'FOUNDATIONS', 'qty': 179970.685, 'unit': 'm2 GBA', 'rate': 400000.0},
    {'cost_type': 'HARD COST', 'main_item': 'STRUCTURAL WORKS', 'description': 'STRUCTURAL WORKS', 'qty': 179970.685, 'unit': 'm2 GBA', 'rate': 1933000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Basic Arsitektur', 'qty': 152658.99, 'unit': 'm2', 'rate': 1058000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Pintu Jendela Kaca', 'qty': 113432.1, 'unit': 'm2', 'rate': 1168897.04},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Precast', 'qty': 0.6, 'unit': 'm2', 'rate': 800000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Window Wall', 'qty': 0.3, 'unit': 'm2', 'rate': 1250000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Double Skin', 'qty': 0.1, 'unit': 'm2', 'rate': 2500000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Pintu Kaca', 'qty': 344.0, 'unit': 'm2', 'rate': 1000000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Railing', 'qty': 6305.0, 'unit': "m'", 'rate': 2200000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Skylight', 'qty': 0.0, 'unit': 'm2', 'rate': 4500000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Pintu Kayu', 'qty': 8992.0, 'unit': 'bh', 'rate': 3500000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Pintu Besi', 'qty': 1032.0, 'unit': 'bh', 'rate': 7000000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Interior Lobby / Korridor', 'qty': 15347.92, 'unit': 'm2', 'rate': 1500000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Gondola', 'qty': 15.0, 'unit': 'unit', 'rate': 600000000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'SBO - Sanitair', 'qty': 3783.0, 'unit': 'unit', 'rate': 27588686.23},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Unit Typical', 'qty': 3783.0, 'unit': 'unit', 'rate': 26875000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Public Wanita', 'qty': 15.0, 'unit': 'unit', 'rate': 98075000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Public Pria', 'qty': 15.0, 'unit': 'unit', 'rate': 77050000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Disable', 'qty': 0.0, 'unit': 'unit', 'rate': 30275000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Mushola', 'qty': 2.0, 'unit': 'unit', 'rate': 36500000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'SBO - Ironmongeries ', 'qty': 10024.0, 'unit': 'unit', 'rate': 863248.20},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Pintu Kayu (Sub)', 'qty': 8992.0, 'unit': 'unit', 'rate': 750000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Pintu Besi (Sub)', 'qty': 1032.0, 'unit': 'unit', 'rate': 1850000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'SBO - Keramik, HT & Marmer', 'qty': 201509.87, 'unit': 'm2 GFA', 'rate': 210000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'HT / CT', 'qty': 0.9, 'unit': 'm2', 'rate': 150000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Vinyl', 'qty': 0.0, 'unit': 'm2', 'rate': 750000.0},
    {'cost_type': 'HARD COST', 'main_item': 'ARCHITECTURAL WORKS', 'description': 'Marmer', 'qty': 0.1, 'unit': 'm2', 'rate': 750000.0},
    {'cost_type': 'HARD COST', 'main_item': 'F F & E', 'description': 'FF&E', 'qty': 1261.0, 'unit': 'unit', 'rate': 32000000.0},
    {'cost_type': 'HARD COST', 'main_item': 'F F & E', 'description': 'Lain2 : Linen chute & Gym Eqpmt', 'qty': 0.0, 'unit': 'ls', 'rate': 32000000.0},
    {'cost_type': 'HARD COST', 'main_item': 'M.E.P WORKS', 'description': 'M.E.P WORKS', 'qty': 179970.685, 'unit': 'm2 GBA', 'rate': 2810941.24},
    {'cost_type': 'HARD COST', 'main_item': 'UTILITY CONNECTION', 'description': 'UTILITY CONNECTION', 'qty': 179970.685, 'unit': 'm2 GBA', 'rate': 92098.33},
    {'cost_type': 'HARD COST', 'main_item': 'EXTERNAL WORKS', 'description': 'EXTERNAL WORKS', 'qty': 22496.935, 'unit': 'm2 AREA', 'rate': 1563000.0},
    {'cost_type': 'HARD COST', 'main_item': 'FACILITY', 'description': 'Fasos / Fasum', 'qty': 0.0, 'unit': 'm2', 'rate': 31000000.0},
    {'cost_type': 'HARD COST', 'main_item': 'FACILITY', 'description': 'Fasilitas Penghuni', 'qty': 2000.0, 'unit': 'm2', 'rate': 10000000.0},
    {'cost_type': 'HARD COST', 'main_item': 'FACILITY', 'description': 'Fasilitas Proyek', 'qty': 2.0, 'unit': 'unit', 'rate': 2000000000.0},
    {'cost_type': 'HARD COST', 'main_item': 'CONTINGENCIES', 'description': 'CONTINGENCIES', 'qty': 3.0, 'unit': '%', 'rate': 1549932414153.24},
    {'cost_type': 'SOFT COST', 'main_item': 'CONSULTANCY SERVICES FEE', 'description': 'Consultancy Services Unit', 'qty': 152658.99, 'unit': 'm2 GFA', 'rate': 174000.0},
    {'cost_type': 'SOFT COST', 'main_item': 'CONSULTANCY SERVICES FEE', 'description': 'Consultancy Services Parkir', 'qty': 0.0, 'unit': 'm2 GFA', 'rate': 53000.0},
    {'cost_type': 'SOFT COST', 'main_item': 'CONSULTANCY SERVICES FEE', 'description': 'Consultancy Operator', 'qty': 0.0, 'unit': 'm2 GFA', 'rate': 25000.0},
    {'cost_type': 'SOFT COST', 'main_item': 'QS SERVICES', 'description': 'QS SERVICES', 'qty': 36.0, 'unit': 'bln', 'rate': 75000000.0},
    {'cost_type': 'SOFT COST', 'main_item': 'PROJECT MANAGEMENT', 'description': 'PROJECT MANAGEMENT SERVICES', 'qty': 36.0, 'unit': 'bln', 'rate': 250000000.0},
    {'cost_type': 'SOFT COST', 'main_item': 'INSURANCE COVERAGE', 'description': 'INSURANCE COVERAGE', 'qty': 0.12, 'unit': '%', 'rate': 1549932414153.24}
]

def calculate_row_total(row):
    """Calculates row logic. Handles % variations correctly"""
    if '%' in str(row['Unit']):
        return (row['Qty'] / 100.0) * row['Rate']
    return row['Qty'] * row['Rate']

st.set_page_config(page_title="Apartment Budget Calculator", layout="wide")
st.title("🏗️ Project Budget Calculator")
st.markdown("Edit the **Quantity (Qty)** or **Rate** below. The Totals and Grand Totals will compute automatically.")

# Convert to dataframe
df = pd.DataFrame(raw_data)
df.rename(columns={'cost_type': 'Cost Type', 'main_item': 'Category', 'description': 'Description', 'qty': 'Qty', 'unit': 'Unit', 'rate': 'Rate'}, inplace=True)

# Split into Hard Cost and Soft Cost
df_hard = df[df['Cost Type'] == 'HARD COST'].drop(columns=['Cost Type']).reset_index(drop=True)
df_soft = df[df['Cost Type'] == 'SOFT COST'].drop(columns=['Cost Type']).reset_index(drop=True)

# --- HARD COST SECTION ---
st.header("🧱 Hard Costs")
edited_hard = st.data_editor(
    df_hard,
    use_container_width=True,
    disabled=["Category", "Description", "Unit"], # Lock identifier columns
    column_config={
        "Qty": st.column_config.NumberColumn("Qty", format="%.2f"),
        "Rate": st.column_config.NumberColumn("Rate (IDR)", format="%d"),
    },
    key="hard_cost_editor"
)

# Calculate Hard Cost Results
edited_hard['Total'] = edited_hard.apply(calculate_row_total, axis=1)
total_hard_cost = edited_hard['Total'].sum()

st.markdown(f"**💰 Total Hard Cost: `IDR {total_hard_cost:,.2f}`**")
st.divider()

# --- SOFT COST SECTION ---
st.header("📐 Soft Costs")
edited_soft = st.data_editor(
    df_soft,
    use_container_width=True,
    disabled=["Category", "Description", "Unit"],
    column_config={
        "Qty": st.column_config.NumberColumn("Qty", format="%.2f"),
        "Rate": st.column_config.NumberColumn("Rate (IDR)", format="%d"),
    },
    key="soft_cost_editor"
)

# Calculate Soft Cost Results
edited_soft['Total'] = edited_soft.apply(calculate_row_total, axis=1)
total_soft_cost = edited_soft['Total'].sum()

st.markdown(f"**💰 Total Soft Cost: `IDR {total_soft_cost:,.2f}`**")
st.divider()

# --- GRAND TOTAL SUMMARY ---
st.header("📊 Executive Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Hard Cost", value=f"IDR {total_hard_cost:,.0f}")
with col2:
    st.metric(label="Total Soft Cost", value=f"IDR {total_soft_cost:,.0f}")
with col3:
    st.metric(label="GRAND TOTAL", value=f"IDR {(total_hard_cost + total_soft_cost):,.0f}")
