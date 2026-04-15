import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cost Estimator", layout="wide")

st.title("Project Cost Estimator")
st.markdown("Adjust the highlighted (yellow) cells from the BOQ below. All other quantities and rates are fixed based on the project parameters.")

# ==========================================
# FIXED PARAMETERS (From Image 1 & White Cells)
# ==========================================
GBA = 179970.69
GFA = 152658.99
SGFA = 124336.77
Facade = 107127.10
ROOM = 1261.00
Area_Atap = 13732.00
Interior_Lobby = 15347.92
Pintu_Kaca_qty = 344.00
Pintu_Kayu_qty = 8992.00
Pintu_Besi_qty = 1032.00
Facility_Deck = 2000.00
Landscape = 22496.94

# Fixed Rates & Percentages
rate_earthworks = 25000
rate_foundations = 400000
rate_structural = 1933000
rate_basic_arsitektur = 1058000
rate_external_works = 1563000
rate_consultancy_unit = 174000
pct_preliminaries = 0.05
pct_contingencies = 0.03
pct_insurance = 0.0012  # 0.12%

# ==========================================
# EDITABLE INPUTS (Yellow Cells)
# ==========================================
st.sidebar.header("Editable Parameters (Yellow Cells)")

with st.sidebar.expander("5. Architectural - Facade", expanded=True):
    precast_pct = st.number_input("Precast (%)", value=60.0) / 100
    precast_rate = st.number_input("Precast Rate", value=800000)
    window_wall_pct = st.number_input("Window Wall (%)", value=30.0) / 100
    window_wall_rate = st.number_input("Window Wall Rate", value=1250000)
    double_skin_pct = st.number_input("Double Skin (%)", value=10.0) / 100
    double_skin_rate = st.number_input("Double Skin Rate", value=2500000)
    pintu_kaca_rate = st.number_input("Pintu Kaca Rate", value=1000000)
    railing_rate = st.number_input("Railing Rate (6,305 m')", value=2200000)
    skylight_rate = st.number_input("Skylight Rate", value=4500000)

with st.sidebar.expander("5. Architectural - Doors & Lobby"):
    pintu_kayu_rate = st.number_input("Pintu Kayu Rate", value=3500000)
    pintu_besi_rate = st.number_input("Pintu Besi Rate", value=7000000)
    interior_lobby_rate = st.number_input("Interior Lobby Rate", value=1500000)
    gondola_qty = st.number_input("Gondola (unit)", value=15)
    gondola_rate = st.number_input("Gondola Rate", value=600000000)

with st.sidebar.expander("5. Architectural - Sanitary & Ironmongeries"):
    sanitair_typical_rate = st.number_input("Sanitair Typical Rate", value=26875000)
    sanitair_wanita_rate = st.number_input("Sanitair Wanita Rate", value=98075000)
    sanitair_pria_rate = st.number_input("Sanitair Pria Rate", value=77050000)
    sanitair_mushola_rate = st.number_input("Sanitair Mushola Rate", value=36500000)
    iron_kayu_rate = st.number_input("Ironmongeries Kayu Rate", value=750000)
    iron_besi_rate = st.number_input("Ironmongeries Besi Rate", value=1850000)

with st.sidebar.expander("5. Architectural - Finishes (Keramik, Carpet, Kaca)"):
    ht_ct_pct = st.number_input("HT / CT (%)", value=90.0) / 100
    ht_ct_rate = st.number_input("HT / CT Rate", value=150000)
    vinyl_pct = st.number_input("Vinyl (%)", value=0.0) / 100
    vinyl_rate = st.number_input("Vinyl Rate", value=750000)
    marmer_pct = st.number_input("Marmer (%)", value=10.0) / 100
    marmer_rate = st.number_input("Marmer Rate", value=750000)
    carpet_qty = st.number_input("Carpet Qty", value=0)
    carpet_rate = st.number_input("Carpet Rate", value=1200000)
    kaca_qty = st.number_input("Kaca Qty", value=0)
    kaca_rate = st.number_input("Kaca Rate", value=700000)

with st.sidebar.expander("5. Architectural - Item Tambahan"):
    item_tambahan_1_name = st.text_input("Item Tambahan 1 Name", value="Item Tambahan 1")
    item_tambahan_1_amt = st.number_input("Item Tambahan 1 Amount (Ls)", value=0)
    item_tambahan_2_name = st.text_input("Item Tambahan 2 Name", value="Item Tambahan 2")
    item_tambahan_2_amt = st.number_input("Item Tambahan 2 Amount (Ls)", value=0)

with st.sidebar.expander("6. FF&E | 7. MEP | 8. Utility | 10. Facility"):
    ffe_rate = st.number_input("FF&E Rate (per unit)", value=32000000)
    lain2_rate = st.number_input("Lain2 (Linen chute, etc) Rate", value=32000000)
    mep_rate = st.number_input("M.E.P Works Rate (per GBA)", value=2810941)
    utility_amt = st.number_input("Utility Connection Amount", value=16575000000)
    fasilitas_penghuni_rate = st.number_input("Fasilitas Penghuni Rate", value=10000000)
    fasilitas_proyek_rate = st.number_input("Fasilitas Proyek Rate", value=2000000000)

