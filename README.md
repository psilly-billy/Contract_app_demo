# Contract Management Application

## Overview
The Contract Management Application is a comprehensive tool designed to streamline the creation, management, and storage of rental and sales contracts. The app supports automated contract generation from user input, previewing contracts, storing them in a local database, viewing detailed contract data, and managing contract records. It also offers contract statistics and alerts for contracts that are nearing their expiry dates.

## Key Features
- **Automated Contract Generation**: Generate rental and sales contracts using pre-defined templates with dynamic placeholders replaced by user-provided data.
- **ID Details Management**: Upload or manually enter user ID details for landlords, tenants, buyers, and sellers.
- **Contract Preview and Download**: Preview the generated contract before saving or downloading a local copy.
- **Database Integration**: Store contract details and user data in an SQLite database for easy retrieval and management.
- **Contract Viewing and Deletion**: View existing contracts, download copies, or delete records both locally and from the database.
- **Statistics Dashboard**: Display graphs showing contract statistics by type.
- **Renewal Alerts**: Notify users about contracts that are close to their expiry dates.

## Technologies Used
- **Programming Language**: Python
- **Web Framework**: Streamlit for a responsive and interactive user interface
- **Database**: SQLite for storing user and contract details
- **Document Processing**: Python-docx for handling Word document templates
- **Image Processing**: PIL (Pillow) for handling image uploads
- **OCR Integration**: External OCR processing for extracting details from ID images
- **Data Visualization**: Matplotlib and Pandas for generating graphs and statistics

## Project Structure
```
contract_management_app/
|-- data/
|   |-- templates/
|       |-- contract_rent.docx
|       |-- contract_sale.docx
|-- contracts_files/
|-- input_forms/
|   |-- contract_selection.py
|   |-- id_upload.py
|   |-- contract_details.py
|   |-- contract_generation.py
|   |-- view_contracts.py
|   |-- form_processing.py
|-- contracts_app.db
|-- main.py
|-- README.md
```

## How to Run the Application
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd contract_management_app
   ```

2. **Install Dependencies**:
   Ensure you have Python installed and then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App**:
   ```bash
   streamlit run main.py
   ```

4. **Access the Application**:
   Open your web browser and navigate to `http://localhost:8501`.

## Next Steps for Improvement
- **User Authentication**: Implement user authentication to restrict access and secure user data.
- **Enhanced OCR Capabilities**: Integrate more robust OCR solutions to handle various ID formats.
- **Advanced Search and Filter Options**: Allow users to filter and search contracts based on various criteria.
- **Contract Editing Feature**: Provide the ability to modify existing contracts before final submission.
- **Cloud Integration**: Store contracts and data in cloud storage (e.g., AWS S3, Google Drive) for better accessibility.
- **Email Notifications**: Send automatic notifications for contracts nearing their expiry or other important events.
- **Multi-language Support**: Support contract generation in multiple languages for broader usage.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your proposed changes.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Contact
For questions, suggestions, or collaboration, please contact m.iurea@gmail.com.

