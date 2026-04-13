import streamlit as st
import pandas as pd

# 1. Initialize session state to hold our database during the session
if 'db' not in st.session_state:
    # Pre-loading your example data
    initial_data = {
        'Room/Work Name': ['Men Toilet', 'Men Toilet', 'Men Toilet', 'Men Toilet'],
        'Project Type': ['Retail', 'Retail', 'Hotel', 'Hotel'],
        'Item Name': ['Closet', 'Jet Washer', 'Closet', 'Jet Washer'],
        'Unit Qty': [3, 3, 2, 2],
        'Unit Price': [7000000, 900000, 5500000, 650000]
    }
    st.session_state.db = pd.DataFrame(initial_data)

st.set_page_config(page_title="Estimating Database", layout="wide")
st.title("Project Estimating Database")

# --- SECTION 1: ADD NEW ITEMS ---
st.header("Add New Item")
with st.form("add_item_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        room_name = st.selectbox("Room / Work Name", 
                                 ["Men Toilet", "Women Toilet", "Disabled", "Architecture", "Sanitary", "Openings"])
        project_type = st.selectbox("Project Type", ["Hotel", "Apartment", "Retail"])
    
    with col2:
        item_name = st.text_input("Item Name (e.g., Urinal, Sink)")
        
    with col3:
        unit_qty = st.number_input("Unit Qty", min_value=1, step=1)
        unit_price = st.number_input("Unit Price", min_value=0, step=50000)

    submitted = st.form_submit_button("Add to Database")
    
    if submitted and item_name:
        new_row = {
            'Room/Work Name': room_name,
            'Project Type': project_type,
            'Item Name': item_name,
            'Unit Qty': unit_qty,
            'Unit Price': unit_price
        }
        # Append the new row to our dataframe
        st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"Added {item_name} to the database!")

st.divider()

# --- SECTION 2: VIEW, SORT & CALCULATE ---
st.header("Database & Subtotals")

# Create a working copy of the database and calculate total price
df = st.session_state.db.copy()
df['Total Price'] = df['Unit Qty'] * df['Unit Price']

# Filtering options
selected_project = st.selectbox("Filter by Project Type", ["All"] + list(df['Project Type'].unique()))

if selected_project != "All":
    filtered_df = df[df['Project Type'] == selected_project]
else:
    filtered_df = df

# Sort the data by Room/Work Name
filtered_df = filtered_df.sort_values(by=['Room/Work Name', 'Item Name'])

# Display the main dataframe
st.dataframe(
    filtered_df, 
    use_container_width=True,
    hide_index=True,
    column_config={
        "Unit Price": st.column_config.NumberColumn(format="%d"),
        "Total Price": st.column_config.NumberColumn(format="%d")
    }
)

# Calculate and display subtotals
if not filtered_df.empty:
    st.subheader("Subtotals by Room/Work Name")
    
    # Group by Room/Work Name and sum the Total Price
    subtotals = filtered_df.groupby('Room/Work Name')['Total Price'].sum().reset_index()
    
    colA, colB = st.columns([2, 1])
    with colA:
        st.dataframe(
            subtotals, 
            use_container_width=True, 
            hide_index=True,
            column_config={"Total Price": st.column_config.NumberColumn(format="%d")}
        )
    
    with colB:
        grand_total = filtered_df['Total Price'].sum()
        st.metric(label="Grand Total", value=f"{grand_total:,.0f}")
