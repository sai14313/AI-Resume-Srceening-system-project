"""
AI Resume Screening & Candidate Ranking System.
A Streamlit application utilizing NLP, PyPDF, Scikit-Learn TF-IDF,
and Cosine Similarity for intelligent candidate screening, skill-gap analysis,
shortlisting, and recruiter intelligence in a clean modern Light Theme.
"""

import os
import io
import pandas as pd
import streamlit as st

from extractor import parse_resume, extract_skills
from matcher import screen_resumes, get_match_tier
from sample_generator import generate_all_sample_resumes, SAMPLE_RESUMES_DATA
from skills_db import ALL_SKILLS
from extractor import format_skill_name

# Custom Light Theme Styling
CUSTOM_LIGHT_CSS = """
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Typography & Base Settings */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #0f172a;
    }
    
    .stApp {
        background-color: #f8fafc;
    }

    /* Header styling */
    .hero-banner {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.02);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #1e293b 0%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.35rem;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #475569;
        font-weight: 500;
        line-height: 1.5;
    }

    /* Metric Cards - Modern Light Theme */
    .metric-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.3rem 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: #2563eb;
    }
    .metric-card.accent-emerald::before { background: #10b981; }
    .metric-card.accent-violet::before { background: #8b5cf6; }
    .metric-card.accent-amber::before { background: #f59e0b; }

    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.35rem;
    }

    /* Skill badges / chips */
    .skill-chip {
        display: inline-flex;
        align-items: center;
        padding: 4px 11px;
        margin: 3px 5px 5px 0;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        transition: all 0.15s ease;
    }
    .skill-matched {
        background-color: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
    }
    .skill-missing {
        background-color: #fff1f2;
        color: #be123c;
        border: 1px solid #fecdd3;
    }
    .skill-extra {
        background-color: #f8fafc;
        color: #334155;
        border: 1px solid #cbd5e1;
    }

    /* Privacy Banner */
    .privacy-notice {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        border-left: 5px solid #2563eb;
        padding: 1rem 1.4rem;
        border-radius: 12px;
        font-size: 0.9rem;
        color: #1e3a8a;
        margin-bottom: 1.75rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }

    /* Candidate Profile Box */
    .candidate-profile-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.4rem;
        margin-top: 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    
    /* Shortlist Tag */
    .shortlist-badge {
        background-color: #fef3c7;
        color: #b45309;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 12px;
        font-size: 0.78rem;
        border: 1px solid #fde68a;
    }

    /* Light Theme Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        color: #475569;
        padding: 8px 18px;
        background-color: transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #2563eb !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
</style>
"""


