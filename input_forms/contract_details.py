import streamlit as st
import json

def load_placeholders(contract_type):
    # Map user-friendly names to filenames
    contract_map = {
        "Rental Contract": "contract_rent.json",
        "Sales Contract": "contract_sale.json"
    }
    json_filename = contract_map.get(contract_type, None)

    if not json_filename:
        raise FileNotFoundError(f"No JSON file found for contract type: {contract_type}")

    json_path = f"placeholders_json/{json_filename}"
    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)

def run_contract_details():
    st.title("Enter Contract Details")
    contract_type = st.session_state.get('contract_type', None)
    if not contract_type:
        st.warning("Please select the contract type first.")
        return

    placeholders = load_placeholders(contract_type)
    if not placeholders:
        st.error("Error loading placeholders.")
        return
    
    contract_data = {}

    # Display contract date as a calendar input
    st.subheader("Contract Date")
    contract_data["contract_date"] = st.date_input("Select Contract Date")

    # Autofill and display the parties' details
    st.subheader("Parties Details")
    if contract_type == "Rental Contract":
        parties = ["landlord", "tenant"]
    elif contract_type == "Sales Contract":
        parties = ["seller", "buyer"]

    for party in parties:
        st.write(f"**{party.capitalize()} Details**")
        if f"{party}_details" in st.session_state:
            for key, value in st.session_state[f"{party}_details"].items():
                contract_data[f"{party}_{key}"] = st.text_input(
                    f"{key.replace('_', ' ').capitalize()} ({party.capitalize()})",
                    value=value,
                    key=f"{party}_{key}_input"
                )
        else:
            st.warning(f"No details found for {party.capitalize()}. Please upload or enter ID details first.")

    if contract_type == "Rental Contract":
        # Display rental-specific details
        st.subheader("Property Details")
        for field, placeholder in placeholders.get("property_details", {}).items():
            contract_data[field] = st.text_input(
                field.replace('_', ' ').capitalize(),
                value="" if placeholder.startswith("[") else placeholder,
                key=f"property_{field}"
            )

        st.subheader("Rental Term")
        contract_data["rental_start_date"] = st.date_input("Rental Start Date")
        contract_data["rental_end_date"] = st.date_input("Rental End Date")

        st.subheader("Rental Price Details")
        contract_data["monthly_rent"] = st.text_input("Monthly Rent")
        contract_data["payment_method"] = st.text_input("Payment Method")
        contract_data["payment_due_date"] = st.date_input("Payment Due Date")

        st.subheader("Deposit Details")
        contract_data["deposit_amount"] = st.text_input("Deposit Amount")

        st.subheader("Advance Payment Details")
        contract_data["advance_payment_amount"] = st.text_input("Advance Payment Amount")
        contract_data["advance_payment_description"] = st.text_area("Advance Payment Description")

        st.subheader("Contract Termination")
        contract_data["penalty_fee"] = st.text_input("Penalty Fee")

        st.subheader("Meter Readings")
        contract_data["hot_water"] = st.text_input("Hot Water Index")
        contract_data["cold_water"] = st.text_input("Cold Water Index")
        contract_data["electricity"] = st.text_input("Electricity Index")

        contract_data["association_balance_due"] = st.text_input("Association Balance Due")
    
    elif contract_type == "Sales Contract":
        # Display sales-specific details
        st.subheader("Property Sale Details")
        contract_data["apartment_number"] = st.text_input("Apartment Number")
        contract_data["building_name"] = st.text_input("Building Name")
        contract_data["staircase"] = st.text_input("Staircase")
        contract_data["floor"] = st.text_input("Floor")
        contract_data["city"] = st.text_input("City")
        contract_data["street_name"] = st.text_input("Street Name")
        contract_data["street_number"] = st.text_input("Street Number")
        contract_data["land_area"] = st.text_input("Land Area")
        #contract_data["shared_ownership"] = st.text_input("Shared Ownership")
        
        st.subheader("Sale Price Details")
        contract_data["sale_price"] = st.text_input("Sale Price")

    if st.button("Save Contract Details"):
        # Store data temporarily in session state for contract generation
        st.session_state['contract_data'] = contract_data
        st.success("Contract details saved temporarily!")
