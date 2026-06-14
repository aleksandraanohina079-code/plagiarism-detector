import PyPDF2
import docx

def extract_text_from_file(file):
    """Извлекает текст из загруженного файла"""
    filename = file.name
    
    if filename.endswith('.txt'):
        return file.read().decode('utf-8')
    
    elif filename.endswith('.docx'):
        doc = docx.Document(file)
        return '\n'.join([p.text for p in doc.paragraphs])
    
    elif filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        return text
    
    return None
