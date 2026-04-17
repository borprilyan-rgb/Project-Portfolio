import streamlit as st
import pandas as pd
import altair as alt
import re

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Project Portfolio", layout="wide")

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

# --- 2.5 SESSION STATE (PROJECT MEMORY) ---
if "projects" not in st.session_state:
    st.session_state.projects = {
        "proj_1": {"name": "New Project 1", "type": "Hotel", "data": {}} # <-- Added "data": {}
    }
    st.session_state.current_proj_id = "proj_1"
    st.session_state.proj_counter = 1


# --- 3. THE "SHEETS" (FUNCTIONS) ---
def show_area_calculator():
    st.title("Area Calculator")
    st.markdown("---")

    # 1. SIDEBAR CONFIG & PLACEHOLDERS
    st.sidebar.subheader("Plot & Block")
    num_plots = st.sidebar.number_input("Number of Plots", min_value=1, value=1)
    
    # Dynamically generate Block Group inputs in the sidebar for each Plot
    blocks_per_plot = {}
    for p in range(int(num_plots)):
        blocks_per_plot[p] = st.sidebar.number_input(f"Block Groups in Plot {p+1}", min_value=1, value=2, key=f"ng_setup_{p}")
    
    st.sidebar.markdown("---")
    
    st.sidebar.header("Area Grand Totals")
    # We create empty slots in the sidebar so we can inject the final math into them later!
    gba_placeholder = st.sidebar.empty()
    gfa_placeholder = st.sidebar.empty()
    sgfa_placeholder = st.sidebar.empty()
    units_placeholder = st.sidebar.empty()

    # Store grand totals across all plots
    grand_total_gba = 0
    grand_total_gfa = 0
    grand_total_sgfa = 0
    grand_total_units = 0

    # 2. CREATE TABS FOR PLOTS
    if int(num_plots) > 0:
        plot_tabs = st.tabs([f"Plot {i+1}" for i in range(int(num_plots))])
        
        for p_idx, p_tab in enumerate(plot_tabs):
            with p_tab:
                plot_gfa = 0
                plot_sgfa = 0
                plot_units = 0
                
                num_groups = blocks_per_plot[p_idx]
                
                # 3. CREATE NESTED TABS FOR BLOCKS
                if int(num_groups) > 0:
                    block_tabs = st.tabs([f"Block Group {g+1}" for g in range(int(num_groups))])
                    
                    for g_idx, b_tab in enumerate(block_tabs):
                        with b_tab:
                            # Header Inputs
                            c1, c2, c3 = st.columns(3)
                            group_name = c1.text_input("Group Name", value=f"Block Group {g_idx+1}", key=f"gn_{p_idx}_{g_idx}")
                            num_blocks = c2.number_input("Number of Blocks", min_value=1, value=6, key=f"nb_{p_idx}_{g_idx}")
                            num_floors = c3.number_input("Typical Floors", min_value=1, value=11, key=f"nf_{p_idx}_{g_idx}")
                            
                            # Common Area Inputs
                            col_com1, col_com2 = st.columns(2)
                            core_area = col_com1.number_input("Core Area per Floor (Lifts/Stairs)", value=105.5, key=f"core_{p_idx}_{g_idx}")
                            corridor_area = col_com2.number_input("Corridor Area per Floor", value=88.8, key=f"corr_{p_idx}_{g_idx}")
                            
                            # UNIT MIX (Per Floor)
                            st.markdown("**Typical Floor Unit Mix (Input)**")
                            
                            default_mix = pd.DataFrame([
                                {"Unit Type": "2BR-1", "Net Area": 74.5, "Units/Floor": 2},
                                {"Unit Type": "3BR", "Net Area": 95.5, "Units/Floor": 1},
                                {"Unit Type": "3BR'", "Net Area": 96.1, "Units/Floor": 4},
                            ])
                            
                            edited_mix = st.data_editor(default_mix, key=f"ed_{p_idx}_{g_idx}", num_rows="dynamic", use_container_width=True)
                            
                            # --- CALCULATION LOGIC ---
                            edited_mix["Net/Fl (Total)"] = edited_mix["Net Area"] * edited_mix["Units/Floor"]
                            total_net_per_floor = edited_mix["Net/Fl (Total)"].sum()
                            total_units_per_floor = edited_mix["Units/Floor"].sum()
                            
                            sgfa_load_factor = (total_net_per_floor + corridor_area) / total_net_per_floor if total_net_per_floor > 0 else 1.0
                            gfa_load_factor = (total_net_per_floor + corridor_area + core_area) / total_net_per_floor if total_net_per_floor > 0 else 1.0
                            
                            edited_mix["SGFA per Unit"] = (edited_mix["Net Area"] * sgfa_load_factor).round(2)
                            edited_mix["SGFA/Fl (Total)"] = (edited_mix["SGFA per Unit"] * edited_mix["Units/Floor"]).round(2)
                            
                            edited_mix["GFA per Unit"] = (edited_mix["Net Area"] * gfa_load_factor).round(2)
                            edited_mix["GFA/Fl (Total)"] = (edited_mix["GFA per Unit"] * edited_mix["Units/Floor"]).round(2)
                            
                            # Filter Display Table (Unit breakdown only)
                            display_cols = ["Unit Type", "Net/Fl (Total)", "SGFA per Unit", "SGFA/Fl (Total)", "GFA per Unit", "GFA/Fl (Total)", "Units/Floor"]
                            display_df = edited_mix[display_cols].copy()
                            display_df.rename(columns={"Units/Floor": "Units"}, inplace=True)
                            
                            sum_sgfa_fl = display_df["SGFA/Fl (Total)"].sum()
                            sum_gfa_fl = display_df["GFA/Fl (Total)"].sum()

                            # Calculate Group Totals (Multiplier applied)
                            group_net = total_net_per_floor * num_blocks * num_floors
                            group_sgfa = sum_sgfa_fl * num_blocks * num_floors
                            group_gfa = sum_gfa_fl * num_blocks * num_floors
                            group_units = total_units_per_floor * num_blocks * num_floors

                            # Create the Dedicated Summary Table
                            summary_df = pd.DataFrame({
                                "Per Floor Metric": ["Net Area", "SGFA", "GFA", "Units"],
                                "Floor Total": [f"{total_net_per_floor:,.2f}", f"{sum_sgfa_fl:,.2f}", f"{sum_gfa_fl:,.2f}", f"{int(total_units_per_floor)}"],
                                f"{group_name} ({num_blocks} Blk x {num_floors} Fl)": ["Total Net Area", "Total SGFA", "Total GFA", "Total Units"],
                                "Group Total": [f"{group_net:,.2f}", f"{group_sgfa:,.2f}", f"{group_gfa:,.2f}", f"{int(group_units)}"]
                            })
                            
                            # --- HIDE TABLES INSIDE AN EXPANDER ---
                            with st.expander(f"View Detailed Calculation Tables for {group_name}", expanded=False):
                                st.markdown("**Calculated Unit Breakdown**")
                                st.dataframe(display_df, use_container_width=True, hide_index=True)
                                
                                st.markdown("**Area Totals Summary**")
                                st.dataframe(summary_df, use_container_width=True, hide_index=True)
                            
                            # Track Plot Totals for the grand summary
                            plot_gfa += group_gfa
                            plot_sgfa += group_sgfa
                            plot_units += group_units

                # 4. NON-TYPICAL AREAS (Now outside the Block Tabs, but inside the Plot Tab)
                st.markdown("---")
                st.subheader(f"Plot {p_idx+1} Non-Typical Areas")
                
                default_nt = pd.DataFrame([
                    {"Area Name": "Ground Floor (Do not fill if typical)", "Floors": 1, "Area/Floor (m2)": 0.0, "Include in GFA": False},
                    {"Area Name": "Podium Area", "Floors": 1, "Area/Floor (m2)": 7548.0, "Include in GFA": False},
                    {"Area Name": "MEP", "Floors": 1, "Area/Floor (m2)": 3471.0, "Include in GFA": False},
                    {"Area Name": "Clubhouse", "Floors": 1, "Area/Floor (m2)": 0.0, "Include in GFA": True},
                ])

                edited_nt = st.data_editor(default_nt, key=f"nt_{p_idx}", num_rows="dynamic", use_container_width=True)

                edited_nt["Total Area (m2)"] = edited_nt["Floors"] * edited_nt["Area/Floor (m2)"]
                
                total_nt_area = edited_nt["Total Area (m2)"].sum()
                nt_gfa_area = edited_nt[edited_nt["Include in GFA"] == True]["Total Area (m2)"].sum()
                
                st.markdown(f"**Non-Typical Totals: {total_nt_area:,.2f} m2 (Total GBA) | {nt_gfa_area:,.2f} m2 (Added to GFA)**")

                # CALCULATE FINAL PLOT GBA & GFA
                plot_gba = plot_gfa + total_nt_area 
                plot_gfa = plot_gfa + nt_gfa_area   
                
                st.divider()
                
                # Plot Totals Table
                plot_totals_df = pd.DataFrame({
                    "Plot Total GBA (m2)": [f"{plot_gba:,.2f}"],
                    "Plot Total GFA (m2)": [f"{plot_gfa:,.2f}"],
                    "Plot Total SGFA (m2)": [f"{plot_sgfa:,.2f}"],
                    "Plot Total Units": [f"{int(plot_units)}"]
                })
                
                st.markdown(f"**PLOT {p_idx+1} GRAND TOTALS**")
                st.dataframe(plot_totals_df, use_container_width=True, hide_index=True)

                # Track for Grand Totals
                grand_total_gba += plot_gba
                grand_total_gfa += plot_gfa
                grand_total_sgfa += plot_sgfa
                grand_total_units += plot_units

    # 5. INJECT FINAL MATH INTO THE SIDEBAR PLACEHOLDERS
    gba_placeholder.metric("Grand Total GBA", f"{grand_total_gba:,.2f} m2")
    gfa_placeholder.metric("Grand Total GFA", f"{grand_total_gfa:,.2f} m2")
    sgfa_placeholder.metric("Grand Total SGFA", f"{grand_total_sgfa:,.2f} m2")
    units_placeholder.metric("Grand Total Units", f"{int(grand_total_units)} Units")
    
