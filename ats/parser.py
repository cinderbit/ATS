"""Resume and document parsing utilities."""

import io
import re
from pathlib import Path

import docx
import pdfplumber


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Extract text from a plain text file."""
    return file_bytes.decode("utf-8", errors="replace")


def parse_resume(file_bytes: bytes, filename: str) -> str:
    """Parse resume file and return extracted text."""
    ext = Path(filename).suffix.lower()
    extractors = {
        ".pdf": extract_text_from_pdf,
        ".docx": extract_text_from_docx,
        ".txt": extract_text_from_txt,
    }
    extractor = extractors.get(ext)
    if not extractor:
        raise ValueError(f"Unsupported file format: {ext}. Use PDF, DOCX, or TXT.")
    return extractor(file_bytes)


def parse_resume_sections(text: str) -> dict:
    """Parse resume text into structured sections (Workday-style section detection).

    Workday ATS parses resumes into specific sections. This mimics that behavior
    by identifying common resume section headers.
    """
    section_patterns = {
        "contact": r"(?i)^(?:contact\s*(?:info(?:rmation)?)?|personal\s*(?:info(?:rmation)?|details))$",
        "summary": r"(?i)^(?:summary|professional\s*summary|executive\s*summary|profile|about\s*me|objective|career\s*objective)$",
        "experience": r"(?i)^(?:experience|work\s*experience|professional\s*experience|employment\s*(?:history)?|work\s*history|career\s*history)$",
        "education": r"(?i)^(?:education|academic\s*(?:background|qualifications?)|educational\s*background|degrees?)$",
        "skills": r"(?i)^(?:skills|technical\s*skills|core\s*(?:competenc(?:ies|e)|skills)|key\s*skills|areas?\s*of\s*expertise|proficienc(?:ies|y)|technologies)$",
        "certifications": r"(?i)^(?:certifications?|licenses?\s*(?:&|and)?\s*certifications?|professional\s*certifications?|credentials?)$",
        "projects": r"(?i)^(?:projects?|key\s*projects?|notable\s*projects?)$",
        "awards": r"(?i)^(?:awards?|honors?|achievements?|awards?\s*(?:&|and)?\s*honors?)$",
        "publications": r"(?i)^(?:publications?|research|papers?)$",
        "volunteer": r"(?i)^(?:volunteer(?:ing)?|community\s*(?:service|involvement))$",
        "languages": r"(?i)^(?:languages?|language\s*skills?)$",
    }

    lines = text.split("\n")
    sections = {}
    current_section = "header"
    current_content = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            current_content.append("")
            continue

        matched_section = None
        for section_name, pattern in section_patterns.items():
            if re.match(pattern, stripped):
                matched_section = section_name
                break

        if matched_section:
            sections[current_section] = "\n".join(current_content).strip()
            current_section = matched_section
            current_content = []
        else:
            current_content.append(stripped)

    sections[current_section] = "\n".join(current_content).strip()
    return sections
