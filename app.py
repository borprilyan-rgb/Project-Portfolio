import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(page_title="Complex Construction Calculator", layout="wide")

st.title("Project Dimension and Cost Calculator")
st.markdown("---")

# --- DATA: PROJECT TYPE PRESETS ---
PROJECT_DEFAULTS = {
    "Hotel": {
        "struc_earth": 25000, "struc_found": 400000, "struc_work": 1933000,
        "facade_precast_pct": 60.0, "facade_precast_rate": 800000,
        "facade_window_pct": 30.0, "facade_window_rate": 1250000,
        "facade_double_pct": 10.0, "facade_double_rate": 2500000,
        "arch_base": 1058000, "door_wood": 3500000, "door_glass": 1000000,
        "door_steel": 7000000, "lobby": 1500000, "gondola": 600000000,
        "san_room_qty": 3.0, "san_room_rate": 26875000, "san_pub_m": 98075000, 
        "san_pub_f": 77050000, "san_dis": 30275000, "san_mushola": 36500000,
        "fl_ht_pct": 90.0, "fl_ht_rate": 150000, "fl_vinyl_pct": 0.0, "fl_vinyl_rate": 750000,
        "fl_marmer_pct": 10.0, "fl_marmer_rate": 750000,
        "kitchen": 0.0, "hw_wood": 750000, "hw_steel": 1850000, "carpet": 0.0,
        "glass": 0.0, "ffe": 32000000, "misc": 0.0, "mep": 2810941.24, # Updated Linen to 0.0
        "utility": 92098, "railing_qty": 5.0, "railing_rate": 0.0, # Updated Railing to 5.0
        "skylight_rate": 0.0,
        "ext_land": 1563000, "fac_pub": 31000000, "fac_res": 10000000, "fac_proj": 2000000000
    },
    "Retail": {
        "struc_earth": 120000, "struc_found": 450000, "struc_work": 3000000,
        "facade_precast_pct": 10.0, "facade_precast_rate": 750000,
        "facade_window_pct": 80.0, "facade_window_rate": 1100000,
        "facade_double_pct": 10.0, "facade_double_rate": 2200000,
        "arch_base": 2500000, "door_wood": 2000000, "door_glass": 6000000,
        "door_steel": 5000000, "lobby": 6000000, "gondola": 450000000,
        "san_room_qty": 0.0, "san_room_rate": 0, "san_pub_m": 35000000, 
        "san_pub_f": 35000000, "san_dis": 35000000, "san_mushola": 15000000,
        "fl_ht_pct": 80.0, "fl_ht_rate": 250000, "fl_vinyl_pct": 10.0, "fl_vinyl_rate": 200000,
        "fl_marmer_pct": 10.0, "fl_marmer_rate": 1200000,
        "kitchen": 0, "hw_wood": 400000, "hw_steel": 700000, "carpet": 250000,
        "glass": 550000, "ffe": 0, "misc": 100000000, "mep": 4000000,
        "utility": 150000, "railing_qty": 0.0, "railing_rate": 800000, 
        "skylight_rate": 2500000,
        "ext_land": 600000, "fac_pub": 2000000, "fac_res": 0, "fac_proj": 3000000
    },
    "Apartment": {
        k: 0.0 for k in ["struc_earth", "struc_found", "struc_work", "facade_precast_pct", "facade_precast_rate", "facade_window_pct", "facade_window_rate", "facade_double_pct", "facade_double_rate", "arch_base", "door_wood", "door_glass", "door_steel", "lobby", "gondola", "san_room_qty", "san_room_rate", "san_pub_m", "san_pub_f", "san_dis", "san_mushola", "fl_ht_pct", "fl_ht_rate", "fl_vinyl_pct", "fl_vinyl_rate", "fl_marmer_pct", "fl_marmer_rate", "kitchen", "hw_wood", "hw_steel", "carpet", "glass", "ffe", "misc", "mep", "utility", "railing_qty", "railing_rate", "skylight_rate", "ext_land", "fac_pub", "fac_res", "fac_proj"]
    },
    "Parking": {
        k: 0.0 for k in ["struc_earth", "struc_found", "struc_work", "facade_precast_pct", "facade_precast_rate", "facade_window_pct", "facade_window_rate", "facade_double_pct", "facade_double_rate", "arch_base", "door_wood", "door_glass", "door_steel", "lobby", "gondola", "san_room_qty", "san_room_rate", "san_pub_m", "san_pub_f", "san_dis", "san_mushola", "fl_ht_pct", "fl_ht_rate", "fl_vinyl_pct", "fl_vinyl_rate", "fl_marmer_pct", "fl_marmer_rate", "kitchen", "hw_wood", "hw_steel", "carpet", "glass", "ffe", "misc", "mep", "utility", "railing_qty", "railing_rate", "skylight_rate", "ext_land", "fac_pub", "fac_res", "fac_proj"]
    }
}

