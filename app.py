import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(page_title="Complex Construction Calculator", layout="wide")

st.title("Project Dimension and Cost Calculator")
st.markdown("---")

# --- DATA: PROJECT TYPE PRESETS ---
# Fill these dictionaries with your actual baseline rates for each building type
PROJECT_DEFAULTS = {
    "Hotel": {
        "struc_earth": 150000, "struc_found": 500000, "struc_work": 3500000,
        "facade_precast_pct": 20.0, "facade_precast_rate": 800000,
        "facade_window_pct": 60.0, "facade_window_rate": 1200000,
        "facade_double_pct": 20.0, "facade_double_rate": 2500000,
        "arch_base": 4000000, "door_wood": 3000000, "door_glass": 5000000,
        "door_steel": 4500000, "lobby": 8000000, "gondola": 500000000,
        "san_room_qty": 1.0, "san_room_rate": 15000000, "san_pub_m": 25000000, 
        "san_pub_f": 25000000, "san_dis": 30000000, "san_mushola": 10000000,
        "fl_ht_pct": 30.0, "fl_ht_rate": 300000, "fl_vinyl_pct": 50.0, "fl_vinyl_rate": 250000,
        "fl_marmer_pct": 20.0, "fl_marmer_rate": 1500000,
        "kitchen": 50000000, "hw_wood": 500000, "hw_steel": 800000, "carpet": 350000,
        "glass": 600000, "ffe": 75000000, "misc": 200000000, "mep": 4500000,
        "utility": 100000, "railing_qty": 3.5, "railing_rate": 800000, 
        "skylight_qty": 50.0, "skylight_rate": 2000000,
        "ext_land": 500000, "fac_pub": 1500000, "fac_res": 2000000, "fac_proj": 5000000
    },
    "Retail": {
        # Placeholders - adjust to actual retail baselines
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
        "skylight_qty": 200.0, "skylight_rate": 2500000,
        "ext_land": 600000, "fac_pub": 2000000, "fac_res": 0, "fac_proj": 3000000
    },
    "Apartment": {
        # Fallback values to prevent errors if not fully filled out yet
        k: 0.0 for k in ["struc_earth", "struc_found", "struc_work", "facade_precast_pct", "facade_precast_rate", "facade_window_pct", "facade_window_rate", "facade_double_pct", "facade_double_rate", "arch_base", "door_wood", "door_glass", "door_steel", "lobby", "gondola", "san_room_qty", "san_room_rate", "san_pub_m", "san_pub_f", "san_dis", "san_mushola", "fl_ht_pct", "fl_ht_rate", "fl_vinyl_pct", "fl_vinyl_rate", "fl_marmer_pct", "fl_marmer_rate", "kitchen", "hw_wood", "hw_steel", "carpet", "glass", "ffe", "misc", "mep", "utility", "railing_qty", "railing_rate", "skylight_qty", "skylight_rate", "ext_land", "fac_pub", "fac_res", "fac_proj"]
    },
    "Parking": {
        # Fallback values to prevent errors if not fully filled out yet
        k: 0.0 for k in ["struc_earth", "struc_found", "struc_work", "facade_precast_pct", "facade_precast_rate", "facade_window_pct", "facade_window_rate", "facade_double_pct", "facade_double_rate", "arch_base", "door_wood", "door_glass", "door_steel", "lobby", "gondola", "san_room_qty", "san_room_rate", "san_pub_m", "san_pub_f", "san_dis", "san_mushola", "fl_ht_pct", "fl_ht_rate", "fl_vinyl_pct", "fl_vinyl_rate", "fl_marmer_pct", "fl_marmer_rate", "kitchen", "hw_wood", "hw_steel", "carpet", "glass", "ffe", "misc", "mep", "utility", "railing_qty", "railing_rate", "skylight_qty", "skylight_rate", "ext_land", "fac_pub", "fac_res", "fac_proj"]
    }
}

# --- STEP 1: PROJECT METRICS ---
st.subheader("Project Metrics Input")
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

# Unpacking Metrics
m = dict(zip(edited_df["Metric"], edited_df["Value"]))
land_area, gba, gfa, facade = m["Land Area (m2)"], m["GBA (m2)"], m["GFA (m2)"], m["Facade (m2)"]
rooms, glass_door, wooden_door, steel_door = m["Room (unit)"], m["Glass Door (unit)"], m["Wooden Door (unit)"], m["Steel Door (unit)"]
lobby_interior, gondola_unit = m["Lobby Interior (m2)"], m["Gondola (unit)"]
toilet_male, toilet_female, disabled_toil, mushola_unit = m["Public Toilet Male (unit)"], m["Public Toilet Female (unit)"], m["Disabled Toilet (unit)"], m["Mushola (unit)"]
carpet_m2, glass_m2, land_m2 = m["Carpet Area (m2)"], m["Glass Area (m2)"], m["Landscape Area (m2)"]
deck_m2, pub_fac_m2, proj_fac_u = m["Facility Deck Area (m2)"], m["Public Facilities (m2)"], m["Project Facilities (unit)"]

st.markdown("---")

