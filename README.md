# ATS Resume Scorer

A Workday-style ATS (Applicant Tracking System) resume scoring tool that analyzes your resume against any job posting and provides a detailed compatibility score.

## Features

- **Resume Parsing** — Supports PDF, DOCX, and TXT formats
- **Job Posting Input** — Paste text directly or provide a URL (scrapes Workday, Greenhouse, Lever, LinkedIn, Indeed, and more)
- **Workday-Style Scoring** — 8 weighted categories mirroring Workday's ATS ranking system
- **Detailed Feedback** — Actionable tips on missing skills, keywords, formatting issues
- **ATS Parse View** — See how an ATS reads your resume sections

## Scoring Categories

| Category | Weight | Description |
|----------|--------|-------------|
| Hard Skills | 25% | Technical skills, tools, and technologies |
| Keyword Relevance | 20% | TF-IDF similarity + keyword overlap |
| Experience | 15% | Years of experience alignment |
| Education | 15% | Degree level and field match |
| Job Title | 10% | Title relevance to the role |
| Certifications | 5% | Required certifications match |
| Soft Skills | 5% | Leadership, communication, etc. |
| Formatting | 5% | ATS-parseable structure |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download NLTK data (first run only)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Run the app
streamlit run app.py
```

## Project Structure

```
ATS/
├── app.py                 # Streamlit web UI
├── requirements.txt       # Python dependencies
├── ats/
│   ├── __init__.py
│   ├── parser.py          # Resume parsing (PDF/DOCX/TXT) + section detection
│   ├── scraper.py         # Job posting URL scraper
│   ├── extractor.py       # Entity extraction (skills, education, experience)
│   └── scorer.py          # Workday-style weighted scoring engine
└── README.md
```

## How It Works

1. **Upload** your resume (PDF, DOCX, or TXT)
2. **Provide** a job posting (paste text or enter URL)
3. **Get** a detailed ATS compatibility score with category breakdown
4. **Review** matched/missing skills, keywords, and actionable feedback
5. **Optimize** your resume based on the recommendations
