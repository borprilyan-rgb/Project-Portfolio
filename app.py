import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(page_title="Complex Construction Calculator", layout="wide")

st.title("Project Dimension and Cost Calculator")
st.markdown("---")

# --- STEP 1: PROJECT METRICS ---
st.subheader("Project Metrics Input")
st.caption("Tip: You can copy values from Excel and paste them directly into this table.")
# --- STEP 1: PROJECT METRICS ---
st.subheader("Project Metrics Input")

initial_metrics = {
    "Metric": [
        "Land Area (m2)", "GBA (m2)", "GFA (m2)", "SGFA (m2)", "Facade (m2)", 
        "Room (unit)", "Glass Door (unit)", "Wooden Door (unit)", 
        "Steel Door (unit)", "Lobby Interior (m2)", "Gondola (unit)",
        "Public Toilet Male (unit)", "Public Toilet Female (unit)", 
        "Disabled Toilet (unit)", "Mushola (unit)"
    ],
    "Value": [0.0] * 15  # Changed from 11 to 15 to match the list above
}
df_metrics = pd.DataFrame(initial_metrics)

# Use data_editor
edited_df = st.data_editor(
    df_metrics, # Fixed: was df_input
    use_container_width=True, 
    hide_index=True,
    column_config={
        "Metric": st.column_config.TextColumn(disabled=True),
        "Value": st.column_config.NumberColumn(format="%.2f")
    }
)

metrics_dict = dict(zip(edited_df["Metric"], edited_df["Value"]))

land_area      = metrics_dict.get("Land Area (m2)", 0.0)
gba            = metrics_dict.get("GBA (m2)", 0.0)
gfa            = metrics_dict.get("GFA (m2)", 0.0)
sgfa           = metrics_dict.get("SGFA (m2)", 0.0)
facade         = metrics_dict.get("Facade (m2)", 0.0)
rooms          = metrics_dict.get("Room (unit)", 0.0)
glass_door     = metrics_dict.get("Glass Door (unit)", 0.0)
wooden_door    = metrics_dict.get("Wooden Door (unit)", 0.0)
steel_door     = metrics_dict.get("Steel Door (unit)", 0.0)
lobby_interior = metrics_dict.get("Lobby Interior (m2)", 0.0)
gondola_unit   = metrics_dict.get("Gondola (unit)", 0.0)
toilet_male   = metrics_dict.get("Public Toilet Male (unit)", 0.0)
toilet_female = metrics_dict.get("Public Toilet Female (unit)", 0.0)
disabled_toil = metrics_dict.get("Disabled Toilet (unit)", 0.0)
mushola_unit  = metrics_dict.get("Mushola (unit)", 0.0)

st.markdown("---")

# --- STEP 2: UNIT RATES ---
st.subheader("Unit Rates and Estimations")
project_type = st.selectbox("Project Type", ["Hotel", "Retail", "Apartment", "Parking"])

# --- TABLE 1: STRUCTURE SECTION ---
st.markdown("**Structure Section**")
df_struc = pd.DataFrame({
    "Description": ["Earthwork Rate (per GBA m2)", "Foundation Rate (per GBA m2)", "Structural Work Rate (per GBA m2)"],
    "Value": [0.0] * 3
})
edit_struc = st.data_editor(df_struc, use_container_width=True, hide_index=True, key="ed_struc")

# --- TABLE 2: FACADE PERCENTAGE ---
st.markdown("**Facade Percentage**")
df_fac_pct = pd.DataFrame({
    "Description": ["Precast (%)", "Window Wall (%)", "Double Skin (%)"],
    "Value": [0.0] * 3
})
edit_fac_pct = st.data_editor(df_fac_pct, use_container_width=True, hide_index=True, key="ed_fac_pct")