# --- STEP 2: UNIT RATES ---
st.subheader("Unit Rates and Estimations")
project_type = st.selectbox("Project Type", ["Hotel", "Retail", "Apartment", "Parking"])

# Load defaults for selected project type
pt_data = PROJECT_DEFAULTS[project_type]

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Structure Section**")
    df_struc = pd.DataFrame({
        "Description": ["Earthwork Rate (per GBA m2)", "Foundation Rate (per GBA m2)", "Structural Work Rate (per GBA m2)"], 
        "Value": [pt_data["struc_earth"], pt_data["struc_found"], pt_data["struc_work"]]
    })
    edit_struc = st.data_editor(df_struc, use_container_width=True, hide_index=True, key="ed_struc")

    st.markdown("**Facade Selection (Ratio & Rate)**")
    df_fac_std = pd.DataFrame({
        "Description": ["Precast", "Window Wall", "Double Skin"], 
        "Ratio (%)": [pt_data["facade_precast_pct"], pt_data["facade_window_pct"], pt_data["facade_double_pct"]], 
        "Rate": [pt_data["facade_precast_rate"], pt_data["facade_window_rate"], pt_data["facade_double_rate"]]
    })
    edit_fac_std = st.data_editor(df_fac_std, use_container_width=True, hide_index=True, key="ed_fac_std")

with col2:
    st.markdown("**Architecture Section**")
    df_arch = pd.DataFrame({
        "Description": ["Architecture Rate (per GFA m2)", f"Wooden Door Rate ({project_type})", f"Glass Door Rate ({project_type})", f"Steel Door Rate ({project_type})", f"Lobby Interior Rate ({project_type})", f"Gondola Rate ({project_type})"], 
        "Value": [pt_data["arch_base"], pt_data["door_wood"], pt_data["door_glass"], pt_data["door_steel"], pt_data["lobby"], pt_data["gondola"]]
    })
    edit_arch = st.data_editor(df_arch, use_container_width=True, hide_index=True, key="ed_arch")

st.markdown(f"**{project_type} Sanitary Section**")
df_sanitary = pd.DataFrame({
    "Description": ["Typical Unit (Qty/Room)", "Public Toilet Male", "Public Toilet Female", "Disabled Toilet", "Mushola/Prayer Room"], 
    "Ratio/Qty": [pt_data["san_room_qty"], 1.0, 1.0, 1.0, 1.0], 
    "Rate": [pt_data["san_room_rate"], pt_data["san_pub_m"], pt_data["san_pub_f"], pt_data["san_dis"], pt_data["san_mushola"]]
})
edit_sanitary = st.data_editor(df_sanitary, use_container_width=True, hide_index=True, key="ed_san")

st.markdown("**Flooring Selection (Ratio & Rate)**")
df_floor_std = pd.DataFrame({
    "Description": ["HT/Ceramic Tile", "Vinyl", "Marmer"], 
    "Ratio (%)": [pt_data["fl_ht_pct"], pt_data["fl_vinyl_pct"], pt_data["fl_marmer_pct"]], 
    "Rate": [pt_data["fl_ht_rate"], pt_data["fl_vinyl_rate"], pt_data["fl_marmer_rate"]]
})
edit_floor_std = st.data_editor(df_floor_std, use_container_width=True, hide_index=True, key="ed_floor_std")

st.markdown("**Architecture, FF&E & MEP Rates**")
df_extra = pd.DataFrame({
    "Description": [
        "Kitchen Equipment (Rate/Room)", "Hardware Pintu Kayu (Rate/Door)", 
        "Hardware Pintu Besi (Rate/Door)", "Carpet Rate (m2)", "Glasses Rate (m2)", 
        "FF&E (Rate/Room)", "Misc (Linen/Gym - Lump Sum)", "MEP Works (Rate/GBA)", 
        "Utility Connection (Rate/GBA)", "Railing (m' per Room)", "Skylight (m2)"
    ], 
    "Qty/Ratio": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, pt_data["railing_qty"], pt_data["skylight_qty"]],
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
    key="ed_extra",
    column_config={
        "Description": st.column_config.TextColumn(disabled=True),
        "Qty/Ratio": st.column_config.NumberColumn("Qty/Ratio", format="%.2f"),
        "Rate": st.column_config.NumberColumn("Rate (Rp)", format="%.2f")
    }
)

st.markdown("**Facilities & External Rates**")
df_fac = pd.DataFrame({
    "Description": ["External Works (Rate/Landscape)", "Public Facilities (Rate/m2)", "Resident Facilities (Rate/Fac Deck)", "Project Facilities (Rate/Unit)"], 
    "Rate": [pt_data["ext_land"], pt_data["fac_pub"], pt_data["fac_res"], pt_data["fac_proj"]]
})
edit_fac = st.data_editor(df_fac, use_container_width=True, hide_index=True, key="ed_fac")

st.markdown("---")

# --- STEP 3: CALCULATION ---