# Fetch the active project type early to set the default quantity for Sanitary
project_type = st.sidebar.selectbox("Select Project Type", ["Hotel", "Retail", "Apartment", "Parking"])
pt_data = PROJECT_DEFAULTS[project_type]

# --- STEP 1: PROJECT METRICS ---
st.subheader("1. Project Metrics Input")

col_m1, col_m2 = st.columns(2)

with col_m1:
    st.markdown("**A. Area Measurement**")
    df_area = pd.DataFrame({
        "Metric": ["Land Area (m2)", "GBA (m2)", "GFA (m2)", "SGFA (m2)"],
        "Value": [49424.40, 179970.69, 152658.99, 124336.77]
    })
    ed_area = st.data_editor(df_area, use_container_width=True, hide_index=True)

    st.markdown("**B. Architecture**")
    df_arch_metric = pd.DataFrame({
        "Metric": ["Facade (m2)", "Room (unit)", "Lobby Interior (m2)", "Gondola (unit)", "Carpet (m2)", "Glass (m2)", "Skylight (m2)"],
        "Value": [107127.10, 1261.00, 15347.92, 15.00, 0.0, 0.0, 0.0]
    })
    ed_arch_metric = st.data_editor(df_arch_metric, use_container_width=True, hide_index=True)

with col_m2:
    st.markdown("**C. Door**")
    df_door = pd.DataFrame({
        "Metric": ["Glass Door", "Wooden Door", "Steel Door"],
        "Value": [344.00, 8992.00, 1032.00]
    })
    ed_door = st.data_editor(df_door, use_container_width=True, hide_index=True)

    st.markdown("**D. Toilet**")
    df_toilet = pd.DataFrame({
        "Metric": ["Typical Unit (qty/room)", "Public Toilet Male (whole area)", "Public Toilet Female (whole area)", "Disabled Toilet (whole area)", "Mushola (unit)"],
        "Value": [pt_data["san_room_qty"], 15.00, 15.00, 0.0, 2.00]
    })
    ed_toilet = st.data_editor(df_toilet, use_container_width=True, hide_index=True)

    st.markdown("**E. Facilities**")
    df_fac_metric = pd.DataFrame({
        "Metric": ["Residential Facility (m2)", "Public Facility (m2)", "Project Facility (unit)", "Landscape Area (m2)"],
        "Value": [0.0, 2000.00, 0.0, 22496.94]
    })
    ed_fac_metric = st.data_editor(df_fac_metric, use_container_width=True, hide_index=True)

# Combine all metrics into one dictionary for easy mapping
all_metrics = pd.concat([ed_area, ed_arch_metric, ed_door, ed_toilet, ed_fac_metric])
m = dict(zip(all_metrics["Metric"], all_metrics["Value"]))

