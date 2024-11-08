import streamlit as st
from input_forms.contract_selection import run_contract_selection
from input_forms.id_upload import process_id_upload
from input_forms.contract_details import run_contract_details
from input_forms.contract_generation import run_contract_generation
from input_forms.view_contracts import view_contracts  # Import the new view contracts function

def run_streamlit_app():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Select Contract Type", "Upload ID Details", "Property Details", "Generate Contract", "View Contracts"])

    # Run the appropriate function based on the selected page
    if page == "Select Contract Type":
        run_contract_selection()
    elif page == "Upload ID Details":
        process_id_upload('buyer')  # Add logic for user type handling as needed
        process_id_upload('seller')
    elif page == "Property Details":
        run_contract_details()
    elif page == "Generate Contract":
        if 'contract_type' in st.session_state:
            run_contract_generation(st.session_state['contract_type'])
        else:
            st.error("Please select the contract type first.")
    elif page == "View Contracts":
        view_contracts()  # Display the contracts and their details

if __name__ == "__main__":
    run_streamlit_app()
