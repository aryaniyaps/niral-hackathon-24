import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_bytes


def pdf_bytes_to_text(pdf_bytes: bytes) -> str:
    # Open the PDF file from bytes
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""

    # Iterate through each page and extract text
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    pdf_document.close()
    return text


def pdf_ocr_to_text(pdf_bytes: bytes) -> str:
    # Open the PDF file from bytes
    pages = convert_from_bytes(pdf_bytes, dpi=600)

    # extract text
    text_data = ""
    for page in pages:
        text = pytesseract.image_to_string(page)
        text_data += text + "\n"
    return text_data
