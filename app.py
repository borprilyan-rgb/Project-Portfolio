import streamlit as st
import pandas as pd
import altair as alt

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
        "fl_ht_pct": 90.0, "fl_ht_rate": {"Standard": 150000.0, "Premium": 350000.0}, 
        "fl_vinyl_pct": 0.0, "fl_vinyl_rate": {"Standard": 500000.0, "Premium": 750000.0},
        "fl_marmer_pct": 10.0, "fl_marmer_rate": {"Standard": 750000.0, "Premium": 1500000.0},
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
        "fl_ht_pct": 90.0, "fl_ht_rate": {"Standard": 150000.0, "Premium": 350000.0}, 
        "fl_vinyl_pct": 0.0, "fl_vinyl_rate": {"Standard": 500000.0, "Premium": 750000.0},
        "fl_marmer_pct": 10.0, "fl_marmer_rate": {"Standard": 750000.0, "Premium": 1500000.0},
        "kitchen": 0.0, "hw_wood": 400000.0, "hw_steel": 700000.0, "carpet": 250000.0,
        "glass": 550000.0, "ffe": 0.0, "misc": 100000000.0, "mep": 4000000.0,
        "utility": 150000.0, "railing_qty": 0.0, "railing_rate": 800000.0, 
        "skylight_rate": 2500000.0,
        "ext_land": 600000.0, "fac_pub": 2000000.0, "fac_res": 0.0, "fac_proj": 3000000.0
    },
    "Apartment": {
        "struc_earth": 120000.0, "struc_found": 450000.0, "struc_work": 3000000.0,
        "facade_precast_pct": 10.0, "facade_precast_rate": 750000.0,
        "facade_window_pct": 80.0, "facade_window_rate": 1100000.0,
        "facade_double_pct": 10.0, "facade_double_rate": 2200000.0,
        "arch_base": 2500000.0, "door_wood": 2000000.0, "door_glass": 6000000.0,
        "door_steel": 5000000.0, "lobby": 6000000.0, "gondola": 450000000.0,
        "san_room_qty": 0.0, "san_room_rate": 0.0, "san_pub_m": 35000000.0, 
        "san_pub_f": 35000000.0, "san_dis": 35000000.0, "san_mushola": 15000000.0,
        "fl_ht_pct": 90.0, "fl_ht_rate": {"Standard": 150000.0, "Premium": 350000.0}, 
        "fl_vinyl_pct": 0.0, "fl_vinyl_rate": {"Standard": 500000.0, "Premium": 750000.0},
        "fl_marmer_pct": 10.0, "fl_marmer_rate": {"Standard": 750000.0, "Premium": 1500000.0},
        "kitchen": 0.0, "hw_wood": 400000.0, "hw_steel": 700000.0, "carpet": 250000.0,
        "glass": 550000.0, "ffe": 0.0, "misc": 100000000.0, "mep": 4000000.0,
        "utility": 150000.0, "railing_qty": 0.0, "railing_rate": 800000.0, 
        "skylight_rate": 2500000.0,
        "ext_land": 600000.0, "fac_pub": 2000000.0, "fac_res": 0.0, "fac_proj": 3000000.0
    },
    "Parking": {
        "struc_earth": 120000.0, "struc_found": 450000.0, "struc_work": 3000000.0,
        "facade_precast_pct": 10.0, "facade_precast_rate": 750000.0,
        "facade_window_pct": 80.0, "facade_window_rate": 1100000.0,
        "facade_double_pct": 10.0, "facade_double_rate": 2200000.0,
        "arch_base": 2500000.0, "door_wood": 2000000.0, "door_glass": 6000000.0,
        "door_steel": 5000000.0, "lobby": 6000000.0, "gondola": 450000000.0,
        "san_room_qty": 0.0, "san_room_rate": 0.0, "san_pub_m": 35000000.0, 
        "san_pub_f": 35000000.0, "san_dis": 35000000.0, "san_mushola": 15000000.0,
        "fl_ht_pct": 90.0, "fl_ht_rate": {"Standard": 150000.0, "Premium": 350000.0}, 
        "fl_vinyl_pct": 0.0, "fl_vinyl_rate": {"Standard": 500000.0, "Premium": 750000.0},
        "fl_marmer_pct": 10.0, "fl_marmer_rate": {"Standard": 750000.0, "Premium": 1500000.0},
        "kitchen": 0.0, "hw_wood": 400000.0, "hw_steel": 700000.0, "carpet": 250000.0,
        "glass": 550000.0, "ffe": 0.0, "misc": 100000000.0, "mep": 4000000.0,
        "utility": 150000.0, "railing_qty": 0.0, "railing_rate": 800000.0, 
        "skylight_rate": 2500000.0,
        "ext_land": 600000.0, "fac_pub": 2000000.0, "fac_res": 0.0, "fac_proj": 3000000.0
    }}

# --- 2.2 LIGHTNING-FAST CALLBACK FUNCTIONS ---
def cb_add_project():
    st.session_state.proj_counter += 1
    new_id = f"proj_{st.session_state.proj_counter}"
    st.session_state.projects[new_id] = {"name": f"New Project {st.session_state.proj_counter}", "type": "Hotel", "data": {}}
    st.session_state.current_proj_id = new_id

def cb_delete_project():
    del st.session_state.projects[st.session_state.current_proj_id]
    st.session_state.current_proj_id = list(st.session_state.projects.keys())[0]

def cb_switch_project():
    selected_label = st.session_state.project_selector
    proj_ids = list(st.session_state.projects.keys())
    proj_labels = [f"{st.session_state.projects[pid]['name']} ({st.session_state.projects[pid]['type']})" for pid in proj_ids]
    if selected_label in proj_labels:
        selected_idx = proj_labels.index(selected_label)
        st.session_state.current_proj_id = proj_ids[selected_idx]     

