import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(page_title="Complex Construction Calculator", layout="wide")

st.title("Project Dimension and Cost Calculator")
st.markdown("---")

# --- STEP 1: PROJECT METRICS ---
st.subheader("Project Metrics Input")
st.caption("Tip: You can copy values from Excel and paste them directly into this table.")

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

edited_df = st.data_editor(
    df_metrics,
    use_container_width=True, 
    hide_index=True,
    column_config={
        "Metric": st.column_config.TextColumn(disabled=True),
        "Value": st.column_config.NumberColumn(format="%.2f")
    }
)

# Unpacking Metrics
m = dict(zip(edited_df["Metric"], edited_df["Value"]))
land_area, gba, gfa, sgfa, facade = m["Land Area (m2)"], m["GBA (m2)"], m["GFA (m2)"], m["SGFA (m2)"], m["Facade (m2)"]
rooms, glass_door, wooden_door, steel_door = m["Room (unit)"], m["Glass Door (unit)"], m["Wooden Door (unit)"], m["Steel Door (unit)"]
lobby_interior, gondola_unit = m["Lobby Interior (m2)"], m["Gondola (unit)"]
toilet_male, toilet_female, disabled_toil, mushola_unit = m["Public Toilet Male (unit)"], m["Public Toilet Female (unit)"], m["Disabled Toilet (unit)"], m["Mushola (unit)"]
carpet_m2, glass_m2, land_m2 = m["Carpet Area (m2)"], m["Glass Area (m2)"], m["Landscape Area (m2)"]
deck_m2, pub_fac_m2, proj_fac_u = m["Facility Deck Area (m2)"], m["Public Facilities (m2)"], m["Project Facilities (unit)"]

st.markdown("---")

# --- STEP 2: UNIT RATES ---
st.subheader("Unit Rates and Estimations")
project_type = st.selectbox("Project Type", ["Hotel", "Retail", "Apartment", "Parking"])

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Structure Section**")
    df_struc = pd.DataFrame({"Description": ["Earthwork Rate (per GBA m2)", "Foundation Rate (per GBA m2)", "Structural Work Rate (per GBA m2)"], "Value": [0.0] * 3})
    edit_struc = st.data_editor(df_struc, use_container_width=True, hide_index=True, key="ed_struc")

    st.markdown("**Facade Selection (Ratio/Rate)**")
    df_fac_std = pd.DataFrame({
        "Description": ["Precast", "Window Wall", "Double Skin"],
        "Ratio": [0.0] * 3,
        "Rate": [0.0] * 3
    })
    edit_fac_pct = st.data_editor(df_fac_std, use_container_width=True, hide_index=True, key="ed_fac_std")

with col2:
    st.markdown("**Architecture Section**")
    df_arch = pd.DataFrame({"Description": ["Architecture Rate (per GFA m2)", "Precast Rate (per m2)", "Window Wall Rate (per m2)", "Double Skin Rate (per m2)", f"Wooden Door Rate ({project_type})", f"Glass Door Rate ({project_type})", f"Steel Door Rate ({project_type})", f"Lobby Interior Rate ({project_type})", f"Gondola Rate ({project_type})"], "Value": [0.0] * 9})
    edit_arch = st.data_editor(df_arch, use_container_width=True, hide_index=True, key="ed_arch")

st.markdown(f"**{project_type} Sanitary Section**")
df_sanitary = pd.DataFrame({"Description": ["Typical Unit (Ratio per Room)", "Public Toilet Male", "Public Toilet Female", "Disabled Toilet", "Mushola/Prayer Room"], "Qty (e.g 3 Typical Unit per Room": [0.0, 1.0, 1.0, 1.0, 1.0], "Rate": [0.0] * 5})
edit_sanitary = st.data_editor(df_sanitary, use_container_width=True, hide_index=True, key="ed_sanitary")

st.markdown("**Flooring Selection (Ratio/Rate)**")
df_floor_std = pd.DataFrame({
    "Description": ["Homogenous/Ceramic Tile", "Vinyl", "Marmer"],
    "Ratio": [0.0] * 3,
    "Rate": [0.0] * 3
})
edit_floor_pct = st.data_editor(df_floor_std, use_container_width=True, hide_index=True, key="ed_floor_std")

