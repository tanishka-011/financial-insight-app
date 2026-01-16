import pdfplumber
import re

SECTION_HEADERS = {
    "MD&A": ["management discussion", "management discussion and analysis"],
    "Market Risk": ["market risk"],
    "Risk Factors": ["risk factors"],
    "Financial Statements": ["financial statements"]
}

METRICS = ["revenue", "profit", "loss", "cash flow", "earnings", "ebitda"]
VALUE_PATTERN = re.compile(r"\$?\d+(?:\.\d+)?\s?(million|billion|mn|bn|crore|lakh)?", re.I)


def pdf_to_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def detect_sections(text):
    sections = {"Unknown": []}
    current = "Unknown"

    for line in text.split("\n"):
        for sec, keys in SECTION_HEADERS.items():
            if any(k in line.lower() for k in keys):
                current = sec
                sections.setdefault(current, [])
        sections[current].append(line)

    return {k: "\n".join(v) for k, v in sections.items() if v}


def extract_metrics(section_text, section_name):
    records = []
    for line in section_text.split("\n"):
        for metric in METRICS:
            if metric in line.lower():
                value = VALUE_PATTERN.search(line)
                records.append({
                    "metric": metric,
                    "value": value.group() if value else None,
                    "section": section_name,
                    "text": line.strip(),
                    "type": "quantitative" if value else "qualitative"
                })
                break
    return records


def financial_insight_pipeline(uploaded_file):
    text = pdf_to_text(uploaded_file)
    sections = detect_sections(text)

    metrics = []
    for sec, content in sections.items():
        metrics.extend(extract_metrics(content, sec))

    return {
        "company": "APPLE",
        "metrics": metrics
    }