# RATE DATABASE ---
def show_rate_database():
    st.title("🗄️ Project Rate Database")
    st.info("View and manage the standard unit rates for all project types.")
    # We will later display your PROJECT_DATABASE dictionary as a clean table here
    st.dataframe(pd.DataFrame(PROJECT_DATABASE).T)

# COST ESTIMATOR ---
def show_cost_estimator():
    import io
    st.title("Cost Calculator")
    st.markdown("---")

    # Get the currently active project from memory
    curr_id = st.session_state.current_proj_id
    curr_proj = st.session_state.projects[curr_id]

    # Initialize the data locker if it doesn't exist
    if "data" not in curr_proj:
        st.session_state.projects[curr_id]["data"] = {}

    # HELPER FUNCTION: Safely pulls saved data from the locker so it survives switching projects!
    def get_val(key, default=0.0):
        return st.session_state.projects[curr_id]["data"].get(key, default)

    # --- PROJECT SETUP (Main Screen) ---
    st.subheader("⚙️ Project Setup")
    c1, c2 = st.columns(2)

    new_name = c1.text_input("Project Name", value=curr_proj["name"])
    types_list = ["Hotel", "Retail", "Apartment", "Parking"]
    type_index = types_list.index(curr_proj["type"]) if curr_proj["type"] in types_list else 0
    new_type = c2.selectbox("Project Type", types_list, index=type_index)

    if new_name != curr_proj["name"] or new_type != curr_proj["type"]:
        st.session_state.projects[curr_id]["name"] = new_name
        st.session_state.projects[curr_id]["type"] = new_type
        st.rerun()

    pt_data = PROJECT_DATABASE[new_type]
    st.markdown("---")

    # --- 1. GLOBAL IMPORT SECTION (Sidebar) ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Upload CSV")
    
    uploaded_file = st.sidebar.file_uploader("Upload Here:", type=["csv"])
    
    if uploaded_file is not None:
        if "last_loaded_file" not in st.session_state or st.session_state.last_loaded_file != uploaded_file.file_id:
            try:
                df_import = pd.read_csv(uploaded_file)
                for index, row in df_import.iterrows():
                    key = str(row["Metric_Key"])
                    val = row["Value"]
                    
                    if key == "proj_name":
                        st.session_state.projects[curr_id]["name"] = str(val)
                    elif key == "proj_type":
                        st.session_state.projects[curr_id]["type"] = str(val)
                    else:
                        # Save directly into the master data locker
                        st.session_state.projects[curr_id]["data"][key] = float(val)
                
                st.session_state.last_loaded_file = uploaded_file.file_id
                st.sidebar.success("✅ Loaded successfully!")
                st.rerun() 
            except Exception as e:
                st.sidebar.error(f"❌ Error loading file: {e}")

    # --- TABS LAYOUT ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏗️ 1. Project Metrics", "🧮 2. Ratios", 
        "💰 3. Unit Rates", "💼 4. Soft Costs", 
        "➕ 5. Custom Items", "📊 6. Results & Summary"
    ])

    # --- TAB 1: PROJECT METRICS ---
    with tab1:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.subheader("A. Area Measurement")
            land_area = st.number_input("Land Area (m2)", value=get_val("m_land", 0.0), step=100.0, key=f"m_land_{curr_id}")
            gba = st.number_input("Total GBA (m2)", value=get_val("m_gba", 0.0), step=100.0, key=f"m_gba_{curr_id}")
            gfa = st.number_input("Total GFA (m2)", value=get_val("m_gfa", 0.0), step=100.0, key=f"m_gfa_{curr_id}")
            sgfa = st.number_input("Total SGFA (m2)", value=get_val("m_sgfa", 0.0), step=100.0, key=f"m_sgfa_{curr_id}")
            
            st.subheader("B. Architecture")
            facade = st.number_input("Facade (m2)", value=get_val("m_facade", 0.0), step=100.0, key=f"m_facade_{curr_id}")
            rooms = st.number_input("Room (unit)", value=get_val("m_rooms", 0.0), step=1.0, key=f"m_rooms_{curr_id}")
            lobby_interior = st.number_input("Lobby Interior (m2)", value=get_val("m_lobby", 0.0), step=10.0, key=f"m_lobby_{curr_id}")
            gondola_unit = st.number_input("Gondola (unit)", value=get_val("m_gondola", 0.0), step=1.0, key=f"m_gondola_{curr_id}")
            carpet_m2 = st.number_input("Carpet Area (m2)", value=get_val("m_carpet", 0.0), step=10.0, key=f"m_carpet_{curr_id}")
            glass_m2 = st.number_input("Glass Area (m2)", value=get_val("m_glass", 0.0), step=10.0, key=f"m_glass_{curr_id}")
            skylight_area = st.number_input("Skylight Area (m2)", value=get_val("m_skylight", 0.0), step=10.0, key=f"m_skylight_{curr_id}")

        with col_m2:
            st.subheader("C. Doors")
            glass_door = st.number_input("Glass Door (unit)", value=get_val("m_door_g", 0.0), step=1.0, key=f"m_door_g_{curr_id}")
            wooden_door = st.number_input("Wooden Door (unit)", value=get_val("m_door_w", 0.0), step=10.0, key=f"m_door_w_{curr_id}")
            steel_door = st.number_input("Steel Door (unit)", value=get_val("m_door_s", 0.0), step=10.0, key=f"m_door_s_{curr_id}")

            st.subheader("D. Toilets")
            toilet_male = st.number_input("Public Toilet Male (units)", value=get_val("m_toil_m", 0.0), step=1.0, key=f"m_toil_m_{curr_id}")
            toilet_female = st.number_input("Public Toilet Female (units)", value=get_val("m_toil_f", 0.0), step=1.0, key=f"m_toil_f_{curr_id}")
            disabled_toil = st.number_input("Disabled Toilet (units)", value=get_val("m_toil_d", 0.0), step=1.0, key=f"m_toil_d_{curr_id}")
            mushola_unit = st.number_input("Mushola (units)", value=get_val("m_mushola", 0.0), step=1.0, key=f"m_mushola_{curr_id}")

            st.subheader("E. Facilities")
            res_fac_m2 = st.number_input("Residential Facility (m2)", value=get_val("m_fac_res", 0.0), step=10.0, key=f"m_fac_res_{curr_id}") 
            pub_fac_m2 = st.number_input("Public Facility (m2)", value=get_val("m_fac_pub", 0.0), step=10.0, key=f"m_fac_pub_{curr_id}")
            proj_fac_u = st.number_input("Project Facility (unit)", value=get_val("m_fac_proj", 0.0), step=1.0, key=f"m_fac_proj_{curr_id}")
            land_m2 = st.number_input("Landscape Area (m2)", value=get_val("m_land_m2", 0.0), step=100.0, key=f"m_land_m2_{curr_id}")

    # --- TAB 2: RATIOS & MULTIPLIERS ---
    with tab2:
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.subheader("Facade Ratio (%)")
            facade_precast_pct = st.number_input("Precast (%)", value=get_val("r_fac_pre", pt_data["facade_precast_pct"]), key=f"r_fac_pre_{curr_id}")
            facade_window_pct = st.number_input("Window Wall (%)", value=get_val("r_fac_win", pt_data["facade_window_pct"]), key=f"r_fac_win_{curr_id}")
            facade_double_pct = st.number_input("Double Skin (%)", value=get_val("r_fac_doub", pt_data["facade_double_pct"]), key=f"r_fac_doub_{curr_id}")
        
        with col_r2:
            st.subheader("Flooring Ratio (%)")
            fl_ht_pct = st.number_input("HT/Ceramic Tile (%)", value=get_val("r_fl_ht", pt_data["fl_ht_pct"]), key=f"r_fl_ht_{curr_id}")
            fl_vinyl_pct = st.number_input("Vinyl (%)", value=get_val("r_fl_vin", pt_data["fl_vinyl_pct"]), key=f"r_fl_vin_{curr_id}")
            fl_marmer_pct = st.number_input("Marmer (%)", value=get_val("r_fl_mar", pt_data["fl_marmer_pct"]), key=f"r_fl_mar_{curr_id}")
            
        with col_r3:
            st.subheader("Per-Room Multipliers")
            san_qty_room = st.number_input("Typical Unit Sanitary (qty/room)", value=get_val("r_san_qty", pt_data["san_room_qty"]), key=f"r_san_qty_{curr_id}")
            railing_qty = st.number_input("Railing Length (m'/room)", value=get_val("r_rail_qty", pt_data["railing_qty"]), key=f"r_rail_qty_{curr_id}")

    # --- TAB 3: UNIT RATES ---
    with tab3:
        with st.expander("🏗️ Structural & Foundation Rates"):
            c1, c2, c3 = st.columns(3)
            struc_earth = c1.number_input("Earthwork Rate", value=get_val("u_earth", pt_data["struc_earth"]), key=f"u_earth_{curr_id}")
            struc_found = c2.number_input("Foundation Rate", value=get_val("u_found", pt_data["struc_found"]), key=f"u_found_{curr_id}")
            struc_work = c3.number_input("Structural Work Rate", value=get_val("u_struc", pt_data["struc_work"]), key=f"u_struc_{curr_id}")
            
        with st.expander("🏢 Architecture & Facade Rates"):
            c1, c2 = st.columns(2)
            arch_base = c1.number_input("Architecture Base", value=get_val("u_arch", pt_data["arch_base"]), key=f"u_arch_{curr_id}")
            lobby_rate = c2.number_input("Lobby Interior Rate", value=get_val("u_lobby", pt_data["lobby"]), key=f"u_lobby_{curr_id}")
            
            c3, c4, c5 = st.columns(3)
            fac_precast_rate = c3.number_input("Precast Rate", value=get_val("u_f_pre", pt_data["facade_precast_rate"]), key=f"u_f_pre_{curr_id}")
            fac_window_rate = c4.number_input("Window Wall Rate", value=get_val("u_f_win", pt_data["facade_window_rate"]), key=f"u_f_win_{curr_id}")
            fac_double_rate = c5.number_input("Double Skin Rate", value=get_val("u_f_doub", pt_data["facade_double_rate"]), key=f"u_f_doub_{curr_id}")

        with st.expander("🚪 Doors & Hardware Rates"):
            c1, c2 = st.columns(2)
            door_wood = c1.number_input("Wooden Door Rate", value=get_val("u_d_wood", pt_data["door_wood"]), key=f"u_d_wood_{curr_id}")
            door_glass = c2.number_input("Glass Door Rate", value=get_val("u_d_glass", pt_data["door_glass"]), key=f"u_d_glass_{curr_id}")
            door_steel = c1.number_input("Steel Door Rate", value=get_val("u_d_steel", pt_data["door_steel"]), key=f"u_d_steel_{curr_id}")
            hw_wood = c2.number_input("Hardware Wooden Door", value=get_val("u_hw_wood", pt_data["hw_wood"]), key=f"u_hw_wood_{curr_id}")
            hw_steel = c1.number_input("Hardware Steel Door", value=get_val("u_hw_steel", pt_data["hw_steel"]), key=f"u_hw_steel_{curr_id}")

        with st.expander("🚽 Sanitary Rates"):
            c1, c2 = st.columns(2)
            san_room_rate = c1.number_input("Typical Unit Sanitary Rate", value=get_val("u_s_room", pt_data["san_room_rate"]), key=f"u_s_room_{curr_id}")
            san_pub_m = c2.number_input("Public Toilet Male Rate", value=get_val("u_s_pub_m", pt_data["san_pub_m"]), key=f"u_s_pub_m_{curr_id}")
            san_pub_f = c1.number_input("Public Toilet Female Rate", value=get_val("u_s_pub_f", pt_data["san_pub_f"]), key=f"u_s_pub_f_{curr_id}")
            san_dis = c2.number_input("Disabled Toilet Rate", value=get_val("u_s_dis", pt_data["san_dis"]), key=f"u_s_dis_{curr_id}")
            san_mushola = c1.number_input("Mushola Rate", value=get_val("u_s_mushola", pt_data["san_mushola"]), key=f"u_s_mushola_{curr_id}")

        with st.expander("🛋️ Flooring, Finishes & Extra Rates"):
            c1, c2, c3 = st.columns(3)
            fl_ht_rate = c1.number_input("HT/Ceramic Rate", value=get_val("u_fl_ht", pt_data["fl_ht_rate"]), key=f"u_fl_ht_{curr_id}")
            fl_vinyl_rate = c2.number_input("Vinyl Rate", value=get_val("u_fl_vin", pt_data["fl_vinyl_rate"]), key=f"u_fl_vin_{curr_id}")
            fl_marmer_rate = c3.number_input("Marmer Rate", value=get_val("u_fl_mar", pt_data["fl_marmer_rate"]), key=f"u_fl_mar_{curr_id}")
            carpet_rate = c1.number_input("Carpet Rate", value=get_val("u_carpet", pt_data["carpet"]), key=f"u_carpet_{curr_id}")
            glass_rate = c2.number_input("Glass Work Rate", value=get_val("u_glass", pt_data["glass"]), key=f"u_glass_{curr_id}")
            skylight_rate = c3.number_input("Skylight Rate", value=get_val("u_sky", pt_data["skylight_rate"]), key=f"u_sky_{curr_id}")
            gondola_rate = c1.number_input("Gondola Rate", value=get_val("u_gondola", pt_data["gondola"]), key=f"u_gondola_{curr_id}")
            railing_rate = c2.number_input("Railing Rate", value=get_val("u_rail", pt_data["railing_rate"]), key=f"u_rail_{curr_id}")

        with st.expander("⚡ MEP & Equipment Rates"):
            c1, c2 = st.columns(2)
            mep_rate = c1.number_input("MEP Works", value=get_val("u_mep", pt_data["mep"]), key=f"u_mep_{curr_id}")
            utility_rate = c2.number_input("Utility Connection", value=get_val("u_util", pt_data["utility"]), key=f"u_util_{curr_id}")
            ffe_rate = c1.number_input("FF&E", value=get_val("u_ffe", pt_data["ffe"]), key=f"u_ffe_{curr_id}")
            kitchen_rate = c2.number_input("Kitchen Equipment", value=get_val("u_kit", pt_data["kitchen"]), key=f"u_kit_{curr_id}")
            misc_rate = c1.number_input("Misc (Linen/Gym LS)", value=get_val("u_misc", pt_data["misc"]), key=f"u_misc_{curr_id}")

        with st.expander("🌳 External & Facility Rates"):
            c1, c2 = st.columns(2)
            ext_land_rate = c1.number_input("External Works (Landscape)", value=get_val("u_ext", pt_data["ext_land"]), key=f"u_ext_{curr_id}")
            fac_pub_rate = c2.number_input("Public Facilities", value=get_val("u_fac_p", pt_data["fac_pub"]), key=f"u_fac_p_{curr_id}")
            fac_res_rate = c1.number_input("Resident Facilities", value=get_val("u_fac_r", pt_data["fac_res"]), key=f"u_fac_r_{curr_id}")
            fac_proj_rate = c2.number_input("Project Facilities", value=get_val("u_fac_pr", pt_data["fac_proj"]), key=f"u_fac_pr_{curr_id}")

    # --- TAB 4: SOFT COSTS SETUP ---
    with tab4:
        sc_col1, sc_col2 = st.columns(2)
        with sc_col1:
            consultancy_rate = st.number_input("Consultancy Rate", value=get_val("sc_cons", 0.0), step=1000.0, key=f"sc_cons_{curr_id}")
            qs_months = st.number_input("QS Duration (Months)", value=get_val("sc_qs_m", 0.0), step=1.0, key=f"sc_qs_m_{curr_id}")
            qs_rate = st.number_input("QS Rate (per Month)", value=get_val("sc_qs_r", 0.0), step=1000000.0, key=f"sc_qs_r_{curr_id}")
        with sc_col2:
            pm_months = st.number_input("PM Duration (Months)", value=get_val("sc_pm_m", 0.0), step=1.0, key=f"sc_pm_m_{curr_id}")
            pm_rate = st.number_input("PM Rate (per Month)", value=get_val("sc_pm_r", 0.0), step=1000000.0, key=f"sc_pm_r_{curr_id}")
            insurance_pct = st.number_input("Insurance (%)", value=get_val("sc_ins", 0.0), step=0.01, key=f"sc_ins_{curr_id}")

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
        t_pub_fac, t_res_fac, t_proj_fac,
        total_custom_cost # <--- Added here!
    ])

    t_preliminary = construction_subtotal * 0.05
    t_contingency = construction_subtotal * 0.03
    grand_total_hc = construction_subtotal + t_preliminary + t_contingency

    # --- SOFT COST CALCULATIONS ---
    t_consultancy = gfa * consultancy_rate
    t_qs = qs_months * qs_rate
    t_pm = pm_months * pm_rate
    t_insurance = construction_subtotal * (insurance_pct / 100.0)

    total_soft_cost = t_consultancy + t_qs + t_pm + t_insurance
    grand_total_project = grand_total_hc + total_soft_cost

    # --- CHART GROUPINGS ---
    group_structure = t_earth + t_found + t_struc
    group_arch = t_arch_base + t_w_door + t_g_door + t_s_door + t_lobby + t_ht + t_vinyl + t_marmer + t_carpet + t_glass_work + t_kitchen + t_hw_w + t_hw_s + t_railing + t_skylight
    group_facade = t_precast + t_window + t_double + t_gondola
    group_sanitary = t_unit_san + t_t_male + t_t_female + t_t_dis + t_mushola
    group_mep = t_ffe + t_misc + t_mep + t_utility
    group_ext = t_external + t_pub_fac + t_res_fac + t_proj_fac
    group_contingency = t_preliminary + t_contingency

