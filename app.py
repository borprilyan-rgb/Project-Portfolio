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
        "fl_waste" : 10.0,
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
    },
    "Luxury Apartment": {
        "arch_base": 1517450.0,
        "mep": 3295000.0,
        "utility": 53362.0,
        "door_wood": 4500000.0, "door_steel": 6750000.0, "door_glass": 1000000.0,
        "hw_wood": 1500000.0, "hw_steel": 1400000.0, "lobby": 2500000.0, "gondola": 2000000000.0,
        "carpet": 0.0, "glass": 0.0, "ffe": 29500000.0, "misc": 5250000000.0, "kitchen": 0.0,
        "san_room_rate": 24450000.0, "san_pub_f": 154175000.0, "san_pub_m": 126225000.0,
        "fl_ht_rate": {"Type1": 350000.0, "Type2": 200000.0},
        "fl_vinyl_rate": {"Type1": 0.0, "Type2": 0.0},
        "fl_marmer_rate": {"Type1": 0.0, "Type2": 0.0},
        "facade_precast_pct": 0.0, "facade_window_pct": 0.0, "facade_double_pct": 0.0,
        "fl_ht_pct": 0.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 0.0,
        "san_room_qty": 1.0, "railing_qty": 0.0,
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 1250000.0, "facade_double_rate": 1000000.0,
        "railing_rate": 1100000.0, "skylight_rate": 4500000.0,
        "san_dis": 24481500.0, "san_mushola": 36500000.0, "ext_land": 632077.0,
        "fac_pub": 0.0, "fac_res": 221432.0, "fac_proj": 2000000000.0,
        "cons": 172813.093
    },
    "Apartment2": {
        "arch_base": 1614800.0,
        "mep": 2247000.0,
        "utility": 84274.0,
        "door_wood": 3500000.0, "door_steel": 6750000.0, "door_glass": 1000000.0,
        "hw_wood": 1500000.0, "hw_steel": 1400000.0, "lobby": 2500000.0, "gondola": 1500000000.0,
        "carpet": 0.0, "glass": 0.0, "ffe": 29500000.0, "misc": 5250000000.0, "kitchen": 0.0,
        "san_room_rate": 24450000.0, "san_pub_f": 154175000.0, "san_pub_m": 126225000.0,
        "fl_ht_rate": {"Type1": 350000.0, "Type2": 200000.0},
        "fl_vinyl_rate": {"Type1": 0.0, "Type2": 0.0},
        "fl_marmer_rate": {"Type1": 0.0, "Type2": 0.0},
        "facade_precast_pct": 0.0, "facade_window_pct": 0.0, "facade_double_pct": 0.0,
        "fl_ht_pct": 0.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 0.0,
        "san_room_qty": 1.0, "railing_qty": 0.0,
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 1250000.0, "facade_double_rate": 1000000.0,
        "railing_rate": 1100000.0, "skylight_rate": 4500000.0,
        "san_dis": 24481500.0, "san_mushola": 36500000.0, "ext_land": 459538.0,
        "fac_pub": 0.0, "fac_res": 72243.0, "fac_proj": 2000000000.0,
        "cons": 171378.327
    },
    "Hotel 3 Star": {
        "arch_base": 1517450.0,
        "mep": 4223000.0,
        "utility": 131787.0,
        "door_wood": 4500000.0, "door_steel": 6750000.0, "door_glass": 1000000.0,
        "hw_wood": 8000000.0, "hw_steel": 1900000.0, "lobby": 5000000.0, "gondola": 1500000000.0,
        "carpet": 0.0, "glass": 0.0, "ffe": 64567647.0, "misc": 5250000000.0, "kitchen": 0.0,
        "san_room_rate": 62050000.0, "san_pub_f": 154175000.0, "san_pub_m": 126225000.0,
        "fl_ht_rate": {"Type1": 350000.0, "Type2": 200000.0},
        "fl_vinyl_rate": {"Type1": 0.0, "Type2": 0.0},
        "fl_marmer_rate": {"Type1": 0.0, "Type2": 0.0},
        "facade_precast_pct": 0.0, "facade_window_pct": 0.0, "facade_double_pct": 0.0,
        "fl_ht_pct": 0.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 0.0,
        "san_room_qty": 1.0, "railing_qty": 0.0,
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 2400000.0, "facade_double_rate": 1000000.0,
        "railing_rate": 1100000.0, "skylight_rate": 4500000.0,
        "san_dis": 62050000.0, "san_mushola": 0.0, "ext_land": 213198.0,
        "fac_pub": 0.0, "fac_res": 108200.0, "fac_proj": 2000000000.0,
        "cons": 173906.6059
    },
    "Retail2": {
        "arch_base": 984500.0,
        "mep": 2651000.0,
        "utility": 23724.0,
        "door_wood": 3500000.0, "door_steel": 5000000.0, "door_glass": 1000000.0,
        "hw_wood": 750000.0, "hw_steel": 1900000.0, "lobby": 2500000.0, "gondola": 2000000000.0,
        "carpet": 0.0, "glass": 0.0, "ffe": 0.0, "misc": 0.0, "kitchen": 0.0,
        "san_room_rate": 0.0, "san_pub_f": 154175000.0, "san_pub_m": 126225000.0,
        "fl_ht_rate": {"Type1": 350000.0, "Type2": 200000.0},
        "fl_vinyl_rate": {"Type1": 0.0, "Type2": 0.0},
        "fl_marmer_rate": {"Type1": 0.0, "Type2": 0.0},
        "facade_precast_pct": 0.0, "facade_window_pct": 0.0, "facade_double_pct": 0.0,
        "fl_ht_pct": 0.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 0.0,
        "san_room_qty": 1.0, "railing_qty": 0.0,
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 1250000.0, "facade_double_rate": 2500000.0,
        "railing_rate": 2000000.0, "skylight_rate": 4500000.0,
        "san_dis": 62050000.0, "san_mushola": 36500000.0, "ext_land": 559277.0,
        "fac_pub": 0.0, "fac_res": 0.0, "fac_proj": 2000000000.0,
        "cons": 181035.685
    },
    "Terrace Village": {
        "arch_base": 1517450.0,
        "mep": 4337000.0,
        "utility": 61168.0,
        "door_wood": 3500000.0, "door_steel": 5000000.0, "door_glass": 1000000.0,
        "hw_wood": 750000.0, "hw_steel": 1400000.0, "lobby": 2500000.0, "gondola": 2000000000.0,
        "carpet": 0.0, "glass": 0.0, "ffe": 0.0, "misc": 5250000000.0, "kitchen": 0.0,
        "san_room_rate": 24450000.0, "san_pub_f": 154175000.0, "san_pub_m": 126225000.0,
        "fl_ht_rate": {"Type1": 350000.0, "Type2": 200000.0},
        "fl_vinyl_rate": {"Type1": 0.0, "Type2": 0.0},
        "fl_marmer_rate": {"Type1": 0.0, "Type2": 0.0},
        "facade_precast_pct": 0.0, "facade_window_pct": 0.0, "facade_double_pct": 0.0,
        "fl_ht_pct": 0.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 0.0,
        "san_room_qty": 1.0, "railing_qty": 0.0,
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 1250000.0, "facade_double_rate": 1000000.0,
        "railing_rate": 2000000.0, "skylight_rate": 4500000.0,
        "san_dis": 24481500.0, "san_mushola": 36500000.0, "ext_land": 1024897.0,
        "fac_pub": 0.0, "fac_res": 1715946.0, "fac_proj": 2000000000.0,
        "cons": 168148.6486
    },
    "Podium Village": {
        "arch_base": 1517450.0,
        "mep": 3142000.0,
        "utility": 45249.0,
        "door_wood": 4500000.0, "door_steel": 6750000.0, "door_glass": 1000000.0,
        "hw_wood": 8000000.0, "hw_steel": 1900000.0, "lobby": 5000000.0, "gondola": 1500000000.0,
        "carpet": 0.0, "glass": 0.0, "ffe": 0.0, "misc": 5250000000.0, "kitchen": 0.0,
        "san_room_rate": 62050000.0, "san_pub_f": 154175000.0, "san_pub_m": 126225000.0,
        "fl_ht_rate": {"Type1": 350000.0, "Type2": 200000.0},
        "fl_vinyl_rate": {"Type1": 0.0, "Type2": 0.0},
        "fl_marmer_rate": {"Type1": 0.0, "Type2": 0.0},
        "facade_precast_pct": 0.0, "facade_window_pct": 0.0, "facade_double_pct": 0.0,
        "fl_ht_pct": 0.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 0.0,
        "san_room_qty": 1.0, "railing_qty": 0.0,
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 2400000.0, "facade_double_rate": 1000000.0,
        "railing_rate": 1100000.0, "skylight_rate": 4500000.0,
        "san_dis": 62050000.0, "san_mushola": 0.0, "ext_land": 416735.0,
        "fac_pub": 0.0, "fac_res": 100897.0, "fac_proj": 2000000000.0,
        "cons": 173505.7655
    },
    "Parking2": {
        "arch_base": 1040000.0,
        "mep": 900000.0,
        "utility": 0.0,
        "door_wood": 0.0, "door_steel": 0.0, "door_glass": 0.0,
        "hw_wood": 0.0, "hw_steel": 0.0, "lobby": 0.0, "gondola": 0.0,
        "carpet": 0.0, "glass": 0.0, "ffe": 0.0, "misc": 0.0, "kitchen": 0.0,
        "san_room_rate": 0.0, "san_pub_f": 0.0, "san_pub_m": 0.0,
        "fl_ht_rate": {"Type1": 0.0, "Type2": 0.0},
        "fl_vinyl_rate": {"Type1": 0.0, "Type2": 0.0},
        "fl_marmer_rate": {"Type1": 0.0, "Type2": 0.0},
        "facade_precast_pct": 0.0, "facade_window_pct": 0.0, "facade_double_pct": 0.0,
        "fl_ht_pct": 0.0, "fl_vinyl_pct": 0.0, "fl_marmer_pct": 0.0,
        "san_room_qty": 1.0, "railing_qty": 0.0,
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "facade_precast_rate": 0.0, "facade_window_rate": 0.0, "facade_double_rate": 0.0,
        "railing_rate": 0.0, "skylight_rate": 0.0,
        "san_dis": 0.0, "san_mushola": 0.0, "ext_land": 0.0,
        "fac_pub": 0.0, "fac_res": 0.0, "fac_proj": 0.0,
        "cons": 52500.0
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
    types_list = ["Hotel", "Retail", "Apartment", "Parking", "Luxury Apartment", "Apartment2", "Hotel 3 Star", "Retail2", "Terrace Village", "Podium Village", "Parking2"]
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "Petunjuk",
        "1. Ukuran", "2. Persen dan Pengali",
        "3. Harga", "4. Soft Costs",
        "5. Item Tambahan", "6. Hasil",
        "7. Pembuktian",
        "Unggah & Unduh",
    ])

