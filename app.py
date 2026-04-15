# --- STEP 2: UNIT RATES (Changeable Numbers) ---
st.subheader("💰 Unit Rates & Estimations")
col_rate1, col_rate2, col_rate3 = st.columns(3)

with col_rate1:
    rate_earthwork = st.number_input("Earthwork Rate (per GBA m²)", min_value=0.0, value=0.0)
    rate_foundation = st.number_input("Foundation Rate (per GBA m²)", min_value=0.0, value=0.0)

with col_rate2:
    rate_structural = st.number_input("Structural Work Rate (per GBA m²)", min_value=0.0, value=0.0)

# --- SUB-SECTION: BASIC ARCHITECTURE ---
st.markdown("#### 🏛️ Basic Architecture")
col_arch1, col_arch2 = st.columns(2)

with col_arch1:
    # Dropdown to select project type
    project_type = st.selectbox(
        "Project Type",
        ["Hotel", "Retail", "Apartment", "Parking"]
    )

with col_arch2:
    # Changeable number for the architecture rate
    rate_architecture = st.number_input(f"Architecture Rate for {project_type} (per GFA m²)", min_value=0.0, value=0.0)

# --- STEP 3: CALCULATIONS ---
total_earthwork = gba * rate_earthwork
total_foundation = gba * rate_foundation
total_structural = gba * rate_structural
# Architecture uses GFA as requested
total_architecture = gfa * rate_architecture

# --- STEP 4: HARD COST INFORMATION TABLE ---
st.header("📊 Hard Cost")

hard_cost_data = {
    "Description": [
        "1. Preliminary Works", 
        "2. Earthwork", 
        "3. Foundation",
        "4. Structural Work",
        f"5. Basic Architecture ({project_type})" # Dynamic Label
    ],
    "Basis": [
        "5% of Hard Cost", 
        f"{gba:,.2f} m² (GBA) x {rate_earthwork:,.2f}", 
        f"{gba:,.2f} m² (GBA) x {rate_foundation:,.2f}",
        f"{gba:,.2f} m² (GBA) x {rate_structural:,.2f}",
        f"{gfa:,.2f} m² (GFA) x {rate_architecture:,.2f}" # Uses GFA
    ],
    "Amount": [
        0.0, 
        total_earthwork, 
        total_foundation,
        total_structural,
        total_architecture
    ]
}

df_hc = pd.DataFrame(hard_cost_data)

# Displaying the table
st.table(df_hc.style.format({"Amount": "{:,.2f}"}))