# --- TAB 5: CUSTOM ITEMS ---
    with tab5:
        st.subheader("➕ Smart Custom Costs")
        st.info("Add custom scope items here. Select a linked metric (e.g., GFA) to automatically calculate: Rate × Multiplier × Metric.")
        
        # 1. Map the string names to your live variables from Tab 1
        dependency_map = {
            "None (Flat Rate)": 1.0, "GBA": gba, "GFA": gfa, "SGFA": sgfa,
            "Land Area": land_area, "Rooms": rooms, "Facade": facade, "Lobby": lobby_interior
        }
        
        # 2. Setup default table
        default_smart_cc = [{"Description": "", "Rate (Rp)": 0.0, "Multiplier (Qty)": 1.0, "Linked Dependency": "None (Flat Rate)"}]
        current_smart_cc = get_val("smart_custom_costs", default_smart_cc)
        
        # 3. Create the Data Editor
        edited_smart_cc = st.data_editor(
            pd.DataFrame(current_smart_cc), 
            num_rows="dynamic", 
            key=f"edit_smart_cc_{curr_id}", 
            column_config={
                "Linked Dependency": st.column_config.SelectboxColumn(
                    "Linked Dependency",
                    options=list(dependency_map.keys()),
                    required=True
                )
            },
            use_container_width=True
        )
        
        # 4. Background Math
        total_custom_cost = 0.0
        for index, row in edited_smart_cc.iterrows():
            rate = float(row.get("Rate (Rp)", 0.0))
            mult = float(row.get("Multiplier (Qty)", 1.0))
            dep_name = row.get("Linked Dependency", "None (Flat Rate)")
            dep_value = dependency_map.get(dep_name, 1.0) 
            total_custom_cost += (rate * mult * dep_value)
            
        st.markdown(f"**Total Custom Costs: Rp {total_custom_cost:,.2f}**")
        
        # 5. Save back to locker
        st.session_state.projects[curr_id]["data"]["smart_custom_costs"] = edited_smart_cc.to_dict('records')


    # --- TAB 6: RESULTS & SUMMARY ---
    with tab6:
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

        st.success("Calculations complete! View metrics below.")
        
        st.markdown("---")
        
        # Cost Breakdown Chart
        st.subheader("Total Project Cost Breakdown (Hard & Soft)")
        chart_data = pd.DataFrame({
            "Category": [
                "Structure/Foundation", "Architecture & Finishes", "Facade", 
                "Sanitary/Plumbing", "MEP & FF&E", "External/Facilities", 
                "Custom Additions (Hard)", # <--- Added Label here
                "Prelim & Contingency", 
                "Consultancy Fee (Soft)", "Quantity Surveyor (Soft)", 
                "Project Management (Soft)", "Insurance (Soft)"
            ],
            "Amount (Rp)": [
                group_structure, group_arch, group_facade, 
                group_sanitary, group_mep, group_ext,
                total_custom_cost,
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


# --- 2. GLOBAL EXPORT SECTION (Placed at the bottom) ---
    
    # Package ALL current variables into a dictionary
    current_metrics = {
        # Project Meta
        "proj_name": new_name, "proj_type": new_type,
        
        # Tab 1
        "m_land": land_area, "m_gba": gba, "m_gfa": gfa, "m_sgfa": sgfa,
        "m_facade": facade, "m_rooms": rooms, "m_lobby": lobby_interior, 
        "m_gondola": gondola_unit, "m_carpet": carpet_m2, "m_glass": glass_m2, 
        "m_skylight": skylight_area, "m_door_g": glass_door, "m_door_w": wooden_door, 
        "m_door_s": steel_door, "m_toil_m": toilet_male, "m_toil_f": toilet_female, 
        "m_toil_d": disabled_toil, "m_mushola": mushola_unit, "m_fac_res": res_fac_m2, 
        "m_fac_pub": pub_fac_m2, "m_fac_proj": proj_fac_u, "m_land_m2": land_m2,
        
        # Tab 2
        "r_fac_pre": facade_precast_pct, "r_fac_win": facade_window_pct, "r_fac_doub": facade_double_pct,
        "r_fl_ht": fl_ht_pct, "r_fl_vin": fl_vinyl_pct, "r_fl_mar": fl_marmer_pct,
        "r_san_qty": san_qty_room, "r_rail_qty": railing_qty,
        
        # Tab 3
        "u_earth": struc_earth, "u_found": struc_found, "u_struc": struc_work, "u_arch": arch_base, 
        "u_lobby": lobby_rate, "u_f_pre": fac_precast_rate, "u_f_win": fac_window_rate, "u_f_doub": fac_double_rate,
        "u_d_wood": door_wood, "u_d_glass": door_glass, "u_d_steel": door_steel, "u_hw_wood": hw_wood, "u_hw_steel": hw_steel,
        "u_s_room": san_room_rate, "u_s_pub_m": san_pub_m, "u_s_pub_f": san_pub_f, "u_s_dis": san_dis, "u_s_mushola": san_mushola,
        "u_fl_ht": fl_ht_rate, "u_fl_vin": fl_vinyl_rate, "u_fl_mar": fl_marmer_rate, "u_carpet": carpet_rate, "u_glass": glass_rate,
        "u_sky": skylight_rate, "u_gondola": gondola_rate, "u_rail": railing_rate, "u_mep": mep_rate, "u_util": utility_rate,
        "u_ffe": ffe_rate, "u_kit": kitchen_rate, "u_misc": misc_rate, "u_ext": ext_land_rate, "u_fac_p": fac_pub_rate, 
        "u_fac_r": fac_res_rate, "u_fac_pr": fac_proj_rate,
        
        # Tab 4
        "sc_cons": consultancy_rate, "sc_qs_m": qs_months, "sc_qs_r": qs_rate, 
        "sc_pm_m": pm_months, "sc_pm_r": pm_rate, "sc_ins": insurance_pct
    }
    
    # MAGIC TRICK: Save live metrics into the master locker so they survive switching!
    st.session_state.projects[curr_id]["data"] = current_metrics

    # Convert to CSV string format
    df_export = pd.DataFrame(list(current_metrics.items()), columns=["Metric_Key", "Value"])
    csv_data = df_export.to_csv(index=False).encode('utf-8')

    # Ensure the subheader is OUTSIDE the button parentheses
    st.sidebar.markdown("---")
    st.sidebar.subheader("Download CSV")
    st.sidebar.download_button(
        label="Download Here",
        data=csv_data,
        file_name=f"{new_name.replace(' ', '_').lower()}_config.csv",
        mime="text/csv",
        use_container_width=True
    )

# --- 4. MAIN NAVIGATION & SIDEBAR PROJECT LIST ---
st.sidebar.title("Main Navigation")

# Workspace Selector (Using standard radio, or segmented_control if Streamlit 1.36+)
page_choice = st.sidebar.radio(
    "Select Workspace:", 
    ["Cost Calculator", "Area Calculator"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Project List")

# "Add Project" Button
if st.sidebar.button("➕ Add New Project", use_container_width=True):
    st.session_state.proj_counter += 1
    new_id = f"proj_{st.session_state.proj_counter}"
    # Added "data": {} to new projects as well!
    st.session_state.projects[new_id] = {"name": f"New Project {st.session_state.proj_counter}", "type": "Hotel", "data": {}}
    st.session_state.current_proj_id = new_id
    st.rerun()

# Format the list to show: "Name (Type)"
proj_ids = list(st.session_state.projects.keys())
proj_labels = [f"{st.session_state.projects[pid]['name']} ({st.session_state.projects[pid]['type']})" for pid in proj_ids]

# Find index of current project to keep it highlighted
current_index = proj_ids.index(st.session_state.current_proj_id) if st.session_state.current_proj_id in proj_ids else 0

# The Project Selection List
selected_label = st.sidebar.radio(
    "Select Active Project:",
    options=proj_labels,
    index=current_index,
    key="project_selector"
)

# Sync sidebar clicks back to session state
selected_idx = proj_labels.index(selected_label)
if st.session_state.current_proj_id != proj_ids[selected_idx]:
    st.session_state.current_proj_id = proj_ids[selected_idx]
    st.rerun() # Refresh to show the newly clicked project's data

st.sidebar.markdown("---")


# --- 5. EXECUTION LOGIC ---
if page_choice == "Area Calculator":
    show_area_calculator()
else:
    show_cost_estimator()
