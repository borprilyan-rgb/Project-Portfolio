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

# --- STEP 1: COMPREHENSIVE METRICS ---
initial_metrics = {
    "Metric": [
        "Land Area (m2)", "GBA (m2)", "GFA (m2)", "SGFA (m2)", "Facade (m2)", 
        "Room (unit)", "Glass Door (unit)", "Wooden Door (unit)", "Steel Door (unit)", 
        "Lobby Interior (m2)", "Gondola (unit)", "Public Toilet Male (unit)", 
        "Public Toilet Female (unit)", "Disabled Toilet (unit)", "Mushola (unit)",
        "Carpet Area (m2)", "Glass Area (m2)", "Landscape Area (m2)", 
        "Facility Deck Area (m2)", "Public Facilities (m2)", "Project Facilities (unit)"
    ],
    "Value": [0.0] * 21 
}
df_metrics = pd.DataFrame(initial_metrics)
edited_df = st.data_editor(df_metrics, use_container_width=True, hide_index=True)

# Unpacking
m = dict(zip(edited_df["Metric"], edited_df["Value"]))
land_area, gba, gfa, sgfa, facade = m["Land Area (m2)"], m["GBA (m2)"], m["GFA (m2)"], m["SGFA (m2)"], m["Facade (m2)"]
rooms, g_door, w_door, s_door = m["Room (unit)"], m["Glass Door (unit)"], m["Wooden Door (unit)"], m["Steel Door (unit)"]
lobby_m2, gondola_u = m["Lobby Interior (m2)"], m["Gondola (unit)"]
t_male, t_female, t_dis, mushola = m["Public Toilet Male (unit)"], m["Public Toilet Female (unit)"], m["Disabled Toilet (unit)"], m["Mushola (unit)"]
carpet_m2, glass_m2, land_m2 = m["Carpet Area (m2)"], m["Glass Area (m2)"], m["Landscape Area (m2)"]
deck_m2, pub_fac_m2, proj_fac_u = m["Facility Deck Area (m2)"], m["Public Facilities (m2)"], m["Project Facilities (unit)"]

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

# --- TABLE 5: FLOORING RATIO (%) ---
st.markdown("**Flooring Selection (%)**")
df_floor_pct = pd.DataFrame({
    "Type": ["Homogenous/Ceramic Tile", "Vinyl", "Marmer"],
    "Ratio (%)": [0.0] * 3
})
edit_floor_pct = st.data_editor(df_floor_pct, use_container_width=True, hide_index=True, key="ed_floor_pct")

# --- TABLE 6: ADDITIONAL ARCH & FF&E ---
st.markdown("**Architecture, FF&E & MEP Rates**")
df_extra = pd.DataFrame({
    "Description": [
        "Kitchen Equipment (Rate/Room)", "Hardware Pintu Kayu (Rate/Door)", "Hardware Pintu Besi (Rate/Door)",
        "Homogenous Tile Rate (m2)", "Vinyl Rate (m2)", "Marmer Rate (m2)", 
        "Carpet Rate (m2)", "Glasses Rate (m2)", 
        "FF&E (Rate/Room)", "Misc (Linen/Gym - Lump Sum)", "MEP Works (Rate/GBA)"
    ],
    "Value": [0.0] * 11
})
edit_extra = st.data_editor(df_extra, use_container_width=True, hide_index=True, key="ed_extra")

# --- TABLE 7: FACILITIES & EXTERNAL ---
st.markdown("**Facilities & External Rates**")
df_fac = pd.DataFrame({
    "Description": [
        "External Works (Rate/Landscape)", "Public Facilities (Rate/m2)", 
        "Resident Facilities (Rate/Fac Deck)", "Project Facilities (Rate/Unit)"
    ],
    "Value": [0.0] * 4
})
edit_fac = st.data_editor(df_fac, use_container_width=True, hide_index=True, key="ed_fac")

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
rate_unit_typical = sanitary_dict[0]["Rate"]

# 2. Public Units (Direct Logic)
rate_toil_male   = sanitary_dict[1]["Rate"]
rate_toil_female = sanitary_dict[2]["Rate"]
rate_disabled    = sanitary_dict[3]["Rate"]
rate_mushola     = sanitary_dict[4]["Rate"]

