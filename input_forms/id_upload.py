import streamlit as st
import os
from ocr.ocr_processing import ocr_space_image, parse_id_details
from PIL import Image

UPLOAD_DIR = "uploads/"

def save_uploaded_file(uploaded_file):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    image = Image.open(uploaded_file)
    image.save(file_path)
    return file_path

def process_id_upload(user_type):
    # Determine user role based on contract type for consistent key naming
    if st.session_state.get('contract_type') == "Rental Contract":
        role_key = 'landlord' if user_type == 'buyer' else 'tenant'
    else:
        role_key = user_type  # 'buyer' or 'seller' for Sales Contract

    st.header(f"Upload or Enter ID Details for {role_key.capitalize()}")

    # Add a unique key for each `st.radio()` to differentiate them
    entry_method = st.radio("Choose input method:", ["Upload ID Image", "Manual Entry"], key=f"{role_key}_entry_method")

    # Initialize session state storage for the user type
    if f"{role_key}_details" not in st.session_state:
        st.session_state[f"{role_key}_details"] = {}

    if entry_method == "Upload ID Image":
        id_file = st.file_uploader(f"Choose an ID image for {role_key.capitalize()}", type=["jpg", "jpeg", "png"], key=f"{role_key}_uploader")
        if id_file:
            id_path = save_uploaded_file(id_file)
            ocr_text = ocr_space_image(id_path)
            if ocr_text:
                details = parse_id_details(ocr_text)
                if details:
                    # Display the details for user review and editing
                    for key in details:
                        details[key] = st.text_input(f"{key.replace('_', ' ').capitalize()} ({role_key.capitalize()})", details.get(key, ''), key=f"{role_key}_{key}")

                    # Save details to session state
                    if st.button(f"Save {role_key.capitalize()} Details", key=f"{role_key}_save_button"):
                        st.session_state[f"{role_key}_details"] = details
                        st.success(f"{role_key.capitalize()} details temporarily saved!")
                        st.write(st.session_state.get(f"{role_key}_details", 'No details available'))
                else:
                    st.warning("No recognizable details found.")
    else:  # Manual Entry
        st.subheader(f"Manual Entry for {role_key.capitalize()} ID Details")
        details = {
            'cnp': st.text_input(f"CNP ({role_key.capitalize()})", key=f"{role_key}_cnp"),
            'last_name': st.text_input(f"Last Name ({role_key.capitalize()})", key=f"{role_key}_last_name"),
            'first_name': st.text_input(f"First Name ({role_key.capitalize()})", key=f"{role_key}_first_name"),
            'nationality': st.text_input(f"Nationality ({role_key.capitalize()})", key=f"{role_key}_nationality"),
            'sex': st.text_input(f"Sex ({role_key.capitalize()})", key=f"{role_key}_sex"),
            'place_of_birth': st.text_input(f"Place of Birth ({role_key.capitalize()})", key=f"{role_key}_place_of_birth"),
            'address': st.text_input(f"Address ({role_key.capitalize()})", key=f"{role_key}_address"),
            'id_series': st.text_input(f"ID Series ({role_key.capitalize()})", key=f"{role_key}_id_series"),
            'issuing_authority': st.text_input(f"Issuing Authority ({role_key.capitalize()})", key=f"{role_key}_issuing_authority"),
            'issue_date': st.text_input(f"Issue Date ({role_key.capitalize()})", key=f"{role_key}_issue_date")
        }

        # Save details to session state
        if st.button(f"Save {role_key.capitalize()} Details", key=f"{role_key}_manual_save_button"):
            st.session_state[f"{role_key}_details"] = details
            st.success(f"{role_key.capitalize()} details temporarily saved!")
            st.write(st.session_state.get(f"{role_key}_details", 'No details available'))
