import re
import pymupdf
from docx import Document


def extract_text_from_pdf(file_path):
    text = ""

    try:
        document = pymupdf.open(file_path)

        for page in document:
            text += page.get_text()

        document.close()

    except Exception as e:
        print("PDF extraction error:", e)

    return text


def extract_text_from_docx(file_path):
    text = ""

    try:
        document = Document(file_path)

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

    except Exception as e:
        print("DOCX extraction error:", e)

    return text


def extract_text(file_path):

    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)

    return ""


def clean_text(text):

    text = text.replace("\x00", " ")

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return "Not detected"


def extract_phone(text):

    patterns = [
        r"\+91[-\s]?\d{10}",
        r"\b\d{10}\b",
        r"\+\d{1,3}[-\s]?\d{7,12}"
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group(0)

    return "Not detected"


def extract_name(text):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if not lines:
        return "Not detected"

    for line in lines[:5]:

        if (
            len(line.split()) >= 2
            and len(line) < 60
            and not any(char.isdigit() for char in line)
            and "@" not in line
        ):
            return line

    return lines[0]


def extract_education(text):

    education_keywords = [
        "b.tech",
        "btech",
        "b.e",
        "bachelor",
        "m.tech",
        "mtech",
        "master",
        "mca",
        "bca",
        "b.sc",
        "m.sc",
        "mba",
        "phd",
        "computer science",
        "engineering"
    ]

    text_lower = text.lower()

    found = []

    for keyword in education_keywords:

        if keyword in text_lower:
            found.append(keyword.upper())

    return list(dict.fromkeys(found))


def extract_experience(text):

    pattern = r"\b(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\b"

    matches = re.findall(
        pattern,
        text.lower()
    )

    if not matches:
        return "Not detected"

    return ", ".join(
        f"{match} years"
        for match in matches
    )


def extract_resume_information(text):

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }