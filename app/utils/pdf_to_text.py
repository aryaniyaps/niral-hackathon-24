from io import BytesIO

import fitz  # PyMuPDF


def pdf_bytes_to_text(pdf_bytes: BytesIO) -> str:
    # Open the PDF file from bytes
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""

    # Iterate through each page and extract text
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    pdf_document.close()
    return text


def pdf_ocr_to_text(pdf_bytes: BytesIO) -> str:
    return ""
