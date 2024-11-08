import streamlit as st
import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime

DB_PATH = 'contracts_app.db'
CONTRACTS_DIR = "contracts_files"

# Function to delete a contract from the database and local storage
def delete_contract(contract_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contract_details WHERE contract_id = ?', (contract_id,))
        cursor.execute('DELETE FROM contracts WHERE contract_id = ?', (contract_id,))
        conn.commit()

    local_path = os.path.join(CONTRACTS_DIR, f"contract_{contract_id}.docx")
    if os.path.exists(local_path):
        os.remove(local_path)
        st.success(f"Contract {contract_id} deleted successfully from database and local storage.")
    else:
        st.warning(f"Contract {contract_id} deleted from database, but local file was not found.")

# Function to generate contract statistics
def generate_contract_statistics():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT contract_type, COUNT(*) FROM contracts GROUP BY contract_type')
        contract_counts = cursor.fetchall()
        
        st.subheader("Contract Statistics")
        cursor.execute('SELECT COUNT(*) FROM contracts')
        total_contracts = cursor.fetchone()[0]
        st.write(f"**Total Number of Contracts:** {total_contracts}")
        
        types, counts = [], []
        for contract_type, count in contract_counts:
            st.write(f"{contract_type.capitalize()}: {count}")
            types.append(contract_type.capitalize())
            counts.append(count)

        if types and counts:
            fig, ax = plt.subplots()
            ax.bar(types, counts, color=['blue', 'green'])
            ax.set_title("Contracts by Type")
            ax.set_xlabel("Contract Type")
            ax.set_ylabel("Number of Contracts")
            st.pyplot(fig)

# Function to display contracts close to expiry
def display_renewal_alert():
    st.subheader("Contracts Close to Expiry")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT contracts.contract_id, contracts.contract_type, details.detail_value AS expiry_date
            FROM contracts
            JOIN contract_details details ON contracts.contract_id = details.contract_id
            WHERE details.detail_key = 'rental_end_date'
        ''')
        contracts = cursor.fetchall()
        
        today = datetime.date.today()
        close_to_expiry = [contract for contract in contracts if datetime.date.fromisoformat(contract[2]) <= (today + datetime.timedelta(days=30))]
        
        if close_to_expiry:
            for contract in close_to_expiry:
                contract_id, contract_type, expiry_date = contract
                st.write(f"**Contract ID {contract_id} ({contract_type.capitalize()}) expires on {expiry_date}")
        else:
            st.write("No contracts close to expiry.")

# Main function to view contracts
def view_contracts():
    st.title("View Existing Contracts")

    with st.expander("Contracts List"):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT contract_id, contract_type, contract_date, landlord_id, tenant_id, seller_id, buyer_id FROM contracts')
            contracts = cursor.fetchall()

            if contracts:
                for contract in contracts:
                    contract_id, contract_type, contract_date, landlord_id, tenant_id, seller_id, buyer_id = contract

                    st.subheader(f"Contract ID: {contract_id}")
                    st.write(f"**Type:** {contract_type.capitalize()}")
                    st.write(f"**Date:** {contract_date}")

                    if landlord_id:
                        cursor.execute('SELECT first_name, last_name FROM users WHERE user_id = ?', (landlord_id,))
                        landlord = cursor.fetchone()
                        st.write(f"**Landlord:** {landlord[0]} {landlord[1]}" if landlord else "**Landlord:** Not found")

                    if tenant_id:
                        cursor.execute('SELECT first_name, last_name FROM users WHERE user_id = ?', (tenant_id,))
                        tenant = cursor.fetchone()
                        st.write(f"**Tenant:** {tenant[0]} {tenant[1]}" if tenant else "**Tenant:** Not found")

                    if seller_id:
                        cursor.execute('SELECT first_name, last_name FROM users WHERE user_id = ?', (seller_id,))
                        seller = cursor.fetchone()
                        st.write(f"**Seller:** {seller[0]} {seller[1]}" if seller else "**Seller:** Not found")

                    if buyer_id:
                        cursor.execute('SELECT first_name, last_name FROM users WHERE user_id = ?', (buyer_id,))
                        buyer = cursor.fetchone()
                        st.write(f"**Buyer:** {buyer[0]} {buyer[1]}" if buyer else "**Buyer:** Not found")

                    # Button to view contract details
                    if st.button(f"View Details for Contract ID {contract_id}", key=f"view_details_{contract_id}"):
                        st.session_state[f"show_details_{contract_id}"] = not st.session_state.get(f"show_details_{contract_id}", False)

                    # Display contract details if toggled
                    if st.session_state.get(f"show_details_{contract_id}", False):
                        cursor.execute('SELECT detail_key, detail_value FROM contract_details WHERE contract_id = ?', (contract_id,))
                        details = cursor.fetchall()
                        if details:
                            st.write("**Contract Details:**")
                            for key, value in details:
                                st.write(f"**{key.replace('_', ' ').capitalize()}:** {value}")
                        else:
                            st.write("No additional details found for this contract.")

                    # Delete button
                    if st.button(f"Delete Contract ID {contract_id}", key=f"delete_{contract_id}"):
                        delete_contract(contract_id)

                    # Download button
                    file_path = os.path.join(CONTRACTS_DIR, f"contract_{contract_id}.docx")
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label=f"Download Contract {contract_id}",
                                data=file,
                                file_name=f"contract_{contract_id}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )

                    st.write("---")
            else:
                st.write("No contracts found in the database.")

    with st.expander("Statistics & Renewals"):
        generate_contract_statistics()
        display_renewal_alert()
