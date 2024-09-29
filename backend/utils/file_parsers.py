import PyPDF2
import docx
import io

def extract_text_from_pdf(file_contents):
    # Wrap the byte content in a BytesIO object to enable seek operations
    pdf_file = io.BytesIO(file_contents)
    reader = PyPDF2.PdfReader(pdf_file)

    text = ''
    for page in reader.pages:
        text += page.extract_text()

    
    return text

def extract_text_from_docx(file_contents):
    doc = docx.Document(file_contents)
    return '\n'.join([para.text for para in doc.paragraphs])
