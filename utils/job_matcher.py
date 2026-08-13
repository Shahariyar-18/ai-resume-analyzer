from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .ats_score import extract_skills


def calculate_similarity(
    resume_text,
    job_description
):

    if (
        not resume_text.strip()
        or not job_description.strip()
    ):
        return 0

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:

        vectors = vectorizer.fit_transform(
            documents
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(
            similarity * 100,
            2
        )

    except Exception:

        return 0


def find_matching_skills(
    resume_text,
    job_description
):

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_description)
    )

    matching = sorted(
        resume_skills.intersection(
            job_skills
        )
    )

    missing = sorted(
        job_skills - resume_skills
    )

    return matching, missing


def analyze_job_match(
    resume_text,
    job_description
):

    similarity_score = calculate_similarity(
        resume_text,
        job_description
    )

    matching_skills, missing_skills = (
        find_matching_skills(
            resume_text,
            job_description
        )
    )

    return {
        "similarity_score": similarity_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }