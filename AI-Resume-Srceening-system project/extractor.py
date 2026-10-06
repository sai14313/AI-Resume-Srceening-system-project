"""
Candidate Resume Information Extractor.
Extracts raw text, contact information, skills, education, and experience from PDF resumes using PyPDF and NLP regex rules.
"""

import io
import re
from typing import Dict, Any, List, Optional
import pypdf
from skills_db import ALL_SKILLS, SKILL_TAXONOMY, EDUCATION_KEYWORDS


def extract_text_from_pdf(pdf_source) -> str:
    """
    Extracts text from a PDF file path, BytesIO, or uploaded file buffer using pypdf.
    Handles multi-page documents, encoding, and potential PDF read errors.
    """
    try:
        if isinstance(pdf_source, (str, bytes)):
            if isinstance(pdf_source, bytes):
                pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_source))
            else:
                pdf_reader = pypdf.PdfReader(pdf_source)
        elif hasattr(pdf_source, "read"):
            # Streamlit UploadedFile or file-like object
            pdf_bytes = pdf_source.read()
            # Reset seek position if possible
            if hasattr(pdf_source, "seek"):
                pdf_source.seek(0)
            pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        else:
            raise ValueError("Unsupported PDF input type.")

        extracted_pages = []
        for i, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text() or ""
            extracted_pages.append(page_text)

        full_text = "\n".join(extracted_pages)
        return clean_text(full_text)
    except Exception as e:
        return f"[Error extracting PDF text: {str(e)}]"


def clean_text(text: str) -> str:
    """
    Cleans raw extracted text: removes extraneous control characters,
    normalizes whitespace, and repairs hyphenated line wraps.
    """
    if not text:
        return ""
    # Fix hyphenated words at line breaks (e.g. engi-\nneering -> engineering)
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    # Replace non-breaking spaces and unusual whitespace
    text = text.replace('\xa0', ' ').replace('\r\n', '\n').replace('\r', '\n')
    # Collapse multiple vertical newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Collapse multiple inline spaces
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()


def extract_email(text: str) -> str:
    """Extracts candidate email address."""
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else "Not Found"


def extract_phone(text: str) -> str:
    """Extracts candidate phone number."""
    # Matches common international, US, and regional phone formats
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{3,5}'
    candidates = re.findall(phone_pattern, text)
    for num in candidates:
        digits_only = re.sub(r'\D', '', num)
        if 9 <= len(digits_only) <= 15:
            return num.strip()
    return "Not Found"


def extract_links(text: str) -> Dict[str, str]:
    """Extracts LinkedIn, GitHub, or portfolio links."""
    links = {}
    linkedin_match = re.search(r'(https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+)', text, re.I)
    if linkedin_match:
        links["LinkedIn"] = linkedin_match.group(1)

    github_match = re.search(r'(https?://(?:www\.)?github\.com/[a-zA-Z0-9_-]+)', text, re.I)
    if github_match:
        links["GitHub"] = github_match.group(1)

    return links


