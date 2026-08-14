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


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "ai-resume-analyzer-secret"
)


# =========================================================
# CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


# Create uploads folder

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# FILE VALIDATION
# =========================================================

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


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# RESUME ANALYSIS
# =========================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    # -----------------------------------------------------
    # Check uploaded file
    # -----------------------------------------------------

    if "resume" not in request.files:

        flash(
            "Please upload a resume.",
            "error"
        )

        return redirect(
            url_for("index")
        )


    resume_file = request.files["resume"]


    # -----------------------------------------------------
    # Job description
    # -----------------------------------------------------

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()


    # -----------------------------------------------------
    # Check filename
    # -----------------------------------------------------

    if resume_file.filename == "":

        flash(
            "Please select a resume file.",
            "error"
        )

        return redirect(
            url_for("index")
        )


    # -----------------------------------------------------
    # Check file extension
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Secure filename
    # -----------------------------------------------------

    filename = secure_filename(
        resume_file.filename
    )


    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )


    # -----------------------------------------------------
    # Save uploaded resume
    # -----------------------------------------------------

    try:

        resume_file.save(
            file_path
        )

    except Exception as error:

        print(
            "File save error:",
            error
        )

        flash(
            "Unable to upload the resume.",
            "error"
        )

        return redirect(
            url_for("index")
        )


    # =====================================================
    # EXTRACT RESUME TEXT
    # =====================================================

    try:

        resume_text = extract_text(
            file_path
        )

        resume_text = clean_text(
            resume_text
        )

    except Exception as error:

        print(
            "Resume parsing error:",
            error
        )

        resume_text = ""


    # -----------------------------------------------------
    # Check extracted text
    # -----------------------------------------------------

    if not resume_text:

        try:

            os.remove(
                file_path
            )

        except Exception:
            pass


        flash(
            "Could not extract text from the resume. "
            "Please upload a valid PDF or DOCX file.",
            "error"
        )

        return redirect(
            url_for("index")
        )


    # =====================================================
    # EXTRACT CANDIDATE INFORMATION
    # =====================================================

    try:

        resume_info = extract_resume_information(
            resume_text
        )

    except Exception as error:

        print(
            "Resume information error:",
            error
        )

        resume_info = {}


    # =====================================================
    # ATS SCORE
    # =====================================================

    try:

        ats_score, skills, ats_breakdown = calculate_ats_score(
            resume_text
        )

    except Exception as error:

        print(
            "ATS scoring error:",
            error
        )

        ats_score = 0

        skills = []

        ats_breakdown = {}


    # =====================================================
    # JOB MATCHING
    # =====================================================

    job_result = {

        "similarity_score": 0,

        "matching_skills": [],

        "missing_skills": []

    }


    if job_description:

        try:

            job_result = analyze_job_match(
                resume_text,
                job_description
            )

        except Exception as error:

            print(
                "Job matching error:",
                error
            )

            job_result = {

                "similarity_score": 0,

                "matching_skills": [],

                "missing_skills": []

            }


    # =====================================================
    # SUGGESTIONS
    # =====================================================

    try:

        suggestions = generate_suggestions(
            resume_text,
            skills,
            job_result.get(
                "similarity_score",
                0
            )
        )

    except Exception as error:

        print(
            "Suggestion generation error:",
            error
        )

        suggestions = []


    # =====================================================
    # DELETE TEMPORARY RESUME
    # =====================================================

    try:

        os.remove(
            file_path
        )

    except Exception as error:

        print(
            "File cleanup error:",
            error
        )


    # =====================================================
    # RESULT PAGE
    # =====================================================

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


# =========================================================
# FILE TOO LARGE ERROR
# =========================================================

@app.errorhandler(413)
def file_too_large(error):

    flash(
        "File is too large. Maximum allowed size is 10 MB.",
        "error"
    )

    return redirect(
        url_for("index")
    )


# =========================================================
# GENERAL ERROR
# =========================================================

@app.errorhandler(500)
def internal_error(error):

    print(
        "Internal server error:",
        error
    )

    return """
    <h1>Something went wrong</h1>
    <p>Please try again.</p>
    """, 500


# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),

        debug=False

    )