with st.sidebar.expander("Soft Cost - Durations"):
    qs_bln = st.number_input("QS Services (Months)", value=36)
    pm_bln = st.number_input("PM Services (Months)", value=36)

# ==========================================
# CALCULATIONS
# ==========================================
# 2. Earthworks & 3. Foundations & 4. Structural
cost_earthworks = GBA * rate_earthworks
cost_foundations = GBA * rate_foundations
cost_structural = GBA * rate_structural

# 5. Architectural
cost_basic_arsitektur = GFA * rate_basic_arsitektur
cost_facade = (Facade * precast_pct * precast_rate) + \
              (Facade * window_wall_pct * window_wall_rate) + \
              (Facade * double_skin_pct * double_skin_rate) + \
              (Pintu_Kaca_qty * pintu_kaca_rate) + \
              (6305 * railing_rate) + \
              (0 * skylight_rate) # Assuming 0 m2 for skylight based on image
cost_pintu_kayu = Pintu_Kayu_qty * pintu_kayu_rate
cost_pintu_besi = Pintu_Besi_qty * pintu_besi_rate
cost_interior_lobby = Interior_Lobby * interior_lobby_rate
cost_gondola = gondola_qty * gondola_rate
cost_sanitair = (3783 * sanitair_typical_rate) + \
                (15 * sanitair_wanita_rate) + \
                (15 * sanitair_pria_rate) + \
                (2 * sanitair_mushola_rate)
cost_ironmongeries = (Pintu_Kayu_qty * iron_kayu_rate) + (Pintu_Besi_qty * iron_besi_rate)
area_keramik = 201509.87
cost_keramik = (area_keramik * ht_ct_pct * ht_ct_rate) + \
               (area_keramik * vinyl_pct * vinyl_rate) + \
               (area_keramik * marmer_pct * marmer_rate)
cost_carpet = carpet_qty * carpet_rate
cost_kaca_tambahan = kaca_qty * kaca_rate

cost_architectural = sum([cost_basic_arsitektur, cost_facade, cost_pintu_kayu, cost_pintu_besi,
                          cost_interior_lobby, cost_gondola, cost_sanitair, cost_ironmongeries,
                          cost_keramik, cost_carpet, cost_kaca_tambahan, 
                          item_tambahan_1_amt, item_tambahan_2_amt])

# 6, 7, 8, 9, 10 Other Hard Costs
cost_ffe = (ROOM * ffe_rate) + (1 * lain2_rate)
cost_mep = GBA * mep_rate
cost_utility = utility_amt
cost_external_works = Landscape * rate_external_works
cost_facility = (Facility_Deck * fasilitas_penghuni_rate) + (2 * fasilitas_proyek_rate)

# Base Hardcost (Utility is excluded from Prelims/Contingency calculation in the original sheet)
base_hardcost = cost_earthworks + cost_foundations + cost_structural + cost_architectural + \
                cost_ffe + cost_mep + cost_external_works + cost_facility

cost_preliminaries = base_hardcost * pct_preliminaries
cost_contingencies = base_hardcost * pct_contingencies

# Total Hard Cost
total_hard_cost = base_hardcost + cost_utility + cost_preliminaries + cost_contingencies

# Soft Costs
cost_consultancy = GFA * rate_consultancy_unit
cost_qs = qs_bln * 75000000
cost_pm = pm_bln * 250000000
cost_insurance = base_hardcost * pct_insurance

total_soft_cost = cost_consultancy + cost_qs + cost_pm + cost_insurance

# Grand Total & Ratio
grand_total = total_hard_cost + total_soft_cost
rasio_sgfa = grand_total / SGFA

# ==========================================
# DISPLAY RESULTS
# ==========================================
col1, col2 = st.columns(2)
col1.metric("Grand Total (IDR)", f"Rp {grand_total:,.0f}")
col2.metric("Rasio SGFA (IDR/m2)", f"Rp {rasio_sgfa:,.0f}")

st.divider()

# Create a DataFrame to display the Breakdown Summary
data = {
    "No": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "", "SOFT", "", "", "", "TOTAL"],
    "Description": [
        "PRELIMINARIES WORKS", "EARTHWORKS", "FOUNDATIONS", "STRUCTURAL WORKS", 
        "ARCHITECTURAL WORKS", "FF & E", "M.E.P WORKS", "UTILITY CONNECTION", 
        "EXTERNAL WORKS", "FACILITY", "CONTINGENCIES", 
        "HARD COST TOTAL", "CONSULTANCY SERVICES", "QS SERVICES", 
        "PROJECT MANAGEMENT", "INSURANCE", "GRAND TOTAL"
    ],
    "Amount (IDR)": [
        cost_preliminaries, cost_earthworks, cost_foundations, cost_structural,
        cost_architectural, cost_ffe, cost_mep, cost_utility, 
        cost_external_works, cost_facility, cost_contingencies, 
        total_hard_cost, cost_consultancy, cost_qs, cost_pm, cost_insurance, grand_total
    ]
}

df_summary = pd.DataFrame(data)

# Formatting the output to look like currency
df_summary["Amount (IDR)"] = df_summary["Amount (IDR)"].apply(lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x)

st.subheader("Cost Summary Breakdown")
st.dataframe(df_summary, use_container_width=True, hide_index=True)
