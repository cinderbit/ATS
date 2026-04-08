"""Entity extraction - skills, education, experience, certifications.

Mirrors Workday's parsing approach which focuses on structured extraction
of key resume entities for matching against job requirements.
"""

import re
from collections import defaultdict

# --- Comprehensive skill/technology lists ---

PROGRAMMING_LANGUAGES = {
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "go", "golang",
    "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl",
    "shell", "bash", "powershell", "sql", "nosql", "html", "css", "sass", "less",
    "objective-c", "dart", "lua", "haskell", "erlang", "elixir", "clojure",
    "groovy", "visual basic", "vba", "assembly", "cobol", "fortran", "julia",
    "solidity", "graphql",
}

FRAMEWORKS_AND_TOOLS = {
    "react", "angular", "vue", "vue.js", "node.js", "nodejs", "express",
    "django", "flask", "fastapi", "spring", "spring boot", ".net", "asp.net",
    "rails", "ruby on rails", "laravel", "next.js", "nextjs", "nuxt",
    "svelte", "gatsby", "remix", "tensorflow", "pytorch", "keras", "scikit-learn",
    "pandas", "numpy", "scipy", "matplotlib", "spark", "hadoop", "kafka",
    "rabbitmq", "redis", "elasticsearch", "mongodb", "postgresql", "mysql",
    "oracle", "sql server", "dynamodb", "cassandra", "neo4j", "firebase",
    "supabase", "docker", "kubernetes", "k8s", "terraform", "ansible",
    "jenkins", "gitlab ci", "github actions", "circleci", "travis ci",
    "aws", "azure", "gcp", "google cloud", "amazon web services",
    "heroku", "vercel", "netlify", "cloudflare", "nginx", "apache",
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    "slack", "figma", "sketch", "adobe xd", "tableau", "power bi",
    "looker", "snowflake", "databricks", "airflow", "dbt", "mlflow",
    "sagemaker", "openai", "langchain", "hugging face", "transformers",
    "webpack", "vite", "babel", "eslint", "prettier", "jest", "mocha",
    "cypress", "selenium", "playwright", "postman", "swagger", "graphql",
    "rest", "restful", "grpc", "websocket", "oauth", "jwt", "saml",
    "ldap", "active directory", "linux", "unix", "windows server",
    "vmware", "vagrant", "packer", "consul", "vault", "prometheus",
    "grafana", "datadog", "splunk", "new relic", "elk stack", "logstash",
    "kibana", "fluentd", "chef", "puppet", "saltstack", "cdk", "cloudformation",
    "sam", "serverless", "lambda", "step functions", "sqs", "sns", "s3",
    "ec2", "ecs", "eks", "fargate", "rds", "aurora", "redshift",
    "athena", "glue", "emr", "kinesis", "api gateway",
}

SOFT_SKILLS = {
    "leadership", "communication", "teamwork", "collaboration", "problem solving",
    "problem-solving", "critical thinking", "analytical", "creativity",
    "adaptability", "time management", "project management", "agile", "scrum",
    "kanban", "waterfall", "mentoring", "coaching", "negotiation",
    "presentation", "public speaking", "strategic thinking", "decision making",
    "conflict resolution", "stakeholder management", "cross-functional",
    "self-motivated", "detail-oriented", "results-driven", "customer-focused",
    "innovative", "resourceful", "proactive", "organizational",
}

CERTIFICATIONS_DB = {
    "aws certified": "AWS Certification",
    "aws solutions architect": "AWS Solutions Architect",
    "aws developer": "AWS Developer",
    "aws sysops": "AWS SysOps",
    "aws devops": "AWS DevOps",
    "azure certified": "Azure Certification",
    "google cloud certified": "Google Cloud Certification",
    "gcp certified": "Google Cloud Certification",
    "pmp": "Project Management Professional",
    "project management professional": "Project Management Professional",
    "scrum master": "Scrum Master",
    "csm": "Certified Scrum Master",
    "psm": "Professional Scrum Master",
    "cissp": "CISSP",
    "cism": "CISM",
    "cisa": "CISA",
    "comptia": "CompTIA",
    "security+": "CompTIA Security+",
    "network+": "CompTIA Network+",
    "a+": "CompTIA A+",
    "cka": "Certified Kubernetes Administrator",
    "ckad": "Certified Kubernetes Application Developer",
    "ceh": "Certified Ethical Hacker",
    "oscp": "OSCP",
    "ccna": "Cisco CCNA",
    "ccnp": "Cisco CCNP",
    "itil": "ITIL",
    "six sigma": "Six Sigma",
    "lean six sigma": "Lean Six Sigma",
    "cpa": "CPA",
    "cfa": "CFA",
    "series 7": "Series 7",
    "series 63": "Series 63",
    "pe license": "Professional Engineer",
    "professional engineer": "Professional Engineer",
    "licensed": "Professional License",
}

EDUCATION_LEVELS = {
    "phd": 5,
    "ph.d": 5,
    "doctorate": 5,
    "doctoral": 5,
    "master": 4,
    "master's": 4,
    "masters": 4,
    "mba": 4,
    "ms": 4,
    "m.s.": 4,
    "m.a.": 4,
    "m.eng": 4,
    "bachelor": 3,
    "bachelor's": 3,
    "bachelors": 3,
    "bs": 3,
    "b.s.": 3,
    "b.a.": 3,
    "b.eng": 3,
    "associate": 2,
    "associate's": 2,
    "associates": 2,
    "a.s.": 2,
    "a.a.": 2,
    "diploma": 1,
    "certificate": 1,
    "high school": 0,
    "ged": 0,
}

