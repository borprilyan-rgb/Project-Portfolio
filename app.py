import streamlit as st
import pandas as pd
import altair as alt

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="ASG Project Suite", layout="wide")

# --- 2. THE DATABASE ---
PROJECT_DATABASE = {
    "Hotel": {
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_pct": 60.0, "facade_precast_rate": 800000.0,
        "facade_window_pct": 30.0, "facade_window_rate": 1250000.0,
        "facade_double_pct": 10.0, "facade_double_rate": 2500000.0,
        "arch_base": 1058000.0, "door_wood": 3500000.0, "door_glass": 1000000.0,
        "door_steel": 7000000.0, "lobby": 1500000.0, "gondola": 600000000.0,
        "san_room_qty": 3.0, "san_room_rate": 26875000.0, "san_pub_m": 98075000.0, 
        "san_pub_f": 77050000.0, "san_dis": 30275000.0, "san_mushola": 36500000.0,
        "fl_ht_pct": 90.0, "fl_ht_rate": 150000.0, "fl_vinyl_pct": 0.0, "fl_vinyl_rate": 750000.0,
        "fl_marmer_pct": 10.0, "fl_marmer_rate": 750000.0,
        "kitchen": 0.0, "hw_wood": 750000.0, "hw_steel": 1850000.0, "carpet": 0.0,
        "glass": 0.0, "ffe": 32000000.0, "misc": 0.0, "mep": 2810941.24,
        "utility": 92098.0, "railing_qty": 5.0, "railing_rate": 2200000.0, 
        "skylight_rate": 0.0,
        "ext_land": 1563000.0, "fac_pub": 31000000.0, "fac_res": 10000000.0, "fac_proj": 2000000000.0
    },
    "Retail": {
        "struc_earth": 120000.0, "struc_found": 450000.0, "struc_work": 3000000.0,
        "facade_precast_pct": 10.0, "facade_precast_rate": 750000.0,
        "facade_window_pct": 80.0, "facade_window_rate": 1100000.0,
        "facade_double_pct": 10.0, "facade_double_rate": 2200000.0,
        "arch_base": 2500000.0, "door_wood": 2000000.0, "door_glass": 6000000.0,
        "door_steel": 5000000.0, "lobby": 6000000.0, "gondola": 450000000.0,
        "san_room_qty": 0.0, "san_room_rate": 0.0, "san_pub_m": 35000000.0, 
        "san_pub_f": 35000000.0, "san_dis": 35000000.0, "san_mushola": 15000000.0,
        "fl_ht_pct": 80.0, "fl_ht_rate": 250000.0, "fl_vinyl_pct": 10.0, "fl_vinyl_rate": 200000.0,
        "fl_marmer_pct": 10.0, "fl_marmer_rate": 1200000.0,
        "kitchen": 0.0, "hw_wood": 400000.0, "hw_steel": 700000.0, "carpet": 250000.0,
        "glass": 550000.0, "ffe": 0.0, "misc": 100000000.0, "mep": 4000000.0,
        "utility": 150000.0, "railing_qty": 0.0, "railing_rate": 800000.0, 
        "skylight_rate": 2500000.0,
        "ext_land": 600000.0, "fac_pub": 2000000.0, "fac_res": 0.0, "fac_proj": 3000000.0
    },
    "Apartment": {k: 0.0 for k in ["struc_earth", "struc_found", "struc_work", "facade_precast_pct", "facade_precast_rate", "facade_window_pct", "facade_window_rate", "facade_double_pct", "facade_double_rate", "arch_base", "door_wood", "door_glass", "door_steel", "lobby", "gondola", "san_room_qty", "san_room_rate", "san_pub_m", "san_pub_f", "san_dis", "san_mushola", "fl_ht_pct", "fl_ht_rate", "fl_vinyl_pct", "fl_vinyl_rate", "fl_marmer_pct", "fl_marmer_rate", "kitchen", "hw_wood", "hw_steel", "carpet", "glass", "ffe", "misc", "mep", "utility", "railing_qty", "railing_rate", "skylight_rate", "ext_land", "fac_pub", "fac_res", "fac_proj"]},
    "Parking": {k: 0.0 for k in ["struc_earth", "struc_found", "struc_work", "facade_precast_pct", "facade_precast_rate", "facade_window_pct", "facade_window_rate", "facade_double_pct", "facade_double_rate", "arch_base", "door_wood", "door_glass", "door_steel", "lobby", "gondola", "san_room_qty", "san_room_rate", "san_pub_m", "san_pub_f", "san_dis", "san_mushola", "fl_ht_pct", "fl_ht_rate", "fl_vinyl_pct", "fl_vinyl_rate", "fl_marmer_pct", "fl_marmer_rate", "kitchen", "hw_wood", "hw_steel", "carpet", "glass", "ffe", "misc", "mep", "utility", "railing_qty", "railing_rate", "skylight_rate", "ext_land", "fac_pub", "fac_res", "fac_proj"]}
}


