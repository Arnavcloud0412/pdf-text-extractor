import streamlit as st
import pytesseract
from pdf2image import convert_from_path
import os

# Configure paths (Adjust for your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
poppler_path = r"E:\poppler-24.08.0\Library\bin"  # Change this to your Poppler bin path

def extract_text_from_pdf(pdf_path):
    """Extract text from a scanned PDF using OCR"""
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    text = ""

    for i, img in enumerate(images):
        page_text = pytesseract.image_to_string(img)
        text += f"--- Page {i+1} ---\n{page_text}\n"

    return text

# Streamlit UI
st.title("PDF Text Extractor (OCR)")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Processing")
    extracted_text = extract_text_from_pdf("temp.pdf")

    # Display extracted text
    st.subheader("Extracted Text:")
    st.text_area("Text Output", extracted_text, height=300)

    # Download button for extracted text
    st.download_button(
        label="📥 Download Extracted Text",
        data=extracted_text,
        file_name="extracted_text.txt",
        mime="text/plain",
    )

    # Cleanup temp file
    os.remove("temp.pdf")