st.markdown("**Additional Rates**")
df_extra = pd.DataFrame({"Description": ["Kitchen Equipment (Rate/Room)", "Hardware Pintu Kayu (Rate/Door)", "Hardware Pintu Besi (Rate/Door)", "Homogenous Tile Rate (m2)", "Vinyl Rate (m2)", "Marmer Rate (m2)", "Carpet Rate (m2)", "Glasses Rate (m2)", "FF&E (Rate/Room)", "Misc (Linen/Gym - Lump Sum)", "MEP Works (Rate/GBA)"], "Value": [0.0] * 11})
edit_extra = st.data_editor(df_extra, use_container_width=True, hide_index=True, key="ed_extra")

st.markdown("**Facilities & External Rates**")
df_fac = pd.DataFrame({"Description": ["External Works (Rate/Landscape)", "Public Facilities (Rate/m2)", "Resident Facilities (Rate/Fac Deck)", "Project Facilities (Rate/Unit)"], "Value": [0.0] * 4})
edit_fac = st.data_editor(df_fac, use_container_width=True, hide_index=True, key="ed_fac")

st.markdown("---")

# --- STEP 3 & 4: CALCULATE BUTTON & TABLE ---

# Mapping variables outside the button
rates_dict = dict(zip(pd.concat([edit_struc, edit_fac_pct, edit_arch])["Description"], pd.concat([edit_struc, edit_fac_pct, edit_arch])["Value"]))
rate_earthwork = rates_dict.get("Earthwork Rate (per GBA m2)", 0.0)
rate_foundation = rates_dict.get("Foundation Rate (per GBA m2)", 0.0)
rate_structural = rates_dict.get("Structural Work Rate (per GBA m2)", 0.0)
precast_p = rates_dict.get("Precast (%)", 0.0)
window_p = rates_dict.get("Window Wall (%)", 0.0)
double_p = rates_dict.get("Double Skin (%)", 0.0)
rate_architecture = rates_dict.get("Architecture Rate (per GFA m2)", 0.0)
rate_precast = rates_dict.get("Precast Rate (per m2)", 0.0)
rate_window = rates_dict.get("Window Wall Rate (per m2)", 0.0)
rate_double = rates_dict.get("Double Skin Rate (per m2)", 0.0)
rate_wooden_door = rates_dict.get(f"Wooden Door Rate ({project_type})", 0.0)
rate_glass_door = rates_dict.get(f"Glass Door Rate ({project_type})", 0.0)
rate_steel_door = rates_dict.get(f"Steel Door Rate ({project_type})", 0.0)
rate_lobby = rates_dict.get(f"Lobby Interior Rate ({project_type})", 0.0)
rate_gondola = rates_dict.get(f"Gondola Rate ({project_type})", 0.0)

sanitary_dict = edit_sanitary.to_dict('records')
ratio_typical = sanitary_dict[0]["Qty (e.g 3 Typical Unit per Room"]
rate_unit_typical = sanitary_dict[0]["Rate"]
rate_toil_male = sanitary_dict[1]["Rate"]
rate_toil_female = sanitary_dict[2]["Rate"]
rate_disabled = sanitary_dict[3]["Rate"]
rate_mushola = sanitary_dict[4]["Rate"]