# Map values to variables
land_area, gba, gfa = m["Land Area (m2)"], m["GBA (m2)"], m["GFA (m2)"]
facade, rooms = m["Facade (m2)"], m["Room (unit)"]
lobby_interior, gondola_unit = m["Lobby Interior (m2)"], m["Gondola (unit)"]
carpet_m2, glass_m2, skylight_area = m["Carpet (m2)"], m["Glass (m2)"], m["Skylight (m2)"]
glass_door, wooden_door, steel_door = m["Glass Door"], m["Wooden Door"], m["Steel Door"]

san_qty_room = m["Typical Unit (qty/room)"]
toilet_male = m["Public Toilet Male (whole area)"]
toilet_female = m["Public Toilet Female (whole area)"]
disabled_toil = m["Disabled Toilet (whole area)"]
mushola_unit = m["Mushola (unit)"]

res_fac_m2 = m["Residential Facility (m2)"]
pub_fac_m2 = m["Public Facility (m2)"]
proj_fac_u = m["Project Facility (unit)"]
land_m2 = m["Landscape Area (m2)"]

st.markdown("---")

# --- STEP 2: ITEM RATIOS ---
st.subheader("2. Item Ratios & Multipliers")
st.markdown("Adjust the material splits and per-room multiplier ratios below:")

col_r1, col_r2, col_r3 = st.columns(3)

with col_r1:
    st.markdown("**Facade Ratio (%)**")
    df_facade_ratio = pd.DataFrame({
        "Description": ["Precast", "Window Wall", "Double Skin"],
        "Ratio (%)": [pt_data["facade_precast_pct"], pt_data["facade_window_pct"], pt_data["facade_double_pct"]]
    })
    edit_fac_ratio = st.data_editor(df_facade_ratio, use_container_width=True, hide_index=True)

with col_r2:
    st.markdown("**Flooring Ratio (%)**")
    df_floor_ratio = pd.DataFrame({
        "Description": ["HT/Ceramic Tile", "Vinyl", "Marmer"],
        "Ratio (%)": [pt_data["fl_ht_pct"], pt_data["fl_vinyl_pct"], pt_data["fl_marmer_pct"]]
    })
    edit_floor_ratio = st.data_editor(df_floor_ratio, use_container_width=True, hide_index=True)

with col_r3:
    st.markdown("**Per-Room Multipliers**")
    df_room_mult = pd.DataFrame({
        "Description": ["Railing Length (m')"],
        "Qty per Room": [pt_data["railing_qty"]]
    })
    edit_room_mult = st.data_editor(df_room_mult, use_container_width=True, hide_index=True)

st.markdown("---")

# --- STEP 3: UNIT RATES (PURE FINANCIAL) ---
st.subheader("3. Unit Rates (Pure Financial)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Structure Section**")
    df_struc = pd.DataFrame({
        "Description": ["Earthwork Rate (per GBA m2)", "Foundation Rate (per GBA m2)", "Structural Work Rate (per GBA m2)"], 
        "Rate": [pt_data["struc_earth"], pt_data["struc_found"], pt_data["struc_work"]]
    })
    edit_struc = st.data_editor(df_struc, use_container_width=True, hide_index=True)

    st.markdown("**Facade Rates**")
    df_facade_rate = pd.DataFrame({
        "Description": ["Precast Rate (m2)", "Window Wall Rate (m2)", "Double Skin Rate (m2)"], 
        "Rate": [pt_data["facade_precast_rate"], pt_data["facade_window_rate"], pt_data["facade_double_rate"]]
    })
    edit_fac_rate = st.data_editor(df_facade_rate, use_container_width=True, hide_index=True)
    
    st.markdown(f"**{project_type} Sanitary Section**")
    df_sanitary = pd.DataFrame({
        "Description": ["Typical Unit Sanitary", "Public Toilet Male", "Public Toilet Female", "Disabled Toilet", "Mushola/Prayer Room"], 
        "Rate": [pt_data["san_room_rate"], pt_data["san_pub_m"], pt_data["san_pub_f"], pt_data["san_dis"], pt_data["san_mushola"]]
    })
    edit_sanitary = st.data_editor(df_sanitary, use_container_width=True, hide_index=True)


