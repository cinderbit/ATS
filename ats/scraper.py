"""Job requisition scraper - extracts job posting text from URLs."""

import re

import requests
from bs4 import BeautifulSoup

# Common selectors for job posting content across major job boards
JOB_CONTENT_SELECTORS = [
    # Workday-specific
    "[data-automation-id='jobPostingDescription']",
    ".job-description",
    ".jobDescriptionContent",
    # Generic job boards
    "#job-details",
    "#jobDescriptionText",
    ".job-detail-body",
    ".job-posting-content",
    ".description__text",
    ".show-more-less-html__markup",
    # Greenhouse
    "#content",
    ".job-post-content",
    # Lever
    ".posting-page",
    ".section-wrapper",
    # General fallbacks
    "[class*='job-description']",
    "[class*='jobDescription']",
    "[class*='job_description']",
    "[id*='job-description']",
    "[id*='jobDescription']",
    "article",
    "main",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def scrape_job_posting(url: str) -> str:
    """Scrape job posting text from a URL.

    Handles common job boards including Workday, Greenhouse, Lever,
    LinkedIn, Indeed, and generic career pages.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to fetch URL: {e}")

    soup = BeautifulSoup(response.text, "lxml")

    # Remove script, style, nav, footer elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    # Try each selector in priority order
    for selector in JOB_CONTENT_SELECTORS:
        elements = soup.select(selector)
        if elements:
            text = "\n\n".join(el.get_text(separator="\n", strip=True) for el in elements)
            cleaned = _clean_text(text)
            if len(cleaned) > 100:
                return cleaned

    # Fallback: extract body text
    body = soup.find("body")
    if body:
        text = body.get_text(separator="\n", strip=True)
        return _clean_text(text)

    raise ValueError("Could not extract job posting content from URL.")


def _clean_text(text: str) -> str:
    """Clean extracted text."""
    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)
    # Strip lines
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def parse_job_text(text: str) -> dict:
    """Parse job requisition text into structured sections."""
    section_patterns = {
        "title": r"(?i)^(?:job\s*title|position|role)\s*:?\s*(.+)",
        "company": r"(?i)^(?:company|organization|employer)\s*:?\s*(.+)",
        "location": r"(?i)^(?:location|office|based\s*in)\s*:?\s*(.+)",
        "description": r"(?i)^(?:description|about\s*(?:the\s*)?(?:role|position|job)|overview|summary)\s*:?",
        "responsibilities": r"(?i)^(?:responsibilities|duties|what\s*you(?:'ll|.will)\s*do|key\s*responsibilities|the\s*role)\s*:?",
        "requirements": r"(?i)^(?:requirements?|qualifications?|what\s*(?:we(?:'re)?\s*look(?:ing)?\s*for|you(?:'ll)?\s*(?:need|bring))|must\s*have|minimum\s*qualifications?|basic\s*qualifications?)\s*:?",
        "preferred": r"(?i)^(?:preferred|nice\s*to\s*have|bonus|desired|preferred\s*qualifications?|additional\s*qualifications?)\s*:?",
        "benefits": r"(?i)^(?:benefits?|perks?|what\s*we\s*offer|compensation)\s*:?",
        "education": r"(?i)^(?:education|degree|academic)\s*:?",
    }

    sections = {"full_text": text}
    lines = text.split("\n")
    current_section = "preamble"
    current_content = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            current_content.append("")
            continue

        matched = None
        for section_name, pattern in section_patterns.items():
            if re.match(pattern, stripped):
                matched = section_name
                break

        if matched:
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = matched
            current_content = []
            # Check if this line has inline content (e.g., "Job Title: Engineer")
            for pattern in section_patterns.values():
                m = re.match(pattern, stripped)
                if m and m.lastindex and m.group(1):
                    current_content.append(m.group(1).strip())
                    break
        else:
            current_content.append(stripped)

    if current_content:
        sections[current_section] = "\n".join(current_content).strip()

    return sections