EDUCATION_FIELDS = {
    "computer science", "software engineering", "information technology",
    "information systems", "data science", "machine learning",
    "artificial intelligence", "electrical engineering", "mechanical engineering",
    "civil engineering", "chemical engineering", "biomedical engineering",
    "mathematics", "statistics", "physics", "chemistry", "biology",
    "business administration", "finance", "accounting", "economics",
    "marketing", "management", "human resources", "psychology",
    "communications", "english", "history", "political science",
    "sociology", "nursing", "medicine", "pharmacy", "law",
    "graphic design", "industrial design", "architecture",
    "environmental science", "cybersecurity", "network engineering",
}


def extract_skills(text: str) -> dict:
    """Extract technical skills, tools, and soft skills from text."""
    text_lower = text.lower()
    found = defaultdict(set)

    for skill in PROGRAMMING_LANGUAGES:
        if _skill_present(text_lower, skill):
            found["programming_languages"].add(skill)

    for skill in FRAMEWORKS_AND_TOOLS:
        if _skill_present(text_lower, skill):
            found["frameworks_and_tools"].add(skill)

    for skill in SOFT_SKILLS:
        if _skill_present(text_lower, skill):
            found["soft_skills"].add(skill)

    return {k: sorted(v) for k, v in found.items()}


def _skill_present(text: str, skill: str) -> bool:
    """Check if a skill is present in text using word boundary matching."""
    pattern = r"(?<![a-zA-Z])" + re.escape(skill) + r"(?![a-zA-Z])"
    return bool(re.search(pattern, text, re.IGNORECASE))


def extract_experience_years(text: str) -> dict:
    """Extract years of experience from text."""
    patterns = [
        r"(\d+)\+?\s*(?:years?|yrs?)[\s\-]*(?:of\s+)?(?:experience|exp)",
        r"(?:experience|exp)[\s:]*(\d+)\+?\s*(?:years?|yrs?)",
        r"(\d+)\+?\s*(?:years?|yrs?)\s+(?:in|of|with)",
    ]

    years_found = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        years_found.extend(int(m) for m in matches)

    # Also infer from work history date ranges
    date_ranges = re.findall(
        r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4})"
        r"\s*[-–—to]+\s*"
        r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}|[Pp]resent|[Cc]urrent)",
        text,
    )

    total_inferred = 0
    for start_str, end_str in date_ranges:
        start_year = _extract_year(start_str)
        if end_str.lower() in ("present", "current"):
            end_year = 2026
        else:
            end_year = _extract_year(end_str)
        if start_year and end_year:
            total_inferred += max(0, end_year - start_year)

    return {
        "explicit_mentions": sorted(set(years_found), reverse=True),
        "max_explicit": max(years_found) if years_found else None,
        "inferred_from_dates": total_inferred,
        "estimated_total": max(
            max(years_found) if years_found else 0,
            total_inferred,
        ),
    }


def _extract_year(date_str: str) -> int | None:
    """Extract year from a date string."""
    match = re.search(r"(\d{4})", date_str)
    return int(match.group(1)) if match else None


def extract_education(text: str) -> dict:
    """Extract education level and field of study."""
    text_lower = text.lower()

    highest_level = -1
    highest_name = None
    for keyword, level in EDUCATION_LEVELS.items():
        if _skill_present(text_lower, keyword) and level > highest_level:
            highest_level = level
            highest_name = keyword

    level_names = {0: "High School", 1: "Certificate/Diploma", 2: "Associate",
                   3: "Bachelor's", 4: "Master's", 5: "Doctorate/PhD"}

    fields_found = []
    for field in EDUCATION_FIELDS:
        if field.lower() in text_lower:
            fields_found.append(field)

    return {
        "highest_level": level_names.get(highest_level, "Not detected"),
        "level_score": highest_level,
        "fields": fields_found,
    }


def extract_certifications(text: str) -> list:
    """Extract certifications and licenses from text."""
    text_lower = text.lower()
    found = []
    for keyword, cert_name in CERTIFICATIONS_DB.items():
        if keyword in text_lower:
            if cert_name not in found:
                found.append(cert_name)
    return found


def extract_job_titles(text: str) -> list:
    """Extract job titles from resume text."""
    title_patterns = [
        r"(?:^|\n)\s*((?:Senior|Junior|Lead|Principal|Staff|Chief|Head|Director|VP|Vice President|Manager|Associate|Entry.Level)\s+[\w\s&/]+?)(?:\s*[-–|@]|\s*at\s)",
        r"(?:^|\n)\s*([\w\s]+?(?:Engineer|Developer|Architect|Designer|Analyst|Scientist|Administrator|Coordinator|Specialist|Consultant|Manager|Director|Officer|Lead))\s*(?:\n|[-–|@,])",
    ]

    titles = []
    for pattern in title_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            title = m.strip()
            if 3 < len(title) < 80:
                titles.append(title)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for t in titles:
        key = t.lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(t)
    return unique[:10]


def extract_all(text: str) -> dict:
    """Run all extraction on a text document."""
    return {
        "skills": extract_skills(text),
        "experience": extract_experience_years(text),
        "education": extract_education(text),
        "certifications": extract_certifications(text),
        "job_titles": extract_job_titles(text),
    }
