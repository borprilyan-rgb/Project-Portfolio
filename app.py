import streamlit as st
import pandas as pd
import altair as alt
from num2words import num2words
from streamlit_local_storage import LocalStorage

local_storage = LocalStorage()

def n2w(amount):
    try:
        amount = float(amount)
        if amount >= 1_000_000_000_000:
            return f"{amount / 1_000_000_000_000:,.2f} Triliun"
        elif amount >= 1_000_000_000:
            return f"{amount / 1_000_000_000:,.2f} Miliar"
        elif amount >= 1_000_000:
            return f"{amount / 1_000_000:,.2f} Juta"
        else:
            return f"{amount:,.0f}"
    except:
        return "0"

def format_idr_compact(amount):
    amount = float(amount)
    if amount >= 1_000_000_000_000:
        return f"{amount / 1_000_000_000_000:,.2f} T"
    elif amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:,.2f} M"
    elif amount >= 1_000_000:
        return f"{amount / 1_000_000:,.1f} Jt"
    else:
        return f"{amount:,.0f}"

# ---------------------------------------------------------------------------
# HELPER: compute custom cost totals from saved smart_custom_costs list
# Uses new schema: Rate * Quantity (flat). No dep_map, no Linked Dependency.
# ---------------------------------------------------------------------------
def compute_custom_buckets(items: list) -> dict:
    """
    Returns a dict with keys matching category bucket names plus 'total'.
    Always uses Rate * Quantity (new flat schema).
    """
    buckets = {
        "prelim": 0.0, "earth": 0.0, "found": 0.0, "struc": 0.0, "arch": 0.0,
        "ffe": 0.0, "mep": 0.0, "ext": 0.0, "fac": 0.0, "cont": 0.0,
        "qs": 0.0, "pm": 0.0, "cons": 0.0, "ins": 0.0, "util": 0.0,
        "total": 0.0,
    }
    cat_map = {
        "HC - 1. Preliminaries":          "prelim",
        "HC - 2. Earthwork":              "earth",
        "HC - 3. Foundation":             "found",
        "HC - 4. Structural Work":        "struc",
        "HC - 5. Architectural Work":     "arch",
        "HC - 6. FF&E & Kitchen":         "ffe",
        "HC - 7. MEP Works":              "mep",
        "HC - 8. External Works":         "ext",
        "HC - 9. Facilities & Misc":      "fac",
        "HC - 10. Contingencies":         "cont",
        "SC - 1. QS Services":            "qs",
        "SC - 2. PM Services":            "pm",
        "SC - 3. Other Consultancy Fee":  "cons",
        "SC - 4. Insurance Coverage":     "ins",
        "SC - 5. Utility Connection":     "util",
    }
    for item in items:
        rate = float(item.get("Rate (Rp)", 0.0) or 0.0)
        # support both old key (Multiplier (Qty)) and new key (Quantity)
        qty  = float(item.get("Quantity", item.get("Multiplier (Qty)", 1.0)) or 1.0)
        val  = rate * qty
        key  = cat_map.get(item.get("Category", ""), None)
        if key:
            buckets[key] += val
        buckets["total"] += val
    return buckets

# ---------------------------------------------------------------------------
# PROJECT DATABASE
# ---------------------------------------------------------------------------
PROJECT_DATABASE = {
    "Apartment": {
        "struc_earth": 25000.0, "struc_found": 400000.0, "struc_work": 1933000.0,
        "arch_base": 1058000.0, "lobby": 1500000.0,
        "facade_precast_rate": 800000.0, "facade_window_rate": 1250000.0, "facade_double_rate": 2500000.0,
        "door_wood": 3500000.0, "door_steel": 7000000.0,
        "hw_wood": 750000.0, "hw_steel": 1850000.0, "door_glass": 1000000.0,
        "san_room_rate": 26875000.0, "san_pub_f": 98075000.0, "san_pub_m": 77050000.0,
        "san_dis": 30275000.0, "san_mushola": 36500000.0,
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
        "cons": 174000.0,
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
        "cons": 199000.0,
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
        "cons": 199000.0,
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
        "cons": 174000.0,
    },
    "Parking": {
        "arch_base": 668000.0,
        "mep": 4000000.0, "utility": 150000.0,
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
        "cons": 53000.0,
    },
}

# ---------------------------------------------------------------------------
# CALLBACKS
# ---------------------------------------------------------------------------
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
        st.session_state.current_proj_id = proj_ids[proj_labels.index(selected_label)]

# ---------------------------------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Project Portfolio", layout="wide")

if "projects" not in st.session_state:
    stored_data = local_storage.getItem("asg_calculator_backup")
    if stored_data and isinstance(stored_data, dict) and "projects_dict" in stored_data:
        st.session_state.projects        = stored_data["projects_dict"]
        st.session_state.current_proj_id = stored_data.get("current_proj_id", list(stored_data["projects_dict"].keys())[0])
        st.session_state.proj_counter    = stored_data.get("proj_counter", 1)
    elif stored_data and isinstance(stored_data, dict):
        # backward compat: old format (projects dict at root)
        st.session_state.projects = stored_data
        st.session_state.current_proj_id = list(stored_data.keys())[0]
        existing_ids = [int(k.split("_")[1]) for k in stored_data if k.startswith("proj_") and k.split("_")[1].isdigit()]
        st.session_state.proj_counter = max(existing_ids) if existing_ids else 1
    else:
        st.session_state.projects = {"proj_1": {"name": "New Project 1", "type": "Hotel", "data": {}}}
        st.session_state.current_proj_id = "proj_1"
        st.session_state.proj_counter = 1
    st.session_state.storage_loaded = True

# ---------------------------------------------------------------------------
# AREA CALCULATOR (unchanged from original)
# ---------------------------------------------------------------------------
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
    gba_placeholder  = st.sidebar.empty()
    gfa_placeholder  = st.sidebar.empty()
    sgfa_placeholder = st.sidebar.empty()
    units_placeholder = st.sidebar.empty()
    grand_total_gba = grand_total_gfa = grand_total_sgfa = grand_total_units = 0
    if int(num_plots) > 0:
        plot_tabs = st.tabs([f"Plot {i+1}" for i in range(int(num_plots))])
        for p_idx, p_tab in enumerate(plot_tabs):
            with p_tab:
                plot_gfa = plot_sgfa = plot_units = 0
                num_groups = blocks_per_plot[p_idx]
                if int(num_groups) > 0:
                    block_tabs = st.tabs([f"Block Group {g+1}" for g in range(int(num_groups))])
                    for g_idx, b_tab in enumerate(block_tabs):
                        with b_tab:
                            c1, c2, c3 = st.columns(3)
                            group_name  = c1.text_input("Group Name", value=f"Block Group {g_idx+1}", key=f"gn_{p_idx}_{g_idx}")
                            num_blocks  = c2.number_input("Number of Blocks", min_value=1, value=6, key=f"nb_{p_idx}_{g_idx}")
                            num_floors  = c3.number_input("Typical Floors", min_value=1, value=11, key=f"nf_{p_idx}_{g_idx}")
                            col_com1, col_com2 = st.columns(2)
                            core_area    = col_com1.number_input("Core Area per Floor", value=105.5, key=f"core_{p_idx}_{g_idx}")
                            corridor_area = col_com2.number_input("Corridor Area per Floor", value=88.8, key=f"corr_{p_idx}_{g_idx}")
                            st.markdown("**Typical Floor Unit Mix**")
                            default_mix = pd.DataFrame([
                                {"Unit Type": "2BR-1", "Net Area": 74.5, "Units/Floor": 2},
                                {"Unit Type": "3BR",   "Net Area": 95.5, "Units/Floor": 1},
                                {"Unit Type": "3BR'",  "Net Area": 96.1, "Units/Floor": 4},
                            ])
                            edited_mix = st.data_editor(default_mix, key=f"ed_{p_idx}_{g_idx}", num_rows="dynamic", use_container_width=True)
                            edited_mix["Net/Fl (Total)"]  = edited_mix["Net Area"] * edited_mix["Units/Floor"]
                            total_net_per_floor   = edited_mix["Net/Fl (Total)"].sum()
                            total_units_per_floor = edited_mix["Units/Floor"].sum()
                            sgfa_load_factor = (total_net_per_floor + corridor_area) / total_net_per_floor if total_net_per_floor > 0 else 1.0
                            gfa_load_factor  = (total_net_per_floor + corridor_area + core_area) / total_net_per_floor if total_net_per_floor > 0 else 1.0
                            edited_mix["SGFA per Unit"]   = (edited_mix["Net Area"] * sgfa_load_factor).round(2)
                            edited_mix["SGFA/Fl (Total)"] = (edited_mix["SGFA per Unit"] * edited_mix["Units/Floor"]).round(2)
                            edited_mix["GFA per Unit"]    = (edited_mix["Net Area"] * gfa_load_factor).round(2)
                            edited_mix["GFA/Fl (Total)"]  = (edited_mix["GFA per Unit"] * edited_mix["Units/Floor"]).round(2)
                            display_cols = ["Unit Type", "Net/Fl (Total)", "SGFA per Unit", "SGFA/Fl (Total)", "GFA per Unit", "GFA/Fl (Total)", "Units/Floor"]
                            display_df   = edited_mix[display_cols].copy()
                            display_df.rename(columns={"Units/Floor": "Units"}, inplace=True)
                            sum_sgfa_fl = display_df["SGFA/Fl (Total)"].sum()
                            sum_gfa_fl  = display_df["GFA/Fl (Total)"].sum()
                            group_net   = total_net_per_floor * num_blocks * num_floors
                            group_sgfa  = sum_sgfa_fl * num_blocks * num_floors
                            group_gfa   = sum_gfa_fl  * num_blocks * num_floors
                            group_units = total_units_per_floor * num_blocks * num_floors
                            summary_df  = pd.DataFrame({
                                "Per Floor Metric": ["Net Area", "SGFA", "GFA", "Units"],
                                "Floor Total": [f"{total_net_per_floor:,.2f}", f"{sum_sgfa_fl:,.2f}", f"{sum_gfa_fl:,.2f}", f"{int(total_units_per_floor)}"],
                                f"{group_name} ({num_blocks} Blk x {num_floors} Fl)": ["Total Net Area", "Total SGFA", "Total GFA", "Total Units"],
                                "Group Total": [f"{group_net:,.2f}", f"{group_sgfa:,.2f}", f"{group_gfa:,.2f}", f"{int(group_units)}"],
                            })
                            with st.expander(f"View Detailed Calculation Tables for {group_name}", expanded=False):
                                st.dataframe(display_df, use_container_width=True, hide_index=True)
                                st.dataframe(summary_df, use_container_width=True, hide_index=True)
                            plot_gfa   += group_gfa
                            plot_sgfa  += group_sgfa
                            plot_units += group_units
                st.markdown("---")
                st.subheader(f"Plot {p_idx+1} Non-Typical Areas")
                default_nt = pd.DataFrame([
                    {"Area Name": "Ground Floor", "Floors": 1, "Area/Floor (m2)": 0.0, "Include in GFA": False},
                    {"Area Name": "Podium Area",  "Floors": 1, "Area/Floor (m2)": 7548.0, "Include in GFA": False},
                    {"Area Name": "MEP",          "Floors": 1, "Area/Floor (m2)": 3471.0, "Include in GFA": False},
                    {"Area Name": "Clubhouse",    "Floors": 1, "Area/Floor (m2)": 0.0,    "Include in GFA": True},
                ])
                edited_nt = st.data_editor(default_nt, key=f"nt_{p_idx}", num_rows="dynamic", use_container_width=True)
                edited_nt["Total Area (m2)"] = edited_nt["Floors"] * edited_nt["Area/Floor (m2)"]
                total_nt_area = edited_nt["Total Area (m2)"].sum()
                nt_gfa_area   = edited_nt[edited_nt["Include in GFA"] == True]["Total Area (m2)"].sum()
                st.markdown(f"**Non-Typical Totals: {total_nt_area:,.2f} m2 (GBA) | {nt_gfa_area:,.2f} m2 (GFA)**")
                plot_gba = plot_gfa + total_nt_area
                plot_gfa = plot_gfa + nt_gfa_area
                st.divider()
                st.markdown(f"**PLOT {p_idx+1} GRAND TOTALS**")
                st.dataframe(pd.DataFrame({
                    "Plot Total GBA (m2)": [f"{plot_gba:,.2f}"],
                    "Plot Total GFA (m2)": [f"{plot_gfa:,.2f}"],
                    "Plot Total SGFA (m2)": [f"{plot_sgfa:,.2f}"],
                    "Plot Total Units": [f"{int(plot_units)}"],
                }), use_container_width=True, hide_index=True)
                grand_total_gba   += plot_gba
                grand_total_gfa   += plot_gfa
                grand_total_sgfa  += plot_sgfa
                grand_total_units += plot_units
    gba_placeholder.metric("Grand Total GBA",   f"{grand_total_gba:,.2f} m2")
    gfa_placeholder.metric("Grand Total GFA",   f"{grand_total_gfa:,.2f} m2")
    sgfa_placeholder.metric("Grand Total SGFA", f"{grand_total_sgfa:,.2f} m2")
    units_placeholder.metric("Grand Total Units", f"{int(grand_total_units)} Units")


# ---------------------------------------------------------------------------
# FLOORING SPEC CALLBACK
# ---------------------------------------------------------------------------
def update_price(metric_key, db_key):
    c_id = st.session_state.current_proj_id
    p_type = st.session_state.projects[c_id]["type"]
    c_type_key = f"{c_id}_{p_type}"
    selected_spec = st.session_state[f"temp_spec_{metric_key}_{c_type_key}"]
    st.session_state.projects[c_id]["data"][f"{metric_key}_spec_type"] = selected_spec
    db_val = PROJECT_DATABASE[p_type][db_key]
    if isinstance(db_val, dict):
        st.session_state[f"u_fl_{metric_key}_{c_type_key}"] = float(db_val.get(selected_spec, 0.0))


# ---------------------------------------------------------------------------
# CANONICAL PROJECT TOTALS
# Used by FAD, Rekap, and cost estimator – single source of truth.
# ---------------------------------------------------------------------------
def get_project_totals(proj_dict: dict) -> dict:
    """
    Compute hc_subtotal, hc_total, sc_total, grand_total for a project dict.
    Returns a dict with area metrics and every cost component.
    Custom costs use compute_custom_buckets (flat Rate × Quantity).
    """
    d      = proj_dict.get("data", {})
    p_type = proj_dict.get("type", "Hotel")
    pt     = PROJECT_DATABASE.get(p_type, PROJECT_DATABASE["Hotel"])

    def v(key, default=0.0):
        val = d.get(key, pt.get(key, default))
        if isinstance(val, (int, float)):
            return float(val)
        try:
            return float(val)
        except (ValueError, TypeError):
            return default

    gba    = v("m_gba");  gfa = v("m_gfa");  sgfa = v("m_sgfa")
    rooms  = v("m_rooms"); facade = v("m_facade")
    f_mult = 1.32

    # base hard costs
    v_earth  = gba * v("u_earth")
    v_found  = gba * v("u_found")
    v_struc  = gba * v("u_struc")
    v_arch   = (
        (gfa * v("u_arch"))
        + (facade * (v("r_fac_pre") / 100) * v("u_f_pre"))
        + (facade * (v("r_fac_win") / 100) * v("u_f_win"))
        + (facade * (v("r_fac_doub") / 100) * v("u_f_doub"))
        + (v("m_door_w") * v("u_d_wood"))
        + (v("m_door_g") * v("u_d_glass"))
        + (v("m_door_s") * v("u_d_steel"))
        + (v("m_lobby")  * v("u_lobby"))
        + (v("m_gondola") * v("u_gondola"))
        + (rooms * v("r_san_qty") * v("u_s_room"))
        + (v("m_toil_m") * v("u_s_pub_m"))
        + (v("m_toil_f") * v("u_s_pub_f"))
        + (v("m_toil_d") * v("u_s_dis"))
        + (v("m_mushola") * v("u_s_mushola"))
        + (v("m_door_w") * v("u_hw_wood"))
        + (v("m_door_s") * v("u_hw_steel"))
        + (gfa * (v("r_fl_ht")  / 100) * v("u_fl_ht")  * f_mult)
        + (gfa * (v("r_fl_vin") / 100) * v("u_fl_vin") * f_mult)
        + (gfa * (v("r_fl_mar") / 100) * v("u_fl_mar") * f_mult)
        + (v("m_carpet")  * v("u_carpet"))
        + (v("m_glass")   * v("u_glass"))
        + (rooms * v("r_rail_qty") * v("u_rail"))
        + (v("m_skylight") * v("u_sky"))
    )
    v_ffe  = (rooms * v("u_ffe")) + (rooms * v("u_kit")) + (v("u_misc") * float(d.get("misc_switch", 0)))
    v_mep  = gba * v("u_mep")
    v_ext  = v("m_land_m2") * v("u_ext")
    v_fac  = (v("m_fac_pub") * v("u_fac_p")) + (v("m_fac_res") * v("u_fac_r")) + (v("m_fac_proj") * v("u_fac_pr"))

    # FIXED: custom costs via canonical helper (Rate × Quantity, flat)
    buckets = compute_custom_buckets(d.get("smart_custom_costs", []))
    # utility is a SOFT cost in tab3 – keep consistent: exclude from hc_subtotal here
    # (utility is NOT in hc_subtotal in the tab2 live calc either)
    hc_subtotal = (
        v_earth + v_found + v_struc + v_arch + v_ffe + v_mep + v_ext + v_fac
        + buckets["earth"] + buckets["found"] + buckets["struc"] + buckets["arch"]
        + buckets["ffe"]   + buckets["mep"]   + buckets["ext"]   + buckets["fac"]
        + buckets["cont"]  # contingency custom goes into base before % is applied
    )
    v_prelim = hc_subtotal * 0.05 + buckets["prelim"]
    v_cont   = (hc_subtotal + v_prelim) * 0.03  # cont custom already in base
    hc_total = hc_subtotal + v_prelim + v_cont

    # soft costs
    v_util = gba * v("u_util")
    v_cons = gfa  * v("sc_cons")
    v_qs   = v("sc_qs_m") * v("sc_qs_r")
    v_pm   = v("sc_pm_m") * v("sc_pm_r")
    v_ins  = hc_subtotal  * (v("sc_ins") / 100.0)
    sc_total = (
        v_util + v_cons + v_qs + v_pm + v_ins
        + buckets["util"] + buckets["cons"] + buckets["qs"] + buckets["pm"] + buckets["ins"]
    )

    return {
        "gba": gba, "gfa": gfa, "sgfa": sgfa, "units": rooms,
        "budget": hc_total + sc_total,
        "hc_total": hc_total, "sc_total": sc_total,
        "hc_subtotal": hc_subtotal,
        "v_earth": v_earth + buckets["earth"],
        "v_found": v_found + buckets["found"],
        "v_struc": v_struc + buckets["struc"],
        "v_arch":  v_arch  + buckets["arch"],
        "v_ffe":   v_ffe   + buckets["ffe"],
        "v_mep":   v_mep   + buckets["mep"],
        "v_util":  v_util  + buckets["util"],
        "v_ext":   v_ext   + buckets["ext"],
        "v_fac":   v_fac   + buckets["fac"],
        "v_prelim": v_prelim,
        "v_cont":  v_cont,
        "v_cons":  v_cons  + buckets["cons"],
        "v_qs":    v_qs    + buckets["qs"],
        "v_pm":    v_pm    + buckets["pm"],
        "v_ins":   v_ins   + buckets["ins"],
    }


# ---------------------------------------------------------------------------
# COST ESTIMATOR
# ---------------------------------------------------------------------------
def show_cost_estimator():
    st.title("Cost Calculator")
    st.markdown("---")

    curr_id   = st.session_state.current_proj_id
    curr_proj = st.session_state.projects[curr_id]
    if "data" not in curr_proj:
        st.session_state.projects[curr_id]["data"] = {}

    def get_val(key, default=0.0):
        val = st.session_state.projects[curr_id]["data"].get(key, default)
        if isinstance(val, list):
            return val
        try:
            return float(val)
        except (ValueError, TypeError):
            return val

    # --- PROJECT SETUP ---
    st.subheader("Data Proyek")
    c1, c2, c3, c4, c5 = st.columns(5)
    new_name   = c1.text_input("Nama Proyek", value=curr_proj["name"])
    types_list = ["Hotel", "Retail", "Apartment", "Parking", "Hotel Bintang 3"]
    type_index = types_list.index(curr_proj["type"]) if curr_proj["type"] in types_list else 0
    new_type   = c2.selectbox("Jenis Proyek", types_list, index=type_index)

    if new_type != curr_proj["type"]:
        st.session_state.projects[curr_id]["type"] = new_type
        st.session_state.projects[curr_id]["data"] = {}
        st.rerun()
    if new_name != curr_proj["name"]:
        st.session_state.projects[curr_id]["name"] = new_name
        st.rerun()

    pt_data       = PROJECT_DATABASE[new_type]
    curr_type_key = f"{curr_id}_{new_type}"

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Petunjuk", "1. Hard Cost", "2. Soft Cost",
        "3. Item Tambahan", "4. Hasil", "5. Pembuktian", "6. Penyimpanan",
    ])

    # -----------------------------------------------------------------------
    # TAB 3 — ITEM TAMBAHAN
    # Rendered first so custom bucket values are ready before tab2 & tab3 calc.
    # -----------------------------------------------------------------------
    with tab4:
        st.subheader("Item Tambahan (Smart Custom Costs)")
        category_options = [
            "HC - 1. Preliminaries", "HC - 2. Earthwork", "HC - 3. Foundation",
            "HC - 4. Structural Work", "HC - 5. Architectural Work", "HC - 6. FF&E & Kitchen",
            "HC - 7. MEP Works", "HC - 8. External Works", "HC - 9. Facilities & Misc",
            "HC - 10. Contingencies",
            "SC - 1. QS Services", "SC - 2. PM Services", "SC - 3. Other Consultancy Fee",
            "SC - 4. Insurance Coverage", "SC - 5. Utility Connection",
        ]
        default_smart_cc = [{"Category": "HC - 5. Architectural Work", "Item Description": "", "Rate (Rp)": 0.0, "Quantity": 1.0}]
        current_smart_cc = get_val("smart_custom_costs", default_smart_cc)

        # migrate old format rows
        display_data = []
        for item in current_smart_cc:
            row = item.copy()
            if "Multiplier (Qty)" in row:
                row["Quantity"] = row.pop("Multiplier (Qty)")
            if "Linked Dependency" in row:
                row.pop("Linked Dependency")
            if "Category" not in row:
                row["Category"] = "HC - 5. Architectural Work"
            rate = float(row.get("Rate (Rp)", 0.0) or 0.0)
            qty  = float(row.get("Quantity", 1.0)   or 1.0)
            row["Total (Rp)"] = f"Rp {rate * qty:,.0f}"
            display_data.append(row)

        edited_df = st.data_editor(
            pd.DataFrame(display_data),
            num_rows="dynamic",
            key=f"edit_smart_cc_{curr_id}",
            column_order=["Item Description", "Rate (Rp)", "Quantity", "Category"],
            column_config={
                "Category":    st.column_config.SelectboxColumn("Alokasi Kategori", options=category_options, required=True),
                "Quantity":    st.column_config.NumberColumn("Quantity", min_value=0.0, default=1.0, format="%.2f"),
                "Rate (Rp)":   st.column_config.NumberColumn("Rate (Rp)", format="%.0f"),
            },
            use_container_width=True,
        )

        # save (without display-only Total column)
        save_data = edited_df.drop(columns=["Total (Rp)"], errors="ignore").to_dict("records")
        st.session_state.projects[curr_id]["data"]["smart_custom_costs"] = save_data

        # compute buckets from the editor result (single source of truth for this session)
        cb = compute_custom_buckets(save_data)

        # summary table
        summary_rows = [
            {"Kategori": cat, "Total (Rp)": val}
            for cat, key in [
                ("HC - 1. Preliminaries", "prelim"), ("HC - 2. Earthwork", "earth"),
                ("HC - 3. Foundation", "found"),     ("HC - 4. Structural Work", "struc"),
                ("HC - 5. Architectural Work", "arch"), ("HC - 6. FF&E & Kitchen", "ffe"),
                ("HC - 7. MEP Works", "mep"),         ("HC - 8. External Works", "ext"),
                ("HC - 9. Facilities & Misc", "fac"), ("HC - 10. Contingencies", "cont"),
                ("SC - 1. QS Services", "qs"),        ("SC - 2. PM Services", "pm"),
                ("SC - 3. Other Consultancy Fee", "cons"), ("SC - 4. Insurance Coverage", "ins"),
                ("SC - 5. Utility Connection", "util"),
            ]
            for val in [cb[key]] if cb[key] > 0
        ]
        st.markdown("---")
        if summary_rows:
            st.markdown("#### Rekap Item Tambahan per Kategori")
            df_s = pd.DataFrame(summary_rows)
            df_s["Total (Rp)"] = df_s["Total (Rp)"].apply(lambda x: f"Rp {x:,.0f}")
            st.dataframe(df_s, hide_index=True, use_container_width=True)
        else:
            st.caption("*Belum ada item tambahan yang bernilai.*")
        st.info(f"**Grand Total Item Tambahan: Rp {cb['total']:,.0f}**")

    # -----------------------------------------------------------------------
    # TAB 1 — PETUNJUK
    # -----------------------------------------------------------------------
    with tab1:
        st.header("Daftar Isi")
        c1, c2, c3 = st.columns(3)
        c1.subheader("Hard Cost")
        c1.markdown("""
        * **1.1 Preliminary** * **1.2 Earthworks** * **1.3 Foundation Works**
        * **1.4 Structural** * **1.5 Architectural**
            * *1.5.1 Basic Finish* * *1.5.2 Lobby* * *1.5.3 Facade*
            * *1.5.4 Pintu* * *1.5.5 Sanitary* * *1.5.6 Lantai* * *1.5.7 Lain-lain*
        * **1.6 FF&E** * **1.7 MEP** * **1.8 External** * **1.9 Facility & Misc** * **1.10 Contingencies**
        """)
        c2.subheader("Soft Cost")
        c2.markdown("""
        * **2.1 Consultancy** * **2.2 Insurances** * **2.3 Utilities**
        """)
        c3.subheader("Other Tab")
        c3.markdown("""
        * **3. Item Tambahan** * **4. Hasil** * **5. Pembuktian** * **6. Unggah & Unduh**
        """)

    # -----------------------------------------------------------------------
    # TAB 2 — HARD COST
    # -----------------------------------------------------------------------
    with tab2:
        st.subheader("Hard Cost")
        c1, c2, c3, c4, c5 = st.columns(5)
        land_area = c1.number_input("Luas Tanah (m2)", value=get_val("m_land", 0.0), step=100.0, key=f"m_land_{curr_id}")
        gba       = c2.number_input("GBA (m2)",        value=get_val("m_gba",  0.0), step=100.0, key=f"m_gba_{curr_id}")
        gfa       = c3.number_input("GFA (m2)",        value=get_val("m_gfa",  0.0), step=100.0, key=f"m_gfa_{curr_id}")
        sgfa      = c4.number_input("SGFA (m2)",       value=get_val("m_sgfa", 0.0), step=100.0, key=f"m_sgfa_{curr_id}")
        rooms     = c5.number_input("Ruang (unit)",    value=get_val("m_rooms",0.0), step=1.0,   key=f"m_rooms_{curr_id}")

        hc_sub_tabs = st.tabs([
            "1. Earthworks", "2. Foundation Works", "3. Structural",
            "4. Architectural", "5. FF&E", "6. MEP",
            "7. External", "8. Facility & Misc",
        ])

        with hc_sub_tabs[0]:
            st.subheader("Earthworks")
            struc_earth = st.number_input("Earthworks (Rp/m2)", value=get_val("u_earth", pt_data["struc_earth"]), key=f"u_earth_{curr_type_key}")
            st.caption(f"GBA: {gba:,.0f} m2  |  Rate: Rp {struc_earth:,.0f}  |  Total: Rp {struc_earth*gba:,.0f}  |  {n2w(struc_earth*gba)}")

        with hc_sub_tabs[1]:
            st.subheader("Foundation")
            struc_found = st.number_input("Foundation Rate (Rp/m2)", value=get_val("u_found", pt_data["struc_found"]), key=f"u_found_{curr_type_key}")
            st.caption(f"GBA: {gba:,.0f} m2  |  Rate: Rp {struc_found:,.0f}  |  Total: Rp {struc_found*gba:,.0f}  |  {n2w(struc_found*gba)}")

        with hc_sub_tabs[2]:
            st.subheader("Structural")
            struc_work = st.number_input("Structural Work Rate (Rp/m2)", value=get_val("u_struc", pt_data["struc_work"]), key=f"u_struc_{curr_type_key}")
            st.caption(f"GBA: {gba:,.0f} m2  |  Rate: Rp {struc_work:,.0f}  |  Total: Rp {struc_work*gba:,.0f}  |  {n2w(struc_work*gba)}")

        with hc_sub_tabs[3]:
            arch_sub_tabs = st.tabs(["1. Basic Finish", "2. Lobby", "3. Facade", "4. Pintu", "5. Sanitary", "6. Lantai", "7. Lain-lain"])

            with arch_sub_tabs[0]:
                st.subheader("Architecture Base")
                arch_base = st.number_input("Architecture Base (Rp/m2)", value=get_val("u_arch", pt_data["arch_base"]), key=f"u_arch_{curr_type_key}")
                st.caption(f"GFA: {gfa:,.0f} m2  |  Total: Rp {arch_base*gfa:,.0f}  |  {n2w(arch_base*gfa)}")

            with arch_sub_tabs[1]:
                st.subheader("Lobby Interior")
                lobby_interior = st.number_input("Lobby Interior (m2)", value=float(get_val("m_lobby", 0.0)), step=10.0, key=f"m_lobby_{curr_id}")
                lobby_rate     = st.number_input("Lobby Rate (Rp/m2)",  value=get_val("u_lobby", pt_data["lobby"]),  key=f"u_lobby_{curr_type_key}")
                st.caption(f"Total: Rp {lobby_rate*lobby_interior:,.0f}  |  {n2w(lobby_rate*lobby_interior)}")

            with arch_sub_tabs[2]:
                st.subheader("Facade")
                facade = st.number_input("Facade (m2)", value=get_val("m_facade", 0.0), step=100.0, key=f"m_facade_{curr_id}")
                c3f, c4f, c5f = st.columns(3)
                fac_precast_rate   = c3f.number_input("Precast Rate (Rp)",     value=get_val("u_f_pre",  pt_data["facade_precast_rate"]),  key=f"u_f_pre_{curr_type_key}")
                fac_window_rate    = c4f.number_input("Window Wall Rate (Rp)", value=get_val("u_f_win",  pt_data["facade_window_rate"]),   key=f"u_f_win_{curr_type_key}")
                fac_double_rate    = c5f.number_input("Double Skin Rate (Rp)", value=get_val("u_f_doub", pt_data["facade_double_rate"]),   key=f"u_f_doub_{curr_type_key}")
                facade_precast_pct = c3f.number_input("Precast (%)",           value=get_val("r_fac_pre", pt_data["facade_precast_pct"]), step=5.0, key=f"r_fac_pre_{curr_type_key}")
                facade_window_pct  = c4f.number_input("Window Wall (%)",       value=get_val("r_fac_win", pt_data["facade_window_pct"]),  step=5.0, key=f"r_fac_win_{curr_type_key}")
                facade_double_pct  = c5f.number_input("Double Skin (%)",       value=get_val("r_fac_doub",pt_data["facade_double_pct"]), step=5.0, key=f"r_fac_doub_{curr_type_key}")
                t_fac_pct = facade_precast_pct + facade_window_pct + facade_double_pct
                c3f.caption(f"Total Precast: Rp {fac_precast_rate*facade*(facade_precast_pct/100):,.0f}")
                c4f.caption(f"Total Window: Rp {fac_window_rate*facade*(facade_window_pct/100):,.0f}")
                c5f.caption(f"Total Double: Rp {fac_double_rate*facade*(facade_double_pct/100):,.0f}")
                if t_fac_pct != 100:
                    st.warning(f"⚠️ Total facade is **{t_fac_pct}%** (bukan 100%)")

            with arch_sub_tabs[3]:
                st.subheader("Pintu")
                c1p, c2p, c3p = st.columns(3)
                wooden_door = c1p.number_input("Wooden Door (unit)", value=get_val("m_door_w", 0.0), step=10.0, key=f"m_door_w_{curr_id}")
                steel_door  = c2p.number_input("Steel Door (unit)",  value=get_val("m_door_s", 0.0), step=10.0, key=f"m_door_s_{curr_id}")
                glass_door  = c3p.number_input("Glass Door (unit)",  value=get_val("m_door_g", 0.0), step=1.0,  key=f"m_door_g_{curr_id}")
                door_wood   = c1p.number_input("Wooden Door Rate (Rp)", value=get_val("u_d_wood",  pt_data["door_wood"]),  key=f"u_d_wood_{curr_type_key}")
                door_steel  = c2p.number_input("Steel Door Rate (Rp)",  value=get_val("u_d_steel", pt_data["door_steel"]), key=f"u_d_steel_{curr_type_key}")
                door_glass  = c3p.number_input("Glass Door Rate (Rp)",  value=get_val("u_d_glass", pt_data["door_glass"]), key=f"u_d_glass_{curr_type_key}")
                hw_wood     = c1p.number_input("Hardware Kayu (Rp)",    value=get_val("u_hw_wood", pt_data["hw_wood"]),    key=f"u_hw_wood_{curr_type_key}")
                hw_steel    = c2p.number_input("Hardware Besi (Rp)",    value=get_val("u_hw_steel",pt_data["hw_steel"]),   key=f"u_hw_steel_{curr_type_key}")
                c1p.caption(f"Total Kayu: Rp {wooden_door*(door_wood+hw_wood):,.0f}")
                c2p.caption(f"Total Besi: Rp {steel_door*(door_steel+hw_steel):,.0f}")
                c3p.caption(f"Total Kaca: Rp {glass_door*door_glass:,.0f}")

            with arch_sub_tabs[4]:
                st.subheader("Sanitary")
                c1s, c2s = st.columns(2)
                with c1s:
                    san_qty_room  = st.number_input("Toilet Private (unit/ruang)", value=get_val("r_san_qty", pt_data["san_room_qty"]), key=f"r_san_qty_{curr_type_key}")
                    san_room_rate = st.number_input("Unit Sanitary Rate (Rp)",     value=get_val("u_s_room",  pt_data["san_room_rate"]),key=f"u_s_room_{curr_type_key}")
                    st.caption(f"Total Private: Rp {rooms*san_qty_room*san_room_rate:,.0f}")
                    disabled_toil = st.number_input("Toilet Difabel (units)", value=get_val("m_toil_d", 0.0), step=1.0, key=f"m_toil_d_{curr_id}")
                    san_dis       = st.number_input("Disabled Rate (Rp)",     value=get_val("u_s_dis",  pt_data["san_dis"]),     key=f"u_s_dis_{curr_type_key}")
                    st.caption(f"Total Difabel: Rp {disabled_toil*san_dis:,.0f}")
                    mushola_unit  = st.number_input("Mushola (units)", value=get_val("m_mushola", 0.0), step=1.0, key=f"m_mushola_{curr_id}")
                    san_mushola   = st.number_input("Mushola Rate (Rp)", value=get_val("u_s_mushola", pt_data["san_mushola"]), key=f"u_s_mushola_{curr_type_key}")
                    st.caption(f"Total Mushola: Rp {mushola_unit*san_mushola:,.0f}")
                with c2s:
                    toilet_male   = st.number_input("Toilet Pria (units)",  value=get_val("m_toil_m", 0.0), step=1.0, key=f"m_toil_m_{curr_id}")
                    san_pub_m     = st.number_input("Public Male Rate (Rp)", value=get_val("u_s_pub_m", pt_data["san_pub_m"]), key=f"u_s_pub_m_{curr_type_key}")
                    st.caption(f"Total Pria: Rp {toilet_male*san_pub_m:,.0f}")
                    toilet_female = st.number_input("Toilet Wanita (units)", value=get_val("m_toil_f", 0.0), step=1.0, key=f"m_toil_f_{curr_id}")
                    san_pub_f     = st.number_input("Public Female Rate (Rp)", value=get_val("u_s_pub_f", pt_data["san_pub_f"]), key=f"u_s_pub_f_{curr_type_key}")
                    st.caption(f"Total Wanita: Rp {toilet_female*san_pub_f:,.0f}")

            with arch_sub_tabs[5]:
                st.subheader("Lantai")
                c1l, c2l, c3l = st.columns(3)
                f_mult = 1.32
                with c1l:
                    ht_idx = 0 if get_val("ht_spec_type", "Type1") == "Type1" else 1
                    st.radio("Spek HT", ["Type1", "Type2"], index=ht_idx, key=f"temp_spec_ht_{curr_type_key}", horizontal=True, on_change=update_price, args=("ht", "fl_ht_rate"))
                    fl_ht_pct  = st.number_input("HT (%)",       value=get_val("r_fl_ht", pt_data["fl_ht_pct"]),  step=5.0, max_value=100.0, key=f"r_fl_ht_{curr_type_key}")
                    fl_ht_rate = st.number_input("HT Rate (Rp)", value=get_val("u_fl_ht", pt_data["fl_ht_rate"]["Type1"]), key=f"u_fl_ht_{curr_type_key}")
                    st.caption(f"Total HT: Rp {gfa*(fl_ht_pct/100)*fl_ht_rate*f_mult:,.0f}  |  {n2w(gfa*(fl_ht_pct/100)*fl_ht_rate*f_mult)}")
                with c2l:
                    vin_idx = 0 if get_val("vin_spec_type", "Type1") == "Type1" else 1
                    st.radio("Spek Vinyl", ["Type1", "Type2"], index=vin_idx, key=f"temp_spec_vin_{curr_type_key}", horizontal=True, on_change=update_price, args=("vin", "fl_vinyl_rate"))
                    fl_vinyl_pct  = st.number_input("Vinyl (%)",       value=get_val("r_fl_vin", pt_data["fl_vinyl_pct"]),  step=5.0, max_value=100.0, key=f"r_fl_vin_{curr_type_key}")
                    fl_vinyl_rate = st.number_input("Vinyl Rate (Rp)", value=get_val("u_fl_vin", pt_data["fl_vinyl_rate"]["Type1"]), key=f"u_fl_vin_{curr_type_key}")
                    st.caption(f"Total Vinyl: Rp {gfa*(fl_vinyl_pct/100)*fl_vinyl_rate*f_mult:,.0f}  |  {n2w(gfa*(fl_vinyl_pct/100)*fl_vinyl_rate*f_mult)}")
                with c3l:
                    mar_idx = 0 if get_val("mar_spec_type", "Type1") == "Type1" else 1
                    st.radio("Spek Marmer", ["Type1", "Type2"], index=mar_idx, key=f"temp_spec_mar_{curr_type_key}", horizontal=True, on_change=update_price, args=("mar", "fl_marmer_rate"))
                    fl_marmer_pct  = st.number_input("Marmer (%)",       value=get_val("r_fl_mar", pt_data["fl_marmer_pct"]),  step=5.0, max_value=100.0, key=f"r_fl_mar_{curr_type_key}")
                    fl_marmer_rate = st.number_input("Marmer Rate (Rp)", value=get_val("u_fl_mar", pt_data["fl_marmer_rate"]["Type1"]), key=f"u_fl_mar_{curr_type_key}")
                    st.caption(f"Total Marmer: Rp {gfa*(fl_marmer_pct/100)*fl_marmer_rate*f_mult:,.0f}  |  {n2w(gfa*(fl_marmer_pct/100)*fl_marmer_rate*f_mult)}")
                t_fl_pct = fl_ht_pct + fl_vinyl_pct + fl_marmer_pct
                if t_fl_pct != 100:
                    st.warning(f"⚠️ Total lantai adalah **{t_fl_pct}%** (bukan 100%)")

            with arch_sub_tabs[6]:
                st.subheader("Lain-lain")
                c1m, c2m, c3m = st.columns(3)
                carpet_m2    = c1m.number_input("Karpet (m2)",     value=get_val("m_carpet",  0.0), step=10.0, key=f"m_carpet_{curr_id}")
                carpet_rate  = c1m.number_input("Carpet Rate (Rp)",value=get_val("u_carpet",  pt_data["carpet"]),  key=f"u_carpet_{curr_type_key}")
                c1m.caption(f"Total: Rp {carpet_m2*carpet_rate:,.0f}")
                glass_m2     = c2m.number_input("Kaca (m2)",       value=get_val("m_glass",   0.0), step=10.0, key=f"m_glass_{curr_id}")
                glass_rate   = c2m.number_input("Glass Rate (Rp)", value=get_val("u_glass",   pt_data["glass"]),   key=f"u_glass_{curr_type_key}")
                c2m.caption(f"Total: Rp {glass_m2*glass_rate:,.0f}")
                skylight_area = c3m.number_input("Skylight (m2)",      value=get_val("m_skylight",0.0), step=10.0, key=f"m_skylight_{curr_id}")
                skylight_rate = c3m.number_input("Skylight Rate (Rp)", value=get_val("u_sky",  pt_data["skylight_rate"]), key=f"u_sky_{curr_type_key}")
                c3m.caption(f"Total: Rp {skylight_area*skylight_rate:,.0f}")
                gondola_unit = c1m.number_input("Gondola (unit)",      value=get_val("m_gondola",0.0), step=1.0, key=f"m_gondola_{curr_id}")
                gondola_rate = c1m.number_input("Gondola Rate (Rp)",   value=get_val("u_gondola",pt_data["gondola"]),  key=f"u_gondola_{curr_type_key}")
                c1m.caption(f"Total: Rp {gondola_unit*gondola_rate:,.0f}")
                railing_qty  = c2m.number_input("Railing (m'/room)",  value=get_val("r_rail_qty",pt_data["railing_qty"]), step=1.0, key=f"r_rail_qty_{curr_type_key}")
                railing_rate = c2m.number_input("Railing Rate (Rp)",  value=get_val("u_rail",  pt_data["railing_rate"]),  key=f"u_rail_{curr_type_key}")
                c2m.caption(f"Total: Rp {rooms*railing_qty*railing_rate:,.0f}")

        with hc_sub_tabs[4]:
            st.subheader("FF&E")
            c1f, c2f, c3f = st.columns(3)
            with c1f.expander("FF&E", expanded=True):
                ffe_rate = st.number_input("FF&E (Rp/room)", value=get_val("u_ffe", pt_data["ffe"]), key=f"u_ffe_{curr_type_key}")
                st.caption(f"{rooms:,.0f} Rooms x Rp {ffe_rate:,.0f} = Rp {rooms*ffe_rate:,.0f}")
            with c2f.expander("Dapur", expanded=True):
                kitchen_rate = st.number_input("Kitchen (Rp/room)", value=get_val("u_kit", pt_data["kitchen"]), key=f"u_kit_{curr_type_key}")
                st.caption(f"Total: Rp {kitchen_rate:,.0f}")
            with c3f.expander("Gym/Linen", expanded=True):
                m_status   = st.radio("Ada Gym/Linen?", ["Tidak", "Ada"], index=1 if get_val("misc_switch", 0) == 1 else 0, key=f"misc_sw_{curr_id}", horizontal=True)
                misc_switch = 1 if m_status == "Ada" else 0
                st.session_state.projects[curr_id]["data"]["misc_switch"] = misc_switch
                misc_rate   = st.number_input("Misc Rate (Rp)", value=get_val("u_misc", pt_data["misc"]), key=f"u_misc_{curr_type_key}")
                st.caption(f"Total: Rp {misc_rate*misc_switch:,.0f}")

        with hc_sub_tabs[5]:
            st.subheader("MEP")
            c1mep, _, _ = st.columns(3)
            mep_rate = c1mep.number_input("MEP Rate (Rp/m2)", value=get_val("u_mep", pt_data["mep"]), key=f"u_mep_{curr_type_key}")
            c1mep.caption(f"GBA: {gba:,.0f} m2  |  Total: Rp {gba*mep_rate:,.0f}  |  {n2w(gba*mep_rate)}")

        with hc_sub_tabs[6]:
            st.subheader("External")
            c1ex, _, _ = st.columns(3)
            land_m2      = c1ex.number_input("Area Lanskap (m2)",     value=get_val("m_land_m2", 0.0), step=100.0, key=f"m_land_m2_{curr_id}")
            ext_land_rate = c1ex.number_input("External Works (Rp/m2)", value=get_val("u_ext", pt_data["ext_land"]), key=f"u_ext_{curr_type_key}")
            c1ex.caption(f"Total: Rp {land_m2*ext_land_rate:,.0f}  |  {n2w(land_m2*ext_land_rate)}")

        with hc_sub_tabs[7]:
            st.subheader("Facilities & Misc")
            c1fc, c2fc, c3fc = st.columns(3)
            pub_fac_m2  = c1fc.number_input("Fasilitas Publik (m2)",   value=get_val("m_fac_pub",  0.0), step=10.0, key=f"m_fac_pub_{curr_id}")
            res_fac_m2  = c2fc.number_input("Fasilitas Penghuni (m2)", value=get_val("m_fac_res",  0.0), step=10.0, key=f"m_fac_res_{curr_id}")
            proj_fac_u  = c3fc.number_input("Fasilitas Proyek (unit)", value=get_val("m_fac_proj", 0.0), step=1.0, max_value=100.0, key=f"m_fac_proj_{curr_id}")
            fac_pub_rate = c1fc.number_input("Publik Rate (Rp/m2)",   value=get_val("u_fac_p",  pt_data["fac_pub"]),  key=f"u_fac_p_{curr_type_key}")
            fac_res_rate = c2fc.number_input("Penghuni Rate (Rp/m2)", value=get_val("u_fac_r",  pt_data["fac_res"]),  key=f"u_fac_r_{curr_type_key}")
            fac_proj_rate = c3fc.number_input("Proyek Rate (Rp/unit)",value=get_val("u_fac_pr", pt_data["fac_proj"]), key=f"u_fac_pr_{curr_type_key}")
            c1fc.caption(f"Total: Rp {pub_fac_m2*fac_pub_rate:,.0f}")
            c2fc.caption(f"Total: Rp {res_fac_m2*fac_res_rate:,.0f}")
            c3fc.caption(f"Total: Rp {proj_fac_u*fac_proj_rate:,.0f}")

        # -------------------------------------------------------------------
        # MASTER CALCULATION — single, authoritative, uses cb (custom buckets)
        # -------------------------------------------------------------------
        f_mult = 1.32
        t_earth      = gba * struc_earth
        t_found      = gba * struc_found
        t_struc      = gba * struc_work
        t_arch_base  = gfa * arch_base #arch
        t_precast    = facade * (facade_precast_pct / 100) * fac_precast_rate #arch
        t_window     = facade * (facade_window_pct  / 100) * fac_window_rate #arch
        t_double     = facade * (facade_double_pct  / 100) * fac_double_rate #arch
        t_w_door     = wooden_door * door_wood #arch
        t_g_door     = glass_door  * door_glass #arch
        t_s_door     = steel_door  * door_steel #arch
        t_lobby      = lobby_interior * lobby_rate #arch
        t_gondola    = gondola_unit   * gondola_rate #arch
        t_unit_san   = rooms * san_qty_room * san_room_rate #arch
        t_t_male     = toilet_male    * san_pub_m #arch
        t_t_female   = toilet_female  * san_pub_f #arch
        t_t_dis      = disabled_toil  * san_dis #arch
        t_mushola    = mushola_unit   * san_mushola #arch
        t_hw_w       = wooden_door    * hw_wood #arch
        t_hw_s       = steel_door     * hw_steel #arch
        t_ht         = gfa * (fl_ht_pct    / 100) * fl_ht_rate    * f_mult #arch
        t_vinyl      = gfa * (fl_vinyl_pct  / 100) * fl_vinyl_rate  * f_mult #arch
        t_marmer     = gfa * (fl_marmer_pct / 100) * fl_marmer_rate * f_mult #arch
        t_carpet     = carpet_m2    * carpet_rate #arch
        t_glass_work = glass_m2     * glass_rate #arch
        t_railing    = rooms * railing_qty  * railing_rate #arch
        t_skylight   = skylight_area * skylight_rate #arch
        t_ffe        = rooms * ffe_rate
        t_kitchen    = rooms * kitchen_rate
        t_misc       = misc_rate * misc_switch
        t_mep        = gba * mep_rate
        t_external   = land_m2  * ext_land_rate
        t_pub_fac    = pub_fac_m2  * fac_pub_rate
        t_res_fac    = res_fac_m2  * fac_res_rate
        t_proj_fac   = proj_fac_u  * fac_proj_rate

        # Base arch subtotal (for display in tables)
        total_arch = sum([
            t_arch_base, t_precast, t_window, t_double,
            t_w_door, t_g_door, t_s_door, t_lobby, t_gondola,
            t_unit_san, t_t_male, t_t_female, t_t_dis, t_mushola,
            t_hw_w, t_hw_s, t_ht, t_vinyl, t_marmer,
            t_carpet, t_glass_work, t_railing, t_skylight,
        ])

        # HC subtotal: base items + each custom HC bucket
        hc_subtotal = (
            t_earth + t_found + t_struc
            + total_arch
            + t_ffe + t_kitchen + t_misc
            + t_mep + t_external
            + t_pub_fac + t_res_fac + t_proj_fac
            + cb["earth"] + cb["found"] + cb["struc"] + cb["arch"]
            + cb["ffe"]   + cb["mep"]   + cb["ext"]   + cb["fac"]
            + cb["cont"]
        )

        t_preliminary = hc_subtotal * 0.05 + cb["prelim"]
        t_contingency = (hc_subtotal + t_preliminary) * 0.03
        hc_total      = hc_subtotal + t_preliminary + t_contingency

        with st.expander("Rekap Hard Cost"):
            st.subheader("Rekap Hard Cost")
            st.dataframe(pd.DataFrame({
                "Project Name":    [curr_proj["name"]],
                "1. Prelim":       [n2w(t_preliminary)],
                "2. Earthwork":    [n2w(t_earth + cb["earth"])],
                "3. Foundation":   [n2w(t_found + cb["found"])],
                "4. Structural":   [n2w(t_struc + cb["struc"])],
                "5. Arch":         [n2w(total_arch + cb["arch"])],
                "6. FF&E":         [n2w(t_ffe + t_kitchen + t_misc + cb["ffe"])],
                "7. MEP":          [n2w(t_mep + cb["mep"])],
                "8. External":     [n2w(t_external + cb["ext"])],
                "9. Facil.":       [n2w(t_pub_fac + t_res_fac + t_proj_fac + cb["fac"])],
                "10. Cont.":       [n2w(t_contingency + cb["cont"])],
                "TOTAL HARD COST": [n2w(hc_total)],
            }), use_container_width=True, hide_index=True)

    # -----------------------------------------------------------------------
    # TAB 3 — SOFT COST
    # -----------------------------------------------------------------------
    with tab3:
        st.subheader("Soft Cost")
        sc_sub_tabs = st.tabs(["1. Consultancy Services", "2. Insurances", "3. Utilities Connection"])

        with sc_sub_tabs[0]:
            sc_col1, sc_col2, sc_col3 = st.columns(3)
            with sc_col1.expander("QS", expanded=True):
                qs_months = st.number_input("Durasi QS (Bulan)", value=get_val("sc_qs_m", 0.0), step=1.0,        key=f"sc_qs_m_{curr_id}")
                qs_rate   = st.number_input("Harga QS (Rp/Mo)", value=get_val("sc_qs_r", 0.0), step=1000000.0,   key=f"sc_qs_r_{curr_id}")
                st.caption(f"Total: Rp {qs_months*qs_rate:,.0f}  |  {n2w(qs_months*qs_rate)}")
            with sc_col2.expander("PM", expanded=True):
                pm_months = st.number_input("Durasi PM (Bulan)", value=get_val("sc_pm_m", 0.0), step=1.0,        key=f"sc_pm_m_{curr_id}")
                pm_rate   = st.number_input("Harga PM (Rp/Mo)", value=get_val("sc_pm_r", 0.0), step=1000000.0,   key=f"sc_pm_r_{curr_id}")
                st.caption(f"Total: Rp {pm_months*pm_rate:,.0f}  |  {n2w(pm_months*pm_rate)}")
            with sc_col3.expander("Other Consultancy", expanded=True):
                consultancy_rate = st.number_input("Konsultan (Rp/m2 GFA)", value=get_val("sc_cons", pt_data["cons"]), key=f"sc_cons_{curr_type_key}")
                st.caption(f"GFA: {gfa:,.0f} m2  |  Total: Rp {gfa*consultancy_rate:,.0f}  |  {n2w(gfa*consultancy_rate)}")

        with sc_sub_tabs[1]:
            insurance_pct = st.number_input("Insurance (%)", value=get_val("sc_ins", 0.12), step=0.01, key=f"sc_ins_{curr_id}")
            t_ins_calc    = hc_subtotal * (insurance_pct / 100.0)
            st.caption(f"HC Subtotal: Rp {hc_subtotal:,.0f} x {insurance_pct}%  |  Total: Rp {t_ins_calc:,.0f}  |  {n2w(t_ins_calc)}")

        with sc_sub_tabs[2]:
            utility_rate = st.number_input("Utility Connection (Rp/m2)", value=get_val("u_util", pt_data["utility"]), key=f"u_util_{curr_type_key}")
            t_util_calc  = gba * utility_rate
            st.caption(f"GBA: {gba:,.0f} m2  |  Total: Rp {t_util_calc:,.0f}  |  {n2w(t_util_calc)}")

        # SC totals — custom SC buckets added here
        t_qs          = qs_months * qs_rate          + cb["qs"]
        t_pm          = pm_months * pm_rate          + cb["pm"]
        t_consultancy = gfa * consultancy_rate       + cb["cons"]
        t_insurance   = hc_subtotal * (insurance_pct / 100.0) + cb["ins"]
        t_utility     = gba * utility_rate           + cb["util"]
        sc_total      = t_qs + t_pm + t_consultancy + t_insurance + t_utility
        grand_total_project = hc_total + sc_total

        with st.expander("Rekap Soft Cost"):
            st.subheader("Rekap Soft Cost")
            st.dataframe(pd.DataFrame({
                "Project Name":    [curr_proj["name"]],
                "1. QS Fee":       [f"{t_qs:,.0f}"],
                "2. PM Fee":       [f"{t_pm:,.0f}"],
                "3. Other Cons.":  [f"{t_consultancy:,.0f}"],
                "4. Insurance":    [f"{t_insurance:,.0f}"],
                "5. Utility":      [f"{t_utility:,.0f}"],
                "TOTAL SOFT COST": [f"{sc_total:,.0f}"],
            }), use_container_width=True, hide_index=True)

    # -----------------------------------------------------------------------
    # SAVE ALL METRICS TO SESSION STATE
    # -----------------------------------------------------------------------
    current_metrics = {
        "proj_name": new_name, "proj_type": new_type,
        "misc_switch": misc_switch,
        "ht_spec_type":  get_val("ht_spec_type",  "Type1"),
        "vin_spec_type": get_val("vin_spec_type",  "Type1"),
        "mar_spec_type": get_val("mar_spec_type",  "Type1"),
        "m_land": land_area, "m_gba": gba, "m_gfa": gfa, "m_sgfa": sgfa,
        "m_facade": facade, "m_rooms": rooms, "m_lobby": lobby_interior,
        "m_gondola": gondola_unit, "m_carpet": carpet_m2, "m_glass": glass_m2,
        "m_skylight": skylight_area, "m_door_g": glass_door, "m_door_w": wooden_door,
        "m_door_s": steel_door, "m_toil_m": toilet_male, "m_toil_f": toilet_female,
        "m_toil_d": disabled_toil, "m_mushola": mushola_unit,
        "m_fac_res": res_fac_m2, "m_fac_pub": pub_fac_m2, "m_fac_proj": proj_fac_u,
        "m_land_m2": land_m2,
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
        "u_ext": ext_land_rate, "u_fac_p": fac_pub_rate, "u_fac_r": fac_res_rate, "u_fac_pr": fac_proj_rate,
        "sc_cons": consultancy_rate, "sc_qs_m": qs_months, "sc_qs_r": qs_rate,
        "sc_pm_m": pm_months, "sc_pm_r": pm_rate, "sc_ins": insurance_pct,
    }
    # preserve keys managed by other sections
    for k in ("smart_custom_costs", "header_info", "assumptions"):
        if k in st.session_state.projects[curr_id]["data"]:
            current_metrics[k] = st.session_state.projects[curr_id]["data"][k]
    st.session_state.projects[curr_id]["data"] = current_metrics

    # -----------------------------------------------------------------------
    # RESULT TABS (use get_project_totals for consistency with FAD/Rekap)
    # -----------------------------------------------------------------------
    m = get_project_totals(st.session_state.projects[curr_id])
    hc_total_r          = m["hc_total"]
    sc_total_r          = m["sc_total"]
    grand_total_r       = m["budget"]
    hc_subtotal_r       = m["hc_subtotal"]

    import io, xlsxwriter, re
    from datetime import date

    with tab5:
        st.subheader("Hasil")
        sum_sub_tabs = st.tabs(["1. Total", "2. Tabel", "3. Chart", "4. FAD", "5. Rekap"])

        # --- SUB TAB 1: TOTAL ---
        with sum_sub_tabs[0]:
            st.subheader("Total")
            c1t, c2t = st.columns(2)
            c1t.markdown(f"""
                <div style="margin-bottom:20px;">
                    <div style="font-size:16px;color:gray;">Total Hard Cost</div>
                    <div style="font-size:28px;font-weight:bold;">Rp {hc_total_r:,.2f}</div>
                    <div style="font-size:14px;color:gray;">{n2w(hc_total_r)} Rupiah</div>
                </div>
            """, unsafe_allow_html=True)
            c2t.markdown(f"""
                <div style="margin-bottom:20px;">
                    <div style="font-size:16px;color:gray;">Total Soft Cost</div>
                    <div style="font-size:28px;font-weight:bold;">Rp {sc_total_r:,.2f}</div>
                    <div style="font-size:14px;color:gray;">{n2w(sc_total_r)} Rupiah</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div style="margin-bottom:30px;padding:15px;border-radius:8px;border:1px solid #4B4C55;">
                    <div style="font-size:18px;">Grand Total Project Cost</div>
                    <div style="font-size:38px;font-weight:bold;">Rp {grand_total_r:,.2f}</div>
                    <div style="font-size:16px;">{n2w(grand_total_r)} Rupiah</div>
                </div>
            """, unsafe_allow_html=True)

        # --- SUB TAB 2: TABEL ---
        with sum_sub_tabs[1]:
            st.subheader("Tabel Rincian")
            st.markdown("#### Hard Cost Breakdown")

            hc_raw = [
                m["v_prelim"],
                t_earth + cb["earth"], t_found + cb["found"], t_struc + cb["struc"],
                t_arch_base, t_precast, t_window, t_double,
                t_w_door, t_g_door, t_s_door, t_lobby, t_gondola,
                t_unit_san, t_t_male, t_t_female, t_t_dis, t_mushola,
                t_kitchen, t_hw_w, t_hw_s, t_ht, t_vinyl, t_marmer,
                t_carpet, t_glass_work,
                t_ffe + cb["ffe"], t_misc,
                t_mep + cb["mep"],
                t_railing, t_skylight,
                t_external + cb["ext"],
                t_pub_fac + t_res_fac + t_proj_fac + cb["fac"],
                cb["total"],   # custom items line
                m["v_cont"],
            ]
            hc_desc = [
                "Preliminary Works",
                "Earthwork", "Foundation", "Structural Work",
                "Basic Architecture", "Facade - Precast", "Facade - Window Wall", "Facade - Double Skin",
                "Wooden Doors", "Glass Doors", "Steel Doors", "Lobby Interior", "Gondola",
                "Typical Unit Sanitary", "Public Toilet Male", "Public Toilet Female", "Disabled Toilet", "Mushola",
                "Kitchen Equipment", "Hardware Pintu Kayu", "Hardware Pintu Besi",
                "HT/Ceramic Tile", "Vinyl Flooring", "Marmer Flooring", "Carpet Work", "Glass Work",
                "FF&E", "Misc. (Linen/Gym)", "MEP Works",
                "Railing Work", "Skylight Work", "External Works",
                "Facilities & Misc", "Smart Custom Costs (all categories)", "Contingencies",
            ]
            st.dataframe(pd.DataFrame({
                "No": list(range(1, len(hc_desc)+1)),
                "Description": hc_desc,
                "Amount (Rp)": [f"Rp {v:,.0f}" for v in hc_raw],
            }), use_container_width=True, hide_index=True)
            st.success(f"**Total Hard Cost: Rp {hc_total_r:,.0f}**")
            st.divider()

            st.markdown("#### Soft Cost Breakdown")
            sc_raw  = [t_consultancy, t_qs, t_pm, t_insurance, t_utility]
            sc_desc = ["Other Consultancy Fee", "QS Services", "PM Services", "Insurance Coverage", "Utility Connection"]
            st.dataframe(pd.DataFrame({
                "No": list(range(1, len(sc_desc)+1)),
                "Description": sc_desc,
                "Amount (Rp)": [f"Rp {v:,.0f}" for v in sc_raw],
            }), use_container_width=True, hide_index=True)
            st.warning(f"**Total Soft Cost: Rp {sc_total_r:,.0f}**")

        # --- SUB TAB 3: CHART ---
        with sum_sub_tabs[2]:
            st.subheader("Chart")
            all_items = [(d, a, "Hard Cost") for d, a in zip(hc_desc, hc_raw)] + \
                        [(d, a, "Soft Cost") for d, a in zip(sc_desc, sc_raw)]
            df_chart = pd.DataFrame(all_items, columns=["Item", "Amount", "Type"])
            df_chart = df_chart[df_chart["Amount"] > 0]
            chart_height = max(400, len(df_chart) * 25)
            chart = alt.Chart(df_chart).mark_bar().encode(
                x=alt.X("Amount:Q", title="Cost (Rp)"),
                y=alt.Y("Item:N", sort="-x", title=""),
                color=alt.Color("Type:N", scale=alt.Scale(domain=["Hard Cost", "Soft Cost"], range=["#1f77b4", "#ff7f0e"])),
                tooltip=["Item", "Type", alt.Tooltip("Amount:Q", format=",.2f")],
            ).properties(height=chart_height)
            st.altair_chart(chart, use_container_width=True)

        # --- SUB TAB 4: FAD ---
        with sum_sub_tabs[3]:
            st.subheader("FAD")
            active_id = st.session_state.current_proj_id
            today_str = date.today().strftime("%d-%m-%Y")
            if "header_info" not in st.session_state.projects[active_id]["data"]:
                st.session_state.projects[active_id]["data"]["header_info"] = {"rev_no": "0", "updated": today_str, "created": today_str}
            with st.expander("Edit Header & Assumptions", expanded=False):
                h_col1, h_col2, h_col3 = st.columns(3)
                rev_input = h_col1.text_input("Revision Number:", value=st.session_state.projects[active_id]["data"]["header_info"]["rev_no"], key=f"rev_{active_id}")
                upd_input = h_col2.text_input("Updated Date:",    value=st.session_state.projects[active_id]["data"]["header_info"]["updated"],  key=f"upd_{active_id}")
                cre_input = h_col3.text_input("Created Date:",    value=st.session_state.projects[active_id]["data"]["header_info"]["created"],  key=f"cre_{active_id}")
                st.session_state.projects[active_id]["data"]["header_info"] = {"rev_no": rev_input, "updated": upd_input, "created": cre_input}
                st.divider()
                current_assums = st.session_state.projects[active_id]["data"].get("assumptions", [
                    "Foundation System Standard Pilecaps.", "No Basement.",
                    "Parking Provision Limited To On Street Level Parking",
                    "Floor To Floor Height At 3.3M", "Facade Alumunium Window Wall - No Double Skin",
                    "External Façade Precast, No Double Skin For Parking Podium If Any.",
                    "Ground Lobby Finishes Completed With Artificial Stone & HT.",
                    "Typical Corridor | Floor Finishes : HT | Wall Finishes : Cement Sand Plaster C/W Emulsion Paint.",
                    "Aircon System | Apartement : AC Split", "SBO Rebars @ Rp. 10.000/Kg",
                    "Excluded Smarthome", "Lift : 2 Passenger Lift + 1 Services Lift / TOWER",
                    "Exclude Wardrobe", "FFE : Kitchen Cabinet, Hob & Hood, Refrigerator & Washing Machine",
                    "Water Heater : Installation Only",
                    "Calculation Area Refer To DP's Calculation Dated 12.03.2026",
                ])
                ed_assum = st.data_editor(pd.DataFrame(current_assums, columns=["Note"]), num_rows="dynamic", use_container_width=True, key=f"ed_sum_{active_id}")
                new_list = ed_assum["Note"].dropna().tolist()
                if new_list != current_assums:
                    st.session_state.projects[active_id]["data"]["assumptions"] = new_list

            st.subheader("Manual Additional Projects")
            if "manual_fad_projects" not in st.session_state:
                st.session_state.manual_fad_projects = pd.DataFrame(columns=["Project Name", "GBA", "GFA", "SGFA", "Units", "Budget Estimate (Rp)"])
            edited_manual_df = st.data_editor(
                st.session_state.manual_fad_projects, num_rows="dynamic", use_container_width=True,
                key="manual_fad_editor",
                column_config={
                    "GBA":   st.column_config.NumberColumn("GBA",  min_value=0, format="%.0f"),
                    "GFA":   st.column_config.NumberColumn("GFA",  min_value=0, format="%.0f"),
                    "SGFA":  st.column_config.NumberColumn("SGFA", min_value=0, format="%.0f"),
                    "Units": st.column_config.NumberColumn("Units",min_value=0, format="%.0f"),
                    "Budget Estimate (Rp)": st.column_config.NumberColumn("Budget Estimate (Rp)", min_value=0, format="%.0f"),
                },
            )

            rev_label = f"R({rev_input})"
            dynamic_assumptions = st.session_state.projects[active_id]["data"].get("assumptions", [])

            # aggregate all projects using canonical get_project_totals
            combined_results = []
            idx = 1
            for p_id, p_data in st.session_state.projects.items():
                pm = get_project_totals(p_data)
                combined_results.append({
                    "idx": idx, "name": p_data["name"].upper(),
                    "gba": pm["gba"], "gfa": pm["gfa"], "sgfa": pm["sgfa"],
                    "units": pm["units"], "budget": pm["budget"],
                })
                idx += 1
            edited_manual_df = edited_manual_df.fillna(0)
            for _, row in edited_manual_df.iterrows():
                p_name = str(row.get("Project Name", f"MANUAL PROJECT {idx}"))
                if p_name in ("nan", "") or not p_name.strip():
                    p_name = f"MANUAL PROJECT {idx}"
                combined_results.append({
                    "idx": idx, "name": p_name.upper(),
                    "gba":    float(row.get("GBA", 0) or 0),
                    "gfa":    float(row.get("GFA", 0) or 0),
                    "sgfa":   float(row.get("SGFA", 0) or 0),
                    "units":  float(row.get("Units", 0) or 0),
                    "budget": float(row.get("Budget Estimate (Rp)", 0) or 0),
                })
                idx += 1

            table_rows_html = ""
            total_gba = total_gfa = total_sgfa = total_budget = 0
            for p in combined_results:
                r_gba  = p["budget"] / p["gba"]  if p["gba"]  > 0 else 0
                r_gfa  = p["budget"] / p["gfa"]  if p["gfa"]  > 0 else 0
                r_sgfa = p["budget"] / p["sgfa"] if p["sgfa"] > 0 else 0
                p.update({"r_gba": r_gba, "r_gfa": r_gfa, "r_sgfa": r_sgfa})
                total_gba += p["gba"]; total_gfa += p["gfa"]; total_sgfa += p["sgfa"]; total_budget += p["budget"]
                table_rows_html += (
                    f"<tr><td style='border:1px solid black;padding:5px;'>{p['idx']}</td>"
                    f"<td style='border:1px solid black;padding:5px;text-align:left;'><b>{p['name']}</b></td>"
                    f"<td style='border:1px solid black;padding:5px;'>{p['gba']:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>{p['gfa']:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>{p['sgfa']:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>{p['units']:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>Units</td>"
                    f"<td style='border:1px solid black;padding:5px;text-align:right;'><b>{p['budget']:,.0f}</b></td>"
                    f"<td style='border:1px solid black;padding:5px;'>{r_gba:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>{r_gfa:,.0f}</td>"
                    f"<td style='border:1px solid black;padding:5px;'>{r_sgfa:,.0f}</td></tr>"
                )
            t_r_gba  = total_budget / total_gba  if total_gba  > 0 else 0
            t_r_gfa  = total_budget / total_gfa  if total_gfa  > 0 else 0
            t_r_sgfa = total_budget / total_sgfa if total_sgfa > 0 else 0

            # Excel FAD
            buffer = io.BytesIO()
            workbook = xlsxwriter.Workbook(buffer, {"in_memory": True, "nan_inf_to_errors": True})
            worksheet = workbook.add_worksheet("Portfolio Summary")
            f_blue_L  = workbook.add_format({"bg_color": "#0062a8", "font_color": "white", "bold": True, "valign": "vcenter"})
            f_th      = workbook.add_format({"bg_color": "#f2f2f2", "bold": True, "align": "center", "valign": "vcenter", "border": 1, "text_wrap": True})
            f_td_c    = workbook.add_format({"align": "center", "valign": "vcenter", "border": 1})
            f_td_L_b  = workbook.add_format({"align": "left", "valign": "vcenter", "border": 1, "bold": True})
            f_td_R_b  = workbook.add_format({"align": "right", "valign": "vcenter", "border": 1, "bold": True, "num_format": "#,##0"})
            f_td_num  = workbook.add_format({"align": "right", "valign": "vcenter", "border": 1, "num_format": "#,##0"})
            f_tot_L   = workbook.add_format({"bg_color": "#e0e0e0", "bold": True, "align": "center", "valign": "vcenter", "border": 1})
            f_tot_num = workbook.add_format({"bg_color": "#e0e0e0", "bold": True, "align": "right",  "valign": "vcenter", "border": 1, "num_format": "#,##0"})
            f_tot_empty = workbook.add_format({"bg_color": "#e0e0e0", "border": 1})
            f_assum_h = workbook.add_format({"bg_color": "#ffdf70", "bold": True, "border": 1, "valign": "vcenter"})
            f_assum_c = workbook.add_format({"align": "center", "border": 1})
            f_assum_L = workbook.add_format({"align": "left", "border": 1})
            worksheet.set_column("A:A", 5); worksheet.set_column("B:B", 38); worksheet.set_column("C:E", 15)
            worksheet.set_column("F:F", 10); worksheet.set_column("G:G", 8); worksheet.set_column("H:H", 22); worksheet.set_column("I:K", 15)
            for row in range(5): worksheet.merge_range(row, 0, row, 10, "", f_blue_L)
            worksheet.write_string(0, 0, f"ASG GROUP PROPERTY DEVELOPMENT | VERSION : {rev_label}", f_blue_L)
            worksheet.write_string(1, 0, "QS & PROCUREMENT DIVISION", f_blue_L)
            worksheet.write_string(2, 0, "PROJECT PORTFOLIO | ALL ACTIVE PROJECTS", f_blue_L)
            worksheet.write_string(3, 0, f"REF. DATA {rev_label} | UPDATED : {upd_input}", f_blue_L)
            worksheet.write_string(4, 0, f"BUDGET ESTIMATE {rev_label} | CREATED : {cre_input}", f_blue_L)
            worksheet.merge_range("A7:A8","SN",f_th); worksheet.merge_range("B7:B8","AREA",f_th)
            worksheet.merge_range("C7:E7","BUILDING AREA (M2)",f_th)
            worksheet.write_string("C8","GBA",f_th); worksheet.write_string("D8","GFA",f_th); worksheet.write_string("E8","SGFA",f_th)
            worksheet.merge_range("F7:G8","UNIT",f_th); worksheet.merge_range("H7:H8","BUDGET ESTIMATE\nRP",f_th)
            worksheet.merge_range("I7:K7","COST RATIO RP/M2",f_th)
            worksheet.write_string("I8","GBA",f_th); worksheet.write_string("J8","GFA",f_th); worksheet.write_string("K8","SGFA",f_th)
            row_idx = 8
            for p in combined_results:
                worksheet.write_number(row_idx,0,p["idx"],f_td_c); worksheet.write_string(row_idx,1,p["name"],f_td_L_b)
                worksheet.write_number(row_idx,2,p["gba"],f_td_num); worksheet.write_number(row_idx,3,p["gfa"],f_td_num)
                worksheet.write_number(row_idx,4,p["sgfa"],f_td_num); worksheet.write_number(row_idx,5,p["units"],f_td_c)
                worksheet.write_string(row_idx,6,"Units",f_td_c); worksheet.write_number(row_idx,7,p["budget"],f_td_R_b)
                worksheet.write_number(row_idx,8,p["r_gba"],f_td_num); worksheet.write_number(row_idx,9,p["r_gfa"],f_td_num)
                worksheet.write_number(row_idx,10,p["r_sgfa"],f_td_num); row_idx += 1
            worksheet.merge_range(row_idx,0,row_idx,1,"TOTAL",f_tot_L)
            worksheet.write_number(row_idx,2,total_gba,f_tot_num); worksheet.write_number(row_idx,3,total_gfa,f_tot_num)
            worksheet.write_number(row_idx,4,total_sgfa,f_tot_num); worksheet.write_string(row_idx,5,"",f_tot_empty)
            worksheet.write_string(row_idx,6,"",f_tot_empty); worksheet.write_number(row_idx,7,total_budget,f_tot_num)
            worksheet.write_number(row_idx,8,t_r_gba,f_tot_num); worksheet.write_number(row_idx,9,t_r_gfa,f_tot_num)
            worksheet.write_number(row_idx,10,t_r_sgfa,f_tot_num)
            row_idx += 2
            worksheet.write_string(row_idx,0,"I.",f_assum_h); worksheet.merge_range(row_idx,1,row_idx,10,"ASSUMPTIONS",f_assum_h)
            for i, assum in enumerate(dynamic_assumptions, 1):
                row_idx += 1
                worksheet.write_number(row_idx,0,i,f_assum_c)
                text = str(assum)
                date_match = re.search(r"(\d{2}[./-]\d{2}[./-]\d{4})", text)
                if date_match:
                    worksheet.merge_range(row_idx,1,row_idx,10,"",f_assum_L)
                    parts = text.split(date_match.group(1))
                    rich_args = []
                    if parts[0]: rich_args.append(parts[0])
                    rich_args.extend([workbook.add_format({"font_color":"red"}), date_match.group(1)])
                    if len(parts) > 1 and parts[1]: rich_args.append(parts[1])
                    worksheet.write_rich_string(row_idx,1,*rich_args,f_assum_L)
                else:
                    worksheet.merge_range(row_idx,1,row_idx,10,text,f_assum_L)
            workbook.close()
            st.download_button(label="Download FAD as .xlsx", data=buffer.getvalue(),
                file_name=f"ASG_Portfolio_{active_id}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True)

            # HTML preview
            assum_html_rows = ""
            for i, assum in enumerate(dynamic_assumptions, 1):
                display_text = re.sub(r"(\d{2}[./-]\d{2}[./-]\d{4})", r"<span style='color:red;'>\1</span>", str(assum))
                assum_html_rows += (f"<tr><td style='text-align:center;border-right:1px solid #e0e0e0;padding:2px;'>{i}</td>"
                                    f"<td style='padding:2px 5px;'>{display_text}</td></tr>")
            html_string = f"""
            <div style="font-family:Calibri,sans-serif;font-size:13px;color:black;background-color:white;padding:20px;border-radius:5px;">
                <div style="background-color:#0062a8;color:white;padding:12px;font-weight:bold;line-height:1.6;font-size:14px;">
                    <div>ASG GROUP PROPERTY DEVELOPMENT <span style="margin-left:20px;">VERSION : {rev_label}</span></div>
                    <div>QS &amp; PROCUREMENT DIVISION</div><div>PROJECT PORTFOLIO | ALL ACTIVE PROJECTS</div>
                    <div>UPDATED : {upd_input}</div><div>CREATED : {cre_input}</div>
                </div><br>
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
                        <td style="border:1px solid black;padding:5px;">GBA</td><td style="border:1px solid black;padding:5px;">GFA</td><td style="border:1px solid black;padding:5px;">SGFA</td>
                        <td style="border:1px solid black;padding:5px;">GBA</td><td style="border:1px solid black;padding:5px;">GFA</td><td style="border:1px solid black;padding:5px;">SGFA</td>
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
                </table><br>
                <table style="width:100%;border-collapse:collapse;border:1px solid #dcdcdc;text-align:left;">
                    <tr style="background-color:#ffdf70;font-weight:bold;">
                        <td style="border:1px solid white;padding:3px 5px;width:30px;text-align:center;">I.</td>
                        <td style="border:1px solid white;padding:3px 5px;">ASSUMPTIONS</td>
                    </tr>{assum_html_rows}
                </table>
            </div>"""
            st.markdown(html_string.replace("\n",""), unsafe_allow_html=True)

        # --- SUB TAB 5: REKAP ---
        with sum_sub_tabs[4]:
            st.subheader("Rekap")
            color_palette = ["#ccffe6", "#ffe6e6", "#e6e6ff", "#ffffe6", "#ffe6ff"]
            all_projects_data = []
            grand_total_all   = 0
            total_gba_all = total_gfa_all = total_sgfa_all = 0
            sum_hc = sum_prelim = sum_earth = sum_found = sum_struc = 0
            sum_arch = sum_ffe = sum_mep = sum_util = sum_ext = sum_fac = sum_cont = 0
            sum_sc = sum_cons = sum_qs = sum_pm = sum_ins = 0

            for p_id, p_dict in st.session_state.projects.items():
                pm = get_project_totals(p_dict)
                proj_entry = {"name": p_dict["name"], "gba": pm["gba"], "gfa": pm["gfa"], "sgfa": pm["sgfa"],
                              "grand": pm["budget"], "vals": pm}
                all_projects_data.append(proj_entry)
                total_gba_all  += pm["gba"];  total_gfa_all  += pm["gfa"];  total_sgfa_all += pm["sgfa"]
                sum_hc    += pm["hc_total"]; sum_prelim += pm["v_prelim"]; sum_earth  += pm["v_earth"]
                sum_found += pm["v_found"];  sum_struc  += pm["v_struc"]; sum_arch   += pm["v_arch"]
                sum_ffe   += pm["v_ffe"];    sum_mep    += pm["v_mep"];   sum_util   += pm["v_util"]
                sum_ext   += pm["v_ext"];    sum_fac    += pm["v_fac"];   sum_cont   += pm["v_cont"]
                sum_sc    += pm["sc_total"]; sum_cons   += pm["v_cons"]; sum_qs     += pm["v_qs"]
                sum_pm    += pm["v_pm"];     sum_ins    += pm["v_ins"]
                grand_total_all += pm["budget"]

            row_map = [
                {"sn":"I",   "desc":"HARDCOST",                   "coa":"118-14-000","key":"hc_total",  "sum":sum_hc,     "is_main":True},
                {"sn":"1",   "desc":"PRELIMINARIES WORKS",        "coa":"118-14-100","key":"v_prelim",  "sum":sum_prelim},
                {"sn":"2",   "desc":"EARTHWORKS",                  "coa":"118-14-200","key":"v_earth",   "sum":sum_earth},
                {"sn":"3",   "desc":"FOUNDATIONS",                 "coa":"118-14-300","key":"v_found",   "sum":sum_found},
                {"sn":"4",   "desc":"STRUCTURAL WORKS",            "coa":"118-14-500","key":"v_struc",   "sum":sum_struc},
                {"sn":"5",   "desc":"ARCHITECTURAL WORKS",         "coa":"118-14-600","key":"v_arch",    "sum":sum_arch},
                {"sn":"6",   "desc":"FF & E",                      "coa":"118-14-700","key":"v_ffe",     "sum":sum_ffe},
                {"sn":"7",   "desc":"M.E.P WORKS",                 "coa":"118-14-800","key":"v_mep",     "sum":sum_mep},
                {"sn":"8",   "desc":"UTILITY CONNECTION",          "coa":"118-13-900","key":"v_util",    "sum":sum_util},
                {"sn":"9",   "desc":"EXTERNAL WORKS",              "coa":"118-14-930","key":"v_ext",     "sum":sum_ext},
                {"sn":"10",  "desc":"FACILITY",                    "coa":"118-14-960","key":"v_fac",     "sum":sum_fac},
                {"sn":"11",  "desc":"CONTINGENCIES",               "coa":"",          "key":"v_cont",    "sum":sum_cont},
                {"sn":"II",  "desc":"SOFTCOST",                    "coa":"118-13-000","key":"sc_total",  "sum":sum_sc,     "is_main":True},
                {"sn":"1",   "desc":"CONSULTANCY SERVICES FEE",    "coa":"118-13-202","key":"v_cons",    "sum":sum_cons},
                {"sn":"2",   "desc":"QS SERVICES",                 "coa":"118-13-201","key":"v_qs",      "sum":sum_qs},
                {"sn":"3",   "desc":"PROJECT MANAGEMENT SERVICES", "coa":"118-13-203","key":"v_pm",      "sum":sum_pm},
                {"sn":"4",   "desc":"INSURANCE COVERAGE",          "coa":"118-13-300","key":"v_ins",     "sum":sum_ins},
                {"sn":"IV",  "desc":"TOTAL, EXCLD PPN",            "coa":"",          "key":"budget",    "sum":grand_total_all, "is_main":True,"is_grand_total":True},
            ]

            # dynamic headers
            header_col_names = '<td colspan="4" style="border:1px solid black;padding:4px;background-color:#e6f2ff;">TOTAL <span style="margin:0 15px;">Cost Ratio (Rp/m2)</span></td>'
            header_ratios    = '<td colspan="4" style="border:1px solid black;padding:4px;background-color:#e6f2ff;color:red;">ALL PROJECTS</td>'
            header_sublabels = '<td style="border:1px solid black;padding:4px;background-color:#e6f2ff;">TOTAL (Rp)</td><td style="border:1px solid black;padding:4px;background-color:#e6f2ff;">GBA</td><td style="border:1px solid black;padding:4px;background-color:#e6f2ff;">GFA</td><td style="border:1px solid black;padding:4px;background-color:#e6f2ff;">SGFA</td>'
            header_empty     = f'<td style="border:1px solid black;padding:4px;background-color:#e6f2ff;">-</td><td style="border:1px solid black;padding:4px;background-color:#e6f2ff;">{total_gba_all:,.0f}</td><td style="border:1px solid black;padding:4px;background-color:#e6f2ff;">{total_gfa_all:,.0f}</td><td style="border:1px solid black;padding:4px;background-color:#e6f2ff;">{total_sgfa_all:,.0f}</td>'
            for i, p in enumerate(all_projects_data):
                bg = color_palette[i % len(color_palette)]
                header_col_names  += f'<td colspan="4" style="border:1px solid black;padding:4px;background-color:{bg};">ESTIMATE <span style="margin:0 15px;">Cost Ratio (Rp/m2)</span></td>'
                header_ratios     += f'<td colspan="4" style="border:1px solid black;padding:4px;background-color:{bg};color:red;">{p["name"].upper()}</td>'
                header_sublabels  += f'<td style="border:1px solid black;padding:4px;background-color:{bg};">TOTAL (Rp)</td><td style="border:1px solid black;padding:4px;background-color:{bg};">GBA</td><td style="border:1px solid black;padding:4px;background-color:{bg};">GFA</td><td style="border:1px solid black;padding:4px;background-color:{bg};">SGFA</td>'
                header_empty      += f'<td style="border:1px solid black;padding:4px;background-color:{bg};">-</td><td style="border:1px solid black;padding:4px;background-color:{bg};">{p["gba"]:,.0f}</td><td style="border:1px solid black;padding:4px;background-color:{bg};">{p["gfa"]:,.0f}</td><td style="border:1px solid black;padding:4px;background-color:{bg};">{p["sgfa"]:,.0f}</td>'

            html_rows = ""
            for row in row_map:
                bg_color = "#e6f2e6" if row.get("is_main") else "white"
                font_w   = "bold"   if row.get("is_main") else "normal"
                blue_bg  = "background-color:#3b82f6;color:white;" if row.get("is_grand_total") else ""
                pct      = (row["sum"] / grand_total_all * 100) if grand_total_all > 0 else 0
                tot_r_gba  = row["sum"] / total_gba_all  if total_gba_all  > 0 else 0
                tot_r_gfa  = row["sum"] / total_gfa_all  if total_gfa_all  > 0 else 0
                tot_r_sgfa = row["sum"] / total_sgfa_all if total_sgfa_all > 0 else 0
                row_html = (
                    f'<tr style="background-color:{bg_color};font-weight:{font_w};{blue_bg}">'
                    f'<td style="border:1px solid black;padding:4px;text-align:center;">{row["sn"]}</td>'
                    f'<td style="border:1px solid black;padding:4px;text-align:left;">{row["desc"]}</td>'
                    f'<td style="border:1px solid black;padding:4px;text-align:center;">{row["coa"]}</td>'
                    f'<td style="border:1px solid black;padding:4px;text-align:center;">{pct:.2f}%</td>'
                    f'<td style="border:1px solid black;padding:4px;text-align:right;">{row["sum"]:,.0f}</td>'
                    f'<td style="border:1px solid black;padding:4px;text-align:right;">{tot_r_gba:,.0f}</td>'
                    f'<td style="border:1px solid black;padding:4px;text-align:right;">{tot_r_gfa:,.0f}</td>'
                    f'<td style="border:1px solid black;padding:4px;text-align:right;">{tot_r_sgfa:,.0f}</td>'
                )
                for p in all_projects_data:
                    val    = p["grand"] if row["key"] == "budget" else p["vals"].get(row["key"], 0)
                    r_gba  = val / p["gba"]  if p["gba"]  > 0 else 0
                    r_gfa  = val / p["gfa"]  if p["gfa"]  > 0 else 0
                    r_sgfa = val / p["sgfa"] if p["sgfa"] > 0 else 0
                    row_html += (f'<td style="border:1px solid black;padding:4px;text-align:right;">{val:,.0f}</td>'
                                 f'<td style="border:1px solid black;padding:4px;text-align:right;">{r_gba:,.0f}</td>'
                                 f'<td style="border:1px solid black;padding:4px;text-align:right;">{r_gfa:,.0f}</td>'
                                 f'<td style="border:1px solid black;padding:4px;text-align:right;">{r_sgfa:,.0f}</td>')
                row_html += "</tr>"
                html_rows += row_html

            detailed_html = f"""
            <div style="font-family:Arial,sans-serif;font-size:11px;color:black;background-color:white;overflow-x:auto;margin-bottom:20px;">
                <table style="width:100%;border-collapse:collapse;border:2px solid black;text-align:center;white-space:nowrap;">
                    <thead>
                        <tr style="background-color:#f2f2f2;font-weight:bold;">
                            <td rowspan="3" style="border:1px solid black;padding:4px;width:30px;">SN</td>
                            <td rowspan="3" style="border:1px solid black;padding:4px;width:200px;">DESCRIPTION</td>
                            <td rowspan="3" style="border:1px solid black;padding:4px;">COA</td>
                            <td rowspan="3" style="border:1px solid black;padding:4px;">%</td>
                            {header_col_names}
                        </tr>
                        <tr style="font-weight:bold;">{header_ratios}</tr>
                        <tr style="background-color:#f2f2f2;font-weight:bold;">{header_sublabels}</tr>
                        <tr style="background-color:#f2f2f2;font-weight:bold;">
                            <td colspan="4" style="border:1px solid black;padding:4px;"></td>
                            {header_empty}
                        </tr>
                    </thead>
                    <tbody>{html_rows}</tbody>
                </table>
            </div>"""
            st.markdown(detailed_html.replace("\n",""), unsafe_allow_html=True)

            # Rekap Excel download
            h_info    = st.session_state.projects[active_id]["data"].get("header_info", {})
            rev_label2 = f"R({h_info.get('rev_no','0')})"
            buffer_det = io.BytesIO()
            wb = xlsxwriter.Workbook(buffer_det, {"in_memory": True})
            ws = wb.add_worksheet("Detailed Estimate")
            f_blue2  = wb.add_format({"bg_color":"#0062a8","font_color":"white","bold":True,"valign":"vcenter"})
            f_th2    = wb.add_format({"bg_color":"#f2f2f2","bold":True,"align":"center","valign":"vcenter","border":1,"text_wrap":True})
            f_th_tot = wb.add_format({"bg_color":"#e6f2ff","bold":True,"align":"center","valign":"vcenter","border":1})
            f_th_tot_red = wb.add_format({"bg_color":"#e6f2ff","bold":True,"align":"center","valign":"vcenter","border":1,"font_color":"red"})
            f_c2     = wb.add_format({"align":"center","valign":"vcenter","border":1})
            f_L2     = wb.add_format({"align":"left","valign":"vcenter","border":1})
            f_pct2   = wb.add_format({"align":"center","valign":"vcenter","border":1,"num_format":"0.00%"})
            f_num2   = wb.add_format({"align":"right","valign":"vcenter","border":1,"num_format":"#,##0"})
            f_mc2    = wb.add_format({"bg_color":"#e6f2e6","bold":True,"align":"center","valign":"vcenter","border":1})
            f_mL2    = wb.add_format({"bg_color":"#e6f2e6","bold":True,"align":"left","valign":"vcenter","border":1})
            f_mpct2  = wb.add_format({"bg_color":"#e6f2e6","bold":True,"align":"center","valign":"vcenter","border":1,"num_format":"0.00%"})
            f_mnum2  = wb.add_format({"bg_color":"#e6f2e6","bold":True,"align":"right","valign":"vcenter","border":1,"num_format":"#,##0"})
            f_gc2    = wb.add_format({"bg_color":"#3b82f6","font_color":"white","bold":True,"align":"center","border":1})
            f_gL2    = wb.add_format({"bg_color":"#3b82f6","font_color":"white","bold":True,"align":"left","border":1})
            f_gpct2  = wb.add_format({"bg_color":"#3b82f6","font_color":"white","bold":True,"align":"center","border":1,"num_format":"0.00%"})
            f_gnum2  = wb.add_format({"bg_color":"#3b82f6","font_color":"white","bold":True,"align":"right","border":1,"num_format":"#,##0"})
            ws.set_column("A:A",5); ws.set_column("B:B",35); ws.set_column("C:C",12); ws.set_column("D:D",8)
            for r in range(5): ws.merge_range(r,0,r,7+(len(all_projects_data)*4),"",f_blue2)
            ws.write_string(0,0,f"ASG GROUP PROPERTY DEVELOPMENT | VERSION : {rev_label2}",f_blue2)
            ws.write_string(1,0,"QS & PROCUREMENT DIVISION",f_blue2)
            ws.write_string(2,0,"DETAILED ESTIMATE | ALL ACTIVE PROJECTS",f_blue2)
            ws.write_string(3,0,f"UPDATED : {h_info.get('updated','')}",f_blue2)
            ws.write_string(4,0,f"CREATED : {h_info.get('created','')}",f_blue2)
            ws.merge_range("A7:A9","SN",f_th2); ws.merge_range("B7:B9","DESCRIPTION",f_th2)
            ws.merge_range("C7:C9","COA",f_th2); ws.merge_range("D7:D9","%",f_th2)
            col_idx = 4
            ws.merge_range(6,col_idx,6,col_idx+3,"ESTIMATE Cost Ratio (Rp/m2)",f_th_tot)
            ws.merge_range(7,col_idx,7,col_idx+3,"TOTAL ALL PROJECTS",f_th_tot_red)
            ws.write(8,col_idx,"TOTAL (Rp)",f_th_tot); ws.write(8,col_idx+1,"GBA",f_th_tot)
            ws.write(8,col_idx+2,"GFA",f_th_tot); ws.write(8,col_idx+3,"SGFA",f_th_tot)
            ws.write_row(9,0,["","","",""],f_th2)
            ws.write(9,col_idx,"-",f_th_tot); ws.write(9,col_idx+1,total_gba_all,f_th_tot)
            ws.write(9,col_idx+2,total_gfa_all,f_th_tot); ws.write(9,col_idx+3,total_sgfa_all,f_th_tot)
            col_idx += 4
            for i, p in enumerate(all_projects_data):
                bg_hex = color_palette[i % len(color_palette)]
                f_ph   = wb.add_format({"bg_color":bg_hex,"bold":True,"align":"center","valign":"vcenter","border":1})
                f_ph_r = wb.add_format({"bg_color":bg_hex,"bold":True,"align":"center","valign":"vcenter","border":1,"font_color":"red"})
                ws.set_column(col_idx,col_idx+3,14)
                ws.merge_range(6,col_idx,6,col_idx+3,"ESTIMATE Cost Ratio (Rp/m2)",f_ph)
                ws.merge_range(7,col_idx,7,col_idx+3,p["name"].upper(),f_ph_r)
                ws.write(8,col_idx,"TOTAL (Rp)",f_ph); ws.write(8,col_idx+1,"GBA",f_ph)
                ws.write(8,col_idx+2,"GFA",f_ph); ws.write(8,col_idx+3,"SGFA",f_ph)
                ws.write(9,col_idx,"-",f_ph); ws.write(9,col_idx+1,p["gba"],f_ph)
                ws.write(9,col_idx+2,p["gfa"],f_ph); ws.write(9,col_idx+3,p["sgfa"],f_ph)
                col_idx += 4
            row_idx2 = 10
            for row in row_map:
                if row.get("is_grand_total"): fc,fs,fp,fn = f_gc2,f_gL2,f_gpct2,f_gnum2
                elif row.get("is_main"):      fc,fs,fp,fn = f_mc2,f_mL2,f_mpct2,f_mnum2
                else:                         fc,fs,fp,fn = f_c2, f_L2, f_pct2, f_num2
                pct_val   = (row["sum"] / grand_total_all) if grand_total_all > 0 else 0
                tot_r_gba = row["sum"] / total_gba_all  if total_gba_all  > 0 else 0
                tot_r_gfa = row["sum"] / total_gfa_all  if total_gfa_all  > 0 else 0
                tot_r_sgfa= row["sum"] / total_sgfa_all if total_sgfa_all > 0 else 0
                ws.write(row_idx2,0,row["sn"],fc); ws.write(row_idx2,1,row["desc"],fs)
                ws.write(row_idx2,2,row["coa"],fc); ws.write(row_idx2,3,pct_val,fp)
                ws.write(row_idx2,4,row["sum"],fn); ws.write(row_idx2,5,tot_r_gba,fn)
                ws.write(row_idx2,6,tot_r_gfa,fn); ws.write(row_idx2,7,tot_r_sgfa,fn)
                col_idx = 8
                for p in all_projects_data:
                    val    = p["grand"] if row["key"] == "budget" else p["vals"].get(row["key"], 0)
                    r_gba  = val / p["gba"]  if p["gba"]  > 0 else 0
                    r_gfa  = val / p["gfa"]  if p["gfa"]  > 0 else 0
                    r_sgfa = val / p["sgfa"] if p["sgfa"] > 0 else 0
                    ws.write(row_idx2,col_idx,val,fn); ws.write(row_idx2,col_idx+1,r_gba,fn)
                    ws.write(row_idx2,col_idx+2,r_gfa,fn); ws.write(row_idx2,col_idx+3,r_sgfa,fn)
                    col_idx += 4
                row_idx2 += 1
            wb.close()
            st.download_button(label="Download Rekap as .xlsx", data=buffer_det.getvalue(),
                file_name="ASG_Detailed_Estimate_All_Projects.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True)

    # -----------------------------------------------------------------------
    # TAB 5 — PEMBUKTIAN (AUDIT)
    # -----------------------------------------------------------------------
    with tab6:
        st.subheader("Audit")
        st.caption(f"Earthwork: Rp {struc_earth:,.0f} x {gba:,.0f} m2 = Rp {struc_earth*gba:,.0f}")
        st.caption(f"Foundation: Rp {struc_found:,.0f} x {gba:,.0f} m2 = Rp {struc_found*gba:,.0f}")
        st.caption(f"Structural: Rp {struc_work:,.0f} x {gba:,.0f} m2 = Rp {struc_work*gba:,.0f}")
        st.caption(f"Arch Base: Rp {arch_base:,.0f} x {gfa:,.0f} m2 = Rp {arch_base*gfa:,.0f}")
        st.caption(f"Precast: Rp {fac_precast_rate:,.0f} x {facade_precast_pct}% x {facade:,.0f} m2 = Rp {t_precast:,.0f}")
        st.caption(f"Window: Rp {fac_window_rate:,.0f} x {facade_window_pct}% x {facade:,.0f} m2 = Rp {t_window:,.0f}")
        st.caption(f"Double: Rp {fac_double_rate:,.0f} x {facade_double_pct}% x {facade:,.0f} m2 = Rp {t_double:,.0f}")
        st.caption(f"Wooden Door: Rp {door_wood:,.0f} x {wooden_door:,.0f} = Rp {t_w_door:,.0f}")
        st.caption(f"Glass Door: Rp {door_glass:,.0f} x {glass_door:,.0f} = Rp {t_g_door:,.0f}")
        st.caption(f"Steel Door: Rp {door_steel:,.0f} x {steel_door:,.0f} = Rp {t_s_door:,.0f}")
        st.caption(f"Lobby: Rp {lobby_rate:,.0f} x {lobby_interior:,.0f} m2 = Rp {t_lobby:,.0f}")
        st.caption(f"Gondola: Rp {gondola_rate:,.0f} x {gondola_unit:,.0f} = Rp {t_gondola:,.0f}")
        st.caption(f"Private San: {rooms:,.0f} x {san_qty_room} x Rp {san_room_rate:,.0f} = Rp {t_unit_san:,.0f}")
        st.caption(f"Toilet Male: {toilet_male:,.0f} x Rp {san_pub_m:,.0f} = Rp {t_t_male:,.0f}")
        st.caption(f"Toilet Female: {toilet_female:,.0f} x Rp {san_pub_f:,.0f} = Rp {t_t_female:,.0f}")
        st.caption(f"Disabled: {disabled_toil:,.0f} x Rp {san_dis:,.0f} = Rp {t_t_dis:,.0f}")
        st.caption(f"Mushola: {mushola_unit:,.0f} x Rp {san_mushola:,.0f} = Rp {t_mushola:,.0f}")
        st.caption(f"Kitchen: {rooms:,.0f} x Rp {kitchen_rate:,.0f} = Rp {t_kitchen:,.0f}")
        st.caption(f"HW Kayu: {wooden_door:,.0f} x Rp {hw_wood:,.0f} = Rp {t_hw_w:,.0f}")
        st.caption(f"HW Besi: {steel_door:,.0f} x Rp {hw_steel:,.0f} = Rp {t_hw_s:,.0f}")
        st.caption(f"HT: {fl_ht_pct}% x {gfa:,.0f} x Rp {fl_ht_rate:,.0f} x 1.32 = Rp {t_ht:,.0f}")
        st.caption(f"Vinyl: {fl_vinyl_pct}% x {gfa:,.0f} x Rp {fl_vinyl_rate:,.0f} x 1.32 = Rp {t_vinyl:,.0f}")
        st.caption(f"Marmer: {fl_marmer_pct}% x {gfa:,.0f} x Rp {fl_marmer_rate:,.0f} x 1.32 = Rp {t_marmer:,.0f}")
        st.caption(f"Carpet: {carpet_m2:,.0f} m2 x Rp {carpet_rate:,.0f} = Rp {t_carpet:,.0f}")
        st.caption(f"Glass: {glass_m2:,.0f} m2 x Rp {glass_rate:,.0f} = Rp {t_glass_work:,.0f}")
        st.caption(f"FF&E: {rooms:,.0f} x Rp {ffe_rate:,.0f} = Rp {t_ffe:,.0f}")
        st.caption(f"Misc: Rp {misc_rate:,.0f} x {misc_switch} = Rp {t_misc:,.0f}")
        st.caption(f"MEP: {gba:,.0f} m2 x Rp {mep_rate:,.0f} = Rp {t_mep:,.0f}")
        st.caption(f"Railing: {rooms*railing_qty:,.0f} m' x Rp {railing_rate:,.0f} = Rp {t_railing:,.0f}")
        st.caption(f"Skylight: {skylight_area:,.0f} m2 x Rp {skylight_rate:,.0f} = Rp {t_skylight:,.0f}")
        st.caption(f"External: {land_m2:,.0f} m2 x Rp {ext_land_rate:,.0f} = Rp {t_external:,.0f}")
        st.caption(f"Public Fac: {pub_fac_m2:,.0f} m2 x Rp {fac_pub_rate:,.0f} = Rp {t_pub_fac:,.0f}")
        st.caption(f"Resident Fac: {res_fac_m2:,.0f} m2 x Rp {fac_res_rate:,.0f} = Rp {t_res_fac:,.0f}")
        st.caption(f"Project Fac: {proj_fac_u:,.0f} u x Rp {fac_proj_rate:,.0f} = Rp {t_proj_fac:,.0f}")
        st.caption(f"Custom Items Total: Rp {cb['total']:,.0f}")
        st.caption(f"HC Subtotal: Rp {hc_subtotal:,.0f}")
        st.caption(f"Preliminary (5%): Rp {t_preliminary:,.0f}")
        st.caption(f"Contingency (3%): Rp {t_contingency:,.0f}")
        st.caption(f"HC Total: Rp {hc_total:,.0f}")
        st.caption(f"Utility: {gba:,.0f} m2 x Rp {utility_rate:,.0f} = Rp {t_utility:,.0f}")
        st.caption(f"Consultancy: {gfa:,.0f} m2 x Rp {consultancy_rate:,.0f} = Rp {t_consultancy:,.0f}")
        st.caption(f"QS: {qs_months} mo x Rp {qs_rate:,.0f} = Rp {t_qs:,.0f}")
        st.caption(f"PM: {pm_months} mo x Rp {pm_rate:,.0f} = Rp {t_pm:,.0f}")
        st.caption(f"Insurance: {insurance_pct}% x Rp {hc_subtotal:,.0f} = Rp {t_insurance:,.0f}")
        st.caption(f"SC Total: Rp {sc_total:,.0f}")
        st.caption(f"GRAND TOTAL: Rp {grand_total_project:,.0f}")

    # -----------------------------------------------------------------------
    # TAB 6 — PENYIMPANAN (UPLOAD / DOWNLOAD)
    # -----------------------------------------------------------------------
    with tab7:
        st.header("Upload & Download")
        c1s, c2s = st.columns(2)
        with c1s:
            uploaded_file = st.file_uploader("Upload Here:", type=["csv"])
            if uploaded_file is not None:
                if "last_loaded_file" not in st.session_state or st.session_state.last_loaded_file != uploaded_file.file_id:
                    try:
                        df_import = pd.read_csv(uploaded_file)
                        new_name_imp  = curr_proj["name"]
                        new_type_imp  = curr_proj["type"]
                        new_data_imp  = {}
                        smart_cc_imp  = []
                        for _, row in df_import.iterrows():
                            key = str(row.get("Metric_Key", ""))
                            val = row.get("Value", 0)
                            if not key or pd.isna(key): continue
                            if key == "proj_name":     new_name_imp = str(val)
                            elif key == "proj_type":   new_type_imp = str(val)
                            elif key == "smart_custom_costs_json":
                                import json
                                try: smart_cc_imp = json.loads(str(val))
                                except: pass
                            elif str(val) in ["Type1", "Type2"]:
                                new_data_imp[key] = str(val)
                            else:
                                try:    new_data_imp[key] = float(val)
                                except: new_data_imp[key] = str(val) if not pd.isna(val) else 0.0
                        if smart_cc_imp:
                            new_data_imp["smart_custom_costs"] = smart_cc_imp
                        st.session_state.projects[curr_id]["name"] = new_name_imp
                        st.session_state.projects[curr_id]["type"] = new_type_imp
                        st.session_state.projects[curr_id]["data"] = new_data_imp
                        suffix_id   = f"_{curr_id}"
                        suffix_type = f"_{curr_id}_{new_type_imp}"
                        keys_to_del = [k for k in st.session_state if k.endswith(suffix_id) or k.endswith(suffix_type)]
                        for k in keys_to_del: del st.session_state[k]
                        st.session_state.last_loaded_file = uploaded_file.file_id
                        st.success("✅ Load Complete!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

            # Export — NOW INCLUDES smart_custom_costs as JSON column
            import json as _json
            csv_data = [{"Metric_Key": "proj_name", "Value": curr_proj["name"]},
                        {"Metric_Key": "proj_type",  "Value": curr_proj["type"]}]
            smart_cc_save = st.session_state.projects[curr_id]["data"].get("smart_custom_costs", [])
            if smart_cc_save:
                csv_data.append({"Metric_Key": "smart_custom_costs_json", "Value": _json.dumps(smart_cc_save)})
            for k, v in st.session_state.projects[curr_id]["data"].items():
                if k not in ("smart_custom_costs", "header_info", "assumptions"):
                    csv_data.append({"Metric_Key": k, "Value": v})
            df_export  = pd.DataFrame(csv_data)
            csv_buffer = df_export.to_csv(index=False).encode("utf-8")
            st.download_button(label="Download", data=csv_buffer,
                file_name=f"Database_{curr_id}.csv", mime="text/csv", use_container_width=True)


# ---------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------------------------
st.sidebar.title("Main Navigation")
page_choice = st.sidebar.selectbox("Pilih Pekerjaan:", ["Cost Calculator", "Area Calculator"])
st.sidebar.markdown("---")
st.sidebar.subheader("Daftar Proyek")

proj_ids    = list(st.session_state.projects.keys())
proj_labels = [f"{st.session_state.projects[pid]['name']} ({st.session_state.projects[pid]['type']})" for pid in proj_ids]
current_index = proj_ids.index(st.session_state.current_proj_id) if st.session_state.current_proj_id in proj_ids else 0

st.sidebar.selectbox("Active Project:", options=proj_labels, index=current_index,
    key="project_selector", on_change=cb_switch_project, label_visibility="collapsed")

c1sb, c2sb = st.sidebar.columns(2)
with c1sb:
    st.button("Tambah", on_click=cb_add_project, type="primary", use_container_width=True)
with c2sb:
    can_delete = len(st.session_state.projects) > 1
    st.button("Hapus", disabled=not can_delete, on_click=cb_delete_project, type="secondary",
              help="Delete Active Project", use_container_width=True)

st.sidebar.markdown("---")

# ---------------------------------------------------------------------------
# PAGE ROUTING
# ---------------------------------------------------------------------------
if page_choice == "Area Calculator":
    show_area_calculator()
else:
    show_cost_estimator()

# ---------------------------------------------------------------------------
# AUTO-SAVE TO LOCAL STORAGE
# ---------------------------------------------------------------------------
if "projects" in st.session_state and st.session_state.get("storage_loaded", False):
    backup_payload = {
        "projects_dict":    st.session_state.projects,
        "current_proj_id":  st.session_state.current_proj_id,
        "proj_counter":     st.session_state.proj_counter,
    }
    local_storage.setItem("asg_calculator_backup", backup_payload)

st.sidebar.caption("v1.2.0 | © 2026 QS & Procurement - ASG")
