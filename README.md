# 📄 AI Resume Screening & Candidate Ranking System

An intelligent, production-ready AI Resume Screening and Candidate Ranking application developed with **Python**, **Streamlit**, **NLP**, **Scikit-learn (TF-IDF & Cosine Similarity)**, and **PyPDF**.

The system enables recruiters, hiring managers, and HR teams to rapidly screen multiple candidate PDF resumes against any target job description, automatically extracting key information (candidate skills, contact details, education, work experience), computing transparent match scores (0 to 100), identifying missing skill gaps, and ranking candidates from best to lowest match.

---

## 🌟 Key Features

- **Modern Clean Light Theme**: Curated luminous light palette with white cards, subtle shadows, crisp slate typography (`Plus Jakarta Sans`), and color-coded status accents.
- **Accurate Multi-PDF Text Extraction**: Uses `pypdf` to extract text from multi-page PDF resumes with cleanup for line breaks, special characters, and formatting.
- **NLP Information & Skill Parsing**:
  - Automatically extracts candidate **Name**, **Email**, **Phone number**, and **Portfolio/LinkedIn/GitHub links**.
  - Recognizes hundreds of technical, cloud, data science, web development, and soft skills using a curated taxonomy.
  - Extracts degree information (Bachelor's, Master's, Ph.D, etc.) and estimated years of professional experience.
- **Custom Must-Have Skills Adder**:
  - Recruiters can add extra mandatory skills to the evaluation via a multi-select dropdown to enforce criteria beyond what was in the JD text.
- **Scikit-Learn TF-IDF & Cosine Similarity Engine**:
  - Unigram and bigram TF-IDF vectorization with sublinear scaling and stop words filtering.
  - Computes semantic cosine similarity between the job description and candidate resumes.
- **Skill Alignment & Gap Analysis**:
  - Direct comparison of candidate skills against job requirements.
  - Categorizes skills into **Matching Skills** (green badges) and **Missing Skills** (red/amber badges).
  - Highlights additional bonus skills brought by candidates.
- **Candidate Shortlisting & Bookmarks**:
  - Click **"⭐ Shortlist"** directly on any candidate card to pin them for final hiring committee review.
  - Filter view to show only shortlisted candidates with one click.
- **Calibrated Multi-Factor Scoring (0 to 100)**:
  - Skill Coverage: 50%
  - TF-IDF Semantic Content Similarity: 35%
  - Profile & Experience Completeness: 15%
  - *Weights are fully customizable via interactive sliders in the sidebar.*
- **Visual Match Tiers**:
  - 🟢 **Exceptional Match** (75 - 100%)
  - 🔵 **Strong Match** (55 - 74%)
  - 🟡 **Moderate Match** (35 - 54%)
  - 🔴 **Low Match** (< 35%)
- **Recruiter Intelligence Hub (4 Feature-Rich Tabs)**:
  1. **🏆 Ranked Leaderboard & Profiles**: Comprehensive summary table, candidate cards with contact links, score breakdowns, and full extracted text reader.
  2. **📊 Visual Analytics & Skill Gap Insights**: Interactive bar charts for candidate score comparisons, score component breakdowns, and a **Pool-wide Skill Demand vs. Supply Matrix**.
  3. **⚖️ Side-by-Side Comparison**: Head-to-head comparison of any two candidates across scores, cosine similarity, matching skills, and education.
  4. **📝 AI Recruiter Briefing & Questions**: Executive briefing identifying top recommendations and tailored technical interview questions targeting candidate skill gaps.
- **Dual CSV Report Exports**:
  - **Download All CSV**: Exports the full ranking report of all evaluated candidates.
  - **Shortlisted Only CSV**: Exports only the bookmarked candidates for the hiring manager.
- **1-Click Synthetic Demo Resumes**:
  - Built-in synthetic PDF resume generator (`sample_generator.py`) providing 5 diverse candidate profiles for testing without needing manual uploads.
- **Privacy & Ethical AI Protection**:
  - 100% local in-memory processing. Resumes are never stored on or transmitted to external servers.
  - Match scores are presented as **decision-support indicators** to assist human review, preserving human-in-the-loop hiring decisions.

---

## 📁 Project Structure

```
AI-Resume-Srceening-system project/
│
├── .streamlit/
│   └── config.toml            # Light theme configuration
├── app.py                     # Main Streamlit dashboard application
├── extractor.py               # PDF text extraction and NLP entity parser
├── matcher.py                 # NLP matching engine, TF-IDF vectorizer & cosine similarity
├── skills_db.py               # Comprehensive taxonomy of technical, data, cloud, & web skills
├── sample_generator.py        # Synthetic PDF resume generator using ReportLab
├── test_pipeline.py           # Verification script for end-to-end pipeline
├── requirements.txt           # Project dependencies
├── sample_resumes/            # Generated synthetic sample PDF resumes for demo
│   ├── alex_rivera_senior_ml_engineer.pdf
│   ├── priya_patel_fullstack_python.pdf
│   ├── david_kim_junior_data_analyst.pdf
│   ├── sarah_connor_devops_cloud.pdf
│   └── emily_watson_marketing_specialist.pdf
└── README.md                  # System documentation & setup guide
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** (Python 3.10, 3.11, 3.12, 3.13, or 3.14) installed.

### 2. Install Dependencies
Open your terminal or PowerShell in the project directory:

```bash
python -m pip install -r requirements.txt
```

*(Or install directly)*:
```bash
python -m pip install streamlit scikit-learn pypdf pandas reportlab
```

### 3. Generate Synthetic Sample Resumes (Optional)
The system includes sample PDF resumes for testing:
```bash
python sample_generator.py
```

### 4. Launch the Streamlit Application
Run the following command in your terminal:

```bash
python -m streamlit run app.py
```

The application will open automatically in your browser at:
```
http://localhost:8501
```

---

## 💡 How to Use the System

1. **Step 1: Enter Job Description & Must-Have Skills**
   - Paste any job description into the text area, **OR**
   - Select a sample pre-loaded benchmark job description from the dropdown (e.g. *Senior Machine Learning & NLP Engineer*).
   - Optionally pick extra must-have skills from the dropdown to enforce criteria.
2. **Step 2: Upload Resumes**
   - Upload multiple PDF resumes using the file uploader, **OR**
   - Click **"🚀 Load 5 Synthetic Demo Resumes"** for instant demonstration with realistic resumes.
3. **Step 3: Explore the Intelligence Tabs**
   - **Leaderboard**: Inspect ranked candidates and deep-dive into skill badges and contact info.
   - **Shortlisting**: Click **"⭐ Shortlist"** on top candidates.
   - **Visual Analytics**: Review match distributions and pool-wide skill shortages.
   - **Side-by-Side**: Compare candidates head-to-head.
   - **Recruiter Briefing**: Review interview questions generated based on missing skill gaps.
4. **Step 4: Filter & Export**
   - Use the sidebar sliders to adjust the minimum score threshold or customize scoring weights.
   - Click **"📥 Download All CSV"** or **"⭐ Shortlisted Only"** to export findings.

---

## 🔒 Privacy & Ethical AI Principles

- **Local Execution**: All PDF processing and text extraction occur strictly on your local machine in memory.
- **Decision-Support Tool**: Matching scores are designed to assist human recruiters in organizing applications. They do not replace human discernment, diversity considerations, or holistic interviews.
