import streamlit as st
import os
import json
from input_forms.form_processing import (
    insert_id_details, insert_property_details, 
    get_id_details, get_property_details
)

from ocr.ocr_processing import ocr_space_image, parse_id_details
from PIL import Image
from input_forms.contract_generation import generate_contract

UPLOAD_DIR = "uploads/"

def save_uploaded_file(uploaded_file, max_size_kb=1024):
    """
    Save the uploaded file to the uploads directory, resize it if necessary, and return the file path.
    Args:
    - uploaded_file: The uploaded file object.
    - max_size_kb: The maximum allowed file size in KB.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    image = Image.open(uploaded_file)

    # Save the image and check its size
    image.save(file_path)
    file_size_kb = os.path.getsize(file_path) / 1024  # Size in KB

    # If the image is larger than max_size_kb, resize it
    if file_size_kb > max_size_kb:
        st.write(f"Original image size: {file_size_kb:.2f} KB, resizing...")
        image = resize_image(image, max_size_kb)
        image.save(file_path, optimize=True, quality=85)
        st.write(f"Resized image saved at {file_path}")

    return file_path

def resize_image(image, max_size_kb, step=5):
    """
    Resize the image to reduce its file size while maintaining a balance between quality and size.
    Args:
    - image: The PIL Image object.
    - max_size_kb: The maximum allowed file size in KB.
    - step: The decrement step for quality reduction.
    """
    quality = 95  # Start with a high quality
    temp_path = os.path.join(UPLOAD_DIR, "temp_resized.jpg")

    # Initial resizing of the image to limit dimensions
    image.thumbnail((800, 800))  # Limit max width and height
    image.save(temp_path, optimize=True, quality=quality)

    file_size_kb = os.path.getsize(temp_path) / 1024  # Size in KB

    # Further reduce quality until the file size is under the max size
    while file_size_kb > max_size_kb and quality > 10:
        quality -= 5
        image.save(temp_path, optimize=True, quality=quality)
        file_size_kb = os.path.getsize(temp_path) / 1024  # Size in KB

    # Load the final resized image
    with Image.open(temp_path) as resized_image:
        resized_image_copy = resized_image.copy()

    os.remove(temp_path)  # Clean up the temp file

    return resized_image_copy

def process_and_display_ocr(image_path, user_type):
    ocr_text = ocr_space_image(image_path)
    if ocr_text:
        details = parse_id_details(ocr_text)
        
        if details:
            st.write(f"Review and edit {user_type.capitalize()} details:")
            details['cnp'] = st.text_input(f"CNP ({user_type.capitalize()})", details.get('cnp', ''))
            details['last_name'] = st.text_input(f"Last Name ({user_type.capitalize()})", details.get('last_name', ''))
            details['first_name'] = st.text_input(f"First Name ({user_type.capitalize()})", details.get('first_name', ''))
            details['nationality'] = st.text_input(f"Nationality ({user_type.capitalize()})", details.get('nationality', ''))
            details['sex'] = st.text_input(f"Sex ({user_type.capitalize()})", details.get('sex', ''))
            details['place_of_birth'] = st.text_input(f"Place of Birth ({user_type.capitalize()})", details.get('place_of_birth', ''))
            details['address'] = st.text_input(f"Address ({user_type.capitalize()})", details.get('address', ''))
            details['id_series'] = st.text_input(f"ID Series ({user_type.capitalize()})", details.get('id_series', ''))
            details['issuing_authority'] = st.text_input(f"Issuing Authority ({user_type.capitalize()})", details.get('issuing_authority', ''))
            details['issue_date'] = st.text_input(f"Issue Date ({user_type.capitalize()})", details.get('issue_date', ''))

            if st.button(f"Save {user_type.capitalize()} Details"):
                insert_id_details(user_id=1, id_data=details, person_type=user_type)  # Replace with appropriate user ID logic
                st.success(f"{user_type.capitalize()} details saved!")
        else:
            st.warning("No recognizable details found. Please check the OCR output.")
    else:
        st.error("OCR failed to extract text from the image. Please try again with a clearer image.")

def load_placeholders(contract_type):
    """
    Load placeholder JSON based on the selected contract type.
    """
    if contract_type == "Rental Contract":
        json_path = "placeholders_json/contract_rent.json"
    elif contract_type == "Sales Contract":
        json_path = "placeholders_json/contract_sale.json"
    else:
        return None

    with open(json_path, "r", encoding="utf-8") as file:
        placeholders = json.load(file)
    return placeholders

def run_streamlit_app():
    st.sidebar.title("Navigation")
    menu_options = ["Select Contract Type", "Upload ID Details", "Property Details", "Generate Contract"]
    selected_option = st.sidebar.radio("Go to", menu_options)

    if selected_option == "Select Contract Type":
        st.title("Select the Type of Contract")
        contract_type = st.selectbox("Select the type of contract:", ["Rental Contract", "Sales Contract"])
        st.session_state['contract_type'] = contract_type
        st.write(f"You selected: {contract_type}")

    elif selected_option == "Upload ID Details":
        st.title("Upload ID Images")
        st.header("Upload ID for Buyer/Renter")
        buyer_id_file = st.file_uploader("Choose an ID image for Buyer/Renter", type=["jpg", "jpeg", "png"])
        if buyer_id_file:
            buyer_id_path = save_uploaded_file(buyer_id_file)
            process_and_display_ocr(buyer_id_path, 'buyer')

        st.header("Upload ID for Seller/Owner")
        seller_id_file = st.file_uploader("Choose an ID image for Seller/Owner", type=["jpg", "jpeg", "png"])
        if seller_id_file:
            seller_id_path = save_uploaded_file(seller_id_file)
            process_and_display_ocr(seller_id_path, 'seller')

    elif selected_option == "Property Details":
        st.title("Enter Property Details")
        contract_type = st.session_state.get('contract_type', None)
        
        if not contract_type:
            st.warning("Please select the contract type in the 'Select Contract Type' section first.")
        else:
            placeholders = load_placeholders(contract_type)
            if placeholders and "property_details" in placeholders:
                for field, placeholder in placeholders["property_details"].items():
                    st.text_input(field.replace('_', ' ').capitalize(), placeholder)

            if st.button("Save Property Details"):
                property_data = {key: st.session_state[key] for key in placeholders["property_details"].keys()}
                insert_property_details(user_id=1, property_data=property_data)
                st.success("Property details saved!")

    elif selected_option == "Generate Contract":
        st.title("Generate Your Contract")
        contract_type = st.session_state.get('contract_type', None)
        if not contract_type:
            st.warning("Please select the type of contract in the 'Select Contract Type' section first.")
        else:
            if st.button("Generate Contract"):
                contract_path = generate_contract(user_id=1, contract_type=contract_type)
                if contract_path:
                    st.success("Contract generated successfully!")
                    st.download_button(
                        label="Download Contract",
                        data=open(contract_path, "rb").read(),
                        file_name=os.path.basename(contract_path),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )