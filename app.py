import streamlit as st
import pandas as pd
import plotly.express as px

# Set up page layout and title
st.set_page_config(page_title="Budget Estimate Dashboard", layout="wide", page_icon="🏗️")

st.title("🏗️ Project Budget Estimate Dashboard")
st.markdown("Interactive budget visualization for the **RWI.PALMBEACH.MIDRISE APARTEMENT** project.")

# Optional File uploader for flexibility
uploaded_file = st.file_uploader("Upload Budget CSV (Optional)", type=['csv'])

# Use the uploaded file or default to the local file
file_path = uploaded_file if uploaded_file is not None else "calc.xlsx - APT.csv"

try:
    # ==========================================
    # 1. Parse Summary Project Metrics (Top part)
    # ==========================================
    df_raw = pd.read_csv(file_path)
    
    st.header("📋 Project Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    # Extract values based on the specific row/column format in the CSV
    lahan = df_raw.iloc[7, 4]
    gba = df_raw.iloc[8, 4]
    gfa = df_raw.iloc[9, 4]
    rooms = df_raw.iloc[12, 4]
    
    col1.metric("LAHAN (m²)", f"{float(lahan):,.2f}")
    col2.metric("GBA", f"{float(gba):,.2f}")
    col3.metric("GFA", f"{float(gfa):,.2f}")
    col4.metric("ROOMS", str(rooms))
    
    st.divider()

    # ==========================================
    # 2. Parse Detailed Cost Data (Bottom part)
    # ==========================================
    # Skip the 15 header rows to get to the main tabular data
    df_data = pd.read_csv(file_path, skiprows=15)
    
    # Rename columns for easier handling
    df_data.columns = ['Empty', 'SN', 'Item_Name', 'Description', 'Code', 'Qty', 'Unit', 'Rate', 'Total', 'Remarks']
    df_data = df_data.drop(columns=['Empty']) # Drop the leading empty column
    
    # Filter rows that represent the MAIN categories (where SN is a number like 1, 2, 3...)
    main_cats = df_data[df_data['SN'].astype(str).str.match(r'^\d+$')].copy()
    main_cats['Total'] = pd.to_numeric(main_cats['Total'], errors='coerce')
    
    # Distinguish between 'Hard Cost' and 'Soft Cost' using the "SOFT COST" row index
    soft_cost_idx = df_data[df_data['SN'] == 'SOFT COST'].index
    if len(soft_cost_idx) > 0:
        idx_split = soft_cost_idx[0]
        # Any row index greater than the "SOFT COST" label becomes a Soft Cost
        main_cats['Cost Type'] = main_cats.index.map(lambda x: 'Soft Cost' if x > idx_split else 'Hard Cost')
    else:
        main_cats['Cost Type'] = 'Hard Cost'

    # ==========================================
    # 3. Visualizations
    # ==========================================
    st.header("📊 Cost Breakdown")
    
    col_fig1, col_fig2 = st.columns(2)
    
    # Bar Chart
    fig_bar = px.bar(
        main_cats, 
        x='Item_Name', 
        y='Total', 
        color='Cost Type',
        title="Total Cost by Category", 
        text_auto='.2s',
        labels={'Item_Name': 'Category', 'Total': 'Total Cost (IDR)'}
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    col_fig1.plotly_chart(fig_bar, use_container_width=True)
    
    # Donut Chart
    fig_pie = px.pie(
        main_cats, 
        names='Item_Name', 
        values='Total', 
        hole=0.4, 
        title="Cost Distribution Share"
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    col_fig2.plotly_chart(fig_pie, use_container_width=True)
    
    st.divider()

    # ==========================================
    # 4. Detailed Data Table
    # ==========================================
    st.header("📝 Detailed Data Table")
    # Clean the display dataframe by removing completely blank rows
    display_df = df_data.dropna(how='all', subset=['SN', 'Item_Name', 'Total']).reset_index(drop=True)
    
    # Format the Total and Rate columns for better readability
    st.dataframe(
        display_df.style.format({
            "Rate": "{:,.2f}",
            "Total": "{:,.2f}"
        }), 
        use_container_width=True,
        height=400
    )

except FileNotFoundError:
    st.warning("⚠️ Please upload a CSV file or ensure `calc.xlsx - APT.csv` is in the same directory as this script.")
except Exception as e:
    st.error(f"❌ Error processing the file: {e}")
