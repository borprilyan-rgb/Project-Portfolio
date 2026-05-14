#region --- LIBRARY AND SUCH ---
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.graph_objects as go
import num2words as n2w
import ast
import numpy as np
import textwrap
import io
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
import json as _json
import os
import tempfile
import base64
from io import BytesIO

APP_VERSION = "1.1.0" #app version for future compatibility check
st.set_page_config(page_title="Project Feasibility Study - Agung Sedayu Group",
                    layout="wide", page_icon="Agung-Sedayu.png",)

st.logo("Agung-Sedayu-Group.png")
#endregion

#region --- DO NOT CHANGE (OR I WILL KICK YOUR BUTT)---
from supabase import create_client, Client
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def force_recalculate_all_projects():
    """Loops through all projects and updates their final totals in the session state."""
    for pid, pdata in st.session_state.projects.items():
        d = pdata.get("data", {})
        curr_type = pdata.get("type", "Hotel")
        pt_data = PROJECT_DATABASE.get(curr_type, {})

        def get_val(key, default=0.0):
            val = d.get(key, default)
            if isinstance(val, list): return val
            try: return float(val)
            except: return val

        # 1. Area Calc
        area_table = get_val("area_table_data", [])
        if isinstance(area_table, list) and len(area_table) > 0:
            calc_gba = calc_gfa = calc_sgfa = 0.0
            for row in area_table:
                row_total = sum(float(row.get(c, 0)) for c in ["Parkir", "Roof/Deck", "MEP Outdoor", "Koridor/Lobby", "Stair, MEP, Etc", "Unit", "Office"])
                calc_gba += row_total
                calc_gfa += row_total - sum(float(row.get(c, 0)) for c in ["Parkir", "Roof/Deck", "MEP Outdoor"])
                calc_sgfa += sum(float(row.get(c, 0)) for c in ["Unit", "Office", "Koridor/Lobby"])
        else:
            calc_gba = get_val("m_gba", 0.0)
            calc_gfa = get_val("m_gfa", 0.0)
            calc_sgfa = get_val("m_sgfa", 0.0)

        # 2. Cost Calc (Simplified core drivers)
        struc_earth = get_val("u_earth", pt_data.get("struc_earth", 0))
        struc_found = get_val("u_found", pt_data.get("struc_found", 0))
        struc_work = get_val("u_struc", pt_data.get("struc_work", 0))
        arch_base = get_val("u_arch", pt_data.get("arch_base", 0))
        facade = get_val("m_facade", 0.0)
        fac_precast_pct = get_val("r_fac_pre", pt_data.get("facade_precast_pct", 0))
        fac_precast_rate = get_val("u_f_pre", pt_data.get("facade_precast_rate", 0))
        rooms = get_val("m_rooms", 0.0)
        ffe_rate = get_val("u_ffe", pt_data.get("ffe", 0))
        mep_rate = get_val("u_mep", pt_data.get("mep", 0))
        utility_rate = get_val("u_util", pt_data.get("utility", 0))
        consultancy_rate = get_val("sc_cons", pt_data.get("cons", 0))
        
        smart_custom_costs = sum(float(item.get("Rate (Rp)", 0)) * float(item.get("Quantity", 1)) for item in get_val("smart_custom_costs", []))

        construction_subtotal = sum([
            (calc_gba * struc_earth), (calc_gba * struc_found), (calc_gba * struc_work), 
            (calc_gfa * arch_base), (facade * (fac_precast_pct / 100) * fac_precast_rate), 
            (rooms * ffe_rate), (calc_gba * mep_rate), (calc_gba * utility_rate), smart_custom_costs
        ])

        t_prelim = construction_subtotal * 0.05
        t_cont = (construction_subtotal + t_prelim) * 0.03
        grand_total_hc = construction_subtotal + t_prelim + t_cont
        total_soft_cost = (calc_gfa * consultancy_rate) + (grand_total_hc * 0.12) 
        
        calc_budget = grand_total_hc + total_soft_cost

        # 3. OVERWRITE THE SAVED DATA
        st.session_state.projects[pid]["data"]["m_gba"] = calc_gba
        st.session_state.projects[pid]["data"]["m_gfa"] = calc_gfa
        st.session_state.projects[pid]["data"]["m_sgfa"] = calc_sgfa
        st.session_state.projects[pid]["data"]["grand_total_project"] = calc_budget
        st.session_state.projects[pid]["data"]["m_rooms"] = rooms
        
    save_data() # Save to cloud/local

def calculate_project_totals(pdata, curr_type):
    """Calculates all totals dynamically for a given project."""
    d = pdata.get("data", {})
    # Default to empty dict if project type isn't in database yet
    pt_data = PROJECT_DATABASE.get(curr_type, {})

    def get_val(key, default=0.0):
        val = d.get(key, default)
        if isinstance(val, list): return val
        try: return float(val)
        except: return val

    # --- Area Calculations ---
    area_table = get_val("area_table_data", [])
    if isinstance(area_table, list) and len(area_table) > 0:
        calc_gba = 0.0
        calc_gfa = 0.0
        calc_sgfa = 0.0
        breakdown_cols = ["Parkir", "Roof/Deck", "MEP Outdoor", "Koridor/Lobby", "Stair, MEP, Etc", "Unit", "Office"]
        
        for row in area_table:
            row_total = sum(float(row.get(c, 0)) for c in breakdown_cols)
            calc_gba += row_total
            calc_gfa += row_total - sum(float(row.get(c, 0)) for c in ["Parkir", "Roof/Deck", "MEP Outdoor"])
            calc_sgfa += sum(float(row.get(c, 0)) for c in ["Unit", "Office", "Koridor/Lobby"])
    else:
        calc_gba = get_val("m_gba", 0.0)
        calc_gfa = get_val("m_gfa", 0.0)
        calc_sgfa = get_val("m_sgfa", 0.0)

    # --- Cost Calculations ---
    struc_earth = get_val("u_earth", pt_data.get("struc_earth", 0))
    struc_found = get_val("u_found", pt_data.get("struc_found", 0))
    struc_work = get_val("u_struc", pt_data.get("struc_work", 0))
    arch_base = get_val("u_arch", pt_data.get("arch_base", 0))
    
    facade = get_val("m_facade", 0.0)
    fac_precast_pct = get_val("r_fac_pre", pt_data.get("facade_precast_pct", 0))
    fac_precast_rate = get_val("u_f_pre", pt_data.get("facade_precast_rate", 0))
    
    rooms = get_val("m_rooms", 0.0)
    ffe_rate = get_val("u_ffe", pt_data.get("ffe", 0))
    mep_rate = get_val("u_mep", pt_data.get("mep", 0))
    utility_rate = get_val("u_util", pt_data.get("utility", 0))
    
    consultancy_rate = get_val("sc_cons", pt_data.get("cons", 0))
    insurance_pct = get_val("sc_ins", 0.12)
    
    smart_custom_costs = sum(float(item.get("Rate (Rp)", 0)) * float(item.get("Quantity", 1)) for item in get_val("smart_custom_costs", []))

    t_earth = calc_gba * struc_earth
    t_found = calc_gba * struc_found
    t_struc = calc_gba * struc_work
    t_arch_base = calc_gfa * arch_base
    t_precast = facade * (fac_precast_pct / 100) * fac_precast_rate
    t_ffe = rooms * ffe_rate
    t_mep = calc_gba * mep_rate
    t_utility = calc_gba * utility_rate
    
    construction_subtotal = sum([t_earth, t_found, t_struc, t_arch_base, t_precast, t_ffe, t_mep, t_utility, smart_custom_costs])

    t_preliminary = construction_subtotal * 0.05
    t_contingency = (construction_subtotal + t_preliminary) * 0.03
    grand_total_hc = construction_subtotal + t_preliminary + t_contingency

    total_soft_cost = (calc_gfa * consultancy_rate) + (grand_total_hc * (insurance_pct / 100.0)) 
    
    calc_budget = grand_total_hc + total_soft_cost

    return calc_gba, calc_gfa, calc_sgfa, calc_budget, rooms

def save_snapshot(snapshot_name):
    token = st.session_state.get("access_token")
    user_id = st.session_state.get("user").id

    if not token or not user_id:
        st.error("Not authenticated.")
        return False

    authed_client = create_client(url, key)
    authed_client.postgrest.auth(token)

    payload = {
        "app_version": APP_VERSION,
        "projects": st.session_state.projects,
        "current_proj_id": st.session_state.current_proj_id,
        "proj_counter": st.session_state.proj_counter
    }

    try:
        authed_client.table("project_snapshots").insert({
            "user_id": user_id,
            "snapshot_name": snapshot_name,
            "data": payload
        }).execute()
        return True
    except Exception as e:
        st.error(f"Project Save Error: {e}")
        return False

def load_snapshots():
    token = st.session_state.get("access_token")
    user = st.session_state.get("user")

    if not token or not user:
        return []

    try:
        authed_client = create_client(url, key)
        authed_client.postgrest.auth(token)

        response = authed_client.table("project_snapshots") \
            .select("id, snapshot_name, created_at") \
            .eq("user_id", user.id) \
            .order("created_at", desc=True) \
            .execute()

        return response.data if response.data else []
    except Exception as e:
        st.error(f"Project Load Error: {e}")
        return []

def load_snapshot_data(snapshot_id):
    token = st.session_state.get("access_token")

    if not token:
        return None

    try:
        authed_client = create_client(url, key)
        authed_client.postgrest.auth(token)

        response = authed_client.table("project_snapshots") \
            .select("data") \
            .eq("id", snapshot_id) \
            .execute()

        if response.data:
            return response.data[0]["data"]
    except Exception as e:
        st.error(f"Saved Project Fetch Error: {e}")
    return None

def delete_snapshot(snapshot_id):
    token = st.session_state.get("access_token")

    if not token:
        return False

    try:
        authed_client = create_client(url, key)
        authed_client.postgrest.auth(token)

        authed_client.table("project_snapshots") \
            .delete() \
            .eq("id", snapshot_id) \
            .execute()
        return True
    except Exception as e:
        st.error(f"Project Delete Error: {e}")
        return False

def show_snapshots():
    st.title("Project Archive")

    # --- SAVE NEW SNAPSHOT ---
    st.subheader("Save Project")
    snapshot_name = st.text_input(
        "Project Name", 
        placeholder="e.g. ASG Tower - Option 2 - Rev3"
    )
    col1, _ = st.columns([1, 6])
    if col1.button("Save Project", use_container_width=True):
        if snapshot_name.strip() == "":
            col1.warning("Please enter Project name.")
        else:
            if save_snapshot(snapshot_name):
                st.success(f"Project **{snapshot_name}** saved!")
                st.rerun()

    st.divider()

    # --- LIST EXISTING SNAPSHOTS ---
    st.subheader("Load Project:")
    snapshots = load_snapshots()

    if not snapshots:
        st.info("No saved projects yet.")
    else:
        for snap in snapshots:
            col1, col2, col3 = st.columns([5, 1, 1])
            
            from datetime import datetime, timedelta

            created_utc = datetime.fromisoformat(snap["created_at"].replace("Z", "+00:00"))
            created_local = created_utc + timedelta(hours=7)
            formatted_date = created_local.strftime("%d %b %Y, %H:%M")
            
            col1.markdown(f"**{snap['snapshot_name']}**  \n  *Saved: {formatted_date} WIB*")
            
            if col2.button("Load Project", key=f"load_{snap['id']}", type="primary", use_container_width=True):
                data = load_snapshot_data(snap["id"])
                if data:
                    st.session_state.projects = data["projects"]
                    st.session_state.current_proj_id = data["current_proj_id"]
                    st.session_state.proj_counter = data["proj_counter"]
                    save_data()  # also update the main auto-save slot
                    st.success(f"Loaded **{snap['snapshot_name']}**!")
                    st.rerun()

            if col3.button("Delete Project", key=f"del_{snap['id']}", use_container_width=True):
                if delete_snapshot(snap["id"]):
                    st.success("Snapshot deleted.")
                    st.rerun()

def save_data():
    if not st.session_state.get("storage_loaded", False):
        return
    if not st.session_state.get("logged_in", False):
        return

    token = st.session_state.get("access_token")
    user_id = st.session_state.get("user").id  # get the logged-in user's ID

    if not token or not user_id:
        st.error("Not authenticated.")
        return

    authed_client = create_client(url, key)
    authed_client.postgrest.auth(token)

    payload = {
        "app_version": APP_VERSION,
        "projects": st.session_state.projects,
        "current_proj_id": st.session_state.current_proj_id,
        "proj_counter": st.session_state.proj_counter
    }

    try:
        authed_client.table("project_storage").upsert({
            "id": f"storage_{user_id}",  # unique row per user
            "user_id": user_id,
            "data": payload
        }).execute()
    except Exception as e:
        st.error(f"Cloud Save Error: {e}")

def load_data():
    token = st.session_state.get("access_token")
    user = st.session_state.get("user")

    if not token or not user:
        return None

    try:
        authed_client = create_client(url, key)
        authed_client.postgrest.auth(token)

        response = authed_client.table("project_storage") \
            .select("data") \
            .eq("id", f"storage_{user.id}") \
            .execute()

        if response.data:
            return response.data[0]["data"]
    except Exception as e:
        st.error(f"Cloud Load Error: {e}")
    return None

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
#endregion

