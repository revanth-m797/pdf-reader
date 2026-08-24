# Document Summary Assistant

A lightweight full-stack Python application that parses digital PDFs and applies OCR technology to physical images to output structured AI summaries.

### Tech Stack
* **Frontend/Backend:** Streamlit
* **Text Extraction:** PyPDF (Digital PDFs) & EasyOCR (Images/Scanned files)
* **Core GenAI Engine:** Google Gen AI SDK (`gemini-3.6-flash`)

### Local Setup
1. Clone this repository.
2. Install the necessary system dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root directory and insert your API credentials:
   ```text
   api_key=your_api_key
   ```
4. Run the web server application from your command terminal:
   ```bash
   streamlit run "app.py_file_path"
   ```