# --- 2.5 SESSION STATE (PROJECT MEMORY) ---
if "projects" not in st.session_state:
    st.session_state.projects = {
        "proj_1": {"name": "New Project 1", "type": "Hotel", "data": {}}
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


def update_price(metric_key, db_key):
    """Fungsi umum untuk update harga DAN teks spek berdasarkan radio"""
    c_id = st.session_state.current_proj_id
    p_type = st.session_state.projects[c_id]["type"]
    
    # 1. Ambil pilihan spek dari radio (Standard/Premium)
    selected_spec = st.session_state[f"temp_spec_{metric_key}_{c_id}"]
    
    # 2. Update TEKS spek di data locker agar masuk ke CSV
    # Ini yang membuat data di image Bapak tidak berubah tadi
    st.session_state.projects[c_id]["data"][f"{metric_key}_spec_type"] = selected_spec
    
    # 3. Ambil data harga dari database
    db_val = PROJECT_DATABASE[p_type][db_key]
    
    if isinstance(db_val, dict):
        new_val = db_val.get(selected_spec, 0.0)
        # 4. TIMPA nilai angka di number_input
        st.session_state[f"u_fl_{metric_key}_{c_id}"] = float(new_val)

# COST ESTIMATOR ---
def show_cost_estimator():
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
    st.subheader("Data Proyek")
    c1, c2, c3, c4, c5 = st.columns(5)

    new_name = c1.text_input("Nama Proyek", value=curr_proj["name"])
    types_list = ["Hotel", "Retail", "Apartment", "Parking"]
    type_index = types_list.index(curr_proj["type"]) if curr_proj["type"] in types_list else 0
    new_type = c2.selectbox("Jenis Proyek", types_list, index=type_index)

    if new_name != curr_proj["name"] or new_type != curr_proj["type"]:
        st.session_state.projects[curr_id]["name"] = new_name
        st.session_state.projects[curr_id]["type"] = new_type
        st.rerun()

    pt_data = PROJECT_DATABASE[new_type]
    st.markdown("---")

    # --- 1. GLOBAL IMPORT SECTION (Sidebar) ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Upload .csv")
    
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
                        # LOGIKA BARU: Cek apakah nilai adalah teks spek atau angka
                        if str(val) in ["Standard", "Premium"]:
                            # Simpan sebagai teks jika Standard/Premium
                            st.session_state.projects[curr_id]["data"][key] = str(val)
                        else:
                            try:
                                # Simpan sebagai angka untuk volume/harga
                                st.session_state.projects[curr_id]["data"][key] = float(val)
                            except:
                                # Backup jika ada teks lain
                                st.session_state.projects[curr_id]["data"][key] = str(val)
                
                st.session_state.last_loaded_file = uploaded_file.file_id
                st.sidebar.success("✅ Loaded successfully!")
                st.rerun() 
            except Exception as e:
                st.sidebar.error(f"❌ Error loading file: {e}")

# --- Tambahkan ini di paling bawah section sidebar (sekitar baris 430+) ---
                st.sidebar.markdown("---")
                st.sidebar.subheader("Export Data")

                # Siapkan Data untuk CSV
    csv_data = []
    # Ambil meta data proyek
    csv_data.append({"Metric_Key": "proj_name", "Value": curr_proj["name"]})
    csv_data.append({"Metric_Key": "proj_type", "Value": curr_proj["type"]})

    # Masukkan semua data dari master locker
    for k, v in st.session_state.projects[curr_id]["data"].items():
        if k != "smart_custom_costs" and k != "header_info" and k != "assumptions":
            csv_data.append({"Metric_Key": k, "Value": v})

    df_export = pd.DataFrame(csv_data)
    csv_buffer = df_export.to_csv(index=False).encode('utf-8')

    st.sidebar.download_button(
        label="Download CSV",
        data=csv_buffer,
        file_name=f"Database_{curr_id}.csv",
        mime="text/csv",
        use_container_width=True
    )

    # --- TABS LAYOUT ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "1. Ukuran", "2. Persen dan Pengali", 
        "3. Harga", "4. Soft Costs", 
        "5. Item Tambahan", "6. Hasil"
    ])

    # --- TAB 1: PROJECT METRICS ---
    with tab1:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            with st.expander("Ukuran Proyek (GBA, GFA, SGFA)", expanded=True):
                st.subheader("Ukuran")
                land_area = st.number_input("Luas Tanah (m2)", value=get_val("m_land", 0.0), step=100.0, key=f"m_land_{curr_id}")
                gba = st.number_input("GBA (m2)", value=get_val("m_gba", 0.0), step=100.0, key=f"m_gba_{curr_id}")
                gfa = st.number_input("GFA (m2)", value=get_val("m_gfa", 0.0), step=100.0, key=f"m_gfa_{curr_id}")
                sgfa = st.number_input("SGFA (m2)", value=get_val("m_sgfa", 0.0), step=100.0, key=f"m_sgfa_{curr_id}")
        with col_m2:    
            with st.expander("Arsitektur", expanded=True):
                st.subheader("Interior")
                rooms = st.number_input("Ruang (unit)", help="Jumlah ruang dalam proyek", value=get_val("m_rooms", 0.0), step=1.0, key=f"m_rooms_{curr_id}")
                facade = st.number_input("Facade (m2)", value=get_val("m_facade", 0.0), step=100.0, key=f"m_facade_{curr_id}")
                lobby_interior = st.number_input("Lobby Interior (m2)", value=get_val("m_lobby", 0.0), step=10.0, key=f"m_lobby_{curr_id}")
                carpet_m2 = st.number_input("Karpet (m2)", value=get_val("m_carpet", 0.0), step=10.0, key=f"m_carpet_{curr_id}")
                glass_m2 = st.number_input("Kaca (m2)", value=get_val("m_glass", 0.0), step=10.0, key=f"m_glass_{curr_id}")
                st.subheader("Eksterior")
                gondola_unit = st.number_input("Gondola (unit)", value=get_val("m_gondola", 0.0), step=1.0, key=f"m_gondola_{curr_id}")
                skylight_area = st.number_input("Skylight (m2)", value=get_val("m_skylight", 0.0), step=10.0, key=f"m_skylight_{curr_id}")
                st.subheader("Pintu")
                glass_door = st.number_input("Glass Door (unit)", value=get_val("m_door_g", 0.0), step=1.0, key=f"m_door_g_{curr_id}")
                wooden_door = st.number_input("Wooden Door (unit)", value=get_val("m_door_w", 0.0), step=10.0, key=f"m_door_w_{curr_id}")
                steel_door = st.number_input("Steel Door (unit)", value=get_val("m_door_s", 0.0), step=10.0, key=f"m_door_s_{curr_id}")

        with col_m3:
            with st.expander("Sanitari", expanded=True):
                st.subheader("Toilet Unit")
                san_qty_room = st.number_input("Toilet Private (unit/ruang)", help= "Cth. 3 Toilet/1 Kamar (Apt)", value=get_val("r_san_qty", pt_data["san_room_qty"]), key=f"r_san_qty_{curr_id}")
                st.subheader("Toilet Umum")
                toilet_male = st.number_input("Toilet Umum - Pria (units)", value=get_val("m_toil_m", 0.0), step=1.0, key=f"m_toil_m_{curr_id}")
                toilet_female = st.number_input("Toilet Umum - Wanita (units)", value=get_val("m_toil_f", 0.0), step=1.0, key=f"m_toil_f_{curr_id}")
                disabled_toil = st.number_input("Toilet Difabel (units)", value=get_val("m_toil_d", 0.0), step=1.0, key=f"m_toil_d_{curr_id}")
                st.subheader("Mushola")
                mushola_unit = st.number_input("Mushola (units)", value=get_val("m_mushola", 0.0), step=1.0, key=f"m_mushola_{curr_id}")

        with col_m4:
            with st.expander("Sanitari", expanded=True):
                st.subheader("Fasilitas")
                res_fac_m2 = st.number_input("Fasilitas Penghuni (m2)", value=get_val("m_fac_res", 0.0), step=10.0, key=f"m_fac_res_{curr_id}") 
                pub_fac_m2 = st.number_input("Fasilitas Publik (m2)", value=get_val("m_fac_pub", 0.0), step=10.0, key=f"m_fac_pub_{curr_id}")
                proj_fac_u = st.number_input("Fasilitas Proyek (unit)", value=get_val("m_fac_proj", 0.0), step=1.0, key=f"m_fac_proj_{curr_id}")
                land_m2 = st.number_input("Area Lanskap (m2)", value=get_val("m_land_m2", 0.0), step=100.0, key=f"m_land_m2_{curr_id}")
                # Bagian Misc Switch
                st.subheader("Miscellaneous")
                m_status = st.radio("Ada Gym/Linen?", ["Tidak", "Ada"], 
                                    index=1 if get_val("misc_switch", 0) == 1 else 0,
                                    key=f"misc_sw_{curr_id}", horizontal=True)
                misc_switch = 1 if m_status == "Ada" else 0
                st.session_state.projects[curr_id]["data"]["misc_switch"] = misc_switch
                
                if misc_switch == 1:
                    m_rate = st.number_input("Rate Misc (Rp)", value=get_val("u_misc", pt_data["misc"]), key=f"u_misc_val_{curr_id}")
                    st.session_state.projects[curr_id]["data"]["u_misc"] = m_rate
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
            railing_qty = st.number_input("Railing Length (m'/room)", value=get_val("r_rail_qty", pt_data["railing_qty"]), key=f"r_rail_qty_{curr_id}")

    # --- TAB 3: UNIT RATES ---
    with tab3:
        with st.expander("Harga Fondasi & Struktur", expanded=True):
            c1, c2, c3 = st.columns(3)
            struc_earth = c1.number_input("Earthwork Rate (Rp)", value=get_val("u_earth", pt_data["struc_earth"]), key=f"u_earth_{curr_id}")
            struc_found = c2.number_input("Foundation Rate (Rp)", value=get_val("u_found", pt_data["struc_found"]), key=f"u_found_{curr_id}")
            struc_work = c3.number_input("Structural Work Rate (Rp)", value=get_val("u_struc", pt_data["struc_work"]), key=f"u_struc_{curr_id}")
            
        with st.expander("Arsitektur & Fasad"):
            c1, c2 = st.columns(2)
            arch_base = c1.number_input("Architecture Base (Rp)", value=get_val("u_arch", pt_data["arch_base"]), key=f"u_arch_{curr_id}")
            lobby_rate = c2.number_input("Lobby Interior Rate (Rp)", value=get_val("u_lobby", pt_data["lobby"]), key=f"u_lobby_{curr_id}")
            
            c3, c4, c5 = st.columns(3)
            fac_precast_rate = c3.number_input("Precast Rate (Rp)", value=get_val("u_f_pre", pt_data["facade_precast_rate"]), key=f"u_f_pre_{curr_id}")
            fac_window_rate = c4.number_input("Window Wall Rate (Rp)", value=get_val("u_f_win", pt_data["facade_window_rate"]), key=f"u_f_win_{curr_id}")
            fac_double_rate = c5.number_input("Double Skin Rate (Rp)", value=get_val("u_f_doub", pt_data["facade_double_rate"]), key=f"u_f_doub_{curr_id}")

        with st.expander("Pintu dan Hardware"):
            c1, c2 = st.columns(2)
            door_wood = c1.number_input("Wooden Door Rate (Rp)", value=get_val("u_d_wood", pt_data["door_wood"]), key=f"u_d_wood_{curr_id}")
            door_glass = c2.number_input("Glass Door Rate (Rp)", value=get_val("u_d_glass", pt_data["door_glass"]), key=f"u_d_glass_{curr_id}")
            door_steel = c1.number_input("Steel Door Rate (Rp)", value=get_val("u_d_steel", pt_data["door_steel"]), key=f"u_d_steel_{curr_id}")
            hw_wood = c2.number_input("Hardware Wooden Door (Rp)", value=get_val("u_hw_wood", pt_data["hw_wood"]), key=f"u_hw_wood_{curr_id}")
            hw_steel = c1.number_input("Hardware Steel Door (Rp)", value=get_val("u_hw_steel", pt_data["hw_steel"]), key=f"u_hw_steel_{curr_id}")

        with st.expander("Sanitari"):
            c1, c2 = st.columns(2)
            san_room_rate = c1.number_input("Typical Unit Sanitary Rate (Rp)", value=get_val("u_s_room", pt_data["san_room_rate"]), key=f"u_s_room_{curr_id}")
            san_pub_m = c2.number_input("Public Toilet Male Rate (Rp)", value=get_val("u_s_pub_m", pt_data["san_pub_m"]), key=f"u_s_pub_m_{curr_id}")
            san_pub_f = c1.number_input("Public Toilet Female Rate (Rp)", value=get_val("u_s_pub_f", pt_data["san_pub_f"]), key=f"u_s_pub_f_{curr_id}")
            san_dis = c2.number_input("Disabled Toilet Rate (Rp)", value=get_val("u_s_dis", pt_data["san_dis"]), key=f"u_s_dis_{curr_id}")
            san_mushola = c1.number_input("Mushola Rate (Rp)", value=get_val("u_s_mushola", pt_data["san_mushola"]), key=f"u_s_mushola_{curr_id}")

        with st.expander("Lantai, Finishing, dan Interior"):
            c1, c2, c3 = st.columns(3)
            st.markdown("**HT/Ceramic Specification**")
            with c1:
                # --- HT ---
                st.radio("Spek HT", ["Standard", "Premium"], 
                    key=f"temp_spec_ht_{curr_id}", # Key Unik
                    horizontal=True, 
                    on_change=update_price, args=("ht", "fl_ht_rate")) # Kirim info HT
                fl_ht_rate = st.number_input("HT Rate (Rp)", 
                                            value=get_val("u_fl_ht", pt_data["fl_ht_rate"]["Standard"]), 
                                            key=f"u_fl_ht_{curr_id}")
            with c2:
                # --- VINYL ---
                st.radio("Spek Vinyl", ["Standard", "Premium"], 
                    key=f"temp_spec_vin_{curr_id}", # Key Unik
                    horizontal=True, 
                    on_change=update_price, args=("vin", "fl_vinyl_rate")) # Kirim info Vinyl
                fl_vinyl_rate = st.number_input("Vinyl Rate (Rp)", 
                                                value=get_val("u_fl_vin", pt_data["fl_vinyl_rate"]["Standard"]), 
                                                key=f"u_fl_vin_{curr_id}")
            with c3:
                # --- MARMER ---
                st.radio("Spek Marmer", ["Standard", "Premium"], 
                    key=f"temp_spec_mar_{curr_id}", # Key Unik
                    horizontal=True, 
                    on_change=update_price, args=("mar", "fl_marmer_rate")) # Kirim info Marmer
                fl_marmer_rate = st.number_input("Marmer Rate (Rp)", 
                                                value=get_val("u_fl_mar", pt_data["fl_marmer_rate"]["Standard"]), 
                                                key=f"u_fl_mar_{curr_id}")
                
            carpet_rate = c1.number_input("Carpet Rate (Rp)", value=get_val("u_carpet", pt_data["carpet"]), key=f"u_carpet_{curr_id}")
            glass_rate = c2.number_input("Glass Work Rate (Rp)", value=get_val("u_glass", pt_data["glass"]), key=f"u_glass_{curr_id}")
            skylight_rate = c3.number_input("Skylight Rate (Rp)", value=get_val("u_sky", pt_data["skylight_rate"]), key=f"u_sky_{curr_id}")
            gondola_rate = c1.number_input("Gondola Rate (Rp)", value=get_val("u_gondola", pt_data["gondola"]), key=f"u_gondola_{curr_id}")
            railing_rate = c2.number_input("Railing Rate (Rp)", value=get_val("u_rail", pt_data["railing_rate"]), key=f"u_rail_{curr_id}")

        with st.expander("MEP, Dapur dan FF&E "):
            c1, c2 = st.columns(2)
            mep_rate = c1.number_input("MEP Works (Rp)", value=get_val("u_mep", pt_data["mep"]), key=f"u_mep_{curr_id}")
            utility_rate = c2.number_input("Utility Connection (Rp)", value=get_val("u_util", pt_data["utility"]), key=f"u_util_{curr_id}")
            ffe_rate = c1.number_input("FF&E (Rp)", value=get_val("u_ffe", pt_data["ffe"]), key=f"u_ffe_{curr_id}")
            kitchen_rate = c2.number_input("Kitchen Equipment (Rp)", value=get_val("u_kit", pt_data["kitchen"]), key=f"u_kit_{curr_id}")
            misc_rate = c1.number_input("Misc (Linen/Gym Equipment) (Rp)", value=get_val("u_misc", pt_data["misc"]), key=f"u_misc_{curr_id}")

        with st.expander("External & Facility Rates"):
            c1, c2 = st.columns(2)
            ext_land_rate = c1.number_input("External Works (Landscape) (Rp)", value=get_val("u_ext", pt_data["ext_land"]), key=f"u_ext_{curr_id}")
            fac_pub_rate = c2.number_input("Public Facilities (Rp)", value=get_val("u_fac_p", pt_data["fac_pub"]), key=f"u_fac_p_{curr_id}")
            fac_res_rate = c1.number_input("Resident Facilities (Rp)", value=get_val("u_fac_r", pt_data["fac_res"]), key=f"u_fac_r_{curr_id}")
            fac_proj_rate = c2.number_input("Project Facilities (Rp)", value=get_val("u_fac_pr", pt_data["fac_proj"]), key=f"u_fac_pr_{curr_id}")

    # --- TAB 4: SOFT COSTS SETUP ---
    with tab4:
        sc_col1, sc_col2 = st.columns(2)
        with sc_col1:
            consultancy_rate = st.number_input("Consultancy Rate (Rp)", value=get_val("sc_cons", 0.0), step=1000.0, key=f"sc_cons_{curr_id}")
            qs_months = st.number_input("QS Duration (Months)", value=get_val("sc_qs_m", 0.0), step=1.0, key=f"sc_qs_m_{curr_id}")
            qs_rate = st.number_input("QS Rate (per Month) (Rp)", value=get_val("sc_qs_r", 0.0), step=1000000.0, key=f"sc_qs_r_{curr_id}")
        with sc_col2:
            pm_months = st.number_input("PM Duration (Months)", value=get_val("sc_pm_m", 0.0), step=1.0, key=f"sc_pm_m_{curr_id}")
            pm_rate = st.number_input("PM Rate (per Month) (Rp)", value=get_val("sc_pm_r", 0.0), step=1000000.0, key=f"sc_pm_r_{curr_id}")
            insurance_pct = st.number_input("Insurance (%)", value=get_val("sc_ins", 0.0), step=0.01, key=f"sc_ins_{curr_id}")

