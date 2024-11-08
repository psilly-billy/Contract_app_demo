import streamlit as st

def run_contract_selection():
    st.title("Select the Type of Contract")
    contract_type = st.selectbox("Select the type of contract:", ["Rental Contract", "Sales Contract"])
    st.session_state['contract_type'] = contract_type
    st.write(f"You selected: {contract_type}")