import streamlit as st
import pandas as pd

# 1. Initialize session state
if 'db' not in st.session_state:
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

# Get dynamic lists from the current database
current_rooms = sorted(st.session_state.db['Room/Work Name'].unique().tolist())
current_projects = sorted(st.session_state.db['Project Type'].unique().tolist())

with st.form("add_item_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Room / Work Name inputs
        room_sel = st.selectbox("Room / Work Name", ["+ Add New..."] + current_rooms)
        new_room = st.text_input("Type new Room Name here (if adding new)")
        
        st.write("") # Spacer
        
        # Project Type inputs
        proj_sel = st.selectbox("Project Type", ["+ Add New..."] + current_projects)
        new_proj = st.text_input("Type new Project Type here (if adding new)")
    
    with col2:
        item_name = st.text_input("Item Name (e.g., Urinal, Sink)")
        
    with col3:
        unit_qty = st.number_input("Unit Qty", min_value=1, step=1)
        unit_price = st.number_input("Unit Price", min_value=0, step=50000)

    submitted = st.form_submit_button("Add to Database")
    
    if submitted and item_name:
        # Determine the final values based on user input
        final_room = new_room if room_sel == "+ Add New..." and new_room else room_sel
        final_project = new_proj if proj_sel == "+ Add New..." and new_proj else proj_sel

        # Validation: prevent empty new categories
        if final_room == "+ Add New..." or final_project == "+ Add New...":
            st.error("⚠️ Please type a name for the new Room or Project Type.")
        else:
            new_row = {
                'Room/Work Name': final_room,
                'Project Type': final_project,
                'Item Name': item_name,
                'Unit Qty': unit_qty,
                'Unit Price': unit_price
            }
            # Append the new row
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Added {item_name} to {final_room} ({final_project})!")

st.divider()

# --- SECTION 2: VIEW, SORT & CALCULATE ---
st.header("Database & Subtotals")

df = st.session_state.db.copy()
df['Total Price'] = df['Unit Qty'] * df['Unit Price']

selected_project = st.selectbox("Filter by Project Type", ["All"] + sorted(df['Project Type'].unique().tolist()))

if selected_project != "All":
    filtered_df = df[df['Project Type'] == selected_project]
else:
    filtered_df = df

filtered_df = filtered_df.sort_values(by=['Room/Work Name', 'Item Name'])

st.dataframe(
    filtered_df, 
    use_container_width=True,
    hide_index=True,
    column_config={
        "Unit Price": st.column_config.NumberColumn(format="%d"),
        "Total Price": st.column_config.NumberColumn(format="%d")
    }
)

if not filtered_df.empty:
    st.subheader("Subtotals by Room/Work Name")
    
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