# --- TAB 5: CUSTOM ITEMS ---
    with tab5:
        st.subheader("Smart Custom Costs")
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
    t_misc = misc_rate * misc_switch
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
    group_arch = t_arch_base + t_w_door + t_g_door + t_s_door + t_lobby + t_ht + t_vinyl + t_marmer + t_carpet + t_gondola + t_glass_work + t_kitchen + t_hw_w + t_hw_s + t_railing + t_skylight
    group_facade = t_precast + t_window + t_double 
    group_sanitary = t_unit_san + t_t_male + t_t_female + t_t_dis + t_mushola
    group_mep = t_ffe + t_misc + t_mep + t_utility
    group_ext = t_external + t_pub_fac + t_res_fac + t_proj_fac
    group_contingency = t_preliminary + t_contingency


    # --- TAB 6: RESULTS & SUMMARY ---
    with tab6:
        st.markdown("---")
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
                t_proj_fac, 
                total_custom_cost,  # <--- PASTIKAN INI ADA DI SINI (URUTAN KE-37)
                t_contingency, 
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
                    "36. Project Facilities", "37. Smart Custom Costs", # <-- Pastikan deskripsi ini ada
                    "38. Contingencies", "39. Consultancy Fee", "40. Quantity Surveyor", "41. Project Management", "42. Insurance Coverage"
                ],
                "Basis": [
                    "5% Subtotal Hard Cost", 
                    f"{gba:,.0f} m2 x Rp {struc_earth:,.0f}", 
                    f"{gba:,.0f} m2 x Rp {struc_found:,.0f}", 
                    f"{gba:,.0f} m2 x Rp {struc_work:,.0f}",  
                    f"{gfa:,.0f} m2 x Rp {arch_base:,.0f}",   
                    f"{facade_precast_pct}% of Facade x Rp {fac_precast_rate:,.0f}", 
                    f"{facade_window_pct}% of Facade x Rp {fac_window_rate:,.0f}", 
                    f"{facade_double_pct}% of Facade x Rp {fac_double_rate:,.0f}", 
                    f"{wooden_door:,.0f} Units x Rp {door_wood:,.0f}", 
                    f"{glass_door:,.0f} Units x Rp {door_glass:,.0f}", 
                    f"{steel_door:,.0f} Units x Rp {door_steel:,.0f}", 
                    f"{lobby_interior:,.0f} m2 x Rp {lobby_rate:,.0f}", 
                    f"{gondola_unit:,.0f} Units x Rp {gondola_rate:,.0f}", 
                    f"{rooms:,.0f} Rms x {san_qty_room} Set x Rp {san_room_rate:,.0f}", 
                    f"{toilet_male:,.0f} Units x Rp {san_pub_m:,.0f}", 
                    f"{toilet_female:,.0f} Units x Rp {san_pub_f:,.0f}", 
                    f"{disabled_toil:,.0f} Units x Rp {san_dis:,.0f}", 
                    f"{mushola_unit:,.0f} Units x Rp {san_mushola:,.0f}", 
                    f"{rooms:,.0f} Rooms x Rp {kitchen_rate:,.0f}", 
                    f"{wooden_door:,.0f} Doors x Rp {hw_wood:,.0f}", 
                    f"{steel_door:,.0f} Doors x Rp {hw_steel:,.0f}", 
                    f"{fl_ht_pct}% of GFA x {f_mult} x Rp {fl_ht_rate:,.0f} ({get_val('ht_spec_type', 'Standard')})", 
                    f"{fl_vinyl_pct}% of GFA x {f_mult} x Rp {fl_vinyl_rate:,.0f}", 
                    f"{fl_marmer_pct}% of GFA x {f_mult} x Rp {fl_marmer_rate:,.0f}", 
                    f"{carpet_m2:,.0f} m2 x Rp {carpet_rate:,.0f}", 
                    f"{glass_m2:,.0f} m2 x Rp {glass_rate:,.0f}", 
                    f"{rooms:,.0f} Rooms x Rp {ffe_rate:,.0f}", 
                    "Switch: " + ("ON" if misc_switch else "OFF") + f" | Rp {misc_rate:,.0f}", 
                    f"{gba:,.0f} m2 x Rp {mep_rate:,.0f}", 
                    f"{gba:,.0f} m2 x Rp {utility_rate:,.0f}", 
                    f"{rooms * railing_qty:,.0f} m' Total x Rp {railing_rate:,.0f}", 
                    f"{skylight_area:,.0f} m2 Total x Rp {skylight_rate:,.0f}", 
                    f"{land_m2:,.0f} m2 x Rp {ext_land_rate:,.0f}", 
                    f"{pub_fac_m2:,.0f} m2 x Rp {fac_pub_rate:,.0f}", 
                    f"{res_fac_m2:,.0f} m2 x Rp {fac_res_rate:,.0f}", 
                    f"{proj_fac_u:,.0f} Units x Rp {fac_proj_rate:,.0f}",
                    " | ".join(get_val("extra_items_summary_list", ["-"])), # 37. Smart Custom Costs
                    "3% Subtotal Hard Cost",
                    f"{gfa:,.0f} m2 x Rp {consultancy_rate:,.0f}", 
                    f"{qs_months} Months x Rp {qs_rate:,.0f}/Mo", 
                    f"{pm_months} Months x Rp {pm_rate:,.0f}/Mo", 
                    f"{insurance_pct}% of Construction Subtotal"
                ],
                "Amount": [f"Rp {val:,.2f}" for val in raw_amounts]
            }
            st.dataframe(pd.DataFrame(cost_data), use_container_width=True, hide_index=True)


