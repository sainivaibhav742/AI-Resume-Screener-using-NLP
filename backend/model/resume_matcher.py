import docx2txt
import fitz  # PyMuPDF
import os

# Example skills/keywords
TARGET_KEYWORDS = [
    "python", "machine learning", "deep learning", "data science",
    "flask", "django", "nlp", "react", "node.js", "sql", "pandas",
    "numpy", "html", "css", "javascript", "git", "api"
]

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def calculate_score(text):
    text_lower = text.lower()
    matches = [kw for kw in TARGET_KEYWORDS if kw in text_lower]
    score = len(matches) / len(TARGET_KEYWORDS) * 100
    return round(score, 2), matches

def match_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.docx':
        text = docx2txt.process(file_path)
    elif ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format")

    score, matched_keywords = calculate_score(text)

    status = "Strong Match" if score >= 70 else "Moderate Match" if score >= 40 else "Needs Improvement"

    return {
        "file_name": os.path.basename(file_path),
        "score": score,
        "status": status,
        "keywords_matched": matched_keywords,
        "preview": text[:500]
    }
