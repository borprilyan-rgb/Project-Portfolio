import streamlit as st
import pandas as pd

# --- 1. DATA EXTRACTION ---
data_retail_pria = {
    "Item": ["CLOSET", "JET WASHER", "WASTAFEL +kran", "Vanity", "Cubicle", "Hand Dryer", "FLOOR DRAIN", "Robe hook & Tissue Holder", "Urinoir", "Partisi Urinoir"],
    "Unit": [3, 3, 3, 3, 3, 2, 9, 3, 3, 3],
    "Unit Price (Rp)": [7000000, 900000, 5000000, 6000000, 15000000, 1050000, 400000, 275000, 3500000, 2500000],
    "Total (Rp)": [21000000, 2700000, 15000000, 18000000, 45000000, 2100000, 3600000, 825000, 10500000, 7500000]
}

data_retail_wanita = {
    "Item": ["CLOSET", "JET WASHER", "WASTAFEL +kran", "Vanity", "Cubicle", "Hand Dryer", "FLOOR DRAIN", "Robe hook & Tissue Holder"],
    "Unit": [5, 5, 3, 3, 5, 2, 8, 5],
    "Unit Price (Rp)": [7000000, 900000, 5000000, 6000000, 15000000, 1050000, 400000, 275000],
    "Total (Rp)": [35000000, 4500000, 15000000, 18000000, 75000000, 2100000, 3200000, 1375000]
}

data_hotel_pria = {
    "Item": ["CLOSET", "JET WASHER", "WASTAFEL +kran", "Vanity", "Cubicle", "Hand Dryer", "FLOOR DRAIN", "Robe hook & Tissu Holder", "Urinoir", "Partisi Urinoir"],
    "Unit": [2, 2, 2, 2, 2, 2, 9, 2, 2, 2],
    "Unit Price (Rp)": [7000000, 900000, 5000000, 6000000, 15000000, 1050000, 400000, 275000, 3500000, 2500000],
    "Total (Rp)": [14000000, 1800000, 10000000, 12000000, 30000000, 2100000, 3600000, 550000, 7000000, 5000000]
}

data_hotel_wanita = {
    "Item": ["CLOSET", "JET WASHER", "WASTAFEL +kran", "Vanity", "Cubicle", "Hand Dryer", "FLOOR DRAIN", "Robe hook & Tissu Holder"],
    "Unit": [3, 3, 3, 3, 3, 2, 8, 3],
    "Unit Price (Rp)": [7000000, 900000, 5000000, 6000000, 15000000, 1050000, 400000, 275000],
    "Total (Rp)": [21000000, 2700000, 15000000, 18000000, 45000000, 2100000, 3200000, 825000]
}

# --- 2. HELPER FUNCTIONS ---
def format_currency(val):
    """Formats numbers to standard comma-separated values."""
    return f"{val:,.0f}"

# --- 3. STREAMLIT UI SETUP ---
st.set_page_config(page_title="Budget Database Toilet", layout="wide")
st.title("Database Estimasi Biaya Toilet Publik")

# Sidebar navigation
st.sidebar.header("Pilih Kategori Toilet")
category = st.sidebar.radio(
    "Navigasi Data:",
    ("Publik Toilet RETAIL - Pria",
     "Publik Toilet RETAIL - Wanita",
     "Publik Toilet Hotel - Pria",
     "Publik Toilet Hotel - Wanita")
)

# --- 4. LOGIC & DISPLAY ---
# Map the selection to the correct data and assign the grand total
if category == "Publik Toilet RETAIL - Pria":
    df = pd.DataFrame(data_retail_pria)
    grand_total = 126225000
elif category == "Publik Toilet RETAIL - Wanita":
    df = pd.DataFrame(data_retail_wanita)
    grand_total = 154175000
elif category == "Publik Toilet Hotel - Pria":
    df = pd.DataFrame(data_hotel_pria)
    grand_total = 86050000
else:
    df = pd.DataFrame(data_hotel_wanita)
    grand_total = 107825000

# Format the numerical columns to look like standard currency
df_display = df.copy()
df_display['Unit Price (Rp)'] = df_display['Unit Price (Rp)'].apply(format_currency)
df_display['Total (Rp)'] = df_display['Total (Rp)'].apply(format_currency)

# Render the layout
st.subheader(category)

# Using st.dataframe allows users to sort columns and scroll if needed
st.dataframe(df_display, use_container_width=True, hide_index=True)

# Render the Grand Total at the bottom
st.markdown(f"### Total Keseluruhan: **Rp {format_currency(grand_total)}**")
