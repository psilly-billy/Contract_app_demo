import requests
import os
import re
import json
import shutil

# Base URL for the OCR.space API
OCR_URL = 'https://api.ocr.space/parse/image'

# Directory to store uploaded ID images
UPLOAD_DIR = "uploads/"

def ocr_space_image(image_path: str, is_url: bool = False) -> str:
    """
    Performs OCR on an image using the OCR.space API.
    
    Args:
    - image_path: File path to the image (or URL if is_url is True).
    - is_url: Set to True if `image_path` is a URL, otherwise False for local file.
    
    Returns:
    - OCR text output as a string.
    """
    
    os.environ["OCR_API_KEY"] = "K83827672188957"  # Replace with your API key

    api_key = os.getenv("OCR_API_KEY")
    if not api_key:
        print("Error: API key is missing.")
        return ""

    # Set up parameters for API request
    payload = {
        'apikey': api_key,
        'OCREngine': '2'  # OCR Engine 2 for better accuracy
    }
    
    # Choose file or URL based on is_url
    files = {'file': open(image_path, 'rb')} if not is_url else None
    if is_url:
        payload['url'] = image_path

    # Make a POST request to OCR.space API
    response = requests.post(OCR_URL, data=payload, files=files if files else None)

    # Check for successful response
    if response.status_code == 200:
        result = response.json()
        if result['IsErroredOnProcessing']:
            print("Error in OCR processing:", result['ErrorMessage'][0])
            return ""
        else:
            parsed_text = result['ParsedResults'][0]['ParsedText']
            return parsed_text
    else:
        print("Error:", response.status_code, response.text)
        return ""

import re

import re

def parse_id_details(ocr_text: str) -> dict:
    """
    Parse OCR output to extract specific fields from the ID using regex and context-based parsing.
    """
    extracted_data = {}

    # Extract CNP using regex
    cnp_match = re.search(r"\bCNP\s*[:]*\s*(\d{13})", ocr_text, re.IGNORECASE)
    if cnp_match:
        extracted_data['cnp'] = cnp_match.group(1).strip()
        print(f"Debug: Matched 'cnp' -> {extracted_data['cnp']}")

    # Extract last name and first name using regex
    last_name_match = re.search(r"Nume/Nom/Last name\s*\n([A-Z]+)", ocr_text, re.IGNORECASE)
    if last_name_match:
        extracted_data['last_name'] = last_name_match.group(1).strip()
        print(f"Debug: Matched 'last_name' -> {extracted_data['last_name']}")

    first_name_match = re.search(r"Prenume/Prenom/First name\s*\n([A-Z\-]+)", ocr_text, re.IGNORECASE)
    if first_name_match:
        extracted_data['first_name'] = first_name_match.group(1).strip()
        print(f"Debug: Matched 'first_name' -> {extracted_data['first_name']}")

    # Extract nationality using context-based parsing
    extracted_data['nationality'] = extract_text_between_markers(ocr_text, "Nationality", "Sex/Sexe/Sex")
    if extracted_data['nationality']:
        extracted_data['nationality'] = extracted_data['nationality'].replace('\n', ' ').strip()
        print(f"Debug: Matched 'nationality' -> {extracted_data['nationality']}")

    # Extract sex using context-based parsing
    extracted_data['sex'] = extract_text_between_markers(ocr_text, "Sex/Sexe/Sex", "Cetatenie")
    if extracted_data['sex']:
        extracted_data['sex'] = extracted_data['sex'].strip()
        print(f"Debug: Matched 'sex' -> {extracted_data['sex']}")

    # Extract place of birth using context-based parsing
    extracted_data['place_of_birth'] = extract_text_between_markers(ocr_text, "Loc nastere/Lieu de naissance/Place of birth", "Domiciliu/Adresse/Address")
    if extracted_data['place_of_birth']:
        extracted_data['place_of_birth'] = extracted_data['place_of_birth'].replace('\n', ' ').strip()
        print(f"Debug: Matched 'place_of_birth' -> {extracted_data['place_of_birth']}")

    # Extract address using regex (can remain as it is)
    address_match = re.search(r"Domiciliu/Adresse/Address\s*\n([A-Za-z\s\(\).,0-9]+)", ocr_text, re.IGNORECASE)
    if address_match:
        extracted_data['address'] = address_match.group(1).strip().replace('\n', ' ')
        print(f"Debug: Matched 'address' -> {extracted_data['address']}")

    # Extract ID series using regex (already robust)
    id_series_match = re.search(r"SERIA\s+([A-Z]{2})\s+NR\s+(\d+)", ocr_text, re.IGNORECASE)
    if id_series_match:
        extracted_data['id_series'] = f"{id_series_match.group(1)} {id_series_match.group(2)}"
        print(f"Debug: Matched 'id_series' -> {extracted_data['id_series']}")

    # Extract issuing authority using context-based parsing
    extracted_data['issuing_authority'] = extract_text_between_markers(ocr_text, "Validity", "IDROU")
    if extracted_data['issuing_authority']:
        extracted_data['issuing_authority'] = extracted_data['issuing_authority'].replace('\n', ' ').strip()
        print(f"Debug: Matched 'issuing_authority' -> {extracted_data['issuing_authority']}")

    # Extract issue date using regex
    issue_date_match = re.search(r"(\d{2}\.\d{2}\.\d{2})", ocr_text)
    if issue_date_match:
        extracted_data['issue_date'] = issue_date_match.group(1).strip()
        print(f"Debug: Matched 'issue_date' -> {extracted_data['issue_date']}")

    return extracted_data

def extract_text_between_markers(text: str, start_marker: str, end_marker: str) -> str:
    """
    Extracts the text between two specified markers.
    """
    start_index = text.find(start_marker)
    end_index = text.find(end_marker, start_index)
    if start_index != -1 and end_index != -1:
        start_index += len(start_marker)
        return text[start_index:end_index].strip()
    return None





def handle_image_upload(image_path: str) -> str:
    """
    Copies the uploaded image file to the UPLOAD_DIR if not already there and returns the file path.
    """
    # Ensure the uploads directory exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    # Define the destination path
    destination_path = os.path.join(UPLOAD_DIR, os.path.basename(image_path))
    
    # Only copy if the file is not already in the destination path
    if os.path.abspath(image_path) != os.path.abspath(destination_path):
        shutil.copy(image_path, destination_path)
        print(f"Image copied to {destination_path}")
    else:
        print(f"Image already exists at {destination_path}")
    
    return destination_path

def save_extracted_data(extracted_data: dict, filename: str = "extracted_data.json") -> None:
    """
    Save the extracted ID details to a JSON file with UTF-8 encoding.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4, ensure_ascii=False)
    print(f"Extracted data saved to {filename}")


# Example usage
if __name__ == "__main__":
    # Simulate user uploading an image file
    uploaded_file = "uploads/image.jpg"  # Replace with the actual path to the uploaded image
    
    # Save the uploaded image to the UPLOAD_DIR
    image_path = handle_image_upload(uploaded_file)
    
    # Perform OCR on the uploaded image
    ocr_text = ocr_space_image(image_path)
    
    if ocr_text:
        print("OCR Result:\n", ocr_text)

        # Parse the details from OCR output
        extracted_details = parse_id_details(ocr_text)
        print("Extracted ID Details:", extracted_details)

        # Save the extracted details to a JSON file
        save_extracted_data(extracted_details)