SAMPLE_JOB_DESCRIPTIONS = {
    "Senior Machine Learning & NLP Engineer": """
Role: Senior Machine Learning Engineer (NLP Focus)
Company: NextGen AI Solutions
Location: Remote / Hybrid

We are seeking an experienced Senior Machine Learning & NLP Engineer to lead the development of enterprise intelligence applications.
Key Responsibilities:
- Design, train, and deploy high-performance NLP models utilizing Python, PyTorch, Scikit-Learn, and Hugging Face Transformers.
- Build semantic search and text retrieval pipelines incorporating TF-IDF, embeddings, and cosine similarity.
- Develop scalable REST APIs using FastAPI/Flask and containerize microservices with Docker on AWS.
- Collaborate with cross-functional teams in an Agile Scrum environment.
- Lead code reviews, implement unit testing, and maintain automated CI/CD deployment pipelines.

Required Skills & Qualifications:
- Bachelor's or Master's degree in Computer Science, AI, or related quantitative field.
- 5+ years of hands-on experience in Machine Learning and Natural Language Processing.
- Proficient in Python, Pandas, NumPy, Scikit-Learn, PyTorch, Docker, AWS, Git, and PostgreSQL.
- Experience with TF-IDF, Transformers, and REST API development.
""",
    "Full-Stack Python & Web Developer": """
Role: Full Stack Python Developer
Company: CloudPulse Systems
Location: New York, NY

We are hiring a versatile Full Stack Developer to build robust, data-centric web platforms.
Responsibilities:
- Build and maintain modern web applications using Python, Django, FastAPI, and React.
- Design normalized relational databases with PostgreSQL and implement Redis caching.
- Build clean RESTful APIs and integrate frontend UI components with backend microservices.
- Write unit tests and maintain CI/CD pipelines on AWS with Docker.

Required Skills & Qualifications:
- Degree in Computer Science, Software Engineering, or equivalent experience.
- 3+ years of experience with Python, React, JavaScript, HTML5, CSS3, and REST APIs.
- Experience with PostgreSQL, Redis, Docker, Git, and Agile development methodologies.
""",
    "Cloud DevOps & Infrastructure Engineer": """
Role: Senior DevOps & Cloud Platform Engineer
Company: Apex Cloud
Location: Austin, TX

Looking for an expert Cloud DevOps Engineer to scale infrastructure and automate CI/CD deployments.
Responsibilities:
- Architect and manage scalable Kubernetes (EKS) and Docker infrastructure on AWS.
- Automate provisioning and configuration using Terraform and Ansible.
- Build robust CI/CD pipelines using Jenkins and GitHub Actions.
- Monitor system health, performance, and alerts with Prometheus and Grafana.

Required Skills:
- 4+ years of DevOps engineering experience.
- Strong proficiency in AWS, Docker, Kubernetes, Linux, Terraform, Ansible, CI/CD, Jenkins, and Python scripting.
- Experience with Git, Bash, and infrastructure monitoring.
""",
    "Data Analyst & Business Intelligence Specialist": """
Role: Data Analyst
Company: Insight Metrics
Location: Chicago, IL

We are seeking a detail-driven Data Analyst to transform complex datasets into actionable business intelligence.
Responsibilities:
- Query relational databases using SQL to extract and transform large transactional datasets.
- Clean, analyze, and model data using Python, Pandas, and Scikit-Learn.
- Build dashboards and reports using Tableau and Excel.
- Present statistical findings and data visualizations to key business stakeholders.

Required Skills:
- Bachelor's degree in Statistics, Data Science, Mathematics, or Economics.
- Proficiency in SQL, Python, Pandas, NumPy, Data Analysis, Matplotlib, Tableau, and Excel.
"""
}