# --- TAB 1: PETUNJUK PEMAKAIAN ---
    with tab1:
        st.header("Keterangan:")        

        st.markdown("""
        **1. Ukuran       :** Untuk pengisian angka luas tanah, GBA, GFA, SGFA, unit kamar, dsb. (***notes:*** pengisian angka berupa qty dan bukan harga)
        
        **2. Persen       :** Untuk angka yang menggunakan rasio (Misal: rasio pekerjaan lantai proyek = 90% HT, 10% Marmer)
        
        **3. Harga        :** Untuk pengisian harga otomatis mengikuti database jenis proyek, dapat diisi manual sesuai kebutuhan.
        
        **4. Soft Costs   :** Untuk pengisian biaya jasa QS, PM, konsultan dan asuransi.
        
        **5. Tambahan     :** Untuk penambahan item khusus, ketik manual untuk nama item, qty dan harga pada tabel.
        
        **6. Hasil        :** Untuk melihat hasil perhitungan total biaya proyek, serta breakdown biaya per kategori.
        
        **7. Pembuktian   :** Untuk melihat perhitungan secara rinci.
                      
        """)
    
    with tab9:
        st.header("Upload & Download")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Import")
            uploaded_file = st.file_uploader("Upload CSV Database:", type=["csv"])

            if uploaded_file is not None:
                file_key = getattr(uploaded_file, 'file_id', uploaded_file.name)
                
                if "last_loaded_file" not in st.session_state or st.session_state.last_loaded_file != file_key:
                    try:
                        df_import = pd.read_csv(uploaded_file)
                        
                        if df_import is not None and not df_import.empty:
                            # Dictionary to hold custom item reconstruction per project found in CSV
                            # Structure: {pid: {idx: {item_data}}}
                            global_temp_custom = {}

                            # Iterate through each row in the CSV
                            for index, row in df_import.iterrows():
                                # Get Project ID from CSV or fallback to current project if missing
                                pid = str(row.get("Project_ID", curr_id)).strip()
                                key = str(row.get("Metric_Key", "")).strip()
                                val = row.get("Value", "")

                                if not key or pd.isna(val): continue 

                                # 1. Ensure the project exists in Session State
                                if pid not in st.session_state.projects:
                                    st.session_state.projects[pid] = {
                                        "name": f"Imported Project {pid}",
                                        "type": "Type1",
                                        "data": {}
                                    }
                                
                                # 2. Handle Metadata (Name/Type)
                                if key == "proj_name":
                                    st.session_state.projects[pid]["name"] = str(val)
                                elif key == "proj_type":
                                    st.session_state.projects[pid]["type"] = str(val)
                                
                                # 3. Handle Custom Inputs (Data Editor Breakdown)
                                elif key.startswith(("input_name", "input_rate", "input_qty")):
                                    if pid not in global_temp_custom:
                                        global_temp_custom[pid] = {}
                                    
                                    try:
                                        idx = int(''.join(filter(str.isdigit, key)))
                                        if idx not in global_temp_custom[pid]:
                                            global_temp_custom[pid][idx] = {"Item Description": "", "Rate (Rp)": 0.0, "Quantity": 1.0}
                                        
                                        if "name" in key:
                                            global_temp_custom[pid][idx]["Item Description"] = str(val)
                                        elif "rate" in key:
                                            global_temp_custom[pid][idx]["Rate (Rp)"] = float(val)
                                        elif "qty" in key:
                                            global_temp_custom[pid][idx]["Quantity"] = float(val)
                                    except: continue

                                # 4. Handle Standard Metrics
                                else:
                                    try:
                                        st.session_state.projects[pid]["data"][key] = float(val)
                                    except (ValueError, TypeError):
                                        st.session_state.projects[pid]["data"][key] = str(val)

                            # 5. Reconstruct 'smart_custom_costs' for all affected projects
                            for pid, items_dict in global_temp_custom.items():
                                sorted_custom = [items_dict[i] for i in sorted(items_dict.keys())]
                                st.session_state.projects[pid]["data"]["smart_custom_costs"] = sorted_custom

                            st.session_state.last_loaded_file = file_key
                            st.success(f"✅ Import Successful! Processed {len(df_import['Project_ID'].unique()) if 'Project_ID' in df_import.columns else 1} project(s).")
                            st.rerun()
                        else:
                            st.warning("⚠️ The uploaded CSV is empty.")

                    except Exception as e:
                        st.error(f"❌ Error during import: {e}")
                        
        with c2:
            st.subheader("Export")

            # --- 1. LOGIC FOR CURRENT PROJECT ONLY ---
            current_project_csv = []
            # Project Meta for current
            current_project_csv.append({"Project_ID": curr_id, "Metric_Key": "proj_name", "Value": curr_proj["name"]})
            current_project_csv.append({"Project_ID": curr_id, "Metric_Key": "proj_type", "Value": curr_proj["type"]})
            
            # Standard Metrics for current
            for k, v in st.session_state.projects[curr_id]["data"].items():
                if k not in ("smart_custom_costs", "header_info", "assumptions"):
                    current_project_csv.append({"Project_ID": curr_id, "Metric_Key": k, "Value": v})
            
            # Custom Items for current
            custom_data_curr = st.session_state.get(f"smart_custom_data_{curr_id}", {})
            for k, v in custom_data_curr.items():
                current_project_csv.append({"Project_ID": curr_id, "Metric_Key": k, "Value": v})

            df_curr = pd.DataFrame(current_project_csv)
            csv_buffer = df_curr.to_csv(index=False).encode("utf-8") # Now defined!


            # --- 2. LOGIC FOR ALL PROJECTS (GLOBAL) ---
            all_projects_csv = []
            for pid, pdata in st.session_state.projects.items():
                all_projects_csv.append({"Project_ID": pid, "Metric_Key": "proj_name", "Value": pdata["name"]})
                all_projects_csv.append({"Project_ID": pid, "Metric_Key": "proj_type", "Value": pdata["type"]})
                
                for k, v in pdata["data"].items():
                    if k not in ("smart_custom_costs", "header_info", "assumptions"):
                        all_projects_csv.append({"Project_ID": pid, "Metric_Key": k, "Value": v})
                
                custom_data_pid = st.session_state.get(f"smart_custom_data_{pid}", {})
                for k, v in custom_data_pid.items():
                    all_projects_csv.append({"Project_ID": pid, "Metric_Key": k, "Value": v})

            df_all = pd.DataFrame(all_projects_csv)
            csv_all_buffer = df_all.to_csv(index=False).encode("utf-8")


            # --- 3. DOWNLOAD BUTTONS ---
            st.write("---")
            
            # Button for Current Project
            st.download_button(
                label=f"📄 Download {curr_proj['name']}",
                data=csv_buffer,
                file_name=f"Project_{curr_id}.csv",
                mime="text/csv",
                use_container_width=True
            )

            # Button for Global Database
            st.download_button(
                label="📥 Download ALL Projects (Global)",
                data=csv_all_buffer,
                file_name="ProCalc_Global_Database.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary" 
            )

    # --- TAB 1: PROJECT METRICS ---
    with tab2:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)

        with col_m1:
            with st.expander("Ukuran Proyek", expanded=True):
                st.subheader("Ukuran")
                land_area = st.number_input("Luas Tanah (m2)", value=get_val("m_land", 0.0), step=100.0, key=f"m_land_{curr_id}")
                gba = st.number_input("GBA (m2)", value=get_val("m_gba", 0.0), step=100.0, key=f"m_gba_{curr_id}")
                gfa = st.number_input("GFA (m2)", value=get_val("m_gfa", 0.0), step=100.0, key=f"m_gfa_{curr_id}")
                sgfa = st.number_input("SGFA (m2)", value=get_val("m_sgfa", 0.0), step=100.0, key=f"m_sgfa_{curr_id}")

        with col_m2:
            with st.expander("Arsitektur", expanded=True):
                st.subheader("Interior")
                rooms = st.number_input("Ruang (unit)", help="cth. 500 unit untuk 1 proyek Apartement A", value=get_val("m_rooms", 0.0), step=1.0, key=f"m_rooms_{curr_id}")
                lobby_interior = st.number_input("Lobby Interior (m2)", help="cth. 500 m2 lobby untuk 1 proyek Apartement A", value=float(get_val("m_lobby", 0.0)), step=10.0, key=f"m_lobby_{curr_id}")
                carpet_m2 = st.number_input("Karpet (m2)", value=get_val("m_carpet", 0.0), step=10.0, key=f"m_carpet_{curr_id}")
                glass_m2 = st.number_input("Kaca (m2)", value=get_val("m_glass", 0.0), step=10.0, key=f"m_glass_{curr_id}")
                st.subheader("Eksterior")
                facade = st.number_input("Facade (m2)", value=get_val("m_facade", 0.0), step=100.0, key=f"m_facade_{curr_id}")
                gondola_unit = st.number_input("Gondola (unit)", value=get_val("m_gondola", 0.0), step=1.0, key=f"m_gondola_{curr_id}")
                skylight_area = st.number_input("Skylight (m2)", value=get_val("m_skylight", 0.0), step=10.0, key=f"m_skylight_{curr_id}")    
                st.subheader("Pintu")
                glass_door = st.number_input("Glass Door (unit)", value=get_val("m_door_g", 0.0), step=1.0, key=f"m_door_g_{curr_id}")
                wooden_door = st.number_input("Wooden Door (unit)", value=get_val("m_door_w", 0.0), step=10.0, key=f"m_door_w_{curr_id}")
                steel_door = st.number_input("Steel Door (unit)", value=get_val("m_door_s", 0.0), step=10.0, key=f"m_door_s_{curr_id}")

        with col_m3:
            with st.expander("Sanitari", expanded=True):
                st.subheader("Toilet Unit")
                san_qty_room = st.number_input("Toilet Private (unit/ruang)", help="Cth. 3 Toilet/1 Kamar (Apt)", value=get_val("r_san_qty", pt_data["san_room_qty"]), key=f"r_san_qty_{curr_type_key}")
                st.subheader("Toilet Umum")
                toilet_male = st.number_input("Toilet Umum - Pria (units)", value=get_val("m_toil_m", 0.0), step=1.0, key=f"m_toil_m_{curr_id}")
                toilet_female = st.number_input("Toilet Umum - Wanita (units)", value=get_val("m_toil_f", 0.0), step=1.0, key=f"m_toil_f_{curr_id}")
                disabled_toil = st.number_input("Toilet Difabel (units)", value=get_val("m_toil_d", 0.0), step=1.0, key=f"m_toil_d_{curr_id}")
                st.subheader("Mushola")
                mushola_unit = st.number_input("Mushola (units)", value=get_val("m_mushola", 0.0), step=1.0, key=f"m_mushola_{curr_id}")

        with col_m4:
            with st.expander("Fasilitas", expanded=True):
                st.subheader("Fasilitas")
                res_fac_m2 = st.number_input("Fasilitas Penghuni (m2)", value=get_val("m_fac_res", 0.0), step=10.0, key=f"m_fac_res_{curr_id}")
                pub_fac_m2 = st.number_input("Fasilitas Publik (m2)", value=get_val("m_fac_pub", 0.0), step=10.0, key=f"m_fac_pub_{curr_id}")
                proj_fac_u = st.number_input("Fasilitas Proyek (unit)", value=get_val("m_fac_proj", 0.0), step=1.0, key=f"m_fac_proj_{curr_id}")
                land_m2 = st.number_input("Area Lanskap (m2)", value=get_val("m_land_m2", 0.0), step=100.0, key=f"m_land_m2_{curr_id}")
                st.subheader("Miscellaneous")
                m_status = st.radio("Ada Gym/Linen?", ["Tidak", "Ada"],
                                    index=1 if get_val("misc_switch", 0) == 1 else 0,
                                    key=f"misc_sw_{curr_id}", horizontal=True)
                misc_switch = 1 if m_status == "Ada" else 0
                st.session_state.projects[curr_id]["data"]["misc_switch"] = misc_switch

    # --- TAB 2: RATIOS & MULTIPLIERS ---
    with tab3:
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            st.subheader("Facade Ratio (%)")
            facade_precast_pct = st.number_input("Precast (%)", value=get_val("r_fac_pre", pt_data["facade_precast_pct"]), step=5.0, key=f"r_fac_pre_{curr_type_key}")
            facade_window_pct = st.number_input("Window Wall (%)", value=get_val("r_fac_win", pt_data["facade_window_pct"]), step=5.0, key=f"r_fac_win_{curr_type_key}")
            facade_double_pct = st.number_input("Double Skin (%)", value=get_val("r_fac_doub", pt_data["facade_double_pct"]), step=5.0, key=f"r_fac_doub_{curr_type_key}")
            t_fac_pct = facade_precast_pct + facade_window_pct + facade_double_pct

            if t_fac_pct != 100:
                st.warning(f"⚠️ Total is **{t_fac_pct}%** (bukan 100%)")
        with col_r3:
            st.subheader("Waste & Skirting (%)")
            fl_waste = st.number_input(
                "Floor Waste", 
                value=get_val("w_floor", pt_data.get("fl_waste", 10)), # Use .get() with 1.1 as default
                key=f"w_floor{curr_type_key}"
            )        
            fl_skirt = st.number_input(
                "Dinding/Skirting (%)", 
                value=get_val("s_floor", pt_data.get("fl_skirt", 20)), 
                key=f"s_floor{curr_type_key}"
            )
            st.caption(f"Luas Lantai + Skirting + Waste: GFA: {gfa:.2f} x {1 + (fl_waste/100):.2f} x {1 + (fl_skirt/100):.2f} = {gfa*(1 + (fl_waste/100))*(1 + (fl_skirt/100)):.2f} m2")

            f_mult = fl_waste * fl_skirt
        
        with col_r2:
            st.subheader("Flooring Ratio (%)")
            fl_ht_pct = st.number_input("HT/Ceramic Tile (%)", value=get_val("r_fl_ht", pt_data["fl_ht_pct"]), step=5.0, key=f"r_fl_ht_{curr_type_key}")
            fl_vinyl_pct = st.number_input("Vinyl (%)", value=get_val("r_fl_vin", pt_data["fl_vinyl_pct"]), step=5.0, key=f"r_fl_vin_{curr_type_key}")
            fl_marmer_pct = st.number_input("Marmer (%)", value=get_val("r_fl_mar", pt_data["fl_marmer_pct"]), step=5.0, key=f"r_fl_mar_{curr_type_key}")
            t_fl_pct = fl_ht_pct + fl_vinyl_pct + fl_marmer_pct

            if t_fl_pct != 100:
                st.warning(f"⚠️ Total is **{t_fl_pct}%** (bukan 100%)")

        with col_r4:
            st.subheader("Railing (m')")
            railing_qty = st.number_input("Railing Length (m'/room)", value=get_val("r_rail_qty", pt_data["railing_qty"]), step=1.0, key=f"r_rail_qty_{curr_type_key}")
            st.caption(f"Total: {railing_qty:.0f} m x {rooms:.0f} unit = {railing_qty * rooms:.0f} m'")

    # --- TAB 3: UNIT RATES ---
    with tab4:
        with st.expander("Harga Fondasi & Struktur", expanded=True):
            c1, c2, c3 = st.columns(3)
            struc_earth = c1.number_input("Earthwork Rate (Rp)", value=get_val("u_earth", pt_data["struc_earth"]), key=f"u_earth_{curr_type_key}")
            struc_found = c2.number_input("Foundation Rate (Rp)", value=get_val("u_found", pt_data["struc_found"]), key=f"u_found_{curr_type_key}")
            struc_work = c3.number_input("Structural Work Rate (Rp)", value=get_val("u_struc", pt_data["struc_work"]), key=f"u_struc_{curr_type_key}")
            #caption
            c1.caption(f"""Hitungan: Rp {struc_earth:,.0f} x GBA: {gba:,.0f} m2  \n  Total Earthwork: Rp {struc_earth * gba:,.0f}  \n  Terbilang: {n2w(struc_earth * gba)}""")
            c2.caption(f"""Hitungan: Rp {struc_found:,.0f} x GBA: {gba:,.0f} m2  \n  Total Foundation: Rp {struc_found * gba:,.0f}  \n  Terbilang: {n2w(struc_found * gba)}""")
            c3.caption(f"""Hitungan: Rp {struc_work:,.0f} x GBA: {gba:,.0f} m2  \n  Total Structural Work: Rp {struc_work * gba:,.0f}  \n  Terbilang: {n2w(struc_work * gba)}""")

        with st.expander("Arsitektur & Fasad"):
            c1, c2 = st.columns(2)
            arch_base = c1.number_input("Architecture Base (Rp)", value=get_val("u_arch", pt_data["arch_base"]), key=f"u_arch_{curr_type_key}")
            lobby_rate = c2.number_input("Lobby Interior Rate (Rp)", value=get_val("u_lobby", pt_data["lobby"]), key=f"u_lobby_{curr_type_key}")
            c3, c4, c5 = st.columns(3)
            fac_precast_rate = c3.number_input("Precast Rate (Rp)", value=get_val("u_f_pre", pt_data["facade_precast_rate"]), key=f"u_f_pre_{curr_type_key}")
            fac_window_rate = c4.number_input("Window Wall Rate (Rp)", value=get_val("u_f_win", pt_data["facade_window_rate"]), key=f"u_f_win_{curr_type_key}")
            fac_double_rate = c5.number_input("Double Skin Rate (Rp)", value=get_val("u_f_doub", pt_data["facade_double_rate"]), key=f"u_f_doub_{curr_type_key}")
            c1.caption(f"""Hitungan: Rp {arch_base:,.0f} x GFA: {gfa:,.0f} m2  \n  Total Architecture Base: Rp {arch_base * gfa:,.0f}  \n  Terbilang: {n2w(arch_base * gfa)}""")
            c2.caption(f"""Hitungan: Rp {lobby_rate:,.0f} x Lobby Interior: {lobby_interior:,.0f} m2  \n  Total Lobby Interior: Rp {lobby_rate * lobby_interior:,.0f}  \n  Terbilang: {n2w(lobby_rate * lobby_interior)}""")
            c3.caption(f"""Hitungan: Rp {fac_precast_rate:,.0f} x Facade: {facade:,.0f} m2 x {facade_precast_pct}%  \n  Total Precast: Rp {fac_precast_rate * facade * (facade_precast_pct/100):,.0f}  \n  Terbilang: {n2w(fac_precast_rate * facade * (facade_precast_pct/100))}""")
            c4.caption(f"""Hitungan: Rp {fac_window_rate:,.0f} x Facade: {facade:,.0f} m2 x {facade_window_pct}%  \n  Total Window Wall: Rp {fac_window_rate * facade * (facade_window_pct/100):,.0f}  \n  Terbilang: {n2w(fac_window_rate * facade * (facade_window_pct/100))}""")
            c5.caption(f"""Hitungan: Rp {fac_double_rate:,.0f} x Facade: {facade:,.0f} m2 x {facade_double_pct}%  \n  Total Double Skin: Rp {fac_double_rate * facade * (facade_double_pct/100):,.0f}  \n  Terbilang: {n2w(fac_double_rate * facade * (facade_double_pct/100))}""")
        with st.expander("Pintu dan Hardware"):
            c1, c2, c3 = st.columns(3)
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

        with st.expander("Sanitari"):
            c1, c2 = st.columns(2)
            san_room_rate = c1.number_input("Typical Unit Sanitary Rate (Rp)", value=get_val("u_s_room", pt_data["san_room_rate"]), key=f"u_s_room_{curr_type_key}")
            c1.caption(f"""Hitungan: Rp {san_room_rate:,.0f} x {rooms:,.0f} Rooms x {san_qty_room} Units / Room  \n  Total Private Bathroom: Rp {rooms * san_qty_room * san_room_rate:,.0f}  \n  Terbilang: {n2w(rooms * san_qty_room * san_room_rate)}""")
            san_pub_m = c2.number_input("Public Toilet Male Rate (Rp)", value=get_val("u_s_pub_m", pt_data["san_pub_m"]), key=f"u_s_pub_m_{curr_type_key}")
            c2.caption(f"""Hitungan: Rp {san_pub_m:,.0f} x {toilet_male:,.0f} Units  \n  Total Public Toilet Male: Rp {toilet_male * san_pub_m:,.0f}  \n  Terbilang: {n2w(toilet_male * san_pub_m)}""")
            san_pub_f = c2.number_input("Public Toilet Female Rate (Rp)", value=get_val("u_s_pub_f", pt_data["san_pub_f"]), key=f"u_s_pub_f_{curr_type_key}")
            c2.caption(f"""Hitungan: Rp {san_pub_f:,.0f} x {toilet_female:,.0f} Units  \n  Total Public Toilet Female: Rp {toilet_female * san_pub_f:,.0f}  \n  Terbilang: {n2w(toilet_female * san_pub_f)}""")
            san_dis = c1.number_input("Disabled Toilet Rate (Rp)", value=get_val("u_s_dis", pt_data["san_dis"]), key=f"u_s_dis_{curr_type_key}")
            c1.caption(f"""Hitungan: Rp {san_dis:,.0f} x {disabled_toil:,.0f} Units  \n  Total Toilet Difabel: Rp {disabled_toil * san_dis:,.0f}  \n  Terbilang: {n2w(disabled_toil * san_dis)}""")
            san_mushola = c1.number_input("Mushola Rate (Rp)", value=get_val("u_s_mushola", pt_data["san_mushola"]), key=f"u_s_mushola_{curr_type_key}")
            c1.caption(f"""Hitungan: Rp {san_mushola:,.0f} x {mushola_unit:,.0f} Units  \n  Total Mushola: Rp {mushola_unit * san_mushola:,.0f}  \n  Terbilang: {n2w(mushola_unit * san_mushola)}""")
        
        with st.expander("Lantai, Finishing, dan Interior"):
            st.subheader("Harga ")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.radio("Spek HT", ["Type1", "Type2"],
                    key=f"temp_spec_ht_{curr_type_key}",
                    horizontal=True,
                    on_change=update_price, args=("ht", "fl_ht_rate"))
                fl_ht_rate = st.number_input("HT Rate (Rp)",
                                            value=get_val("u_fl_ht", pt_data["fl_ht_rate"]["Type1"]),
                                            key=f"u_fl_ht_{curr_type_key}")
                c1.caption(f"""Hitungan: {fl_ht_pct}% of GFA x Rp {fl_ht_rate:,.0f} x {gfa:,.0f} m2 x 1.1 x 1.2  \n  Total HT: Rp {gfa * (fl_ht_pct / 100) * fl_ht_rate * 1.32:,.0f}  \n  Terbilang: {n2w(gfa * (fl_ht_pct / 100) * fl_ht_rate * 1.32)}""")

            with c2:
                st.radio("Spek Vinyl", ["Type1", "Type2"],
                    key=f"temp_spec_vin_{curr_type_key}",
                    horizontal=True,
                    on_change=update_price, args=("vin", "fl_vinyl_rate"))
                fl_vinyl_rate = st.number_input("Vinyl Rate (Rp)",
                                                value=get_val("u_fl_vin", pt_data["fl_vinyl_rate"]["Type1"]),
                                                key=f"u_fl_vin_{curr_type_key}")
                c2.caption(f"""Hitungan: {fl_vinyl_pct}% of GFA x Rp {fl_vinyl_rate:,.0f} x {gfa:,.0f} m2 x 1.1 x 1.2  \n  Total Vinyl: Rp {gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * 1.32:,.0f}  \n  Terbilang: {n2w(gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * 1.32)}""")
            
            with c3:
                st.radio("Spek Marmer", ["Type1", "Type2"],
                    key=f"temp_spec_mar_{curr_type_key}",
                    horizontal=True,
                    on_change=update_price, args=("mar", "fl_marmer_rate"))
                fl_marmer_rate = st.number_input("Marmer Rate (Rp)",
                                                value=get_val("u_fl_mar", pt_data["fl_marmer_rate"]["Type1"]),
                                                key=f"u_fl_mar_{curr_type_key}")
                c3.caption(f"""Hitungan: {fl_marmer_pct}% of GFA x Rp {fl_marmer_rate:,.0f} x {gfa:,.0f} m2 x 1.1 x 1.2  \n  Total Marmer: Rp {gfa * (fl_marmer_pct / 100) * fl_marmer_rate * 1.32:,.0f}  \n  Terbilang: {n2w(gfa * (fl_marmer_pct / 100) * fl_marmer_rate * 1.32)}""")
                
            carpet_rate = c1.number_input("Carpet Rate (Rp)", value=get_val("u_carpet", pt_data["carpet"]), key=f"u_carpet_{curr_type_key}")
            c1.caption(f"""Hitungan: {carpet_m2:,.0f} m2 x Rp {carpet_rate:,.0f}  \n  Total Carpet Work: Rp {carpet_m2 * carpet_rate:,.0f}  \n  Terbilang: {n2w(carpet_m2 * carpet_rate)}""")
            glass_rate = c2.number_input("Glass Work Rate (Rp)", value=get_val("u_glass", pt_data["glass"]), key=f"u_glass_{curr_type_key}")
            c2.caption(f"""Hitungan: {glass_m2:,.0f} m2 x Rp {glass_rate:,.0f}  \n  Total Glass Work: Rp {glass_m2 * glass_rate:,.0f}  \n  Terbilang: {n2w(glass_m2 * glass_rate)}""")            
            skylight_rate = c3.number_input("Skylight Rate (Rp)", value=get_val("u_sky", pt_data["skylight_rate"]), key=f"u_sky_{curr_type_key}")
            c3.caption(f"""Hitungan: {skylight_area:,.0f} m2 Total x Rp {skylight_rate:,.0f}  \n  Total Skylight Work: Rp {skylight_area * skylight_rate:,.0f}  \n  Terbilang: {n2w(skylight_area * skylight_rate)}""")
            gondola_rate = c1.number_input("Gondola Rate (Rp)", value=get_val("u_gondola", pt_data["gondola"]), key=f"u_gondola_{curr_type_key}")
            c1.caption(f"""Hitungan: {gondola_unit:,.0f} Units x Rp {gondola_rate:,.0f}  \n  Total Gondola: Rp {gondola_unit * gondola_rate:,.0f}  \n  Terbilang: {n2w(gondola_unit * gondola_rate)}""")
            railing_rate = c2.number_input("Railing Rate (Rp)", value=get_val("u_rail", pt_data["railing_rate"]), key=f"u_rail_{curr_type_key}")
            c2.caption(f"""Hitungan: {rooms * railing_qty:,.0f} m' Total x Rp {railing_rate:,.0f}  \n  Total Railing Work: Rp {rooms * railing_qty * railing_rate:,.0f}  \n  Terbilang: {n2w(rooms * railing_qty * railing_rate)}""")

        with st.expander("MEP, Dapur dan FF&E"):
            c1, c2 = st.columns(2)
            mep_rate = c1.number_input("MEP Works (Rp)", value=get_val("u_mep", pt_data["mep"]), key=f"u_mep_{curr_type_key}")
            c1.caption(f"""Hitungan: {gba:,.0f} m2 x Rp {mep_rate:,.0f}  \n  Total MEP Works: Rp {gba * mep_rate:,.0f}  \n  Terbilang: {n2w(gba * mep_rate)}""")
            utility_rate = c2.number_input("Utility Connection (Rp)", value=get_val("u_util", pt_data["utility"]), key=f"u_util_{curr_type_key}")
            c2.caption(f"""Hitungan: {gba:,.0f} m2 x Rp {utility_rate:,.0f}  \n  Total Utility Connection: Rp {gba * utility_rate:,.0f}  \n  Terbilang: {n2w(gba * utility_rate)}""")

            ffe_rate = c1.number_input("FF&E (Rp)", value=get_val("u_ffe", pt_data["ffe"]), key=f"u_ffe_{curr_type_key}")
            c1.caption(f"""Hitungan: {rooms:,.0f} Rooms x Rp {ffe_rate:,.0f}  \n  Total FF&E: Rp {rooms * ffe_rate:,.0f}  \n  Terbilang: {n2w(rooms * ffe_rate)}""")

            kitchen_rate = c2.number_input("Kitchen Equipment (Rp)", value=get_val("u_kit", pt_data["kitchen"]), key=f"u_kit_{curr_type_key}")
            c2.caption(f"""Hitungan: {rooms:,.0f} Rooms x Rp {kitchen_rate:,.0f}  \n  Total Kitchen Equipment: Rp {rooms * kitchen_rate:,.0f}  \n  Terbilang: {n2w(rooms * kitchen_rate)}""")

            misc_rate = c1.number_input("Misc (Linen/Gym Equipment) (Rp)", value=get_val("u_misc", pt_data["misc"]), key=f"u_misc_{curr_type_key}")
            c1.caption(f"""Hitungan: Rp {misc_rate if misc_switch else 0:,.0f}  \n  Total Misc. Costs: Rp {misc_rate * misc_switch:,.0f}  \n  Terbilang: {n2w(misc_rate * misc_switch)}""")
        
        with st.expander("External & Facility Rates"):
            c1, c2 = st.columns(2)
            ext_land_rate = c1.number_input("External Works (Landscape) (Rp)", value=get_val("u_ext", pt_data["ext_land"]), key=f"u_ext_{curr_type_key}")
            fac_pub_rate = c2.number_input("Public Facilities (Rp)", value=get_val("u_fac_p", pt_data["fac_pub"]), key=f"u_fac_p_{curr_type_key}")
            c1.caption(f"""Hitungan: {land_m2:,.0f} m2 x Rp {ext_land_rate:,.0f}  \n  Total External Works: Rp {land_m2 * ext_land_rate:,.0f}  \n  Terbilang: {n2w(land_m2 * ext_land_rate)}""")
            c2.caption(f"""Hitungan: {pub_fac_m2:,.0f} m2 x Rp {fac_pub_rate:,.0f}  \n  Total Public Facilities: Rp {pub_fac_m2 * fac_pub_rate:,.0f}  \n  Terbilang: {n2w(pub_fac_m2 * fac_pub_rate)}""")
            fac_res_rate = c1.number_input("Resident Facilities (Rp)", value=get_val("u_fac_r", pt_data["fac_res"]), key=f"u_fac_r_{curr_type_key}")
            fac_proj_rate = c2.number_input("Project Facilities (Rp)", value=get_val("u_fac_pr", pt_data["fac_proj"]), key=f"u_fac_pr_{curr_type_key}")
            c1.caption(f"""Hitungan: GFA: {gfa:,.0f} m2 x Rp {fac_res_rate:,.0f}  \n  Total Resident Facilities: Rp {gfa * fac_res_rate:,.0f}  \n  Terbilang: {n2w(gfa * fac_res_rate)}""")
            c2.caption(f"""Hitungan: {proj_fac_u:,.0f} Units x Rp {fac_proj_rate:,.0f}  \n  Total Project Facilities: Rp {proj_fac_u * fac_proj_rate:,.0f}  \n  Terbilang: {n2w(proj_fac_u * fac_proj_rate)}""")

    # --- TAB 4: SOFT COSTS ---
    with tab5:
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
            with st.expander("Lainnya", expanded=True):
                consultancy_rate = st.number_input("Biaya Konsultan (Rp) per m2 GFA", help="Biaya konsultan per m2 GFA", value=get_val("sc_cons", pt_data["cons"]), key=f"sc_cons_{curr_type_key}")
                st.caption(f"""Hitungan: {gfa:,.0f} m2 x Rp {consultancy_rate:,.0f}  \n  Total Consultancy Fee: Rp {gfa * consultancy_rate:,.0f}  \n  Terbilang: {n2w(gfa * consultancy_rate)}""")
                insurance_pct = st.number_input("Insurance (%)", help="Persentase premi asuransi", value=get_val("sc_ins", 0.12), step=0.01, key=f"sc_ins_{curr_id}")
    
    # --- TAB 5: CUSTOM ITEMS ---
    with tab6:
        st.subheader("Item Tambahan")

        default_smart_cc = [{"Item Description": "", "Rate (Rp)": 0.0, "Quantity": 1.0}]
        current_smart_cc = get_val("smart_custom_costs", default_smart_cc)

        edited_smart_cc = st.data_editor(
            pd.DataFrame(current_smart_cc),
            num_rows="dynamic",
            key=f"edit_smart_cc_{curr_id}",
            column_config={
                "Quantity": st.column_config.NumberColumn(
                    "Quantity",
                    min_value=0,
                    default=1.0,
                    format="%.2f"
                )
            },
            use_container_width=True
        )

        smart_custom_costs = 0.0
        
        # New: List to store breakdown strings
        smart_custom_inputs = {}
        smart_custom_costs = 0.0
        breakdown_details = []

        for index, row in edited_smart_cc.iterrows():
            # Create a 1-based suffix for your keys (1, 2, 3...)
            suffix = index + 1
            
            desc = row.get("Item Description", "")
            rate = float(row.get("Rate (Rp)", 0.0))
            qty = float(row.get("Quantity", 1.0))
            
            # Store individual keys as requested
            smart_custom_inputs[f"input_name{suffix}"] = desc
            smart_custom_inputs[f"input_rate{suffix}"] = rate
            smart_custom_inputs[f"input_qty{suffix}"] = qty
            
            # Keep the total for the UI/Summary
            item_total = rate * qty
            smart_custom_costs += item_total

            if rate > 0:
                calc_str = f"**{desc}**: Rp {rate:,.2f} × {qty} qty = **Rp {item_total:,.2f}**"
                breakdown_details.append(calc_str)

        # Save this dictionary into your session state / get_val system
        # This allows you to export it to PROJECT_DATABASE later
        st.session_state[f"smart_custom_data_{curr_id}"] = smart_custom_inputs

        st.markdown("---")
        st.markdown(f"### Total Harga Item Custom: Rp {smart_custom_costs:,.2f}")

    # --- LIVE AUTO-CALCULATIONS ---
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
    f_mult = (1 + (fl_waste/100)) * (1 + (fl_skirt/100))
    t_ht      = gfa * (fl_ht_pct / 100) * fl_ht_rate * f_mult
    t_vinyl   = gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * f_mult
    t_marmer  = gfa * (fl_marmer_pct / 100) * fl_marmer_rate * f_mult
    t_carpet     = carpet_m2 * carpet_rate
    t_glass_work = glass_m2 * glass_rate
    t_ffe        = rooms * ffe_rate
    t_misc       = misc_rate * misc_switch
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
        t_marmer, t_carpet, t_glass_work, t_ffe, t_misc, t_mep, t_utility,
        t_railing, t_skylight, t_external, t_pub_fac, t_res_fac, t_proj_fac,
        smart_custom_costs
    ])

    t_preliminary = (construction_subtotal) * 0.05
    t_contingency = (construction_subtotal + t_preliminary) * 0.03
    grand_total_hc = construction_subtotal + t_preliminary + t_contingency

    t_consultancy = gfa * consultancy_rate
    t_qs = qs_months * qs_rate
    t_pm = pm_months * pm_rate
    t_insurance = (grand_total_hc) * (insurance_pct / 100.0)

    total_soft_cost = t_consultancy + t_qs + t_pm + t_insurance
    grand_total_project = grand_total_hc + total_soft_cost

    group_earth = t_earth 
    group_found = t_found 
    group_struc = t_struc
    
    group_facade = t_precast + t_window + t_double
    group_sanitary = t_unit_san + t_t_male + t_t_female + t_t_dis + t_mushola
    group_floor =  t_ht + t_vinyl + t_marmer 
    group_door = t_w_door + t_g_door + t_s_door + t_hw_w + t_hw_s
    group_arch = (t_arch_base + + t_lobby + t_carpet + t_gondola 
                  + t_glass_work + t_kitchen  + t_railing + t_skylight 
                  + group_facade + group_sanitary + group_floor + group_door
                  + smart_custom_costs)
    
    group_ffe = t_ffe + t_misc 
    group_mep = t_mep 
    group_utility = t_utility
    group_ext = t_external
    group_misc = t_pub_fac + t_res_fac + t_proj_fac
    group_prelim = t_preliminary
    group_conting = t_contingency
    group_soft_cost = total_soft_cost
    group_hard_cost = grand_total_hc
    group_total = total_soft_cost + grand_total_hc

    # --- TAB 6: RESULTS ---

    with tab7:
        tab1, tab2, tab3 = st.tabs([
        "Hasil",
        "Tabel", "Chart",
        ])
        
        with tab1:
            box_base = "margin-bottom: 12px; padding: 8px; border-radius: 5px; background-color: #FFFFFF; border: 1px solid #E0E0E0;"
            label_style = "font-size: 12px; color: #666666; font-weight: bold;"
            val_style = "font-size: 14px; font-weight: bold; color: #000000; margin-top: 4px;"
            with st.expander("Detail Hard Cost", expanded=False):
                cs1, cs2, cs3, cs4, cs5, cs6 = st.columns(6)

                # 1. Preliminary (Army Green - Start)
                cs1.markdown(f"""<div style="{box_base} border-left: 5px solid #CDDC39;">
                    <div style="{label_style}">Preliminary</div>
                    <div style="{val_style}">{n2w(group_prelim)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_prelim:,.0f}</div>
                </div>""", unsafe_allow_html=True)

                # 2. Earthwork (Lime)
                cs2.markdown(f"""<div style="{box_base} border-left: 5px solid #8BC34A;">
                    <div style="{label_style}">Earthwork</div>
                    <div style="{val_style}">{n2w(group_earth)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_earth:,.0f}</div>
                </div>""", unsafe_allow_html=True)

                # 3. Utility (Sage Green)
                cs3.markdown(f"""<div style="{box_base} border-left: 5px solid #4CAF50;">
                    <div style="{label_style}">Utility</div>
                    <div style="{val_style}">{n2w(group_utility)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_utility:,.0f}</div>
                </div>""", unsafe_allow_html=True)

                # 4. Foundation (Soft Green)
                cs4.markdown(f"""<div style="{box_base} border-left: 5px solid #689F38;">
                    <div style="{label_style}">Foundation</div>
                    <div style="{val_style}">{n2w(group_found)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_found:,.0f}</div>
                </div>""", unsafe_allow_html=True)

                # 5. Structural (Success Green)
                cs5.markdown(f"""<div style="{box_base} border-left: 5px solid #388E3C;">
                    <div style="{label_style}">Structural</div>
                    <div style="{val_style}">{n2w(group_struc)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_struc:,.0f}</div>
                </div>""", unsafe_allow_html=True)

                # 6. External Works (Olive)
                cs6.markdown(f"""<div style="{box_base} border-left: 5px solid #254E18;">
                    <div style="{label_style}">External Works</div>
                    <div style="{val_style}">{n2w(group_ext)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_ext:,.0f}</div>
                </div>""", unsafe_allow_html=True)


                # --- ROW 2: ct1 to ct6 ---
                ct1, ct2, ct3, ct4, ct5, ct6 = st.columns(6)

                # 7. Architecture (Medium Green)
                ct2.markdown(f"""<div style="{box_base} border-left: 5px solid #9CCC65;">
                    <div style="{label_style}">Architecture</div>
                    <div style="{val_style}">{n2w(group_arch)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_arch:,.0f}</div>
                </div>""", unsafe_allow_html=True)

                # 8. Miscellaneous (Dark Olive)
                ct3.markdown(f"""<div style="{box_base} border-left: 5px solid #558B2F;">
                    <div style="{label_style}">Miscellaneous</div>
                    <div style="{val_style}">{n2w(group_misc)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_misc:,.0f}</div>
                </div>""", unsafe_allow_html=True)

                # 9. FF & E (Dark Green)
                ct4.markdown(f"""<div style="{box_base} border-left: 5px solid #2E7D32;">
                    <div style="{label_style}">FF & E</div>
                    <div style="{val_style}">{n2w(group_ffe)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_ffe:,.0f}</div>
                </div>""", unsafe_allow_html=True)

                # 10. Contingency (Deep Army)
                ct6.markdown(f"""<div style="{box_base} border-left: 5px solid #1B5E20;">
                    <div style="{label_style}">Contingency</div>
                    <div style="{val_style}">{n2w(group_conting)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_conting:,.0f}</div>
                </div>""", unsafe_allow_html=True)

                # 11. MEP Works (Forest Green)
                ct5.markdown(f"""<div style="{box_base} border-left: 5px solid #33691E;">
                    <div style="{label_style}">MEP Works</div>
                    <div style="{val_style}">{n2w(group_mep)}</div>
                    <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {group_mep:,.0f}</div>
                </div>""", unsafe_allow_html=True)
            
    # --- TOTALS SUMMARY ---
            c1, c2 = st.columns(2)

            # Common styles
            summary_base = "margin-bottom: 20px; padding: 15px; border-radius: 8px; background-color: #FFFFFF; border: 1px solid #E0E0E0;"
            summary_label = "font-size: 16px; color: #666666; font-weight: bold;"
            summary_val = "font-size: 24px; font-weight: bold; color: #000000; line-height: 1.2; margin-top: 5px;"
            summary_n2w = "font-size: 14px; color: #888888; font-weight: normal; margin-top: 5px;"

            # Hard Cost - Starting with Lime Accent
            c1.markdown(f"""
                <div style="{summary_base} border-left: 8px solid #CDDC39; background-color: #F9F9F0">
                    <div style="{summary_label}">Total Hard Cost</div>
                    <div style="{summary_val}">Rp {grand_total_hc:,.2f}</div>
                    <div style="{summary_n2w}">Terbilang: {n2w(grand_total_hc)} Rupiah</div>
                </div>
            """, unsafe_allow_html=True)


            # Soft Cost - Moving to Success Green Accent
            c2.markdown(f"""
                <div style="{summary_base} border-left: 8px solid #4CAF50; background-color: #F1F8F1">
                    <div style="{summary_label}">Total Soft Cost</div>
                    <div style="{summary_val}">Rp {total_soft_cost:,.2f}</div>
                    <div style="{summary_n2w}">Terbilang: {n2w(total_soft_cost)} Rupiah</div>
                </div>
            """, unsafe_allow_html=True)

            # Grand Total - Final Army Green Accent (Thicker border and larger font)
            st.markdown(f"""
                <div style="{summary_base} border-left: 12px solid #254E18; padding: 20px; background-color: #F5F7F5">
                    <div style="font-size: 18px; color: #666666; font-weight: bold;">Project Cost</div>
                    <div style="font-size: clamp(24px, 4vw, 30px); font-weight: bold; color: #000000; line-height: 1.2; margin-top: 10px;">
                        Rp {grand_total_project:,.2f}
                    </div>
                    <div style="font-size: 16px; color: #888888; margin-top: 8px;">
                        Terbilang: {n2w(grand_total_project)} Rupiah
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
    with tab2:
        # 1. Initialize the toggle state if it doesn't exist
        if 'show_details' not in st.session_state:
            st.session_state.show_details = True

        # 2. Add the Toggle Button
        label = "Hide Details" if st.session_state.show_details else "Show Details"
        if st.button(label):
            st.session_state.show_details = not st.session_state.show_details
            st.rerun()

        # 3. Define the full dataset
        raw_amounts = [
            t_preliminary, t_earth, t_found, 
            t_struc, group_arch, t_arch_base,
            t_precast, t_window, t_double, 
            t_w_door, t_g_door, t_s_door, 
            t_lobby, t_gondola, t_unit_san, 
            t_t_male, t_t_female, t_t_dis, 
            t_mushola, t_kitchen, t_hw_w,
            t_hw_s, t_ht, t_vinyl, 
            t_marmer, t_carpet, t_railing, 
            t_skylight, t_glass_work, smart_custom_costs,
            group_ffe, t_ffe, t_misc, 
            t_mep, t_utility,
            t_external, group_misc, t_pub_fac, 
            t_res_fac, t_proj_fac,
            t_contingency,
            t_consultancy, t_qs, 
            t_pm, t_insurance
        ]

        original_descriptions = [
            "1. Preliminary Works", "2. Earthwork", "3. Foundation", 
            "4. Structural Work", "5. Total Architecture", "5.1 Basic Architecture",
            "5.2 Facade - Precast", "5.3 Facade - Window Wall", "5.4 Facade - Double Skin", 
            "5.5 Wooden Doors", "5.6 Glass Doors", "5.7 Steel Doors", 
            "5.8 Lobby Interior", "5.9 Gondola",  "5.10 Typical Unit Sanitary", 
            "5.11 Public Toilet Male", "5.12 Public Toilet Female", "5.13. Disabled Toilet", 
            "5.14 Mushola", "5.15 Kitchen Equipment", "5.16 Hardware Pintu Kayu",
            "5.17 Hardware Pintu Besi", "5.18 HT/Ceramic Tile", "5.19 Vinyl Flooring", 
            "5.20 Marmer Flooring", "5.21 Carpet Work", "5.22 Railing Work", 
            "5.23 Skylight Work", "5.24. Glass Work", "5.25 Custom Item (Architecture)",
            "6. Total FF&E", "6.1 FF&E", "6.2 Misc. (Linen/Gym)", 
            "7. MEP Works", "8. Utility Connection",
            "9. External Works", "10. Miscellanous/Facility", "10.1. Public Facilities", 
            "10.2. Resident Facilities", "10.3 Project Facilities",
            "11. Contingencies", 
            "1. Consultancy Fee", "2. Quantity Surveyor", 
            "3. Project Management", "4. Insurance Coverage"
        ]

        # 4. Filter and Indent Logic
        filtered_data = []
        major_numbers = [f"{i}. " for i in range(1, 12)]

        for desc, amt in zip(original_descriptions, raw_amounts):
            is_major = any(desc.startswith(num) for num in major_numbers)
            
            if st.session_state.show_details:
                # If showing details, indent sub-items
                display_desc = desc if is_major else f"    {desc}"
                filtered_data.append({"Description": display_desc, "Amount": amt})
            else:
                # If hiding details, only append major items
                if is_major:
                    filtered_data.append({"Description": desc, "Amount": amt})

        # 5. Create DataFrame
        df = pd.DataFrame(filtered_data)
        df["Amount"] = df["Amount"].apply(lambda x: f"Rp {x:,.2f}")

        # 6. Styling Logic (Bold Major Items)
        def style_major_rows(row):
            clean_desc = row["Description"].strip()
            is_major = any(clean_desc.startswith(num) for num in major_numbers)
            return ['font-weight: bold' if is_major else '' for _ in row]

        # 7. Display
        styled_df = df.style.apply(style_major_rows, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
        with tab3:
            st.subheader("Total Project Cost Breakdown")

            # 1. Define the dictionary first
            detailed_items = {
                "Item": [
                    "Preliminary", "Earthwork", "Foundation", "Structural", 
                    "Architecture Work", "FF&E", "MEP Works", "Utility",
                    "External/Landscape", "Misc/Facility", "Contingency",
                    "Soft Cost/Consultancy & Insurance"
                ],
                "Amount": [
                    group_prelim, group_earth, group_found, group_struc, 
                    group_arch, group_ffe, group_mep, group_utility, 
                    group_ext, group_misc,
                    group_conting, group_soft_cost
                ],
                # Adding 'Type' helps with color coding the chart
                "Type": ["Hard Cost"]*11 + ["Soft Cost"]*1 
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
        "w_floor": fl_waste, "s_floor" :fl_skirt,
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

    with tab8:
        st.markdown("This Page is Intentionally Left Blank")
        

# def show_portfolio_summary():
#     import io
#     import xlsxwriter
#     import re
#     from datetime import date

#     tab_summary, tab_detailed = st.tabs(["FAD", "Rekap"])
    
#     with tab_summary:
#             st.subheader("Tabel FAD")
#             active_id = st.session_state.current_proj_id
#             today_str = date.today().strftime("%d-%m-%Y")

#             if "header_info" not in st.session_state.projects[active_id]["data"]:
#                 st.session_state.projects[active_id]["data"]["header_info"] = {
#                     "rev_no": "0", "updated": today_str, "created": today_str
#                 }

#             with st.expander("Edit Header & Assumptions", expanded=False):
#                 h_col1, h_col2, h_col3 = st.columns(3)
#                 rev_input = h_col1.text_input("Revision Number:", value=st.session_state.projects[active_id]["data"]["header_info"]["rev_no"], key=f"rev_{active_id}")
#                 upd_input = h_col2.text_input("Updated Date:", value=st.session_state.projects[active_id]["data"]["header_info"]["updated"], key=f"upd_{active_id}")
#                 cre_input = h_col3.text_input("Created Date:", value=st.session_state.projects[active_id]["data"]["header_info"]["created"], key=f"cre_{active_id}")
#                 st.session_state.projects[active_id]["data"]["header_info"] = {"rev_no": rev_input, "updated": upd_input, "created": cre_input}

#                 st.divider()
#                 current_assums = st.session_state.projects[active_id]["data"].get("assumptions", [
#                     "Foundation System Standard Pilecaps.",
#                     "No Basement.",
#                     "Parking Provision Limited To On Street Level Parking",
#                     "Floor To Floor Height At 3.3M",
#                     "Facade Alumunium Window Wall - No Double Skin",
#                     "External Façade Precast, No Double Skin For Parking Podium If Any.",
#                     "Ground Lobby Finishes Completed With Artificial Stone & HT.",
#                     "Typical Corridor | Floor Finishes : HT | Wall Finishes : Cement Sand Plaster C/W Emulsion Paint.",
#                     "Aircon System | Apartement : AC Split",
#                     "SBO Rebars @ Rp. 10.000/Kg",
#                     "Excluded Smarthome",
#                     "Lift : 2 Passenger Lift + 1 Services Lift / TOWER",
#                     "Exclude Wardrobe",
#                     "FFE : Kitchen Cabinet, Hob & Hood, Refrigerator & Washing Machine",
#                     "Water Heater : Installation Only",
#                     "Calculation Area Refer To DP's Calculation Dated 12.03.2026"
#                 ])

#                 df_assum = pd.DataFrame(current_assums, columns=["Note"])
#                 ed_assum = st.data_editor(df_assum, num_rows="dynamic", use_container_width=True, key=f"ed_sum_{active_id}")

#                 new_list = ed_assum["Note"].dropna().tolist()
#                 if new_list != current_assums:
#                     st.session_state.projects[active_id]["data"]["assumptions"] = new_list

#             # --- MANUAL PROJECTS EDITOR ---
#             st.markdown("---")
#             st.subheader("Manual Additional Projects")
#             st.caption("Add custom projects to the FAD summary below. Cost Ratios (Rp/m2) will be calculated automatically.")
            
#             if "manual_fad_projects" not in st.session_state:
#                 st.session_state.manual_fad_projects = pd.DataFrame(columns=[
#                     "Project Name", "GBA", "GFA", "SGFA", "Units", "Budget Estimate (Rp)"
#                 ])

#             edited_manual_df = st.data_editor(
#                 st.session_state.manual_fad_projects,
#                 num_rows="dynamic",
#                 use_container_width=True,
#                 key="manual_fad_editor",
#                 column_config={
#                     "GBA": st.column_config.NumberColumn("GBA", min_value=0, format="%.0f"),
#                     "GFA": st.column_config.NumberColumn("GFA", min_value=0, format="%.0f"),
#                     "SGFA": st.column_config.NumberColumn("SGFA", min_value=0, format="%.0f"),
#                     "Units": st.column_config.NumberColumn("Units", min_value=0, format="%.0f"),
#                     "Budget Estimate (Rp)": st.column_config.NumberColumn("Budget Estimate (Rp)", min_value=0, format="%.0f")
#                 }
#             )

#             rev_label = f"R({rev_input})"
#             h_upd = upd_input
#             h_cre = cre_input
#             dynamic_assumptions = current_assums

#             def get_project_totals(proj_dict):
#                 d = proj_dict.get("data", {})
#                 pt_data = PROJECT_DATABASE.get(proj_dict["type"], PROJECT_DATABASE["Hotel"])
#                 def v(key, default=0.0):
#                     return d.get(key, pt_data.get(key, default))
#                 gba = v("m_gba"); gfa = v("m_gfa"); sgfa = v("m_sgfa")
#                 rooms = v("m_rooms"); facade = v("m_facade")
#                 f_mult = fl_waste * fl_skirt
#                 hc = (
#                     (gba * v("u_earth")) + (gba * v("u_found")) + (gba * v("u_struc")) + (gfa * v("u_arch")) +
#                     (facade * (v("r_fac_pre") / 100) * v("u_f_pre")) + (facade * (v("r_fac_win") / 100) * v("u_f_win")) +
#                     (facade * (v("r_fac_doub") / 100) * v("u_f_doub")) + (v("m_door_w") * v("u_d_wood")) +
#                     (v("m_door_g") * v("u_d_glass")) + (v("m_door_s") * v("u_d_steel")) +
#                     (v("m_lobby") * v("u_lobby")) + (v("m_gondola") * v("u_gondola")) +
#                     (rooms * v("r_san_qty") * v("u_s_room")) + (v("m_toil_m") * v("u_s_pub_m")) +
#                     (v("m_toil_f") * v("u_s_pub_f")) + (v("m_toil_d") * v("u_s_dis")) +
#                     (v("m_mushola") * v("u_s_mushola")) + (rooms * v("u_kit")) +
#                     (v("m_door_w") * v("u_hw_wood")) + (v("m_door_s") * v("u_hw_steel")) +
#                     (gfa * (v("r_fl_ht") / 100) * v("u_fl_ht") * f_mult) +
#                     (gfa * (v("r_fl_vin") / 100) * v("u_fl_vin") * f_mult) +
#                     (gfa * (v("r_fl_mar") / 100) * v("u_fl_mar") * f_mult) +
#                     (v("m_carpet") * v("u_carpet")) + (v("m_glass") * v("u_glass")) +
#                     (rooms * v("u_ffe")) + (v("u_misc") * d.get("misc_switch", 0)) +
#                     (gba * v("u_mep")) + (gba * v("u_util")) +
#                     (rooms * v("r_rail_qty") * v("u_rail")) + (v("m_skylight") * v("u_sky")) +
#                     (v("m_land_m2") * v("u_ext")) + (v("m_fac_pub") * v("u_fac_p")) +
#                     (v("m_fac_res") * v("u_fac_r")) + (v("m_fac_proj") * v("u_fac_pr")) + v("smart_custom_costs")
#                 )
                
#                 custom_costs = d.get("smart_custom_costs", [])
#                 dep_map = {
#                     "None (Flat Rate)": 1.0, "GBA": gba, "GFA": gfa, "SGFA": sgfa,
#                     "Land Area": v("m_land"), "Rooms": rooms, "Facade": facade, "Lobby": v("m_lobby")
#                 }
#                 for item in custom_costs:
#                     hc += (float(item.get("Rate (Rp)", 0)) * float(item.get("Quantity", 1)) *
#                         dep_map.get(item.get("Linked Dependency"), 1.0))
#                 hc_total = hc + (hc * 0.05) + (hc * 0.03)
#                 sc_total = ((gfa * v("sc_cons")) + (v("sc_qs_m") * v("sc_qs_r")) +
#                             (v("sc_pm_m") * v("sc_pm_r")) + (hc * (v("sc_ins") / 100)))
#                 return {"gba": gba, "gfa": gfa, "sgfa": sgfa, "units": rooms, "budget": hc_total + sc_total}

#             # --- DATA AGGREGATION (CALCULATED + MANUAL) ---
#             combined_results = []
#             idx = 1
            
#             # 1. Add Auto-Calculated Projects
#             for p_id, p_data in st.session_state.projects.items():
#                 m = get_project_totals(p_data)
#                 combined_results.append({
#                     "idx": idx, "name": p_data["name"].upper(),
#                     "gba": m["gba"], "gfa": m["gfa"], "sgfa": m["sgfa"],
#                     "units": m["units"], "budget": m["budget"]
#                 })
#                 idx += 1

#             # 2. Add Manual Projects
#             edited_manual_df = edited_manual_df.fillna(0) # <--- ADD THIS LINE
#             for _, row in edited_manual_df.iterrows():
#                 p_name = str(row.get("Project Name", f"MANUAL PROJECT {idx}"))
#                 if p_name == "nan" or not p_name.strip(): p_name = f"MANUAL PROJECT {idx}"
                
#                 combined_results.append({
#                     "idx": idx, "name": p_name.upper(),
#                     "gba": float(row.get("GBA", 0) or 0),
#                     "gfa": float(row.get("GFA", 0) or 0),
#                     "sgfa": float(row.get("SGFA", 0) or 0),
#                     "units": float(row.get("Units", 0) or 0),
#                     "budget": float(row.get("Budget Estimate (Rp)", 0) or 0)
#                 })
#                 idx += 1

#             # 3. Calculate Ratios & Totals
#             table_rows_html = ""
#             total_gba = total_gfa = total_sgfa = total_budget = 0

#             for p in combined_results:
#                 r_gba  = p["budget"] / p["gba"]  if p["gba"]  > 0 else 0
#                 r_gfa  = p["budget"] / p["gfa"]  if p["gfa"]  > 0 else 0
#                 r_sgfa = p["budget"] / p["sgfa"] if p["sgfa"] > 0 else 0

#                 p["r_gba"] = r_gba
#                 p["r_gfa"] = r_gfa
#                 p["r_sgfa"] = r_sgfa

#                 total_gba += p["gba"]
#                 total_gfa += p["gfa"]
#                 total_sgfa += p["sgfa"]
#                 total_budget += p["budget"]

#                 table_rows_html += (
#                     f"<tr>"
#                     f"<td style='border:1px solid black;padding:5px;'>{p['idx']}</td>"
#                     f"<td style='border:1px solid black;padding:5px;text-align:left;'><b>{p['name']}</b></td>"
#                     f"<td style='border:1px solid black;padding:5px;'>{p['gba']:,.0f}</td>"
#                     f"<td style='border:1px solid black;padding:5px;'>{p['gfa']:,.0f}</td>"
#                     f"<td style='border:1px solid black;padding:5px;'>{p['sgfa']:,.0f}</td>"
#                     f"<td style='border:1px solid black;padding:5px;'>{p['units']:,.0f}</td>"
#                     f"<td style='border:1px solid black;padding:5px;'>Units</td>"
#                     f"<td style='border:1px solid black;padding:5px;text-align:right;'><b>{p['budget']:,.0f}</b></td>"
#                     f"<td style='border:1px solid black;padding:5px;'>{r_gba:,.0f}</td>"
#                     f"<td style='border:1px solid black;padding:5px;'>{r_gfa:,.0f}</td>"
#                     f"<td style='border:1px solid black;padding:5px;'>{r_sgfa:,.0f}</td>"
#                     f"</tr>"
#                 )

#             t_r_gba  = total_budget / total_gba  if total_gba  > 0 else 0
#             t_r_gfa  = total_budget / total_gfa  if total_gfa  > 0 else 0
#             t_r_sgfa = total_budget / total_sgfa if total_sgfa > 0 else 0

#             # --- EXCEL BUILDER ---
#             buffer = io.BytesIO()
#             workbook = xlsxwriter.Workbook(buffer, {"in_memory": True, "nan_inf_to_errors": True})
#             worksheet = workbook.add_worksheet("Portfolio Summary")

#             f_blue_L    = workbook.add_format({"bg_color": "#0062a8", "font_color": "white", "bold": True, "valign": "vcenter"})
#             f_th        = workbook.add_format({"bg_color": "#f2f2f2", "bold": True, "align": "center", "valign": "vcenter", "border": 1, "text_wrap": True})
#             f_td_c      = workbook.add_format({"align": "center", "valign": "vcenter", "border": 1})
#             f_td_L_b    = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1, "bold": True})
#             f_td_R_b    = workbook.add_format({"align": "right", "valign": "vcenter", "border": 1, "bold": True, "num_format": "#,##0"})
#             f_td_num    = workbook.add_format({"align": "right", "valign": "vcenter", "border": 1, "num_format": "#,##0"})
#             f_tot_L     = workbook.add_format({"bg_color": "#e0e0e0", "bold": True, "align": "center", "valign": "vcenter", "border": 1})
#             f_tot_num   = workbook.add_format({"bg_color": "#e0e0e0", "bold": True, "align": "right", "valign": "vcenter", "border": 1, "num_format": "#,##0"})
#             f_tot_empty = workbook.add_format({"bg_color": "#e0e0e0", "border": 1})
#             f_assum_h   = workbook.add_format({"bg_color": "#ffdf70", "bold": True, "border": 1, "valign": "vcenter"})
#             f_assum_c   = workbook.add_format({"align": "center", "border": 1})
#             f_assum_L   = workbook.add_format({"align": "left", "border": 1})

#             worksheet.set_column("A:A", 5); worksheet.set_column("B:B", 38); worksheet.set_column("C:E", 15)
#             worksheet.set_column("F:F", 10); worksheet.set_column("G:G", 8); worksheet.set_column("H:H", 22)
#             worksheet.set_column("I:K", 15)

#             for row in range(5):
#                 worksheet.merge_range(row, 0, row, 10, "", f_blue_L)
#             worksheet.write_string(0, 0, f"ASG GROUP PROPERTY DEVELOPMENT | VERSION : {rev_label}", f_blue_L)
#             worksheet.write_string(1, 0, "QS & PROCUREMENT DIVISION", f_blue_L)
#             worksheet.write_string(2, 0, "PROJECT PORTFOLIO | ALL ACTIVE PROJECTS", f_blue_L)
#             worksheet.write_string(3, 0, f"REF. DATA {rev_label} | CONCEPT PDF COMPARISON STUDY BY DPA | UPDATED : {h_upd}", f_blue_L)
#             worksheet.write_string(4, 0, f"BUDGET ESTIMATE {rev_label} | CREATED : {h_cre}", f_blue_L)

#             worksheet.merge_range("A7:A8", "SN", f_th); worksheet.merge_range("B7:B8", "AREA", f_th)
#             worksheet.merge_range("C7:E7", "BUILDING AREA (M2)", f_th)
#             worksheet.write_string("C8", "GBA", f_th); worksheet.write_string("D8", "GFA", f_th); worksheet.write_string("E8", "SGFA", f_th)
#             worksheet.merge_range("F7:G8", "UNIT", f_th); worksheet.merge_range("H7:H8", "BUDGET ESTIMATE\nRP", f_th)
#             worksheet.merge_range("I7:K7", "COST RATIO RP/M2", f_th)
#             worksheet.write_string("I8", "GBA", f_th); worksheet.write_string("J8", "GFA", f_th); worksheet.write_string("K8", "SGFA", f_th)

#             row_idx = 8
#             for p in combined_results:
#                 worksheet.write_number(row_idx, 0, p["idx"], f_td_c)
#                 worksheet.write_string(row_idx, 1, p["name"], f_td_L_b)
#                 worksheet.write_number(row_idx, 2, p["gba"], f_td_num)
#                 worksheet.write_number(row_idx, 3, p["gfa"], f_td_num)
#                 worksheet.write_number(row_idx, 4, p["sgfa"], f_td_num)
#                 worksheet.write_number(row_idx, 5, p["units"], f_td_c)
#                 worksheet.write_string(row_idx, 6, "Units", f_td_c)
#                 worksheet.write_number(row_idx, 7, p["budget"], f_td_R_b)
#                 worksheet.write_number(row_idx, 8, p["r_gba"], f_td_num)
#                 worksheet.write_number(row_idx, 9, p["r_gfa"], f_td_num)
#                 worksheet.write_number(row_idx, 10, p["r_sgfa"], f_td_num)
#                 row_idx += 1

#             worksheet.merge_range(row_idx, 0, row_idx, 1, "TOTAL", f_tot_L)
#             worksheet.write_number(row_idx, 2, total_gba, f_tot_num)
#             worksheet.write_number(row_idx, 3, total_gfa, f_tot_num)
#             worksheet.write_number(row_idx, 4, total_sgfa, f_tot_num)
#             worksheet.write_string(row_idx, 5, "", f_tot_empty)
#             worksheet.write_string(row_idx, 6, "", f_tot_empty)
#             worksheet.write_number(row_idx, 7, total_budget, f_tot_num)
#             worksheet.write_number(row_idx, 8, t_r_gba, f_tot_num)
#             worksheet.write_number(row_idx, 9, t_r_gfa, f_tot_num)
#             worksheet.write_number(row_idx, 10, t_r_sgfa, f_tot_num)

#             row_idx += 2
#             worksheet.write_string(row_idx, 0, "I.", f_assum_h)
#             worksheet.merge_range(row_idx, 1, row_idx, 10, "ASSUMPTIONS", f_assum_h)
#             for i, assum in enumerate(dynamic_assumptions, 1):
#                 row_idx += 1
#                 worksheet.write_number(row_idx, 0, i, f_assum_c)
#                 text = str(assum)
#                 date_match = re.search(r"(\d{2}[./-]\d{2}[./-]\d{4})", text)
#                 if date_match:
#                     worksheet.merge_range(row_idx, 1, row_idx, 10, "", f_assum_L)
#                     parts = text.split(date_match.group(1))
#                     rich_args = []
#                     if parts[0]: rich_args.append(parts[0])
#                     rich_args.extend([workbook.add_format({"font_color": "red"}), date_match.group(1)])
#                     if len(parts) > 1 and parts[1]: rich_args.append(parts[1])
#                     worksheet.write_rich_string(row_idx, 1, *rich_args, f_assum_L)
#                 else:
#                     worksheet.merge_range(row_idx, 1, row_idx, 10, text, f_assum_L)
#             workbook.close()

#             st.download_button(
#                 label="Download FAD as .xlsx",
#                 data=buffer.getvalue(),
#                 file_name=f"ASG_Portfolio_{active_id}.xlsx",
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                 use_container_width=True
#             )

#             # --- HTML TABLE RENDER ---
#             assum_html_rows = ""
#             for i, assum in enumerate(dynamic_assumptions, 1):
#                 display_text = re.sub(r"(\d{2}[./-]\d{2}[./-]\d{4})", r"<span style='color:red;'>\1</span>", str(assum))
#                 assum_html_rows += (
#                     f"<tr><td style='text-align:center;border-right:1px solid #e0e0e0;padding:2px;'>{i}</td>"
#                     f"<td style='padding:2px 5px;'>{display_text}</td></tr>"
#                 )

#             html_string = f"""
#             <div style="font-family:Calibri,sans-serif;font-size:13px;color:black;background-color:white;padding:20px;border-radius:5px;">
#                 <div style="background-color:#0062a8;color:white;padding:12px;font-weight:bold;line-height:1.6;font-size:14px;text-align:left;">
#                     <div>ASG GROUP PROPERTY DEVELOPMENT <span style="margin-left:20px;">VERSION : {rev_label}</span></div>
#                     <div>QS &amp; PROCUREMENT DIVISION</div>
#                     <div>PROJECT PORTFOLIO | ALL ACTIVE PROJECTS</div>
#                     <div>REF. DATA {rev_label} | CONCEPT PDF COMPARISON STUDY BY DPA <span style="margin-left:20px;">UPDATED : {h_upd}</span></div>
#                     <div>BUDGET ESTIMATE {rev_label} <span style="margin-left:20px;">CREATED : {h_cre}</span></div>
#                 </div>
#                 <br>
#                 <table style="width:100%;border-collapse:collapse;border:2px solid black;text-align:center;">
#                     <tr style="background-color:#f2f2f2;font-weight:bold;">
#                         <td rowspan="2" style="border:1px solid black;padding:5px;">SN</td>
#                         <td rowspan="2" style="border:1px solid black;padding:5px;">AREA</td>
#                         <td colspan="3" style="border:1px solid black;padding:5px;">BUILDING AREA (M2)</td>
#                         <td colspan="2" rowspan="2" style="border:1px solid black;padding:5px;">UNIT</td>
#                         <td rowspan="2" style="border:1px solid black;padding:5px;">BUDGET ESTIMATE<br>RP</td>
#                         <td colspan="3" style="border:1px solid black;padding:5px;">COST RATIO RP/M2</td>
#                     </tr>
#                     <tr style="background-color:#f2f2f2;font-weight:bold;">
#                         <td style="border:1px solid black;padding:5px;">GBA</td>
#                         <td style="border:1px solid black;padding:5px;">GFA</td>
#                         <td style="border:1px solid black;padding:5px;">SGFA</td>
#                         <td style="border:1px solid black;padding:5px;">GBA</td>
#                         <td style="border:1px solid black;padding:5px;">GFA</td>
#                         <td style="border:1px solid black;padding:5px;">SGFA</td>
#                     </tr>
#                     {table_rows_html}
#                     <tr style="background-color:#e0e0e0;font-weight:bold;">
#                         <td colspan="2" style="border:1px solid black;padding:5px;">TOTAL</td>
#                         <td style="border:1px solid black;padding:5px;">{total_gba:,.0f}</td>
#                         <td style="border:1px solid black;padding:5px;">{total_gfa:,.0f}</td>
#                         <td style="border:1px solid black;padding:5px;">{total_sgfa:,.0f}</td>
#                         <td colspan="2" style="border:1px solid black;padding:5px;"></td>
#                         <td style="border:1px solid black;padding:5px;text-align:right;">{total_budget:,.0f}</td>
#                         <td style="border:1px solid black;padding:5px;">{t_r_gba:,.0f}</td>
#                         <td style="border:1px solid black;padding:5px;">{t_r_gfa:,.0f}</td>
#                         <td style="border:1px solid black;padding:5px;">{t_r_sgfa:,.0f}</td>
#                     </tr>
#                 </table>
#                 <br>
#                 <table style="width:100%;border-collapse:collapse;border:1px solid #dcdcdc;text-align:left;">
#                     <tr style="background-color:#ffdf70;font-weight:bold;">
#                         <td style="border:1px solid white;padding:3px 5px;width:30px;text-align:center;">I.</td>
#                         <td style="border:1px solid white;padding:3px 5px;">ASSUMPTIONS</td>
#                     </tr>
#                     {assum_html_rows}
#                 </table>
#             </div>
#             """
#             st.markdown(html_string.replace("\n", ""), unsafe_allow_html=True)

#     with tab_detailed:
#             st.subheader("Tabel Rekapitulasi")

#             # 1. SETUP: Prepare to collect data for ALL projects
#             all_projects_data = []
#             grand_total_all_projects = 0
            
#             # Area trackers for combined ratios
#             total_gba_all = 0; total_gfa_all = 0; total_sgfa_all = 0
            
#             # Subtotal trackers for the first "TOTAL" column
#             sum_hardcost = 0; sum_prelim = 0; sum_earth = 0; sum_found = 0; sum_struc = 0
#             sum_arch = 0; sum_ffe = 0; sum_mep = 0; sum_util = 0; sum_ext = 0; sum_fac = 0
#             sum_cont = 0; sum_softcost = 0; sum_cons = 0; sum_qs = 0; sum_pm = 0; sum_ins = 0

#             # 2. CALCULATE EACH PROJECT
#             for p_id, p_dict in st.session_state.projects.items():
#                 d = p_dict.get("data", {})
#                 pt_data = PROJECT_DATABASE.get(p_dict["type"], PROJECT_DATABASE["Hotel"])
                
#                 def v(key, default=0.0):
#                     try:
#                         return float(d.get(key, pt_data.get(key, default)))
#                     except (ValueError, TypeError):
#                         return 0.0

#                 gba = v("m_gba"); gfa = v("m_gfa"); sgfa = v("m_sgfa")
#                 facade = v("m_facade"); rooms = v("m_rooms")
#                 f_mult = fl_waste * fl_skirt

#                 # Hardcosts
#                 v_earth = gba * v("u_earth")
#                 v_found = gba * v("u_found")
#                 v_struc = gba * v("u_struc")
#                 v_arch = (
#                     (gfa * v("u_arch")) + (facade * (v("r_fac_pre") / 100) * v("u_f_pre")) + 
#                     (facade * (v("r_fac_win") / 100) * v("u_f_win")) + (facade * (v("r_fac_doub") / 100) * v("u_f_doub")) + 
#                     (v("m_door_w") * v("u_d_wood")) + (v("m_door_g") * v("u_d_glass")) + (v("m_door_s") * v("u_d_steel")) + 
#                     (v("m_lobby") * v("u_lobby")) + (v("m_gondola") * v("u_gondola")) + (rooms * v("r_san_qty") * v("u_s_room")) + 
#                     (v("m_toil_m") * v("u_s_pub_m")) + (v("m_toil_f") * v("u_s_pub_f")) + (v("m_toil_d") * v("u_s_dis")) + 
#                     (v("m_mushola") * v("u_s_mushola")) + (v("m_door_w") * v("u_hw_wood")) + (v("m_door_s") * v("u_hw_steel")) + 
#                     (gfa * (v("r_fl_ht") / 100) * v("u_fl_ht") * f_mult) + (gfa * (v("r_fl_vin") / 100) * v("u_fl_vin") * f_mult) + 
#                     (gfa * (v("r_fl_mar") / 100) * v("u_fl_mar") * f_mult) + (v("m_carpet") * v("u_carpet")) + 
#                     (v("m_glass") * v("u_glass")) + (rooms * v("r_rail_qty") * v("u_rail")) + (v("m_skylight") * v("u_sky")) + (v("smart_custom_costs"))
#                 )
#                 v_ffe = (rooms * v("u_ffe")) + (rooms * v("u_kit")) + (v("u_misc") * d.get("misc_switch", 0))
#                 v_mep = gba * v("u_mep")
#                 v_util = gba * v("u_util")
#                 v_ext = v("m_land_m2") * v("u_ext")
#                 v_fac = (v("m_fac_pub") * v("u_fac_p")) + (v("m_fac_res") * v("u_fac_r")) + (v("m_fac_proj") * v("u_fac_pr"))
                
#                 # Custom
#                 c_costs = d.get("smart_custom_costs", [])
#                 dep_map = {"None (Flat Rate)": 1.0, "GBA": gba, "GFA": gfa, "SGFA": sgfa, "Land Area": v("m_land"), "Rooms": rooms, "Facade": facade, "Lobby": v("m_lobby")}
#                 v_custom = sum([(float(item.get("Rate (Rp)", 0)) * float(item.get("Quantity", 1)) * dep_map.get(item.get("Linked Dependency"), 1.0)) for item in c_costs])

#                 hc_sub = v_earth + v_found + v_struc + v_arch + v_ffe + v_mep + v_util + v_ext + v_fac + v_custom
#                 v_prelim = (hc_sub) * 0.05
#                 v_cont = (hc_sub) * 0.03
#                 hc_tot = hc_sub + v_prelim + v_cont

#                 # Softcosts
#                 v_cons = gfa * v("sc_cons")
#                 v_qs = v("sc_qs_m") * v("sc_qs_r")
#                 v_pm = v("sc_pm_m") * v("sc_pm_r")
#                 v_ins = (hc_sub) * (v("sc_ins") / 100)
#                 sc_tot = v_cons + v_qs + v_pm + v_ins
                
#                 p_grand = hc_tot + sc_tot

#                 # Store for this project
#                 proj_data = {
#                     "name": p_dict["name"], "gba": gba, "gfa": gfa, "sgfa": sgfa, "grand": p_grand,
#                     "vals": {
#                         "hc": hc_tot, "prelim": v_prelim, "earth": v_earth, "found": v_found, "struc": v_struc,
#                         "arch": v_arch, "ffe": v_ffe, "mep": v_mep, "util": v_util, "ext": v_ext, "fac": v_fac,
#                         "cont": v_cont, "sc": sc_tot, "cons": v_cons, "qs": v_qs, "pm": v_pm, "ins": v_ins
#                     }
#                 }
#                 all_projects_data.append(proj_data)

#                 # Add to grand totals
#                 total_gba_all += gba
#                 total_gfa_all += gfa
#                 total_sgfa_all += sgfa
                
#                 sum_hardcost += hc_tot; sum_prelim += v_prelim; sum_earth += v_earth; sum_found += v_found
#                 sum_struc += v_struc; sum_arch += v_arch; sum_ffe += v_ffe; sum_mep += v_mep
#                 sum_util += v_util; sum_ext += v_ext; sum_fac += v_fac; sum_cont += v_cont
#                 sum_softcost += sc_tot; sum_cons += v_cons; sum_qs += v_qs; sum_pm += v_pm; sum_ins += v_ins
#                 grand_total_all_projects += p_grand

#             # 3. BUILD DYNAMIC HTML HEADERS
#             color_palette = ["#ccffe6", "#ffe6e6", "#e6e6ff", "#ffffe6", "#ffe6ff"] # Colors for different projects
            
#             # Header Row 1 (Project Names)
#             header_col_names = f'<td colspan="4" style="border:1px solid black; padding:4px; background-color: #e6f2ff;">TOTAL <span style="margin:0 15px;">Cost Ratio (Rp/m2)</span></td>'
            
#             # Header Row 2 (Cost Ratio Titles)
#             header_ratios = f'<td colspan="4" style="border:1px solid black; padding:4px; background-color: #e6f2ff; color: red;">ALL PROJECTS</td>'
            
#             # Header Row 3 (GBA/GFA/SGFA labels)
#             header_sublabels = f"""
#                 <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">TOTAL (Rp)</td>
#                 <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">GBA</td>
#                 <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">GFA</td>
#                 <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">SGFA</td>
#             """
            
#             # Header Row 4 (Overall Area Totals)
#             header_empty = f"""
#                 <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">-</td>
#                 <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">{total_gba_all:,.0f}</td>
#                 <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">{total_gfa_all:,.0f}</td>
#                 <td style="border:1px solid black; padding:4px; background-color: #e6f2ff;">{total_sgfa_all:,.0f}</td>
#             """

#             for i, p in enumerate(all_projects_data):
#                 bg_col = color_palette[i % len(color_palette)]
                
#                 header_col_names += f'<td colspan="4" style="border:1px solid black; padding:4px; background-color: {bg_col};">ESTIMATE <span style="margin:0 15px;">Cost Ratio (Rp/m2)</span></td>'
#                 header_ratios += f'<td colspan="4" style="border:1px solid black; padding:4px; background-color: {bg_col}; color: red;">{p["name"].upper()}</td>'
#                 header_sublabels += f"""
#                     <td style="border:1px solid black; padding:4px; background-color: {bg_col};">TOTAL (Rp)</td>
#                     <td style="border:1px solid black; padding:4px; background-color: {bg_col};">GBA</td>
#                     <td style="border:1px solid black; padding:4px; background-color: {bg_col};">GFA</td>
#                     <td style="border:1px solid black; padding:4px; background-color: {bg_col};">SGFA</td>
#                 """
#                 header_empty += f"""
#                     <td style="border:1px solid black; padding:4px; background-color: {bg_col};">-</td>
#                     <td style="border:1px solid black; padding:4px; background-color: {bg_col};">{p["gba"]:,.0f}</td>
#                     <td style="border:1px solid black; padding:4px; background-color: {bg_col};">{p["gfa"]:,.0f}</td>
#                     <td style="border:1px solid black; padding:4px; background-color: {bg_col};">{p["sgfa"]:,.0f}</td>
#                 """

#             # 4. ROW DEFINITIONS
#             row_map = [
#                 {"sn": "I", "desc": "HARDCOST", "coa": "118-14-000", "key": "hc", "sum": sum_hardcost, "is_main": True},
#                 {"sn": "1", "desc": "PRELIMINARIES WORKS", "coa": "118-14-100", "key": "prelim", "sum": sum_prelim, "is_main": False},
#                 {"sn": "2", "desc": "EARTHWORKS", "coa": "118-14-200", "key": "earth", "sum": sum_earth, "is_main": False},
#                 {"sn": "3", "desc": "FOUNDATIONS", "coa": "118-14-300", "key": "found", "sum": sum_found, "is_main": False},
#                 {"sn": "4", "desc": "STRUCTURAL WORKS", "coa": "118-14-500", "key": "struc", "sum": sum_struc, "is_main": False},
#                 {"sn": "5", "desc": "ARCHITECTURAL WORKS", "coa": "118-14-600", "key": "arch", "sum": sum_arch, "is_main": False},
#                 {"sn": "6", "desc": "FF & E", "coa": "118-14-700", "key": "ffe", "sum": sum_ffe, "is_main": False},
#                 {"sn": "7", "desc": "M.E.P WORKS", "coa": "118-14-800", "key": "mep", "sum": sum_mep, "is_main": False},
#                 {"sn": "8", "desc": "UTILITY CONNECTION", "coa": "118-13-900", "key": "util", "sum": sum_util, "is_main": False},
#                 {"sn": "9", "desc": "EXTERNAL WORKS", "coa": "118-14-930", "key": "ext", "sum": sum_ext, "is_main": False},
#                 {"sn": "10", "desc": "FACILITY", "coa": "118-14-960", "key": "fac", "sum": sum_fac, "is_main": False},
#                 {"sn": "11", "desc": "CONTINGENCIES", "coa": "", "key": "cont", "sum": sum_cont, "is_main": False},
#                 {"sn": "II", "desc": "SOFTCOST", "coa": "118-13-000", "key": "sc", "sum": sum_softcost, "is_main": True},
#                 {"sn": "1", "desc": "CONSULTANCY SERVICES FEE", "coa": "118-13-202", "key": "cons", "sum": sum_cons, "is_main": False},
#                 {"sn": "2", "desc": "QS SERVICES", "coa": "118-13-201", "key": "qs", "sum": sum_qs, "is_main": False},
#                 {"sn": "3", "desc": "PROJECT MANAGEMENT SERVICES", "coa": "118-13-203", "key": "pm", "sum": sum_pm, "is_main": False},
#                 {"sn": "4", "desc": "INSURANCE COVERAGE", "coa": "118-13-300", "key": "ins", "sum": sum_ins, "is_main": False},
#                 {"sn": "IV", "desc": "TOTAL, EXCLD PPN", "coa": "", "key": "grand", "sum": grand_total_all_projects, "is_main": True, "is_grand_total": True}
#             ]

#             # 5. BUILD DATA ROWS DYNAMICALLY
#             html_rows = ""
#             for row in row_map:
#                 bg_color = "#e6f2e6" if row.get("is_main") else "white"
#                 font_w = "bold" if row.get("is_main") else "normal"
#                 blue_bg = "background-color:#3b82f6;color:white;" if row.get("is_grand_total") else ""
                
#                 pct = (row["sum"] / grand_total_all_projects * 100) if grand_total_all_projects > 0 else 0
                
#                 # Overall Portfolio Ratios
#                 tot_r_gba = (row["sum"] / total_gba_all) if total_gba_all > 0 else 0
#                 tot_r_gfa = (row["sum"] / total_gfa_all) if total_gfa_all > 0 else 0
#                 tot_r_sgfa = (row["sum"] / total_sgfa_all) if total_sgfa_all > 0 else 0

#                 # Start row with left-side static labels and the Grand Total section
#                 row_html = f"""
#                 <tr style="background-color:{bg_color}; font-weight:{font_w}; {blue_bg}">
#                     <td style="border:1px solid black; padding:4px; text-align:center;">{row['sn']}</td>
#                     <td style="border:1px solid black; padding:4px; text-align:left;">{row['desc']}</td>
#                     <td style="border:1px solid black; padding:4px; text-align:center;">{row['coa']}</td>
#                     <td style="border:1px solid black; padding:4px; text-align:center;">{pct:.2f}%</td>
#                     <td style="border:1px solid black; padding:4px; text-align:right;">{row['sum']:,.0f}</td>
#                     <td style="border:1px solid black; padding:4px; text-align:right;">{tot_r_gba:,.0f}</td>
#                     <td style="border:1px solid black; padding:4px; text-align:right;">{tot_r_gfa:,.0f}</td>
#                     <td style="border:1px solid black; padding:4px; text-align:right;">{tot_r_sgfa:,.0f}</td>
#                 """
                
#                 # Append data dynamically for each project
#                 for p in all_projects_data:
#                     val = p['grand'] if row['key'] == 'grand' else p['vals'][row['key']]
#                     r_gba = (val / p['gba']) if p['gba'] > 0 else 0
#                     r_gfa = (val / p['gfa']) if p['gfa'] > 0 else 0
#                     r_sgfa = (val / p['sgfa']) if p['sgfa'] > 0 else 0
                    
#                     row_html += f"""
#                         <td style="border:1px solid black; padding:4px; text-align:right;">{val:,.0f}</td>
#                         <td style="border:1px solid black; padding:4px; text-align:right;">{r_gba:,.0f}</td>
#                         <td style="border:1px solid black; padding:4px; text-align:right;">{r_gfa:,.0f}</td>
#                         <td style="border:1px solid black; padding:4px; text-align:right;">{r_sgfa:,.0f}</td>
#                     """
                
#                 row_html += "</tr>"
#                 html_rows += row_html

#             # 6. RENDER FINAL TABLE
#             detailed_html = f"""
#             <div style="font-family: Arial, sans-serif; font-size: 11px; color: black; background-color: white; overflow-x: auto; margin-bottom: 20px;">
#                 <table style="width: 100%; border-collapse: collapse; border: 2px solid black; text-align: center; white-space: nowrap;">
#                     <thead>
#                         <tr style="background-color: #f2f2f2; font-weight: bold;">
#                             <td rowspan="3" style="border:1px solid black; padding:4px; width:30px;">SN</td>
#                             <td rowspan="3" style="border:1px solid black; padding:4px; width:200px;">DESCRIPTION</td>
#                             <td rowspan="3" style="border:1px solid black; padding:4px;">COA</td>
#                             <td rowspan="3" style="border:1px solid black; padding:4px;">%</td>
#                             {header_col_names}
#                         </tr>
#                         <tr style="font-weight: bold;">
#                             {header_ratios}
#                         </tr>
#                         <tr style="background-color: #f2f2f2; font-weight: bold;">
#                             {header_sublabels}
#                         </tr>
#                         <tr style="background-color: #f2f2f2; font-weight: bold;">
#                             <td colspan="4" style="border:1px solid black; padding:4px;"></td>
#                             {header_empty}
#                         </tr>
#                     </thead>
#                     <tbody>
#                         {html_rows}
#                     </tbody>
#                 </table>
#             </div>
#             """
#             st.markdown(detailed_html.replace("\n", ""), unsafe_allow_html=True)

#             # --- EXCEL DOWNLOAD LOGIC ---
#             h_info = st.session_state.projects[active_id]["data"].get("header_info", {})
#             rev_label = f"R({h_info.get('rev_no', '0')})"
#             h_upd = h_info.get("updated", "")
#             h_cre = h_info.get("created", "")

#             buffer_det = io.BytesIO()
#             wb = xlsxwriter.Workbook(buffer_det, {"in_memory": True})
#             ws = wb.add_worksheet("Detailed Estimate")

#             # Formats
#             f_blue = wb.add_format({"bg_color": "#0062a8", "font_color": "white", "bold": True, "valign": "vcenter"})
#             f_th = wb.add_format({"bg_color": "#f2f2f2", "bold": True, "align": "center", "valign": "vcenter", "border": 1, "text_wrap": True})
#             f_th_tot = wb.add_format({"bg_color": "#e6f2ff", "bold": True, "align": "center", "valign": "vcenter", "border": 1})
#             f_th_tot_red = wb.add_format({"bg_color": "#e6f2ff", "bold": True, "align": "center", "valign": "vcenter", "border": 1, "font_color": "red"})
            
#             f_c = wb.add_format({"align": "center", "valign": "vcenter", "border": 1})
#             f_L = wb.add_format({"align": "left", "valign": "vcenter", "border": 1})
#             f_pct = wb.add_format({"align": "center", "valign": "vcenter", "border": 1, "num_format": "0.00%"})
#             f_num = wb.add_format({"align": "right", "valign": "vcenter", "border": 1, "num_format": "#,##0"})

#             f_mc = wb.add_format({"bg_color": "#e6f2e6", "bold": True, "align": "center", "valign": "vcenter", "border": 1})
#             f_mL = wb.add_format({"bg_color": "#e6f2e6", "bold": True, "align": "left", "valign": "vcenter", "border": 1})
#             f_mpct = wb.add_format({"bg_color": "#e6f2e6", "bold": True, "align": "center", "valign": "vcenter", "border": 1, "num_format": "0.00%"})
#             f_mnum = wb.add_format({"bg_color": "#e6f2e6", "bold": True, "align": "right", "valign": "vcenter", "border": 1, "num_format": "#,##0"})

#             f_gc = wb.add_format({"bg_color": "#3b82f6", "font_color": "white", "bold": True, "align": "center", "border": 1})
#             f_gL = wb.add_format({"bg_color": "#3b82f6", "font_color": "white", "bold": True, "align": "left", "border": 1})
#             f_gpct = wb.add_format({"bg_color": "#3b82f6", "font_color": "white", "bold": True, "align": "center", "border": 1, "num_format": "0.00%"})
#             f_gnum = wb.add_format({"bg_color": "#3b82f6", "font_color": "white", "bold": True, "align": "right", "border": 1, "num_format": "#,##0"})

#             ws.set_column("A:A", 5); ws.set_column("B:B", 35); ws.set_column("C:C", 12); ws.set_column("D:D", 8)
            
#             # Header Block
#             for r in range(5): ws.merge_range(r, 0, r, 7 + (len(all_projects_data)*4), "", f_blue)
#             ws.write_string(0, 0, f"ASG GROUP PROPERTY DEVELOPMENT | VERSION : {rev_label}", f_blue)
#             ws.write_string(1, 0, "QS & PROCUREMENT DIVISION", f_blue)
#             ws.write_string(2, 0, "DETAILED ESTIMATE | ALL ACTIVE PROJECTS", f_blue)
#             ws.write_string(3, 0, f"REF. DATA {rev_label} | CONCEPT PDF COMPARISON STUDY BY DPA | UPDATED : {h_upd}", f_blue)
#             ws.write_string(4, 0, f"BUDGET ESTIMATE {rev_label} | CREATED : {h_cre}", f_blue)

#             # Table Headers
#             ws.merge_range("A7:A9", "SN", f_th); ws.merge_range("B7:B9", "DESCRIPTION", f_th)
#             ws.merge_range("C7:C9", "COA", f_th); ws.merge_range("D7:D9", "%", f_th)

#             # Dynamic Header Columns
#             col_idx = 4
#             ws.merge_range(6, col_idx, 6, col_idx+3, "ESTIMATE Cost Ratio (Rp/m2)", f_th_tot)
#             ws.merge_range(7, col_idx, 7, col_idx+3, "TOTAL ALL PROJECTS", f_th_tot_red)
#             ws.write(8, col_idx, "TOTAL (Rp)", f_th_tot); ws.write(8, col_idx+1, "GBA", f_th_tot)
#             ws.write(8, col_idx+2, "GFA", f_th_tot); ws.write(8, col_idx+3, "SGFA", f_th_tot)
            
#             # Write Total Area row
#             ws.write_row(9, 0, ["", "", "", ""], f_th)
#             ws.write(9, col_idx, "-", f_th_tot); ws.write(9, col_idx+1, total_gba_all, f_th_tot)
#             ws.write(9, col_idx+2, total_gfa_all, f_th_tot); ws.write(9, col_idx+3, total_sgfa_all, f_th_tot)
#             col_idx += 4

#             for i, p in enumerate(all_projects_data):
#                 color_hex = color_palette[i % len(color_palette)]
#                 f_proj_th = wb.add_format({"bg_color": color_hex, "bold": True, "align": "center", "valign": "vcenter", "border": 1})
#                 f_proj_th_red = wb.add_format({"bg_color": color_hex, "bold": True, "align": "center", "valign": "vcenter", "border": 1, "font_color": "red"})
                
#                 ws.set_column(col_idx, col_idx+3, 14)
#                 ws.merge_range(6, col_idx, 6, col_idx+3, "ESTIMATE Cost Ratio (Rp/m2)", f_proj_th)
#                 ws.merge_range(7, col_idx, 7, col_idx+3, p["name"].upper(), f_proj_th_red)
#                 ws.write(8, col_idx, "TOTAL (Rp)", f_proj_th); ws.write(8, col_idx+1, "GBA", f_proj_th)
#                 ws.write(8, col_idx+2, "GFA", f_proj_th); ws.write(8, col_idx+3, "SGFA", f_proj_th)
                
#                 ws.write(9, col_idx, "-", f_proj_th); ws.write(9, col_idx+1, p["gba"], f_proj_th)
#                 ws.write(9, col_idx+2, p["gfa"], f_proj_th); ws.write(9, col_idx+3, p["sgfa"], f_proj_th)
#                 col_idx += 4

#             # Write Data
#             row_idx = 10
#             for row in row_map:
#                 if row.get("is_grand_total"): fmt_c, fmt_str, fmt_pct, fmt_num = f_gc, f_gL, f_gpct, f_gnum
#                 elif row.get("is_main"): fmt_c, fmt_str, fmt_pct, fmt_num = f_mc, f_mL, f_mpct, f_mnum
#                 else: fmt_c, fmt_str, fmt_pct, fmt_num = f_c, f_L, f_pct, f_num

#                 pct_val = (row["sum"] / grand_total_all_projects) if grand_total_all_projects > 0 else 0

#                 ws.write(row_idx, 0, row['sn'], fmt_c)
#                 ws.write(row_idx, 1, row['desc'], fmt_str)
#                 ws.write(row_idx, 2, row['coa'], fmt_c)
#                 ws.write(row_idx, 3, pct_val, fmt_pct)
                
#                 # Grand totals and their ratios
#                 tot_r_gba = (row["sum"] / total_gba_all) if total_gba_all > 0 else 0
#                 tot_r_gfa = (row["sum"] / total_gfa_all) if total_gfa_all > 0 else 0
#                 tot_r_sgfa = (row["sum"] / total_sgfa_all) if total_sgfa_all > 0 else 0
                
#                 ws.write(row_idx, 4, row['sum'], fmt_num)
#                 ws.write(row_idx, 5, tot_r_gba, fmt_num); ws.write(row_idx, 6, tot_r_gfa, fmt_num); ws.write(row_idx, 7, tot_r_sgfa, fmt_num)

#                 col_idx = 8
#                 for p in all_projects_data:
#                     val = p['grand'] if row['key'] == 'grand' else p['vals'][row['key']]
#                     r_gba = (val / p['gba']) if p['gba'] > 0 else 0
#                     r_gfa = (val / p['gfa']) if p['gfa'] > 0 else 0
#                     r_sgfa = (val / p['sgfa']) if p['sgfa'] > 0 else 0

#                     ws.write(row_idx, col_idx, val, fmt_num)
#                     ws.write(row_idx, col_idx+1, r_gba, fmt_num)
#                     ws.write(row_idx, col_idx+2, r_gfa, fmt_num)
#                     ws.write(row_idx, col_idx+3, r_sgfa, fmt_num)
#                     col_idx += 4

#                 row_idx += 1

#             wb.close()

#             st.download_button(
#                 label="Download Rekap as .xlsx",
#                 data=buffer_det.getvalue(),
#                 file_name="ASG_Detailed_Estimate_All_Projects.xlsx",
#                 mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                 use_container_width=True
#             )

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.title("Main Navigation")

page_choice = st.sidebar.radio(
    "Pilih Pekerjaan:",
    ["Cost Calculator", "Area Calculator", "Summary"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Daftar Proyek")

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
# elif page_choice == "Summary":
#     show_portfolio_summary()
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
