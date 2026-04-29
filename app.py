import streamlit as st
import pandas as pd
import altair as alt
from num2words import num2words
from streamlit_local_storage import LocalStorage

# Initialize the storage object immediately
local_storage = LocalStorage()

def n2w(amount):
    try:
        amount = float(amount)
        if amount >= 1_000_000_000_000: # Trillion
            return f"{amount / 1_000_000_000_000:,.2f} Triliun"
        elif amount >= 1_000_000_000: # Billion (Miliar)
            return f"{amount / 1_000_000_000:,.2f} Miliar"
        elif amount >= 1_000_000: # Million (Juta)
            return f"{amount / 1_000_000:,.2f} Juta"
        else:
            return f"{amount:,.0f}"
    except:
        return "0"

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Project Portfolio", layout="wide")

PROJECT_DATABASE = {
    "Apartment": {
        #Foundation & Structure
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        #Architecture
        "arch_base": 1058000.0, "lobby": 1500000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 1250000.0, "facade_double_rate": 2500000.0,
        #Pintu & Hardware
        "door_wood": 3500000.0, "door_steel": 7000000.0,
        "hw_wood": 750000.0, "hw_steel": 1850000.0, "door_glass": 1000000.0, 
        #Sanitari
        "san_room_rate": 26875000.0, "san_pub_f": 98075000.0, "san_pub_m": 77050000.0,
        "san_dis": 30275000.0, "san_mushola": 36500000.0,
        #Lantai, Finishing & Interior
        "fl_ht_rate": {"Type1": 150000.0, "Type2": 350000.0},
        "fl_vinyl_rate": {"Type1": 500000.0, "Type2": 750000.0},
        "fl_marmer_rate": {"Type1": 750000.0, "Type2": 1500000.0},

        "gondola": 600000000.0, "carpet": 1200000.0, "glass": 700000.0,
        
        "ffe": 32000000.0, "misc": 32000000.0, "kitchen": 0.0,

        "facade_precast_pct": 10.0, "facade_window_pct": 80.0, "facade_double_pct": 10.0,
        "fl_ht_pct": 90.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 10.0,
        "san_room_qty": 1.0, "railing_qty": 0.0,
        "mep": 4000000.0, "utility": 150000.0,
        "railing_rate": 2200000.0, "skylight_rate": 4500000.0,
         "ext_land": 1563000.0,
        "fac_pub": 31000000.0, "fac_res": 10000000.0, "fac_proj": 2000000000.0,
        "cons": 174000.0
    },
    "Hotel": {
        "arch_base": 1079000.0, "door_wood": 4750000.0, "door_steel": 8000000.0,
        "hw_wood": 8250000.0, "hw_steel": 2850000.0, "lobby": 2000000.0,
        "gondola": 2000000000.0, "carpet": 1200000.0, "glass": 800000.0,
        "san_room_rate": 62050000.0, "san_pub_f": 107825000.0, "san_pub_m": 86050000.0,
        "ffe": 59650000.0, "misc": 52500000.0, "kitchen": 0.0,
        "fl_ht_rate": {"Type1": 150000.0, "Type2": 350000.0},
        "fl_vinyl_rate": {"Type1": 500000.0, "Type2": 750000.0},
        "fl_marmer_rate": {"Type1": 750000.0, "Type2": 1500000.0},
        "facade_precast_pct": 60.0, "facade_window_pct": 30.0, "facade_double_pct": 10.0,
        "fl_ht_pct": 90.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 10.0,
        "san_room_qty": 3.0, "railing_qty": 5.0,
        "mep": 2810941.24, "utility": 92098.0,
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 1250000.0, "facade_double_rate": 2500000.0,
        "door_glass": 1000000.0, "railing_rate": 2200000.0, "skylight_rate": 4500000.0,
        "san_dis": 30275000.0, "san_mushola": 36500000.0, "ext_land": 1563000.0,
        "fac_pub": 31000000.0, "fac_res": 10000000.0, "fac_proj": 2000000000.0,
        "cons": 199000.0
    },
        "Hotel Bintang 3": {
        "arch_base": 1079000.0, "door_wood": 4750000.0, "door_steel": 8000000.0,
        "hw_wood": 8250000.0, "hw_steel": 2850000.0, "lobby": 2000000.0,
        "gondola": 2000000000.0, "carpet": 1200000.0, "glass": 800000.0,
        "san_room_rate": 62050000.0, "san_pub_f": 107825000.0, "san_pub_m": 86050000.0,
        "ffe": 59650000.0, "misc": 52500000.0, "kitchen": 0.0,
        "fl_ht_rate": {"Type1": 150000.0, "Type2": 350000.0},
        "fl_vinyl_rate": {"Type1": 500000.0, "Type2": 750000.0},
        "fl_marmer_rate": {"Type1": 750000.0, "Type2": 1500000.0},
        "facade_precast_pct": 60.0, "facade_window_pct": 30.0, "facade_double_pct": 10.0,
        "fl_ht_pct": 90.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 10.0,
        "san_room_qty": 3.0, "railing_qty": 5.0,
        "mep": 2810941.24, "utility": 92098.0,

        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,

        "facade_precast_rate": 800000.0, "facade_window_rate": 1250000.0, "facade_double_rate": 2500000.0,
        "door_glass": 1000000.0, "railing_rate": 2200000.0, "skylight_rate": 4500000.0,
        "san_dis": 30275000.0, "san_mushola": 36500000.0, "ext_land": 1563000.0,
        "fac_pub": 31000000.0, "fac_res": 10000000.0, "fac_proj": 2000000000.0,
        "cons": 199000.0
    },
    "Retail": {
        "arch_base": 1084000.0, "door_wood": 6000000.0, "door_steel": 8000000.0,
        "hw_wood": 6500000.0, "hw_steel": 2850000.0, "lobby": 2500000.0,
        "gondola": 2500000000.0, "carpet": 1500000.0, "glass": 800000.0,
        "san_room_rate": 0.0, "san_pub_f": 154175000.0, "san_pub_m": 126225000.0,
        "ffe": 0.0, "misc": 0.0, "kitchen": 0.0,
        "fl_ht_rate": {"Type1": 150000.0, "Type2": 350000.0},
        "fl_vinyl_rate": {"Type1": 500000.0, "Type2": 750000.0},
        "fl_marmer_rate": {"Type1": 750000.0, "Type2": 1500000.0},
        "facade_precast_pct": 10.0, "facade_window_pct": 80.0, "facade_double_pct": 10.0,
        "fl_ht_pct": 90.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 10.0,
        "san_room_qty": 0.0, "railing_qty": 0.0,
        "mep": 4000000.0, "utility": 150000.0,
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 1250000.0, "facade_double_rate": 2500000.0,
        "door_glass": 1000000.0, "railing_rate": 2200000.0, "skylight_rate": 4500000.0,
        "san_dis": 30275000.0, "san_mushola": 36500000.0, "ext_land": 1563000.0,
        "fac_pub": 31000000.0, "fac_res": 10000000.0, "fac_proj": 2000000000.0,
        "cons": 174000.0
    },
    "Parking": {
        "arch_base": 668000.0,
        "mep": 4000000.0,
        "utility": 150000.0,
        "door_wood": 0.0, "door_steel": 0.0, "door_glass": 0.0,
        "hw_wood": 0.0, "hw_steel": 0.0, "lobby": 0.0, "gondola": 0.0,
        "carpet": 0.0, "glass": 0.0, "ffe": 0.0, "misc": 0.0, "kitchen": 0.0,
        "san_room_rate": 0.0, "san_pub_f": 0.0, "san_pub_m": 0.0,
        "fl_ht_rate": {"Type1": 0.0, "Type2": 0.0},
        "fl_vinyl_rate": {"Type1": 0.0, "Type2": 0.0},
        "fl_marmer_rate": {"Type1": 0.0, "Type2": 0.0},
        "facade_precast_pct": 10.0, "facade_window_pct": 80.0, "facade_double_pct": 10.0,
        "fl_ht_pct": 90.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 10.0,
        "san_room_qty": 0.0, "railing_qty": 0.0,
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 1250000.0, "facade_double_rate": 2500000.0,
        "railing_rate": 2200000.0, "skylight_rate": 4500000.0,
        "san_dis": 30275000.0, "san_mushola": 36500000.0, "ext_land": 1563000.0,
        "fac_pub": 31000000.0, "fac_res": 10000000.0, "fac_proj": 2000000000.0,
        "cons": 53000.0
    }
}

#region# 2. Callback Functions
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
#endregion#

#region# 3. SESSION STATE
if "projects" not in st.session_state:
    # Look for a backup in the browser's "Cookie" (LocalStorage)
    stored_data = local_storage.getItem("asg_calculator_backup")
    
    if stored_data:
        # CAVEAT 3 FIX: Check if it's our new "Wrapped" payload
        if "projects_dict" in stored_data:
            st.session_state.projects = stored_data["projects_dict"]
            st.session_state.current_proj_id = stored_data.get("current_proj_id", list(st.session_state.projects.keys())[0])
            st.session_state.proj_counter = stored_data.get("proj_counter", 1)
        else:
            # Backward compatibility for the old cookie format
            st.session_state.projects = stored_data
            st.session_state.current_proj_id = list(stored_data.keys())[0]
            
            # BUG 1 FIX: Safely derive max ID to prevent collision after deletes
            existing_ids = []
            for k in stored_data.keys():
                if k.startswith("proj_"):
                    parts = k.split("_")
                    if len(parts) > 1 and parts[1].isdigit():
                        existing_ids.append(int(parts[1]))
            st.session_state.proj_counter = max(existing_ids) if existing_ids else 1
            
        # BUG 2 FIX: Flag that storage has successfully loaded
        st.session_state.storage_loaded = True

    elif stored_data == {} or stored_data is None:
        # If no cookie exists, create a blank project
        st.session_state.projects = {
            "proj_1": {"name": "New Project 1", "type": "Hotel", "data": {}}
        }
        st.session_state.current_proj_id = "proj_1"
        st.session_state.proj_counter = 1
        st.session_state.storage_loaded = True
#endregion#

# --- 4. PAGE FUNCTIONS ---

def show_area_calculator():
    st.title("Area Calculator")
    st.markdown("---")

    st.sidebar.subheader("Plot & Block")
    num_plots = st.sidebar.number_input("Number of Plots", min_value=1, value=1)

    blocks_per_plot = {}
    for p in range(int(num_plots)):
        blocks_per_plot[p] = st.sidebar.number_input(f"Block Groups in Plot {p+1}", min_value=1, value=2, key=f"ng_setup_{p}")

    st.sidebar.markdown("---")
    st.sidebar.header("Area Grand Totals")
    gba_placeholder = st.sidebar.empty()
    gfa_placeholder = st.sidebar.empty()
    sgfa_placeholder = st.sidebar.empty()
    units_placeholder = st.sidebar.empty()

    grand_total_gba = 0
    grand_total_gfa = 0
    grand_total_sgfa = 0
    grand_total_units = 0

    if int(num_plots) > 0:
        plot_tabs = st.tabs([f"Plot {i+1}" for i in range(int(num_plots))])

        for p_idx, p_tab in enumerate(plot_tabs):
            with p_tab:
                plot_gfa = 0
                plot_sgfa = 0
                plot_units = 0

                num_groups = blocks_per_plot[p_idx]

                if int(num_groups) > 0:
                    block_tabs = st.tabs([f"Block Group {g+1}" for g in range(int(num_groups))])

                    for g_idx, b_tab in enumerate(block_tabs):
                        with b_tab:
                            c1, c2, c3 = st.columns(3)
                            group_name = c1.text_input("Group Name", value=f"Block Group {g_idx+1}", key=f"gn_{p_idx}_{g_idx}")
                            num_blocks = c2.number_input("Number of Blocks", min_value=1, value=6, key=f"nb_{p_idx}_{g_idx}")
                            num_floors = c3.number_input("Typical Floors", min_value=1, value=11, key=f"nf_{p_idx}_{g_idx}")

                            col_com1, col_com2 = st.columns(2)
                            core_area = col_com1.number_input("Core Area per Floor (Lifts/Stairs)", value=105.5, key=f"core_{p_idx}_{g_idx}")
                            corridor_area = col_com2.number_input("Corridor Area per Floor", value=88.8, key=f"corr_{p_idx}_{g_idx}")

                            st.markdown("**Typical Floor Unit Mix (Input)**")
                            default_mix = pd.DataFrame([
                                {"Unit Type": "2BR-1", "Net Area": 74.5, "Units/Floor": 2},
                                {"Unit Type": "3BR", "Net Area": 95.5, "Units/Floor": 1},
                                {"Unit Type": "3BR'", "Net Area": 96.1, "Units/Floor": 4},
                            ])
                            edited_mix = st.data_editor(default_mix, key=f"ed_{p_idx}_{g_idx}", num_rows="dynamic", use_container_width=True)

                            edited_mix["Net/Fl (Total)"] = edited_mix["Net Area"] * edited_mix["Units/Floor"]
                            total_net_per_floor = edited_mix["Net/Fl (Total)"].sum()
                            total_units_per_floor = edited_mix["Units/Floor"].sum()

                            sgfa_load_factor = (total_net_per_floor + corridor_area) / total_net_per_floor if total_net_per_floor > 0 else 1.0
                            gfa_load_factor = (total_net_per_floor + corridor_area + core_area) / total_net_per_floor if total_net_per_floor > 0 else 1.0

                            edited_mix["SGFA per Unit"] = (edited_mix["Net Area"] * sgfa_load_factor).round(2)
                            edited_mix["SGFA/Fl (Total)"] = (edited_mix["SGFA per Unit"] * edited_mix["Units/Floor"]).round(2)
                            edited_mix["GFA per Unit"] = (edited_mix["Net Area"] * gfa_load_factor).round(2)
                            edited_mix["GFA/Fl (Total)"] = (edited_mix["GFA per Unit"] * edited_mix["Units/Floor"]).round(2)

                            display_cols = ["Unit Type", "Net/Fl (Total)", "SGFA per Unit", "SGFA/Fl (Total)", "GFA per Unit", "GFA/Fl (Total)", "Units/Floor"]
                            display_df = edited_mix[display_cols].copy()
                            display_df.rename(columns={"Units/Floor": "Units"}, inplace=True)

                            sum_sgfa_fl = display_df["SGFA/Fl (Total)"].sum()
                            sum_gfa_fl = display_df["GFA/Fl (Total)"].sum()

                            group_net = total_net_per_floor * num_blocks * num_floors
                            group_sgfa = sum_sgfa_fl * num_blocks * num_floors
                            group_gfa = sum_gfa_fl * num_blocks * num_floors
                            group_units = total_units_per_floor * num_blocks * num_floors

                            summary_df = pd.DataFrame({
                                "Per Floor Metric": ["Net Area", "SGFA", "GFA", "Units"],
                                "Floor Total": [f"{total_net_per_floor:,.2f}", f"{sum_sgfa_fl:,.2f}", f"{sum_gfa_fl:,.2f}", f"{int(total_units_per_floor)}"],
                                f"{group_name} ({num_blocks} Blk x {num_floors} Fl)": ["Total Net Area", "Total SGFA", "Total GFA", "Total Units"],
                                "Group Total": [f"{group_net:,.2f}", f"{group_sgfa:,.2f}", f"{group_gfa:,.2f}", f"{int(group_units)}"]
                            })

                            with st.expander(f"View Detailed Calculation Tables for {group_name}", expanded=False):
                                st.markdown("**Calculated Unit Breakdown**")
                                st.dataframe(display_df, use_container_width=True, hide_index=True)
                                st.markdown("**Area Totals Summary**")
                                st.dataframe(summary_df, use_container_width=True, hide_index=True)

                            plot_gfa += group_gfa
                            plot_sgfa += group_sgfa
                            plot_units += group_units

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

                plot_gba = plot_gfa + total_nt_area
                plot_gfa = plot_gfa + nt_gfa_area

                st.divider()

                plot_totals_df = pd.DataFrame({
                    "Plot Total GBA (m2)": [f"{plot_gba:,.2f}"],
                    "Plot Total GFA (m2)": [f"{plot_gfa:,.2f}"],
                    "Plot Total SGFA (m2)": [f"{plot_sgfa:,.2f}"],
                    "Plot Total Units": [f"{int(plot_units)}"]
                })

                st.markdown(f"**PLOT {p_idx+1} GRAND TOTALS**")
                st.dataframe(plot_totals_df, use_container_width=True, hide_index=True)

                grand_total_gba += plot_gba
                grand_total_gfa += plot_gfa
                grand_total_sgfa += plot_sgfa
                grand_total_units += plot_units

    gba_placeholder.metric("Grand Total GBA", f"{grand_total_gba:,.2f} m2")
    gfa_placeholder.metric("Grand Total GFA", f"{grand_total_gfa:,.2f} m2")
    sgfa_placeholder.metric("Grand Total SGFA", f"{grand_total_sgfa:,.2f} m2")
    units_placeholder.metric("Grand Total Units", f"{int(grand_total_units)} Units")