def main():
    # Set Streamlit page configuration
    st.set_page_config(
        page_title="AI Resume Screening & Candidate Ranking System",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(CUSTOM_LIGHT_CSS, unsafe_allow_html=True)

    # Initialize session state for shortlist if not present
    if "shortlist" not in st.session_state:
        st.session_state.shortlist = set()

    # Sidebar: Light Theme Controls
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/artificial-intelligence.png", width=56)
        st.markdown("### **Resume Screener AI**")
        st.caption("AI-Powered Candidate Ranking & ATS Intelligence")
        
        st.markdown("---")
        st.subheader("⚙️ Scoring Model Weights")
        w_skills = st.slider("Skill Match Weight (%)", 10, 80, 50, 5, help="Direct coverage of required skills")
        w_tfidf = st.slider("TF-IDF Semantic Similarity (%)", 10, 80, 35, 5, help="Semantic cosine similarity from text")
        w_profile = st.slider("Profile & Credentials (%)", 0, 40, 15, 5, help="Education degree and work experience")

        st.markdown("---")
        st.subheader("🔍 Filters & Search")
        min_score = st.slider("Minimum Match Score (%)", 0, 100, 0, 5)
        search_keyword = st.text_input("Search Candidate or Skill", "", placeholder="e.g. PyTorch, Docker, Rivera")
        only_shortlisted = st.checkbox("⭐ Show Shortlisted Candidates Only", False)

        st.markdown("---")
        st.markdown(f"**⭐ Shortlisted:** `{len(st.session_state.shortlist)} candidate(s)`")
        if st.session_state.shortlist:
            if st.button("Clear Shortlist", use_container_width=True):
                st.session_state.shortlist.clear()
                st.rerun()

        st.markdown("---")
        st.markdown("""
        **🛡️ Privacy & Security:**
        - ✅ Resumes processed strictly in-memory.
        - 🔒 Zero external API transmissions.
        - ⚖️ Decision-support intelligence only.
        """)

    # Main Hero Banner in Light Theme
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">📄 AI Resume Screening & Candidate Ranking System</div>
        <div class="hero-subtitle">Intelligent ATS Screening Engine powered by NLP, Scikit-Learn TF-IDF, Cosine Similarity, and Automated Skill Gap Analysis.</div>
    </div>
    """, unsafe_allow_html=True)

    # Privacy Banner
    st.markdown("""
    <div class="privacy-notice">
        <b>⚖️ Ethical AI & Privacy Safeguard:</b> Candidate match scores and skill ratings are designed as <b>decision-support indicators</b> to assist recruiters in prioritizing candidate reviews. Final hiring decisions must involve holistic human evaluation. All PDF resumes are parsed locally in-memory.
    </div>
    """, unsafe_allow_html=True)

    # Section 1: Job Description Input
    st.subheader("1. Target Job Requirements")
    
    col_preset, col_clear = st.columns([4, 1])
    with col_preset:
        selected_sample = st.selectbox(
            "📋 Or populate from curated industry benchmark descriptions:",
            ["-- Select a Sample Job Description or write custom --"] + list(SAMPLE_JOB_DESCRIPTIONS.keys())
        )
    with col_clear:
        if st.button("Reset Form", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    default_jd = ""
    if selected_sample in SAMPLE_JOB_DESCRIPTIONS:
        default_jd = SAMPLE_JOB_DESCRIPTIONS[selected_sample]

    jd_text = st.text_area(
        "Paste or edit Job Description requirements below:",
        value=default_jd,
        height=170,
        placeholder="Enter required responsibilities, technical skills, education criteria, and experience expectations..."
    )

    # Detect skills in JD in real-time
    detected_jd_skills = []
    if jd_text.strip():
        detected_jd_skills = extract_skills(jd_text)

    # Extra custom must-have skills adder
    col_extra_skills, col_view_skills = st.columns([3, 2])
    with col_extra_skills:
        extra_skills = st.multiselect(
            "➕ Add custom must-have skills (optional):",
            options=sorted(list(set([s.title() for s in ALL_SKILLS[:120]]))),
            help="Select additional mandatory skills you want to enforce beyond what was detected in the JD text"
        )

    # Combined target skills
    active_target_skills = list(detected_jd_skills)
    for ext in extra_skills:
        if ext.lower() not in [s.lower() for s in active_target_skills]:
            active_target_skills.append(ext)

    with col_view_skills:
        if active_target_skills:
            st.markdown(f"**Identified Target Skills ({len(active_target_skills)}):**")
            chips_html = " ".join([f'<span class="skill-chip skill-matched">{s}</span>' for s in active_target_skills[:10]])
            if len(active_target_skills) > 10:
                chips_html += f" <span class='skill-chip skill-extra'>+{len(active_target_skills)-10} more</span>"
            st.markdown(chips_html, unsafe_allow_html=True)
        else:
            st.caption("No target skills detected yet. Write or select a Job Description.")

    st.markdown("---")

    # Section 2: Resume Ingestion
    st.subheader("2. Upload Candidate Resumes (PDF)")

    col_upload, col_demo = st.columns([3, 2])
    with col_upload:
        uploaded_files = st.file_uploader(
            "Upload one or more candidate resumes (PDF format):",
            type=["pdf"],
            accept_multiple_files=True,
            help="Select multiple PDF resumes from your device"
        )

    with col_demo:
        st.markdown("**Quick Testing with Synthetic Resumes:**")
        st.markdown("Test all features instantly with 5 realistic synthetic candidate profiles:")
        load_demo = st.button("🚀 Load 5 Synthetic Demo Resumes", use_container_width=True, type="secondary")

    if "parsed_resumes" not in st.session_state:
        st.session_state.parsed_resumes = []

    # Handle demo loading
    if load_demo:
        with st.spinner("Generating and parsing synthetic sample resumes..."):
            samples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_resumes")
            if not os.path.exists(samples_dir) or len(os.listdir(samples_dir)) == 0:
                generate_all_sample_resumes(samples_dir)
            
            demo_parsed = []
            for item in SAMPLE_RESUMES_DATA:
                pdf_path = os.path.join(samples_dir, item["filename"])
                if os.path.exists(pdf_path):
                    parsed = parse_resume(pdf_path, filename=item["filename"])
                    demo_parsed.append(parsed)

            st.session_state.parsed_resumes = demo_parsed
            st.session_state.demo_mode = True
            st.success(f"Loaded {len(demo_parsed)} synthetic sample resumes successfully!")

    # Handle uploaded files
    if uploaded_files:
        with st.spinner(f"Parsing {len(uploaded_files)} uploaded resume(s)..."):
            uploaded_parsed = []
            for uploaded_file in uploaded_files:
                parsed = parse_resume(uploaded_file, filename=uploaded_file.name)
                uploaded_parsed.append(parsed)
            st.session_state.parsed_resumes = uploaded_parsed
            st.session_state.demo_mode = False

    parsed_candidates = st.session_state.get("parsed_resumes", [])

    if not parsed_candidates:
        st.info("👆 Please paste a job description and upload PDF resumes (or click 'Load 5 Synthetic Demo Resumes') to start screening.")
        return

    st.success(f"Ready: {len(parsed_candidates)} candidate resume(s) loaded into in-memory engine.")

    # Section 3: Evaluation & Screening Pipeline
    if not jd_text.strip():
        st.warning("⚠️ Please provide a Job Description above to evaluate and rank candidate resumes.")
        return

    with st.spinner("Running Scikit-Learn TF-IDF vectorization and skill alignment engine..."):
        ranked_candidates = screen_resumes(
            job_description=jd_text,
            parsed_candidates=parsed_candidates,
            weight_skills=float(w_skills),
            weight_tfidf=float(w_tfidf),
            weight_profile=float(w_profile),
            extra_required_skills=extra_skills
        )

    # Filter by threshold and search query
    filtered_candidates = [
        c for c in ranked_candidates
        if c["match_score"] >= min_score
    ]
    if only_shortlisted:
        filtered_candidates = [
            c for c in filtered_candidates
            if c["filename"] in st.session_state.shortlist
        ]
    if search_keyword.strip():
        kw = search_keyword.strip().lower()
        filtered_candidates = [
            c for c in filtered_candidates
            if kw in c["name"].lower()
            or any(kw in s.lower() for s in c.get("skills", []))
            or any(kw in s.lower() for s in c.get("matching_skills", []))
            or kw in c.get("email", "").lower()
        ]

    st.markdown("---")
    st.subheader("3. Screening Dashboard & Recruiter Intelligence")

    # Overview KPI Cards
    if ranked_candidates:
        top_cand = ranked_candidates[0]
        avg_score = round(sum(c["match_score"] for c in ranked_candidates) / len(ranked_candidates), 1)
        
        all_matched = []
        for c in ranked_candidates:
            all_matched.extend(c.get("matching_skills", []))
        most_common_skill = max(set(all_matched), key=all_matched.count) if all_matched else "None"

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(ranked_candidates)}</div>
                <div class="metric-label">Resumes Screened</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-card accent-emerald">
                <div class="metric-value" style="color: #059669;">{top_cand['match_score']}%</div>
                <div class="metric-label">Top Score ({top_cand['name'].split()[0]})</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="metric-card accent-violet">
                <div class="metric-value" style="color: #7c3aed;">{avg_score}%</div>
                <div class="metric-label">Average Match Score</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
            <div class="metric-card accent-amber">
                <div class="metric-value" style="color: #d97706; font-size: 1.5rem; padding-top: 6px;">{most_common_skill}</div>
                <div class="metric-label">Most Common Matched Skill</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4 Main Tabs
    tab_rankings, tab_analytics, tab_compare, tab_briefing = st.tabs([
        "🏆 Ranked Leaderboard & Profiles",
        "📊 Visual Analytics & Skill Gap Insights",
        "⚖️ Side-by-Side Comparison",
        "📝 AI Recruiter Briefing & Questions"
    ])

    # ================= TAB 1: RANKINGS & PROFILES =================
    with tab_rankings:
        # Leaderboard Summary Table
        table_rows = []
        for c in filtered_candidates:
            is_sl = "⭐ Yes" if c["filename"] in st.session_state.shortlist else "No"
            table_rows.append({
                "Rank": f"#{c['rank']}",
                "Shortlisted": is_sl,
                "Candidate Name": c["name"],
                "Match Score": f"{c['match_score']}%",
                "Tier": f"{c['tier_icon']} {c['match_tier']}",
                "Cosine Similarity": f"{c['cosine_similarity']}%",
                "Matched Skills": f"{c['matched_skills_count']} / {c['required_skills_count']}",
                "Email": c["email"],
                "Phone": c["phone"]
            })

        if table_rows:
            df_summary = pd.DataFrame(table_rows)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
        else:
            st.warning("No candidates match your current filter criteria.")

        # Export Section
        st.markdown("<br>", unsafe_allow_html=True)
        col_dl1, col_dl2, col_dl3 = st.columns([2, 1, 1])
        with col_dl1:
            st.markdown("💾 **Export Candidate Screening Reports:**")
            st.caption("Download structured CSV reports for recruitment pipelines and ATS archives.")
        
        # Build Export Data
        export_records = []
        for c in ranked_candidates:
            export_records.append({
                "Rank": c["rank"],
                "Candidate Name": c["name"],
                "Shortlisted": "Yes" if c["filename"] in st.session_state.shortlist else "No",
                "Match Score (0-100)": c["match_score"],
                "Match Tier": c["match_tier"],
                "Cosine Similarity (%)": c["cosine_similarity"],
                "Matched Skills Count": c["matched_skills_count"],
                "Required Skills Count": c["required_skills_count"],
                "Matching Skills List": "; ".join(c["matching_skills"]),
                "Missing Skills List": "; ".join(c["missing_skills"]),
                "Additional Skills List": "; ".join(c["additional_skills"]),
                "Email": c["email"],
                "Phone": c["phone"],
                "Education Summary": "; ".join(c["education"]),
                "Filename": c["filename"]
            })
        df_export_all = pd.DataFrame(export_records)

        with col_dl2:
            csv_buf_all = io.StringIO()
            df_export_all.to_csv(csv_buf_all, index=False)
            st.download_button(
                label="📥 Download All CSV",
                data=csv_buf_all.getvalue(),
                file_name="all_candidates_screening_report.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )

        with col_dl3:
            df_shortlist = df_export_all[df_export_all["Shortlisted"] == "Yes"]
            csv_buf_sl = io.StringIO()
            df_shortlist.to_csv(csv_buf_sl, index=False)
            st.download_button(
                label=f"⭐ Shortlisted Only ({len(df_shortlist)})",
                data=csv_buf_sl.getvalue(),
                file_name="shortlisted_candidates_report.csv",
                mime="text/csv",
                use_container_width=True,
                disabled=(len(df_shortlist) == 0)
            )

        st.markdown("---")
        st.subheader("Deep-Dive Candidate Profiles")

        for c in filtered_candidates:
            is_bookmarked = c["filename"] in st.session_state.shortlist
            bookmark_label = "⭐ Shortlisted" if is_bookmarked else "☆ Add to Shortlist"

            with st.expander(
                f"Rank #{c['rank']} — {c['name']}  |  Score: {c['match_score']}/100  |  {c['tier_icon']} {c['match_tier']} ({c['matched_skills_count']} matching skills)",
                expanded=(c["rank"] == 1)
            ):
                c_left, c_right = st.columns([3, 2])

                with c_left:
                    # Header row with Shortlist action
                    col_name, col_sl_btn = st.columns([3, 1])
                    with col_name:
                        st.markdown(f"### {c['name']}")
                    with col_sl_btn:
                        if st.button(bookmark_label, key=f"sl_btn_{c['filename']}_{c['rank']}"):
                            if is_bookmarked:
                                st.session_state.shortlist.remove(c["filename"])
                            else:
                                st.session_state.shortlist.add(c["filename"])
                            st.rerun()

                    st.markdown(f"**Source Document:** `{c['filename']}`")
                    st.markdown(f"📧 **Email:** [{c['email']}](mailto:{c['email']}) &nbsp;&nbsp;|&nbsp;&nbsp; 📞 **Phone:** `{c['phone']}`")
                    
                    if c.get("links"):
                        link_md = " &nbsp;|&nbsp; ".join([f"[{k}]({v})" for k, v in c["links"].items()])
                        st.markdown(f"🌐 **Profiles:** {link_md}")

                    st.markdown("---")
                    st.markdown("#### 🎯 Skill Breakdown")

                    # Matching Skills
                    st.markdown(f"**✅ Matching Skills ({len(c['matching_skills'])}):**")
                    if c["matching_skills"]:
                        matched_html = " ".join([f'<span class="skill-chip skill-matched">✓ {s}</span>' for s in c["matching_skills"]])
                        st.markdown(matched_html, unsafe_allow_html=True)
                    else:
                        st.caption("No direct skill matches found for job requirements.")

                    # Missing Skills
                    st.markdown(f"<br>**❌ Missing Job Requirements ({len(c['missing_skills'])}):**", unsafe_allow_html=True)
                    if c["missing_skills"]:
                        missing_html = " ".join([f'<span class="skill-chip skill-missing">✕ {s}</span>' for s in c["missing_skills"]])
                        st.markdown(missing_html, unsafe_allow_html=True)
                    else:
                        st.success("Candidate satisfies 100% of the recognized job requirements!")

                    # Additional Skills
                    if c.get("additional_skills"):
                        st.markdown(f"<br>**✨ Additional Discovered Skills ({len(c['additional_skills'])}):**", unsafe_allow_html=True)
                        extra_html = " ".join([f'<span class="skill-chip skill-extra">{s}</span>' for s in c["additional_skills"][:14]])
                        if len(c["additional_skills"]) > 14:
                            extra_html += f" <span class='skill-chip skill-extra'>+{len(c['additional_skills'])-14} more</span>"
                        st.markdown(extra_html, unsafe_allow_html=True)

                with c_right:
                    # Score Breakdown Card in Light Theme
                    st.markdown(f"""
                    <div style="background-color: #ffffff; border-radius: 12px; padding: 1.3rem; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 0.95rem; font-weight: 700; color: #334155;">Composite Score</span>
                            <span style="font-size: 2rem; font-weight: 800; color: {c['tier_color']};">{c['match_score']}/100</span>
                        </div>
                        <div style="margin-top: 2px; font-size: 0.88rem; color: {c['tier_color']}; font-weight: 700;">
                            {c['tier_icon']} {c['match_tier']}
                        </div>
                        <hr style="margin: 0.9rem 0; border: 0; border-top: 1px solid #f1f5f9;">
                        <div style="font-size: 0.85rem; color: #475569;">
                            <div style="display:flex; justify-content: space-between; margin-bottom: 6px;">
                                <span>Skill Coverage Score:</span>
                                <b style="color: #0f172a;">{c['score_breakdown']['skill_coverage_pct']}%</b>
                            </div>
                            <div style="display:flex; justify-content: space-between; margin-bottom: 6px;">
                                <span>TF-IDF Content Similarity:</span>
                                <b style="color: #0f172a;">{c['cosine_similarity']}%</b>
                            </div>
                            <div style="display:flex; justify-content: space-between; margin-bottom: 6px;">
                                <span>Calibrated Semantic Fit:</span>
                                <b style="color: #0f172a;">{c['score_breakdown']['calibrated_content_alignment']}%</b>
                            </div>
                            <div style="display:flex; justify-content: space-between; margin-bottom: 6px;">
                                <span>Profile Credential Points:</span>
                                <b style="color: #0f172a;">{c['score_breakdown']['profile_factor_points']} pts</b>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("#### 🎓 Education & Experience")
                    for edu in c.get("education", []):
                        st.markdown(f"- {edu}")

                    exp_data = c.get("experience", {})
                    est_years = exp_data.get("estimated_years")
                    if est_years:
                        st.markdown(f"💼 **Estimated Experience:** ~{est_years} years")

                # Extracted Text Viewer
                with st.expander("📄 View Extracted PDF Text", expanded=False):
                    st.text_area(
                        f"Raw Text Extracted from {c['filename']}:",
                        c.get("raw_text", ""),
                        height=180,
                        key=f"text_view_{c['filename']}_{c['rank']}"
                    )

    # ================= TAB 2: VISUAL ANALYTICS =================
    with tab_analytics:
        st.subheader("Candidate Pool Visual Analytics")
        col_ch1, col_ch2 = st.columns(2)

        with col_ch1:
            st.markdown("#### 📈 Candidate Match Score Comparison")
            chart_df = pd.DataFrame({
                "Candidate": [c["name"] for c in ranked_candidates],
                "Match Score (%)": [c["match_score"] for c in ranked_candidates]
            }).set_index("Candidate")
            st.bar_chart(chart_df, color="#2563eb")

        with col_ch2:
            st.markdown("#### 🔍 Scoring Factors Breakdown")
            component_df = pd.DataFrame({
                "Candidate": [c["name"] for c in ranked_candidates],
                "Skill Coverage (%)": [c["score_breakdown"]["skill_coverage_pct"] for c in ranked_candidates],
                "Semantic Fit (%)": [c["score_breakdown"]["calibrated_content_alignment"] for c in ranked_candidates]
            }).set_index("Candidate")
            st.bar_chart(component_df)

        st.markdown("---")
        st.subheader("🎯 Required Skill Demand vs. Candidate Supply")
        st.caption("Shows how many candidates in your pool possess each skill required by the Job Description.")

        target_skill_set = active_target_skills if active_target_skills else detected_jd_skills
        if target_skill_set:
            skill_counts = []
            for skill in target_skill_set:
                matching_count = sum(
                    1 for c in ranked_candidates
                    if any(skill.lower() == s.lower() for s in c.get("matching_skills", []))
                )
                skill_counts.append({
                    "Skill": skill,
                    "Candidates with Skill": matching_count,
                    "Coverage Percentage": round((matching_count / len(ranked_candidates)) * 100, 1)
                })

            df_skill_supply = pd.DataFrame(skill_counts).sort_values(by="Candidates with Skill", ascending=False)
            st.bar_chart(df_skill_supply.set_index("Skill")["Candidates with Skill"], color="#10b981")
            
            with st.expander("📋 View Detailed Skill Supply Data Table"):
                st.dataframe(df_skill_supply, use_container_width=True, hide_index=True)
        else:
            st.info("No explicit target skills identified to generate skill supply chart.")

    # ================= TAB 3: SIDE-BY-SIDE COMPARISON =================
    with tab_compare:
        st.subheader("⚖️ Side-by-Side Candidate Comparator")
        st.caption("Select two candidates to compare their qualifications, skills, and scoring factors side-by-side.")

        candidate_names = [c["name"] for c in ranked_candidates]
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            cand1_name = st.selectbox("Select Candidate A:", candidate_names, index=0)
        with col_sel2:
            default_cand2_idx = 1 if len(candidate_names) > 1 else 0
            cand2_name = st.selectbox("Select Candidate B:", candidate_names, index=default_cand2_idx)

        c1 = next(c for c in ranked_candidates if c["name"] == cand1_name)
        c2 = next(c for c in ranked_candidates if c["name"] == cand2_name)

        col_cmp1, col_cmp2 = st.columns(2)
        
        with col_cmp1:
            st.markdown(f"""
            <div class="candidate-profile-box">
                <h3 style="margin-top:0;">{c1['name']} (#{c1['rank']})</h3>
                <div style="font-size: 1.8rem; font-weight: 800; color: {c1['tier_color']};">{c1['match_score']}%</div>
                <div style="font-weight: 600; color: {c1['tier_color']};">{c1['tier_icon']} {c1['match_tier']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**Email:** `{c1['email']}`")
            st.markdown(f"**Phone:** `{c1['phone']}`")
            st.markdown(f"**Matched Skills ({len(c1['matching_skills'])}):**")
            if c1['matching_skills']:
                st.markdown(" ".join([f'<span class="skill-chip skill-matched">✓ {s}</span>' for s in c1['matching_skills']]), unsafe_allow_html=True)
            else:
                st.caption("None")

            st.markdown(f"<br>**Missing Skills ({len(c1['missing_skills'])}):**", unsafe_allow_html=True)
            if c1['missing_skills']:
                st.markdown(" ".join([f'<span class="skill-chip skill-missing">✕ {s}</span>' for s in c1['missing_skills']]), unsafe_allow_html=True)
            else:
                st.success("None (100% Coverage)")

            st.markdown("<br>**Education Background:**", unsafe_allow_html=True)
            for e in c1.get("education", []):
                st.markdown(f"- {e}")

        with col_cmp2:
            st.markdown(f"""
            <div class="candidate-profile-box">
                <h3 style="margin-top:0;">{c2['name']} (#{c2['rank']})</h3>
                <div style="font-size: 1.8rem; font-weight: 800; color: {c2['tier_color']};">{c2['match_score']}%</div>
                <div style="font-weight: 600; color: {c2['tier_color']};">{c2['tier_icon']} {c2['match_tier']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**Email:** `{c2['email']}`")
            st.markdown(f"**Phone:** `{c2['phone']}`")
            st.markdown(f"**Cosine Similarity:** `{c2['cosine_similarity']}%`")
            st.markdown(f"**Matched Skills ({len(c2['matching_skills'])}):**")
            if c2['matching_skills']:
                st.markdown(" ".join([f'<span class="skill-chip skill-matched">✓ {s}</span>' for s in c2['matching_skills']]), unsafe_allow_html=True)
            else:
                st.caption("None")

            st.markdown(f"<br>**Missing Skills ({len(c2['missing_skills'])}):**", unsafe_allow_html=True)
            if c2['missing_skills']:
                st.markdown(" ".join([f'<span class="skill-chip skill-missing">✕ {s}</span>' for s in c2['missing_skills']]), unsafe_allow_html=True)
            else:
                st.success("None (100% Coverage)")

            st.markdown("<br>**Education Background:**", unsafe_allow_html=True)
            for e in c2.get("education", []):
                st.markdown(f"- {e}")

    # ================= TAB 4: RECRUITER BRIEFING =================
    with tab_briefing:
        st.subheader("📝 Automated Recruiter Briefing & Interview Prompts")
        top = ranked_candidates[0]
        
        st.markdown(f"""
        ### Executive Screening Summary:
        - **Primary Recommended Candidate:** **{top['name']}** with an exceptional match score of **{top['match_score']}%** ({top['matched_skills_count']} of {top['required_skills_count']} required skills matched).
        - **Candidate Strengths:** Strong background in {', '.join(top['matching_skills'][:5]) if top['matching_skills'] else 'core domains'}.
        - **Total Applicants Evaluated:** {len(ranked_candidates)} resumes.
        """)

        st.markdown("---")
        st.markdown("### 🎯 Recommended Behavioral & Technical Interview Questions")
        st.caption("Tailored interview questions based on candidate skill gaps to probe during screening rounds:")

        for cand in ranked_candidates[:3]:
            with st.expander(f"Interview Prep for {cand['name']} (Rank #{cand['rank']})"):
                if cand['missing_skills']:
                    st.markdown("**Questions to probe on missing/unlisted skills:**")
                    for s in cand['missing_skills'][:4]:
                        st.markdown(f"- *\"We noticed {s} is a requirement for this position. Could you describe your level of exposure or past projects where you had to quickly ramp up on {s}?\"*")
                else:
                    st.markdown("- *\"You meet all stated technical requirements! Walk us through your most challenging architectural problem and how you scaled your solution.\"*")


if __name__ == "__main__":
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    ctx = get_script_run_ctx(suppress_warning=True)
    if ctx is None:
        print("\n" + "=" * 72)
        print("  [!] STREAMLIT APPLICATION LAUNCH NOTICE")
        print("  This application must be run using Streamlit CLI, not bare Python.")
        print("")
        print("  Run this command in your terminal:")
        print("      streamlit run app.py")
        print("      - or -")
        print("      python -m streamlit run app.py")
        print("=" * 72 + "\n")
    else:
        main()
