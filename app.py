"""ATS Resume Scorer - Workday-Style Resume Analysis Tool.

A Streamlit web application that scores your resume against a job posting
using the same weighted criteria that Workday's ATS uses for candidate ranking.

Usage:
    streamlit run app.py
"""

import streamlit as st

from ats.extractor import extract_all
from ats.parser import parse_resume, parse_resume_sections
from ats.scorer import SCORING_WEIGHTS, score_resume
from ats.scraper import parse_job_text, scrape_job_posting

# --- Page Config ---
st.set_page_config(
    page_title="ATS Resume Scorer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
st.markdown("""
<style>
    .score-card {
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    .score-high { background: linear-gradient(135deg, #00c853, #69f0ae); color: #1b5e20; }
    .score-mid { background: linear-gradient(135deg, #ffd600, #ffff8d); color: #f57f17; }
    .score-low { background: linear-gradient(135deg, #ff1744, #ff8a80); color: #b71c1c; }
    .metric-label { font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-value { font-size: 2.5rem; font-weight: 800; }
    .section-header { border-bottom: 2px solid #e0e0e0; padding-bottom: 0.5rem; margin-top: 1.5rem; }
    div[data-testid="stProgress"] > div > div > div { height: 12px; border-radius: 6px; }
</style>
""", unsafe_allow_html=True)


def main():
    # --- Header ---
    st.title("ATS Resume Scorer")
    st.caption("Workday-style resume analysis  |  Score your resume against any job posting")

    # --- Sidebar ---
    with st.sidebar:
        st.header("How It Works")
        st.markdown("""
        This tool mirrors **Workday's ATS scoring** across 8 weighted categories:

        | Category | Weight |
        |----------|--------|
        | Hard Skills | 25% |
        | Keywords | 20% |
        | Experience | 15% |
        | Education | 15% |
        | Job Title | 10% |
        | Certifications | 5% |
        | Soft Skills | 5% |
        | Formatting | 5% |

        **Upload your resume** and provide a job posting to get your score.
        """)

        st.divider()
        st.markdown("**Supported Formats:** PDF, DOCX, TXT")
        st.markdown("**Job Input:** URL or paste text")

    # --- Input Section ---
    col_resume, col_job = st.columns(2)

    with col_resume:
        st.subheader("1. Upload Your Resume")
        uploaded_file = st.file_uploader(
            "Upload resume (PDF, DOCX, or TXT)",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, TXT",
        )

    with col_job:
        st.subheader("2. Provide Job Posting")
        job_input_method = st.radio(
            "How would you like to provide the job posting?",
            ["Paste Text", "Enter URL"],
            horizontal=True,
        )

        if job_input_method == "Enter URL":
            job_url = st.text_input(
                "Job posting URL",
                placeholder="https://company.wd5.myworkdayjobs.com/...",
            )
            job_text_input = None
        else:
            job_text_input = st.text_area(
                "Paste the job description",
                height=250,
                placeholder="Paste the full job description here...",
            )
            job_url = None

    # --- Score Button ---
    st.divider()
    score_button = st.button("Score My Resume", type="primary", use_container_width=True)

    if score_button:
        # Validate inputs
        if not uploaded_file:
            st.error("Please upload your resume.")
            return

        if job_input_method == "Enter URL" and not job_url:
            st.error("Please enter a job posting URL.")
            return
        elif job_input_method == "Paste Text" and not job_text_input:
            st.error("Please paste the job description.")
            return

        with st.spinner("Analyzing your resume..."):
            try:
                # Parse resume
                resume_bytes = uploaded_file.read()
                resume_text = parse_resume(resume_bytes, uploaded_file.name)

                if not resume_text.strip():
                    st.error("Could not extract text from your resume. Please try a different format.")
                    return

                # Get job text
                if job_url:
                    with st.status("Fetching job posting..."):
                        job_text = scrape_job_posting(job_url)
                else:
                    job_text = job_text_input

                if not job_text.strip():
                    st.error("Job posting text is empty.")
                    return

                # Score
                results = score_resume(resume_text, job_text)

            except ConnectionError as e:
                st.error(f"Could not fetch job posting: {e}")
                return
            except Exception as e:
                st.error(f"Error: {e}")
                return

        # --- Display Results ---
        _display_results(results, resume_text, job_text)


def _display_results(results: dict, resume_text: str, job_text: str):
    """Display the scoring results."""
    overall = results["overall_score"]
    grade = results["grade"]
    scores = results["category_scores"]
    details = results["details"]
    feedback = results["feedback"]

    # --- Overall Score ---
    st.markdown("---")

    if overall >= 75:
        score_class = "score-high"
        verdict = "Strong Match"
    elif overall >= 55:
        score_class = "score-mid"
        verdict = "Moderate Match"
    else:
        score_class = "score-low"
        verdict = "Needs Improvement"

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="score-card {score_class}">
            <div class="metric-label">ATS COMPATIBILITY SCORE</div>
            <div class="metric-value">{overall}/100</div>
            <div style="font-size: 1.3rem; font-weight: 600;">Grade: {grade} — {verdict}</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Category Breakdown ---
    st.markdown('<h3 class="section-header">Category Breakdown</h3>', unsafe_allow_html=True)

    weight_labels = {
        "hard_skills": ("Hard Skills", "25%"),
        "keyword_relevance": ("Keyword Relevance", "20%"),
        "experience": ("Experience", "15%"),
        "education": ("Education", "15%"),
        "job_title": ("Job Title", "10%"),
        "certifications": ("Certifications", "5%"),
        "soft_skills": ("Soft Skills", "5%"),
        "formatting": ("Formatting", "5%"),
    }

    cols = st.columns(4)
    for i, (key, (label, weight)) in enumerate(weight_labels.items()):
        with cols[i % 4]:
            score_val = scores[key]
            color = "#00c853" if score_val >= 75 else "#ffd600" if score_val >= 50 else "#ff1744"
            st.markdown(f"**{label}** ({weight})")
            st.progress(score_val / 100)
            st.markdown(f"<span style='color:{color}; font-weight:700;'>{score_val}/100</span>",
                        unsafe_allow_html=True)

    # --- Detailed Analysis Tabs ---
    st.markdown('<h3 class="section-header">Detailed Analysis</h3>', unsafe_allow_html=True)

    tab_skills, tab_keywords, tab_exp, tab_edu, tab_other, tab_feedback = st.tabs([
        "Skills", "Keywords", "Experience", "Education", "Other", "Feedback & Tips",
    ])

    with tab_skills:
        _display_skills_tab(details)

    with tab_keywords:
        _display_keywords_tab(details)

    with tab_exp:
        _display_experience_tab(details)

    with tab_edu:
        _display_education_tab(details)

    with tab_other:
        _display_other_tab(details)

    with tab_feedback:
        _display_feedback_tab(feedback)

    # --- Resume Sections Detected ---
    with st.expander("Resume Sections Detected (ATS Parse View)"):
        sections = parse_resume_sections(resume_text)
        for section_name, content in sections.items():
            if content.strip():
                st.markdown(f"**{section_name.upper()}**")
                st.text(content[:500] + ("..." if len(content) > 500 else ""))
                st.divider()

    # --- Raw Extracted Data ---
    with st.expander("Raw Extraction Data"):
        col_r, col_j = st.columns(2)
        with col_r:
            st.markdown("**Resume Entities**")
            st.json(results["resume_data"])
        with col_j:
            st.markdown("**Job Posting Entities**")
            st.json(results["job_data"])


def _display_skills_tab(details: dict):
    hs = details["hard_skills"]
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Matched Skills**")
        matched = hs.get("matched", [])
        if matched:
            for skill in matched:
                st.markdown(f"- :green[{skill}]")
        else:
            st.info("No matching skills found.")

    with col2:
        st.markdown("**Missing Skills (from job posting)**")
        missing = hs.get("missing", [])
        if missing:
            for skill in missing:
                st.markdown(f"- :red[{skill}]")
        else:
            st.success("No missing skills!")

    extra = hs.get("extra", [])
    if extra:
        st.markdown("**Additional Skills (not in job posting)**")
        st.write(", ".join(extra))

    if "match_ratio" in hs:
        st.metric("Skills Match Rate", f"{hs['match_ratio']}%")


def _display_keywords_tab(details: dict):
    kw = details["keyword_relevance"]
    col1, col2 = st.columns(2)

    with col1:
        st.metric("TF-IDF Similarity", f"{kw.get('tfidf_similarity', 0)}%")
        st.metric("Keyword Overlap", f"{kw.get('keyword_overlap_pct', 0)}%")

    with col2:
        st.markdown("**Top Matching Keywords**")
        matching = kw.get("matching_keywords", [])
        if matching:
            st.write(", ".join(matching[:20]))
        else:
            st.info("No significant keyword matches.")

    missing_kw = kw.get("missing_keywords", [])
    if missing_kw:
        st.markdown("**Keywords to Add**")
        st.write(", ".join(missing_kw[:20]))


def _display_experience_tab(details: dict):
    exp = details["experience"]
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Your Experience", f"{exp.get('resume_years', 'N/A')} years")
    with col2:
        req = exp.get("required_years", "Not specified")
        st.metric("Required Experience", f"{req} years" if isinstance(req, (int, float)) else str(req))

    diff = exp.get("difference")
    if diff is not None:
        if diff >= 0:
            st.success(f"You exceed the requirement by {diff} year(s).")
        else:
            st.warning(f"You are {abs(diff)} year(s) below the requirement.")

    note = exp.get("note")
    if note:
        st.info(note)


def _display_education_tab(details: dict):
    edu = details["education"]
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Your Education", edu.get("resume_level", "Not detected"))
        fields = edu.get("resume_fields", [])
        if fields:
            st.write("**Fields:** " + ", ".join(fields))

    with col2:
        st.metric("Required Education", edu.get("required_level", "Not specified"))
        job_fields = edu.get("job_fields", [])
        if job_fields:
            st.write("**Required Fields:** " + ", ".join(job_fields))

    note = edu.get("level_note")
    if note:
        st.info(note)


def _display_other_tab(details: dict):
    # Job Title
    st.markdown("**Job Title Match**")
    jt = details["job_title"]
    titles = jt.get("resume_titles", [])
    matched = jt.get("matched_titles", [])
    if matched:
        st.success(f"Matching titles: {', '.join(matched)}")
    elif titles:
        st.warning(f"Your titles ({', '.join(titles[:3])}) don't closely match the job posting.")
    else:
        st.warning("No job titles detected in your resume.")

    st.divider()

    # Certifications
    st.markdown("**Certifications**")
    cert = details["certifications"]
    if cert.get("matched"):
        st.success(f"Matched: {', '.join(cert['matched'])}")
    if cert.get("missing"):
        st.warning(f"Missing: {', '.join(cert['missing'])}")
    if cert.get("resume_certs") and not cert.get("matched") and not cert.get("missing"):
        st.info(f"Your certifications: {', '.join(cert['resume_certs'])}")
    if cert.get("note"):
        st.info(cert["note"])

    st.divider()

    # Soft Skills
    st.markdown("**Soft Skills**")
    ss = details["soft_skills"]
    if ss.get("matched"):
        st.success(f"Matched: {', '.join(ss['matched'])}")
    if ss.get("missing"):
        st.warning(f"Consider adding: {', '.join(ss['missing'])}")
    if ss.get("note"):
        st.info(ss["note"])

    st.divider()

    # Formatting
    st.markdown("**Resume Formatting (ATS Compatibility)**")
    fmt = details["formatting"]
    sections = fmt.get("sections_found", [])
    if sections:
        st.write("**Detected sections:** " + ", ".join(sections))
    critical = fmt.get("critical_missing", [])
    if critical:
        st.error(f"Missing critical sections: {', '.join(critical)}")
    suggestions = fmt.get("suggestions", [])
    for s in suggestions:
        st.warning(s)


def _display_feedback_tab(feedback: dict):
    strengths = feedback.get("strengths", [])
    improvements = feedback.get("improvements", [])
    critical = feedback.get("critical_gaps", [])

    if critical:
        st.markdown("**Critical Issues**")
        for item in critical:
            st.error(item)

    if improvements:
        st.markdown("**Recommended Improvements**")
        for item in improvements:
            st.warning(item)

    if strengths:
        st.markdown("**Strengths**")
        for item in strengths:
            st.success(item)

    if not strengths and not improvements and not critical:
        st.info("No specific feedback generated. Your resume may need more content for thorough analysis.")

    st.divider()
    st.markdown("""
    **General ATS Tips (Workday-specific):**
    - Use standard section headings (Experience, Education, Skills, etc.)
    - Avoid tables, columns, graphics, and headers/footers — Workday can't parse them
    - Use standard fonts and simple formatting
    - Include exact keywords from the job posting
    - Spell out acronyms at least once (e.g., "Amazon Web Services (AWS)")
    - List skills explicitly in a dedicated Skills section
    - Use reverse chronological order for experience
    - Include months and years for all dates
    - Save as PDF for best compatibility (DOCX is also accepted)
    """)


if __name__ == "__main__":
    main()