if st.button("Run Calculation", type="primary", use_container_width=True):
    extra = dict(zip(edit_extra["Description"], edit_extra["Value"]))
    fac = dict(zip(edit_fac["Description"], edit_fac["Value"]))

    t_earth = gba * rate_earthwork
    t_found = gba * rate_foundation
    t_struc = gba * rate_structural
    t_arch_base = gfa * rate_architecture
    fac_records = edit_fac_pct.to_dict('records')
    t_precast = facade * fac_records[0]["Ratio"] * fac_records[0]["Rate"]
    t_window  = facade * fac_records[1]["Ratio"] * fac_records[1]["Rate"]
    t_double  = facade * fac_records[2]["Ratio"] * fac_records[2]["Rate"]
    t_w_door = wooden_door * rate_wooden_door
    t_g_door = glass_door * rate_glass_door
    t_s_door = steel_door * rate_steel_door
    t_lobby = lobby_interior * rate_lobby
    t_gondola = gondola_unit * rate_gondola
    t_unit_san = rooms * ratio_typical * rate_unit_typical
    t_t_male, t_t_female = toilet_male * rate_toil_male, toilet_female * rate_toil_female
    t_t_dis, t_mushola = disabled_toil * rate_disabled, mushola_unit * rate_mushola
    t_kitchen = rooms * extra.get("Kitchen Equipment (Rate/Room)", 0.0)
    t_hw_w = wooden_door * extra.get("Hardware Pintu Kayu (Rate/Door)", 0.0)
    t_hw_s = steel_door * extra.get("Hardware Pintu Besi (Rate/Door)", 0.0)
    f_mult = 1.1 * 1.2 
    floor_records = edit_floor_pct.to_dict('records')
    f_mult = 1.32 
    t_ht     = gfa * floor_records[0]["Ratio"] * floor_records[0]["Rate"] * f_mult
    t_vinyl  = gfa * floor_records[1]["Ratio"] * floor_records[1]["Rate"] * f_mult
    t_marmer = gfa * floor_records[2]["Ratio"] * floor_records[2]["Rate"] * f_mult
    t_carpet = carpet_m2 * extra.get("Carpet Rate (m2)", 0)
    t_glass_work = glass_m2 * extra.get("Glasses Rate (m2)", 0)
    t_ffe = rooms * extra.get("FF&E (Rate/Room)", 0)
    t_misc = 1 * extra.get("Misc (Linen/Gym - Lump Sum)", 0)
    t_mep = gba * extra.get("MEP Works (Rate/GBA)", 0)
    t_external = land_m2 * fac.get("External Works (Rate/Landscape)", 0)
    t_pub_fac = pub_fac_m2 * fac.get("Public Facilities (Rate/m2)", 0)
    t_res_fac = deck_m2 * fac.get("Resident Facilities (Rate/Fac Deck)", 0)
    t_proj_fac = proj_fac_u * fac.get("Project Facilities (Rate/Unit)", 0)

    subtotal_for_pct = sum([t_earth, t_found, t_struc, t_arch_base, t_precast, t_window, t_double, t_w_door, t_g_door, t_s_door, t_lobby, t_gondola, t_unit_san, t_t_male, t_t_female, t_t_dis, t_mushola, t_kitchen, t_hw_w, t_hw_s, t_ht, t_vinyl, t_marmer, t_carpet, t_glass_work, t_ffe, t_misc, t_mep, t_external, t_pub_fac, t_res_fac, t_proj_fac])
    t_subtotal_pure = subtotal_for_pct 
    
    t_contingency = t_subtotal_pure * 0.03
    t_preliminary = t_subtotal_pure * 0.05
    grand_total_hc = t_subtotal_pure + t_contingency + t_preliminary

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
            "5% Subtotal", f"{gba:,.0f} m2", f"{gba:,.0f} m2", f"{gba:,.0f} m2", f"{gfa:,.0f} m2", 
            f"{facade:,.0f} m2 x {fac_records[0]['Ratio']}", f"{facade:,.0f} m2 x {fac_records[1]['Ratio']}", f"{facade:,.0f} m2 x {fac_records[2]['Ratio']}",
            f"{wooden_door} units", f"{glass_door} units", f"{steel_door} units", f"{lobby_interior} m2", f"{gondola_unit} units",
            f"{rooms} rms x {ratio_typical}", f"{toilet_male} units", f"{toilet_female} units", f"{disabled_toil} units", f"{mushola_unit} units",
            f"{rooms} rooms", f"{wooden_door} doors", f"{steel_door} doors", 
            f"{gfa:,.0f} m2 x {floor_records[0]['Ratio']} x 1.32", f"{gfa:,.0f} m2 x {floor_records[1]['Ratio']} x 1.32", f"{gfa:,.0f} m2 x {floor_records[2]['Ratio']} x 1.32",
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
    
    st.header("Hard Cost Table")
    st.dataframe(pd.DataFrame(hard_cost_data), use_container_width=True, hide_index=True, column_config={"Amount": st.column_config.NumberColumn(format="Rp %,.2f")})
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Subtotal (Excl. Prelim & Cont.)", f"Rp {t_subtotal_pure:,.2f}")
    with col_res2:
        st.metric("Grand Total (Incl. Prelim & Cont.)", f"Rp {grand_total_hc:,.2f}")
    st.success("Calculations updated!")