PROJECT_DATABASE = { #Change only when asked
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

#region --- DO NOT CHANGE#2 (OR I WILL KICK YOUR FACE)---
def cb_add_project():
    st.session_state.proj_counter += 1
    new_id = f"proj_{st.session_state.proj_counter}"
    st.session_state.projects[new_id] = {"name": f"New Project {st.session_state.proj_counter}", "type": "Hotel", "data": {}}
    st.session_state.current_proj_id = new_id

def cb_delete_project():
    del st.session_state.projects[st.session_state.current_proj_id]
    st.session_state.current_proj_id = list(st.session_state.projects.keys())[0]

def cb_switch_project():
    # Use .get() to avoid the AttributeError if the key is missing
    selected_label = st.session_state.get("project_selector")
    
    if not selected_label:
        return

    proj_ids = list(st.session_state.projects.keys())
    proj_labels = [f"{st.session_state.projects[pid]['name']} ({st.session_state.projects[pid]['type']})" for pid in proj_ids]
    
    if selected_label in proj_labels:
        selected_idx = proj_labels.index(selected_label)
        st.session_state.current_proj_id = proj_ids[selected_idx]
        save_data()     

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

def show_project_database(): #database page
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

def show_area_calculator(): #area calculator page
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
        with st.expander("Building Floor Config", expanded=False):
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
      
def update_price(metric_key, db_key): #this function pulls~
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

def show_cost_estimator(): #cost calculator page
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
    tab1, tab2, tab3, tab5, tab4, tab6, tab7, tab8, tab9 = st.tabs([
        "Welcome",
        "1. Ukuran", "2. Rasio",
        "3. Soft Costs", "4. Harga",
        "5. Item Tambahan", "6. Hasil",
        "7. Pembuktian",
        "Unggah & Unduh",
    ])

# --- TAB 1: WELCOME ---
    with tab1:
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&display=swap');
            
            /* General Hero Styling */
            .hero-card {
                background: #ffffff; border: 0.5px solid #e0e0e0; border-radius: 12px;
                padding: 1.75rem 1.5rem 1.5rem; margin-bottom: 2rem;
            }
            .hero-badge {
                display: inline-flex; align-items: center; gap: 6px;
                font-size: 11px; font-weight: 600; letter-spacing: 0.07em;
                text-transform: uppercase; background: #f5f5f5;
                color: #666; border: 0.5px solid #ddd; border-radius: 8px;
                padding: 4px 10px; margin-bottom: 1rem;
            }
            .hero-title { font-size: 22px; font-weight: 600; color: #1a1a1a; margin: 0 0 8px; }
            .hero-sub   { font-size: 14px; color: #555; margin: 0; line-height: 1.6; }
            .hero-divider { height: 1px; background: #eee; margin: 1.25rem 0; }
            .hero-meta  { display: flex; gap: 1.5rem; flex-wrap: wrap; }
            .hero-meta-item { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #666; }
            
            /* Section Titles */
            .section-label {
                font-size: 12px; font-weight: 600; letter-spacing: 0.08em;
                text-transform: uppercase; color: #3e4095; margin: 0 0 1rem;
                border-bottom: 1px solid #eee; padding-bottom: 6px;
            }
            
            /* Grid & Cards */
            .step-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 2rem; }
            .step-card {
                background: #fff; border: 0.5px solid #e0e0e0; border-radius: 12px;
                padding: 1.25rem; transition: border-color 0.15s, box-shadow 0.15s;
            }
            .step-card:hover { border-color: #3e4095; box-shadow: 0 4px 12px rgba(62, 64, 149, 0.05); }
            .step-top  { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
            
            /* Icons for Navigation Menu */
            .nav-icon {
                width: 28px; height: 28px; border-radius: 6px;
                background: #f0f0f5; color: #3e4095; font-size: 14px;
                display: flex; align-items: center; justify-content: center; flex-shrink: 0;
            }
            
            /* Numbers for Steps */
            .step-num  {
                width: 24px; height: 24px; border-radius: 6px;
                background: #3e4095; color: #fff; font-size: 11px; font-weight: 600;
                display: flex; align-items: center; justify-content: center; flex-shrink: 0;
            }
            
            /* Text inside cards */
            .step-title { font-size: 14px; font-weight: 600; color: #1a1a1a; }
            .step-desc  { font-size: 13px; color: #666; line-height: 1.5; margin: 0; }
            .step-caption {
                font-size: 11px !important;
                color: #9CA3AF !important;
                margin-top: 4px !important;
                font-style: italic;
            }
            
            /* Tooltip/Info Box */
            .tip-box {
                background: #f8f8ff; border: 0.5px solid #e0e0ff;
                border-left: 3px solid #3e4095; border-radius: 0 8px 8px 0;
                padding: 1rem; display: flex; align-items: flex-start; gap: 12px;
            }
            .tip-icon { font-size: 18px; color: #3e4095; margin-top: -2px; flex-shrink: 0; }
            .tip-text  { font-size: 13px; color: #444; margin: 0; line-height: 1.5; }
        </style>

        <!-- HERO SECTION -->
        <div class="hero-card">
            <div class="hero-badge">&#128200; Workspace Dashboard</div>
            <p class="hero-title">Project Feasibility Study</p>
            <p class="hero-sub">Analisis kelayakan proyek secara komprehensif dengan estimasi biaya yang akurat.</p>
            <div class="hero-divider"></div>
            <div class="hero-meta">
                <div class="hero-meta-item">&#128202; Perhitungan area & biaya terintegrasi</div>
                <div class="hero-meta-item">&#129516; Breakdown biaya otomatis</div>
                <div class="hero-meta-item">&#128452; Terkoneksi dengan Database master</div>
            </div>
        </div>

        <!-- SECTION 1: MAIN NAVIGATION -->
        <p class="section-label">🧭 Penjelasan Menu Utama (Sidebar)</p>
        <div class="step-grid">
            <div class="step-card">
                <div class="step-top"><div class="nav-icon">🧮</div><span class="step-title">Cost Calculator</span></div>
                <p class="step-desc">Modul utama untuk menghitung rincian dan estimasi kelayakan biaya proyek.</p>
            </div>
            <div class="step-card">
                <div class="step-top"><div class="nav-icon">📐</div><span class="step-title">Area Calculator</span></div>
                <p class="step-desc">Kalkulator khusus untuk merencanakan parameter dimensi dan luas area.</p>
            </div>
            <div class="step-card">
                <div class="step-top"><div class="nav-icon">🗄️</div><span class="step-title">Database</span></div>
                <p class="step-desc">Pusat data acuan harga satuan, material, dan referensi standar proyek.</p>
            </div>
            <div class="step-card">
                <div class="step-top"><div class="nav-icon">📊</div><span class="step-title">Summary</span></div>
                <p class="step-desc">Ringkasan eksekutif dan dashboard pelaporan dari hasil perhitungan akhir.</p>
            </div>
            <div class="step-card">
                <div class="step-top"><div class="nav-icon">📂</div><span class="step-title">Project Archive</span></div>
                <p class="step-desc">Manajemen berkas: simpan, muat (load), dan kelola histori versi proyek Anda.</p>
            </div>
        </div>

        <!-- SECTION 2: COST CALCULATOR WORKFLOW -->
        <p class="section-label">⚙️ Alur Kerja: Cost Calculator</p>
        <div class="step-grid">
            <div class="step-card">
                <div class="step-top"><div class="step-num">1</div><span class="step-title">Ukuran</span></div>
                <p class="step-desc">Isi luas tanah, GBA, GFA, SGFA, dan jumlah unit.</p>
                <p class="step-caption">Input berupa qty, bukan harga.</p>
            </div>
            <div class="step-card">
                <div class="step-top"><div class="step-num">2</div><span class="step-title">Rasio</span></div>
                <p class="step-desc">Untuk input rasio material lantai & fasad.</p>
                <p class="step-caption">Input berupa persentase (%).</p>
            </div>
            <div class="step-card">
                <div class="step-top"><div class="step-num">3</div><span class="step-title">Soft Cost</span></div>
                <p class="step-desc">Biaya jasa QS, PM, konsultan, dan asuransi proyek.</p>
            </div>
            <div class="step-card">
                <div class="step-top"><div class="step-num">4</div><span class="step-title">Harga</span></div>
                <p class="step-desc">Harga otomatis mengikuti database jenis proyek.</p>
                <p class="step-caption">Dapat disesuaikan manual (override).</p>
            </div>
            <div class="step-card">
                <div class="step-top"><div class="step-num">5</div><span class="step-title">Tambahan</span></div>
                <p class="step-desc">Penambahan item khusus atau spesifik proyek.</p>
                <p class="step-caption">Input manual untuk Nama, Qty, dan Harga.</p>
            </div>
            <div class="step-card">
                <div class="step-top"><div class="step-num">6</div><span class="step-title">Hasil</span></div>
                <p class="step-desc">Dashboard hasil perhitungan total biaya proyek keseluruhan.</p>
            </div>
            <div class="step-card">
                <div class="step-top"><div class="step-num">7</div><span class="step-title">Pembuktian</span></div>
                <p class="step-desc">Tampilkan perhitungan rinci per item untuk verifikasi dan audit QS.</p>
            </div>
        </div>

        <!-- TIP BOX -->
        <div class="tip-box">
            <span class="tip-icon">&#8505;</span>
            <p class="tip-text"><strong>Rekomendasi Alur:</strong> Jika Anda memulai proyek baru, masuk ke <strong>Area Calculator</strong> terlebih dahulu. Setelah luasan didapat, pindah ke <strong>Cost Calculator</strong> (Mulai dari tab Ukuran hingga Hasil). Jangan lupa simpan pekerjaan Anda di <strong>Project Archive</strong> sebelum keluar.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
                            import ast  # Needed to turn strings back into tables
                            df_import = pd.read_csv(uploaded_file)
                            
                            if df_import is not None and not df_import.empty:
                                global_temp_custom = {}
                                import_pid_map = {} # Track mapped IDs to prevent row-by-row renaming

                                for index, row in df_import.iterrows():
                                    # Get raw ID
                                    raw_pid = str(row.get("Project_ID", curr_id)).strip()
                                    key = str(row.get("Metric_Key", "")).strip()
                                    val = row.get("Value", "")

                                    if not key or pd.isna(val): continue 

                                    # 1. Handle Project ID Mapping (Renaming if duplicate exists)
                                    if raw_pid not in import_pid_map:
                                        target_pid = raw_pid
                                        if target_pid in st.session_state.projects:
                                            # Unique suffix for this file import
                                            target_pid = f"{target_pid}_imported_{file_key[:4]}"
                                        import_pid_map[raw_pid] = target_pid

                                    pid = import_pid_map[raw_pid]

                                    if pid not in st.session_state.projects:
                                        st.session_state.projects[pid] = {
                                            "name": f"Imported Project {pid}",
                                            "type": "Hotel", 
                                            "data": {}
                                        }
                                    
                                    # 2. Handle Metadata
                                    if key == "proj_name":
                                        st.session_state.projects[pid]["name"] = str(val)
                                    elif key == "proj_type":
                                        st.session_state.projects[pid]["type"] = str(val)
                                    
                                    # 3. Handle Custom Item Reconstruction
                                    elif key.startswith(("input_name", "input_rate", "input_qty")):
                                        if pid not in global_temp_custom:
                                            global_temp_custom[pid] = {}
                                        try:
                                            idx = int(''.join(filter(str.isdigit, key)))
                                            if idx not in global_temp_custom[pid]:
                                                global_temp_custom[pid][idx] = {"Item Description": "", "Rate (Rp)": 0.0, "Quantity": 1.0}
                                            
                                            if "name" in key: global_temp_custom[pid][idx]["Item Description"] = str(val)
                                            elif "rate" in key: global_temp_custom[pid][idx]["Rate (Rp)"] = float(val)
                                            elif "qty" in key: global_temp_custom[pid][idx]["Quantity"] = float(val)
                                        except: continue

                                    # 4. Handle Standard Metrics & Nested Tables (Area Calculator)
                                    else:
                                        try:
                                            str_val = str(val).strip()

                                            # Strip surrounding quotes that CSV may add
                                            if str_val.startswith('"') and str_val.endswith('"'):
                                                str_val = str_val[1:-1]

                                            if str_val.startswith("[{") or str_val.startswith("['"): 
                                                # Try JSON first (clean), then fall back to Python literal
                                                try:
                                                    st.session_state.projects[pid]["data"][key] = _json.loads(str_val)
                                                except Exception:
                                                    try:
                                                        st.session_state.projects[pid]["data"][key] = ast.literal_eval(str_val)
                                                    except Exception:
                                                        st.session_state.projects[pid]["data"][key] = str_val
                                            else:
                                                try:
                                                    st.session_state.projects[pid]["data"][key] = float(val)
                                                except (ValueError, TypeError):
                                                    st.session_state.projects[pid]["data"][key] = str(val)
                                        except (ValueError, TypeError, SyntaxError):
                                            st.session_state.projects[pid]["data"][key] = str(val)

                                # 5. Finalize Custom Item Lists
                                for pid_key, items_dict in global_temp_custom.items():
                                    sorted_custom = [items_dict[i] for i in sorted(items_dict.keys())]
                                    st.session_state.projects[pid_key]["data"]["smart_custom_costs"] = sorted_custom

                                # 6. CLEAR UI CACHE ANCHORS (Crucial for Area Calculator reload)
                                keys_to_clear = [k for k in st.session_state.keys() if "base_table_" in k or "area_editor_" in k]
                                for k in keys_to_clear:
                                    del st.session_state[k]

                                st.session_state.last_loaded_file = file_key
                                st.success(f"✅ Import Successful! New projects created to avoid overwrites.")
                                st.rerun()
                            else:
                                st.warning("⚠️ The uploaded CSV is empty.")
                        except Exception as e:
                            st.error(f"❌ Error during import: {e}")
                            
            with c2:
                st.subheader("Export")
                # --- 1. CURRENT PROJECT ONLY ---
                current_project_csv = []
                current_project_csv.append({"Project_ID": curr_id, "Metric_Key": "proj_name", "Value": curr_proj["name"]})
                current_project_csv.append({"Project_ID": curr_id, "Metric_Key": "proj_type", "Value": curr_proj["type"]})
                
                for k, v in st.session_state.projects[curr_id]["data"].items():
                    if k not in ("header_info", "assumptions"):
                        serialized_v = _json.dumps(v) if isinstance(v, list) else v
                        current_project_csv.append({"Project_ID": curr_id, "Metric_Key": k, "Value": serialized_v})

                df_curr = pd.DataFrame(current_project_csv)
                csv_buffer = df_curr.to_csv(index=False).encode("utf-8")

                # --- 2. GLOBAL DATABASE ---
                all_projects_csv = []
                for pid, pdata in st.session_state.projects.items():
                    all_projects_csv.append({"Project_ID": pid, "Metric_Key": "proj_name", "Value": pdata["name"]})
                    all_projects_csv.append({"Project_ID": pid, "Metric_Key": "proj_type", "Value": pdata["type"]})
                    for k, v in pdata["data"].items():
                        if k not in ("header_info", "assumptions"):
                            all_projects_csv.append({"Project_ID": pid, "Metric_Key": k, "Value": v})

                df_all = pd.DataFrame(all_projects_csv)
                csv_all_buffer = df_all.to_csv(index=False).encode("utf-8")

                # --- 3. DOWNLOAD BUTTONS ---
                st.download_button(
                    label=f"Download {curr_proj['name']} only",
                    data=csv_buffer,
                    file_name=f"Project_{curr_id}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                st.download_button(
                    label="Download All Projects",
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
            fl_skirt = st.number_input(
                "Skirting (%)", 
                value=get_val("s_floor", pt_data.get("fl_skirt", 20)), 
                key=f"s_floor{curr_type_key}"
            )
            fl_waste = st.number_input(
                "Floor Waste (%)", 
                value=get_val("w_floor", pt_data.get("fl_waste", 10)), # Use .get() with 1.1 as default
                key=f"w_floor{curr_type_key}"
            )        

            st.caption(f"Luas Lantai + Skirting + Waste: GFA: {gfa:.2f} x {1 + (fl_skirt/100):.2f} x {1 + (fl_waste/100):.2f} = {gfa*(1 + (fl_waste/100))*(1 + (fl_skirt/100)):.2f} m2")

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
            # ADD THIS LINE BELOW
            column_order=["Item Description", "Quantity", "Rate (Rp)"], 
            column_config={
                "Item Description": st.column_config.TextColumn("Item Description", width="large"),
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

# ... (keep your loop the same) ...
        
        # 1. Update the 'smart_custom_data' for export logic (what you already have)
        st.session_state[f"smart_custom_data_{curr_id}"] = smart_custom_inputs
        
        # 2. ADD THIS: Update the raw list so the table editor actually remembers the rows!
        st.session_state.projects[curr_id]["data"]["smart_custom_costs"] = edited_smart_cc.to_dict('records')
        
        # 3. Now save to JSON
        save_data()
        
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
        tab1, tab2, tab3 = st.tabs([
        "Hasil",
        "Tabel", "Chart"
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
    st.session_state.projects[curr_id]["data"]["grand_total_project"] = grand_total_project
    save_data()

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

#region --- DO NOT CHANGE#3 (OR GOD HELP ME) ---
def generate_exact_portfolio_excel(port_meta, port_data, port_assumptions):
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Portfolio Summary"

    # --- 1. Styling Definitions ---
    blue_fill = PatternFill(start_color="005A9C", end_color="005A9C", fill_type="solid")
    gray_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    yellow_fill = PatternFill(start_color="FFD966", end_color="FFD966", fill_type="solid")
    
    white_font = Font(color="FFFFFF", bold=True, name='Calibri', size=11)
    bold_font = Font(bold=True, name='Calibri', size=10)
    reg_font = Font(bold=False, name='Calibri', size=10)
    small_font = Font(name='Calibri', size=9)
    
    black_border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                          top=Side(style='thin'), bottom=Side(style='thin'))
    
    center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
    left_align = Alignment(horizontal='left', vertical='center', wrap_text=True)
    right_align = Alignment(horizontal='right', vertical='center')

    # --- 2. Blue Header Section ---
    headers = [
        ["ASG GROUP PROPERTY DEVELOPMENT", f"VERSION : {port_meta.get('version', '')}"],
        ["QS & PROCUREMENT DIVISION", f"UPDATED : {port_meta.get('updated', '')}"],
        [port_meta.get('title', ''), f"CREATED : {port_meta.get('created', '')}"],
        [port_meta.get('ref', ''), ""]
    ]

    for r_idx, (text_left, text_right) in enumerate(headers, 1):
        for c_idx in range(1, 12):
            c = ws.cell(row=r_idx, column=c_idx)
            c.fill = blue_fill
            c.font = white_font
            if c_idx == 1: c.value = text_left
            if c_idx == 11: 
                c.value = text_right
                c.alignment = Alignment(horizontal='right')
        ws.merge_cells(start_row=r_idx, start_column=1, end_row=r_idx, end_column=10)

    # --- 3. Table Header (Rows 6 & 7) ---
    ws.merge_cells(start_row=6, start_column=1, end_row=7, end_column=1) # SN
    ws.merge_cells(start_row=6, start_column=2, end_row=7, end_column=2) # AREA
    ws.merge_cells(start_row=6, start_column=3, end_row=6, end_column=5) # BLDG AREA
    ws.merge_cells(start_row=6, start_column=6, end_row=6, end_column=7) # UNIT
    ws.merge_cells(start_row=6, start_column=8, end_row=7, end_column=8) # BUDGET
    ws.merge_cells(start_row=6, start_column=9, end_row=6, end_column=11) # COST RATIO

    header_labels = {
        (6, 1): "SN", (6, 2): "AREA", (6, 3): "BUILDING AREA (M2)", 
        (6, 6): "UNIT", (6, 8): "BUDGET ESTIMATE\nRP", (6, 9): "COST RATIO RP/M2",
        (7, 3): "GBA", (7, 4): "GFA", (7, 5): "SGFA", (7, 9): "GBA", (7, 10): "GFA", (7, 11): "SGFA"
    }

    for (r, c), text in header_labels.items():
        cell = ws.cell(row=r, column=c, value=text)
        cell.alignment = center_align
        cell.font = bold_font
        cell.fill = gray_fill

    for r in range(6, 8):
        for c in range(1, 12):
            ws.cell(row=r, column=c).border = black_border

    # --- 4. Data Rows ---
    current_row = 8
    for p_row in port_data:
        is_total = p_row.get("AREA") == "TOTAL"
        is_parking = "PARKING" in str(p_row.get("AREA", "")).upper()
        
        # Set SN and Area
        ws.cell(row=current_row, column=1, value=p_row.get("SN", "")).alignment = center_align
        
        area_cell = ws.cell(row=current_row, column=2, value=p_row.get("AREA", ""))
        area_cell.alignment = Alignment(horizontal='left', vertical='top' if is_parking else 'center', wrap_text=True)
        
        # Set Values
        cols = ["GBA", "GFA", "SGFA", "QTY", "UNIT", "BUDGET", "R_GBA", "R_GFA", "R_SGFA"]
        for i, key in enumerate(cols, 3):
            val = p_row.get(key, "")
            cell = ws.cell(row=current_row, column=i, value=val)
            cell.alignment = Alignment(vertical='top' if is_parking else 'center', horizontal='right' if i != 7 else 'center')
            
            if key in ["GBA", "GFA", "SGFA"]: cell.number_format = "#,##0.00"
            if key in ["BUDGET", "R_GBA", "R_GFA", "R_SGFA"]: cell.number_format = "#,##0"

        # Apply Row Styles
        for c in range(1, 12):
            ws.cell(row=current_row, column=c).border = black_border
            ws.cell(row=current_row, column=c).font = bold_font if (p_row.get("SN") or is_total) else reg_font
            if is_total: ws.cell(row=current_row, column=c).fill = gray_fill

        if is_total:
            ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=2)
            ws.cell(row=current_row, column=6, value="TOTAL").alignment = center_align

        # Adjust height for multi-line rows (Parking)
        if is_parking:
            ws.row_dimensions[current_row].height = 100 

        current_row += 1

    # --- 5. Assumptions Section ---
    current_row += 1
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=11)
    cell_assump = ws.cell(row=current_row, column=1, value="I.  ASSUMPTIONS")
    cell_assump.font = bold_font
    for c in range(1, 12):
        ws.cell(row=current_row, column=c).fill = yellow_fill
        ws.cell(row=current_row, column=c).border = black_border

    current_row += 1
    for _, a_row in port_assumptions.iterrows():
        ws.cell(row=current_row, column=1, value=a_row.get("No.", "")).alignment = center_align
        
        desc_cell = ws.cell(row=current_row, column=2, value=a_row.get("Assumption Description", ""))
        desc_cell.alignment = Alignment(wrap_text=True)
        ws.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=11)
        
        for c in range(1, 12):
            ws.cell(row=current_row, column=c).border = black_border
        current_row += 1

    # Column Widths
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 35
    for c in ['C', 'D', 'E', 'H', 'I', 'J', 'K']:
        ws.column_dimensions[c].width = 16

    wb.save(output)
    return output.getvalue()

def generate_recap_excel(port_meta, projects):
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Recap Cost"

    # --- EXACT MATH ENGINE ---
    def get_recap_values(pdata):
        d = pdata.get("data", {})
        curr_type = pdata.get("type", "Hotel")
        pt_data = PROJECT_DATABASE.get(curr_type, {})
        
        def get_val(key, default_db_key, default_val=0.0):
            val = d.get(key)
            if val is not None and val != "":
                try: return float(val)
                except: pass
            if default_db_key and default_db_key in pt_data:
                try: return float(pt_data[default_db_key])
                except: pass
            return float(default_val)
            
        gba = get_val("m_gba", None, 0); gfa = get_val("m_gfa", None, 0)
        struc_earth = get_val("u_earth", "struc_earth", 0)
        struc_found = get_val("u_found", "struc_found", 0)
        struc_work = get_val("u_struc", "struc_work", 0)
        arch_base = get_val("u_arch", "arch_base", 0)
        facade = get_val("m_facade", None, 0)
        facade_precast_pct = get_val("r_fac_pre", "facade_precast_pct", 0)
        facade_precast_rate = get_val("u_f_pre", "facade_precast_rate", 0)
        facade_window_pct = get_val("r_fac_win", "facade_window_pct", 0)
        facade_window_rate = get_val("u_f_win", "facade_window_rate", 0)
        facade_double_pct = get_val("r_fac_doub", "facade_double_pct", 0)
        facade_double_rate = get_val("u_f_doub", "facade_double_rate", 0)
        wooden_door = get_val("m_door_w", None, 0); door_wood = get_val("u_d_wood", "door_wood", 0)
        glass_door = get_val("m_door_g", None, 0); door_glass = get_val("u_d_glass", "door_glass", 0)
        steel_door = get_val("m_door_s", None, 0); door_steel = get_val("u_d_steel", "door_steel", 0)
        lobby_interior = get_val("m_lobby", None, 0); lobby_rate = get_val("u_lobby", "lobby", 0)
        gondola_unit = get_val("m_gondola", None, 0); gondola_rate = get_val("u_gondola", "gondola", 0)
        rooms = get_val("m_rooms", None, 0)
        san_qty_room = get_val("r_san_qty", "san_room_qty", 0); san_room_rate = get_val("u_s_room", "san_room_rate", 0)
        toilet_male = get_val("m_toil_m", None, 0); san_pub_m = get_val("u_s_pub_m", "san_pub_m", 0)
        toilet_female = get_val("m_toil_f", None, 0); san_pub_f = get_val("u_s_pub_f", "san_pub_f", 0)
        disabled_toil = get_val("m_toil_d", None, 0); san_dis = get_val("u_s_dis", "san_dis", 0)
        mushola_unit = get_val("m_mushola", None, 0); san_mushola = get_val("u_s_mushola", "san_mushola", 0)
        kitchen_rate = get_val("u_kit", "kitchen", 0)
        hw_wood = get_val("u_hw_wood", "hw_wood", 0); hw_steel = get_val("u_hw_steel", "hw_steel", 0)
        fl_waste = get_val("w_floor", "fl_waste", 10); fl_skirt = get_val("s_floor", "fl_skirt", 20)
        fl_ht_pct = get_val("r_fl_ht", "fl_ht_pct", 0); fl_ht_rate = get_val("u_fl_ht", None, 0) 
        fl_vinyl_pct = get_val("r_fl_vin", "fl_vinyl_pct", 0); fl_vinyl_rate = get_val("u_fl_vin", None, 0)
        fl_marmer_pct = get_val("r_fl_mar", "fl_marmer_pct", 0); fl_marmer_rate = get_val("u_fl_mar", None, 0)
        carpet_m2 = get_val("m_carpet", None, 0); carpet_rate = get_val("u_carpet", "carpet", 0)
        glass_m2 = get_val("m_glass", None, 0); glass_rate = get_val("u_glass", "glass", 0)
        ffe_rate = get_val("u_ffe", "ffe", 0); misc_rate = get_val("u_misc", "misc", 0); misc_switch = get_val("misc_switch", None, 0)
        mep_rate = get_val("u_mep", "mep", 0); utility_rate = get_val("u_util", "utility", 0)
        railing_qty = get_val("r_rail_qty", "railing_qty", 0); railing_rate = get_val("u_rail", "railing_rate", 0)
        skylight_area = get_val("m_skylight", None, 0); skylight_rate = get_val("u_sky", "skylight_rate", 0)
        land_m2 = get_val("m_land_m2", None, 0); ext_land_rate = get_val("u_ext", "ext_land", 0)
        pub_fac_m2 = get_val("m_fac_pub", None, 0); fac_pub_rate = get_val("u_fac_p", "fac_pub", 0)
        res_fac_m2 = get_val("m_fac_res", None, 0); fac_res_rate = get_val("u_fac_r", "fac_res", 0)
        proj_fac_u = get_val("m_fac_proj", None, 0); fac_proj_rate = get_val("u_fac_pr", "fac_proj", 0)
        consultancy_rate = get_val("sc_cons", "cons", 0); qs_months = get_val("sc_qs_m", None, 0); qs_rate = get_val("sc_qs_r", None, 0)
        pm_months = get_val("sc_pm_m", None, 0); pm_rate = get_val("sc_pm_r", None, 0); insurance_pct = get_val("sc_ins", None, 0.12)
        smart_custom_costs = sum(float(i.get("Rate (Rp)", 0)) * float(i.get("Quantity", 1)) for i in d.get("smart_custom_costs", []) if isinstance(i, dict))

        t_earth = gba * struc_earth; t_found = gba * struc_found; t_struc = gba * struc_work; t_arch_base = gfa * arch_base
        t_precast = facade * (facade_precast_pct / 100) * facade_precast_rate; t_window = facade * (facade_window_pct / 100) * facade_window_rate
        t_double = facade * (facade_double_pct / 100) * facade_double_rate; t_w_door = wooden_door * door_wood
        t_g_door = glass_door * door_glass; t_s_door = steel_door * door_steel; t_lobby = lobby_interior * lobby_rate
        t_gondola = gondola_unit * gondola_rate; t_unit_san = rooms * san_qty_room * san_room_rate
        t_t_male = toilet_male * san_pub_m; t_t_female = toilet_female * san_pub_f; t_t_dis = disabled_toil * san_dis
        t_mushola = mushola_unit * san_mushola; t_kitchen = rooms * kitchen_rate; t_hw_w = wooden_door * hw_wood
        t_hw_s = steel_door * hw_steel; f_mult = (1 + (fl_waste/100)) * (1 + (fl_skirt/100))
        t_ht = gfa * (fl_ht_pct / 100) * fl_ht_rate * f_mult; t_vinyl = gfa * (fl_vinyl_pct / 100) * fl_vinyl_rate * f_mult
        t_marmer = gfa * (fl_marmer_pct / 100) * fl_marmer_rate * f_mult; t_carpet = carpet_m2 * carpet_rate
        t_glass_work = glass_m2 * glass_rate; t_ffe = rooms * ffe_rate; t_misc = misc_rate * misc_switch
        t_mep = gba * mep_rate; t_utility = gba * utility_rate; t_railing = (rooms * railing_qty) * railing_rate
        t_skylight = skylight_area * skylight_rate; t_external = land_m2 * ext_land_rate
        t_pub_fac = pub_fac_m2 * fac_pub_rate; t_res_fac = res_fac_m2 * fac_res_rate; t_proj_fac = proj_fac_u * fac_proj_rate

        construction_subtotal = sum([
            t_earth, t_found, t_struc, t_arch_base, t_precast, t_window, t_double, t_w_door, t_g_door, t_s_door, 
            t_lobby, t_gondola, t_unit_san, t_t_male, t_t_female, t_t_dis, t_mushola, t_kitchen, t_hw_w, t_hw_s, 
            t_ht, t_vinyl, t_marmer, t_carpet, t_glass_work, t_ffe, t_misc, t_mep, t_utility, t_railing, t_skylight, 
            t_external, t_pub_fac, t_res_fac, t_proj_fac, smart_custom_costs
        ])

        t_preliminary = construction_subtotal * 0.05
        t_contingency = (construction_subtotal + t_preliminary) * 0.03
        grand_total_hc = construction_subtotal + t_preliminary + t_contingency

        t_consultancy = gfa * consultancy_rate
        t_qs = qs_months * qs_rate
        t_pm = pm_months * pm_rate
        t_insurance = grand_total_hc * (insurance_pct / 100.0)

        total_soft_cost = t_consultancy + t_qs + t_pm + t_insurance
        grand_total_project = grand_total_hc + total_soft_cost

        group_arch = (t_arch_base + t_lobby + t_carpet + t_gondola + t_glass_work + t_kitchen + t_railing + t_skylight + 
                      (t_precast + t_window + t_double) + (t_unit_san + t_t_male + t_t_female + t_t_dis + t_mushola) + 
                      (t_ht + t_vinyl + t_marmer) + (t_w_door + t_g_door + t_s_door + t_hw_w + t_hw_s) + smart_custom_costs)
        
        return {
            "EARTHWORKS": t_earth, "FOUNDATIONS": t_found, "STRUCTURAL WORKS": t_struc,
            "ARCHITECTURAL WORKS": group_arch, "FF & E": t_ffe + t_misc, "M.E.P WORKS": t_mep,
            "UTILITY CONNECTION": t_utility, "EXTERNAL WORKS": t_external, "FACILITY": t_pub_fac + t_res_fac + t_proj_fac,
            "PRELIMINARIES WORKS": t_preliminary, "CONTINGENCIES": t_contingency, "HARDCOST": grand_total_hc,
            "CONSULTANCY SERVICES FEE": t_consultancy, "QS SERVICES": t_qs, 
            "PROJECT MANAGEMENT SERVICES": t_pm, "INSURANCE COVERAGE": t_insurance,
            "SOFTCOST": total_soft_cost, "TOTAL, EXCLD PPN": grand_total_project
        }
    
    if "recap_math_engine" not in st.session_state:
        st.session_state.recap_math_engine = get_recap_values

    # --- Generate Global Totals ---
    tot_cache = {}; global_cost = {}; tot_gba = tot_gfa = tot_sgfa = 0
    for pid, pdata in projects.items():
        vals = get_recap_values(pdata)
        tot_cache[pid] = vals
        for k, v in vals.items(): global_cost[k] = global_cost.get(k, 0) + v
        d = pdata.get("data", {})
        tot_gba += float(d.get("m_gba", 0)); tot_gfa += float(d.get("m_gfa", 0)); tot_sgfa += float(d.get("m_sgfa", 0))

    # Calculate global % divisors
    global_hc = global_cost.get("HARDCOST", 0)
    global_sc = global_cost.get("SOFTCOST", 0)
    safe_hc = global_hc if global_hc > 0 else 1
    safe_sc = global_sc if global_sc > 0 else 1

    # --- 1. Styling Definitions ---
    blue_fill = PatternFill(start_color="0070C0", end_color="0070C0", fill_type="solid")
    white_font, bold_font, reg_font = Font(color="FFFFFF", bold=True, size=10), Font(bold=True, size=9), Font(size=9)
    black_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    center_align, left_align = Alignment(horizontal='center', vertical='center', wrap_text=True), Alignment(horizontal='left', vertical='center')

    # --- 2. Blue Metadata Header ---
    headers = [["ASG GROUP PROPERTY DEVELOPMENT", f"VERSION : {port_meta.get('version', '')}"], ["QS & PROCUREMENT DIVISION", f"UPDATED : {port_meta.get('updated', '')}"], [port_meta.get('title', ''), f"CREATED : {port_meta.get('created', '')}"], [port_meta.get('ref', ''), ""]]
    for r_idx, (text_left, text_right) in enumerate(headers, 1):
        for c in range(1, 100): ws.cell(row=r_idx, column=c).fill = blue_fill
        ws.cell(row=r_idx, column=1, value=text_left).font = white_font
        ws.cell(row=r_idx, column=15, value=text_right).font = white_font
        ws.cell(row=r_idx, column=15).alignment = Alignment(horizontal='right', vertical='center')

    # --- 3. Static Table Headers ---
    static_cols = [("SN", 1), ("DESCRIPTION", 2), ("COA", 3), ("%", 4)]
    for name, col_idx in static_cols:
        ws.merge_cells(start_row=6, start_column=col_idx, end_row=9, end_column=col_idx)
        c = ws.cell(row=6, column=col_idx, value=name)
        c.alignment, c.font, c.fill = center_align, bold_font, PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
        for r in range(6, 10): ws.cell(row=r, column=col_idx).border = black_border

    # --- 4. Dynamic Project Headers ---
    bg_colors = ["EAEAEA", "FCE4D6", "F2DCDB", "E1D5E7", "DDEBF7", "E2EFDA", "D9E1F2", "F4B084", "FFF2CC"]
    project_list = [("TOTAL", {"name": "TOTAL"})] + list(projects.items())
    current_col = 5
    
    for i, (pid, pdata) in enumerate(project_list):
        group_fill = PatternFill(start_color=bg_colors[i % len(bg_colors)], end_color=bg_colors[i % len(bg_colors)], fill_type="solid")
        ws.merge_cells(start_row=6, start_column=current_col, end_row=6, end_column=current_col+4)
        c = ws.cell(row=6, column=current_col, value=pdata.get('name', 'PROJECT').upper())
        c.alignment, c.font, c.fill = center_align, bold_font, group_fill
        
        ws.cell(row=7, column=current_col, value="ESTIMATE").alignment = center_align
        ws.merge_cells(start_row=7, start_column=current_col+1, end_row=7, end_column=current_col+4)
        ws.cell(row=7, column=current_col+1, value="Cost Ratio (Rp/m2)").alignment = center_align
        
        for j, lbl in enumerate(["TOTAL", "GBA", "GFA", "SGFA", "NFA"]):
            ws.cell(row=8, column=current_col+j, value=lbl).alignment = center_align
            
        if pid == "TOTAL":
            gba, gfa, sgfa, nfa = tot_gba, tot_gfa, tot_sgfa, tot_gfa * 0.82
        else:
            d = pdata.get("data", {})
            gba, gfa, sgfa = float(d.get("m_gba", 0)), float(d.get("m_gfa", 0)), float(d.get("m_sgfa", 0))
            nfa = gfa * 0.82
        
        gba_f = gba if gba > 0 else 1; gfa_f = gfa if gfa > 0 else 1; sgfa_f = sgfa if sgfa > 0 else 1; nfa_f = nfa if nfa > 0 else 1
            
        for j, val in enumerate(["Rp", gba, gfa, sgfa, nfa]):
            c = ws.cell(row=9, column=current_col+j, value=val)
            c.alignment = center_align
            if j > 0: c.number_format = '#,##0'

        for r in range(6, 10):
            for c_idx in range(current_col, current_col+5):
                ws.cell(row=r, column=c_idx).fill = group_fill
                ws.cell(row=r, column=c_idx).border = black_border
        current_col += 5

    # --- 5. Data Rows Map (With Categories for %) ---
    row_mapping = [
        ("I", "HARDCOST", "118-14-000", True, "HC"), ("1", "PRELIMINARIES WORKS", "118-14-100", False, "HC"), 
        ("2", "EARTHWORKS", "118-14-200", False, "HC"), ("3", "FOUNDATIONS", "118-14-300", False, "HC"), 
        ("4", "STRUCTURAL WORKS", "118-14-500", False, "HC"), ("5", "ARCHITECTURAL WORKS", "118-14-600", False, "HC"),
        ("6", "FF & E", "118-14-700", False, "HC"), ("7", "M.E.P WORKS", "118-14-800", False, "HC"), 
        ("8", "UTILITY CONNECTION", "118-13-900", False, "HC"), ("9", "EXTERNAL WORKS", "118-14-930", False, "HC"), 
        ("10", "FACILITY", "118-14-960", False, "HC"), ("11", "CONTINGENCIES", "", False, "HC"),
        ("II", "SOFTCOST", "118-13-000", True, "SC_TOTAL"), ("1", "CONSULTANCY SERVICES FEE", "118-13-202", False, "SC"), 
        ("2", "QS SERVICES", "118-13-201", False, "SC"), ("3", "PROJECT MANAGEMENT SERVICES", "118-13-203", False, "SC"), 
        ("4", "INSURANCE COVERAGE", "118-13-300", False, "SC"), ("IV", "TOTAL, EXCLD PPN", "", True, "TOTAL")
    ]

    r_idx = 10
    for sn, desc, coa, is_bold, cat in row_mapping:
        # Calculate % based on Global Totals and Category
        global_val = global_cost.get(desc, 0)
        if cat == "HC": pct = global_val / safe_hc
        elif cat == "SC": pct = global_val / safe_sc
        elif cat == "SC_TOTAL": pct = global_val / safe_hc # Softcost total vs Hardcost
        elif cat == "TOTAL": pct = global_val / safe_hc # Grand total vs Hardcost
        else: pct = 0

        ws.cell(row=r_idx, column=1, value=sn).alignment = center_align
        ws.cell(row=r_idx, column=2, value=desc).alignment = left_align
        ws.cell(row=r_idx, column=3, value=coa).alignment = center_align
        
        # Write Percentage
        pct_cell = ws.cell(row=r_idx, column=4, value=pct)
        pct_cell.alignment = center_align
        pct_cell.number_format = '0.00%'

        for c in range(1, 5):
            ws.cell(row=r_idx, column=c).border = black_border
            ws.cell(row=r_idx, column=c).font = bold_font if is_bold else reg_font

        col_offset = 5
        for pid, pdata in project_list:
            val = global_cost.get(desc, 0) if pid == "TOTAL" else tot_cache[pid].get(desc, 0)
            
            if pid == "TOTAL":
                gba_f = tot_gba if tot_gba > 0 else 1; gfa_f = tot_gfa if tot_gfa > 0 else 1
                sgfa_f = tot_sgfa if tot_sgfa > 0 else 1; nfa_f = (tot_gfa*0.82) if tot_gfa > 0 else 1
            else:
                d = pdata.get("data", {})
                gba_f = float(d.get("m_gba", 1) if d.get("m_gba", 0) > 0 else 1)
                gfa_f = float(d.get("m_gfa", 1) if d.get("m_gfa", 0) > 0 else 1)
                sgfa_f = float(d.get("m_sgfa", 1) if d.get("m_sgfa", 0) > 0 else 1)
                nfa_f = gfa_f * 0.82
            
            for j, v in enumerate([val, val/gba_f, val/gfa_f, val/sgfa_f, val/nfa_f]):
                c = ws.cell(row=r_idx, column=col_offset+j, value=v)
                c.number_format = '#,##0'
                c.border = black_border
                c.font = bold_font if is_bold else reg_font
                if is_bold: c.fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
            col_offset += 5
        r_idx += 1

    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 35
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 10
    for c in range(5, col_offset): ws.column_dimensions[get_column_letter(c)].width = 16
    ws.freeze_panes = 'E10'
    wb.save(output)
    return output.getvalue()
#endregion

def show_portfolio_summary():
    st.title("Summary")
    
    # ==========================================
    # 1. INITIALIZE EDITABLE SESSION STATE
    # ==========================================
    if "port_meta" not in st.session_state:
        st.session_state.port_meta = {
            "title": "PROJECT PORTFOLIO | PIK2.D2.GINZA.MIDTOWN OPT.2 R(1)",
            "ref": "REF. DATA R(0) | CONCEPT DWG 2026-02-02.DPA",
            "version": "R (1) OPT2",
            "updated": "02-02-2026",
            "created": "02-02-2026"
        }

    if "port_assumptions" not in st.session_state:
        st.session_state.port_assumptions = pd.DataFrame({
            "No.": [str(i) for i in range(1, 18)],
            "Assumption Description": [
                "Include Vacuum Project + Urugan kembali asumsi 1m",
                "Foundation System standard pilecaps.",
                "No Basement and No Parking Podium.",
                "Parking provison limited to ON STREET LEVEL parking; Floor Hardener finish",
                "Floor to Floor Height at 3.5M",
                "Facade Alumunium Window Wall - + Grill Outdoor AC",
                "External Façade Precast, No double skin for parking podium if any.",
                "Ground Lobby Finishes completed with Artificial stone & HT.",
                "Typical Corridor | Floor finishes : HT | Wall Finishes : Cement Sand Plaster c/w Emulsion Paint.",
                "Aircon System | Apartement : AC Split | Hotel : VRF SYSTEM",
                "SBO Rebars @ Rp. 10.000/kg",
                "Excluded Smarthome",
                "Lift : Luxury Apartment : 8 Private Lift + 2 Services Lift | Hotel 3* : 3 Passenger Lift + 1 Services Lift\nTerrace Village : 16 Private Lift + 8 Services Lift | Retail : No Elevator + Escalator 12 units\nApartment 2 : 4 Passenger Lift + 2 Services Lift\nPodium Village : 10 Private Lift + 5 Services Lift",
                "Exclude Wardrobe",
                "FFE : Kitchen cabinet, Hob & Hood, Refrigerator & Washing Machine",
                "Water Heater : Installation only",
                "Based on Resume Calculation DP dated on 2026.02.02"
            ]
        })

    # ==========================================
    # 2. TABS SETUP
    # ==========================================
    summary_list = ["Pengaturan", "FAD", "Rekap"]
    summary_tabs = st.tabs(summary_list)
    
    # --- TAB 1: EDITABLE NATIVE COMPONENTS ---
    with summary_tabs[0]:
        st.subheader("1. Header Configuration")
        col1, col2 = st.columns(2)
        st.session_state.port_meta["title"] = col1.text_input("Project Title", value=st.session_state.port_meta["title"])
        st.session_state.port_meta["ref"] = col2.text_input("Reference Data", value=st.session_state.port_meta["ref"])
        
        col3, col4, col5 = st.columns(3)
        st.session_state.port_meta["version"] = col3.text_input("Version", value=st.session_state.port_meta["version"])
        st.session_state.port_meta["updated"] = col4.text_input("Updated Date", value=st.session_state.port_meta["updated"])
        st.session_state.port_meta["created"] = col5.text_input("Created Date", value=st.session_state.port_meta["created"])

        st.markdown("---")
        
        st.subheader("2. Assumptions Configuration")
        edited_assumptions = st.data_editor(
            st.session_state.port_assumptions,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config={
                "No.": st.column_config.NumberColumn("No.", width="small"),
                "Assumption Description": st.column_config.TextColumn("Assumption Description", width="large"),
            }
        )
        st.session_state.port_assumptions = edited_assumptions

    # --- TAB 2: EXACT FORMAT MIRROR (HTML/CSS) ---
    with summary_tabs[1]:
        st.subheader("Feasibility Analysis Data (FAD)")

        # 1. DATA PREPARATION (Define raw_data BEFORE anything else)
        raw_data = []
        tot_gba = tot_gfa = tot_sgfa = tot_budget = 0
        
        # Loop through projects to build the data list
        for sn, (pid, pdata) in enumerate(st.session_state.projects.items(), 1):
            # Recalculate fresh numbers
            gba, gfa, sgfa, budget, qty = calculate_project_totals(pdata, pdata.get("type", "Hotel"))
            
            raw_data.append({
                "SN": sn,
                "AREA": pdata.get("name", f"Project {sn}"),
                "GBA": gba, "GFA": gfa, "SGFA": sgfa,
                "QTY": qty, 
                "UNIT": "Units" if "Hotel" not in pdata.get("type", "") else "RoomKey",
                "BUDGET": budget,
                "R_GBA": budget / gba if gba > 0 else 0,
                "R_GFA": budget / gfa if gfa > 0 else 0,
                "R_SGFA": budget / sgfa if sgfa > 0 else 0
            })
            tot_gba += gba; tot_gfa += gfa; tot_sgfa += sgfa; tot_budget += budget

        # Add the TOTAL row
        raw_data.append({
            "SN": "", "AREA": "TOTAL",
            "GBA": tot_gba, "GFA": tot_gfa, "SGFA": tot_sgfa,
            "QTY": None, "UNIT": "TOTAL",
            "BUDGET": tot_budget,
            "R_GBA": tot_budget / tot_gba if tot_gba > 0 else 0,
            "R_GFA": tot_budget / tot_gfa if tot_gfa > 0 else 0,
            "R_SGFA": tot_budget / tot_sgfa if tot_sgfa > 0 else 0
        })

        # 2. UI CONTROLS (Now they can safely see raw_data)
        col_btn1, col_btn2, _ = st.columns([1.5, 1.5, 3])
        
        with col_btn2:
            if st.button("Sync", use_container_width=True):
                force_recalculate_all_projects()
                st.rerun()
                
        with col_btn1:
            # This will now work because raw_data was defined in Step 1
            excel_output = generate_exact_portfolio_excel(
                st.session_state.port_meta, 
                raw_data, 
                st.session_state.port_assumptions
            )
            
            st.download_button(
                label="Download Excel",
                data=excel_output,
                file_name="ASG_Portfolio_Summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )
                
        # 1. CSS Styles (Flush left to avoid markdown code blocks)
        css_styles = """<style>
.asg-container { 
    font-family: Calibri, sans-serif; 
    font-size: 13px; 
    color: #000000 !important; 
    background-color: #FFFFFF !important; 
    padding: 15px;
    border-radius: 5px;
}
.asg-header {
    background-color: #0070C0 !important; color: #FFFFFF !important; padding: 6px 12px; 
    font-weight: bold; font-size: 13px; display: flex; justify-content: space-between;
    line-height: 1.4; margin-bottom: 15px;
}
.asg-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; background-color: #FFFFFF !important; }
.asg-table th, .asg-table td { border: 2px solid #000000 !important; padding: 5px 8px; text-align: right; vertical-align: middle; color: #000000 !important; }
.asg-table th { background-color: #F2F2F2 !important; text-align: center; font-weight: bold; color: #000000 !important; }
.asg-table td.left { text-align: left; font-weight: bold; }
.asg-table td.center { text-align: center; font-weight: bold; }
.asg-table .bold-row td { font-weight: bold; }
.asg-assumptions { width: 100%; border-collapse: collapse; font-size: 12px; background-color: #FFFFFF !important; }
.asg-assumptions td { border: 1px solid #D9D9D9 !important; padding: 4px 8px; color: #000000 !important; }
.asg-assumptions .yellow-header { background-color: #FFD966 !important; font-weight: bold; text-align: left; color: #000000 !important; }
</style>"""

        # 2. Dynamic Header Block
        header_html = f"""<div class="asg-container">
<div class="asg-header">
    <div>
        ASG GROUP PROPERTY DEVELOPMENT<br>
        QS & PROCUREMENT DIVISION<br>
        {st.session_state.port_meta["title"]}<br>
        {st.session_state.port_meta["ref"]}
    </div>
    <div style="text-align: right;">
        VERSION &nbsp;&nbsp;: {st.session_state.port_meta["version"]}<br>
        UPDATED &nbsp;: {st.session_state.port_meta["updated"]}<br>
        CREATED &nbsp;: {st.session_state.port_meta["created"]}
    </div>
</div>"""

        # 3. Dynamic Data Table Core
        table_start = """<table class="asg-table">
<thead>
    <tr>
        <th rowspan="2" style="width: 3%;">SN</th>
        <th rowspan="2" style="width: 18%;">AREA</th>
        <th colspan="3">BUILDING AREA (M2)</th>
        <th colspan="2" style="width: 10%;">UNIT</th>
        <th rowspan="2" style="width: 14%;">BUDGET ESTIMATE<br>RP</th>
        <th colspan="3">COST RATIO RP/M2</th>
    </tr>
    <tr>
        <th>GBA</th><th>GFA</th><th>SGFA</th>
        <th></th><th></th>
        <th>GBA</th><th>GFA</th><th>SGFA</th>
    </tr>
</thead>
<tbody>"""
        
        # 4. Generate Dynamic Rows from Active Projects
        table_rows = ""
        tot_gba = tot_gfa = tot_sgfa = tot_budget = 0
        
        for sn, (pid, pdata) in enumerate(st.session_state.projects.items(), 1):
            d = pdata.get("data", {})
            name = pdata.get("name", f"Project {sn}")
            ptype = pdata.get("type", "")
            
            gba = float(d.get("m_gba", 0.0))
            gfa = float(d.get("m_gfa", 0.0))
            sgfa = float(d.get("m_sgfa", 0.0))
            qty = float(d.get("m_rooms", 0.0))
            budget = float(d.get("grand_total_project", 0.0))
            
            if "Hotel" in ptype: unit_lbl = "RoomKey"
            elif "Parking" in ptype: unit_lbl = "lots"
            else: unit_lbl = "Units"
            
            r_gba = budget / gba if gba > 0 else 0
            r_gfa = budget / gfa if gfa > 0 else 0
            r_sgfa = budget / sgfa if sgfa > 0 else 0
            
            table_rows += f"""<tr class="bold-row">
<td class="center">{sn}</td>
<td class="left">{name}</td>
<td>{gba:,.2f}</td><td>{gfa:,.2f}</td><td>{sgfa:,.2f}</td>
<td class="center">{qty:,.0f}</td><td class="center">{unit_lbl}</td>
<td>{budget:,.0f}</td>
<td>{r_gba:,.0f}</td><td>{r_gfa:,.0f}</td><td>{r_sgfa:,.0f}</td>
</tr>"""
            
            tot_gba += gba
            tot_gfa += gfa
            tot_sgfa += sgfa
            tot_budget += budget

        tot_r_gba = tot_budget / tot_gba if tot_gba > 0 else 0
        tot_r_gfa = tot_budget / tot_gfa if tot_gfa > 0 else 0
        tot_r_sgfa = tot_budget / tot_sgfa if tot_sgfa > 0 else 0

        table_end = f"""<tr class="bold-row" style="background-color: #F2F2F2;">
<td class="center" colspan="2">TOTAL</td>
<td>{tot_gba:,.2f}</td><td>{tot_gfa:,.2f}</td><td>{tot_sgfa:,.2f}</td>
<td class="center" colspan="2">TOTAL</td>
<td>{tot_budget:,.0f}</td>
<td>{tot_r_gba:,.0f}</td><td>{tot_r_gfa:,.0f}</td><td>{tot_r_sgfa:,.0f}</td>
</tr>
</tbody>
</table>"""

        assumptions_html = """<table class="asg-assumptions">
<tr>
    <td class="yellow-header" style="width: 3%;">I.</td>
    <td class="yellow-header">ASSUMPTIONS</td>
</tr>"""
        for _, row in st.session_state.port_assumptions.iterrows():
            num = row.get("No.", "")
            desc = row.get("Assumption Description", "")
            if pd.notna(desc) and str(desc).strip() != "":
                assumptions_html += f"""<tr>
<td style="text-align: center;">{num}</td>
<td>{desc}</td>
</tr>"""
        assumptions_html += """</table></div>"""

        full_html = css_styles + header_html + table_start + table_rows + table_end + assumptions_html
        
        st.markdown(full_html, unsafe_allow_html=True)

# --- TAB 3: WIDE RECAP COST ---
    with summary_tabs[2]:
        st.subheader("Comprehensive Recap Matrix (Cost & Ratios)")
        
        if "recap_math_engine" not in st.session_state:
            _ = generate_recap_excel(st.session_state.port_meta, st.session_state.projects)
            
        math_engine = st.session_state.recap_math_engine
        
        col_btn, col_info = st.columns([1.5, 4.5])
        with col_btn:
            recap_excel_data = generate_recap_excel(
                st.session_state.port_meta, 
                st.session_state.projects
            )
            st.download_button(
                label="Download Excel",
                data=recap_excel_data,
                file_name="ASG_Recap_Cost_Wide.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )


        # --- GENERATE HTML PREVIEW ---
        bg_colors = ["#EAEAEA", "#FCE4D6", "#F2DCDB", "#E1D5E7", "#DDEBF7", "#E2EFDA", "#D9E1F2", "#F4B084", "#FFF2CC"]
        project_list = [("TOTAL", {"name": "TOTAL"})] + list(st.session_state.projects.items())

        tot_cache = {}; global_cost = {}; tot_gba = tot_gfa = tot_sgfa = 0
        for pid, pdata in st.session_state.projects.items():
            vals = math_engine(pdata)
            tot_cache[pid] = vals
            for k, v in vals.items(): global_cost[k] = global_cost.get(k, 0) + v
            d = pdata.get("data", {})
            tot_gba += float(d.get("m_gba", 0)); tot_gfa += float(d.get("m_gfa", 0)); tot_sgfa += float(d.get("m_sgfa", 0))

        global_hc = global_cost.get("HARDCOST", 0); safe_hc = global_hc if global_hc > 0 else 1
        global_sc = global_cost.get("SOFTCOST", 0); safe_sc = global_sc if global_sc > 0 else 1

        html_str = """
        <style>
        .recap-wrapper { 
            width: 100%; 
            overflow-x: auto; 
            font-family: Calibri, sans-serif; 
            font-size: 11px; 
        }

        /* DESKTOP ONLY: Add the comparison space */
        @media (min-width: 1024px) {
            .recap-wrapper { 
                padding-right: 600px; 
            }
        }

        /* MOBILE SPECIFIC: Ensure it takes the full width and handles sticky better */
        @media (max-width: 1023px) {
            .recap-wrapper { 
                padding-right: 0px; 
            }
            .sticky-col2 { 
                min-width: 120px !important; /* Shrink description for small screens */
            }
        }

        .recap-table { 
            border-collapse: separate; 
            border-spacing: 0; 
            white-space: nowrap; 
        }

        .recap-table th {
            text-align: center !important; /* Forces all header text to center */
            font-weight: bold; 
            vertical-align: middle;
            border-top: 1px solid #000;
            border-right: 1px solid #000;
            border-bottom: 1px solid #000;
            border-left: 1px solid #000;
            padding: 4px 6px;
            background-color: #fff;
        }
        
        .recap-table td {
            border-right: 1px solid #000;
            border-bottom: 1px solid #000;
            border-left: 1px solid #000;
            padding: 4px 6px;
            background-color: #fff;
        }

        .sticky-col, .sticky-col2 { 
            position: sticky; 
            background-color: #F2F2F2 !important; 
            z-index: 5; 
        }
        
        .sticky-col3, .sticky-col4 { 
            background-color: #F2F2F2 !important; 
            z-index: 5; 
        }

        .sticky-col  { left: 0; }
        .sticky-col2 { left: 20px; text-align: left !important; }
        .bold-row { font-weight: bold; background-color: #F9F9F9; }
        
        </style>
        <div class="recap-wrapper"><table class="recap-table">
        """

        html_str += "<tr><th rowspan='4' class='sticky-col'>SN</th><th rowspan='4' class='sticky-col2' style='min-width:200px;'>DESCRIPTION</th><th rowspan='4' class='sticky-col3'>COA</th><th rowspan='4' class='sticky-col4'>%</th>"
        for i, (pid, pdata) in enumerate(project_list):
            color = bg_colors[i % len(bg_colors)]
            html_str += f"<th colspan='5' style='background-color:{color}; color:#000;'>{pdata.get('name', 'PROJECT').upper()}</th>"
        html_str += "</tr><tr>"
        for i in range(len(project_list)):
            color = bg_colors[i % len(bg_colors)]
            html_str += f"<th style='background-color:{color};'>ESTIMATE</th><th colspan='4' style='background-color:{color};'>Cost Ratio (Rp/m2)</th>"
        html_str += "</tr><tr>"
        for i in range(len(project_list)):
            color = bg_colors[i % len(bg_colors)]
            html_str += f"<th style='background-color:{color};'>TOTAL</th><th style='background-color:{color};'>GBA</th><th style='background-color:{color};'>GFA</th><th style='background-color:{color};'>SGFA</th><th style='background-color:{color};'>NFA</th>"
        html_str += "</tr><tr>"
        for i, (pid, pdata) in enumerate(project_list):
            color = bg_colors[i % len(bg_colors)]
            if pid == "TOTAL":
                gba, gfa, sgfa, nfa = tot_gba, tot_gfa, tot_sgfa, tot_gfa * 0.82
            else:
                d = pdata.get("data", {})
                gba, gfa, sgfa = float(d.get("m_gba", 0)), float(d.get("m_gfa", 0)), float(d.get("m_sgfa", 0))
                nfa = gfa * 0.82
            html_str += f"<th style='background-color:{color};'>Rp</th><th style='background-color:{color};'>{gba:,.0f}</th><th style='background-color:{color};'>{gfa:,.0f}</th><th style='background-color:{color};'>{sgfa:,.0f}</th><th style='background-color:{color};'>{nfa:,.0f}</th>"
        html_str += "</tr>"

        row_mapping = [
            ("I", "HARDCOST", "118-14-000", True, "HC"), ("1", "PRELIMINARIES WORKS", "118-14-100", False, "HC"), 
            ("2", "EARTHWORKS", "118-14-200", False, "HC"), ("3", "FOUNDATIONS", "118-14-300", False, "HC"), 
            ("4", "STRUCTURAL WORKS", "118-14-500", False, "HC"), ("5", "ARCHITECTURAL WORKS", "118-14-600", False, "HC"),
            ("6", "FF & E", "118-14-700", False, "HC"), ("7", "M.E.P WORKS", "118-14-800", False, "HC"), 
            ("8", "UTILITY CONNECTION", "118-13-900", False, "HC"), ("9", "EXTERNAL WORKS", "118-14-930", False, "HC"), 
            ("10", "FACILITY", "118-14-960", False, "HC"), ("11", "CONTINGENCIES", "", False, "HC"),
            ("II", "SOFTCOST", "118-13-000", True, "SC_TOTAL"), ("1", "CONSULTANCY SERVICES FEE", "118-13-202", False, "SC"), 
            ("2", "QS SERVICES", "118-13-201", False, "SC"), ("3", "PROJECT MANAGEMENT SERVICES", "118-13-203", False, "SC"), 
            ("4", "INSURANCE COVERAGE", "118-13-300", False, "SC"), ("IV", "TOTAL, EXCLD PPN", "", True, "TOTAL")
        ]

        for sn, desc, coa, is_bold, cat in row_mapping:
            global_val = global_cost.get(desc, 0)
            if cat == "HC": pct = global_val / safe_hc
            elif cat == "SC": pct = global_val / safe_sc
            elif cat in ["SC_TOTAL", "TOTAL"]: pct = global_val / safe_hc
            else: pct = 0

            tr_class = " class='bold-row'" if is_bold else ""
            html_str += f"<tr{tr_class}>"
            # Sticky Columns (Anchor columns remain neutral grey)
            html_str += f"<td class='sticky-col' style='text-align:center;'>{sn}</td>"
            html_str += f"<td class='sticky-col2'>{desc}</td>"
            html_str += f"<td class='sticky-col3'>{coa}</td>"
            html_str += f"<td class='sticky-col4'>{pct*100:.2f}%</td>"
            
            # Project Data Columns (Colored to match headers)
            for i, (pid, pdata) in enumerate(project_list):
                val = global_cost.get(desc, 0) if pid == "TOTAL" else tot_cache[pid].get(desc, 0)
                color = bg_colors[i % len(bg_colors)] # Get the header's color
                
                # Calculate divisors
                if pid == "TOTAL":
                    gba_f, gfa_f, sgfa_f = tot_gba or 1, tot_gfa or 1, tot_sgfa or 1
                    nfa_f = (tot_gfa * 0.82) or 1
                else:
                    d = pdata.get("data", {})
                    gba_f = float(d.get("m_gba") or 1)
                    gfa_f = float(d.get("m_gfa") or 1)
                    sgfa_f = float(d.get("m_sgfa") or 1)
                    nfa_f = gfa_f * 0.82 or 1
                
                # Apply the background color style to every <td> in this column
                c_style = f"style='background-color:{color};'"
                
                html_str += f"<td {c_style}>{val:,.0f}</td>"
                html_str += f"<td {c_style}>{val/gba_f:,.0f}</td>"
                html_str += f"<td {c_style}>{val/gfa_f:,.0f}</td>"
                html_str += f"<td {c_style}>{val/sgfa_f:,.0f}</td>"
                html_str += f"<td {c_style}>{val/nfa_f:,.0f}</td>"
            
            # Spacer for desktop 'over-scroll' comparison
            html_str += "<td style='border:none; background:transparent; min-width:600px;'></td>"
            html_str += "</tr>"

        html_str += "</table></div>"
        st.markdown(html_str, unsafe_allow_html=True)

#region --- LOGIN SCREEN AND SIDE BAR(INSIDE MAIN APP) ---
from supabase import create_client, Client

# 1. SETUP & SESSION CHECK
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

import time

def login_screen():
    st.markdown("""
        <style>
            /* Hide the default Streamlit sidebar and top header */
            [data-testid="stSidebar"] {display: none;}
            [data-testid="stHeader"] {display: none;}
            
            /* --- RESPONSIVE SPACING FIX --- */
            /* 1. Default spacing for Desktop (PC) */
            .block-container {
                padding-top: 4rem !important; 
            }
            
            /* 2. Overrides for Mobile (Screens smaller than 768px) */
            @media (max-width: 768px) {
                .block-container {
                    padding-top: 1rem !important; /* Pulls everything up on mobile */
                }
                /* Hides the empty left column on mobile so it doesn't push the form down */
                [data-testid="column"]:nth-of-type(1) {
                    display: none !important;
                }
            }
            
            /* Typography & Alignment */
            .login-header {
                text-align: center;
                margin-top: 1rem;
                margin-bottom: 1.5rem;
            }
            .login-title {
                color: #1E3A8A;
                font-size: 26px;
                font-weight: 700;
                margin-bottom: 5px;
            }
            .login-subtitle {
                color: #6B7280;
                font-size: 15px;
            }
            
            /* Form Card Styling */
            [data-testid="stForm"] {
                border: 1px solid rgba(49, 51, 63, 0.1);
                border-radius: 12px;
                padding: 2rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
                background-color: var(--background-color);
            }
            
            /* HTML Logo Styling */
            .logo-container {
                display: flex;
                justify-content: center;
                margin-bottom: 0.5rem;
            }
            .logo-container img {
                width: 45%; /* Keeps the logo scaled similarly to the old column layout */
                max-width: 200px;
            }
        </style>
    """, unsafe_allow_html=True)
        
    # 2. Adjust Layout Proportions (creates a clean, focused center column)
    col1, center_col, col3 = st.columns([1.5, 2, 1.5])
    
    with center_col:
        # 3. Nesting the logo right above the text for perfect alignment
        logo_col_1, logo_col_2, logo_col_3 = st.columns([1, 1.5, 1])
        with logo_col_2:
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQWTNsgu_c6WzJAehb4zQ3qdTKNauleAXe4w&s", use_container_width=True)
            
        st.markdown("""
            <div class="login-header">
                <div class="login-title">Project Feasibility Study</div>
                <div class="login-subtitle">Please sign in to your account</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 4. The Login Form
        with st.form("login_gate", clear_on_submit=False):
            # Added placeholders for better UX
            email = st.text_input("Email", placeholder="name@agungsedayu.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.write("") # Small gap before button
            submit = st.form_submit_button("Sign In", use_container_width=True, type="primary")
            
            if submit:
                # Basic input validation
                if not email or not password:
                    st.warning("Please enter both email and password.", icon="⚠️")
                else:
                    # Added a spinner so the UI doesn't freeze during API calls
                    with st.spinner("Authenticating securely..."):
                        try:
                            res = supabase.auth.sign_in_with_password({
                                "email": email, 
                                "password": password
                            })
                            
                            supabase.postgrest.auth(res.session.access_token)
                            st.session_state.logged_in = True
                            st.session_state.user = res.user
                            st.session_state.access_token = res.session.access_token

                            # Clear projects so main_app() re-loads from Supabase
                            for key in ["projects", "storage_loaded"]:
                                if key in st.session_state:
                                    del st.session_state[key]
                            
                            # Format username to look cleaner (e.g., john.doe -> John Doe)
                            raw_username = res.user.email.split("@")[0]
                            clean_username = raw_username.replace('.', ' ').title()
                            
                            st.success(f"Identity Verified. Welcome back, **{clean_username}**! 👋")
                            time.sleep(0.8)  # Slightly faster transition
                            st.rerun()
                            
                        except Exception as e:
                            # Catch generic invalid credential messages and make them user-friendly
                            error_msg = str(e)
                            if "Invalid login credentials" in error_msg or "400" in error_msg:
                                st.error("Invalid email or password. Please try again.", icon="❌")
                            else:
                                st.error(f"Authentication error: {error_msg}", icon="🚨")

    # 5. Professional Footer
    st.markdown(f"""
        <hr style="border: none; border-top: 1px solid #E5E7EB; margin-top: 50px; margin-bottom: 20px;">
        <div style='text-align: center; color: #9CA3AF; font-size: 12px; font-family: sans-serif; line-height: 1.6;'>
            v{APP_VERSION} | &copy; 2026 QS & Procurement - ASG. All rights reserved.<br>
            <span style="letter-spacing: 1px; font-weight: 500;">INTERNAL CORPORATE USE ONLY</span>
        </div>
    """, unsafe_allow_html=True)

# 3. THE ACTUAL APPLICATION
def main_app():
    # The 'Assembler'
    if "projects" not in st.session_state:
        stored_data = load_data()
        
        if stored_data:
            st.session_state.projects = stored_data["projects"]
            st.session_state.current_proj_id = stored_data["current_proj_id"]
            st.session_state.proj_counter = stored_data["proj_counter"]
            
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
            st.session_state.projects = {"proj_1": {"name": "New Project 1", "type": "Hotel", "data": {}}}
            st.session_state.current_proj_id = "proj_1"
            st.session_state.proj_counter = 1
        
        st.session_state.storage_loaded = True

    #region --- SIDEBAR ----
    st.sidebar.title("Main Navigation")

    user_email = st.session_state.get("user").email
    username = user_email.split("@")[0]
    st.sidebar.markdown(f"Hello, **{username}**!")


    page_choice = st.sidebar.radio(
        "Pilih Pekerjaan:",
        ["Cost Calculator", "Area Calculator", "Database", "Summary", "Project Archive"]
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
        save_data() # SAVE HERE
        needs_rerun = True

    if new_type != curr_proj["type"]:
        st.session_state.projects[curr_id]["type"] = new_type
        st.session_state.projects[curr_id]["data"] = {}
        save_data() # SAVE HERE
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
        if st.button("Hapus", type="secondary", use_container_width=True):
            del st.session_state.projects[st.session_state.current_proj_id]
            st.session_state.current_proj_id = list(st.session_state.projects.keys())[0]
            save_data()
            st.rerun()
        
        if st.sidebar.button("Hapus Semua Proyek", type="secondary", use_container_width=True):
            st.session_state.projects = {"proj_1": {"name": "New Project 1", "type": "Hotel", "data": {}}}
            st.session_state.proj_counter = 1
            st.session_state.current_proj_id = "proj_1"
            save_data()
            st.rerun()

    # --- NEW: GLOBAL PROJECT EDITOR IN SIDEBAR ---
    st.sidebar.markdown("---")

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

    if st.sidebar.button("Logout", type="primary"):
        st.session_state.logged_in = False
        st.session_state.access_token = None
        st.session_state.user = None
        del st.session_state["projects"]
        del st.session_state["storage_loaded"]
        st.rerun()
        
    st.sidebar.caption(f"v{APP_VERSION} | © 2026 QS & Procurement - ASG")
    #endregion
    
    if page_choice == "Area Calculator":
        show_area_calculator()
    elif page_choice == "Database":
        show_project_database()
    elif page_choice == "Summary":
        show_portfolio_summary()
    elif page_choice == "Project Archive":
        show_snapshots()
    else:
        show_cost_estimator()

# 4. THE GATEKEEPER LOGIC
# Replace your entire gatekeeper section at the bottom with this:

if not st.session_state.logged_in:
    login_screen()
else:
    # Re-apply token on EVERY script run, not just after login
    token = st.session_state.get("access_token")
    if token:
        supabase.postgrest.auth(token)
    main_app()
#endregion

#region --- THANK YOU ---
# Version: 1.1.0
# Environment: Streamlit 1.56.0, Python 3.13
# for the future me or any IT person that might look at this code,
# this code is made in 2026, by a totally newbie programmer wannabe, 
# but with over 8 years of work experience and Architecture Bachelor 
# (architure as in construction, not that architecture)
# if someday this might not work, know that I (Boris Prilyan Sidabutar, B. Arch) 
# make this alone (many thanks especially to Jesus and for Gemini and Claude too)
#endregion