# --- SANITARY MATH ---
# Unit Typical = Rate * Rooms (from Step 1)
total_toil_male    = toilet_male * rate_toil_male
total_toil_female  = toilet_female * rate_toil_female
total_disabled     = disabled_toil * rate_disabled
total_mushola      = mushola_unit * rate_mushola

st.markdown("---")
# --- STEP 3 & 4: INITIALIZATION, CALCULATION, AND TABLE ---

# 1. Safety Initialization (so the script doesn't crash on load)
t_preliminary = t_earth = t_found = t_struc = t_arch_base = 0.0
t_precast = t_window = t_double = t_w_door = t_g_door = t_s_door = 0.0
t_lobby = t_gondola = t_unit_san = t_t_male = t_t_female = t_t_dis = 0.0
t_mushola = t_kitchen = t_hw_w = t_hw_s = t_ht = t_vinyl = t_marmer = 0.0
t_carpet = t_glass_work = t_ffe = t_misc = t_mep = t_external = 0.0
t_pub_fac = t_res_fac = t_proj_fac = t_contingency = 0.0

if st.button("Run Calculation", type="primary", use_container_width=True):
    # a. Map the extra rates
    extra = dict(zip(edit_extra["Description"], edit_extra["Value"]))
    fac = dict(zip(edit_fac["Description"], edit_fac["Value"]))
    f_pct = dict(zip(edit_floor_pct["Type"], edit_floor_pct["Ratio (%)"]))
    
    # b. Perform Math (Using variables from Step 1 unpacking)
    t_earth = gba * rate_earthwork
    t_found = gba * rate_foundation
    t_struc = gba * rate_structural
    t_arch_base = gfa * rate_architecture
    t_precast = facade * (precast_p/100) * rate_precast
    t_window = facade * (window_p/100) * rate_window
    t_double = facade * (double_p/100) * rate_double
    t_w_door = wooden_door * rate_wooden_door
    t_g_door = glass_door * rate_glass_door
    t_s_door = steel_door * rate_steel_door
    t_lobby = lobby_interior * rate_lobby
    t_gondola = gondola_unit * rate_gondola
    
    t_unit_san = rooms * ratio_typical * rate_unit_typical
    t_t_male = toilet_male * rate_toil_male
    t_t_female = toilet_female * rate_toil_female
    t_t_dis = disabled_toil * rate_disabled
    t_mushola = mushola_unit * rate_mushola
    
    t_kitchen = rooms * extra.get("Kitchen Equipment (Rate/Room)", 0.0)
    t_hw_w = wooden_door * extra.get("Hardware Pintu Kayu (Rate/Door)", 0.0)
    t_hw_s = steel_door * extra.get("Hardware Pintu Besi (Rate/Door)", 0.0)
    
    f_mult = 1.1 * 1.2 
    t_ht = gfa * (f_pct.get("Homogenous/Ceramic Tile", 0)/100) * extra.get("Homogenous Tile Rate (m2)", 0) * f_mult
    t_vinyl = gfa * (f_pct.get("Vinyl", 0)/100) * extra.get("Vinyl Rate (m2)", 0) * f_mult
    t_marmer = gfa * (f_pct.get("Marmer", 0)/100) * extra.get("Marmer Rate (m2)", 0) * f_mult
    
    t_carpet = carpet_m2 * extra.get("Carpet Rate (m2)", 0)
    t_glass_work = glass_m2 * extra.get("Glasses Rate (m2)", 0)
    t_ffe = rooms * extra.get("FF&E (Rate/Room)", 0)
    t_misc = 1 * extra.get("Misc (Linen/Gym - Lump Sum)", 0)
    t_mep = gba * extra.get("MEP Works (Rate/GBA)", 0)
    t_external = land_m2 * fac.get("External Works (Rate/Landscape)", 0)
    t_pub_fac = pub_fac_m2 * fac.get("Public Facilities (Rate/m2)", 0)
    t_res_fac = deck_m2 * fac.get("Resident Facilities (Rate/Fac Deck)", 0)
    t_proj_fac = proj_fac_u * fac.get("Project Facilities (Rate/Unit)", 0)

    # c. Calculate Subtotal and Percentages
    items_to_sum = [
        t_earth, t_found, t_struc, t_arch_base, t_precast, t_window, t_double,
        t_w_door, t_g_door, t_s_door, t_lobby, t_gondola, t_unit_san, t_t_male,
        t_t_female, t_t_dis, t_mushola, t_kitchen, t_hw_w, t_hw_s, t_ht, t_vinyl,
        t_marmer, t_carpet, t_glass_work, t_ffe, t_misc, t_mep, t_external,
        t_pub_fac, t_res_fac, t_proj_fac
    ]
    subtotal_for_pct = sum(items_to_sum)
    
    t_contingency = subtotal_for_pct * 0.03
    t_preliminary = subtotal_for_pct * 0.05
    grand_total_hc = subtotal_for_pct + t_contingency + t_preliminary

    # d. Define Table Data (Dictionary inside the button)
    hard_cost_data = {
        "Description": [
            "1. Preliminary Works", "2. Earthwork", "3. Foundation", "4. Structural Work",
            "5. Basic Architecture", "6. Facade - Precast", "7. Facade - Window Wall", "8. Facade - Double Skin",
            "9. Wooden Doors", "10. Glass Doors", "11. Steel Doors", "12. Lobby Interior", "13. Gondola",
            "14. Typical Unit Sanitary", "15. Public Toilet Male", "16. Public Toilet Female", "17. Disabled Toilet", "18. Mushola",
            "19. Kitchen Equipment", "20. Hardware Pintu Kayu", "21. Hardware Pintu Besi", "22. HT/Ceramic Tile",
            "23. Vinyl Flooring", "24. Marmer Flooring", "25. Carpet Work", "26. Glass Work", "27. FF&E",
            "28. Misc. (Linen/Gym)", "29. MEP Works", "30. External Works", "31. Public Facilities",
            "32. Resident Facilities", "33. Project Facilities", "34. Contingencies"
        ],
        "Basis": [
            "5% Subtotal", f"{gba:,.0f} m2 (GBA)", f"{gba:,.0f} m2 (GBA)", f"{gba:,.0f} m2 (GBA)",
            f"{gfa:,.0f} m2 (GFA)", "Facade %", "Facade %", "Facade %",
            f"{wooden_door} units", f"{glass_door} units", f"{steel_door} units", f"{lobby_interior} m2", f"{gondola_unit} units",
            f"{rooms} rooms", f"{toilet_male} units", f"{toilet_female} units", f"{disabled_toil} units", f"{mushola_unit} units",
            f"{rooms} rooms", f"{wooden_door} units", f"{steel_door} units", "GFA x 1.32 x %", "GFA x 1.32 x %", "GFA x 1.32 x %",
            f"{carpet_m2} m2", f"{glass_m2} m2", f"{rooms} rooms", "1 LS", f"{gba:,.0f} m2",
            f"{land_m2} m2", f"{pub_fac_m2} m2", f"{deck_m2} m2", f"{proj_fac_u} units", "3% Subtotal"
        ],
        "Amount": [
            t_preliminary, t_earth, t_found, t_struc, t_arch_base, t_precast, t_window, t_double,
            t_w_door, t_g_door, t_s_door, t_lobby, t_gondola, t_unit_san, t_t_male,
            t_t_female, t_t_dis, t_mushola, t_kitchen, t_hw_w, t_hw_s, t_ht, t_vinyl,
            t_marmer, t_carpet, t_glass_work, t_ffe, t_misc, t_mep, t_external,
            t_pub_fac, t_res_fac, t_proj_fac, t_contingency
        ]
    }

    # e. Display Table
    st.header("Hard Cost Table")
    st.dataframe(
        pd.DataFrame(hard_cost_data),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Description": st.column_config.TextColumn("Description", width="medium"),
            "Basis": st.column_config.TextColumn("Basis", width="small"),
            "Amount": st.column_config.NumberColumn("Amount (Rp)", format="Rp %,.2f", width="medium"),
        }
    )
    
    st.metric("Total Hard Cost (incl. Prelim & Contingency)", f"Rp {grand_total_hc:,.2f}")
    st.success("Calculations updated successfully!")
