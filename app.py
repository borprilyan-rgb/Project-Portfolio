import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.graph_objects as go
import num2words as n2w

import json
import os
import tempfile

#streamlit run app.py
APP_VERSION = "1.1.0"

local_storage = None

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
    "Terrace Villa": {
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
    "Podium Villa": {
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

st.set_page_config(page_title="Project Portfolio", layout="wide")

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

#region
# Initialization
if "projects" not in st.session_state:
    stored_data = load_data()
    
    if stored_data:
        # Restore from JSON
        st.session_state.projects = stored_data["projects"]
        st.session_state.current_proj_id = stored_data["current_proj_id"]
        st.session_state.proj_counter = stored_data["proj_counter"]
        
        # Migration check (v1.0.0 -> v1.1.0)
        if stored_data.get("app_version", "1.0.0") < "1.1.0":
            for pid in st.session_state.projects:
                p_data = st.session_state.projects[pid].get("data", {})
                if "vis_land" not in p_data:
                    p_data.update({
                        "vis_land": 1000.0, "vis_floors": 5, "vis_stair": 20.0,
                        "vis_mep": 20.0, "vis_corr": 50.0, "vis_unit": 100.0,
                        "vis_lobby": 50.0, "vis_roof": 80.0, "vis_mep_out": 20.0
                    })
                    st.session_state.projects[pid]["data"] = p_data
    else:
        # Default fresh start
        st.session_state.projects = {"proj_1": {"name": "New Project 1", "type": "Hotel", "data": {}}}
        st.session_state.current_proj_id = "proj_1"
        st.session_state.proj_counter = 1
    
    st.session_state.storage_loaded = True
#endregion

def show_project_database():
    tab1, tab2 = st.tabs([
    "Database", " "
    ])

# --- TAB 1: PETUNJUK PEMAKAIAN ---
    with tab1:
        flattened_data = []
        for project_type, metrics in PROJECT_DATABASE.items():
            row = {"Project Type": project_type}
            for key, value in metrics.items():
                # Handle nested rate dictionaries (e.g., fl_ht_rate)
                if isinstance(value, dict):
                    for sub_key, sub_val in value.items():
                        row[f"{key}_{sub_key}"] = sub_val
                else:
                    row[key] = value
            flattened_data.append(row)

        # 2. Create DataFrame
        df_db = pd.DataFrame(flattened_data)

        # 3. Display in Streamlit
        st.subheader("Standard Project Database Rates")
        st.dataframe(
            df_db, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Project Type": st.column_config.TextColumn("Project Type", width="medium"),
                "struc_work": st.column_config.NumberColumn("Structure Rate", format="Rp %,.0f"),
                "arch_base": st.column_config.NumberColumn("Arch Base", format="Rp %,.0f"),
            }
        )

def show_area_calculator():
    st.title("Area Calculator")
    
    # 1. Identify the Active Project
    curr_id = st.session_state.current_proj_id
    curr_proj = st.session_state.projects[curr_id]
    
    def get_area_val(key, default=0.0):
        return curr_proj["data"].get(key, default)

    tab1, tab2 = st.tabs(["Calculator", "Trial"])
    
    with tab1:
        st.subheader("1. Detailed Area Breakdown - Floor Stacking")
        st.caption("Input your breakdown per floor. GBA, GFA, SGFA, and NFA will be calculated automatically.")

        # ==========================================
        # THE FIX: THE STATE ANCHOR
        # ==========================================
        # We isolate the base data so the data_editor doesn't reset on every keystroke.
        base_key = f"base_table_{curr_id}"
        
        if base_key not in st.session_state:
            if "area_table_data" in curr_proj["data"]:
                st.session_state[base_key] = curr_proj["data"]["area_table_data"]
            else:
                default_stack = [
                    {"FL": "Roof Machine", "Space Type": "Roof", "Parkir": 0.0, "Roof/Deck": 200.0, "MEP Outdoor": 80.0, "Koridor/Lobby": 0.0, "Stair, MEP, Etc": 790.0, "Unit": 0.0, "Office": 0.0},
                    {"FL": "Roof", "Space Type": "Roof", "Parkir": 0.0, "Roof/Deck": 200.0, "MEP Outdoor": 80.0, "Koridor/Lobby": 0.0, "Stair, MEP, Etc": 790.0, "Unit": 0.0, "Office": 0.0},
                    {"FL": "5F", "Space Type": "Unit", "Parkir": 0.0, "Roof/Deck": 0.0, "MEP Outdoor": 0.0, "Koridor/Lobby": 75.0, "Stair, MEP, Etc": 150.0, "Unit": 500.0, "Office": 0.0},
                    {"FL": "4F", "Space Type": "Unit", "Parkir": 0.0, "Roof/Deck": 0.0, "MEP Outdoor": 0.0, "Koridor/Lobby": 75.0, "Stair, MEP, Etc": 150.0, "Unit": 500.0, "Office": 0.0},
                    {"FL": "3F", "Space Type": "Unit", "Parkir": 0.0, "Roof/Deck": 0.0, "MEP Outdoor": 0.0, "Koridor/Lobby": 75.0, "Stair, MEP, Etc": 150.0, "Unit": 500.0, "Office": 0.0},
                    {"FL": "2F", "Space Type": "Unit", "Parkir": 0.0, "Roof/Deck": 0.0, "MEP Outdoor": 0.0, "Koridor/Lobby": 75.0, "Stair, MEP, Etc": 150.0, "Unit": 500.0, "Office": 0.0},
                    {"FL": "1F", "Space Type": "Lobby", "Parkir": 0.0, "Roof/Deck": 0.0, "MEP Outdoor": 20.0, "Koridor/Lobby": 75.0, "Stair, MEP, Etc": 0.0, "Unit": 500.0, "Office": 0.0}
                ]
                st.session_state[base_key] = default_stack
                curr_proj["data"]["area_table_data"] = default_stack

        # --- TOP SETUP CONTROLS ---
        with st.expander("⚙️ Quick Floor Generator", expanded=False):
            c_name, c_h, c_b, c_u = st.columns(4)
            
            # Using get_area_val ensures the data survives page reloads
            tower_name = c_name.text_input("Tower Name", value=get_area_val("tname", "1 TOWER"), key=f"wid_tname_{curr_id}")
            curr_proj["data"]["tname"] = tower_name
            
            f2f_height = c_h.number_input("Floor-to-floor (m)", value=float(get_area_val("f2f", 3.5)), step=0.1, key=f"wid_f2f_{curr_id}")
            curr_proj["data"]["f2f"] = f2f_height
            
            basements = c_b.number_input("Basements / LG", min_value=0, value=int(get_area_val("base_in", 1)), step=1, key=f"wid_base_{curr_id}")
            curr_proj["data"]["base_in"] = basements
            
            upper_floors = c_u.number_input("Upper floors", min_value=1, value=int(get_area_val("up_in", 5)), step=1, key=f"wid_up_{curr_id}")
            curr_proj["data"]["up_in"] = upper_floors
            
            if st.button("Generate Default Stack", type="primary"):
                new_data = [
                    {"FL": "Roof Machine", "Space Type": "Roof", "Parkir": 0.0, "Roof/Deck": 0.0, "MEP Outdoor": 50.0, "Koridor/Lobby": 0.0, "Stair, MEP, Etc": 150.0, "Unit": 0.0, "Office": 0.0},
                    {"FL": "Roof", "Space Type": "Roof", "Parkir": 0.0, "Roof/Deck": 200.0, "MEP Outdoor": 80.0, "Koridor/Lobby": 0.0, "Stair, MEP, Etc": 790.0, "Unit": 0.0, "Office": 0.0}
                ]
                for i in range(upper_floors, 1, -1):
                    new_data.append({"FL": f"{i}F", "Space Type": "Unit", "Parkir": 0.0, "Roof/Deck": 0.0, "MEP Outdoor": 0.0, "Koridor/Lobby": 75.0, "Stair, MEP, Etc": 150.0, "Unit": 500.0, "Office": 0.0})
                new_data.append({"FL": "1F", "Space Type": "Lobby", "Parkir": 0.0, "Roof/Deck": 0.0, "MEP Outdoor": 20.0, "Koridor/Lobby": 75.0, "Stair, MEP, Etc": 0.0, "Unit": 500.0, "Office": 0.0})
                for i in range(1, basements + 1):
                    fl_name = "LG" if i == 1 else f"B{i-1}"
                    new_data.append({"FL": fl_name, "Space Type": "Carpark", "Parkir": 800.0, "Roof/Deck": 0.0, "MEP Outdoor": 0.0, "Koridor/Lobby": 0.0, "Stair, MEP, Etc": 150.0, "Unit": 0.0, "Office": 0.0})
                
                # Update Anchor and clear editor memory
                st.session_state[base_key] = new_data
                if f"area_editor_{curr_id}" in st.session_state:
                    del st.session_state[f"area_editor_{curr_id}"]
                st.rerun()

        st.markdown(f"##### {tower_name} — Area Breakdown Editor")

        # --- TABLE UTILITY CONTROLS ---
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
        with col_btn1:
            if st.button("➕ Add floor (Top)", use_container_width=True):
                # Pull current edited state, add row, make it the new Anchor
                current_state = curr_proj["data"].get("area_table_data", [])
                insert_idx = 1 if len(current_state) > 0 and current_state[0]["FL"] == "Roof" else 0
                current_state.insert(insert_idx, {"FL": "New", "Space Type": "Unit", "Parkir": 0.0, "Roof/Deck": 0.0, "MEP Outdoor": 0.0, "Koridor/Lobby": 0.0, "Stair, MEP, Etc": 0.0, "Unit": 0.0, "Office": 0.0})
                
                st.session_state[base_key] = current_state
                if f"area_editor_{curr_id}" in st.session_state:
                    del st.session_state[f"area_editor_{curr_id}"]
                st.rerun()  

        # --- BUILD DATAFRAME FROM ANCHOR ---
        
        base_data = st.session_state.get(base_key, [])

        # ✅ Normalize area table data
        if not isinstance(base_data, list) or not base_data or not isinstance(base_data[0], dict):
            base_data = [
                {
                    "FL": "1F",
                    "Space Type": "Lobby",
                    "Parkir": 0.0,
                    "Roof/Deck": 0.0,
                    "MEP Outdoor": 0.0,
                    "Koridor/Lobby": 0.0,
                    "Stair, MEP, Etc": 0.0,
                    "Unit": 0.0,
                    "Office": 0.0
                }
            ]
            st.session_state[base_key] = base_data
            curr_proj["data"]["area_table_data"] = base_data

        df_area = pd.DataFrame(base_data)

        breakdown_cols = ["Parkir", "Roof/Deck", "MEP Outdoor", "Koridor/Lobby", "Stair, MEP, Etc", "Unit", "Office"]
        
        # FULL WIDTH EDITOR
        edited_df = st.data_editor(
            df_area,
            num_rows="dynamic",
            use_container_width=True,
            key=f"area_editor_{curr_id}",
            hide_index=True,
            column_order=["FL", "Space Type"] + breakdown_cols,
            column_config={
                "Space Type": st.column_config.SelectboxColumn("Space Type", options=["Roof", "Unit", "Lobby", "Ramp", "Carpark", "Facility"], required=True)
            }
        )

        # --- CALCULATIONS ---
        edited_df["TOTAL"] = edited_df[breakdown_cols].sum(axis=1)
        edited_df["GBA"] = edited_df["TOTAL"]
        edited_df["GFA"] = edited_df["TOTAL"] - edited_df[["Parkir", "Roof/Deck", "MEP Outdoor"]].sum(axis=1)
        edited_df["SGFA"] = edited_df[["Unit", "Office", "Koridor/Lobby"]].sum(axis=1)
        edited_df["NFA"] = edited_df[["Unit", "Office"]].sum(axis=1)
        
        # Silently update project data for CSV export without disturbing the Anchor
        curr_proj["data"]["area_table_data"] = edited_df[["FL", "Space Type"] + breakdown_cols].to_dict('records')

        st.divider()

        # [ ... Your PLOTLY code continues exactly the same from here ... ]

# ==========================================
        # VISUALIZATION DASHBOARD SECTION (PLOTLY EDITION)
        # ==========================================
        col_viz_left, col_viz_right = st.columns([1.5, 1], gap="large")

        # Crisp Web-Safe Architectural Colors
        CAT_COLORS = {
            "Unit": "#709DE1",            # Muted Blue
            "Office": "#A9C4F0",          # Light Blue
            "Koridor/Lobby": "#94C37D",   # Muted Green
            "Stair, MEP, Etc": "#F4B16A", # Soft Orange
            "Parkir": "#B7B7B7",          # Dark Gray
            "Roof/Deck": "#D9D9D9",       # Light Gray
            "MEP Outdoor": "#8C8C8C",     # Medium Gray
            "Lobby_Override": "#C17AA0"   # Muted Purple
        }

        # --- LEFT: CONCEPTUAL SECTION (PLOTLY) ---
        with col_viz_left:
            st.markdown("##### BUILDING AREA VISUALIZATION")
            
            draw_df = edited_df.iloc[::-1].reset_index(drop=True)
            floor_labels = draw_df['FL'].tolist()
            
            draw_order = ["Office", "Unit", "Koridor/Lobby", "Stair, MEP, Etc", "Parkir", "MEP Outdoor", "Roof/Deck"]

            # Initialize data structures for Plotly
            bases = {col: [] for col in draw_order}
            widths = {col: [] for col in draw_order}
            hover_texts = {col: [] for col in draw_order}
            text_labels = {col: [] for col in draw_order}
            unit_colors = [] # Special handling for Unit vs Lobby color

            # Calculate the exact starting X coordinate for each block to center the floor
            for idx, row in draw_df.iterrows():
                gba = row["GBA"]
                sp_type = str(row["Space Type"])
                
                # Center the floor mass
                curr_x = -gba / 2
                
                # Check for Lobby override
                if "Lobby" in sp_type:
                    unit_colors.append(CAT_COLORS["Lobby_Override"])
                else:
                    unit_colors.append(CAT_COLORS["Unit"])

                for col in draw_order:
                    val = row.get(col, 0)
                    if val > 0:
                        widths[col].append(val)
                        bases[col].append(curr_x)
                        
                        # Formatting hover and inside text
                        display_name = "LOBBY" if (col == "Unit" and "Lobby" in sp_type) else col
                        hover_texts[col].append(f"<b>{display_name}</b><br>{val:,.0f} m²")
                        
                        # Only show text inside if the block is relatively wide (> 10% of GBA)
                        if val / gba > 0.1:
                            short_name = "CORR" if col == "Koridor/Lobby" else ("MEP" if col in ["Stair, MEP, Etc", "MEP Outdoor"] else display_name)
                            text_labels[col].append(f"{short_name}<br>{val:,.0f}m²")
                        else:
                            text_labels[col].append("")
                            
                        curr_x += val
                    else:
                        # Append 0/empty to keep arrays aligned with the Y-axis
                        widths[col].append(0)
                        bases[col].append(0)
                        hover_texts[col].append("")
                        text_labels[col].append("")

            # Build the Plotly Figure
            fig = go.Figure()

            for col in draw_order:
                # Apply the specific color array if it's the Unit column, otherwise use standard color
                marker_color = unit_colors if col == "Unit" else CAT_COLORS.get(col, "#ffffff")
                
                fig.add_trace(go.Bar(
                    y=floor_labels,
                    x=widths[col],
                    base=bases[col],
                    name=col,
                    orientation='h',
                    marker=dict(
                        color=marker_color,
                        line=dict(color='#111111', width=1.5) # Crisp borders
                    ),
                    text=text_labels[col],
                    textposition='inside',
                    insidetextanchor='middle',
                    hoverinfo='text',
                    hovertext=hover_texts[col],
                    textfont=dict(color='black', size=11, family="Arial")
                ))

            # Layout Styling
            fig.update_layout(
                barmode='stack',
                showlegend=False,
                height=max(450, len(draw_df) * 45), # Dynamic height
                margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode='closest',
                xaxis=dict(
                    showgrid=False, 
                    zeroline=False, 
                    showticklabels=False # Hide X axis numbers to keep architectural look
                ),
                yaxis=dict(
                    showgrid=False,
                    tickfont=dict(size=14, color='black', weight='bold')
                )
            )

            # Add Ground Line
            fig.add_hline(y=-0.5, line_width=4, line_color="black")

            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# --- RIGHT: DATA SUMMARY & DISTRIBUTION (ARCHITECTURAL SPEC STYLE) ---
        with col_viz_right:
            st.markdown("##### PROJECT SUMMARY & ANALYSIS")
            
            # 1. Calculation Logic
            total_gba = edited_df["GBA"].sum()
            total_gfa = edited_df["GFA"].sum()
            total_sgfa = edited_df["SGFA"].sum()
            total_nfa = edited_df["NFA"].sum()
            total_circ = edited_df["Koridor/Lobby"].sum()
            total_serv = edited_df["Stair, MEP, Etc"].sum()
            total_non_gfa = edited_df[["Parkir", "Roof/Deck", "MEP Outdoor"]].sum().sum()
            
            # Efficiency is NFA / GFA (common QS metric)
            efficiency = (total_nfa / total_gfa * 100) if total_gfa > 0 else 0

            # 2. Create the "Spec Sheet" using Matplotlib
            # Slightly taller figure to accommodate the 5 rows comfortably
            fig_sum, ax_sum = plt.subplots(figsize=(5, 3.2))
            fig_sum.patch.set_facecolor('#ffffff')
            ax_sum.set_facecolor('#ffffff')
            
            # Y-Positions for the 5 rows
            rows = [0.80, 0.60, 0.40, 0.20, 0.00]
            row_height = 0.18
            
            # Background boxes for metrics - Colors matching your Excel reference
            ax_sum.add_patch(patches.Rectangle((0, rows[0]), 1, row_height, color='#d9ead3', zorder=1)) # Green: NFA/Efficiency
            ax_sum.add_patch(patches.Rectangle((0, rows[1]), 1, row_height, color='#f3f3f3', zorder=1)) # Gray: SGFA
            ax_sum.add_patch(patches.Rectangle((0, rows[2]), 1, row_height, color='#e6f2ff', zorder=1)) # Blue: GFA
            ax_sum.add_patch(patches.Rectangle((0, rows[3]), 1, row_height, color='#e2e2e2', zorder=1)) # Gray: GBA
            ax_sum.add_patch(patches.Rectangle((0, rows[4]), 1, row_height, color='#ffffff', zorder=1)) # White: Info

            # Text Styling
            text_params = {'ha': 'left', 'va': 'center', 'fontsize': 10, 'color': '#444', 'family': 'sans-serif'}
            val_params = {'ha': 'right', 'va': 'center', 'fontsize': 11, 'weight': 'bold', 'color': '#000'}

            # Row 1: NFA & Efficiency
            ax_sum.text(0.05, rows[0] + row_height/2, f"NFA (Efficiency: {efficiency:.1f}%)", **text_params)
            ax_sum.text(0.95, rows[0] + row_height/2, f"{total_nfa:,.0f} m²", **val_params)
            
            # Row 2: SGFA
            ax_sum.text(0.05, rows[1] + row_height/2, "SGFA (Semi-Gross Floor Area)", **text_params)
            ax_sum.text(0.95, rows[1] + row_height/2, f"{total_sgfa:,.0f} m²", **val_params)
            
            # Row 3: GFA
            ax_sum.text(0.05, rows[2] + row_height/2, "GFA (Gross Floor Area)", **text_params)
            ax_sum.text(0.95, rows[2] + row_height/2, f"{total_gfa:,.0f} m²", **val_params)
            
            # Row 4: GBA
            ax_sum.text(0.05, rows[3] + row_height/2, "GBA (Gross Building Area)", **text_params)
            ax_sum.text(0.95, rows[3] + row_height/2, f"{total_gba:,.0f} m²", **val_params)
            
            # Row 5: Building Info
            ax_sum.text(0.05, rows[4] + row_height/2, f"DATA SUMMARY: {len(edited_df)} Total Floors", 
                        ha='left', va='center', fontsize=9, color='#777', style='italic')

            ax_sum.set_xlim(0, 1)
            ax_sum.set_ylim(-0.05, 1.05)
            ax_sum.axis('off')
            st.pyplot(fig_sum)

            st.markdown("##### AREA DISTRIBUTION (%)")

            # 3. Distribution Bar Chart
            fig2, ax2 = plt.subplots(figsize=(5, 3.5))
            fig2.patch.set_facecolor('#ffffff')
            
            categories = ['NFA', 'Circ.', 'Services', 'Non-GFA']
            values = [total_nfa, total_circ, total_serv, total_non_gfa]
            colors = [CAT_COLORS["Unit"], CAT_COLORS["Koridor/Lobby"], CAT_COLORS["Stair, MEP, Etc"], CAT_COLORS["Roof/Deck"]]
            percentages = [(v / total_gba * 100) if total_gba > 0 else 0 for v in values]

            bars = ax2.bar(categories, percentages, color=colors, edgecolor='#111', linewidth=1.2, width=0.6)

            for bar, pct in zip(bars, percentages):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 1, f'{pct:.1f}%', 
                         ha='center', va='bottom', fontsize=10, weight='bold')

            ax2.set_ylim(0, max(percentages) + 15 if max(percentages) > 0 else 100)
            ax2.axis('off')
            
            # Add category labels manually to keep it clean
            for i, cat in enumerate(categories):
                ax2.text(i, -max(percentages)*0.1, cat, ha='center', fontsize=9, weight='bold', color='#444')

            st.pyplot(fig2, use_container_width=True)

    with tab2:
        st.subheader("2. Top-Down Feasibility Estimator")
        st.caption("Hitung cepat kebutuhan GBA dan GFA berdasarkan target unit penjualan dan efisiensi.")

        col_t1, col_t2, col_t3 = st.columns(3)

        with col_t1:
            st.markdown("#### 1. Target Penjualan (NFA)")
            target_units = st.number_input("Target Jumlah Unit", min_value=1, value=500, step=10, key="td_units")
            avg_unit_size = st.number_input("Rata-rata Luas Unit (m²)", min_value=10.0, value=35.0, step=1.0, key="td_avg_size")
            
            # Math: Target NFA
            est_nfa = target_units * avg_unit_size
            st.info(f"**Total NFA:** {est_nfa:,.0f} m²")

        with col_t2:
            st.markdown("#### 2. Efisiensi Bangunan (GFA)")
            target_efficiency = st.slider("Target Efisiensi Floorplate (%)", min_value=60, max_value=95, value=82, step=1, help="NFA dibagi GFA. Standar Apartemen ~82-85%.", key="td_eff")
            
            # Math: GFA based on efficiency
            est_gfa = est_nfa / (target_efficiency / 100)
            core_area = est_gfa - est_nfa
            st.info(f"**Total GFA:** {est_gfa:,.0f} m²\n\n*(Core/Sirkulasi: {core_area:,.0f} m²)*")

        with col_t3:
            st.markdown("#### 3. Kebutuhan Parkir (GBA)")
            lot_ratio = st.number_input("Rasio Parkir (Lot/Unit)", min_value=0.0, value=0.5, step=0.1, help="Misal 0.5 = 1 lot untuk 2 unit.", key="td_ratio")
            m2_per_lot = st.number_input("Luas GBA per Lot (m²)", min_value=15.0, value=30.0, step=1.0, help="Termasuk ramp & jalan. Standar ~28-30m².", key="td_m2_lot")
            
            # Math: Parking & GBA
            req_lots = target_units * lot_ratio
            parking_gba = req_lots * m2_per_lot
            est_gba = est_gfa + parking_gba
            st.info(f"**Total GBA:** {est_gba:,.0f} m²\n\n*(Kebutuhan: {req_lots:,.0f} Lot)*")

        st.markdown("---")
        
        # --- SUMMARY DASHBOARD ---
        st.markdown("### Ringkasan Area Makro")
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("GBA (Gross Building Area)", f"{est_gba:,.0f} m²", help="Total area terbangun termasuk parkir.")
        sc2.metric("GFA (Gross Floor Area)", f"{est_gfa:,.0f} m²", help="Total area tertutup (Unit + Core).")
        sc3.metric("NFA (Net Floor Area)", f"{est_nfa:,.0f} m²", help="Total area yang bisa dijual/disewakan.")
        sc4.metric("Kapasitas Parkir", f"{req_lots:,.0f} Mobil", help=f"Berdasarkan rasio {lot_ratio} lot per unit.")

        # --- PROPORTIONAL VISUALIZATION ---
        st.markdown("#### Proporsi Area Terbangun (GBA Breakdown)")
        st.caption("Visualisasi ini menunjukkan berapa banyak area non-jual (Core & Parkir) yang harus dibangun untuk mendukung target NFA Anda.")
        
        # A clean horizontal stacked bar chart using matplotlib
        fig, ax = plt.subplots(figsize=(10, 2.5))
        
        # Plotting [NFA] + [Core] + [Parking] = GBA
        ax.barh(0, est_nfa, color='#FAD7A0', edgecolor='black', label=f'NFA (Sellable)')
        ax.barh(0, core_area, left=est_nfa, color='#AED6F1', edgecolor='black', label=f'Core & Sirkulasi')
        ax.barh(0, parking_gba, left=(est_nfa + core_area), color='#95A5A6', edgecolor='black', label=f'Area Parkir / Podium')
        
        # Adding text labels inside the bars
        if est_nfa > (est_gba * 0.05): # Only show text if the bar is wide enough
            ax.text(est_nfa/2, 0, f"NFA\n{est_nfa:,.0f} m²\n({(est_nfa/est_gba*100):.1f}%)", ha='center', va='center', fontsize=9, weight='bold')
        if core_area > (est_gba * 0.05):
            ax.text(est_nfa + core_area/2, 0, f"CORE\n{core_area:,.0f} m²\n({(core_area/est_gba*100):.1f}%)", ha='center', va='center', fontsize=9)
        if parking_gba > (est_gba * 0.05):
            ax.text(est_nfa + core_area + parking_gba/2, 0, f"PARKIR\n{parking_gba:,.0f} m²\n({(parking_gba/est_gba*100):.1f}%)", ha='center', va='center', fontsize=9, color='white', weight='bold')

        # Clean up the chart
        ax.set_yticks([])
        ax.set_xlim(0, est_gba * 1.02)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_xlabel("Total Area Terbangun (m²)")
        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=3, frameon=False)
        
        st.pyplot(fig)

            