def update_price(metric_key, db_key):
    """Update flooring price based on spec radio selection."""
    c_id = st.session_state.current_proj_id
    p_type = st.session_state.projects[c_id]["type"]
    c_type_key = f"{c_id}_{p_type}"
    selected_spec = st.session_state[f"temp_spec_{metric_key}_{c_type_key}"]
    st.session_state.projects[c_id]["data"][f"{metric_key}_spec_type"] = selected_spec
    db_val = PROJECT_DATABASE[p_type][db_key]
    if isinstance(db_val, dict):
        new_val = db_val.get(selected_spec, 0.0)
        st.session_state[f"u_fl_{metric_key}_{c_type_key}"] = float(new_val)


def show_cost_estimator():
    st.title("Cost Calculator")
    st.markdown("---")

    curr_id = st.session_state.current_proj_id
    curr_proj = st.session_state.projects[curr_id]

    if "data" not in curr_proj:
        st.session_state.projects[curr_id]["data"] = {}

    def get_val(key, default=0.0):
        data_dict = st.session_state.projects[curr_id]["data"]
        val = data_dict.get(key, default)
        
        # If the value is a list (for Custom Items), return it immediately
        if isinstance(val, list):
            return val
            
        # For everything else (numbers/strings), try to force to float
        try:
            return float(val)
        except (ValueError, TypeError):
            # If it's not a number (like "Type1"), return it as is
            return val

    # --- PROJECT SETUP ---
    st.subheader("Data Proyek")
    c1, c2, c3, c4, c5 = st.columns(5)

    new_name = c1.text_input("Nama Proyek", value=curr_proj["name"])
    types_list = ["Hotel", "Retail", "Apartment", "Parking", "Hotel Bintang 3"]
    type_index = types_list.index(curr_proj["type"]) if curr_proj["type"] in types_list else 0
    new_type = c2.selectbox("Jenis Proyek", types_list, index=type_index)

    if new_type != curr_proj["type"]:
        st.session_state.projects[curr_id]["type"] = new_type
        st.session_state.projects[curr_id]["data"] = {} # Clear old rates
        st.rerun()

    if new_name != curr_proj["name"]:
        st.session_state.projects[curr_id]["name"] = new_name
        
        st.rerun()

    pt_data = PROJECT_DATABASE[new_type]
    curr_type_key = f"{curr_id}_{new_type}"



    st.markdown("---")

    # --- TABS ---
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Petunjuk",
        "1. Hard Cost",
        "2. Soft Cost",
        "3. Item Tambahan", 
        "4. Hasil",
        "5. Pembuktian",
        "6. Penyimpanan",
    ])

# --- TAB 1: PETUNJUK PEMAKAIAN ---
    with tab1:
        st.header("Daftar Isi")
        
        c1, c2, c3=st.columns(3)
        
        c1.subheader("Hard Cost")
        c1.markdown("""
        * **1.1 Preliminary**
        * **1.2 Earthworks**
        * **1.3 Foundation Works**
        * **1.4 Structural**
        * **1.5 Architectural**
            * *1.5.1 Basic Finish* 
            * *1.5.2 Lobby* 
            * *1.5.3 Facade*
            * *1.5.4 Pintu* 
            * *1.5.5 Sanitary* 
            * *1.5.6 Lantai*
            * *1.5.7 Lain-lain*
        * **1.6 FF&E**
        * **1.7 MEP**
        * **1.8 External**
        * **1.9 Facility & Misc**
        * **1.10 Contingencies**
        """)

        c2.subheader("Soft Cost")
        c2.markdown("""
        * **2.1 Consultancy**
        * **2.2 Insurances**
        * **2.3 Utilities**
        """)
        
        c3.subheader("Other Tab")
        c3.markdown("""
        * **3. Item Tambahan**
        * **4. Hasil**
        * **5. Pembuktian**
        * **6. Unggah & Unduh**
        """)


    with tab2:
        st.subheader("Hard Cost")
        c1, c2, c3, c4, c5 = st.columns(5)
        gba = c2.number_input("GBA (m2)", value=get_val("m_gba", 0.0), step=100.0, key=f"m_gba_{curr_id}")
        gfa = c3.number_input("GFA (m2)", value=get_val("m_gfa", 0.0), step=100.0, key=f"m_gfa_{curr_id}")
        sgfa = c4.number_input("SGFA (m2)", value=get_val("m_sgfa", 0.0), step=100.0, key=f"m_sgfa_{curr_id}")
        rooms = c5.number_input("Ruang (unit)", help="untuk Apartment/Hotel/Proyek Residensial", value=get_val("m_rooms", 0.0), step=1.0, key=f"m_rooms_{curr_id}")
        land_area = c1.number_input("Luas Tanah (m2)", value=get_val("m_land", 0.0), step=100.0, key=f"m_land_{curr_id}")

        # --- 2. THE ENGINE: PRE-CALCULATION (Mencegah UnboundLocalError) ---
        # Definisi variabel t_ satu per satu berdasarkan input/database
        t_earth      = gba * get_val("u_earth", pt_data["struc_earth"])
        t_found      = gba * get_val("u_found", pt_data["struc_found"])
        t_struc      = gba * get_val("u_struc", pt_data["struc_work"])
        t_arch_base  = gfa * get_val("u_arch", pt_data["arch_base"])
        t_lobby      = get_val("m_lobby", 0.0) * get_val("u_lobby", pt_data["lobby"])
        
        # Facade components
        _f_m2        = get_val("m_facade", 0.0)
        t_precast    = _f_m2 * (get_val("r_fac_pre", pt_data["facade_precast_pct"])/100) * get_val("u_f_pre", pt_data["facade_precast_rate"])
        t_window     = _f_m2 * (get_val("r_fac_win", pt_data["facade_window_pct"])/100) * get_val("u_f_win", pt_data["facade_window_rate"])
        t_double     = _f_m2 * (get_val("r_fac_doub", pt_data["facade_double_pct"])/100) * get_val("u_f_doub", pt_data["facade_double_rate"])
        
        # Doors & Sanitary
        t_w_door     = get_val("m_door_w", 0.0) * get_val("u_d_wood", pt_data["door_wood"])
        t_g_door     = get_val("m_door_g", 0.0) * get_val("u_d_glass", pt_data["door_glass"])
        t_s_door     = get_val("m_door_s", 0.0) * get_val("u_d_steel", pt_data["door_steel"])
        t_hw_w       = get_val("m_door_w", 0.0) * get_val("u_hw_wood", pt_data["hw_wood"])
        t_hw_s       = get_val("m_door_s", 0.0) * get_val("u_hw_steel", pt_data["hw_steel"])
        
        t_unit_san   = rooms * get_val("r_san_qty", pt_data["san_room_qty"]) * get_val("u_s_room", pt_data["san_room_rate"])
        t_t_male     = get_val("m_toil_m", 0.0) * get_val("u_s_pub_m", pt_data["san_pub_m"])
        t_t_female   = get_val("m_toil_f", 0.0) * get_val("u_s_pub_f", pt_data["san_pub_f"])
        t_t_dis      = get_val("m_toil_d", 0.0) * get_val("u_s_dis", pt_data["san_dis"])
        t_mushola    = get_val("m_mushola", 0.0) * get_val("u_s_mushola", pt_data["san_mushola"])

        # Finishing (Multiplier 1.32)
        t_ht         = gfa * (get_val("r_fl_ht", pt_data["fl_ht_pct"])/100) * get_val("u_fl_ht", pt_data["fl_ht_rate"]["Type1"]) * 1.32
        t_vinyl      = gfa * (get_val("r_fl_vin", pt_data["fl_vinyl_pct"])/100) * get_val("u_fl_vin", pt_data["fl_vinyl_rate"]["Type1"]) * 1.32
        t_marmer     = gfa * (get_val("r_fl_mar", pt_data["fl_marmer_pct"])/100) * get_val("u_fl_mar", pt_data["fl_marmer_rate"]["Type1"]) * 1.32

        # Misc Arch
        t_carpet     = get_val("m_carpet", 0.0) * get_val("u_carpet", pt_data["carpet"])
        t_glass_work = get_val("m_glass", 0.0) * get_val("u_glass", pt_data["glass"])
        t_railing    = (rooms * get_val("r_rail_qty", pt_data["railing_qty"])) * get_val("u_rail", pt_data["railing_rate"])
        t_skylight   = get_val("m_skylight", 0.0) * get_val("u_sky", pt_data["skylight_rate"])
        t_gondola    = get_val("m_gondola", 0.0) * get_val("u_gondola", pt_data["gondola"])

        # FF&E, MEP, External, Facilities
        t_ffe        = rooms * get_val("u_ffe", pt_data["ffe"])
        t_kitchen    = rooms * get_val("u_kit", pt_data["kitchen"])
        t_misc       = get_val("u_misc", pt_data["misc"]) * st.session_state.projects[curr_id]["data"].get("misc_switch", 0)
        t_mep        = gba * get_val("u_mep", pt_data["mep"])
        t_external   = get_val("m_land_m2", 0.0) * get_val("u_ext", pt_data["ext_land"])
        t_pub_fac    = get_val("m_fac_pub", 0.0) * get_val("u_fac_p", pt_data["fac_pub"])
        t_res_fac    = get_val("m_fac_res", 0.0) * get_val("u_fac_r", pt_data["fac_res"])
        t_proj_fac   = get_val("m_fac_proj", 0.0) * get_val("u_fac_pr", pt_data["fac_proj"])

        # --- GRAND TOTALS ---
        total_arch_display = sum([
            t_arch_base, t_precast, t_window, t_double, t_w_door, t_g_door, t_s_door, 
            t_lobby, t_unit_san, t_t_male, t_t_female, t_t_dis, t_mushola, 
            t_hw_w, t_hw_s, t_ht, t_vinyl, t_marmer, t_carpet, t_glass_work, 
            t_railing, t_skylight, t_gondola
        ])

        hc_subtotal = sum([
            t_earth, t_found, t_struc, total_arch_display, 
            t_ffe, t_kitchen, t_misc, t_mep, t_external, 
            t_pub_fac, t_res_fac, t_proj_fac
        ])

        t_preliminary = hc_subtotal * 0.05
        t_contingency = hc_subtotal * 0.03
        hc_total = hc_subtotal + t_preliminary + t_contingency

        # --- 3. QUICK RECAP DASHBOARD (TAMPIL DI ATAS TABS) ---
        # Dashboard Row 2 & 3 - Condensed using Markdown & Captions
        # This takes up much less vertical space
        col_group_1 = st.columns(10)
        items_1_10 = [
            ("1. Prelim", t_preliminary),
            ("2. Earthwork", t_earth),
            ("3. Found", t_found),
            ("4. Struc", t_struc),
            ("5. Arch", total_arch_display),
            ("6. FF&E", t_ffe + t_kitchen),
            ("7. MEP", t_mep),
            ("8. External", t_external),
            ("9. Facil", t_pub_fac + t_res_fac + t_proj_fac),
            ("10. Cont.", t_contingency)
        ]