with col2:
    st.markdown("**Architecture Section**")
    df_arch = pd.DataFrame({
        "Description": ["Architecture Base (per GFA m2)", "Wooden Door Rate", "Glass Door Rate", "Steel Door Rate", "Lobby Interior Rate", "Gondola Rate"], 
        "Rate": [pt_data["arch_base"], pt_data["door_wood"], pt_data["door_glass"], pt_data["door_steel"], pt_data["lobby"], pt_data["gondola"]]
    })
    edit_arch = st.data_editor(df_arch, use_container_width=True, hide_index=True)

    st.markdown("**Flooring Rates**")
    df_floor_rate = pd.DataFrame({
        "Description": ["HT/Ceramic Tile Rate", "Vinyl Rate", "Marmer Rate"], 
        "Rate": [pt_data["fl_ht_rate"], pt_data["fl_vinyl_rate"], pt_data["fl_marmer_rate"]]
    })
    edit_floor_rate = st.data_editor(df_floor_rate, use_container_width=True, hide_index=True)

st.markdown("**Architecture, FF&E & MEP Rates**")
df_extra = pd.DataFrame({
    "Description": [
        "Kitchen Equipment (Rate/Room)", "Hardware Pintu Kayu (Rate/Door)", 
        "Hardware Pintu Besi (Rate/Door)", "Carpet Rate (m2)", "Glasses Rate (m2)", 
        "FF&E (Rate/Room)", "Misc (Linen/Gym - Lump Sum)", "MEP Works (Rate/GBA)", 
        "Utility Connection (Rate/GBA)", "Railing (Rate/m')", "Skylight (Rate/m2)"
    ], 
    "Rate": [
        pt_data["kitchen"], pt_data["hw_wood"], pt_data["hw_steel"], pt_data["carpet"], 
        pt_data["glass"], pt_data["ffe"], pt_data["misc"], pt_data["mep"], 
        pt_data["utility"], pt_data["railing_rate"], pt_data["skylight_rate"]
    ]
})

edit_extra = st.data_editor(
    df_extra, 
    use_container_width=True, 
    hide_index=True, 
    column_config={
        "Description": st.column_config.TextColumn(disabled=True),
        "Rate": st.column_config.NumberColumn("Rate (Rp)", format="%.2f")
    }
)

st.markdown("**Facilities & External Rates**")
df_fac = pd.DataFrame({
    "Description": ["External Works (Rate/Landscape)", "Public Facilities (Rate/m2)", "Resident Facilities (Rate/Fac Deck)", "Project Facilities (Rate/Unit)"], 
    "Rate": [pt_data["ext_land"], pt_data["fac_pub"], pt_data["fac_res"], pt_data["fac_proj"]]
})
edit_fac = st.data_editor(df_fac, use_container_width=True, hide_index=True)

st.markdown("---")

# --- STEP 4: CALCULATION ---