# --- 3. THE "SHEETS" (FUNCTIONS) ---

def show_area_calculator():
    st.title("📏 Detailed Area Calculation Sheet")
    st.info("This section handles the breakdown of GBA, GFA, and SGFA including deductions.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Input dimensions")
        st.write("Area logic goes here...")


def show_cost_estimator():
    st.title("Project Dimension and Cost Calculator")
    st.markdown("---")

    # --- SIDEBAR: COST ESTIMATOR SPECIFIC ---
    st.sidebar.header("Project Setup")
    project_type = st.sidebar.selectbox("Select Project Type", ["Hotel", "Retail", "Apartment", "Parking"])
    pt_data = PROJECT_DATABASE[project_type]

    st.sidebar.header("🏢 Project Dimensions")

    # Primary Area Inputs
    gba = st.sidebar.number_input("GBA (Gross Building Area) - m2", value=179970.69, step=100.0)
    gfa = st.sidebar.number_input("GFA (Gross Floor Area) - m2", value=152658.99, step=100.0)
    sgfa = st.sidebar.number_input("SGFA (Semi-Gross Floor Area) - m2", value=124336.77, step=100.0)

    st.sidebar.markdown("---")
    st.sidebar.header("📊 Efficiency Metrics")

    # Efficiency Calculations
    if gba > 0:
        gfa_eff = (gfa / gba) * 100
        sgfa_eff = (sgfa / gba) * 100
        
        st.sidebar.metric("GFA Efficiency", f"{gfa_eff:.2f}%")
        st.sidebar.metric("SGFA Efficiency", f"{sgfa_eff:.2f}%")

    # --- TABS LAYOUT ---
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏗️ 1. Project Metrics", 
        "🧮 2. Ratios & Multipliers", 
        "💰 3. Unit Rates", 
        "💼 4. Soft Costs", 
        "📊 5. Results & Summary"
    ])

    # --- TAB 1: PROJECT METRICS ---
    with tab1:
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.subheader("B. Architecture")
            facade = st.number_input("Facade (m2)", value=107127.10, step=100.0)
            rooms = st.number_input("Room (unit)", value=1261.0, step=1.0)
            lobby_interior = st.number_input("Lobby Interior (m2)", value=15347.92, step=10.0)
            gondola_unit = st.number_input("Gondola (unit)", value=15.0, step=1.0)
            carpet_m2 = st.number_input("Carpet Area (m2)", value=0.0, step=10.0)
            glass_m2 = st.number_input("Glass Area (m2)", value=0.0, step=10.0)
            skylight_area = st.number_input("Skylight Area (m2)", value=0.0, step=10.0)

        with col_m2:
            st.subheader("C. Doors")
            glass_door = st.number_input("Glass Door (unit)", value=344.0, step=1.0)
            wooden_door = st.number_input("Wooden Door (unit)", value=8992.0, step=10.0)
            steel_door = st.number_input("Steel Door (unit)", value=1032.0, step=10.0)

            st.subheader("D. Toilets")
            toilet_male = st.number_input("Public Toilet Male (units)", value=15.0, step=1.0)
            toilet_female = st.number_input("Public Toilet Female (units)", value=15.0, step=1.0)
            disabled_toil = st.number_input("Disabled Toilet (units)", value=0.0, step=1.0)
            mushola_unit = st.number_input("Mushola (units)", value=2.0, step=1.0)

            st.subheader("E. Facilities")
            res_fac_m2 = st.number_input("Residential Facility (m2)", value=2000.0, step=10.0) 
            pub_fac_m2 = st.number_input("Public Facility (m2)", value=0.0, step=10.0)
            proj_fac_u = st.number_input("Project Facility (unit)", value=2.0, step=1.0)
            land_m2 = st.number_input("Landscape Area (m2)", value=22496.94, step=100.0)

    # --- TAB 2: RATIOS & MULTIPLIERS ---
    with tab2:
        st.info("Adjust the material splits and per-room multiplier ratios below.")
        
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.subheader("Facade Ratio (%)")
            facade_precast_pct = st.number_input("Precast (%)", value=pt_data["facade_precast_pct"])
            facade_window_pct = st.number_input("Window Wall (%)", value=pt_data["facade_window_pct"])
            facade_double_pct = st.number_input("Double Skin (%)", value=pt_data["facade_double_pct"])
            
            # 100% Safety Check for Facade
            facade_total = facade_precast_pct + facade_window_pct + facade_double_pct
            if facade_total != 100.0:
                st.warning(f"⚠️ **Total: {facade_total}%**. Facade splits should equal 100%.")
        
        with col_r2:
            st.subheader("Flooring Ratio (%)")
            fl_ht_pct = st.number_input("HT/Ceramic Tile (%)", value=pt_data["fl_ht_pct"])
            fl_vinyl_pct = st.number_input("Vinyl (%)", value=pt_data["fl_vinyl_pct"])
            fl_marmer_pct = st.number_input("Marmer (%)", value=pt_data["fl_marmer_pct"])
            
            # 100% Safety Check for Flooring
            fl_total = fl_ht_pct + fl_vinyl_pct + fl_marmer_pct
            if fl_total != 100.0:
                st.warning(f"⚠️ **Total: {fl_total}%**. Flooring splits should equal 100%.")
            
        with col_r3:
            st.subheader("Per-Room Multipliers")
            san_qty_room = st.number_input("Typical Unit Sanitary (qty/room)", value=pt_data["san_room_qty"])
            railing_qty = st.number_input("Railing Length (m'/room)", value=pt_data["railing_qty"])

    # --- TAB 3: UNIT RATES ---
    with tab3:
        st.info("These values are pre-filled based on your selected Project Type. Expand a section to override the defaults.")
        
        with st.expander("🏗️ Structural & Foundation Rates"):
            c1, c2, c3 = st.columns(3)
            struc_earth = c1.number_input("Earthwork Rate (per GBA)", value=pt_data["struc_earth"])
            struc_found = c2.number_input("Foundation Rate (per GBA)", value=pt_data["struc_found"])
            struc_work = c3.number_input("Structural Work Rate (per GBA)", value=pt_data["struc_work"])
            
        with st.expander("🏢 Architecture & Facade Rates"):
            c1, c2 = st.columns(2)
            arch_base = c1.number_input("Architecture Base (per GFA)", value=pt_data["arch_base"])
            lobby_rate = c2.number_input("Lobby Interior Rate", value=pt_data["lobby"])
            
            st.markdown("##### Facade Rates")
            c3, c4, c5 = st.columns(3)
            fac_precast_rate = c3.number_input("Precast Rate", value=pt_data["facade_precast_rate"])
            fac_window_rate = c4.number_input("Window Wall Rate", value=pt_data["facade_window_rate"])
            fac_double_rate = c5.number_input("Double Skin Rate", value=pt_data["facade_double_rate"])

        with st.expander("🚪 Doors & Hardware Rates"):
            c1, c2 = st.columns(2)
            door_wood = c1.number_input("Wooden Door Rate", value=pt_data["door_wood"])
            door_glass = c2.number_input("Glass Door Rate", value=pt_data["door_glass"])
            door_steel = c1.number_input("Steel Door Rate", value=pt_data["door_steel"])
            hw_wood = c2.number_input("Hardware Wooden Door", value=pt_data["hw_wood"])
            hw_steel = c1.number_input("Hardware Steel Door", value=pt_data["hw_steel"])

        with st.expander("🚽 Sanitary Rates"):
            c1, c2 = st.columns(2)
            san_room_rate = c1.number_input("Typical Unit Sanitary Rate", value=pt_data["san_room_rate"])
            san_pub_m = c2.number_input("Public Toilet Male Rate", value=pt_data["san_pub_m"])
            san_pub_f = c1.number_input("Public Toilet Female Rate", value=pt_data["san_pub_f"])
            san_dis = c2.number_input("Disabled Toilet Rate", value=pt_data["san_dis"])
            san_mushola = c1.number_input("Mushola Rate", value=pt_data["san_mushola"])

        with st.expander("🛋️ Flooring, Finishes & Extra Rates"):
            c1, c2, c3 = st.columns(3)
            fl_ht_rate = c1.number_input("HT/Ceramic Rate", value=pt_data["fl_ht_rate"])
            fl_vinyl_rate = c2.number_input("Vinyl Rate", value=pt_data["fl_vinyl_rate"])
            fl_marmer_rate = c3.number_input("Marmer Rate", value=pt_data["fl_marmer_rate"])
            carpet_rate = c1.number_input("Carpet Rate", value=pt_data["carpet"])
            glass_rate = c2.number_input("Glass Work Rate", value=pt_data["glass"])
            skylight_rate = c3.number_input("Skylight Rate", value=pt_data["skylight_rate"])
            gondola_rate = c1.number_input("Gondola Rate", value=pt_data["gondola"])
            railing_rate = c2.number_input("Railing Rate (m')", value=pt_data["railing_rate"])

        with st.expander("⚡ MEP & Equipment Rates"):
            c1, c2 = st.columns(2)
            mep_rate = c1.number_input("MEP Works (per GBA)", value=pt_data["mep"])
            utility_rate = c2.number_input("Utility Connection (per GBA)", value=pt_data["utility"])
            ffe_rate = c1.number_input("FF&E (Rate/Room)", value=pt_data["ffe"])
            kitchen_rate = c2.number_input("Kitchen Equipment (Rate/Room)", value=pt_data["kitchen"])
            misc_rate = c1.number_input("Misc (Linen/Gym LS)", value=pt_data["misc"])

        with st.expander("🌳 External & Facility Rates"):
            c1, c2 = st.columns(2)
            ext_land_rate = c1.number_input("External Works (Landscape)", value=pt_data["ext_land"])
            fac_pub_rate = c2.number_input("Public Facilities (m2)", value=pt_data["fac_pub"])
            fac_res_rate = c1.number_input("Resident Facilities (m2)", value=pt_data["fac_res"])
            fac_proj_rate = c2.number_input("Project Facilities (Unit)", value=pt_data["fac_proj"])


    # --- LIVE AUTO-CALCULATIONS (HARD COSTS) ---
    t_earth = gba * struc_earth
    t_found = gba * struc_found
    t_struc = gba * struc_work
    t_arch_base = gfa * arch_base

    t_precast = facade * (facade_precast_pct / 100) * fac_precast_rate
    t_window  = facade * (facade_window_pct / 100) * fac_window_rate
    t_double  = facade * (facade_double_pct / 100) * fac_double_rate

    t_w_door = wooden_door * door_wood
    t_g_door = glass_door * door_glass
    t_s_door = steel_door * door_steel
    t_lobby  = lobby_interior * lobby_rate
    t_gondola = gondola_unit * gondola_rate

    t_unit_san = rooms * san_qty_room * san_room_rate
    t_t_male   = toilet_male * san_pub_m
    t_t_female = toilet_female * san_pub_f
    t_t_dis    = disabled_toil * san_dis
    t_mushola  = mushola_unit * san_mushola

    t_kitchen = rooms * kitchen_rate
    t_hw_w    = wooden_door * hw_wood
    t_hw_s    = steel_door * hw_steel

    f_mult = 1.32
    t_ht      = gfa * (fl_ht_pct / 100) * fl_ht_rate * f_mult
    t_vinyl  = gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * f_mult
    t_marmer = gfa * (fl_marmer_pct / 100) * fl_marmer_rate * f_mult

    t_carpet     = carpet_m2 * carpet_rate
    t_glass_work = glass_m2 * glass_rate
    t_ffe        = rooms * ffe_rate
    t_misc       = misc_rate
    t_mep        = gba * mep_rate
    t_utility    = gba * utility_rate

    t_railing    = (rooms * railing_qty) * railing_rate
    t_skylight   = skylight_area * skylight_rate

    t_external = land_m2 * ext_land_rate
    t_pub_fac  = pub_fac_m2 * fac_pub_rate
    t_res_fac  = res_fac_m2 * fac_res_rate
    t_proj_fac = proj_fac_u * fac_proj_rate

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


    # --- TAB 4: SOFT COSTS SETUP ---
    with tab4:
        st.subheader("Soft Costs Setup")
        sc_col1, sc_col2 = st.columns(2)
        
        with sc_col1:
            st.markdown("##### 1. Consultancy Service Fee")
            consultancy_rate = st.number_input("Consultancy Rate (per GFA)", value=174000.0, step=1000.0)
            
            st.markdown("##### 2. Quantity Surveyor Service")
            qs_months = st.number_input("QS Duration (Months)", value=36.0, step=1.0)
            qs_rate = st.number_input("QS Rate (per Month)", value=75000000.0, step=1000000.0)
            
        with sc_col2:
            st.markdown("##### 3. Project Management Service")
            pm_months = st.number_input("PM Duration (Months)", value=36.0, step=1.0)
            pm_rate = st.number_input("PM Rate (per Month)", value=250000000.0, step=1000000.0)
            
            st.markdown("##### 4. Insurance Coverage")
            insurance_pct = st.number_input("Insurance (% of Hard Cost Exclude Prelim/Contingency)", value=0.12, step=0.01)

    # --- SOFT COST CALCULATIONS ---
    t_consultancy = gfa * consultancy_rate
    t_qs = qs_months * qs_rate
    t_pm = pm_months * pm_rate
    t_insurance = construction_subtotal * (insurance_pct / 100.0)

    total_soft_cost = t_consultancy + t_qs + t_pm + t_insurance
    grand_total_project = grand_total_hc + total_soft_cost

    # Chart Groupings
    group_structure = t_earth + t_found + t_struc
    group_arch = t_arch_base + t_w_door + t_g_door + t_s_door + t_lobby + t_ht + t_vinyl + t_marmer + t_carpet + t_glass_work + t_kitchen + t_hw_w + t_hw_s + t_railing + t_skylight
    group_facade = t_precast + t_window + t_double + t_gondola
    group_sanitary = t_unit_san + t_t_male + t_t_female + t_t_dis + t_mushola
    group_mep = t_ffe + t_misc + t_mep + t_utility
    group_ext = t_external + t_pub_fac + t_res_fac + t_proj_fac
    group_contingency = t_preliminary + t_contingency


    # --- TAB 5: RESULTS & SUMMARY ---
    with tab5:
        st.markdown("---")
        
        # MOBILE WRAP FIX for Subtotal and Grand Totals in Tab 5
        st.markdown(f"""
            <div style="margin-bottom: 20px;">
                <div style="font-size: 16px; color: gray; margin-bottom: 5px;">Hard Cost (Exclude Preliminary & Contingency)</div>
                <div style="font-size: 28px; font-weight: bold; word-wrap: break-word; white-space: normal; line-height: 1.2;">
                    Rp {construction_subtotal:,.2f}
                </div>
            </div>
            
            <div style="margin-bottom: 20px;">
                <div style="font-size: 16px; color: gray; margin-bottom: 5px;">Total Project Hard Cost</div>
                <div style="font-size: 28px; font-weight: bold; word-wrap: break-word; white-space: normal; line-height: 1.2;">
                    Rp {grand_total_hc:,.2f}
                </div>
            </div>
            
            <div style="margin-bottom: 20px;">
                <div style="font-size: 16px; color: gray; margin-bottom: 5px;">Total Soft Cost</div>
                <div style="font-size: 28px; font-weight: bold; color: #4DA8DA; word-wrap: break-word; white-space: normal; line-height: 1.2;">
                    Rp {total_soft_cost:,.2f}
                </div>
            </div>

            <div style="margin-bottom: 30px; padding: 15px; background-color: #1E1E1E; border-radius: 8px; border: 1px solid #4B4C55;">
                <div style="font-size: 18px; color: #FAFAFA; margin-bottom: 5px;">Grand Total Project Cost (Hard + Soft)</div>
                <div style="font-size: 38px; font-weight: bold; color: #4CAF50; word-wrap: break-word; white-space: normal; line-height: 1.2;">
                    Rp {grand_total_project:,.2f}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Cost Breakdown Chart
        st.subheader("Total Project Cost Breakdown (Hard & Soft)")
        
        chart_data = pd.DataFrame({
            "Category": [
                "Structure/Foundation", "Architecture & Finishes", "Facade", 
                "Sanitary/Plumbing", "MEP & FF&E", "External/Facilities", 
                "Prelim & Contingency", 
                "Consultancy Fee (Soft)", "Quantity Surveyor (Soft)", 
                "Project Management (Soft)", "Insurance (Soft)"
            ],
            "Amount (Rp)": [
                group_structure, group_arch, group_facade, 
                group_sanitary, group_mep, group_ext, 
                group_contingency, 
                t_consultancy, t_qs, 
                t_pm, t_insurance
            ]
        })
        
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X("Amount (Rp):Q", title="Cost (Rp)"),
            y=alt.Y("Category:N", sort="-x", title=""),
            color=alt.Color("Category:N", legend=None),
            tooltip=["Category", alt.Tooltip("Amount (Rp):Q", format=",.2f")]
        ).properties(height=450)
        
        st.altair_chart(chart, use_container_width=True)

        st.markdown("---")

        # Detailed Table Expander
        with st.expander("View Detailed Project Cost Table"):
            raw_amounts = [
                t_preliminary, t_earth, t_found, t_struc, t_arch_base,
                t_precast, t_window, t_double, t_w_door, t_g_door,
                t_s_door, t_lobby, t_gondola, t_unit_san, t_t_male,
                t_t_female, t_t_dis, t_mushola, t_kitchen, t_hw_w,
                t_hw_s, t_ht, t_vinyl, t_marmer, t_carpet,
                t_glass_work, t_ffe, t_misc, t_mep, t_utility,
                t_railing, t_skylight, t_external, t_pub_fac, t_res_fac,
                t_proj_fac, t_contingency, 
                t_consultancy, t_qs, t_pm, t_insurance
            ]
            
            cost_data = {
                "Description": [
                    "1. Preliminary Works", "2. Earthwork", "3. Foundation", "4. Structural Work", "5. Basic Architecture",
                    "6. Facade - Precast", "7. Facade - Window Wall", "8. Facade - Double Skin", "9. Wooden Doors", "10. Glass Doors",
                    "11. Steel Doors", "12. Lobby Interior", "13. Gondola", "14. Typical Unit Sanitary", "15. Public Toilet Male",
                    "16. Public Toilet Female", "17. Disabled Toilet", "18. Mushola", "19. Kitchen Equipment", "20. Hardware Pintu Kayu",
                    "21. Hardware Pintu Besi", "22. HT/Ceramic Tile", "23. Vinyl Flooring", "24. Marmer Flooring", "25. Carpet Work",
                    "26. Glass Work", "27. FF&E", "28. Misc. (Linen/Gym)", "29. MEP Works", "30. Utility Connection",
                    "31. Railing Work", "32. Skylight Work", "33. External Works", "34. Public Facilities", "35. Resident Facilities",
                    "36. Project Facilities", "37. Contingencies",
                    "38. Consultancy Service Fee", "39. Quantity Surveyor Service", "40. Project Management Service", "41. Insurance Coverage"
                ],
                "Basis": [
                    "5% Subtotal", f"{gba:,.0f} m2", f"{gba:,.0f} m2", f"{gba:,.0f} m2", f"{gfa:,.0f} m2", 
                    f"{facade_precast_pct}%", f"{facade_window_pct}%", f"{facade_double_pct}%", f"{wooden_door} units", f"{glass_door} units", 
                    f"{steel_door} units", f"{lobby_interior} m2", f"{gondola_unit} units", f"{rooms} rms", f"{toilet_male} units", 
                    f"{toilet_female} units", f"{disabled_toil} units", f"{mushola_unit} units", f"{rooms} rooms", f"{wooden_door} doors", 
                    f"{steel_door} doors", f"{fl_ht_pct}% x 1.32", f"{fl_vinyl_pct}% x 1.32", f"{fl_marmer_pct}% x 1.32", f"{carpet_m2} m2", 
                    f"{glass_m2} m2", f"{rooms} rooms", "1 LS", f"{gba:,.0f} m2", 
                    f"{gba:,.0f} m2 (Utility)", 
                    f"{rooms * railing_qty:,.0f} m' (Total)", 
                    f"{skylight_area:,.0f} m2 (Total)", 
                    f"{land_m2} m2", f"{pub_fac_m2} m2", f"{res_fac_m2} m2", f"{proj_fac_u} units", "3% Subtotal",
                    f"{gfa:,.0f} m2 (GFA)", f"{qs_months} Months", f"{pm_months} Months", f"{insurance_pct}% of HC Excl. Prelim/Cont"
                ],
                "Amount": [f"Rp {val:,.2f}" for val in raw_amounts]
            }
            
            st.dataframe(pd.DataFrame(cost_data), use_container_width=True, hide_index=True)


# --- 4. MAIN NAVIGATION (The Sidebar Switcher) ---
st.sidebar.title("Main Navigation")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/id/8/88/Screenshot_20231031_155650_Chrome_Beta.jpg", width=100)

# The radio button controls which function gets executed
page_choice = st.sidebar.radio("Go to Sheet:", ["Cost Estimator", "Area Detail Calculator"])

st.sidebar.markdown("---")

# --- 5. EXECUTION LOGIC ---
if page_choice == "Area Detail Calculator":
    show_area_calculator()
else:
    show_cost_estimator()
