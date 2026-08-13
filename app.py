import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from werkzeug.utils import secure_filename

from utils.resume_parser import (
    extract_text,
    clean_text,
    extract_resume_information
)

from utils.ats_score import (
    calculate_ats_score,
    generate_suggestions
)

from utils.job_matcher import (
    analyze_job_match
)


app = Flask(__name__)

app.secret_key = "ai-resume-analyzer-secret"

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/")
def index():

    return render_template(
        "index.html"
    )


@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    if "resume" not in request.files:

        flash(
            "Please upload a resume.",
            "error"
        )

        return redirect(
            url_for("index")
        )

    resume_file = request.files["resume"]

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()

    if resume_file.filename == "":

        flash(
            "Please select a resume file.",
            "error"
        )

        return redirect(
            url_for("index")
        )

    if not allowed_file(
        resume_file.filename
    ):

        flash(
            "Only PDF and DOCX files are supported.",
            "error"
        )

        return redirect(
            url_for("index")
        )

    filename = secure_filename(
        resume_file.filename
    )

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    resume_file.save(file_path)

    # Extract resume text

    resume_text = extract_text(
        file_path
    )

    resume_text = clean_text(
        resume_text
    )

    if not resume_text:

        flash(
            "Could not extract text from the resume.",
            "error"
        )

        return redirect(
            url_for("index")
        )

    # Candidate information

    resume_info = extract_resume_information(
        resume_text
    )

    # ATS score

    ats_score, skills, ats_breakdown = calculate_ats_score(
        resume_text
    )

    # Job matching

    job_result = {
        "similarity_score": 0,
        "matching_skills": [],
        "missing_skills": []
    }

    if job_description:

        job_result = analyze_job_match(
            resume_text,
            job_description
        )

    # Suggestions

    suggestions = generate_suggestions(
        resume_text,
        skills,
        job_result["similarity_score"]
    )

    # Remove uploaded file

    try:
        os.remove(file_path)

    except Exception:
        pass

    return render_template(
    "result.html",
    resume_info=resume_info,
    ats_score=ats_score,
    ats_breakdown=ats_breakdown,
    skills=skills,
    suggestions=suggestions,
    job_result=job_result,
    resume_text=resume_text
)


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )