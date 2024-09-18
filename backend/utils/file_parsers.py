from pdfminer.high_level import extract_text
import docx
import io

# Function to extract text from PDF files
def extract_text_from_pdf(file):
    # Convert SpooledTemporaryFile to BytesIO
    pdf_file = io.BytesIO(file.read())
    text = extract_text(pdf_file)
    return text

# Function to extract text from DOCX files
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])