# --- ULTRA COMPACT HTML TABLE WITH MERGED TOTAL ROW ---
        header_fill = "#2c3e50"  # Slate Gray
        
        html_table = f"""
        <div style="overflow-x: auto; margin-bottom: 20px;">
            <table style="width:100%; border-collapse: collapse; font-family: sans-serif; font-size: 11px; border: 1px solid #ddd;">
                <tr style="background-color: {header_fill}; color: white;">
                    {"".join([f'<th style="padding: 5px; text-align: center; border: 1px solid #444;">{item[0]}</th>' for item in items_1_10])}
                </tr>
                <tr style="background-color: white;">
                    {"".join([f'<td style="padding: 8px; text-align: center; border: 1px solid #ddd;">{item[1]/1e6:,.1f}jt</td>' for item in items_1_10])}
                </tr>
                <tr style="background-color: #f8f9fa; font-weight: bold; border-top: 2px solid #2c3e50;">
                    <td colspan="9" style="padding: 8px; text-align: right; border: 1px solid #ddd;">TOTAL HARD COST :</td>
                    <td style="padding: 8px; text-align: center; border: 1px solid #ddd; background-color: #fff3cd;">{hc_total/1e6:,.2f}jt</td>
                </tr>
            </table>
        </div>
        """
        
        st.write(html_table, unsafe_allow_html=True)
        st.success(f"Total Hard Cost: Rp {hc_total/1e6:,.0f}jt")

        # --- 4. THE SUB TABS ---
        hc_sub_tabs = st.tabs(["1. Preliminary", "2. Earthworks", 
                               "3. Foundation Works", "4. Structural", 
                               "5. Architectural", "6. FF&E", "7. MEP", 
                               "8. External", "9. Facility & Misc", 
                               "10. Contingencies"
                               ])

        with hc_sub_tabs[1]:
            st.subheader("Earthworks")
            struc_earth = st.number_input("Earthworks (Rp)", value=get_val("u_earth", pt_data["struc_earth"]), key=f"u_earth_{curr_type_key}")
            st.caption(f"""
                        GBA      : {gba:,.0f} m2  
                        Hitungan : Rp {struc_earth:,.0f} x {gba:,.0f} m2  
                        Total    : Rp {struc_earth * gba:,.0f}  
                        Terbilang: {n2w(struc_earth * gba)}""")
        with hc_sub_tabs[2]:
            st.subheader("Foundation")
            struc_found = st.number_input("Foundation Rate (Rp)", value=get_val("u_found", pt_data["struc_found"]), key=f"u_found_{curr_type_key}")
            st.caption(f"""
                        GBA      : {gba:,.0f} m2  
                        Hitungan: Rp {struc_found:,.0f} x GBA: {gba:,.0f} m2  
                        Total: Rp {struc_found * gba:,.0f}  
                        Terbilang: {n2w(struc_found * gba)}""")

        with hc_sub_tabs[3]:
            st.subheader("Structural")
            struc_work = st.number_input("Structural Work Rate (Rp)", value=get_val("u_struc", pt_data["struc_work"]), key=f"u_struc_{curr_type_key}")
            st.caption(f"""
                        GBA      : {gba:,.0f} m2  
                        Hitungan: Rp {struc_work:,.0f} x GBA: {gba:,.0f} m2  
                        Total: Rp {struc_work * gba:,.0f}  
                        Terbilang: {n2w(struc_work * gba)}""")

        with hc_sub_tabs[4]:
            
            t_arch_base  = gfa * get_val("u_arch", pt_data["arch_base"])
            t_lobby      = get_val("m_lobby", 0.0) * get_val("u_lobby", pt_data["lobby"])
            
            _f_m2        = get_val("m_facade", 0.0)
            t_precast    = _f_m2 * (get_val("r_fac_pre", pt_data["facade_precast_pct"])/100) * get_val("u_f_pre", pt_data["facade_precast_rate"])
            t_window     = _f_m2 * (get_val("r_fac_win", pt_data["facade_window_pct"])/100) * get_val("u_f_win", pt_data["facade_window_rate"])
            t_double     = _f_m2 * (get_val("r_fac_doub", pt_data["facade_double_pct"])/100) * get_val("u_f_doub", pt_data["facade_double_rate"])
            
            t_doors_tot  = (get_val("m_door_w", 0.0) * (get_val("u_d_wood", pt_data["door_wood"]) + get_val("u_hw_wood", pt_data["hw_wood"]))) + \
                           (get_val("m_door_s", 0.0) * (get_val("u_d_steel", pt_data["door_steel"]) + get_val("u_hw_steel", pt_data["hw_steel"]))) + \
                           (get_val("m_door_g", 0.0) * get_val("u_d_glass", pt_data["door_glass"]))

            t_san_tot    = (rooms * get_val("r_san_qty", pt_data["san_room_qty"]) * get_val("u_s_room", pt_data["san_room_rate"])) + \
                           (get_val("m_toil_m", 0.0) * get_val("u_s_pub_m", pt_data["san_pub_m"])) + \
                           (get_val("m_toil_f", 0.0) * get_val("u_s_pub_f", pt_data["san_pub_f"])) + \
                           (get_val("m_toil_d", 0.0) * get_val("u_s_dis", pt_data["san_dis"])) + \
                           (get_val("m_mushola", 0.0) * get_val("u_s_mushola", pt_data["san_mushola"]))

            t_floors_tot = gfa * 1.32 * (
                                (get_val("r_fl_ht", pt_data["fl_ht_pct"])/100 * get_val("u_fl_ht", pt_data["fl_ht_rate"]["Type1"])) +
                                (get_val("r_fl_vin", pt_data["fl_vinyl_pct"])/100 * get_val("u_fl_vin", pt_data["fl_vinyl_rate"]["Type1"])) +
                                (get_val("r_fl_mar", pt_data["fl_marmer_pct"])/100 * get_val("u_fl_mar", pt_data["fl_marmer_rate"]["Type1"]))
                           )

            t_misc_tot   = (get_val("m_carpet", 0.0) * get_val("u_carpet", pt_data["carpet"])) + \
                           (get_val("m_glass", 0.0) * get_val("u_glass", pt_data["glass"])) + \
                           (get_val("m_skylight", 0.0) * get_val("u_sky", pt_data["skylight_rate"])) + \
                           (get_val("m_gondola", 0.0) * get_val("u_gondola", pt_data["gondola"])) + \
                           (rooms * get_val("r_rail_qty", pt_data["railing_qty"]) * get_val("u_rail", pt_data["railing_rate"]))

            # Final Architectural Sum
            total_arch_display = sum([t_arch_base, t_lobby, t_precast, t_window, t_double, t_doors_tot, t_san_tot, t_floors_tot, t_misc_tot])

            st.success(f"**Total Architectural Work: Rp {total_arch_display:,.0f}** ( {n2w(total_arch_display)} )")
     
            arch_sub_tabs = st.tabs(["1. Basic Finish", "2. Lobby", "3. Facade", "4. Pintu", "5. Sanitary", "6. Lantai", "7. Lain-lain"])

            with arch_sub_tabs[0]:
                st.subheader("Pekerjaan Arsitektur - Architecture Base")
                arch_base = st.number_input("Architecture Base (Rp)", value=get_val("u_arch", pt_data["arch_base"]), key=f"u_arch_{curr_type_key}")
                st.caption(f"""Hitungan: Rp {arch_base:,.0f} x GFA: {gfa:,.0f} m2  \n  Total Architecture Base: Rp {arch_base * gfa:,.0f}  \n  Terbilang: {n2w(arch_base * gfa)}""")
            with arch_sub_tabs[1]:
                st.subheader("Pekerjaan Arsitektur - Lobby Interior")
                lobby_interior = st.number_input("Lobby Interior (m2)", help="cth. 500 m2 lobby untuk 1 proyek Apartement A", value=float(get_val("m_lobby", 0.0)), step=10.0, key=f"m_lobby_{curr_id}")
                lobby_rate = st.number_input("Lobby Interior Rate (Rp)", value=get_val("u_lobby", pt_data["lobby"]), key=f"u_lobby_{curr_type_key}")
                st.caption(f"""Hitungan: Rp {lobby_rate:,.0f} x Lobby Interior: {lobby_interior:,.0f} m2  \n  Total Lobby Interior: Rp {lobby_rate * lobby_interior:,.0f}  \n  Terbilang: {n2w(lobby_rate * lobby_interior)}""")
            with arch_sub_tabs[2]:
                st.subheader("Pekerjaan Arsitektur - Facade")
                facade = st.number_input("Facade (m2)", value=get_val("m_facade", 0.0), step=100.0, key=f"m_facade_{curr_id}")
                c3, c4, c5 = st.columns(3)

                fac_precast_rate = c3.number_input("Precast Rate (Rp)", value=get_val("u_f_pre", pt_data["facade_precast_rate"]), key=f"u_f_pre_{curr_type_key}")
                fac_window_rate = c4.number_input("Window Wall Rate (Rp)", value=get_val("u_f_win", pt_data["facade_window_rate"]), key=f"u_f_win_{curr_type_key}")
                fac_double_rate = c5.number_input("Double Skin Rate (Rp)", value=get_val("u_f_doub", pt_data["facade_double_rate"]), key=f"u_f_doub_{curr_type_key}")
                
                facade_precast_pct = c3.number_input("Precast (%)", value=get_val("r_fac_pre", pt_data["facade_precast_pct"]), step=5.0, key=f"r_fac_pre_{curr_type_key}")
                facade_window_pct = c4.number_input("Window Wall (%)", value=get_val("r_fac_win", pt_data["facade_window_pct"]), step=5.0, key=f"r_fac_win_{curr_type_key}")
                facade_double_pct = c5.number_input("Double Skin (%)", value=get_val("r_fac_doub", pt_data["facade_double_pct"]), step=5.0, key=f"r_fac_doub_{curr_type_key}")
                t_fac_pct = facade_precast_pct + facade_window_pct + facade_double_pct
                c3.caption(f"""Hitungan: Rp {fac_precast_rate:,.0f} x Facade: {facade:,.0f} m2 x {facade_precast_pct}%  \n  Total Precast: Rp {fac_precast_rate * facade * (facade_precast_pct/100):,.0f}  \n  Terbilang: {n2w(fac_precast_rate * facade * (facade_precast_pct/100))}""")
                c4.caption(f"""Hitungan: Rp {fac_window_rate:,.0f} x Facade: {facade:,.0f} m2 x {facade_window_pct}%  \n  Total Window Wall: Rp {fac_window_rate * facade * (facade_window_pct/100):,.0f}  \n  Terbilang: {n2w(fac_window_rate * facade * (facade_window_pct/100))}""")
                c5.caption(f"""Hitungan: Rp {fac_double_rate:,.0f} x Facade: {facade:,.0f} m2 x {facade_double_pct}%  \n  Total Double Skin: Rp {fac_double_rate * facade * (facade_double_pct/100):,.0f}  \n  Terbilang: {n2w(fac_double_rate * facade * (facade_double_pct/100))}""")
            
            t_fac_pct = facade_precast_pct + facade_window_pct + facade_double_pct
            if t_fac_pct != 100:
                st.warning(f"⚠️ Total is **{t_fac_pct}%** (bukan 100%)")
            
            with arch_sub_tabs[3]:
                st.subheader("Pekerjaan Arsitektur - Pintu")
                c1, c2, c3 = st.columns(3)
                glass_door = c3.number_input("Glass Door (unit)", value=get_val("m_door_g", 0.0), step=1.0, key=f"m_door_g_{curr_id}")
                wooden_door = c1.number_input("Wooden Door (unit)", value=get_val("m_door_w", 0.0), step=10.0, key=f"m_door_w_{curr_id}")
                steel_door = c2.number_input("Steel Door (unit)", value=get_val("m_door_s", 0.0), step=10.0, key=f"m_door_s_{curr_id}")

                door_wood = c1.number_input("Wooden Door Rate (Rp)", value=get_val("u_d_wood", pt_data["door_wood"]), key=f"u_d_wood_{curr_type_key}")
                door_glass = c3.number_input("Glass Door Rate (Rp)", value=get_val("u_d_glass", pt_data["door_glass"]), key=f"u_d_glass_{curr_type_key}")
                door_steel = c2.number_input("Steel Door Rate (Rp)", value=get_val("u_d_steel", pt_data["door_steel"]), key=f"u_d_steel_{curr_type_key}")
                c1.caption(f"""Hitungan: Rp {door_wood:,.0f} x  {wooden_door:,.0f} unit  \n  Total Pintu Kayu: Rp {door_wood * wooden_door:,.0f}  \n  Terbilang: {n2w(door_wood * wooden_door)}""")
                c3.caption(f"""Hitungan: Rp {door_glass:,.0f} x  {glass_door:,.0f} unit  \n  Total Pintu Kaca: Rp {door_glass * glass_door:,.0f}  \n  Terbilang: {n2w(door_glass * glass_door)}""")
                c2.caption(f"""Hitungan: Rp {door_steel:,.0f} x  {steel_door:,.0f} unit  \n  Total Pintu Baja: Rp {door_steel * steel_door:,.0f}  \n  Terbilang: {n2w(door_steel * steel_door)}""")
                hw_wood = c1.number_input("Hardware Wooden Door (Rp)", value=get_val("u_hw_wood", pt_data["hw_wood"]), key=f"u_hw_wood_{curr_type_key}")
                hw_steel = c2.number_input("Hardware Steel Door (Rp)", value=get_val("u_hw_steel", pt_data["hw_steel"]), key=f"u_hw_steel_{curr_type_key}")
                c1.caption(f"""Hitungan: Rp {hw_wood:,.0f} x  {wooden_door:,.0f} unit  \n  Total Hardware Pintu Kayu: Rp {hw_wood * wooden_door:,.0f}  \n  Terbilang: {n2w(hw_wood * wooden_door)}""")
                c2.caption(f"""Hitungan: Rp {hw_steel:,.0f} x  {steel_door:,.0f} unit  \n  Total Hardware Pintu Baja: Rp {hw_steel * steel_door:,.0f}  \n  Terbilang: {n2w(hw_steel * steel_door)}""")

            with arch_sub_tabs[4]:
                st.subheader("Pekerjaan Arsitektur - Sanitary")                
                c1, c2 = st.columns(2)
                with c1:
                    san_qty_room = st.number_input("Toilet Private (unit/ruang)", help="Cth. 3 Toilet/1 Kamar (Apt)", value=get_val("r_san_qty", pt_data["san_room_qty"]), key=f"r_san_qty_{curr_type_key}")
                    san_room_rate = st.number_input("Typical Unit Sanitary Rate (Rp)", value=get_val("u_s_room", pt_data["san_room_rate"]), key=f"u_s_room_{curr_type_key}")
                    st.caption(f"""Hitungan: Rp {san_room_rate:,.0f} x {rooms:,.0f} Rooms x {san_qty_room} Units / Room  \n  Total Private Bathroom: Rp {rooms * san_qty_room * san_room_rate:,.0f}  \n  Terbilang: {n2w(rooms * san_qty_room * san_room_rate)}""")

                    disabled_toil = st.number_input("Toilet Difabel (units)", value=get_val("m_toil_d", 0.0), step=1.0, key=f"m_toil_d_{curr_id}")
                    san_dis = st.number_input("Disabled Toilet Rate (Rp)", value=get_val("u_s_dis", pt_data["san_dis"]), key=f"u_s_dis_{curr_type_key}")
                    st.caption(f"""Hitungan: Rp {san_dis:,.0f} x {disabled_toil:,.0f} Units  \n  Total Toilet Difabel: Rp {disabled_toil * san_dis:,.0f}  \n  Terbilang: {n2w(disabled_toil * san_dis)}""")

                    mushola_unit = st.number_input("Mushola (units)", value=get_val("m_mushola", 0.0), step=1.0, key=f"m_mushola_{curr_id}")
                    san_mushola = st.number_input("Mushola Rate (Rp)", value=get_val("u_s_mushola", pt_data["san_mushola"]), key=f"u_s_mushola_{curr_type_key}")
                    st.caption(f"""Hitungan: Rp {san_mushola:,.0f} x {mushola_unit:,.0f} Units  \n  Total Mushola: Rp {mushola_unit * san_mushola:,.0f}  \n  Terbilang: {n2w(mushola_unit * san_mushola)}""")

                with c2:
                    toilet_male = st.number_input("Toilet Umum - Pria (units)", value=get_val("m_toil_m", 0.0), step=1.0, key=f"m_toil_m_{curr_id}")
                    san_pub_m = st.number_input("Public Toilet Male Rate (Rp)", value=get_val("u_s_pub_m", pt_data["san_pub_m"]), key=f"u_s_pub_m_{curr_type_key}")
                    st.caption(f"""Hitungan: Rp {san_pub_m:,.0f} x {toilet_male:,.0f} Units  \n  Total Public Toilet Male: Rp {toilet_male * san_pub_m:,.0f}  \n  Terbilang: {n2w(toilet_male * san_pub_m)}""")

                    toilet_female = st.number_input("Toilet Umum - Wanita (units)", value=get_val("m_toil_f", 0.0), step=1.0, key=f"m_toil_f_{curr_id}")
                    san_pub_f = st.number_input("Public Toilet Female Rate (Rp)", value=get_val("u_s_pub_f", pt_data["san_pub_f"]), key=f"u_s_pub_f_{curr_type_key}")
                    st.caption(f"""Hitungan: Rp {san_pub_f:,.0f} x {toilet_female:,.0f} Units  \n  Total Public Toilet Female: Rp {toilet_female * san_pub_f:,.0f}  \n  Terbilang: {n2w(toilet_female * san_pub_f)}""")


            with arch_sub_tabs[5]:
                st.subheader("Pekerjaan Arsitektur - Lantai")
                c1, c2, c3 = st.columns(3)
                f_mult = 1.1*1.2

                with c1:
                    # Dynamically set index based on saved data
                    ht_idx = 0 if get_val("ht_spec_type", "Type1") == "Type1" else 1
                    
                    st.radio("Spek HT", ["Type1", "Type2"],
                        index=ht_idx, # <--- Added
                        key=f"temp_spec_ht_{curr_type_key}",
                        horizontal=True,
                        on_change=update_price, args=("ht", "fl_ht_rate"))
                    
                    fl_ht_pct = st.number_input("HT/Ceramic Tile (%)", value=get_val("r_fl_ht", pt_data["fl_ht_pct"]), step=5.0, max_value=100.0, key=f"r_fl_ht_{curr_type_key}")
                    fl_ht_rate = st.number_input("HT Rate (Rp)", value=get_val("u_fl_ht", pt_data["fl_ht_rate"]["Type1"]), key=f"u_fl_ht_{curr_type_key}")
                    st.caption(f"""Hitungan: {fl_ht_pct}% of GFA x Rp {fl_ht_rate:,.0f} x {gfa:,.0f} m2 x 1.1 x 1.2  \n  Total HT: Rp {gfa * (fl_ht_pct / 100) * fl_ht_rate * 1.32:,.0f}  \n  Terbilang: {n2w(gfa * (fl_ht_pct / 100) * fl_ht_rate * 1.32)}""")

                with c2:
                    vin_idx = 0 if get_val("vin_spec_type", "Type1") == "Type1" else 1
                    
                    st.radio("Spek Vinyl", ["Type1", "Type2"],
                        index=vin_idx, # <--- Added
                        key=f"temp_spec_vin_{curr_type_key}",
                        horizontal=True,
                        on_change=update_price, args=("vin", "fl_vinyl_rate"))
                        
                    fl_vinyl_pct = st.number_input("Vinyl (%)", value=get_val("r_fl_vin", pt_data["fl_vinyl_pct"]), step=5.0, max_value=100.0, key=f"r_fl_vin_{curr_type_key}")
                    fl_vinyl_rate = st.number_input("Vinyl Rate (Rp)", value=get_val("u_fl_vin", pt_data["fl_vinyl_rate"]["Type1"]), key=f"u_fl_vin_{curr_type_key}")
                    st.caption(f"""Hitungan: {fl_vinyl_pct}% of GFA x Rp {fl_vinyl_rate:,.0f} x {gfa:,.0f} m2 x 1.1 x 1.2  \n  Total Vinyl: Rp {gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * 1.32:,.0f}  \n  Terbilang: {n2w(gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * 1.32)}""")
                
                with c3:
                    mar_idx = 0 if get_val("mar_spec_type", "Type1") == "Type1" else 1
                    
                    st.radio("Spek Marmer", ["Type1", "Type2"],
                        index=mar_idx, # <--- Added
                        key=f"temp_spec_mar_{curr_type_key}",
                        horizontal=True,
                        on_change=update_price, args=("mar", "fl_marmer_rate"))
                        
                    fl_marmer_pct = st.number_input("Marmer (%)", value=get_val("r_fl_mar", pt_data["fl_marmer_pct"]), step=5.0, max_value=100.0, key=f"r_fl_mar_{curr_type_key}")
                    fl_marmer_rate = st.number_input("Marmer Rate (Rp)", value=get_val("u_fl_mar", pt_data["fl_marmer_rate"]["Type1"]), key=f"u_fl_mar_{curr_type_key}")
                    st.caption(f"""Hitungan: {fl_marmer_pct}% of GFA x Rp {fl_marmer_rate:,.0f} x {gfa:,.0f} m2 x 1.1 x 1.2  \n  Total Marmer: Rp {gfa * (fl_marmer_pct / 100) * fl_marmer_rate * 1.32:,.0f}  \n  Terbilang: {n2w(gfa * (fl_marmer_pct / 100) * fl_marmer_rate * 1.32)}""")
                    
                    t_fl_pct = fl_ht_pct + fl_vinyl_pct + fl_marmer_pct

                if t_fl_pct != 100:
                    st.warning(f"⚠️ Total is **{t_fl_pct}%** (bukan 100%)")

                st.markdown("---")
                
            with arch_sub_tabs[6]:
                st.subheader("Pekerjaan Arsitektur - Lain-lain")
                c1, c2, c3 = st.columns(3)
                carpet_m2 = c1.number_input("Karpet (m2)", value=get_val("m_carpet", 0.0), step=10.0, key=f"m_carpet_{curr_id}")            
                carpet_rate = c1.number_input("Carpet Rate (Rp)", value=get_val("u_carpet", pt_data["carpet"]), key=f"u_carpet_{curr_type_key}")
                c1.caption(f"""Hitungan: {carpet_m2:,.0f} m2 x Rp {carpet_rate:,.0f}  \n  Total Carpet Work: Rp {carpet_m2 * carpet_rate:,.0f}  \n  Terbilang: {n2w(carpet_m2 * carpet_rate)}""")
                
                glass_m2 = c2.number_input("Kaca (m2)", value=get_val("m_glass", 0.0), step=10.0, key=f"m_glass_{curr_id}")
                glass_rate = c2.number_input("Glass Work Rate (Rp)", value=get_val("u_glass", pt_data["glass"]), key=f"u_glass_{curr_type_key}")
                c2.caption(f"""Hitungan: {glass_m2:,.0f} m2 x Rp {glass_rate:,.0f}  \n  Total Glass Work: Rp {glass_m2 * glass_rate:,.0f}  \n  Terbilang: {n2w(glass_m2 * glass_rate)}""")            
                
                skylight_area = c3.number_input("Skylight (m2)", value=get_val("m_skylight", 0.0), step=10.0, key=f"m_skylight_{curr_id}")    
                skylight_rate = c3.number_input("Skylight Rate (Rp)", value=get_val("u_sky", pt_data["skylight_rate"]), key=f"u_sky_{curr_type_key}")
                c3.caption(f"""Hitungan: {skylight_area:,.0f} m2 Total x Rp {skylight_rate:,.0f}  \n  Total Skylight Work: Rp {skylight_area * skylight_rate:,.0f}  \n  Terbilang: {n2w(skylight_area * skylight_rate)}""")
                
                gondola_unit = c1.number_input("Gondola (unit)", value=get_val("m_gondola", 0.0), step=1.0, key=f"m_gondola_{curr_id}")
                gondola_rate = c1.number_input("Gondola Rate (Rp)", value=get_val("u_gondola", pt_data["gondola"]), key=f"u_gondola_{curr_type_key}")
                c1.caption(f"""Hitungan: {gondola_unit:,.0f} Units x Rp {gondola_rate:,.0f}  \n  Total Gondola: Rp {gondola_unit * gondola_rate:,.0f}  \n  Terbilang: {n2w(gondola_unit * gondola_rate)}""")
                
                railing_qty = c2.number_input("Railing Length (m'/room)", value=get_val("r_rail_qty", pt_data["railing_qty"]), step=1.0, key=f"r_rail_qty_{curr_type_key}")
                railing_rate = c2.number_input("Railing Rate (Rp)", value=get_val("u_rail", pt_data["railing_rate"]), key=f"u_rail_{curr_type_key}")
                c2.caption(f"""Hitungan: {railing_qty:,.0f} m' x Rooms {rooms:,.0f} unit x Rp {railing_rate:,.0f}  \n  Total Railing Work: Rp {rooms * railing_qty * railing_rate:,.0f}  \n  Terbilang: {n2w(rooms * railing_qty * railing_rate)}""")
                
        with hc_sub_tabs[5]:
            st.subheader("FF&E")
            c1, c2, c3 = st.columns(3)
            
            with c1.expander("FF&E", expanded=True):
                ffe_rate = st.number_input("FF&E (Rp)", value=get_val("u_ffe", pt_data["ffe"]), key=f"u_ffe_{curr_type_key}")
                st.caption(f"""Hitungan: {rooms:,.0f} Rooms x Rp {ffe_rate:,.0f}  \n  Total FF&E: Rp {rooms * ffe_rate:,.0f}  \n  Terbilang: {n2w(rooms * ffe_rate)}""")

            with c2.expander("Dapur", expanded=True):
                kitchen_rate = st.number_input("Kitchen Equipment (Rp)", value=get_val("u_kit", pt_data["kitchen"]), key=f"u_kit_{curr_type_key}")
                st.caption(f"""Hitungan: Rp {kitchen_rate:,.0f}  \n  Total Kitchen Equipment: Rp {kitchen_rate:,.0f}  \n  Terbilang: {n2w(kitchen_rate)}""")

            with c3.expander("Gym/Linen", expanded=True):    
                m_status = st.radio("Ada Gym/Linen?", ["Tidak", "Ada"],
                                    index=1 if get_val("misc_switch", 0) == 1 else 0,
                                    key=f"misc_sw_{curr_id}", horizontal=True)
                misc_switch = 1 if m_status == "Ada" else 0
                st.session_state.projects[curr_id]["data"]["misc_switch"] = misc_switch

                misc_rate = st.number_input("Misc (Linen/Gym Equipment) (Rp)", value=get_val("u_misc", pt_data["misc"]), key=f"u_misc_{curr_type_key}")
                st.caption(f"""Hitungan: Rp {misc_rate if misc_switch else 0:,.0f}  \n  Total Misc. Costs: Rp {misc_rate * misc_switch:,.0f}  \n  Terbilang: {n2w(misc_rate * misc_switch)}""")
        
        with hc_sub_tabs[6]:
            st.subheader("MEP")
            c1, c2, c3 = st.columns(3)
            
            mep_rate = c1.number_input("MEP Works (Rp)", value=get_val("u_mep", pt_data["mep"]), key=f"u_mep_{curr_type_key}")
            c1.caption(f"""Hitungan: {gba:,.0f} m2 x Rp {mep_rate:,.0f}  \n  Total MEP Works: Rp {gba * mep_rate:,.0f}  \n  Terbilang: {n2w(gba * mep_rate)}""")
        
        with hc_sub_tabs[7]:
            st.subheader("External")
            c1, c2, c3 = st.columns(3)

            land_m2 = c1.number_input("Area Lanskap (m2)", value=get_val("m_land_m2", 0.0), step=100.0, key=f"m_land_m2_{curr_id}")
            ext_land_rate = c1.number_input("External Works (Landscape) (Rp)", value=get_val("u_ext", pt_data["ext_land"]), key=f"u_ext_{curr_type_key}")
            c1.caption(f"""Hitungan: {land_m2:,.0f} m2 x Rp {ext_land_rate:,.0f}  \n  Total External Works: Rp {land_m2 * ext_land_rate:,.0f}  \n  Terbilang: {n2w(land_m2 * ext_land_rate)}""")
        
        with hc_sub_tabs[8]:
            st.subheader("Facilities & Misc")
            c1, c2, c3 = st.columns(3)
            MAX_UNITS=100.0

            res_fac_m2 = c2.number_input("Fasilitas Penghuni (m2)", value=get_val("m_fac_res", 0.0), step=10.0, key=f"m_fac_res_{curr_id}")
            pub_fac_m2 = c1.number_input("Fasilitas Publik (m2)", value=get_val("m_fac_pub", 0.0), step=10.0, key=f"m_fac_pub_{curr_id}")
            proj_fac_u = c3.number_input("Fasilitas Proyek (unit)", value=get_val("m_fac_proj", 0.0), step=1.0, max_value=MAX_UNITS, key=f"m_fac_proj_{curr_id}")

            fac_pub_rate = c1.number_input("Fasilitas Publik (Rp)", value=get_val("u_fac_p", pt_data["fac_pub"]), key=f"u_fac_p_{curr_type_key}")
            fac_res_rate = c2.number_input("Fasilitas Penghuni (Rp)", value=get_val("u_fac_r", pt_data["fac_res"]), key=f"u_fac_r_{curr_type_key}")
            fac_proj_rate = c3.number_input("Fasilitas Proyek (Rp)", value=get_val("u_fac_pr", pt_data["fac_proj"]), key=f"u_fac_pr_{curr_type_key}")
            
            c1.caption(f"""Hitungan: {pub_fac_m2:,.0f} m2 x Rp {fac_pub_rate:,.0f}  \n  Total Public Facilities: Rp {pub_fac_m2 * fac_pub_rate:,.0f}  \n  Terbilang: {n2w(pub_fac_m2 * fac_pub_rate)}""")
            c2.caption(f"""Hitungan: {res_fac_m2:,.0f} m2 x Rp {fac_res_rate:,.0f}  \n  Total Resident Facilities: Rp {res_fac_m2 * fac_res_rate:,.0f}  \n  Terbilang: {n2w(res_fac_m2 * fac_res_rate)}""")
            c3.caption(f"""Hitungan: {proj_fac_u:,.0f} Units x Rp {fac_proj_rate:,.0f}  \n  Total Project Facilities: Rp {proj_fac_u * fac_proj_rate:,.0f}  \n  Terbilang: {n2w(proj_fac_u * fac_proj_rate)}""")

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
        t_vinyl   = gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * f_mult
        t_marmer  = gfa * (fl_marmer_pct / 100) * fl_marmer_rate * f_mult
        t_carpet     = carpet_m2 * carpet_rate
        t_glass_work = glass_m2 * glass_rate
        t_ffe        = rooms * ffe_rate
        t_misc       = misc_rate * misc_switch
        t_mep        = gba * mep_rate
        t_railing    = (rooms * railing_qty) * railing_rate
        t_skylight   = skylight_area * skylight_rate
        t_external = land_m2 * ext_land_rate
        t_pub_fac  = pub_fac_m2 * fac_pub_rate
        t_res_fac  = res_fac_m2 * fac_res_rate
        t_proj_fac = proj_fac_u * fac_proj_rate

        hc_subtotal = sum([
            t_earth, t_found, t_struc, t_arch_base, t_precast, t_window, t_double,
            t_w_door, t_g_door, t_s_door, t_lobby, t_gondola, t_unit_san, t_t_male,
            t_t_female, t_t_dis, t_mushola, t_kitchen, t_hw_w, t_hw_s, t_ht, t_vinyl,
            t_marmer, t_carpet, t_glass_work, t_ffe, t_misc, t_mep, 
            t_railing, t_skylight, t_external, t_pub_fac, t_res_fac, t_proj_fac,
            # total_custom_cost
        ])

        t_preliminary = (hc_subtotal) * 0.05
        t_contingency = (hc_subtotal) * 0.03
        hc_total = hc_subtotal + t_preliminary + t_contingency

        with hc_sub_tabs[0]:
            st.subheader("Preliminary")
            f"5% x Rp {(hc_subtotal):,.0f} = Rp {(0.05 * hc_subtotal):,.0f}",


        with hc_sub_tabs[9]:
            st.subheader("Contingency")
            f"3% x Rp {(hc_subtotal):,.0f} = {(0.03 * hc_subtotal):,.0f}",


    with tab3:
        st.subheader("Soft Cost")
        sc_sub_tabs = st.tabs(["1. Consultancy Services", "2. Insurances", "3. Utilities Connection"])
        with sc_sub_tabs [0]:
            sc_col1, sc_col2, sc_col3 = st.columns(3)
            with sc_col1:
                with st.expander("QS", expanded=True):
                    qs_months = st.number_input("Durasi QS (Bulan)", value=get_val("sc_qs_m", 0.0), step=1.0, key=f"sc_qs_m_{curr_id}")
                    qs_rate = st.number_input("Harga QS (per Bulan) (Rp)", value=get_val("sc_qs_r", 0.0), step=1000000.0, key=f"sc_qs_r_{curr_id}")
                    st.caption(f"""Hitungan: {qs_months} Months x Rp {qs_rate:,.0f}/Mo  \n  Total QS Services: Rp {qs_months * qs_rate:,.0f}  \n  Terbilang: {n2w(qs_months * qs_rate)}""")
            with sc_col2:
                with st.expander("PM", expanded=True):
                    pm_months = st.number_input("Durasi PM (Bulan)", value=get_val("sc_pm_m", 0.0), step=1.0, key=f"sc_pm_m_{curr_id}")
                    pm_rate = st.number_input("Harga PM (per Bulan) (Rp)", value=get_val("sc_pm_r", 0.0), step=1000000.0, key=f"sc_pm_r_{curr_id}")
                    st.caption(f"""Hitungan: {pm_months} Months x Rp {pm_rate:,.0f}/Mo  \n  Total PM Services: Rp {pm_months * pm_rate:,.0f}  \n  Terbilang: {n2w(pm_months * pm_rate)}""")                
            with sc_col3:
                with st.expander("Other Consultancy", expanded=True):
                    consultancy_rate = st.number_input("Biaya Konsultan (Rp) per m2 GFA", help="Biaya konsultan per m2 GFA", value=get_val("sc_cons", pt_data["cons"]), key=f"sc_cons_{curr_type_key}")
                    st.caption(f"""Hitungan: {gfa:,.0f} m2 x Rp {consultancy_rate:,.0f}  \n  Total Consultancy Fee: Rp {gfa * consultancy_rate:,.0f}  \n  Terbilang: {n2w(gfa * consultancy_rate)}""")
        with sc_sub_tabs [1]:
            insurance_pct = st.number_input("Insurance (%)", help="Persentase premi asuransi", value=get_val("sc_ins", 0.12), step=0.01, key=f"sc_ins_{curr_id}")
            st.caption(f"""Hitungan: {gfa:,.0f} m2 x Rp {hc_subtotal:,.0f}  \n  Total: Rp {gfa * hc_subtotal:,.0f}  \n  Terbilang: {n2w(gfa * hc_subtotal)}""")
        with sc_sub_tabs [2]:
            utility_rate = st.number_input("Utility Connection (Rp)", value=get_val("u_util", pt_data["utility"]), key=f"u_util_{curr_type_key}")
            st.caption(f"""Hitungan: {gba:,.0f} m2 x Rp {utility_rate:,.0f}  \n  Total Utility Connection: Rp {gba * utility_rate:,.0f}  \n  Terbilang: {n2w(gba * utility_rate)}""")

        t_consultancy = gfa * consultancy_rate
        t_qs = qs_months * qs_rate
        t_pm = pm_months * pm_rate
        t_insurance = (hc_subtotal) * (insurance_pct / 100.0)
        t_utility    = gba * utility_rate
        
        sc_total = t_consultancy + t_qs + t_pm + t_insurance+t_utility
        
        grand_total_project = hc_total + sc_total

    with tab7:
        st.header("Upload & Download")
        c1, c2 = st.columns(2)
        with c1:
            uploaded_file = st.file_uploader("Upload Here:", type=["csv"])

            if uploaded_file is not None:
                if "last_loaded_file" not in st.session_state or st.session_state.last_loaded_file != uploaded_file.file_id:
                    try:
                        df_import = pd.read_csv(uploaded_file)
                        
                        # 1. Prepare temporary storage
                        new_name = curr_proj["name"]
                        new_type = curr_proj["type"]
                        new_data = {}

                        # 2. Extract the data
                        for index, row in df_import.iterrows():
                            key = str(row.get("Metric_Key", ""))
                            val = row.get("Value", 0)

                            if not key or pd.isna(key): continue

                            if key == "proj_name":
                                new_name = str(val)
                            elif key == "proj_type":
                                new_type = str(val)
                            elif str(val) in ["Type1", "Type2"]:
                                new_data[key] = str(val)
                            else:
                                try:
                                    new_data[key] = float(val)
                                except:
                                    new_data[key] = str(val) if not pd.isna(val) else 0.0

                        # 3. Save to backend
                        st.session_state.projects[curr_id]["name"] = new_name
                        st.session_state.projects[curr_id]["type"] = new_type
                        st.session_state.projects[curr_id]["data"] = new_data

                        # 4. THE PURGE: Delete widget memory so it forces a fresh read
                        suffix_id = f"_{curr_id}"
                        suffix_type = f"_{curr_id}_{new_type}"
                        
                        keys_to_delete = []
                        for k in st.session_state.keys():
                            if k.endswith(suffix_id) or k.endswith(suffix_type):
                                keys_to_delete.append(k)
                                
                        for k in keys_to_delete:
                            del st.session_state[k]

                        st.session_state.last_loaded_file = uploaded_file.file_id
                        st.success("✅ Load Complete! UI Synchronized.")
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Critical Error: {e}")

            # Export Block
            csv_data = []
            csv_data.append({"Metric_Key": "proj_name", "Value": curr_proj["name"]})
            csv_data.append({"Metric_Key": "proj_type", "Value": curr_proj["type"]})
            for k, v in st.session_state.projects[curr_id]["data"].items():
                if k not in ("smart_custom_costs", "header_info", "assumptions"):
                    csv_data.append({"Metric_Key": k, "Value": v})

            df_export = pd.DataFrame(csv_data)
            csv_buffer = df_export.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download",
                data=csv_buffer,
                file_name=f"Database_{curr_id}.csv",
                mime="text/csv",
                use_container_width=True
            )
  
    # --- TAB 5: CUSTOM ITEMS ---
    with tab4:
        st.subheader("Item Tambahan")

        dependency_map = {
            "None (Flat Rate)": 1.0, "GBA": gba, "GFA": gfa, "SGFA": sgfa,
            "Land Area": land_area, "Rooms": rooms, "Facade": facade, "Lobby": lobby_interior, "Toilet Private" : san_qty_room * rooms
        }

        default_smart_cc = [{"Item Description": "", "Rate (Rp)": 0.0, "Multiplier (Qty)": 1.0, "Linked Dependency": "None (Flat Rate)"}]
        current_smart_cc = get_val("smart_custom_costs", default_smart_cc)

        edited_smart_cc = st.data_editor(
            pd.DataFrame(current_smart_cc),
            num_rows="dynamic",
            key=f"edit_smart_cc_{curr_id}",
            column_config={
                "Linked Dependency": st.column_config.SelectboxColumn(
                    "Linked Dependency",
                    options=list(dependency_map.keys()),
                    required=True
                ),
                "Multiplier (Qty)": st.column_config.NumberColumn(
                    "Multiplier (Qty)",
                    min_value=0,
                    default=1.0,
                    format="%.2f"
                )
            },
            use_container_width=True
        )

        total_custom_cost = 0.0
        
        # New: List to store breakdown strings
        breakdown_details = []

        for index, row in edited_smart_cc.iterrows():
            desc = row.get("Item Description", f"Item {index + 1}")
            rate = float(row.get("Rate (Rp)", 0.0))
            mult = float(row.get("Multiplier (Qty)", 1.0))
            dep_name = row.get("Linked Dependency", "None (Flat Rate)")
            dep_value = dependency_map.get(dep_name, 1.0)
            
            # Calculate item total
            item_total = rate * mult * dep_value
            total_custom_cost += item_total

            # Create a descriptive string for each item
            if rate > 0:
                calc_str = f"**{desc}**: Rp {rate:,.2f} × {mult} qty"
                if dep_name != "None (Flat Rate)":
                    calc_str += f" × {dep_value:,.2f} ({dep_name})"
                calc_str += f" = **Rp {item_total:,.2f}**"
                breakdown_details.append(calc_str)

        # Display the breakdown
        if breakdown_details:
            with st.expander("Detail Item Custom", expanded=True):
                for detail in breakdown_details:
                    st.caption(detail) # Or use st.write() for larger text

        st.markdown("---")
        st.markdown(f"### Total Harga Item Custom: Rp {total_custom_cost:,.2f}")


    group_structure = t_earth + t_found + t_struc
    group_arch = (t_arch_base + t_w_door + t_g_door + t_s_door + t_lobby + t_ht + t_vinyl +
                  t_marmer + t_carpet + t_gondola + t_glass_work + t_kitchen + t_hw_w + t_hw_s + t_railing + t_skylight)
    group_facade = t_precast + t_window + t_double
    group_sanitary = t_unit_san + t_t_male + t_t_female + t_t_dis + t_mushola
    group_mep = t_ffe + t_misc + t_mep + t_utility
    group_ext = t_external + t_pub_fac + t_res_fac + t_proj_fac
    group_contingency = t_preliminary + t_contingency


    with tab5:
        st.subheader("Hasil")
        sum_sub_tabs = st.tabs(["1. Total", "2. Tabel", "3. Chart", "4. FAD", "5. Rekap"])

        with sum_sub_tabs[0]:
            st.subheader("Total")
            c1, c2 = st.columns(2)
            c1.markdown(f"""
                <div style="margin-bottom: 20px;">
                    <div style="font-size: 16px; color: gray; margin-bottom: 5px;">Total Hard Cost</div>
                    <div style="font-size: 28px; font-weight: bold; word-wrap: break-word; white-space: normal; line-height: 1.5;">
                        <div>Rp {hc_total:,.2f}</div>
                        <div style="font-size: 16px; color: gray; font-weight: normal; margin-bottom: 5px;">Terbilang: {n2w(hc_total)} Rupiah</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            c2.markdown(f"""
                <div style="margin-bottom: 20px;">
                    <div style="font-size: 16px; color: gray; margin-bottom: 5px;">Total Soft Cost</div>
                    <div style="font-size: 28px; font-weight: bold; word-wrap: break-word; white-space: normal; line-height: 1.5;">
                        <div>Rp {sc_total:,.2f}</div>
                        <div style="font-size: 16px; color: gray; font-weight: normal; margin-bottom: 5px;">Terbilang: {n2w(sc_total)} Rupiah</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div style="margin-bottom: 30px; padding: 15px; border-radius: 8px; border: 1px solid #4B4C55;">
                    <div style="font-size: 18px; margin-bottom: 5px;">Grand Total Project Cost (Hard Cost + Soft Cost)</div>
                    <div style="font-size: 38px; font-weight: bold; word-wrap: break-word; white-space: normal; line-height: 1.5;">
                        <div>Rp {grand_total_project:,.2f}</div>
                        <div style="font-size: 16px; font-weight: normal; margin-bottom: 5px;">Terbilang: {n2w(grand_total_project)} Rupiah</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with sum_sub_tabs[1]:
            st.subheader("Tabel")
            raw_amounts = [
                t_preliminary, t_earth, t_found, t_struc, t_arch_base,
                t_precast, t_window, t_double, t_w_door, t_g_door,
                t_s_door, t_lobby, t_gondola, t_unit_san, t_t_male,
                t_t_female, t_t_dis, t_mushola, t_kitchen, t_hw_w,
                t_hw_s, t_ht, t_vinyl, t_marmer, t_carpet,
                t_glass_work, t_ffe, t_misc, t_mep, t_utility,
                t_railing, t_skylight, t_external, t_pub_fac, t_res_fac,
                t_proj_fac,
                total_custom_cost,
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
                    "36. Project Facilities", "37. Smart Custom Costs",
                    "38. Contingencies", "39. Consultancy Fee", "40. Quantity Surveyor", "41. Project Management", "42. Insurance Coverage"
                ],
                "Basis": [
                    f"5% x Rp {(hc_subtotal):,.0f}",
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
                    f"{rooms:,.0f} Rooms x {san_qty_room} Set x Rp {san_room_rate:,.0f}",
                    f"{toilet_male:,.0f} Units x Rp {san_pub_m:,.0f}",
                    f"{toilet_female:,.0f} Units x Rp {san_pub_f:,.0f}",
                    f"{disabled_toil:,.0f} Units x Rp {san_dis:,.0f}",
                    f"{mushola_unit:,.0f} Units x Rp {san_mushola:,.0f}",
                    f"{rooms:,.0f} Rooms x Rp {kitchen_rate:,.0f}",
                    f"{wooden_door:,.0f} Doors x Rp {hw_wood:,.0f}",
                    f"{steel_door:,.0f} Doors x Rp {hw_steel:,.0f}",
                    f"{fl_ht_pct}% of GFA x {f_mult} x Rp {fl_ht_rate:,.0f}",
                    f"{fl_vinyl_pct}% of GFA x {f_mult} x Rp {fl_vinyl_rate:,.0f}",
                    f"{fl_marmer_pct}% of GFA x {f_mult} x Rp {fl_marmer_rate:,.0f}",
                    f"{carpet_m2:,.0f} m2 x Rp {carpet_rate:,.0f}",
                    f"{glass_m2:,.0f} m2 x Rp {glass_rate:,.0f}",
                    f"{rooms:,.0f} Rooms x Rp {ffe_rate:,.0f}",
                    f"Rp {misc_rate if misc_switch else 0:,.0f}",
                    f"{gba:,.0f} m2 x Rp {mep_rate:,.0f}",
                    f"{gba:,.0f} m2 x Rp {utility_rate:,.0f}",
                    f"{rooms * railing_qty:,.0f} m' Total x Rp {railing_rate:,.0f}",
                    f"{skylight_area:,.0f} m2 Total x Rp {skylight_rate:,.0f}",
                    f"{land_m2:,.0f} m2 x Rp {ext_land_rate:,.0f}",
                    f"{pub_fac_m2:,.0f} m2 x Rp {fac_pub_rate:,.0f}",
                    f"{res_fac_m2:,.0f} m2 x Rp {fac_res_rate:,.0f}",
                    f"{proj_fac_u:,.0f} Units x Rp {fac_proj_rate:,.0f}",
                    " | ".join(get_val("extra_items_summary_list", ["-"])),
                    f"3% x Rp {(hc_subtotal):,.0f}",
                    f"{gfa:,.0f} m2 x Rp {consultancy_rate:,.0f}",
                    f"{qs_months} Months x Rp {qs_rate:,.0f}/Mo",
                    f"{pm_months} Months x Rp {pm_rate:,.0f}/Mo",
                    f"{insurance_pct}% x Rp {(hc_subtotal):,.0f}"
                ],
                "Amount": [f"Rp {val:,.2f}" for val in raw_amounts]
            }
            st.dataframe(pd.DataFrame(cost_data), use_container_width=True, hide_index=True)

        with sum_sub_tabs[2]:            
            st.subheader("Chart")

            # 1. Define the dictionary first
            detailed_items = {
                "Item": [
                    "Preliminary", "Earthwork", "Foundation", "Structural", "Basic Arch",
                    "Precast", "Window Wall", "Double Skin", "Wooden Doors", "Glass Doors",
                    "Steel Doors", "Lobby", "Gondola", "Unit Sanitary", "Public Toilet (M)",
                    "Public Toilet (F)", "Disabled Toilet", "Mushola", "Kitchen Eq.", "Hardware (Wood)",
                    "Hardware (Steel)", "HT/Ceramic", "Vinyl", "Marmer", "Carpet",
                    "Glass Work", "FF&E", "Misc (Linen/Gym)", "MEP Works", "Utility",
                    "Railing", "Skylight", "External/Landscape", "Public Fac.", "Resident Fac.",
                    "Project Fac.", "Custom Items", "Contingency",
                    "Consultancy", "QS Fee", "PM Fee", "Insurance"
                ],
                "Amount": [
                    t_preliminary, t_earth, t_found, t_struc, t_arch_base,
                    t_precast, t_window, t_double, t_w_door, t_g_door,
                    t_s_door, t_lobby, t_gondola, t_unit_san, t_t_male,
                    t_t_female, t_t_dis, t_mushola, t_kitchen, t_hw_w,
                    t_hw_s, t_ht, t_vinyl, t_marmer, t_carpet,
                    t_glass_work, t_ffe, t_misc, t_mep, t_utility,
                    t_railing, t_skylight, t_external, t_pub_fac, t_res_fac,
                    t_proj_fac, total_custom_cost, t_contingency,
                    t_consultancy, t_qs, t_pm, t_insurance
                ],
                # Adding 'Type' helps with color coding the chart
                "Type": ["Hard Cost"]*38 + ["Soft Cost"]*4 
            }


            # 2. Convert to DataFrame and FILTER OUT zeros
            df_detailed = pd.DataFrame(detailed_items)
            df_detailed = df_detailed[df_detailed["Amount"] > 0] 

            # 3. Dynamic height calculation
            chart_height = max(400, len(df_detailed) * 25)

            # 4. Create the Chart
            detailed_chart = alt.Chart(df_detailed).mark_bar().encode(
                x=alt.X("Amount:Q", title="Cost (Rp)"),
                y=alt.Y("Item:N", sort="-x", title=""),
                # Color by Type (Hard vs Soft) makes it much easier to read!
                color=alt.Color("Type:N", scale=alt.Scale(domain=['Hard Cost', 'Soft Cost'], range=['#1f77b4', '#ff7f0e'])),
                tooltip=["Item", "Type", alt.Tooltip("Amount:Q", format=",.2f")]
            ).properties(height=chart_height)

            st.altair_chart(detailed_chart, use_container_width=True)
            st.markdown("---")

        # --- SAVE ALL METRICS TO SESSION STATE ---
        current_metrics = {
            "proj_name": new_name, "proj_type": new_type,
            "misc_switch": misc_switch,
            "ht_spec_type": get_val("ht_spec_type", "Type1"),
            "vin_spec_type": get_val("vin_spec_type", "Type1"),
            "mar_spec_type": get_val("mar_spec_type", "Type1"),
            "m_land": land_area, "m_gba": gba, "m_gfa": gfa, "m_sgfa": sgfa,
            "m_facade": facade, "m_rooms": rooms, "m_lobby": lobby_interior,
            "m_gondola": gondola_unit, "m_carpet": carpet_m2, "m_glass": glass_m2,
            "m_skylight": skylight_area, "m_door_g": glass_door, "m_door_w": wooden_door,
            "m_door_s": steel_door, "m_toil_m": toilet_male, "m_toil_f": toilet_female,
            "m_toil_d": disabled_toil, "m_mushola": mushola_unit, "m_fac_res": res_fac_m2,
            "m_fac_pub": pub_fac_m2, "m_fac_proj": proj_fac_u, "m_land_m2": land_m2,
            "r_fac_pre": facade_precast_pct, "r_fac_win": facade_window_pct, "r_fac_doub": facade_double_pct,
            "r_fl_ht": fl_ht_pct, "r_fl_vin": fl_vinyl_pct, "r_fl_mar": fl_marmer_pct,
            "r_san_qty": san_qty_room, "r_rail_qty": railing_qty,
            "u_earth": struc_earth, "u_found": struc_found, "u_struc": struc_work, "u_arch": arch_base,
            "u_lobby": lobby_rate, "u_f_pre": fac_precast_rate, "u_f_win": fac_window_rate, "u_f_doub": fac_double_rate,
            "u_d_wood": door_wood, "u_d_glass": door_glass, "u_d_steel": door_steel,
            "u_hw_wood": hw_wood, "u_hw_steel": hw_steel,
            "u_s_room": san_room_rate, "u_s_pub_m": san_pub_m, "u_s_pub_f": san_pub_f,
            "u_s_dis": san_dis, "u_s_mushola": san_mushola,
            "u_fl_ht": fl_ht_rate, "u_fl_vin": fl_vinyl_rate, "u_fl_mar": fl_marmer_rate,
            "u_carpet": carpet_rate, "u_glass": glass_rate, "u_sky": skylight_rate,
            "u_gondola": gondola_rate, "u_rail": railing_rate,
            "u_mep": mep_rate, "u_util": utility_rate,
            "u_ffe": ffe_rate, "u_kit": kitchen_rate, "u_misc": misc_rate,
            "u_ext": ext_land_rate, "u_fac_p": fac_pub_rate,
            "u_fac_r": fac_res_rate, "u_fac_pr": fac_proj_rate,
            "sc_cons": consultancy_rate, "sc_qs_m": qs_months, "sc_qs_r": qs_rate,
            "sc_pm_m": pm_months, "sc_pm_r": pm_rate, "sc_ins": insurance_pct
        }
        # Preserve keys managed elsewhere (custom costs, header, assumptions)
        for k in ("smart_custom_costs", "header_info", "assumptions"):
            if k in st.session_state.projects[curr_id]["data"]:
                current_metrics[k] = st.session_state.projects[curr_id]["data"][k]
        st.session_state.projects[curr_id]["data"] = current_metrics

        import io
        import xlsxwriter
        import re
        from datetime import date
    
        with sum_sub_tabs[3]:
            st.subheader("FAD")
            active_id = st.session_state.current_proj_id
            today_str = date.today().strftime("%d-%m-%Y")

            if "header_info" not in st.session_state.projects[active_id]["data"]:
                st.session_state.projects[active_id]["data"]["header_info"] = {
                    "rev_no": "0", "updated": today_str, "created": today_str
                }

            with st.expander("Edit Header & Assumptions", expanded=False):
                h_col1, h_col2, h_col3 = st.columns(3)
                rev_input = h_col1.text_input("Revision Number:", value=st.session_state.projects[active_id]["data"]["header_info"]["rev_no"], key=f"rev_{active_id}")
                upd_input = h_col2.text_input("Updated Date:", value=st.session_state.projects[active_id]["data"]["header_info"]["updated"], key=f"upd_{active_id}")
                cre_input = h_col3.text_input("Created Date:", value=st.session_state.projects[active_id]["data"]["header_info"]["created"], key=f"cre_{active_id}")
                st.session_state.projects[active_id]["data"]["header_info"] = {"rev_no": rev_input, "updated": upd_input, "created": cre_input}

                st.divider()
                current_assums = st.session_state.projects[active_id]["data"].get("assumptions", [
                    "Foundation System Standard Pilecaps.",
                    "No Basement.",
                    "Parking Provision Limited To On Street Level Parking",
                    "Floor To Floor Height At 3.3M",
                    "Facade Alumunium Window Wall - No Double Skin",
                    "External Façade Precast, No Double Skin For Parking Podium If Any.",
                    "Ground Lobby Finishes Completed With Artificial Stone & HT.",
                    "Typical Corridor | Floor Finishes : HT | Wall Finishes : Cement Sand Plaster C/W Emulsion Paint.",
                    "Aircon System | Apartement : AC Split",
                    "SBO Rebars @ Rp. 10.000/Kg",
                    "Excluded Smarthome",
                    "Lift : 2 Passenger Lift + 1 Services Lift / TOWER",
                    "Exclude Wardrobe",
                    "FFE : Kitchen Cabinet, Hob & Hood, Refrigerator & Washing Machine",
                    "Water Heater : Installation Only",
                    "Calculation Area Refer To DP's Calculation Dated 12.03.2026"
                ])

                df_assum = pd.DataFrame(current_assums, columns=["Note"])
                ed_assum = st.data_editor(df_assum, num_rows="dynamic", use_container_width=True, key=f"ed_sum_{active_id}")

                new_list = ed_assum["Note"].dropna().tolist()
                if new_list != current_assums:
                    st.session_state.projects[active_id]["data"]["assumptions"] = new_list

            # --- MANUAL PROJECTS EDITOR ---
            st.markdown("---")
            st.subheader("Manual Additional Projects")
            st.caption("Add custom projects to the FAD summary below. Cost Ratios (Rp/m2) will be calculated automatically.")
            
            if "manual_fad_projects" not in st.session_state:
                st.session_state.manual_fad_projects = pd.DataFrame(columns=[
                    "Project Name", "GBA", "GFA", "SGFA", "Units", "Budget Estimate (Rp)"
                ])

            edited_manual_df = st.data_editor(
                st.session_state.manual_fad_projects,
                num_rows="dynamic",
                use_container_width=True,
                key="manual_fad_editor",
                column_config={
                    "GBA": st.column_config.NumberColumn("GBA", min_value=0, format="%.0f"),
                    "GFA": st.column_config.NumberColumn("GFA", min_value=0, format="%.0f"),
                    "SGFA": st.column_config.NumberColumn("SGFA", min_value=0, format="%.0f"),
                    "Units": st.column_config.NumberColumn("Units", min_value=0, format="%.0f"),
                    "Budget Estimate (Rp)": st.column_config.NumberColumn("Budget Estimate (Rp)", min_value=0, format="%.0f")
                }
            )

            rev_label = f"R({rev_input})"
            h_upd = upd_input
            h_cre = cre_input
            dynamic_assumptions = current_assums

            def get_project_totals(proj_dict):
                d = proj_dict.get("data", {})
                pt_data = PROJECT_DATABASE.get(proj_dict["type"], PROJECT_DATABASE["Hotel"])
                def v(key, default=0.0):
                    return d.get(key, pt_data.get(key, default))
                gba = v("m_gba"); gfa = v("m_gfa"); sgfa = v("m_sgfa")
                rooms = v("m_rooms"); facade = v("m_facade")
                f_mult = 1.32
                hc = (
                    (gba * v("u_earth")) + (gba * v("u_found")) + (gba * v("u_struc")) + (gfa * v("u_arch")) +
                    (facade * (v("r_fac_pre") / 100) * v("u_f_pre")) + (facade * (v("r_fac_win") / 100) * v("u_f_win")) +
                    (facade * (v("r_fac_doub") / 100) * v("u_f_doub")) + (v("m_door_w") * v("u_d_wood")) +
                    (v("m_door_g") * v("u_d_glass")) + (v("m_door_s") * v("u_d_steel")) +
                    (v("m_lobby") * v("u_lobby")) + (v("m_gondola") * v("u_gondola")) +
                    (rooms * v("r_san_qty") * v("u_s_room")) + (v("m_toil_m") * v("u_s_pub_m")) +
                    (v("m_toil_f") * v("u_s_pub_f")) + (v("m_toil_d") * v("u_s_dis")) +
                    (v("m_mushola") * v("u_s_mushola")) + (rooms * v("u_kit")) +
                    (v("m_door_w") * v("u_hw_wood")) + (v("m_door_s") * v("u_hw_steel")) +
                    (gfa * (v("r_fl_ht") / 100) * v("u_fl_ht") * f_mult) +
                    (gfa * (v("r_fl_vin") / 100) * v("u_fl_vin") * f_mult) +
                    (gfa * (v("r_fl_mar") / 100) * v("u_fl_mar") * f_mult) +
                    (v("m_carpet") * v("u_carpet")) + (v("m_glass") * v("u_glass")) +
                    (rooms * v("u_ffe")) + (v("u_misc") * d.get("misc_switch", 0)) +
                    (gba * v("u_mep")) + (gba * v("u_util")) +
                    (rooms * v("r_rail_qty") * v("u_rail")) + (v("m_skylight") * v("u_sky")) +
                    (v("m_land_m2") * v("u_ext")) + (v("m_fac_pub") * v("u_fac_p")) +
                    (v("m_fac_res") * v("u_fac_r")) + (v("m_fac_proj") * v("u_fac_pr"))
                )
                custom_costs = d.get("smart_custom_costs", [])
                dep_map = {
                    "None (Flat Rate)": 1.0, "GBA": gba, "GFA": gfa, "SGFA": sgfa,
                    "Land Area": v("m_land"), "Rooms": rooms, "Facade": facade, "Lobby": v("m_lobby")
                }
                for item in custom_costs:
                    hc += (float(item.get("Rate (Rp)", 0)) * float(item.get("Multiplier (Qty)", 1)) *
                        dep_map.get(item.get("Linked Dependency"), 1.0))
                hc_total = hc + (hc * 0.05) + (hc * 0.03)
                sc_total = ((gfa * v("sc_cons")) + (v("sc_qs_m") * v("sc_qs_r")) +
                            (v("sc_pm_m") * v("sc_pm_r")) + (hc * (v("sc_ins") / 100)))
                return {"gba": gba, "gfa": gfa, "sgfa": sgfa, "units": rooms, "budget": hc_total + sc_total}

            # --- DATA AGGREGATION (CALCULATED + MANUAL) ---
            combined_results = []
            idx = 1
            
            # 1. Add Auto-Calculated Projects
            for p_id, p_data in st.session_state.projects.items():
                m = get_project_totals(p_data)
                combined_results.append({
                    "idx": idx, "name": p_data["name"].upper(),
                    "gba": m["gba"], "gfa": m["gfa"], "sgfa": m["sgfa"],
                    "units": m["units"], "budget": m["budget"]
                })
                idx += 1

            # 2. Add Manual Projects
            edited_manual_df = edited_manual_df.fillna(0) # <--- ADD THIS LINE
            for _, row in edited_manual_df.iterrows():
                p_name = str(row.get("Project Name", f"MANUAL PROJECT {idx}"))
                if p_name == "nan" or not p_name.strip(): p_name = f"MANUAL PROJECT {idx}"
                
                combined_results.append({
                    "idx": idx, "name": p_name.upper(),
                    "gba": float(row.get("GBA", 0) or 0),
                    "gfa": float(row.get("GFA", 0) or 0),
                    "sgfa": float(row.get("SGFA", 0) or 0),
                    "units": float(row.get("Units", 0) or 0),
                    "budget": float(row.get("Budget Estimate (Rp)", 0) or 0)
                })
                idx += 1

            # 3. Calculate Ratios & Totals
            table_rows_html = ""
            total_gba = total_gfa = total_sgfa = total_budget = 0

            for p in combined_results:
                r_gba  = p["budget"] / p["gba"]  if p["gba"]  > 0 else 0
                r_gfa  = p["budget"] / p["gfa"]  if p["gfa"]  > 0 else 0
                r_sgfa = p["budget"] / p["sgfa"] if p["sgfa"] > 0 else 0

                p["r_gba"] = r_gba
                p["r_gfa"] = r_gfa
                p["r_sgfa"] = r_sgfa

                total_gba += p["gba"]
                total_gfa += p["gfa"]
                total_sgfa += p["sgfa"]
                total_budget += p["budget"]

                table_rows_html += (
                    f"<tr>"
                    f"<td style='border:1px solid black;padding:5px;'>{p['idx']}</td>"
                    f"<td style='border:1px solid black;padding:5px;text-align:left;'><b>{p['name']}</b></td>"
                    f"<td style='border:1px solid black;padding:5px;'>{p['gba']:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>{p['gfa']:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>{p['sgfa']:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>{p['units']:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>Units</td>"
                    f"<td style='border:1px solid black;padding:5px;text-align:right;'><b>{p['budget']:,.0f}</b></td>"
                    f"<td style='border:1px solid black;padding:5px;'>{r_gba:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>{r_gfa:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>{r_sgfa:,.0f}</td>"
                    f"</tr>"
                )

            t_r_gba  = total_budget / total_gba  if total_gba  > 0 else 0
            t_r_gfa  = total_budget / total_gfa  if total_gfa  > 0 else 0
            t_r_sgfa = total_budget / total_sgfa if total_sgfa > 0 else 0

            # --- EXCEL BUILDER ---
            buffer = io.BytesIO()
            workbook = xlsxwriter.Workbook(buffer, {"in_memory": True, "nan_inf_to_errors": True})
            worksheet = workbook.add_worksheet("Portfolio Summary")

            f_blue_L    = workbook.add_format({"bg_color": "#0062a8", "font_color": "white", "bold": True, "valign": "vcenter"})
            f_th        = workbook.add_format({"bg_color": "#f2f2f2", "bold": True, "align": "center", "valign": "vcenter", "border": 1, "text_wrap": True})
            f_td_c      = workbook.add_format({"align": "center", "valign": "vcenter", "border": 1})
            f_td_L_b    = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1, "bold": True})
            f_td_R_b    = workbook.add_format({"align": "right", "valign": "vcenter", "border": 1, "bold": True, "num_format": "#,##0"})
            f_td_num    = workbook.add_format({"align": "right", "valign": "vcenter", "border": 1, "num_format": "#,##0"})
            f_tot_L     = workbook.add_format({"bg_color": "#e0e0e0", "bold": True, "align": "center", "valign": "vcenter", "border": 1})
            f_tot_num   = workbook.add_format({"bg_color": "#e0e0e0", "bold": True, "align": "right", "valign": "vcenter", "border": 1, "num_format": "#,##0"})
            f_tot_empty = workbook.add_format({"bg_color": "#e0e0e0", "border": 1})
            f_assum_h   = workbook.add_format({"bg_color": "#ffdf70", "bold": True, "border": 1, "valign": "vcenter"})
            f_assum_c   = workbook.add_format({"align": "center", "border": 1})
            f_assum_L   = workbook.add_format({"align": "left", "border": 1})

            worksheet.set_column("A:A", 5); worksheet.set_column("B:B", 38); worksheet.set_column("C:E", 15)
            worksheet.set_column("F:F", 10); worksheet.set_column("G:G", 8); worksheet.set_column("H:H", 22)
            worksheet.set_column("I:K", 15)

            for row in range(5):
                worksheet.merge_range(row, 0, row, 10, "", f_blue_L)
            worksheet.write_string(0, 0, f"ASG GROUP PROPERTY DEVELOPMENT | VERSION : {rev_label}", f_blue_L)
            worksheet.write_string(1, 0, "QS & PROCUREMENT DIVISION", f_blue_L)
            worksheet.write_string(2, 0, "PROJECT PORTFOLIO | ALL ACTIVE PROJECTS", f_blue_L)
            worksheet.write_string(3, 0, f"REF. DATA {rev_label} | CONCEPT PDF COMPARISON STUDY BY DPA | UPDATED : {h_upd}", f_blue_L)
            worksheet.write_string(4, 0, f"BUDGET ESTIMATE {rev_label} | CREATED : {h_cre}", f_blue_L)

            worksheet.merge_range("A7:A8", "SN", f_th); worksheet.merge_range("B7:B8", "AREA", f_th)
            worksheet.merge_range("C7:E7", "BUILDING AREA (M2)", f_th)
            worksheet.write_string("C8", "GBA", f_th); worksheet.write_string("D8", "GFA", f_th); worksheet.write_string("E8", "SGFA", f_th)
            worksheet.merge_range("F7:G8", "UNIT", f_th); worksheet.merge_range("H7:H8", "BUDGET ESTIMATE\nRP", f_th)
            worksheet.merge_range("I7:K7", "COST RATIO RP/M2", f_th)
            worksheet.write_string("I8", "GBA", f_th); worksheet.write_string("J8", "GFA", f_th); worksheet.write_string("K8", "SGFA", f_th)

            row_idx = 8
            for p in combined_results:
                worksheet.write_number(row_idx, 0, p["idx"], f_td_c)
                worksheet.write_string(row_idx, 1, p["name"], f_td_L_b)
                worksheet.write_number(row_idx, 2, p["gba"], f_td_num)
                worksheet.write_number(row_idx, 3, p["gfa"], f_td_num)
                worksheet.write_number(row_idx, 4, p["sgfa"], f_td_num)
                worksheet.write_number(row_idx, 5, p["units"], f_td_c)
                worksheet.write_string(row_idx, 6, "Units", f_td_c)
                worksheet.write_number(row_idx, 7, p["budget"], f_td_R_b)
                worksheet.write_number(row_idx, 8, p["r_gba"], f_td_num)
                worksheet.write_number(row_idx, 9, p["r_gfa"], f_td_num)
                worksheet.write_number(row_idx, 10, p["r_sgfa"], f_td_num)
                row_idx += 1

            worksheet.merge_range(row_idx, 0, row_idx, 1, "TOTAL", f_tot_L)
            worksheet.write_number(row_idx, 2, total_gba, f_tot_num)
            worksheet.write_number(row_idx, 3, total_gfa, f_tot_num)
            worksheet.write_number(row_idx, 4, total_sgfa, f_tot_num)
            worksheet.write_string(row_idx, 5, "", f_tot_empty)
            worksheet.write_string(row_idx, 6, "", f_tot_empty)
            worksheet.write_number(row_idx, 7, total_budget, f_tot_num)
            worksheet.write_number(row_idx, 8, t_r_gba, f_tot_num)
            worksheet.write_number(row_idx, 9, t_r_gfa, f_tot_num)
            worksheet.write_number(row_idx, 10, t_r_sgfa, f_tot_num)

            row_idx += 2
            worksheet.write_string(row_idx, 0, "I.", f_assum_h)
            worksheet.merge_range(row_idx, 1, row_idx, 10, "ASSUMPTIONS", f_assum_h)
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
                    rich_args.extend([workbook.add_format({"font_color": "red"}), date_match.group(1)])
                    if len(parts) > 1 and parts[1]: rich_args.append(parts[1])
                    worksheet.write_rich_string(row_idx, 1, *rich_args, f_assum_L)
                else:
                    worksheet.merge_range(row_idx, 1, row_idx, 10, text, f_assum_L)
            workbook.close()

            st.download_button(
                label="Download FAD as .xlsx",
                data=buffer.getvalue(),
                file_name=f"ASG_Portfolio_{active_id}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

            # --- HTML TABLE RENDER ---
            assum_html_rows = ""
            for i, assum in enumerate(dynamic_assumptions, 1):
                display_text = re.sub(r"(\d{2}[./-]\d{2}[./-]\d{4})", r"<span style='color:red;'>\1</span>", str(assum))
                assum_html_rows += (
                    f"<tr><td style='text-align:center;border-right:1px solid #e0e0e0;padding:2px;'>{i}</td>"
                    f"<td style='padding:2px 5px;'>{display_text}</td></tr>"
                )

            html_string = f"""
            <div style="font-family:Calibri,sans-serif;font-size:13px;color:black;background-color:white;padding:20px;border-radius:5px;">
                <div style="background-color:#0062a8;color:white;padding:12px;font-weight:bold;line-height:1.6;font-size:14px;text-align:left;">
                    <div>ASG GROUP PROPERTY DEVELOPMENT <span style="margin-left:20px;">VERSION : {rev_label}</span></div>
                    <div>QS &amp; PROCUREMENT DIVISION</div>
                    <div>PROJECT PORTFOLIO | ALL ACTIVE PROJECTS</div>
                    <div>REF. DATA {rev_label} | CONCEPT PDF COMPARISON STUDY BY DPA <span style="margin-left:20px;">UPDATED : {h_upd}</span></div>
                    <div>BUDGET ESTIMATE {rev_label} <span style="margin-left:20px;">CREATED : {h_cre}</span></div>
                </div>
                <br>
                <table style="width:100%;border-collapse:collapse;border:2px solid black;text-align:center;">
                    <tr style="background-color:#f2f2f2;font-weight:bold;">
                        <td rowspan="2" style="border:1px solid black;padding:5px;">SN</td>
                        <td rowspan="2" style="border:1px solid black;padding:5px;">AREA</td>
                        <td colspan="3" style="border:1px solid black;padding:5px;">BUILDING AREA (M2)</td>
                        <td colspan="2" rowspan="2" style="border:1px solid black;padding:5px;">UNIT</td>
                        <td rowspan="2" style="border:1px solid black;padding:5px;">BUDGET ESTIMATE<br>RP</td>
                        <td colspan="3" style="border:1px solid black;padding:5px;">COST RATIO RP/M2</td>
                    </tr>
                    <tr style="background-color:#f2f2f2;font-weight:bold;">
                        <td style="border:1px solid black;padding:5px;">GBA</td>
                        <td style="border:1px solid black;padding:5px;">GFA</td>
                        <td style="border:1px solid black;padding:5px;">SGFA</td>
                        <td style="border:1px solid black;padding:5px;">GBA</td>
                        <td style="border:1px solid black;padding:5px;">GFA</td>
                        <td style="border:1px solid black;padding:5px;">SGFA</td>
                    </tr>
                    {table_rows_html}
                    <tr style="background-color:#e0e0e0;font-weight:bold;">
                        <td colspan="2" style="border:1px solid black;padding:5px;">TOTAL</td>
                        <td style="border:1px solid black;padding:5px;">{total_gba:,.0f}</td>
                        <td style="border:1px solid black;padding:5px;">{total_gfa:,.0f}</td>
                        <td style="border:1px solid black;padding:5px;">{total_sgfa:,.0f}</td>
                        <td colspan="2" style="border:1px solid black;padding:5px;"></td>
                        <td style="border:1px solid black;padding:5px;text-align:right;">{total_budget:,.0f}</td>
                        <td style="border:1px solid black;padding:5px;">{t_r_gba:,.0f}</td>
                        <td style="border:1px solid black;padding:5px;">{t_r_gfa:,.0f}</td>
                        <td style="border:1px solid black;padding:5px;">{t_r_sgfa:,.0f}</td>
                    </tr>
                </table>
                <br>
                <table style="width:100%;border-collapse:collapse;border:1px solid #dcdcdc;text-align:left;">
                    <tr style="background-color:#ffdf70;font-weight:bold;">
                        <td style="border:1px solid white;padding:3px 5px;width:30px;text-align:center;">I.</td>
                        <td style="border:1px solid white;padding:3px 5px;">ASSUMPTIONS</td>
                    </tr>
                    {assum_html_rows}
                </table>
            </div>
            """
            st.markdown(html_string.replace("\n", ""), unsafe_allow_html=True)

        with sum_sub_tabs[4]:
            st.subheader("Rekap")

            # 1. SETUP: Prepare to collect data for ALL projects
            all_projects_data = []
            grand_total_all_projects = 0
            
            # Area trackers for combined ratios
            total_gba_all = 0; total_gfa_all = 0; total_sgfa_all = 0
            
            # Subtotal trackers for the first "TOTAL" column
            sum_hardcost = 0; sum_prelim = 0; sum_earth = 0; sum_found = 0; sum_struc = 0
            sum_arch = 0; sum_ffe = 0; sum_mep = 0; sum_util = 0; sum_ext = 0; sum_fac = 0
            sum_cont = 0; sum_softcost = 0; sum_cons = 0; sum_qs = 0; sum_pm = 0; sum_ins = 0

            # 2. CALCULATE EACH PROJECT
            for p_id, p_dict in st.session_state.projects.items():
                d = p_dict.get("data", {})
                pt_data = PROJECT_DATABASE.get(p_dict["type"], PROJECT_DATABASE["Hotel"])
                
                def v(key, default=0.0):
                    try:
                        return float(d.get(key, pt_data.get(key, default)))
                    except (ValueError, TypeError):
                        return 0.0

                gba = v("m_gba"); gfa = v("m_gfa"); sgfa = v("m_sgfa")
                facade = v("m_facade"); rooms = v("m_rooms")
                f_mult = 1.32

                # Hardcosts
                v_earth = gba * v("u_earth")
                v_found = gba * v("u_found")
                v_struc = gba * v("u_struc")
                v_arch = (
                    (gfa * v("u_arch")) + (facade * (v("r_fac_pre") / 100) * v("u_f_pre")) + 
                    (facade * (v("r_fac_win") / 100) * v("u_f_win")) + (facade * (v("r_fac_doub") / 100) * v("u_f_doub")) + 
                    (v("m_door_w") * v("u_d_wood")) + (v("m_door_g") * v("u_d_glass")) + (v("m_door_s") * v("u_d_steel")) + 
                    (v("m_lobby") * v("u_lobby")) + (v("m_gondola") * v("u_gondola")) + (rooms * v("r_san_qty") * v("u_s_room")) + 
                    (v("m_toil_m") * v("u_s_pub_m")) + (v("m_toil_f") * v("u_s_pub_f")) + (v("m_toil_d") * v("u_s_dis")) + 
                    (v("m_mushola") * v("u_s_mushola")) + (v("m_door_w") * v("u_hw_wood")) + (v("m_door_s") * v("u_hw_steel")) + 
                    (gfa * (v("r_fl_ht") / 100) * v("u_fl_ht") * f_mult) + (gfa * (v("r_fl_vin") / 100) * v("u_fl_vin") * f_mult) + 
                    (gfa * (v("r_fl_mar") / 100) * v("u_fl_mar") * f_mult) + (v("m_carpet") * v("u_carpet")) + 
                    (v("m_glass") * v("u_glass")) + (rooms * v("r_rail_qty") * v("u_rail")) + (v("m_skylight") * v("u_sky"))
                )
                v_ffe = (rooms * v("u_ffe")) + (rooms * v("u_kit")) + (v("u_misc") * d.get("misc_switch", 0))
                v_mep = gba * v("u_mep")
                v_util = gba * v("u_util")
                v_ext = v("m_land_m2") * v("u_ext")
                v_fac = (v("m_fac_pub") * v("u_fac_p")) + (v("m_fac_res") * v("u_fac_r")) + (v("m_fac_proj") * v("u_fac_pr"))
                
                # Custom
                c_costs = d.get("smart_custom_costs", [])
                dep_map = {"None (Flat Rate)": 1.0, "GBA": gba, "GFA": gfa, "SGFA": sgfa, "Land Area": v("m_land"), "Rooms": rooms, "Facade": facade, "Lobby": v("m_lobby")}
                v_custom = sum([(float(item.get("Rate (Rp)", 0)) * float(item.get("Multiplier (Qty)", 1)) * dep_map.get(item.get("Linked Dependency"), 1.0)) for item in c_costs])

                hc_sub = v_earth + v_found + v_struc + v_arch + v_ffe + v_mep + v_util + v_ext + v_fac + v_custom
                v_prelim = (hc_sub) * 0.05
                v_cont = (hc_sub) * 0.03
                hc_tot = hc_sub + v_prelim + v_cont

                # Softcosts
                v_cons = gfa * v("sc_cons")
                v_qs = v("sc_qs_m") * v("sc_qs_r")
                v_pm = v("sc_pm_m") * v("sc_pm_r")
                v_ins = (hc_sub) * (v("sc_ins") / 100)
                sc_tot = v_cons + v_qs + v_pm + v_ins
                
                p_grand = hc_tot + sc_tot

                # Store for this project
                proj_data = {
                    "name": p_dict["name"], "gba": gba, "gfa": gfa, "sgfa": sgfa, "grand": p_grand,
                    "vals": {
                        "hc": hc_tot, "prelim": v_prelim, "earth": v_earth, "found": v_found, "struc": v_struc,
                        "arch": v_arch, "ffe": v_ffe, "mep": v_mep, "util": v_util, "ext": v_ext, "fac": v_fac,
                        "cont": v_cont, "sc": sc_tot, "cons": v_cons, "qs": v_qs, "pm": v_pm, "ins": v_ins
                    }
                }
                all_projects_data.append(proj_data)

                # Add to grand totals
                total_gba_all += gba
                total_gfa_all += gfa
                total_sgfa_all += sgfa
                
                sum_hardcost += hc_tot; sum_prelim += v_prelim; sum_earth += v_earth; sum_found += v_found
                sum_struc += v_struc; sum_arch += v_arch; sum_ffe += v_ffe; sum_mep += v_mep
                sum_util += v_util; sum_ext += v_ext; sum_fac += v_fac; sum_cont += v_cont
                sum_softcost += sc_tot; sum_cons += v_cons; sum_qs += v_qs; sum_pm += v_pm; sum_ins += v_ins
                grand_total_all_projects += p_grand

            # 3. BUILD DYNAMIC HTML HEADERS
            color_palette = ["#ccffe6", "#ffe6e6", "#e6e6ff", "#ffffe6", "#ffe6ff"] # Colors for different projects
            
            # Header Row 1 (Project Names)
            header_col_names = f'<td colspan="4" style="border:1px solid black; padding:4px; background-color: #e6f2ff;">TOTAL <span style="margin:0 15px;">Cost Ratio (Rp/m2)</span></td>'
            
            # Header Row 2 (Cost Ratio Titles)
            header_ratios = f'<td colspan="4" style="border:1px solid black; padding:4px; background-color: #e6f2ff; color: red;">ALL PROJECTS</td>'
            
            # Header Row 3 (GBA/GFA/SGFA labels)
            header_sublabels = f"""
                <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">TOTAL (Rp)</td>
                <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">GBA</td>
                <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">GFA</td>
                <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">SGFA</td>
            """
            
            # Header Row 4 (Overall Area Totals)
            header_empty = f"""
                <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">-</td>
                <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">{total_gba_all:,.0f}</td>
                <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">{total_gfa_all:,.0f}</td>
                <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">{total_sgfa_all:,.0f}</td>
            """

            for i, p in enumerate(all_projects_data):
                bg_col = color_palette[i % len(color_palette)]
                
                header_col_names += f'<td colspan="4" style="border:1px solid black; padding:4px; background-color: {bg_col};">ESTIMATE <span style="margin:0 15px;">Cost Ratio (Rp/m2)</span></td>'
                header_ratios += f'<td colspan="4" style="border:1px solid black; padding:4px; background-color: {bg_col}; color: red;">{p["name"].upper()}</td>'
                header_sublabels += f"""
                    <td style="border:1px solid black; padding:4px; background-color: {bg_col};">TOTAL (Rp)</td>
                    <td style="border:1px solid black; padding:4px; background-color: {bg_col};">GBA</td>
                    <td style="border:1px solid black; padding:4px; background-color: {bg_col};">GFA</td>
                    <td style="border:1px solid black; padding:4px; background-color: {bg_col};">SGFA</td>
                """
                header_empty += f"""
                    <td style="border:1px solid black; padding:4px; background-color: {bg_col};">-</td>
                    <td style="border:1px solid black; padding:4px; background-color: {bg_col};">{p["gba"]:,.0f}</td>
                    <td style="border:1px solid black; padding:4px; background-color: {bg_col};">{p["gfa"]:,.0f}</td>
                    <td style="border:1px solid black; padding:4px; background-color: {bg_col};">{p["sgfa"]:,.0f}</td>
                """

            # 4. ROW DEFINITIONS
            row_map = [
                {"sn": "I", "desc": "HARDCOST", "coa": "118-14-000", "key": "hc", "sum": sum_hardcost, "is_main": True},
                {"sn": "1", "desc": "PRELIMINARIES WORKS", "coa": "118-14-100", "key": "prelim", "sum": sum_prelim, "is_main": False},
                {"sn": "2", "desc": "EARTHWORKS", "coa": "118-14-200", "key": "earth", "sum": sum_earth, "is_main": False},
                {"sn": "3", "desc": "FOUNDATIONS", "coa": "118-14-300", "key": "found", "sum": sum_found, "is_main": False},
                {"sn": "4", "desc": "STRUCTURAL WORKS", "coa": "118-14-500", "key": "struc", "sum": sum_struc, "is_main": False},
                {"sn": "5", "desc": "ARCHITECTURAL WORKS", "coa": "118-14-600", "key": "arch", "sum": sum_arch, "is_main": False},
                {"sn": "6", "desc": "FF & E", "coa": "118-14-700", "key": "ffe", "sum": sum_ffe, "is_main": False},
                {"sn": "7", "desc": "M.E.P WORKS", "coa": "118-14-800", "key": "mep", "sum": sum_mep, "is_main": False},
                {"sn": "8", "desc": "UTILITY CONNECTION", "coa": "118-13-900", "key": "util", "sum": sum_util, "is_main": False},
                {"sn": "9", "desc": "EXTERNAL WORKS", "coa": "118-14-930", "key": "ext", "sum": sum_ext, "is_main": False},
                {"sn": "10", "desc": "FACILITY", "coa": "118-14-960", "key": "fac", "sum": sum_fac, "is_main": False},
                {"sn": "11", "desc": "CONTINGENCIES", "coa": "", "key": "cont", "sum": sum_cont, "is_main": False},
                {"sn": "II", "desc": "SOFTCOST", "coa": "118-13-000", "key": "sc", "sum": sum_softcost, "is_main": True},
                {"sn": "1", "desc": "CONSULTANCY SERVICES FEE", "coa": "118-13-202", "key": "cons", "sum": sum_cons, "is_main": False},
                {"sn": "2", "desc": "QS SERVICES", "coa": "118-13-201", "key": "qs", "sum": sum_qs, "is_main": False},
                {"sn": "3", "desc": "PROJECT MANAGEMENT SERVICES", "coa": "118-13-203", "key": "pm", "sum": sum_pm, "is_main": False},
                {"sn": "4", "desc": "INSURANCE COVERAGE", "coa": "118-13-300", "key": "ins", "sum": sum_ins, "is_main": False},
                {"sn": "IV", "desc": "TOTAL, EXCLD PPN", "coa": "", "key": "grand", "sum": grand_total_all_projects, "is_main": True, "is_grand_total": True}
            ]

            # 5. BUILD DATA ROWS DYNAMICALLY
            html_rows = ""
            for row in row_map:
                bg_color = "#e6f2e6" if row.get("is_main") else "white"
                font_w = "bold" if row.get("is_main") else "normal"
                blue_bg = "background-color:#3b82f6;color:white;" if row.get("is_grand_total") else ""
                
                pct = (row["sum"] / grand_total_all_projects * 100) if grand_total_all_projects > 0 else 0
                
                # Overall Portfolio Ratios
                tot_r_gba = (row["sum"] / total_gba_all) if total_gba_all > 0 else 0
                tot_r_gfa = (row["sum"] / total_gfa_all) if total_gfa_all > 0 else 0
                tot_r_sgfa = (row["sum"] / total_sgfa_all) if total_sgfa_all > 0 else 0

                # Start row with left-side static labels and the Grand Total section
                row_html = f"""
                <tr style="background-color:{bg_color}; font-weight:{font_w}; {blue_bg}">
                    <td style="border:1px solid black; padding:4px; text-align:center;">{row['sn']}</td>
                    <td style="border:1px solid black; padding:4px; text-align:left;">{row['desc']}</td>
                    <td style="border:1px solid black; padding:4px; text-align:center;">{row['coa']}</td>
                    <td style="border:1px solid black; padding:4px; text-align:center;">{pct:.2f}%</td>
                    <td style="border:1px solid black; padding:4px; text-align:right;">{row['sum']:,.0f}</td>
                    <td style="border:1px solid black; padding:4px; text-align:right;">{tot_r_gba:,.0f}</td>
                    <td style="border:1px solid black; padding:4px; text-align:right;">{tot_r_gfa:,.0f}</td>
                    <td style="border:1px solid black; padding:4px; text-align:right;">{tot_r_sgfa:,.0f}</td>
                """
                
                # Append data dynamically for each project
                for p in all_projects_data:
                    val = p['grand'] if row['key'] == 'grand' else p['vals'][row['key']]
                    r_gba = (val / p['gba']) if p['gba'] > 0 else 0
                    r_gfa = (val / p['gfa']) if p['gfa'] > 0 else 0
                    r_sgfa = (val / p['sgfa']) if p['sgfa'] > 0 else 0
                    
                    row_html += f"""
                        <td style="border:1px solid black; padding:4px; text-align:right;">{val:,.0f}</td>
                        <td style="border:1px solid black; padding:4px; text-align:right;">{r_gba:,.0f}</td>
                        <td style="border:1px solid black; padding:4px; text-align:right;">{r_gfa:,.0f}</td>
                        <td style="border:1px solid black; padding:4px; text-align:right;">{r_sgfa:,.0f}</td>
                    """
                
                row_html += "</tr>"
                html_rows += row_html

            # 6. RENDER FINAL TABLE
            detailed_html = f"""
            <div style="font-family: Arial, sans-serif; font-size: 11px; color: black; background-color: white; overflow-x: auto; margin-bottom: 20px;">
                <table style="width: 100%; border-collapse: collapse; border: 2px solid black; text-align: center; white-space: nowrap;">
                    <thead>
                        <tr style="background-color: #f2f2f2; font-weight: bold;">
                            <td rowspan="3" style="border:1px solid black; padding:4px; width:30px;">SN</td>
                            <td rowspan="3" style="border:1px solid black; padding:4px; width:200px;">DESCRIPTION</td>
                            <td rowspan="3" style="border:1px solid black; padding:4px;">COA</td>
                            <td rowspan="3" style="border:1px solid black; padding:4px;">%</td>
                            {header_col_names}
                        </tr>
                        <tr style="font-weight: bold;">
                            {header_ratios}
                        </tr>
                        <tr style="background-color: #f2f2f2; font-weight: bold;">
                            {header_sublabels}
                        </tr>
                        <tr style="background-color: #f2f2f2; font-weight: bold;">
                            <td colspan="4" style="border:1px solid black; padding:4px;"></td>
                            {header_empty}
                        </tr>
                    </thead>
                    <tbody>
                        {html_rows}
                    </tbody>
                </table>
            </div>
            """
            st.markdown(detailed_html.replace("\n", ""), unsafe_allow_html=True)

            # --- EXCEL DOWNLOAD LOGIC ---
            h_info = st.session_state.projects[active_id]["data"].get("header_info", {})
            rev_label = f"R({h_info.get('rev_no', '0')})"
            h_upd = h_info.get("updated", "")
            h_cre = h_info.get("created", "")

            buffer_det = io.BytesIO()
            wb = xlsxwriter.Workbook(buffer_det, {"in_memory": True})
            ws = wb.add_worksheet("Detailed Estimate")

            # Formats
            f_blue = wb.add_format({"bg_color": "#0062a8", "font_color": "white", "bold": True, "valign": "vcenter"})
            f_th = wb.add_format({"bg_color": "#f2f2f2", "bold": True, "align": "center", "valign": "vcenter", "border": 1, "text_wrap": True})
            f_th_tot = wb.add_format({"bg_color": "#e6f2ff", "bold": True, "align": "center", "valign": "vcenter", "border": 1})
            f_th_tot_red = wb.add_format({"bg_color": "#e6f2ff", "bold": True, "align": "center", "valign": "vcenter", "border": 1, "font_color": "red"})
            
            f_c = wb.add_format({"align": "center", "valign": "vcenter", "border": 1})
            f_L = wb.add_format({"align": "left", "valign": "vcenter", "border": 1})
            f_pct = wb.add_format({"align": "center", "valign": "vcenter", "border": 1, "num_format": "0.00%"})
            f_num = wb.add_format({"align": "right", "valign": "vcenter", "border": 1, "num_format": "#,##0"})

            f_mc = wb.add_format({"bg_color": "#e6f2e6", "bold": True, "align": "center", "valign": "vcenter", "border": 1})
            f_mL = wb.add_format({"bg_color": "#e6f2e6", "bold": True, "align": "left", "valign": "vcenter", "border": 1})
            f_mpct = wb.add_format({"bg_color": "#e6f2e6", "bold": True, "align": "center", "valign": "vcenter", "border": 1, "num_format": "0.00%"})
            f_mnum = wb.add_format({"bg_color": "#e6f2e6", "bold": True, "align": "right", "valign": "vcenter", "border": 1, "num_format": "#,##0"})

            f_gc = wb.add_format({"bg_color": "#3b82f6", "font_color": "white", "bold": True, "align": "center", "border": 1})
            f_gL = wb.add_format({"bg_color": "#3b82f6", "font_color": "white", "bold": True, "align": "left", "border": 1})
            f_gpct = wb.add_format({"bg_color": "#3b82f6", "font_color": "white", "bold": True, "align": "center", "border": 1, "num_format": "0.00%"})
            f_gnum = wb.add_format({"bg_color": "#3b82f6", "font_color": "white", "bold": True, "align": "right", "border": 1, "num_format": "#,##0"})

            ws.set_column("A:A", 5); ws.set_column("B:B", 35); ws.set_column("C:C", 12); ws.set_column("D:D", 8)
            
            # Header Block
            for r in range(5): ws.merge_range(r, 0, r, 7 + (len(all_projects_data)*4), "", f_blue)
            ws.write_string(0, 0, f"ASG GROUP PROPERTY DEVELOPMENT | VERSION : {rev_label}", f_blue)
            ws.write_string(1, 0, "QS & PROCUREMENT DIVISION", f_blue)
            ws.write_string(2, 0, "DETAILED ESTIMATE | ALL ACTIVE PROJECTS", f_blue)
            ws.write_string(3, 0, f"REF. DATA {rev_label} | CONCEPT PDF COMPARISON STUDY BY DPA | UPDATED : {h_upd}", f_blue)
            ws.write_string(4, 0, f"BUDGET ESTIMATE {rev_label} | CREATED : {h_cre}", f_blue)

            # Table Headers
            ws.merge_range("A7:A9", "SN", f_th); ws.merge_range("B7:B9", "DESCRIPTION", f_th)
            ws.merge_range("C7:C9", "COA", f_th); ws.merge_range("D7:D9", "%", f_th)

            # Dynamic Header Columns
            col_idx = 4
            ws.merge_range(6, col_idx, 6, col_idx+3, "ESTIMATE Cost Ratio (Rp/m2)", f_th_tot)
            ws.merge_range(7, col_idx, 7, col_idx+3, "TOTAL ALL PROJECTS", f_th_tot_red)
            ws.write(8, col_idx, "TOTAL (Rp)", f_th_tot); ws.write(8, col_idx+1, "GBA", f_th_tot)
            ws.write(8, col_idx+2, "GFA", f_th_tot); ws.write(8, col_idx+3, "SGFA", f_th_tot)
            
            # Write Total Area row
            ws.write_row(9, 0, ["", "", "", ""], f_th)
            ws.write(9, col_idx, "-", f_th_tot); ws.write(9, col_idx+1, total_gba_all, f_th_tot)
            ws.write(9, col_idx+2, total_gfa_all, f_th_tot); ws.write(9, col_idx+3, total_sgfa_all, f_th_tot)
            col_idx += 4

            for i, p in enumerate(all_projects_data):
                color_hex = color_palette[i % len(color_palette)]
                f_proj_th = wb.add_format({"bg_color": color_hex, "bold": True, "align": "center", "valign": "vcenter", "border": 1})
                f_proj_th_red = wb.add_format({"bg_color": color_hex, "bold": True, "align": "center", "valign": "vcenter", "border": 1, "font_color": "red"})
                
                ws.set_column(col_idx, col_idx+3, 14)
                ws.merge_range(6, col_idx, 6, col_idx+3, "ESTIMATE Cost Ratio (Rp/m2)", f_proj_th)
                ws.merge_range(7, col_idx, 7, col_idx+3, p["name"].upper(), f_proj_th_red)
                ws.write(8, col_idx, "TOTAL (Rp)", f_proj_th); ws.write(8, col_idx+1, "GBA", f_proj_th)
                ws.write(8, col_idx+2, "GFA", f_proj_th); ws.write(8, col_idx+3, "SGFA", f_proj_th)
                
                ws.write(9, col_idx, "-", f_proj_th); ws.write(9, col_idx+1, p["gba"], f_proj_th)
                ws.write(9, col_idx+2, p["gfa"], f_proj_th); ws.write(9, col_idx+3, p["sgfa"], f_proj_th)
                col_idx += 4

            # Write Data
            row_idx = 10
            for row in row_map:
                if row.get("is_grand_total"): fmt_c, fmt_str, fmt_pct, fmt_num = f_gc, f_gL, f_gpct, f_gnum
                elif row.get("is_main"): fmt_c, fmt_str, fmt_pct, fmt_num = f_mc, f_mL, f_mpct, f_mnum
                else: fmt_c, fmt_str, fmt_pct, fmt_num = f_c, f_L, f_pct, f_num

                pct_val = (row["sum"] / grand_total_all_projects) if grand_total_all_projects > 0 else 0

                ws.write(row_idx, 0, row['sn'], fmt_c)
                ws.write(row_idx, 1, row['desc'], fmt_str)
                ws.write(row_idx, 2, row['coa'], fmt_c)
                ws.write(row_idx, 3, pct_val, fmt_pct)
                
                # Grand totals and their ratios
                tot_r_gba = (row["sum"] / total_gba_all) if total_gba_all > 0 else 0
                tot_r_gfa = (row["sum"] / total_gfa_all) if total_gfa_all > 0 else 0
                tot_r_sgfa = (row["sum"] / total_sgfa_all) if total_sgfa_all > 0 else 0
                
                ws.write(row_idx, 4, row['sum'], fmt_num)
                ws.write(row_idx, 5, tot_r_gba, fmt_num); ws.write(row_idx, 6, tot_r_gfa, fmt_num); ws.write(row_idx, 7, tot_r_sgfa, fmt_num)

                col_idx = 8
                for p in all_projects_data:
                    val = p['grand'] if row['key'] == 'grand' else p['vals'][row['key']]
                    r_gba = (val / p['gba']) if p['gba'] > 0 else 0
                    r_gfa = (val / p['gfa']) if p['gfa'] > 0 else 0
                    r_sgfa = (val / p['sgfa']) if p['sgfa'] > 0 else 0

                    ws.write(row_idx, col_idx, val, fmt_num)
                    ws.write(row_idx, col_idx+1, r_gba, fmt_num)
                    ws.write(row_idx, col_idx+2, r_gfa, fmt_num)
                    ws.write(row_idx, col_idx+3, r_sgfa, fmt_num)
                    col_idx += 4

                row_idx += 1

            wb.close()

            st.download_button(
                label="Download Rekap as .xlsx",
                data=buffer_det.getvalue(),
                file_name="ASG_Detailed_Estimate_All_Projects.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )


    with tab6:
        st.subheader("Audit")
        
        st.caption(f"Total Earthwork: Rp {struc_earth:,.0f} x GBA: {gba:,.0f} m2 = Rp {struc_earth * gba:,.0f}")
        st.caption(f"Total Foundation: Rp {struc_found:,.0f} x GBA: {gba:,.0f} m2 = Rp {struc_found * gba:,.0f}")
        st.caption(f"Total Structural Work: Rp {struc_work:,.0f} x GBA: {gba:,.0f} m2 = Rp {struc_work * gba:,.0f}")
        st.caption(f"Total Basic Architecture: Rp {arch_base:,.0f} x GFA: {gfa:,.0f} m2 = Rp {arch_base * gfa:,.0f}")
        st.caption(f"Total Facade Precast: Rp {fac_precast_rate:,.0f} x {facade_precast_pct}% of Facade: {facade:,.0f} m2 = Rp {(facade * (facade_precast_pct / 100) * fac_precast_rate):,.0f}")
        st.caption(f"Total Facade Window: Rp {fac_window_rate:,.0f} x {facade_window_pct}% of Facade: {facade:,.0f} m2 = Rp {(facade * (facade_window_pct / 100) * fac_window_rate):,.0f}")
        st.caption(f"Total Facade Double Skin: Rp {fac_double_rate:,.0f} x {facade_double_pct}% of Facade: {facade:,.0f} m2 = Rp {(facade * (facade_double_pct / 100) * fac_double_rate):,.0f}")
        st.caption(f"Total Wooden Doors: Rp {door_wood:,.0f} x {wooden_door:,.0f} Units = Rp {(wooden_door * door_wood):,.0f}")
        st.caption(f"Total Glass Doors: Rp {door_glass:,.0f} x {glass_door:,.0f} Units = Rp {(glass_door * door_glass):,.0f}")
        st.caption(f"Total Steel Doors: Rp {door_steel:,.0f} x {steel_door:,.0f} Units = Rp {(steel_door * door_steel):,.0f}")
        st.caption(f"Total Lobby Interior: Rp {lobby_rate:,.0f} x {lobby_interior:,.0f} m2 = Rp {(lobby_interior * lobby_rate):,.0f}")
        st.caption(f"Total Gondola: Rp {gondola_rate:,.0f} x {gondola_unit:,.0f} Units = Rp {(gondola_unit * gondola_rate):,.0f}")
        st.caption(f"Total Typical Unit Sanitary: Rp {san_room_rate:,.0f} x {rooms:,.0f} Rooms x {san_qty_room} Set = Rp {(rooms * san_qty_room * san_room_rate):,.0f}")
        st.caption(f"Total Public Toilet Male: Rp {san_pub_m:,.0f} x {toilet_male:,.0f} Units = Rp {(toilet_male * san_pub_m):,.0f}")
        st.caption(f"Total Public Toilet Female: Rp {san_pub_f:,.0f} x {toilet_female:,.0f} Units = Rp {(toilet_female * san_pub_f):,.0f}")
        st.caption(f"Total Disabled Toilet: Rp {san_dis:,.0f} x {disabled_toil:,.0f} Units = Rp {(disabled_toil * san_dis):,.0f}")
        st.caption(f"Total Mushola: Rp {san_mushola:,.0f} x {mushola_unit:,.0f} Units = Rp {(mushola_unit * san_mushola):,.0f}")
        st.caption(f"Total Kitchen Equipment: Rp {kitchen_rate:,.0f} x {rooms:,.0f} Rooms = Rp {(rooms * kitchen_rate):,.0f}")
        st.caption(f"Total Hardware Pintu Kayu: Rp {hw_wood:,.0f} x {wooden_door:,.0f} Doors = Rp {(wooden_door * hw_wood):,.0f}")
        st.caption(f"Total Hardware Pintu Besi: Rp {hw_steel:,.0f} x {steel_door:,.0f} Doors = Rp {(steel_door * hw_steel):,.0f}")
        st.caption(f"Total HT/Ceramic Tile: Rp {fl_ht_rate:,.0f} x {fl_ht_pct}% of GFA: {gfa:,.0f} m2 x {f_mult} = Rp {(gfa * (fl_ht_pct / 100) * fl_ht_rate * f_mult):,.0f}")
        st.caption(f"Total Vinyl Flooring: Rp {fl_vinyl_rate:,.0f} x {fl_vinyl_pct}% of GFA: {gfa:,.0f} m2 x {f_mult} = Rp {(gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * f_mult):,.0f}")
        st.caption(f"Total Marmer Flooring: Rp {fl_marmer_rate:,.0f} x {fl_marmer_pct}% of GFA: {gfa:,.0f} m2 x {f_mult} = Rp {(gfa * (fl_marmer_pct / 100) * fl_marmer_rate * f_mult):,.0f}")
        st.caption(f"Total Carpet Work: Rp {carpet_rate:,.0f} x {carpet_m2:,.0f} m2 = Rp {(carpet_m2 * carpet_rate):,.0f}")
        st.caption(f"Total Glass Work: Rp {glass_rate:,.0f} x {glass_m2:,.0f} m2 = Rp {(glass_m2 * glass_rate):,.0f}")
        st.caption(f"Total FF&E: Rp {ffe_rate:,.0f} x {rooms:,.0f} Rooms = Rp {(rooms * ffe_rate):,.0f}")
        st.caption(f"Total Misc. Costs: Rp {misc_rate:,.0f} x Rp {misc_rate if misc_switch else 0:,.0f} = Rp {(misc_rate * misc_switch):,.0f}")
        st.caption(f"Total MEP Works: Rp {mep_rate:,.0f} x {gba:,.0f} m2 = Rp {(gba * mep_rate):,.0f}")
        st.caption(f"Total Utility Connection: Rp {utility_rate:,.0f} x {gba:,.0f} m2 = Rp {(gba * utility_rate):,.0f}")
        st.caption(f"Total Railing Work: Rp {railing_rate:,.0f} x {rooms * railing_qty:,.0f} m' Total = Rp {(rooms * railing_qty * railing_rate):,.0f}")
        st.caption(f"Total Skylight Work: Rp {skylight_rate:,.0f} x {skylight_area:,.0f} m2 Total = Rp {(skylight_area * skylight_rate):,.0f}")
        st.caption(f"Total External Works: Rp {ext_land_rate:,.0f} x {land_m2:,.0f} m2 = Rp {(land_m2 * ext_land_rate):,.0f}")
        st.caption(f"Total Public Facilities: Rp {fac_pub_rate:,.0f} x {pub_fac_m2:,.0f} m2 = Rp {(pub_fac_m2 * fac_pub_rate):,.0f}")
        st.caption(f"Total Resident Facilities: Rp {fac_res_rate:,.0f} x {res_fac_m2:,.0f} m2 = Rp {(res_fac_m2 * fac_res_rate):,.0f}")
        st.caption(f"Total Project Facilities: Rp {fac_proj_rate:,.0f} x {proj_fac_u:,.0f} Units = Rp {(proj_fac_u * fac_proj_rate):,.0f}")


# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.title("Main Navigation")

page_choice = st.sidebar.selectbox(
    "Pilih Pekerjaan:",
    ["Cost Calculator", "Area Calculator"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Daftar Proyek")

proj_ids = list(st.session_state.projects.keys())
proj_labels = [f"{st.session_state.projects[pid]['name']} ({st.session_state.projects[pid]['type']})" for pid in proj_ids]
current_index = proj_ids.index(st.session_state.current_proj_id) if st.session_state.current_proj_id in proj_ids else 0

st.sidebar.selectbox(
    "Active Project:",
    options=proj_labels,
    index=current_index,
    key="project_selector",
    on_change=cb_switch_project,
    label_visibility="collapsed"
)

import streamlit as st

c1, c2 = st.sidebar.columns(2)

with c1:
    st.button("Tambah", on_click=cb_add_project, type="primary", use_container_width=True)

with c2:
    can_delete = len(st.session_state.projects) > 1
    st.button("Hapus", disabled=not can_delete, on_click=cb_delete_project, type="secondary", help="Delete Active Project", use_container_width=True)


st.sidebar.markdown("---")

# --- 6. PAGE ROUTING ---
if page_choice == "Area Calculator":
    show_area_calculator()
else:
    show_cost_estimator()

# --- END OF SCRIPT ---
# BUG 2 FIX: Guard the save operation with the storage_loaded flag
if "projects" in st.session_state and st.session_state.get("storage_loaded", False):
    # CAVEAT 3 FIX: Wrap the payload so we remember the active project and counter
    backup_payload = {
        "projects_dict": st.session_state.projects,
        "current_proj_id": st.session_state.current_proj_id,
        "proj_counter": st.session_state.proj_counter
    }
    local_storage.setItem("asg_calculator_backup", backup_payload)

st.sidebar.caption("v1.1.0 | © 2026 QS & Procurement - ASG")