# --- TABLE 3: ARCHITECTURE SECTION ---
st.markdown("**Architecture Section**")
df_arch = pd.DataFrame({
    "Description": [
        "Architecture Rate (per GFA m2)", "Precast Rate (per m2)", "Window Wall Rate (per m2)", 
        "Double Skin Rate (per m2)", f"Wooden Door Rate ({project_type})", 
        f"Glass Door Rate ({project_type})", f"Steel Door Rate ({project_type})", 
        f"Lobby Interior Rate ({project_type})", f"Gondola Rate ({project_type})"
    ],
    "Value": [0.0] * 9
})
edit_arch = st.data_editor(df_arch, use_container_width=True, hide_index=True, key="ed_arch")

# --- TABLE 4: SANITARY SECTION ---
# --- TABLE 4: SANITARY SECTION ---
st.markdown(f"**{project_type} Sanitary Section**")

# Prepare the data
df_sanitary = pd.DataFrame({
    "Description": [
        "Typical Unit (Ratio per Room)", 
        "Public Toilet Male", 
        "Public Toilet Female", 
        "Disabled Toilet", 
        "Mushola/Prayer Room"
    ],
    "Ratio/Qty": [0.0, 1.0, 1.0, 1.0, 1.0],  # Default to 1 for others
    "Rate": [0.0] * 5
})

edit_sanitary = st.data_editor(
    df_sanitary, 
    use_container_width=True, 
    hide_index=True, 
    key="ed_sanitary",
    column_config={
        "Description": st.column_config.TextColumn(disabled=True),
        "Ratio/Qty": st.column_config.NumberColumn(
            "Ratio",
            help="For Typical Unit: How many bathrooms per room? (The rest are fixed at 1)",
            format="%.1f"
        ),
        "Rate": st.column_config.NumberColumn("Rate per Unit", format="%.2f")
    }
)

# --- MAP EDITED RATES TO VARIABLES ---
all_rates = pd.concat([edit_struc, edit_fac_pct, edit_arch])
rates_dict = dict(zip(all_rates["Description"], all_rates["Value"]))

rate_earthwork     = rates_dict.get("Earthwork Rate (per GBA m2)", 0.0)
rate_foundation    = rates_dict.get("Foundation Rate (per GBA m2)", 0.0)
rate_structural    = rates_dict.get("Structural Work Rate (per GBA m2)", 0.0)
precast_p          = rates_dict.get("Precast (%)", 0.0)
window_p           = rates_dict.get("Window Wall (%)", 0.0)
double_p           = rates_dict.get("Double Skin (%)", 0.0)
rate_architecture  = rates_dict.get("Architecture Rate (per GFA m2)", 0.0)
rate_precast       = rates_dict.get("Precast Rate (per m2)", 0.0)
rate_window        = rates_dict.get("Window Wall Rate (per m2)", 0.0)
rate_double        = rates_dict.get("Double Skin Rate (per m2)", 0.0)
rate_wooden_door   = rates_dict.get(f"Wooden Door Rate ({project_type})", 0.0)
rate_glass_door    = rates_dict.get(f"Glass Door Rate ({project_type})", 0.0)
rate_steel_door    = rates_dict.get(f"Steel Door Rate ({project_type})", 0.0)
rate_lobby         = rates_dict.get(f"Lobby Interior Rate ({project_type})", 0.0)
rate_gondola       = rates_dict.get(f"Gondola Rate ({project_type})", 0.0)

# Convert editor to dictionary for mapping
sanitary_dict = edit_sanitary.to_dict('records')

# 1. Typical Unit (Ratio Logic)
ratio_typical = sanitary_dict[0]["Ratio/Qty"]
rate_typical  = sanitary_dict[0]["Rate"]

# 2. Public Units (Direct Logic)
rate_toil_male   = sanitary_dict[1]["Rate"]
rate_toil_female = sanitary_dict[2]["Rate"]
rate_disabled    = sanitary_dict[3]["Rate"]
rate_mushola     = sanitary_dict[4]["Rate"]

# --- SANITARY MATH ---
# Unit Typical = Rate * Rooms (from Step 1)
total_unit_typical = rooms * rate_unit_typical
total_toil_male    = toilet_male * rate_toil_male
total_toil_female  = toilet_female * rate_toil_female
total_disabled     = disabled_toil * rate_disabled
total_mushola      = mushola_unit * rate_mushola

