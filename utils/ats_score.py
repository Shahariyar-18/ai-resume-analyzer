import re


SKILLS = {
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "nodejs",
    "flask",
    "django",
    "fastapi",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "opencv",
    "nlp",
    "natural language processing",
    "computer vision",
    "power bi",
    "tableau",
    "excel",
    "linux",
    "rest api",
    "api",
    "communication",
    "leadership",
    "problem solving",
    "teamwork",
    "time management"
}


ACTION_WORDS = {
    "developed",
    "designed",
    "implemented",
    "created",
    "managed",
    "improved",
    "optimized",
    "analyzed",
    "built",
    "automated",
    "engineered",
    "deployed",
    "maintained",
    "tested",
    "integrated",
    "configured",
    "led",
    "delivered",
    "implemented"
}


SECTION_KEYWORDS = {
    "summary": [
        "summary",
        "profile",
        "objective",
        "about me"
    ],

    "experience": [
        "experience",
        "work experience",
        "employment",
        "professional experience"
    ],

    "education": [
        "education",
        "academic",
        "qualification"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technologies"
    ],

    "projects": [
        "projects",
        "personal projects",
        "academic projects"
    ],

    "certifications": [
        "certification",
        "certifications",
        "courses",
        "training"
    ],

    "achievements": [
        "achievement",
        "achievements",
        "awards"
    ]
}


def extract_skills(text):

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(found_skills)


def check_email(text):

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    return bool(re.search(pattern, text))


def check_phone(text):

    patterns = [
        r"\b\d{10}\b",
        r"\+91[-\s]?\d{10}",
        r"\+\d{1,3}[-\s]?\d{7,12}"
    ]

    return any(
        re.search(pattern, text)
        for pattern in patterns
    )


def detect_sections(text):

    text_lower = text.lower()

    detected = {}

    for section, keywords in SECTION_KEYWORDS.items():

        detected[section] = any(
            keyword in text_lower
            for keyword in keywords
        )

    return detected


def calculate_keyword_score(text):

    skills = extract_skills(text)

    # Maximum 20 points

    return min(
        len(skills) * 2,
        20
    )


def calculate_contact_score(text):

    score = 0

    if check_email(text):
        score += 5

    if check_phone(text):
        score += 5

    return score


def calculate_section_score(text):

    sections = detect_sections(text)

    # 7 sections × approximately 2 points

    score = sum(
        2
        for exists in sections.values()
        if exists
    )

    return min(score, 14)


def calculate_experience_score(text):

    text_lower = text.lower()

    score = 0

    experience_patterns = [
        r"\b\d+\+?\s*(years?|yrs?)\b",
        r"\bintern(ship)?\b",
        r"\bdeveloper\b",
        r"\bengineer\b",
        r"\banalyst\b",
        r"\bmanager\b"
    ]

    for pattern in experience_patterns:

        if re.search(
            pattern,
            text_lower
        ):

            score += 2

    return min(score, 10)


def calculate_action_score(text):

    text_lower = text.lower()

    count = 0

    for word in ACTION_WORDS:

        count += len(
            re.findall(
                r"\b" + re.escape(word) + r"\b",
                text_lower
            )
        )

    return min(
        count,
        10
    )


def calculate_length_score(text):

    word_count = len(
        text.split()
    )

    if 500 <= word_count <= 1000:
        return 10

    if 300 <= word_count < 500:
        return 8

    if 1000 < word_count <= 1400:
        return 8

    if 200 <= word_count < 300:
        return 5

    return 2


def calculate_format_score(text):

    score = 0

    sections = detect_sections(text)

    # Basic structure

    if sections["summary"]:
        score += 2

    if sections["skills"]:
        score += 2

    if sections["experience"]:
        score += 2

    if sections["education"]:
        score += 2

    if sections["projects"]:
        score += 2

    return min(
        score,
        10
    )


def calculate_ats_score(text):

    contact_score = calculate_contact_score(text)

    keyword_score = calculate_keyword_score(text)

    section_score = calculate_section_score(text)

    experience_score = calculate_experience_score(text)

    action_score = calculate_action_score(text)

    length_score = calculate_length_score(text)

    format_score = calculate_format_score(text)

    breakdown = {

        "Contact Information":
            contact_score,

        "Keywords & Skills":
            keyword_score,

        "Resume Sections":
            section_score,

        "Experience":
            experience_score,

        "Action Verbs":
            action_score,

        "Resume Length":
            length_score,

        "Structure & Format":
            format_score
    }

    score = sum(
        breakdown.values()
    )

    score = min(
        score,
        100
    )

    skills = extract_skills(text)

    return score, skills, breakdown


def generate_suggestions(
    text,
    skills,
    job_match_score=None
):

    suggestions = []

    text_lower = text.lower()

    sections = detect_sections(text)

    if not check_email(text):

        suggestions.append(
            "Add a professional email address to your resume."
        )

    if not check_phone(text):

        suggestions.append(
            "Add a valid phone number so recruiters can contact you."
        )

    if not sections["summary"]:

        suggestions.append(
            "Add a concise professional summary highlighting your strengths and career goals."
        )

    if not sections["skills"]:

        suggestions.append(
            "Create a dedicated Skills section containing relevant technical skills."
        )

    if not sections["experience"]:

        suggestions.append(
            "Add internship, employment, freelance, or practical experience."
        )

    if not sections["projects"]:

        suggestions.append(
            "Add 2–4 relevant projects with technologies and measurable results."
        )

    if not sections["education"]:

        suggestions.append(
            "Add your educational qualifications."
        )

    if not sections["certifications"]:

        suggestions.append(
            "Consider adding relevant certifications, courses, or training."
        )

    word_count = len(
        text.split()
    )

    if word_count < 300:

        suggestions.append(
            "Your resume is quite short. Add relevant achievements, projects, skills, or experience."
        )

    elif word_count > 1400:

        suggestions.append(
            "Your resume is lengthy. Remove repetitive or less relevant information."
        )

    action_count = 0

    for word in ACTION_WORDS:

        action_count += len(
            re.findall(
                r"\b" + re.escape(word) + r"\b",
                text_lower
            )
        )

    if action_count < 3:

        suggestions.append(
            "Use stronger action verbs such as Developed, Designed, Implemented, Optimized, and Automated."
        )

    if len(skills) < 5:

        suggestions.append(
            "Add more relevant technical and professional skills."
        )

    if (
        job_match_score is not None
        and job_match_score < 60
    ):

        suggestions.append(
            "Your resume has a low job-description match. Add relevant keywords and skills from the target job."
        )

    if not suggestions:

        suggestions.append(
            "Your resume looks strong. Continue tailoring it to each specific job description."
        )

    return suggestions