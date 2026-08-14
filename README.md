# 🤖 AI Resume Analyzer

> An AI-powered resume analysis and job matching web application built with Python, Flask, NLP, and Machine Learning.

AI Resume Analyzer helps candidates evaluate their resumes by analyzing ATS compatibility, extracting skills, comparing resumes with job descriptions, identifying missing keywords, and providing useful resume insights through a modern and responsive web interface.

---
## 🌐 Live Demo

Try the AI resume analyzer:

👉https://ai-resume-analyzer-1-74sw.onrender.com/

## ✨ Features

- 📄 Upload **PDF and DOCX** resumes
- 🤖 AI-powered resume analysis
- 📊 ATS compatibility scoring
- 🧠 Resume skill extraction
- 🎯 Job description matching
- 🔍 Keyword matching
- ⚠️ Missing keyword detection
- 💼 Job compatibility analysis
- 📋 Resume text extraction
- 📈 Resume strength analysis
- 💡 Resume improvement suggestions
- 🖱️ Drag & drop resume upload
- 📁 File selection and validation
- ⚡ Flask-based backend
- 🎨 Modern and professional UI
- 📱 Responsive design
- 🔄 Loading state during resume analysis
- 📊 Dedicated analysis result page

---

## 🖥️ Application Workflow

```text
                 ┌────────────────────┐
                 │    Upload Resume   │
                 │      PDF / DOCX    │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │   Resume Parser    │
                 │   Text Extraction  │
                 └─────────┬──────────┘
                           │
                           ▼
              ┌────────────────────────────┐
              │      Resume Analysis       │
              └─────────────┬──────────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       ┌───────────┐  ┌────────────┐  ┌────────────┐
       │ ATS Score │  │   Skills   │  │  Keywords  │
       │           │  │ Extraction │  │  Analysis  │
       └─────┬─────┘  └──────┬─────┘  └──────┬─────┘
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                  ┌────────────────────┐
                  │   Job Description  │
                  │      Matching      │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │  Analysis Results  │
                  │ ATS • Skills •     │
                  │ Job Match • Tips   │
                  └────────────────────┘
```

---

## 🎯 Project Objectives

The main objectives of the AI Resume Analyzer are:

- Automate the initial resume analysis process
- Evaluate resume ATS compatibility
- Extract relevant technical and professional skills
- Compare resumes with specific job descriptions
- Identify matching and missing keywords
- Calculate job compatibility
- Help candidates understand their resume strengths
- Provide suggestions for improving resume content
- Create a simple and user-friendly resume analysis platform

---

## 🛠️ Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Responsive Web Design
- Drag & Drop API

### Backend

- Python
- Flask
- Gunicorn

### AI / Machine Learning

- Natural Language Processing (NLP)
- Machine Learning
- Keyword Matching
- Text Analysis
- Scikit-learn

### Resume Processing

- PyMuPDF
- python-docx

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Python Virtual Environment

### Deployment

- Render
- Gunicorn

---

## 📁 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── uploads/
│   └── .gitkeep
│
├── utils/
│   ├── __init__.py
│   ├── resume_parser.py
│   ├── ats_score.py
│   └── job_matcher.py
│
├── templates/
│   ├── index.html
│   └── result.html
│
└── static/
    │
    ├── css/
    │   ├── style.css
    │   └── result.css
    │
    └── js/
        └── script.js
```

## 📊 ATS Analysis

The ATS analyzer evaluates the resume based on relevant resume information and job-description matching.

The analysis can include:

- ATS Score
- Matching Keywords
- Missing Keywords
- Relevant Skills
- Resume Strengths
- Resume Weaknesses
- Job Compatibility
- Improvement Suggestions

### Example

```text
ATS SCORE

████████████████░░░░  82%

JOB COMPATIBILITY

██████████████████░░  91%

MATCHING SKILLS

✓ Python
✓ Flask
✓ SQL
✓ Machine Learning
✓ Git

MISSING SKILLS

• REST API
• Docker
```

## 📄 Supported Resume Formats

| Format | Supported |
|--------|-----------|
| PDF | ✅ |
| DOCX | ✅ |
| DOC | ❌ |
| TXT | ❌ |
| Images | ❌ |

**Maximum file size:** 10 MB


## 👨‍💻 Author

**Shahariyar Khan**

Computer Science & Engineering — Artificial Intelligence

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

Your support helps improve and expand the project.