def update_price(metric_key, db_key):
    """Update flooring price based on spec radio selection."""
    c_id = st.session_state.current_proj_id
    
    # 1. Safety check: Ensure the project actually exists
    if c_id not in st.session_state.projects:
        return 

    p_type = st.session_state.projects[c_id]["type"]
    c_type_key = f"{c_id}_{p_type}"
    widget_key = f"temp_spec_{metric_key}_{c_type_key}"
    
    # 2. Use .get() to securely fetch the value without throwing a KeyError
    selected_spec = st.session_state.get(widget_key)
    
    # 3. If the widget was destroyed or doesn't exist, quietly exit
    if selected_spec is None:
        return

    # 4. Proceed with normal update
    st.session_state.projects[c_id]["data"][f"{metric_key}_spec_type"] = selected_spec
    db_val = PROJECT_DATABASE.get(p_type, {}).get(db_key, {})
    
    if isinstance(db_val, dict):
        new_val = db_val.get(selected_spec, 0.0)
        st.session_state[f"u_fl_{metric_key}_{c_type_key}"] = float(new_val)

def show_cost_estimator():
    st.title("Cost Calculator")

    st.markdown("""
        <style>
            .metric-container {
                position: relative;
                display: inline-block;
                width: 100%;
            }
            .custom-tooltip {
                visibility: hidden;
                width: 240px;
                background-color: #FFFFFF;
                color: #262730;
                text-align: left;
                border-radius: 8px;
                padding: 12px;
                position: absolute;
                z-index: 1000;
                bottom: 110%; 
                left: 50%;
                transform: translateX(-50%);
                opacity: 0;
                transition: opacity 0.3s;
                font-size: 12px;
                border: 1px solid #CDDC39;
                box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
                line-height: 1.5;
            }
            .metric-container:hover .custom-tooltip {
                visibility: visible;
                opacity: 1;
            }
            /* Triangle arrow for tooltip */
            .custom-tooltip::after {
                content: "";
                position: absolute;
                top: 100%;
                left: 50%;
                margin-left: -5px;
                border-width: 5px;
                border-style: solid;
                border-color: #262730 transparent transparent transparent;
            }
        </style>
        """, unsafe_allow_html=True)

    # --- NEW: REUSABLE CARD HELPER ---
    def draw_hover_card(label, display_val, raw_val, color, formula):
        box_base = f"margin-bottom: 12px; padding: 8px; border-radius: 5px; background-color: #FFFFFF; border: 1px solid #E0E0E0; border-left: 5px solid {color};"
        label_style = "font-size: 12px; color: #666666; font-weight: bold;"
        val_style = "font-size: 14px; font-weight: bold; color: #000000; margin-top: 4px;"
        
        st.markdown(f"""
        <div class="metric-container">
            <div style="{box_base}">
                <div style="{label_style}">{label}</div>
                <div style="{val_style}">{display_val}</div>
                <div style="font-size: 10px; color: #888888; margin-top: 2px;">Rp {raw_val:,.0f}</div>
            </div>
            <div class="custom-tooltip">
                <strong style="color:{color}; font-size:13px;">Calculation Logic:</strong><br>
                {formula}
            </div>
        </div>
        """, unsafe_allow_html=True)

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
    curr_type = curr_proj["type"]
    pt_data = PROJECT_DATABASE[curr_type]
    curr_type_key = f"{curr_id}_{curr_type}"

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
            
            # Button for Current Project
            st.download_button(
                label=f"Download {curr_proj['name']} only",
                data=csv_buffer,
                file_name=f"Project_{curr_id}.csv",
                mime="text/csv",
                use_container_width=True
            )

            # Button for Global Database
            st.download_button(
                label="Download All Projects ",
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

            f_mult = (1 + (fl_waste/100)) * (1 + (fl_skirt/100))
        
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
                c1.caption(f"""Hitungan: {fl_ht_pct}% of GFA x Rp {fl_ht_rate:,.0f} x {gfa:,.0f} m2 x {f_mult}  \n  Total HT: Rp {gfa * (fl_ht_pct / 100) * fl_ht_rate * f_mult:,.0f}  \n  Terbilang: {n2w(gfa * (fl_ht_pct / 100) * fl_ht_rate * f_mult)}""")

            with c2:
                st.radio("Spek Vinyl", ["Type1", "Type2"],
                    key=f"temp_spec_vin_{curr_type_key}",
                    horizontal=True,
                    on_change=update_price, args=("vin", "fl_vinyl_rate"))
                fl_vinyl_rate = st.number_input("Vinyl Rate (Rp)",
                                                value=get_val("u_fl_vin", pt_data["fl_vinyl_rate"]["Type1"]),
                                                key=f"u_fl_vin_{curr_type_key}")
                c2.caption(f"""Hitungan: {fl_vinyl_pct}% of GFA x Rp {fl_vinyl_rate:,.0f} x {gfa:,.0f} m2 x {f_mult}  \n  Total Vinyl: Rp {gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * f_mult:,.0f}  \n  Terbilang: {n2w(gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * f_mult)}""")
            
            with c3:
                st.radio("Spek Marmer", ["Type1", "Type2"],
                    key=f"temp_spec_mar_{curr_type_key}",
                    horizontal=True,
                    on_change=update_price, args=("mar", "fl_marmer_rate"))
                fl_marmer_rate = st.number_input("Marmer Rate (Rp)",
                                                value=get_val("u_fl_mar", pt_data["fl_marmer_rate"]["Type1"]),
                                                key=f"u_fl_mar_{curr_type_key}")
                c3.caption(f"""Hitungan: {fl_marmer_pct}% of GFA x Rp {fl_marmer_rate:,.0f} x {gfa:,.0f} m2 x {f_mult}  \n  Total Marmer: Rp {gfa * (fl_marmer_pct / 100) * fl_marmer_rate * f_mult:,.0f}  \n  Terbilang: {n2w(gfa * (fl_marmer_pct / 100) * fl_marmer_rate * f_mult)}""")
                
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
            c1.caption(f"""Hitungan: {res_fac_m2:,.0f} m2 x Rp {fac_res_rate:,.0f}  \n  Total Resident Facilities: Rp {res_fac_m2 * fac_res_rate:,.0f}  \n  Terbilang: {n2w(res_fac_m2 * fac_res_rate)}""")
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

    with tab7:
        tab1, tab2, tab3, tab4 = st.tabs([
        "Hasil",
        "Tabel", "Chart", "Experimental"
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
                    <div style="font-size: 12px; color: #888888; margin-top: 8px;">
                        Rp {grand_total_hc:,.2f} + Rp {total_soft_cost:,.2f} =
                    </div>
                    <div style="font-size: clamp(24px, 4vw, 30px); font-weight: bold; color: #000000; line-height: 1.2; margin-top: 10px;">
                        Rp {grand_total_project:,.2f}
                    </div>
                    <div style="font-size: 16px; color: #888888; margin-top: 8px;">
                        Terbilang: {n2w(grand_total_project)} Rupiah
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
    with tab2:
        if 'show_details' not in st.session_state:
            st.session_state.show_details = True

        # 2. Add the Toggle Button
        label = "Hide Details" if st.session_state.show_details else "Show Details"
        if st.button(label):
            st.session_state.show_details = not st.session_state.show_details
            st.rerun()

        # 3. Define the full dataset as a Dictionary
        data_dict = {
            # --- MAIN CONSTRUCTION ---
            "1. Preliminary Works": t_preliminary,
            "2. Earthwork": t_earth,
            "3. Foundation": t_found,
            "4. Structural Work": t_struc,
            
            # --- ARCHITECTURE ---
            "5. Total Architecture": group_arch,
            "5.1 Basic Architecture": t_arch_base,
            "5.2 Facade - Precast": t_precast,
            "5.3 Facade - Window Wall": t_window,
            "5.4 Facade - Double Skin": t_double,
            "5.5 Wooden Doors": t_w_door,
            "5.6 Glass Doors": t_g_door,
            "5.7 Steel Doors": t_s_door,
            "5.8 Lobby Interior": t_lobby,
            "5.9 Gondola": t_gondola,
            "5.10 Typical Unit Sanitary": t_unit_san,
            "5.11 Public Toilet Male": t_t_male,
            "5.12 Public Toilet Female": t_t_female,
            "5.13 Disabled Toilet": t_t_dis,
            "5.14 Mushola": t_mushola,
            "5.15 Kitchen Equipment": t_kitchen,
            "5.16 Hardware Pintu Kayu": t_hw_w,
            "5.17 Hardware Pintu Besi": t_hw_s,
            "5.18 HT/Ceramic Tile": t_ht,
            "5.19 Vinyl Flooring": t_vinyl,
            "5.20 Marmer Flooring": t_marmer,
            "5.21 Carpet Work": t_carpet,
            "5.22 Railing Work": t_railing,
            "5.23 Skylight Work": t_skylight,
            "5.24 Glass Work": t_glass_work,
            "5.25 Custom Item (Architecture)": smart_custom_costs,

            # --- FF&E & SERVICES ---
            "6. Total FF&E": group_ffe,
            "6.1 FF&E": t_ffe,
            "6.2 Misc. (Linen/Gym)": t_misc,
            "7. MEP Works": t_mep,
            "8. Utility Connection": t_utility,

            # --- EXTERNAL & FACILITIES ---
            "9. External Works": t_external,
            "10. Miscellanous/Facility": group_misc,
            "10.1 Public Facilities": t_pub_fac,
            "10.2 Resident Facilities": t_res_fac,
            "10.3 Project Facilities": t_proj_fac,

            # --- CONTINGENCY ---
            "11. Contingencies": t_contingency,

            # --- SOFT COSTS / CONSULTANTS ---
            "12. Consultancy Fee": t_consultancy,
            "13. Quantity Surveyor": t_qs,
            "14. Project Management": t_pm,
            "15. Insurance Coverage": t_insurance
        }

        # 4. Extract into lists for your DataFrame automatically
        original_descriptions = list(data_dict.keys())
        raw_amounts = list(data_dict.values())

        # 4. Filter and Indent Logic
        filtered_data = []
        major_numbers = [f"{i}. " for i in range(1, 16)]

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
            hover = alt.selection_point(on='mouseover', nearest=True, fields=['Item'], empty=False)

            detailed_chart = alt.Chart(df_detailed).mark_bar().encode(
                x=alt.X("Amount:Q", title="Cost (Rp)"),
                y=alt.Y("Item:N", sort="-x", title=""),
                opacity=alt.condition(hover, alt.value(1), alt.value(0.7)),
                color=alt.Color("Type:N", scale=alt.Scale(domain=['Hard Cost', 'Soft Cost'], range=["#1f77b4", "#c2a136"])),
                tooltip=["Item", "Type", alt.Tooltip("Amount:Q", format=",.2f")]
            ).properties(height=chart_height).add_params(hover)

            st.altair_chart(detailed_chart, use_container_width=True)

    with tab4:
        with st.expander("Detail Hard Cost", expanded=False):
            cs1, cs2, cs3, cs4, cs5, cs6 = st.columns(6)

            with cs1:
                draw_hover_card("Preliminary", n2w(group_prelim), group_prelim, "#CDDC39", 
                                f"5% × Subtotal Construction (Rp {construction_subtotal:,.0f})")
            
            with cs2:
                draw_hover_card("Earthwork", n2w(group_earth), group_earth, "#8BC34A", 
                                f"GBA ({gba:,.0f} m2) × Rate (Rp {struc_earth:,.0f})")
            
            with cs3:
                draw_hover_card("Utility", n2w(group_utility), group_utility, "#4CAF50", 
                                f"GBA ({gba:,.0f} m2) × Rate (Rp {utility_rate:,.0f})")
            
            with cs4:
                draw_hover_card("Foundation", n2w(group_found), group_found, "#689F38", 
                                f"GBA ({gba:,.0f} m2) × Rate (Rp {struc_found:,.0f})")
            
            with cs5:
                draw_hover_card("Structural", n2w(group_struc), group_struc, "#388E3C", 
                                f"GBA ({gba:,.0f} m2) × Rate (Rp {struc_work:,.0f})")
            
            with cs6:
                draw_hover_card("External Works", n2w(group_ext), group_ext, "#254E18", 
                                f"Landscape ({land_m2:,.0f} m2) × Rate (Rp {ext_land_rate:,.0f})")

            # --- ROW 2 ---
            ct1, ct2, ct3, ct4, ct5, ct6 = st.columns(6)
            
            with ct2:
                draw_hover_card("Architecture", n2w(group_arch), group_arch, "#9CCC65", 
                                "Base Arch + Facade + Sanitary + Flooring + Custom Items")
            
            with ct3:
                draw_hover_card("Miscellaneous", n2w(group_misc), group_misc, "#558B2F", 
                                "Public Fac. + Resident Fac. + Project Fac.")
            
            with ct4:
                draw_hover_card("FF & E", n2w(group_ffe), group_ffe, "#2E7D32", 
                                f"({rooms:,.0f} Units × FF&E Rate: Rp {ffe_rate:,.0f})\n"
                                f"+ Misc. Linen/Gym: (Rp {misc_rate*misc_switch:,.0f})")

            with ct5:
                draw_hover_card("MEP Works", n2w(group_mep), group_mep, "#33691E", 
                                f"GBA ({gba:,.0f} m2) × Rate (Rp {mep_rate:,.0f})")

            with ct6:
                draw_hover_card("Contingency", n2w(group_conting), group_conting, "#1B5E20", 
                                f"3% × (Construction + Prelim) (Rp {construction_subtotal + t_preliminary:,.0f})")

# --- SAVE ALL METRICS TO SESSION STATE ---
    # We use .update() so we NEVER delete the Area Calculator's data!
    st.session_state.projects[curr_id]["data"].update({
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
    })


    with tab8:
            st.header("Detail Pembuktian & Logika Perhitungan")

            # Group 1: Structural Audit
            with st.expander("1. Struktur & Pondasi", expanded=True):
                audit_struc = pd.DataFrame([
                    {"Item": "Earthwork", "Formula": f"GBA ({gba:,.0f} m2) × Rate (Rp {struc_earth:,.0f})", "Total": t_earth},
                    {"Item": "Foundation", "Formula": f"GBA ({gba:,.0f} m2) × Rate (Rp {struc_found:,.0f})", "Total": t_found},
                    {"Item": "Structural Work", "Formula": f"GBA ({gba:,.0f} m2) × Rate (Rp {struc_work:,.0f})", "Total": t_struc},
                ])
                st.table(audit_struc.style.format({"Total": "Rp {:,.2f}"}))

            # Group 2: Architectural Base & Facade Audit
            with st.expander("2. Arsitektur Dasar & Fasad"):
                audit_arch = pd.DataFrame([
                    {"Item": "Architecture Base", "Formula": f"GFA ({gfa:,.0f} m2) × Rate (Rp {arch_base:,.0f})", "Total": t_arch_base},
                    {"Item": "Facade Precast", "Formula": f"Facade ({facade:,.0f} m2) × {facade_precast_pct}% × Rate (Rp {fac_precast_rate:,.0f})", "Total": t_precast},
                    {"Item": "Facade Window Wall", "Formula": f"Facade ({facade:,.0f} m2) × {facade_window_pct}% × Rate (Rp {fac_window_rate:,.0f})", "Total": t_window},
                    {"Item": "Facade Double Skin", "Formula": f"Facade ({facade:,.0f} m2) × {facade_double_pct}% × Rate (Rp {fac_double_rate:,.0f})", "Total": t_double},
                ])
                st.table(audit_arch.style.format({"Total": "Rp {:,.2f}"}))

            # Group 3: Doors & Hardware
            with st.expander("3. Pintu & Hardware"):
                audit_door = pd.DataFrame([
                    {"Item": "Wooden Door", "Formula": f"{wooden_door:,.0f} Unit × Rate (Rp {door_wood:,.0f})", "Total": t_w_door},
                    {"Item": "Glass Door", "Formula": f"{glass_door:,.0f} Unit × Rate (Rp {door_glass:,.0f})", "Total": t_g_door},
                    {"Item": "Steel Door", "Formula": f"{steel_door:,.0f} Unit × Rate (Rp {door_steel:,.0f})", "Total": t_s_door},
                    {"Item": "Hardware Wooden Door", "Formula": f"{wooden_door:,.0f} Unit × Rate (Rp {hw_wood:,.0f})", "Total": t_hw_w},
                    {"Item": "Hardware Steel Door", "Formula": f"{steel_door:,.0f} Unit × Rate (Rp {hw_steel:,.0f})", "Total": t_hw_s},
                ])
                st.table(audit_door.style.format({"Total": "Rp {:,.2f}"}))

            # Group 4: Sanitary Audit
            with st.expander("4. Sanitari"):
                audit_san = pd.DataFrame([
                    {"Item": "Typical Unit Sanitary", "Formula": f"{rooms:,.0f} Rooms × {san_qty_room} Unit/Room × Rate (Rp {san_room_rate:,.0f})", "Total": t_unit_san},
                    {"Item": "Public Toilet Male", "Formula": f"{toilet_male:,.0f} Unit × Rate (Rp {san_pub_m:,.0f})", "Total": t_t_male},
                    {"Item": "Public Toilet Female", "Formula": f"{toilet_female:,.0f} Unit × Rate (Rp {san_pub_f:,.0f})", "Total": t_t_female},
                    {"Item": "Disabled Toilet", "Formula": f"{disabled_toil:,.0f} Unit × Rate (Rp {san_dis:,.0f})", "Total": t_t_dis},
                    {"Item": "Mushola", "Formula": f"{mushola_unit:,.0f} Unit × Rate (Rp {san_mushola:,.0f})", "Total": t_mushola},
                ])
                st.table(audit_san.style.format({"Total": "Rp {:,.2f}"}))

            # Group 5: Flooring Logic (Waste & Skirting Proof)
            with st.expander("5. Lantai (Termasuk Waste & Skirting)"):
                st.markdown(fr"""
                **Rumus Pengali Lantai (f_mult):**  
                $(1 + \text{{Waste}} \%) \times (1 + \text{{Skirting}} \%) = (1 + {fl_waste/100}) \times (1 + {fl_skirt/100}) = **{f_mult:.4f}**$
                """)
                audit_floor = pd.DataFrame([
                    {"Item": "HT / Tile", "Formula": f"GFA ({gfa:,.0f} m2) × {fl_ht_pct}% × {f_mult:.4f} × Rate (Rp {fl_ht_rate:,.0f})", "Total": t_ht},
                    {"Item": "Vinyl", "Formula": f"GFA ({gfa:,.0f} m2) × {fl_vinyl_pct}% × {f_mult:.4f} × Rate (Rp {fl_vinyl_rate:,.0f})", "Total": t_vinyl},
                    {"Item": "Marmer", "Formula": f"GFA ({gfa:,.0f} m2) × {fl_marmer_pct}% × {f_mult:.4f} × Rate (Rp {fl_marmer_rate:,.0f})", "Total": t_marmer},
                ])
                st.table(audit_floor.style.format({"Total": "Rp {:,.2f}"}))

            # Group 6: Finishing & Interior Misc
            with st.expander("6. Finishing, Interior & Lainnya"):
                audit_fin = pd.DataFrame([
                    {"Item": "Lobby Interior", "Formula": f"{lobby_interior:,.0f} m2 × Rate (Rp {lobby_rate:,.0f})", "Total": t_lobby},
                    {"Item": "Carpet Work", "Formula": f"{carpet_m2:,.0f} m2 × Rate (Rp {carpet_rate:,.0f})", "Total": t_carpet},
                    {"Item": "Glass Work", "Formula": f"{glass_m2:,.0f} m2 × Rate (Rp {glass_rate:,.0f})", "Total": t_glass_work},
                    {"Item": "Skylight", "Formula": f"{skylight_area:,.0f} m2 × Rate (Rp {skylight_rate:,.0f})", "Total": t_skylight},
                    {"Item": "Railing", "Formula": f"({rooms:,.0f} Rooms × {railing_qty} m'/room) × Rate (Rp {railing_rate:,.0f})", "Total": t_railing},
                    {"Item": "Gondola", "Formula": f"{gondola_unit:,.0f} Unit × Rate (Rp {gondola_rate:,.0f})", "Total": t_gondola},
                ])
                st.table(audit_fin.style.format({"Total": "Rp {:,.2f}"}))

            # Group 7: MEP, Dapur & FF&E
            with st.expander("7. MEP, Dapur & FF&E"):
                audit_mep = pd.DataFrame([
                    {"Item": "MEP Works", "Formula": f"GBA ({gba:,.0f} m2) × Rate (Rp {mep_rate:,.0f})", "Total": t_mep},
                    {"Item": "Utility Connection", "Formula": f"GBA ({gba:,.0f} m2) × Rate (Rp {utility_rate:,.0f})", "Total": t_utility},
                    {"Item": "FF&E", "Formula": f"{rooms:,.0f} Rooms × Rate (Rp {ffe_rate:,.0f})", "Total": t_ffe},
                    {"Item": "Kitchen Equipment", "Formula": f"{rooms:,.0f} Rooms × Rate (Rp {kitchen_rate:,.0f})", "Total": t_kitchen},
                    {"Item": "Misc (Linen/Gym)", "Formula": f"Switch ({misc_switch}) × Rate (Rp {misc_rate:,.0f})", "Total": t_misc},
                ])
                st.table(audit_mep.style.format({"Total": "Rp {:,.2f}"}))

            # Group 8: External & Facilities
            with st.expander("8. Fasilitas & Area Eksternal"):
                audit_ext = pd.DataFrame([
                    {"Item": "External Works (Landscape)", "Formula": f"{land_m2:,.0f} m2 × Rate (Rp {ext_land_rate:,.0f})", "Total": t_external},
                    {"Item": "Public Facilities", "Formula": f"{pub_fac_m2:,.0f} m2 × Rate (Rp {fac_pub_rate:,.0f})", "Total": t_pub_fac},
                    {"Item": "Resident Facilities", "Formula": f"GFA ({gfa:,.0f} m2) × Rate (Rp {fac_res_rate:,.0f})", "Total": t_res_fac},
                    {"Item": "Project Facilities", "Formula": f"{proj_fac_u:,.0f} Unit × Rate (Rp {fac_proj_rate:,.0f})", "Total": t_proj_fac},
                ])
                st.table(audit_ext.style.format({"Total": "Rp {:,.2f}"}))

            # Group 9: Markups (Prelim & Contingency)
            with st.expander("9. Preliminaries & Contingency"):
                audit_markup = pd.DataFrame([
                    {"Item": "Preliminary Works", "Formula": f"Construction Subtotal (Rp {construction_subtotal:,.0f}) × 5%", "Total": t_preliminary},
                    {"Item": "Contingencies", "Formula": f"(Subtotal + Prelim) (Rp {construction_subtotal + t_preliminary:,.0f}) × 3%", "Total": t_contingency},
                ])
                st.table(audit_markup.style.format({"Total": "Rp {:,.2f}"}))

            # Group 10: Soft Costs (Consultants & Insurance)
            with st.expander("10. Soft Costs (Consultants, QS, PM, Insurance)"):
                audit_soft = pd.DataFrame([
                    {"Item": "Consultancy Fee", "Formula": f"GFA ({gfa:,.0f} m2) × Rate (Rp {consultancy_rate:,.0f})", "Total": t_consultancy},
                    {"Item": "QS Services", "Formula": f"{qs_months} Months × Rate (Rp {qs_rate:,.0f})", "Total": t_qs},
                    {"Item": "PM Services", "Formula": f"{pm_months} Months × Rate (Rp {pm_rate:,.0f})", "Total": t_pm},
                    {"Item": "Insurance Coverage", "Formula": f"Total Hard Cost (Rp {grand_total_hc:,.0f}) × {insurance_pct}%", "Total": t_insurance},
                ])
                st.table(audit_soft.style.format({"Total": "Rp {:,.2f}"}))
                
            # Group 11: Custom Items Tracker
            with st.expander("11. Item Tambahan (Custom)"):
                if smart_custom_costs > 0:
                    st.markdown(f"**Total Item Tambahan:** Rp {smart_custom_costs:,.2f}")
                    for detail in breakdown_details:
                        st.markdown(f"- {detail}")
                else:
                    st.info("Tidak ada item tambahan (custom) yang dimasukkan.")

# ==========================================
# SIDEBAR & GLOBAL NAVIGATION
# ==========================================
st.sidebar.title("Main Navigation")

page_choice = st.sidebar.radio(
    "Pilih Pekerjaan:",
    ["Cost Calculator", "Area Calculator", "Database"]
)

st.sidebar.markdown("---")

proj_ids = list(st.session_state.projects.keys())
proj_labels = [f"{st.session_state.projects[pid]['name']} ({st.session_state.projects[pid]['type']})" for pid in proj_ids]
current_index = proj_ids.index(st.session_state.current_proj_id) if st.session_state.current_proj_id in proj_ids else 0

curr_id = st.session_state.current_proj_id
curr_proj = st.session_state.projects[curr_id]

new_name = st.sidebar.text_input("Nama Proyek", value=curr_proj["name"], key=f"sb_name_{curr_id}")

types_list = ["Hotel", "Retail", "Apartment", "Parking", "Luxury Apartment", "Apartment2", "Hotel 3 Star", "Retail2", "Terrace Villa", "Podium Villa", "Parking2"]
type_index = types_list.index(curr_proj["type"]) if curr_proj["type"] in types_list else 0
new_type = st.sidebar.selectbox("Jenis Proyek", types_list, index=type_index, key=f"sb_type_{curr_id}")

needs_rerun = False
if new_name != curr_proj["name"]:
    st.session_state.projects[curr_id]["name"] = new_name
    needs_rerun = True

if new_type != curr_proj["type"]:
    st.session_state.projects[curr_id]["type"] = new_type
    st.session_state.projects[curr_id]["data"] = {} # Clear old rates on type change
    needs_rerun = True

if needs_rerun:
    st.rerun()

st.sidebar.subheader("Daftar Proyek")
st.sidebar.radio(
    "Active Project:",
    options=proj_labels,
    index=current_index,
    key="project_selector",
    on_change=cb_switch_project,
    label_visibility="collapsed"
)

c1, c2 = st.sidebar.columns(2)

with c1:
    st.button("Tambah", on_click=cb_add_project, type="primary", use_container_width=True)

with c2:
    can_delete = len(st.session_state.projects) > 1
    st.button("Hapus", disabled=not can_delete, on_click=cb_delete_project, type="secondary", help="Delete Active Project", use_container_width=True)

# --- NEW: GLOBAL PROJECT EDITOR IN SIDEBAR ---
st.sidebar.markdown("---")


# --- PAGE ROUTING ---
if page_choice == "Area Calculator":
    show_area_calculator()
elif page_choice == "Database":
    show_project_database()
else:
    show_cost_estimator()

# --- BACKUP SYSTEM ---
if "projects" in st.session_state and st.session_state.get("storage_loaded", False):
    backup_payload = {
        "app_version": APP_VERSION,
        "projects_dict": st.session_state.projects,
        "current_proj_id": st.session_state.current_proj_id,
        "proj_counter": st.session_state.proj_counter
    }

    # Local storage disabled
    pass

st.sidebar.caption(f"v{APP_VERSION} | © 2026 QS & Procurement - ASG")

if st.session_state.get("storage_loaded", False):
    save_data()