def extract_name(text: str, fallback_filename: str = "") -> str:
    """
    Extracts candidate name from the top lines of the resume.
    Uses heuristic cleaning and fallbacks to sanitized filename.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    stop_tokens = ["resume", "curriculum", "vitae", "cv", "profile", "contact", "email", "phone", "experience", "education", "skills"]
    
    for line in lines[:8]:
        # Discard lines with email, URLs, or long text
        if "@" in line or "http" in line or "www" in line:
            continue
        cleaned = re.sub(r'[^a-zA-Z\s]', '', line).strip()
        words = cleaned.split()
        if 2 <= len(words) <= 4:
            if not any(token in cleaned.lower() for token in stop_tokens):
                return cleaned.title()

    # Fallback to filename
    if fallback_filename:
        name_part = re.sub(r'\.pdf$', '', fallback_filename, flags=re.I)
        name_part = re.sub(r'[-_]', ' ', name_part)
        words = [w for w in name_part.split() if w.lower() not in ["resume", "cv", "profile", "doc", "updated", "final"]]
        if words:
            return " ".join(words).title()

    return "Candidate"


def extract_skills(text: str) -> List[str]:
    """
    Extracts identified technical and professional skills from text
    by matching against the curated skills taxonomy with accurate boundaries.
    """
    if not text:
        return []
    
    lower_text = " " + text.lower() + " "
    found_skills = set()

    for skill in ALL_SKILLS:
        skill_lower = skill.lower()
        # Build safe regex boundary
        # If skill contains punctuation like c++, c#, .net, escape it
        escaped = re.escape(skill_lower)
        pattern = r'(?<![a-zA-Z0-9])' + escaped + r'(?![a-zA-Z0-9])'
        
        if re.search(pattern, lower_text):
            # Normalize casing for presentation
            found_skills.add(format_skill_name(skill))

    return sorted(list(found_skills))


def format_skill_name(skill: str) -> str:
    """Formats skill name nicely for display (e.g. 'nlp' -> 'NLP', 'aws' -> 'AWS')."""
    acronyms = {
        "nlp": "NLP", "llm": "LLM", "ai": "AI", "ml": "ML", "sql": "SQL",
        "aws": "AWS", "gcp": "GCP", "ci/cd": "CI/CD", "k8s": "K8s",
        "api": "API", "rest api": "REST API", "restful api": "RESTful API",
        "html": "HTML", "html5": "HTML5", "css": "CSS", "css3": "CSS3",
        "tf-idf": "TF-IDF", "tfidf": "TF-IDF", "bert": "BERT", "t-sql": "T-SQL",
        "tdd": "TDD", "etl": "ETL", "dbt": "dbt", "c++": "C++", "c#": "C#",
        "r": "R", "c": "C", "vue.js": "Vue.js", "node.js": "Node.js",
        "next.js": "Next.js", "react.js": "React.js", "scikit-learn": "Scikit-Learn",
        "sklearn": "Scikit-Learn", "pytorch": "PyTorch", "tensorflow": "TensorFlow"
    }
    skill_lower = skill.lower()
    if skill_lower in acronyms:
        return acronyms[skill_lower]
    return skill.title()


def extract_education(text: str) -> List[str]:
    """
    Identifies education entries, degrees, and academic institutions.
    """
    found_degrees = []
    lines = text.split("\n")
    
    for line in lines:
        line_clean = line.strip()
        line_lower = line_clean.lower()
        for kw in EDUCATION_KEYWORDS:
            # Word boundary check for degrees
            if re.search(r'\b' + re.escape(kw) + r'\b', line_lower):
                if len(line_clean) < 120 and line_clean not in found_degrees:
                    found_degrees.append(line_clean)
                    break

    if not found_degrees:
        # Check for generic mention
        if "computer science" in text.lower():
            found_degrees.append("B.S. / Degree in Computer Science (Mentioned)")
        elif "engineering" in text.lower():
            found_degrees.append("Degree in Engineering (Mentioned)")
        else:
            found_degrees.append("Education details available in resume text")

    return found_degrees[:4]


def extract_experience_summary(text: str) -> Dict[str, Any]:
    """
    Extracts estimated years of experience and notable career points.
    """
    years_pattern = r'(\b\d{1,2}(?:\.\d)?)\+?\s*(?:years?|yrs?)\b(?:\s*(?:of)?\s*(?:experience|exp))?'
    matches = re.findall(years_pattern, text, re.I)
    estimated_years = None
    if matches:
        numeric_vals = [float(m) for m in matches if float(m) <= 40]
        if numeric_vals:
            estimated_years = max(numeric_vals)

    # Search for year ranges e.g. 2018 - 2023, 2021 - Present
    date_ranges = re.findall(r'\b(20\d{2}|19\d{2})\s*(?:-|–|to)\s*(20\d{2}|present|current)\b', text, re.I)
    
    return {
        "estimated_years": estimated_years,
        "date_ranges_found": len(date_ranges),
        "has_senior_roles": bool(re.search(r'\b(lead|senior|principal|architect|manager|director)\b', text, re.I))
    }


def parse_resume(pdf_source, filename: str = "") -> Dict[str, Any]:
    """
    Master pipeline: parses PDF, extracts text, metadata, contacts,
    skills, education, and experience indicators into a unified dictionary.
    """
    raw_text = extract_text_from_pdf(pdf_source)
    is_error = raw_text.startswith("[Error") or len(raw_text.strip()) == 0
    
    if is_error:
        return {
            "filename": filename,
            "raw_text": raw_text,
            "name": extract_name("", fallback_filename=filename),
            "email": "N/A",
            "phone": "N/A",
            "links": {},
            "skills": [],
            "education": ["Extraction Failed or PDF is empty/scanned"],
            "experience": {"estimated_years": None, "date_ranges_found": 0, "has_senior_roles": False},
            "is_valid": False,
            "error_msg": raw_text if raw_text.startswith("[Error") else "PDF contains no selectable text."
        }

    name = extract_name(raw_text, fallback_filename=filename)
    email = extract_email(raw_text)
    phone = extract_phone(raw_text)
    links = extract_links(raw_text)
    skills = extract_skills(raw_text)
    education = extract_education(raw_text)
    experience = extract_experience_summary(raw_text)

    return {
        "filename": filename,
        "raw_text": raw_text,
        "name": name,
        "email": email,
        "phone": phone,
        "links": links,
        "skills": skills,
        "education": education,
        "experience": experience,
        "is_valid": True,
        "word_count": len(raw_text.split()),
        "char_count": len(raw_text)
    }