if st.button("Run Calculation", type="primary", use_container_width=True):
    # --- 1. DATA EXTRACTION ---
    ex_recs = edit_extra.to_dict('records')
    fac_recs = edit_fac.to_dict('records')
    san_recs = edit_sanitary.to_dict('records')
    f_recs = edit_fac_std.to_dict('records')
    fl_recs = edit_floor_std.to_dict('records')
    
    rates_dict = dict(zip(pd.concat([edit_struc, edit_arch])["Description"], 
                         pd.concat([edit_struc, edit_arch])["Value"]))

    # --- 2. CALCULATIONS ---
    t_earth = gba * rates_dict.get("Earthwork Rate (per GBA m2)", 0.0)
    t_found = gba * rates_dict.get("Foundation Rate (per GBA m2)", 0.0)
    t_struc = gba * rates_dict.get("Structural Work Rate (per GBA m2)", 0.0)
    t_arch_base = gfa * rates_dict.get("Architecture Rate (per GFA m2)", 0.0)
    
    t_precast = facade * (f_recs[0]["Ratio (%)"] / 100) * f_recs[0]["Rate"]
    t_window  = facade * (f_recs[1]["Ratio (%)"] / 100) * f_recs[1]["Rate"]
    t_double  = facade * (f_recs[2]["Ratio (%)"] / 100) * f_recs[2]["Rate"]
    
    t_w_door = wooden_door * rates_dict.get(f"Wooden Door Rate ({project_type})", 0.0)
    t_g_door = glass_door * rates_dict.get(f"Glass Door Rate ({project_type})", 0.0)
    t_s_door = steel_door * rates_dict.get(f"Steel Door Rate ({project_type})", 0.0)
    t_lobby  = lobby_interior * rates_dict.get(f"Lobby Interior Rate ({project_type})", 0.0)
    t_gondola = gondola_unit * rates_dict.get(f"Gondola Rate ({project_type})", 0.0)

    t_unit_san = rooms * san_recs[0]["Ratio/Qty"] * san_recs[0]["Rate"]
    t_t_male   = toilet_male * san_recs[1]["Rate"]
    t_t_female = toilet_female * san_recs[2]["Rate"]
    t_t_dis    = disabled_toil * san_recs[3]["Rate"]
    t_mushola  = mushola_unit * san_recs[4]["Rate"]

    t_kitchen = rooms * ex_recs[0]["Rate"]
    t_hw_w    = wooden_door * ex_recs[1]["Rate"]
    t_hw_s    = steel_door * ex_recs[2]["Rate"]
    
    f_mult = 1.32
    t_ht     = gfa * (fl_recs[0]["Ratio (%)"] / 100) * fl_recs[0]["Rate"] * f_mult
    t_vinyl  = gfa * (fl_recs[1]["Ratio (%)"] / 100) * fl_recs[1]["Rate"] * f_mult
    t_marmer = gfa * (fl_recs[2]["Ratio (%)"] / 100) * fl_recs[2]["Rate"] * f_mult
    
    t_carpet     = carpet_m2 * ex_recs[3]["Rate"]
    t_glass_work = glass_m2 * ex_recs[4]["Rate"]
    t_ffe        = rooms * ex_recs[5]["Rate"]
    t_misc       = ex_recs[6]["Rate"]
    t_mep        = gba * ex_recs[7]["Rate"]
    t_utility    = gba * ex_recs[8]["Rate"]
    t_railing    = (rooms * ex_recs[9]["Qty/Ratio"]) * ex_recs[9]["Rate"]
    t_skylight   = ex_recs[10]["Qty/Ratio"] * ex_recs[10]["Rate"]

    t_external = land_m2 * fac_recs[0]["Rate"]
    t_pub_fac  = pub_fac_m2 * fac_recs[1]["Rate"]
    t_res_fac  = deck_m2 * fac_recs[2]["Rate"]
    t_proj_fac = proj_fac_u * fac_recs[3]["Rate"]

    # 7. Final Totals
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

    # --- STEP 4: TABLE DISPLAY ---
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
            f"{f_recs[0]['Ratio (%)']}%", f"{f_recs[1]['Ratio (%)']}%", f"{f_recs[2]['Ratio (%)']}%", f"{wooden_door} units", f"{glass_door} units", 
            f"{steel_door} units", f"{lobby_interior} m2", f"{gondola_unit} units", f"{rooms} rms", f"{toilet_male} units", 
            f"{toilet_female} units", f"{disabled_toil} units", f"{mushola_unit} units", f"{rooms} rooms", f"{wooden_door} doors", 
            f"{steel_door} doors", f"{fl_recs[0]['Ratio (%)']}% x 1.32", f"{fl_recs[1]['Ratio (%)']}% x 1.32", f"{fl_recs[2]['Ratio (%)']}% x 1.32", f"{carpet_m2} m2", 
            f"{glass_m2} m2", f"{rooms} rooms", "1 LS", f"{gba:,.0f} m2", 
            f"{gba:,.0f} m2 (Utility)", 
            f"{rooms * ex_recs[9]['Qty/Ratio']:,.0f} m' (Total)", 
            f"{ex_recs[10]['Qty/Ratio']:,.0f} m2 (Total)", 
            f"{land_m2} m2", f"{pub_fac_m2} m2", f"{deck_m2} m2", f"{proj_fac_u} units", "3% Subtotal" 
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