# --- 2. GLOBAL EXPORT SECTION ---
    
    # Package ALL current variables into a dictionary
    current_metrics = {
        # Project Meta
        "proj_name": new_name, 
        "proj_type": new_type,
        "misc_switch": misc_switch,
        "ht_spec_type": get_val("ht_spec_type", "Standard"),
        "vin_spec_type": get_val("vin_spec_type", "Standard"),
        "mar_spec_type": get_val("mar_spec_type", "Standard"),
        
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
        "u_ffe": ffe_rate, "u_kit": kitchen_rate, "u_misc": m_rate if misc_switch == 1 else 0.0, "u_ext": ext_land_rate, "u_fac_p": fac_pub_rate, 
        "u_fac_r": fac_res_rate, "u_fac_pr": fac_proj_rate,
        
        # Tab 4
        "sc_cons": consultancy_rate, "sc_qs_m": qs_months, "sc_qs_r": qs_rate, 
        "sc_pm_m": pm_months, "sc_pm_r": pm_rate, "sc_ins": insurance_pct
    }
    
    # Save live metrics into the master locker
    st.session_state.projects[curr_id]["data"] = current_metrics

def show_portfolio_summary():
    import io
    import xlsxwriter
    import re
    from datetime import date
    st.markdown("---")
    
    active_id = st.session_state.current_proj_id
    today_str = date.today().strftime("%d-%m-%Y")
    
    # 1. Ensure header data exists
    if "header_info" not in st.session_state.projects[active_id]["data"]:
        st.session_state.projects[active_id]["data"]["header_info"] = {
            "rev_no": "0",
            "updated": today_str,
            "created": today_str
        }

    # 2. --- HEADER & ASSUMPTIONS EDITOR ---
    with st.expander("📝 Edit Report Header & Assumptions", expanded=False):
        h_col1, h_col2, h_col3 = st.columns(3)
        rev_input = h_col1.text_input("Revision Number:", value=st.session_state.projects[active_id]["data"]["header_info"]["rev_no"], key=f"rev_{active_id}")
        upd_input = h_col2.text_input("Updated Date:", value=st.session_state.projects[active_id]["data"]["header_info"]["updated"], key=f"upd_{active_id}")
        cre_input = h_col3.text_input("Created Date:", value=st.session_state.projects[active_id]["data"]["header_info"]["created"], key=f"cre_{active_id}")
        
        st.session_state.projects[active_id]["data"]["header_info"] = {"rev_no": rev_input, "updated": upd_input, "created": cre_input}
        
        st.divider()
        current_assums = st.session_state.projects[active_id]["data"].get("assumptions", ["Foundation System standard pilecaps.", "No Basement."])
        df_assum = pd.DataFrame(current_assums, columns=["Note"])
        ed_assum = st.data_editor(df_assum, num_rows="dynamic", use_container_width=True, key=f"ed_sum_{active_id}")
        
        new_list = ed_assum["Note"].dropna().tolist()
        if new_list != current_assums:
            st.session_state.projects[active_id]["data"]["assumptions"] = new_list
            st.rerun()

    # 3. --- PREPARE VARIABLES FOR RENDERING ---
    rev_label = f"R({rev_input})"
    h_upd = upd_input
    h_cre = cre_input
    dynamic_assumptions = st.session_state.projects[active_id]["data"].get("assumptions", [])

    # 4. --- DATA CALCULATION LOOP ---
    # (We need to run this first to create table_rows_html)
    def get_project_totals(proj_dict):
        d = proj_dict.get("data", {})
        pt_data = PROJECT_DATABASE.get(proj_dict["type"], PROJECT_DATABASE["Hotel"])
        def v(key, default=0.0): return d.get(key, pt_data.get(key, default))
        
        gba = v("m_gba"); gfa = v("m_gfa"); sgfa = v("m_sgfa"); rooms = v("m_rooms"); facade = v("m_facade")
        f_mult = 1.32
        
        hc = ((gba * v("u_earth")) + (gba * v("u_found")) + (gba * v("u_struc")) + (gfa * v("u_arch")) + 
              (facade * (v("r_fac_pre")/100) * v("u_f_pre")) + (facade * (v("r_fac_win")/100) * v("u_f_win")) +
              (facade * (v("r_fac_doub")/100) * v("u_f_doub")) + (v("m_door_w") * v("u_d_wood")) + 
              (v("m_door_g") * v("u_d_glass")) + (v("m_door_s") * v("u_d_steel")) + (v("m_lobby") * v("u_lobby")) + 
              (v("m_gondola") * v("u_gondola")) + (rooms * v("r_san_qty") * v("u_s_room")) + 
              (v("m_toil_m") * v("u_s_pub_m")) + (v("m_toil_f") * v("u_s_pub_f")) + 
              (v("m_toil_d") * v("u_s_dis")) + (v("m_mushola") * v("u_s_mushola")) + (rooms * v("u_kit")) + 
              (v("m_door_w") * v("u_hw_wood")) + (v("m_door_s") * v("u_hw_steel")) + 
              (gfa * (v("r_fl_ht")/100) * v("u_fl_ht") * f_mult) + (gfa * (v("r_fl_vin")/100) * v("u_fl_vin") * f_mult) +
              (gfa * (v("r_fl_mar")/100) * v("u_fl_mar") * f_mult) + (v("m_carpet") * v("u_carpet")) + 
              (v("m_glass") * v("u_glass")) + (rooms * v("u_ffe")) + v("u_misc") + (gba * v("u_mep")) + 
              (gba * v("u_util")) + (rooms * v("r_rail_qty") * v("u_rail")) + (v("m_skylight") * v("u_sky")) +
              (v("m_land_m2") * v("u_ext")) + (v("m_fac_pub") * v("u_fac_p")) + (v("m_fac_res") * v("u_fac_r")) + 
              (v("m_fac_proj") * v("u_fac_pr")))
        
        custom_costs = d.get("smart_custom_costs", [])
        dep_map = {"None (Flat Rate)": 1.0, "GBA": gba, "GFA": gfa, "SGFA": sgfa, "Land Area": v("m_land"), "Rooms": rooms, "Facade": facade, "Lobby": v("m_lobby")}
        for item in custom_costs:
            hc += float(item.get("Rate (Rp)", 0)) * float(item.get("Multiplier (Qty)", 1)) * dep_map.get(item.get("Linked Dependency"), 1.0)
        
        hc_total = hc + (hc * 0.05) + (hc * 0.03) 
        sc_total = (gfa * v("sc_cons")) + (v("sc_qs_m") * v("sc_qs_r")) + (v("sc_pm_m") * v("sc_pm_r")) + (hc * (v("sc_ins")/100))
        return {"gba": gba, "gfa": gfa, "sgfa": sgfa, "units": rooms, "budget": hc_total + sc_total}

    table_rows_html = ""
    total_gba = total_gfa = total_sgfa = total_budget = 0
    project_results = []
    for idx, (p_id, p_data) in enumerate(st.session_state.projects.items(), 1):
        m = get_project_totals(p_data)
        r_gba = m["budget"] / m["gba"] if m["gba"] > 0 else 0
        r_gfa = m["budget"] / m["gfa"] if m["gfa"] > 0 else 0
        r_sgfa = m["budget"] / m["sgfa"] if m["sgfa"] > 0 else 0
        total_gba += m["gba"]; total_gfa += m["gfa"]; total_sgfa += m["sgfa"]; total_budget += m["budget"]
        project_results.append({"idx": idx, "name": p_data['name'].upper(), "gba": m["gba"], "gfa": m["gfa"], "sgfa": m["sgfa"], "units": m["units"], "budget": m["budget"], "r_gba": r_gba, "r_gfa": r_gfa, "r_sgfa": r_sgfa})
        
        table_rows_html += f"<tr><td style='border: 1px solid black; padding: 5px;'>{idx}</td><td style='border: 1px solid black; padding: 5px; text-align: left;'><b>{p_data['name'].upper()}</b></td><td style='border: 1px solid black; padding: 5px;'>{m['gba']:,.0f}</td><td style='border: 1px solid black; padding: 5px;'>{m['gfa']:,.0f}</td><td style='border: 1px solid black; padding: 5px;'>{m['sgfa']:,.0f}</td><td style='border: 1px solid black; padding: 5px;'>{m['units']:,.0f}</td><td style='border: 1px solid black; padding: 5px;'>Units</td><td style='border: 1px solid black; padding: 5px; text-align: right;'><b>{m['budget']:,.0f}</b></td><td style='border: 1px solid black; padding: 5px;'>{r_gba:,.0f}</td><td style='border: 1px solid black; padding: 5px;'>{r_gfa:,.0f}</td><td style='border: 1px solid black; padding: 5px;'>{r_sgfa:,.0f}</td></tr>"

    t_r_gba = total_budget / total_gba if total_gba > 0 else 0
    t_r_gfa = total_budget / total_gfa if total_gfa > 0 else 0
    t_r_sgfa = total_budget / total_sgfa if total_sgfa > 0 else 0

    # 5. --- EXCEL BUILDER ENGINE ---
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer, {'in_memory': True})
    worksheet = workbook.add_worksheet('Portfolio Summary')
    
    # Styles
    f_blue_L = workbook.add_format({'bg_color': '#0062a8', 'font_color': 'white', 'bold': True, 'valign': 'vcenter'})
    f_th = workbook.add_format({'bg_color': '#f2f2f2', 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True})
    f_td_c = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
    f_td_L_b = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'border': 1, 'bold': True})
    f_td_R_b = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'border': 1, 'bold': True, 'num_format': '#,##0'})
    f_td_num = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'border': 1, 'num_format': '#,##0'})
    f_tot_L = workbook.add_format({'bg_color': '#e0e0e0', 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
    f_tot_num = workbook.add_format({'bg_color': '#e0e0e0', 'bold': True, 'align': 'right', 'valign': 'vcenter', 'border': 1, 'num_format': '#,##0'})
    f_tot_empty = workbook.add_format({'bg_color': '#e0e0e0', 'border': 1})
    f_assum_h = workbook.add_format({'bg_color': '#ffdf70', 'bold': True, 'border': 1, 'valign': 'vcenter'})
    f_assum_c = workbook.add_format({'align': 'center', 'border': 1})
    f_assum_L = workbook.add_format({'align': 'left', 'border': 1})

    worksheet.set_column('A:A', 5); worksheet.set_column('B:B', 38); worksheet.set_column('C:E', 15); worksheet.set_column('F:F', 10); worksheet.set_column('G:G', 8); worksheet.set_column('H:H', 22); worksheet.set_column('I:K', 15)

    for row in range(5): worksheet.merge_range(row, 0, row, 10, "", f_blue_L)
    worksheet.write_string(0, 0, f"ASG GROUP PROPERTY DEVELOPMENT | VERSION : {rev_label}", f_blue_L)
    worksheet.write_string(1, 0, "QS & PROCUREMENT DIVISION", f_blue_L)
    worksheet.write_string(2, 0, "PROJECT PORTFOLIO | ALL ACTIVE PROJECTS", f_blue_L)
    worksheet.write_string(3, 0, f"REF. DATA {rev_label} | CONCEPT PDF COMPARISON STUDY BY DPA | UPDATED : {h_upd}", f_blue_L)
    worksheet.write_string(4, 0, f"BUDGET ESTIMATE {rev_label} | CREATED : {h_cre}", f_blue_L)

    worksheet.merge_range("A7:A8", "SN", f_th); worksheet.merge_range("B7:B8", "AREA", f_th); worksheet.merge_range("C7:E7", "BUILDING AREA (M2)", f_th)
    worksheet.write_string("C8", "GBA", f_th); worksheet.write_string("D8", "GFA", f_th); worksheet.write_string("E8", "SGFA", f_th)
    worksheet.merge_range("F7:G8", "UNIT", f_th); worksheet.merge_range("H7:H8", "BUDGET ESTIMATE\nRP", f_th)
    worksheet.merge_range("I7:K7", "COST RATIO RP/M2", f_th)
    worksheet.write_string("I8", "GBA", f_th); worksheet.write_string("J8", "GFA", f_th); worksheet.write_string("K8", "SGFA", f_th)

    row_idx = 8
    for p in project_results:
        worksheet.write_number(row_idx, 0, p['idx'], f_td_c); worksheet.write_string(row_idx, 1, p['name'], f_td_L_b)
        worksheet.write_number(row_idx, 2, p['gba'], f_td_num); worksheet.write_number(row_idx, 3, p['gfa'], f_td_num); worksheet.write_number(row_idx, 4, p['sgfa'], f_td_num)
        worksheet.write_number(row_idx, 5, p['units'], f_td_c); worksheet.write_string(row_idx, 6, "Units", f_td_c); worksheet.write_number(row_idx, 7, p['budget'], f_td_R_b)
        worksheet.write_number(row_idx, 8, p['r_gba'], f_td_num); worksheet.write_number(row_idx, 9, p['r_gfa'], f_td_num); worksheet.write_number(row_idx, 10, p['r_sgfa'], f_td_num)
        row_idx += 1

    worksheet.merge_range(row_idx, 0, row_idx, 1, "TOTAL", f_tot_L)
    worksheet.write_number(row_idx, 2, total_gba, f_tot_num); worksheet.write_number(row_idx, 3, total_gfa, f_tot_num); worksheet.write_number(row_idx, 4, total_sgfa, f_tot_num)
    worksheet.write_string(row_idx, 5, "", f_tot_empty); worksheet.write_string(row_idx, 6, "", f_tot_empty); worksheet.write_number(row_idx, 7, total_budget, f_tot_num)
    worksheet.write_number(row_idx, 8, t_r_gba, f_tot_num); worksheet.write_number(row_idx, 9, t_r_gfa, f_tot_num); worksheet.write_number(row_idx, 10, t_r_sgfa, f_tot_num)

    row_idx += 2
    worksheet.write_string(row_idx, 0, "I.", f_assum_h); worksheet.merge_range(row_idx, 1, row_idx, 10, "ASSUMPTIONS", f_assum_h)
    for i, assum in enumerate(dynamic_assumptions, 1):
        row_idx += 1
        worksheet.write_number(row_idx, 0, i, f_assum_c)
        text = str(assum)
        date_match = re.search(r"(\d{2}[./-]\d{2}[./-]\d{4})", text)
        if date_match:
            worksheet.merge_range(row_idx, 1, row_idx, 10, "", f_assum_L)
            parts = text.split(date_match.group(1))
            rich_args = []
            if parts[0]: rich_args.append(parts[0])
            rich_args.extend([workbook.add_format({'font_color': 'red'}), date_match.group(1)])
            if len(parts) > 1 and parts[1]: rich_args.append(parts[1])
            worksheet.write_rich_string(row_idx, 1, *rich_args, f_assum_L)
        else:
            worksheet.merge_range(row_idx, 1, row_idx, 10, text, f_assum_L)
    workbook.close()

    # 6. --- DOWNLOAD BUTTON ---
    st.download_button(label="📊 Download Portfolio as Excel", data=buffer.getvalue(), file_name=f"ASG_Portfolio_{active_id}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

    # 7. --- RENDER HTML TABLE ---
    assum_html_rows = ""
    for i, assum in enumerate(dynamic_assumptions, 1):
        display_text = re.sub(r"(\d{2}[./-]\d{2}[./-]\d{4})", r"<span style='color:red;'>\1</span>", str(assum))
        assum_html_rows += f"<tr><td style='text-align: center; border-right: 1px solid #e0e0e0; padding: 2px;'>{i}</td><td style='padding: 2px 5px;'>{display_text}</td></tr>"

    html_string = f"""
    <div style="font-family: Calibri, sans-serif; font-size: 13px; color: black; background-color: white; padding: 20px; border-radius: 5px;">
        <div style="background-color: #0062a8; color: white; padding: 12px; font-weight: bold; line-height: 1.6; font-size: 14px; text-align: left;">
            <div>ASG GROUP PROPERTY DEVELOPMENT <span style="margin-left: 20px;">VERSION : {rev_label}</span></div>
            <div>QS & PROCUREMENT DIVISION</div>
            <div>PROJECT PORTFOLIO | ALL ACTIVE PROJECTS</div>
            <div>REF. DATA {rev_label} | CONCEPT PDF COMPARISON STUDY BY DPA <span style="margin-left: 20px;">UPDATED : {h_upd}</span></div>
            <div>BUDGET ESTIMATE {rev_label} <span style="margin-left: 20px;">CREATED : {h_cre}</span></div>
        </div>
        <br>
        <table style="width: 100%; border-collapse: collapse; border: 2px solid black; text-align: center;">
            <tr style="background-color: #f2f2f2; font-weight: bold;"><td rowspan="2" style="border: 1px solid black; padding: 5px;">SN</td><td rowspan="2" style="border: 1px solid black; padding: 5px;">AREA</td><td colspan="3" style="border: 1px solid black; padding: 5px;">BUILDING AREA (M2)</td><td colspan="2" rowspan="2" style="border: 1px solid black; padding: 5px;">UNIT</td><td rowspan="2" style="border: 1px solid black; padding: 5px;">BUDGET ESTIMATE<br>RP</td><td colspan="3" style="border: 1px solid black; padding: 5px;">COST RATIO RP/M2</td></tr>
            <tr style="background-color: #f2f2f2; font-weight: bold;"><td style="border: 1px solid black; padding: 5px;">GBA</td><td style="border: 1px solid black; padding: 5px;">GFA</td><td style="border: 1px solid black; padding: 5px;">SGFA</td><td style="border: 1px solid black; padding: 5px;">GBA</td><td style="border: 1px solid black; padding: 5px;">GFA</td><td style="border: 1px solid black; padding: 5px;">SGFA</td></tr>
            {table_rows_html}
            <tr style="background-color: #e0e0e0; font-weight: bold;"><td colspan="2" style="border: 1px solid black; padding: 5px;">TOTAL</td><td style="border: 1px solid black; padding: 5px;">{total_gba:,.0f}</td><td style="border: 1px solid black; padding: 5px;">{total_gfa:,.0f}</td><td style="border: 1px solid black; padding: 5px;">{total_sgfa:,.0f}</td><td colspan="2" style="border: 1px solid black; padding: 5px;"></td><td style="border: 1px solid black; padding: 5px; text-align: right;">{total_budget:,.0f}</td><td style="border: 1px solid black; padding: 5px;">{t_r_gba:,.0f}</td><td style="border: 1px solid black; padding: 5px;">{t_r_gfa:,.0f}</td><td style="border: 1px solid black; padding: 5px;">{t_r_sgfa:,.0f}</td></tr>
        </table>
        <br>
        <table style="width: 100%; border-collapse: collapse; border: 1px solid #dcdcdc; text-align: left;"><tr style="background-color: #ffdf70; font-weight: bold;"><td style="border: 1px solid white; padding: 3px 5px; width: 30px; text-align: center;">I.</td><td style="border: 1px solid white; padding: 3px 5px;">ASSUMPTIONS</td></tr>{assum_html_rows}</table>
    </div>
    """
    st.markdown(html_string.replace('\n', ''), unsafe_allow_html=True)

# --- 4. MAIN NAVIGATION & SIDEBAR PROJECT LIST ---
st.sidebar.title("Main Navigation")

page_choice = st.sidebar.radio(
    "Select Workspace:", 
    ["Cost Calculator", "Area Calculator", "Portfolio Summary"] 
)

st.sidebar.markdown("---")
st.sidebar.subheader("Daftar Proyek Aktif")

# Use the callback to add projects instantly
st.sidebar.button("Tambah Proyek", on_click=cb_add_project, use_container_width=True)

proj_ids = list(st.session_state.projects.keys())
proj_labels = [f"{st.session_state.projects[pid]['name']} ({st.session_state.projects[pid]['type']})" for pid in proj_ids]
current_index = proj_ids.index(st.session_state.current_proj_id) if st.session_state.current_proj_id in proj_ids else 0

st.sidebar.radio(
    "Active Project:",
    options=proj_labels,
    index=current_index,
    key="project_selector",
    on_change=cb_switch_project,
    label_visibility="collapsed"
)

col_del = st.sidebar.columns(1)[0]
with col_del:
    can_delete = len(st.session_state.projects) > 1
    st.button("Hapus", disabled=not can_delete, on_click=cb_delete_project, help="Delete Active Project", use_container_width=True)

st.sidebar.markdown("---")

# --- 5. EXECUTION LOGIC ---
if page_choice == "Portfolio Summary":     # <-- Added Routing
    show_portfolio_summary()
elif page_choice == "Area Calculator":
    show_area_calculator()
else:
    show_cost_estimator()
