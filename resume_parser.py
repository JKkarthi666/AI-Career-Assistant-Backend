import pdfplumber
from docx import Document
import re

SKILLS_DB = [
    "python",
    "django",
    "fastapi",
    "flask",
    "machine learning",
    "ai",
    "react",
    "nodejs",
    "sql",
    "mongodb",
    "aws",
    "docker",
    "kubernetes",
    "java",
    "javascript",
]

def extract_text_from_pdf(file_path):
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            found_skills.append(skill)

    return list(set(found_skills))


def parse_resume(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)

    else:
        raise Exception("Unsupported file")

    skills = extract_skills(text)

    return {
        "text": text,
        "skills": skills
    }