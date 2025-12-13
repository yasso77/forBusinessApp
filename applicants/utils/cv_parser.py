import re
import pdfplumber
from docx import Document

# =========================
# Arabic Normalization Regex
# =========================
ARABIC_DIACRITICS = re.compile(r'[\u0617-\u061A\u064B-\u0652]')

def normalize_text(text: str) -> str:
    """
    Normalize Arabic & English text for search
    """
    if not text:
        return ""

    # Remove Arabic diacritics
    text = re.sub(ARABIC_DIACRITICS, '', text)

    # Normalize Arabic letters
    replacements = {
        'أ': 'ا',
        'إ': 'ا',
        'آ': 'ا',
        'ى': 'ي',
        'ؤ': 'و',
        'ئ': 'ي',
        'ة': 'ه',
    }
    for src, target in replacements.items():
        text = text.replace(src, target)

    # Normalize English
    text = text.lower()

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# =========================
# CV Text Extraction
# =========================
def extract_pdf_text(file_path: str) -> str:
    """
    Extract text from PDF CV
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()


def extract_docx_text(file_path: str) -> str:
    """
    Extract text from Word CV
    """
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs).strip()


# =========================
# Language Detection
# =========================
def detect_cv_language(text: str) -> str:
    """
    Detect if CV is Arabic, English or Mixed
    """
    has_arabic = bool(re.search(r'[\u0600-\u06FF]', text))
    has_english = bool(re.search(r'[A-Za-z]', text))

    if has_arabic and has_english:
        return "Mixed"
    if has_arabic:
        return "Arabic"
    if has_english:
        return "English"
    return "Unknown"


import re

# =========================
# Email Extraction
# =========================
def extract_email(text: str):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None


# =========================
# Mobile Extraction (Egypt + Intl)
# =========================
def extract_mobile(text: str):
    patterns = [
        r'\+?\d{1,3}[\s\-]?\d{3,4}[\s\-]?\d{3,4}[\s\-]?\d{3,4}',
        r'\b01[0-2,5]\d{8}\b'  # Egypt
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0).replace(" ", "")
    return None


# =========================
# Gender Detection (Simple Heuristic)
# =========================
def extract_gender(text: str):
    text = text.lower()
    if re.search(r'\b(male|man|ذكر)\b', text):
        return "Male"
    if re.search(r'\b(female|woman|أنثى)\b', text):
        return "Female"
    return None


# =========================
# Name Extraction (First Line Heuristic)
# =========================
def extract_full_name(text: str):
    lines = text.splitlines()
    for line in lines[:5]:
        clean = line.strip()
        if 2 <= len(clean.split()) <= 4 and len(clean) < 50:
            return clean
    return None


# =========================
# Job Title Extraction
# =========================
def extract_job_title(text: str):
    patterns = [
        r'job title[:\-]?\s*(.+)',
        r'position[:\-]?\s*(.+)',
        r'current position[:\-]?\s*(.+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).split('\n')[0].strip()
    return None


# =========================
# Years of Experience
# =========================
def extract_years_of_experience(text: str):
    match = re.search(r'(\d{1,2})\+?\s+years? of experience', text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None


# =========================
# Skills Extraction
# =========================
def extract_skills(text: str):
    skills_section = re.search(
        r'(skills|core skills|technical skills)(.*?)(education|experience)',
        text,
        re.IGNORECASE | re.DOTALL
    )
    if not skills_section:
        return None

    raw = skills_section.group(2)
    skills = re.split(r'[•,\n\-]', raw)
    skills = [s.strip() for s in skills if len(s.strip()) > 2]
    return ", ".join(skills[:30]) if skills else None


# =========================
# Spoken Languages
# =========================
def extract_languages(text: str):
    match = re.search(
        r'(languages)(.*?)(education|experience|skills)',
        text,
        re.IGNORECASE | re.DOTALL
    )
    if match:
        langs = re.split(r'[•,\n\-]', match.group(2))
        langs = [l.strip() for l in langs if len(l.strip()) > 2]
        return ", ".join(langs)
    return None


# =========================
# Education Level
# =========================
def extract_education_level(text: str):
    if re.search(r'bachelor|b\.sc|bsc|degree', text, re.IGNORECASE):
        return "Bachelor"
    if re.search(r'master|m\.sc|msc', text, re.IGNORECASE):
        return "Master"
    if re.search(r'phd|doctorate', text, re.IGNORECASE):
        return "PhD"
    if re.search(r'diploma', text, re.IGNORECASE):
        return "Diploma"
    return None


# =========================
# Last University
# =========================
def extract_university(text: str):
    match = re.search(
        r'(university|institute|college)\s+(.*)',
        text,
        re.IGNORECASE
    )
    if match:
        return match.group(2).split('\n')[0].strip()
    return None


# =========================
# Country & City
# =========================
def extract_location(text: str):
    city = None
    country = None

    match = re.search(r'location[:\-]?\s*(.+)', text, re.IGNORECASE)
    if match:
        parts = match.group(1).split(',')
        city = parts[0].strip()
        if len(parts) > 1:
            country = parts[1].strip()

    return city, country


# =========================
# Target Country (Heuristic)
# =========================
def extract_target_country(text: str):
    if re.search(r'(uae|dubai)', text, re.IGNORECASE):
        return "UAE"
    if re.search(r'(saudi|ksa)', text, re.IGNORECASE):
        return "Saudi Arabia"
    if re.search(r'(qatar)', text, re.IGNORECASE):
        return "Qatar"
    if re.search(r'(germany)', text, re.IGNORECASE):
        return "Germany"
    return None


# =========================
# Availability
# =========================
def extract_availability(text: str):
    if re.search(r'immediately|available now', text, re.IGNORECASE):
        return "Immediate"
    if re.search(r'notice period', text, re.IGNORECASE):
        return "Notice Period"
    return None


