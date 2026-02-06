from pypdf import PdfReader
from pathlib import Path
from typing import List, Dict


# pdf loader
def load_pdf(file_path: str)-> List[Dict]:
    path = Path(file_path)

    # validate if exists
    if not path.exists:
        raise FileNotFoundError(f"file not found {file_path}")
    
    # validate file extension
    if path.suffix.lower != ".pdf":
        raise ValueError("file must be a PDF!!!")
    
    content = []


    try:
        reader = PdfReader(file_path)

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            
            content.append({
                "page": page_num,
                "text": text.strip() if text else ""
            })
    
    except Exception as e:
        raise RuntimeError(f"error readign file: {e}")
    
    return content


# text loader
def load_text(file_path:str)-> List[Dict]:
    path = Path(file_path)

    # validate if exists
    if not path.exists():
        raise FileNotFoundError(f"file not found {file_path}")
    
    # validate file extension
    if path.suffix.lower() != ".txt":
        raise ValueError("file must be a txt!!!")
    

    try:
        text = path.read_text(encoding="utf-8")

        return [{
            "page": 1,
            "text": text.strip()
        }]

    except Exception as e:
        raise RuntimeError(f"Error reading text file: {e}")