"""
Synthetic Sample Resume Generator using ReportLab.
Generates realistic, professional PDF resumes for testing and demonstrations.
All candidate profiles are synthetic and generated for demonstration purposes.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

SAMPLE_RESUMES_DATA = [
    {
        "filename": "alex_rivera_senior_ml_engineer.pdf",
        "name": "Alex Rivera",
        "title": "Senior Machine Learning & NLP Engineer",
        "contact": "alex.rivera.ai@example.com | +1 (555) 342-8901 | linkedin.com/in/alex-rivera-ml | github.com/alexrivera-ai",
        "summary": "Innovative Senior Machine Learning Engineer with 6+ years of experience designing, training, and deploying end-to-end NLP and predictive systems. Proven track record in Scikit-Learn, PyTorch, Transformers, TF-IDF, and scalable cloud architectures on AWS.",
        "skills": "Python, Machine Learning, Deep Learning, NLP, Natural Language Processing, Scikit-Learn, PyTorch, TensorFlow, TF-IDF, Cosine Similarity, Hugging Face, Transformers, Pandas, NumPy, Docker, AWS, Git, CI/CD, REST API, PostgreSQL, Agile",
        "experience": [
            ("Senior ML & NLP Engineer - Nexus AI Labs (2021 - Present)",
             "• Spearheaded semantic document retrieval system using TF-IDF, embeddings, and cosine similarity, reducing query latency by 45%.\n"
             "• Built and deployed scalable transformer-based NLP classification models with PyTorch, Docker, and AWS SageMaker.\n"
             "• Led agile team of 5 engineers conducting regular code reviews and implementing automated CI/CD pipelines."),
            ("Machine Learning Engineer - DataPulse Analytics (2018 - 2021)",
             "• Developed customer sentiment analysis and recommendation engines with Scikit-Learn and Pandas.\n"
             "• Extracted actionable business metrics from semi-structured data pipelines using Python and PostgreSQL.")
        ],
        "education": "Master of Science in Computer Science (Artificial Intelligence) - Stanford University, 2018\nBachelor of Science in Computer Engineering - UC Berkeley, 2016"
    },
    {
        "filename": "priya_patel_fullstack_python.pdf",
        "name": "Priya Patel",
        "title": "Lead Full-Stack Python & Backend Engineer",
        "contact": "priya.patel.dev@example.com | +1 (555) 781-2294 | linkedin.com/in/priyapatel-dev | github.com/priyapatel-tech",
        "summary": "Full-Stack Software Engineer with 5+ years of expertise in Python, FastAPI, Django, and modern React. Passionate about building high-performance microservices, clean REST APIs, and integrating machine learning models into user-friendly web dashboards.",
        "skills": "Python, Django, FastAPI, Flask, JavaScript, TypeScript, React, REST API, PostgreSQL, Redis, Docker, Git, CI/CD, AWS, Machine Learning, Scikit-Learn, Pandas, HTML5, CSS3, Agile, Unit Testing",
        "experience": [
            ("Lead Backend Engineer - CloudPeak Systems (2020 - Present)",
             "• Designed asynchronous microservices handling 2M+ requests/day with Python, FastAPI, and Redis caching.\n"
             "• Integrated scikit-learn predictive scoring models into real-time customer analytics dashboards.\n"
             "• Managed Docker containers and automated GitHub Actions CI/CD workflows."),
            ("Full Stack Developer - ByteWave Solutions (2018 - 2020)",
             "• Developed interactive web applications using React, Python, Django, and PostgreSQL.\n"
             "• Implemented secure JWT authentication and role-based access control systems.")
        ],
        "education": "Bachelor of Technology in Computer Science - University of Illinois, 2018"
    },
    {
        "filename": "david_kim_junior_data_analyst.pdf",
        "name": "David Kim",
        "title": "Junior Data Analyst & Python Programmer",
        "contact": "david.kim.analyst@example.com | +1 (555) 619-3382 | linkedin.com/in/davidkim-data",
        "summary": "Detail-oriented Data Analyst with 2+ years of professional experience in data manipulation, exploratory analysis, and statistical modeling using Python, SQL, Pandas, and Scikit-Learn.",
        "skills": "Python, SQL, Pandas, NumPy, Scikit-Learn, Data Analysis, Matplotlib, Seaborn, MySQL, Tableau, Excel, Git, Statistics, Problem Solving",
        "experience": [
            ("Junior Data Analyst - Insight Metrics (2022 - Present)",
             "• Processed and cleaned datasets containing 500k+ rows with Pandas and Python scripts.\n"
             "• Built exploratory machine learning regression models using Scikit-Learn to forecast quarterly sales trends.\n"
             "• Created automated executive reports and interactive Tableau dashboards."),
            ("Data Intern - Metro Research (2021 - 2022)",
             "• Wrote complex SQL queries to extract data from MySQL relational databases."
            )
        ],
        "education": "Bachelor of Science in Statistics & Data Science - University of Washington, 2022"
    },
    {
        "filename": "sarah_connor_devops_cloud.pdf",
        "name": "Sarah Connor",
        "title": "DevOps & Cloud Infrastructure Engineer",
        "contact": "sarah.connor.infra@example.com | +1 (555) 902-4411 | linkedin.com/in/sarah-connor-cloud | github.com/sconnor-infra",
        "summary": "DevOps Engineer with 4+ years of hands-on experience orchestrating multi-region cloud infrastructures, Kubernetes clusters, Dockerized services, and automated CI/CD pipelines on AWS.",
        "skills": "AWS, Docker, Kubernetes, Linux, Bash, Terraform, Ansible, CI/CD, Jenkins, Git, Python, Prometheus, Grafana, Microservices, System Design",
        "experience": [
            ("DevOps Engineer - Apex Cloud Solutions (2021 - Present)",
             "• Architected scalable Kubernetes (EKS) clusters on AWS with 99.99% uptime.\n"
             "• Automated infrastructure provisioning with Terraform and Ansible configurations.\n"
             "• Implemented comprehensive monitoring with Prometheus and Grafana alerting systems."),
            ("Systems Administrator - Cyberdyne Tech (2019 - 2021)",
             "• Maintained 100+ Linux enterprise servers, bash automation scripts, and Jenkins CI builds."
            )
        ],
        "education": "Bachelor of Science in Information Technology - Georgia Tech, 2019"
    },
    {
        "filename": "emily_watson_marketing_specialist.pdf",
        "name": "Emily Watson",
        "title": "Digital Marketing & Brand Communications Specialist",
        "contact": "emily.watson.mktg@example.com | +1 (555) 438-1920 | linkedin.com/in/emily-watson-market",
        "summary": "Creative and results-driven Digital Marketing Specialist with 4 years of experience leading multi-channel growth campaigns, content marketing, SEO optimization, and brand storytelling.",
        "skills": "Digital Marketing, SEO, Content Strategy, Google Analytics, Social Media Management, Copywriting, Creative Direction, Brand Strategy, Project Management, Communication",
        "experience": [
            ("Digital Marketing Specialist - BrightWave Media (2021 - Present)",
             "• Managed inbound marketing campaigns generating 35% growth in organic website leads.\n"
             "• Spearheaded SEO keyword research and content calendar creation for B2B tech clients.\n"
             "• Tracked performance metrics and campaign conversions using Google Analytics."),
            ("Content Marketing Coordinator - Spark Agency (2019 - 2021)",
             "• Authored high-converting blog posts, email newsletters, and customer case studies."
            )
        ],
        "education": "Bachelor of Arts in Communications & Marketing - Boston University, 2019"
    }
]


def create_resume_pdf(data: dict, output_dir: str):
    """Creates a clean, professional PDF resume for synthetic candidate data."""
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, data["filename"])
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=2
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=4
    )
    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=10
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        leftIndent=10,
        spaceAfter=3
    )

    story = []

    # Header
    story.append(Paragraph(data["name"], title_style))
    story.append(Paragraph(data["title"], subtitle_style))
    story.append(Paragraph(data["contact"], contact_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=8))

    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    story.append(Paragraph(data["summary"], body_style))
    story.append(Spacer(1, 4))

    # Core Skills
    story.append(Paragraph("CORE SKILLS & TECHNOLOGIES", heading_style))
    story.append(Paragraph(f"<b>Key Competencies:</b> {data['skills']}", body_style))
    story.append(Spacer(1, 4))

    # Experience
    story.append(Paragraph("WORK EXPERIENCE", heading_style))
    for job_title, job_details in data["experience"]:
        story.append(Paragraph(f"<b>{job_title}</b>", body_style))
        for line in job_details.split("\n"):
            if line.strip():
                story.append(Paragraph(line.strip(), bullet_style))
        story.append(Spacer(1, 2))

    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    for edu_line in data["education"].split("\n"):
        story.append(Paragraph(edu_line.strip(), body_style))

    doc.build(story)
    return pdf_path


def generate_all_sample_resumes(output_dir: str = "sample_resumes") -> list:
    """Generates all synthetic PDF resumes in the target directory."""
    created_files = []
    for candidate_data in SAMPLE_RESUMES_DATA:
        filepath = create_resume_pdf(candidate_data, output_dir)
        created_files.append(filepath)
    return created_files


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, "sample_resumes")
    files = generate_all_sample_resumes(target_dir)
    print(f"Successfully generated {len(files)} sample resumes in: {target_dir}")
