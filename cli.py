#!/usr/bin/env python3
"""ATS Resume Scorer - CLI Interface.

Usage:
    python cli.py --resume path/to/resume.pdf --job-url "https://..."
    python cli.py --resume path/to/resume.pdf --job-text path/to/job.txt
    python cli.py --resume path/to/resume.pdf  (prompts for job text via stdin)
"""

import argparse
import sys
from pathlib import Path

from ats.parser import parse_resume
from ats.scorer import SCORING_WEIGHTS, score_resume
from ats.scraper import scrape_job_posting


# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CYAN = "\033[96m"


def color_score(score: float) -> str:
    if score >= 75:
        return f"{GREEN}{score:.1f}{RESET}"
    elif score >= 50:
        return f"{YELLOW}{score:.1f}{RESET}"
    else:
        return f"{RED}{score:.1f}{RESET}"


def bar(score: float, width: int = 30) -> str:
    filled = int(score / 100 * width)
    empty = width - filled
    if score >= 75:
        color = GREEN
    elif score >= 50:
        color = YELLOW
    else:
        color = RED
    return f"{color}{'█' * filled}{'░' * empty}{RESET}"


def print_results(results: dict):
    overall = results["overall_score"]
    grade = results["grade"]
    scores = results["category_scores"]
    details = results["details"]
    feedback = results["feedback"]

    # Header
    print()
    print(f"{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}           ATS RESUME SCORE REPORT{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")
    print()

    # Overall score
    if overall >= 75:
        tier = f"{GREEN}Strong Match{RESET}"
    elif overall >= 55:
        tier = f"{YELLOW}Moderate Match{RESET}"
    else:
        tier = f"{RED}Needs Improvement{RESET}"

    print(f"  {BOLD}Overall Score:{RESET}  {color_score(overall)} / 100  ({BOLD}{grade}{RESET})")
    print(f"  {BOLD}Verdict:{RESET}        {tier}")
    print()

    # Category breakdown
    print(f"{BOLD}{'─' * 60}{RESET}")
    print(f"{BOLD}  CATEGORY BREAKDOWN{RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}")

    labels = {
        "hard_skills": "Hard Skills",
        "keyword_relevance": "Keywords",
        "experience": "Experience",
        "education": "Education",
        "job_title": "Job Title",
        "certifications": "Certifications",
        "soft_skills": "Soft Skills",
        "formatting": "Formatting",
    }

    for key, label in labels.items():
        weight = SCORING_WEIGHTS[key]
        score_val = scores[key]
        weighted = score_val * weight
        print(f"  {label:18s} {bar(score_val)} {color_score(score_val):>20s}  {DIM}(x{weight:.0%} = {weighted:.1f}){RESET}")

    print()

    # Skills detail
    hs = details["hard_skills"]
    matched = hs.get("matched", [])
    missing = hs.get("missing", [])
    if matched:
        print(f"{BOLD}{'─' * 60}{RESET}")
        print(f"  {GREEN}Matched Skills:{RESET} {', '.join(matched)}")
    if missing:
        print(f"  {RED}Missing Skills:{RESET} {', '.join(missing)}")

    # Keywords
    kw = details["keyword_relevance"]
    missing_kw = kw.get("missing_keywords", [])
    if missing_kw:
        print(f"  {YELLOW}Keywords to Add:{RESET} {', '.join(missing_kw[:15])}")

    # Experience
    exp = details["experience"]
    resume_yrs = exp.get("resume_years", "?")
    req_yrs = exp.get("required_years", "Not specified")
    print(f"\n  {BOLD}Experience:{RESET} You have ~{resume_yrs} yrs | Required: {req_yrs}")

    # Education
    edu = details["education"]
    print(f"  {BOLD}Education:{RESET}  You: {edu.get('resume_level', 'N/A')} | Required: {edu.get('required_level', 'N/A')}")

    # Certifications
    cert = details["certifications"]
    if cert.get("matched"):
        print(f"  {GREEN}Matched Certs:{RESET} {', '.join(cert['matched'])}")
    if cert.get("missing"):
        print(f"  {RED}Missing Certs:{RESET} {', '.join(cert['missing'])}")

    # Feedback
    print()
    print(f"{BOLD}{'─' * 60}{RESET}")
    print(f"{BOLD}  FEEDBACK{RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}")

    if feedback.get("critical_gaps"):
        for item in feedback["critical_gaps"]:
            print(f"  {RED}[CRITICAL]{RESET} {item}")

    if feedback.get("improvements"):
        for item in feedback["improvements"]:
            print(f"  {YELLOW}[IMPROVE]{RESET}  {item}")

    if feedback.get("strengths"):
        for item in feedback["strengths"]:
            print(f"  {GREEN}[STRONG]{RESET}   {item}")

    print()
    print(f"{BOLD}{'=' * 60}{RESET}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="ATS Resume Scorer - Score your resume against a job posting (Workday-style)",
    )
    parser.add_argument(
        "--resume", "-r",
        required=True,
        help="Path to your resume file (PDF, DOCX, or TXT)",
    )

    job_group = parser.add_mutually_exclusive_group()
    job_group.add_argument(
        "--job-url", "-u",
        help="URL to the job posting",
    )
    job_group.add_argument(
        "--job-text", "-t",
        help="Path to a text file containing the job description",
    )

    args = parser.parse_args()

    # Parse resume
    resume_path = Path(args.resume)
    if not resume_path.exists():
        print(f"{RED}Error: Resume file not found: {resume_path}{RESET}", file=sys.stderr)
        sys.exit(1)

    print(f"{DIM}Parsing resume: {resume_path.name}...{RESET}")
    resume_bytes = resume_path.read_bytes()
    try:
        resume_text = parse_resume(resume_bytes, resume_path.name)
    except ValueError as e:
        print(f"{RED}Error: {e}{RESET}", file=sys.stderr)
        sys.exit(1)

    if not resume_text.strip():
        print(f"{RED}Error: Could not extract text from resume.{RESET}", file=sys.stderr)
        sys.exit(1)

    # Get job text
    if args.job_url:
        print(f"{DIM}Fetching job posting from URL...{RESET}")
        try:
            job_text = scrape_job_posting(args.job_url)
        except (ConnectionError, ValueError) as e:
            print(f"{RED}Error fetching URL: {e}{RESET}", file=sys.stderr)
            sys.exit(1)
    elif args.job_text:
        job_path = Path(args.job_text)
        if not job_path.exists():
            print(f"{RED}Error: Job text file not found: {job_path}{RESET}", file=sys.stderr)
            sys.exit(1)
        job_text = job_path.read_text()
    else:
        print("Paste the job description below (press Ctrl+D or Ctrl+Z when done):")
        print(f"{DIM}{'─' * 40}{RESET}")
        job_text = sys.stdin.read()

    if not job_text.strip():
        print(f"{RED}Error: Job description is empty.{RESET}", file=sys.stderr)
        sys.exit(1)

    # Score
    print(f"{DIM}Scoring resume...{RESET}")
    results = score_resume(resume_text, job_text)

    # Display
    print_results(results)


if __name__ == "__main__":
    main()
