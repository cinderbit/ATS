"""Workday-style ATS Resume Scoring Engine.

Workday's ATS scoring evaluates candidates across multiple weighted dimensions.
This engine replicates that approach with the following scoring categories:

  1. Hard Skills Match (25%)     - Technical skills, tools, technologies
  2. Keyword Relevance (20%)     - TF-IDF cosine similarity + exact keyword overlap
  3. Experience Alignment (15%)  - Years of experience vs. requirement
  4. Education Match (15%)       - Degree level and field of study
  5. Job Title Relevance (10%)   - Title alignment with role
  6. Certifications (5%)         - Required/preferred certifications
  7. Soft Skills (5%)            - Leadership, communication, etc.
  8. Resume Formatting (5%)      - ATS-parseable structure detection

Each category scores 0-100, then the weighted total gives the final ATS score.
"""

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from . import extractor


# --- Scoring weights (mirror Workday's emphasis) ---
SCORING_WEIGHTS = {
    "hard_skills": 0.25,
    "keyword_relevance": 0.20,
    "experience": 0.15,
    "education": 0.15,
    "job_title": 0.10,
    "certifications": 0.05,
    "soft_skills": 0.05,
    "formatting": 0.05,
}


def score_resume(resume_text: str, job_text: str) -> dict:
    """Score a resume against a job requisition.

    Returns a detailed scoring breakdown with category scores,
    overall score, and actionable feedback.
    """
    resume_data = extractor.extract_all(resume_text)
    job_data = extractor.extract_all(job_text)

    scores = {}
    details = {}

    # 1. Hard Skills Match (25%)
    scores["hard_skills"], details["hard_skills"] = _score_hard_skills(
        resume_data["skills"], job_data["skills"]
    )

    # 2. Keyword Relevance (20%)
    scores["keyword_relevance"], details["keyword_relevance"] = _score_keywords(
        resume_text, job_text
    )

    # 3. Experience Alignment (15%)
    scores["experience"], details["experience"] = _score_experience(
        resume_data["experience"], job_data["experience"]
    )

    # 4. Education Match (15%)
    scores["education"], details["education"] = _score_education(
        resume_data["education"], job_data["education"]
    )

    # 5. Job Title Relevance (10%)
    scores["job_title"], details["job_title"] = _score_job_title(
        resume_data["job_titles"], job_text
    )

    # 6. Certifications (5%)
    scores["certifications"], details["certifications"] = _score_certifications(
        resume_data["certifications"], job_data["certifications"]
    )

    # 7. Soft Skills (5%)
    scores["soft_skills"], details["soft_skills"] = _score_soft_skills(
        resume_data["skills"].get("soft_skills", []),
        job_data["skills"].get("soft_skills", []),
    )

    # 8. Resume Formatting (5%)
    scores["formatting"], details["formatting"] = _score_formatting(resume_text)

    # Calculate weighted total
    overall = sum(scores[k] * SCORING_WEIGHTS[k] for k in SCORING_WEIGHTS)

    # Generate feedback
    feedback = _generate_feedback(scores, details, resume_data, job_data)

    return {
        "overall_score": round(overall, 1),
        "category_scores": {k: round(v, 1) for k, v in scores.items()},
        "weights": SCORING_WEIGHTS,
        "details": details,
        "feedback": feedback,
        "resume_data": resume_data,
        "job_data": job_data,
        "grade": _score_to_grade(overall),
    }


def _score_hard_skills(resume_skills: dict, job_skills: dict) -> tuple:
    """Score technical skills match."""
    resume_tech = set(resume_skills.get("programming_languages", []))
    resume_tools = set(resume_skills.get("frameworks_and_tools", []))
    resume_all = resume_tech | resume_tools

    job_tech = set(job_skills.get("programming_languages", []))
    job_tools = set(job_skills.get("frameworks_and_tools", []))
    job_all = job_tech | job_tools

    if not job_all:
        return 75.0, {
            "matched": sorted(resume_all),
            "missing": [],
            "extra": [],
            "note": "No specific technical skills detected in job posting.",
        }

    matched = resume_all & job_all
    missing = job_all - resume_all
    extra = resume_all - job_all

    match_ratio = len(matched) / len(job_all) if job_all else 0

    # Workday scores on a curve - having 70%+ of skills is very good
    if match_ratio >= 0.9:
        score = 95 + (match_ratio - 0.9) * 50
    elif match_ratio >= 0.7:
        score = 80 + (match_ratio - 0.7) * 75
    elif match_ratio >= 0.5:
        score = 60 + (match_ratio - 0.5) * 100
    elif match_ratio >= 0.3:
        score = 35 + (match_ratio - 0.3) * 125
    else:
        score = match_ratio * 116

    score = min(100, max(0, score))

    return score, {
        "matched": sorted(matched),
        "missing": sorted(missing),
        "extra": sorted(extra),
        "match_ratio": round(match_ratio * 100, 1),
    }


def _score_keywords(resume_text: str, job_text: str) -> tuple:
    """Score keyword relevance using TF-IDF cosine similarity."""
    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=500,
            ngram_range=(1, 2),
            min_df=1,
        )
        tfidf_matrix = vectorizer.fit_transform([job_text, resume_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except ValueError:
        similarity = 0.0

    # Extract key terms from job posting
    job_words = set(_extract_meaningful_words(job_text))
    resume_words = set(_extract_meaningful_words(resume_text))

    if job_words:
        overlap = job_words & resume_words
        keyword_overlap_ratio = len(overlap) / len(job_words)
    else:
        overlap = set()
        keyword_overlap_ratio = 0

    # Combine TF-IDF similarity and keyword overlap
    combined = (similarity * 0.6 + keyword_overlap_ratio * 0.4) * 100
    score = min(100, max(0, combined))

    return score, {
        "tfidf_similarity": round(similarity * 100, 1),
        "keyword_overlap_pct": round(keyword_overlap_ratio * 100, 1),
        "matching_keywords": sorted(overlap)[:30],
        "missing_keywords": sorted(job_words - resume_words)[:20],
    }


def _extract_meaningful_words(text: str) -> list:
    """Extract meaningful multi-word terms and single words (2+ chars)."""
    # Simple but effective: extract words that aren't common stopwords
    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "shall",
        "should", "may", "might", "can", "could", "this", "that", "these",
        "those", "it", "its", "we", "our", "you", "your", "they", "their",
        "from", "as", "not", "all", "any", "each", "every", "both", "few",
        "more", "most", "other", "some", "such", "no", "nor", "too", "very",
        "just", "about", "above", "after", "again", "also", "am", "an",
        "because", "before", "between", "during", "into", "through", "up",
        "out", "over", "under", "here", "there", "when", "where", "which",
        "while", "who", "whom", "what", "how", "than", "then", "so", "if",
        "only", "own", "same", "her", "his", "him", "she", "he", "me", "my",
        "etc", "per", "via", "within", "without", "ability", "able",
        "including", "include", "work", "working", "role", "position", "job",
        "team", "company", "us", "new", "well", "one", "two", "must",
    }
    words = re.findall(r"\b[a-z][a-z+#.-]+\b", text.lower())
    return [w for w in words if w not in stopwords and len(w) > 2]


def _score_experience(resume_exp: dict, job_exp: dict) -> tuple:
    """Score experience alignment."""
    resume_years = resume_exp.get("estimated_total", 0)
    job_years_required = job_exp.get("max_explicit")

    if not job_years_required:
        # Try to infer from common patterns in job data
        if resume_years > 0:
            return 70.0, {
                "resume_years": resume_years,
                "required_years": "Not specified",
                "note": "Job posting doesn't specify years required.",
            }
        return 50.0, {
            "resume_years": resume_years,
            "required_years": "Not specified",
            "note": "Could not determine experience from either document.",
        }

    diff = resume_years - job_years_required

    if diff >= 3:
        score = 95.0  # Exceeds by 3+
    elif diff >= 0:
        score = 80.0 + diff * 5  # Meets or slightly exceeds
    elif diff >= -1:
        score = 65.0  # Close to meeting
    elif diff >= -2:
        score = 45.0  # Somewhat short
    elif diff >= -3:
        score = 30.0  # Significantly short
    else:
        score = max(10.0, 30.0 + diff * 5)

    return score, {
        "resume_years": resume_years,
        "required_years": job_years_required,
        "difference": diff,
    }


def _score_education(resume_edu: dict, job_edu: dict) -> tuple:
    """Score education match."""
    resume_level = resume_edu.get("level_score", -1)
    job_level = job_edu.get("level_score", -1)
    resume_fields = set(f.lower() for f in resume_edu.get("fields", []))
    job_fields = set(f.lower() for f in job_edu.get("fields", []))

    # Level scoring
    if job_level < 0:
        level_score = 70.0  # No education requirement detected
        level_note = "No specific education requirement detected."
    elif resume_level >= job_level:
        level_score = 90.0 + min(10, (resume_level - job_level) * 5)
        level_note = "Meets or exceeds education requirement."
    elif resume_level == job_level - 1:
        level_score = 60.0
        level_note = "One level below required education."
    else:
        level_score = max(20.0, 60 - (job_level - resume_level) * 20)
        level_note = "Below required education level."

    # Field scoring
    if job_fields and resume_fields:
        field_overlap = resume_fields & job_fields
        if field_overlap:
            field_score = 100.0
        else:
            # Check for related fields
            field_score = 50.0
    elif not job_fields:
        field_score = 80.0
    else:
        field_score = 40.0

    combined = level_score * 0.6 + field_score * 0.4

    return combined, {
        "resume_level": resume_edu.get("highest_level", "Not detected"),
        "required_level": job_edu.get("highest_level", "Not specified"),
        "resume_fields": sorted(resume_edu.get("fields", [])),
        "job_fields": sorted(job_edu.get("fields", [])),
        "level_note": level_note,
    }


def _score_job_title(resume_titles: list, job_text: str) -> tuple:
    """Score job title relevance against the job posting."""
    if not resume_titles:
        return 40.0, {"note": "No job titles detected in resume.", "matched_titles": []}

    job_lower = job_text.lower()
    matched = []
    best_score = 0

    for title in resume_titles:
        title_lower = title.lower()
        title_words = set(title_lower.split())

        # Check for exact title match
        if title_lower in job_lower:
            matched.append(title)
            best_score = max(best_score, 100)
            continue

        # Check for partial word overlap
        job_words = set(job_lower.split())
        overlap = title_words & job_words
        if overlap:
            ratio = len(overlap) / len(title_words)
            score = ratio * 85
            if score > 40:
                matched.append(title)
            best_score = max(best_score, score)

    if not matched:
        best_score = 25.0

    return min(100, best_score), {
        "resume_titles": resume_titles[:5],
        "matched_titles": matched,
    }


def _score_certifications(resume_certs: list, job_certs: list) -> tuple:
    """Score certification matches."""
    if not job_certs:
        if resume_certs:
            return 85.0, {
                "matched": [],
                "resume_certs": resume_certs,
                "required_certs": [],
                "note": "No certifications required. Your certifications are a bonus.",
            }
        return 70.0, {
            "matched": [],
            "resume_certs": [],
            "required_certs": [],
            "note": "No certifications required or found.",
        }

    resume_set = set(c.lower() for c in resume_certs)
    job_set = set(c.lower() for c in job_certs)
    matched = resume_set & job_set

    if not job_set:
        ratio = 1.0
    else:
        ratio = len(matched) / len(job_set)

    score = ratio * 100

    return score, {
        "matched": sorted(matched),
        "resume_certs": resume_certs,
        "required_certs": job_certs,
        "missing": sorted(job_set - resume_set),
    }


def _score_soft_skills(resume_soft: list, job_soft: list) -> tuple:
    """Score soft skills match."""
    if not job_soft:
        return 70.0, {
            "matched": [],
            "missing": [],
            "note": "No specific soft skills detected in job posting.",
        }

    resume_set = set(s.lower() for s in resume_soft)
    job_set = set(s.lower() for s in job_soft)
    matched = resume_set & job_set
    missing = job_set - resume_set

    ratio = len(matched) / len(job_set) if job_set else 0
    score = min(100, ratio * 100 + 20) if matched else 15

    return score, {
        "matched": sorted(matched),
        "missing": sorted(missing),
    }


def _score_formatting(resume_text: str) -> tuple:
    """Score resume formatting/structure for ATS compatibility.

    Workday's parser expects specific sections and clean formatting.
    """
    from .parser import parse_resume_sections

    sections = parse_resume_sections(resume_text)
    found_sections = set(sections.keys()) - {"header"}

    critical_sections = {"experience", "education", "skills"}
    important_sections = {"summary", "certifications"}
    bonus_sections = {"projects", "awards", "languages", "volunteer"}

    critical_found = critical_sections & found_sections
    important_found = important_sections & found_sections
    bonus_found = bonus_sections & found_sections

    score = 0
    # Critical sections: 20 points each (max 60)
    score += len(critical_found) * 20
    # Important sections: 10 points each (max 20)
    score += len(important_found) * 10
    # Bonus sections: 5 points each (max 20, capped)
    score += min(20, len(bonus_found) * 5)

    # Check for clean formatting indicators
    lines = resume_text.split("\n")
    non_empty_lines = [l for l in lines if l.strip()]

    # Penalize very short resumes
    if len(non_empty_lines) < 10:
        score = max(0, score - 20)

    # Bonus for reasonable length
    if 30 <= len(non_empty_lines) <= 200:
        score = min(100, score + 5)

    score = min(100, max(0, score))

    return score, {
        "sections_found": sorted(found_sections),
        "critical_missing": sorted(critical_sections - found_sections),
        "suggestions": _formatting_suggestions(found_sections, critical_sections, important_sections),
    }


def _formatting_suggestions(found: set, critical: set, important: set) -> list:
    """Generate formatting improvement suggestions."""
    suggestions = []
    missing_critical = critical - found
    missing_important = important - found

    if missing_critical:
        suggestions.append(
            f"Add clearly labeled sections for: {', '.join(sorted(missing_critical))}. "
            "Workday requires these sections for proper parsing."
        )
    if missing_important:
        suggestions.append(
            f"Consider adding: {', '.join(sorted(missing_important))} section(s) for better scoring."
        )
    if "contact" not in found:
        suggestions.append("Ensure contact information is clearly visible at the top.")

    return suggestions


def _score_to_grade(score: float) -> str:
    """Convert numeric score to a letter grade."""
    if score >= 90:
        return "A+"
    elif score >= 85:
        return "A"
    elif score >= 80:
        return "A-"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "B-"
    elif score >= 60:
        return "C+"
    elif score >= 55:
        return "C"
    elif score >= 50:
        return "C-"
    elif score >= 45:
        return "D+"
    elif score >= 40:
        return "D"
    else:
        return "F"


def _generate_feedback(scores: dict, details: dict,
                       resume_data: dict, job_data: dict) -> dict:
    """Generate actionable feedback to improve the resume score."""
    strengths = []
    improvements = []
    critical = []

    # Hard skills feedback
    hs = scores["hard_skills"]
    hs_detail = details["hard_skills"]
    if hs >= 80:
        strengths.append(f"Strong technical skills match ({hs_detail.get('match_ratio', 0)}% of required skills found).")
    elif hs >= 50:
        missing = hs_detail.get("missing", [])
        if missing:
            improvements.append(
                f"Add these missing skills to your resume if you have them: {', '.join(missing[:8])}."
            )
    else:
        missing = hs_detail.get("missing", [])
        if missing:
            critical.append(
                f"Significant skills gap. Missing: {', '.join(missing[:10])}. "
                "Consider whether this role aligns with your skillset."
            )

    # Keyword feedback
    kw = scores["keyword_relevance"]
    kw_detail = details["keyword_relevance"]
    if kw >= 70:
        strengths.append("Good keyword alignment with the job posting.")
    else:
        missing_kw = kw_detail.get("missing_keywords", [])
        if missing_kw:
            improvements.append(
                f"Incorporate these keywords from the job posting: {', '.join(missing_kw[:10])}."
            )

    # Experience feedback
    exp = scores["experience"]
    exp_detail = details["experience"]
    if exp >= 80:
        strengths.append(f"Experience level aligns well ({exp_detail.get('resume_years', '?')} years).")
    elif exp < 50:
        req = exp_detail.get("required_years", "?")
        have = exp_detail.get("resume_years", "?")
        critical.append(
            f"Experience gap: role requires {req} years, resume shows ~{have} years."
        )

    # Education feedback
    edu = scores["education"]
    edu_detail = details["education"]
    if edu >= 80:
        strengths.append(f"Education meets requirements ({edu_detail.get('resume_level', 'detected')}).")
    elif edu < 50:
        improvements.append(
            f"Education may not meet requirements. "
            f"Required: {edu_detail.get('required_level', 'Not specified')}. "
            f"Found: {edu_detail.get('resume_level', 'Not detected')}."
        )

    # Formatting feedback
    fmt = scores["formatting"]
    fmt_detail = details["formatting"]
    if fmt >= 70:
        strengths.append("Resume structure is ATS-friendly.")
    else:
        suggestions = fmt_detail.get("suggestions", [])
        for s in suggestions:
            improvements.append(s)

    # Certifications
    cert_detail = details["certifications"]
    if cert_detail.get("missing"):
        improvements.append(
            f"Consider obtaining: {', '.join(cert_detail['missing'][:5])}."
        )

    # Soft skills
    ss_detail = details["soft_skills"]
    if ss_detail.get("missing"):
        improvements.append(
            f"Mention these soft skills if applicable: {', '.join(ss_detail['missing'][:5])}."
        )

    return {
        "strengths": strengths,
        "improvements": improvements,
        "critical_gaps": critical,
    }