st.markdown("---")

# Initialize variables to avoid "Variable not defined" errors
total_earthwork = total_foundation = total_structural = 0.0
total_architecture = total_precast = total_window = total_double_skin = 0.0
total_wooden_doors = total_glass_doors = total_steel_doors = 0.0
total_lobby = total_gondola = 0.0
total_unit_typical = total_toil_male = total_toil_female = total_disabled = total_mushola = 0.0

# --- STEP 3: THE CALCULATE BUTTON ---
if st.button("Run Calculation", type="primary", use_container_width=True):
    # Math is performed inside the button trigger
    total_earthwork    = gba * rate_earthwork
    total_foundation   = gba * rate_foundation
    total_structural   = gba * rate_structural
    total_architecture = gfa * rate_architecture
    total_precast      = facade * (precast_p / 100) * rate_precast
    total_window       = facade * (window_p / 100) * rate_window
    total_double_skin  = facade * (double_p / 100) * rate_double
    total_wooden_doors = wooden_door * rate_wooden_door
    total_glass_doors  = glass_door * rate_glass_door
    total_steel_doors  = steel_door * rate_steel_door
    total_lobby        = lobby_interior * rate_lobby
    total_gondola      = gondola_unit * rate_gondola
    total_unit_typical = rooms * ratio_typical * rate_typical
    total_toil_male    = toilet_male * rate_toil_male
    total_toil_female  = toilet_female * rate_toil_female
    total_disabled     = disabled_toil * rate_disabled
    total_mushola      = mushola_unit * rate_mushola
    
    st.success("Calculations updated successfully!")

# --- STEP 4: HARD COST TABLE ---
st.header("Hard Cost Table")

hard_cost_data = {
    "Description": [
        "1. Preliminary Works", "2. Earthwork", "3. Foundation", "4. Structural Work",
        f"5. Basic Architecture ({project_type})", "6. Facade - Precast", "7. Facade - Window Wall", "8. Facade - Double Skin",
        f"9. Wooden Doors ({project_type})", f"10. Glass Doors ({project_type})", f"11. Steel Doors ({project_type})",
        f"12. Lobby Interior ({project_type})", f"13. Gondola ({project_type})",
        f"14. Typical Unit Sanitary ({project_type})", f"15. Public Toilet Male ({project_type})",
        f"16. Public Toilet Female ({project_type})", f"17. Disabled Toilet ({project_type})", f"18. Mushola/Prayer Room ({project_type})"
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
        f"{steel_door} units x {rate_steel_door:,.2f}",
        f"{lobby_interior:,.2f} m2 x {rate_lobby:,.2f}",
        f"{gondola_unit} units x {rate_gondola:,.2f}",
        f"{rooms} rooms x {ratio_typical} qty x {rate_typical:,.2f}",
        f"{toilet_male} units x {rate_toil_male:,.2f}",              
        f"{toilet_female} units x {rate_toil_female:,.2f}",           
        f"{disabled_toil} units x {rate_disabled:,.2f}",         
        f"{mushola_unit} units x {rate_mushola:,.2f}" 
    ],
    "Amount": [
        0.0, total_earthwork, total_foundation, total_structural,
        total_architecture, total_precast, total_window, total_double_skin,
        total_wooden_doors, total_glass_doors, total_steel_doors,
        total_lobby, total_gondola, total_unit_typical, 
        total_toil_male, total_toil_female, total_disabled, total_mushola
    ]
}

df_hc = pd.DataFrame(hard_cost_data)

st.dataframe(
    df_hc, # No need for .style.format here if using column_config
    use_container_width=True,
    hide_index=True,
    column_config={
        "Description": st.column_config.TextColumn(
            "Description",
            width="medium",
        ),
        "Basis": st.column_config.TextColumn(
            "Basis",
            width="small",
        ),
        "Amount": st.column_config.NumberColumn(
            "Amount (Rp)",
            format="Rp %,.2f",
            width="medium",
        ),
    }
)