if st.button("Run Calculation", type="primary", use_container_width=True):
    # Data extraction
    r_fac_ratio = edit_fac_ratio.to_dict('records')
    r_fl_ratio = edit_floor_ratio.to_dict('records')
    r_room_mult = edit_room_mult.to_dict('records')
    
    r_fac_rate = edit_fac_rate.to_dict('records')
    r_fl_rate = edit_floor_rate.to_dict('records')
    r_san = edit_sanitary.to_dict('records')
    r_ex = edit_extra.to_dict('records')
    r_fac = edit_fac.to_dict('records')
    
    rates_dict = dict(zip(pd.concat([edit_struc, edit_arch])["Description"], 
                         pd.concat([edit_struc, edit_arch])["Rate"]))

    # Calculations
    t_earth = gba * rates_dict.get("Earthwork Rate (per GBA m2)", 0.0)
    t_found = gba * rates_dict.get("Foundation Rate (per GBA m2)", 0.0)
    t_struc = gba * rates_dict.get("Structural Work Rate (per GBA m2)", 0.0)
    t_arch_base = gfa * rates_dict.get("Architecture Base (per GFA m2)", 0.0)
    
    t_precast = facade * (r_fac_ratio[0]["Ratio (%)"] / 100) * r_fac_rate[0]["Rate"]
    t_window  = facade * (r_fac_ratio[1]["Ratio (%)"] / 100) * r_fac_rate[1]["Rate"]
    t_double  = facade * (r_fac_ratio[2]["Ratio (%)"] / 100) * r_fac_rate[2]["Rate"]
    
    t_w_door = wooden_door * rates_dict.get("Wooden Door Rate", 0.0)
    t_g_door = glass_door * rates_dict.get("Glass Door Rate", 0.0)
    t_s_door = steel_door * rates_dict.get("Steel Door Rate", 0.0)
    t_lobby  = lobby_interior * rates_dict.get("Lobby Interior Rate", 0.0)
    t_gondola = gondola_unit * rates_dict.get("Gondola Rate", 0.0)

    t_unit_san = rooms * san_qty_room * r_san[0]["Rate"]
    t_t_male   = toilet_male * r_san[1]["Rate"]
    t_t_female = toilet_female * r_san[2]["Rate"]
    t_t_dis    = disabled_toil * r_san[3]["Rate"]
    t_mushola  = mushola_unit * r_san[4]["Rate"]

    t_kitchen = rooms * r_ex[0]["Rate"]
    t_hw_w    = wooden_door * r_ex[1]["Rate"]
    t_hw_s    = steel_door * r_ex[2]["Rate"]
    
    f_mult = 1.32
    t_ht     = gfa * (r_fl_ratio[0]["Ratio (%)"] / 100) * r_fl_rate[0]["Rate"] * f_mult
    t_vinyl  = gfa * (r_fl_ratio[1]["Ratio (%)"] / 100) * r_fl_rate[1]["Rate"] * f_mult
    t_marmer = gfa * (r_fl_ratio[2]["Ratio (%)"] / 100) * r_fl_rate[2]["Rate"] * f_mult
    
    t_carpet     = carpet_m2 * r_ex[3]["Rate"]
    t_glass_work = glass_m2 * r_ex[4]["Rate"]
    t_ffe        = rooms * r_ex[5]["Rate"]
    t_misc       = r_ex[6]["Rate"]
    t_mep        = gba * r_ex[7]["Rate"]
    t_utility    = gba * r_ex[8]["Rate"]
    
    t_railing    = (rooms * r_room_mult[0]["Qty per Room"]) * r_ex[9]["Rate"]
    t_skylight   = skylight_area * r_ex[10]["Rate"]

    t_external = land_m2 * r_fac[0]["Rate"]
    t_pub_fac  = pub_fac_m2 * r_fac[1]["Rate"]
    t_res_fac  = res_fac_m2 * r_fac[2]["Rate"]
    t_proj_fac = proj_fac_u * r_fac[3]["Rate"]

    construction_subtotal = sum([
        t_earth, t_found, t_struc, t_arch_base, t_precast, t_window, t_double,
        t_w_door, t_g_door, t_s_door, t_lobby, t_gondola, t_unit_san, t_t_male,
        t_t_female, t_t_dis, t_mushola, t_kitchen, t_hw_w, t_hw_s, t_ht, t_vinyl,
        t_marmer, t_carpet, t_glass_work, t_ffe, t_misc, t_mep, t_utility, t_railing, t_skylight, t_external,
        t_pub_fac, t_res_fac, t_proj_fac
    ])
    
    t_preliminary = construction_subtotal * 0.05
    t_contingency = construction_subtotal * 0.03
    grand_total_hc = construction_subtotal + t_preliminary + t_contingency

    # Table Display
    hard_cost_data = {
        "Description": [
            "1. Preliminary Works", "2. Earthwork", "3. Foundation", "4. Structural Work", "5. Basic Architecture",
            "6. Facade - Precast", "7. Facade - Window Wall", "8. Facade - Double Skin", "9. Wooden Doors", "10. Glass Doors",
            "11. Steel Doors", "12. Lobby Interior", "13. Gondola", "14. Typical Unit Sanitary", "15. Public Toilet Male",
            "16. Public Toilet Female", "17. Disabled Toilet", "18. Mushola", "19. Kitchen Equipment", "20. Hardware Pintu Kayu",
            "21. Hardware Pintu Besi", "22. HT/Ceramic Tile", "23. Vinyl Flooring", "24. Marmer Flooring", "25. Carpet Work",
            "26. Glass Work", "27. FF&E", "28. Misc. (Linen/Gym)", "29. MEP Works", "30. Utility Connection",
            "31. Railing Work", "32. Skylight Work", "33. External Works", "34. Public Facilities", "35. Resident Facilities",
            "36. Project Facilities", "37. Contingencies"
        ],
        "Basis": [
            "5% Subtotal", f"{gba:,.0f} m2", f"{gba:,.0f} m2", f"{gba:,.0f} m2", f"{gfa:,.0f} m2", 
            f"{r_fac_ratio[0]['Ratio (%)']}%", f"{r_fac_ratio[1]['Ratio (%)']}%", f"{r_fac_ratio[2]['Ratio (%)']}%", f"{wooden_door} units", f"{glass_door} units", 
            f"{steel_door} units", f"{lobby_interior} m2", f"{gondola_unit} units", f"{rooms} rms", f"{toilet_male} units", 
            f"{toilet_female} units", f"{disabled_toil} units", f"{mushola_unit} units", f"{rooms} rooms", f"{wooden_door} doors", 
            f"{steel_door} doors", f"{r_fl_ratio[0]['Ratio (%)']}% x 1.32", f"{r_fl_ratio[1]['Ratio (%)']}% x 1.32", f"{r_fl_ratio[2]['Ratio (%)']}% x 1.32", f"{carpet_m2} m2", 
            f"{glass_m2} m2", f"{rooms} rooms", "1 LS", f"{gba:,.0f} m2", 
            f"{gba:,.0f} m2 (Utility)", 
            f"{rooms * r_room_mult[0]['Qty per Room']:,.0f} m' (Total)", 
            f"{skylight_area:,.0f} m2 (Total)", 
            f"{land_m2} m2", f"{pub_fac_m2} m2", f"{res_fac_m2} m2", f"{proj_fac_u} units", "3% Subtotal" 
        ],
        "Amount": [
            t_preliminary, t_earth, t_found, t_struc, t_arch_base,
            t_precast, t_window, t_double, t_w_door, t_g_door,
            t_s_door, t_lobby, t_gondola, t_unit_san, t_t_male,
            t_t_female, t_t_dis, t_mushola, t_kitchen, t_hw_w,
            t_hw_s, t_ht, t_vinyl, t_marmer, t_carpet,
            t_glass_work, t_ffe, t_misc, t_mep, t_utility,
            t_railing, t_skylight, t_external, t_pub_fac, t_res_fac,
            t_proj_fac, t_contingency
        ]
    }
    
    st.header("Hard Cost Table")
    st.dataframe(pd.DataFrame(hard_cost_data), use_container_width=True, hide_index=True, column_config={"Amount": st.column_config.NumberColumn(format="Rp %,.2f")})
    
    c1, c2 = st.columns(2)
    c1.metric("Exclude Preliminary & Contingency", f"Rp {construction_subtotal:,.2f}")
    c2.metric("Total Project Hard Cost", f"Rp {grand_total_hc:,.2f}")
    st.success("Calculations updated successfully!")
