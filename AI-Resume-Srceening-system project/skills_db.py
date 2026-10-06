"""
Comprehensive Skills Database and Taxonomy for Resume & Job Description Analysis.
Includes technical, cloud, data, web, DevOps, database, and soft skills.
"""

SKILL_TAXONOMY = {
    "Programming Languages": [
        "python", "java", "c++", "c#", "c", "javascript", "typescript",
        "go", "golang", "rust", "ruby", "php", "swift", "kotlin", "scala",
        "r", "sql", "html", "html5", "css", "css3", "bash", "shell", "powershell",
        "dart", "matlab", "perl"
    ],
    "AI, ML & Data Science": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "scikit-learn", "sklearn", "tensorflow", "pytorch",
        "keras", "hugging face", "transformers", "llm", "large language models",
        "langchain", "llamaindex", "pandas", "numpy", "scipy", "matplotlib",
        "seaborn", "opencv", "nltk", "spacy", "tf-idf", "tfidf", "cosine similarity",
        "word2vec", "bert", "xgboost", "lightgbm", "catboost", "data analysis",
        "data engineering", "feature engineering", "predictive modeling",
        "neural networks", "clustering", "regression", "classification",
        "time series", "reinforcement learning", "genai", "generative ai"
    ],
    "Web & Backend Frameworks": [
        "react", "react.js", "angular", "vue", "vue.js", "next.js", "nuxt.js",
        "node.js", "nodejs", "express", "express.js", "django", "flask",
        "fastapi", "spring boot", "asp.net", "ruby on rails", "laravel",
        "graphql", "rest api", "restful api", "microservices", "tailwind css",
        "bootstrap", "redux", "html/css", "websockets", "grpc"
    ],
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "microsoft azure", "gcp",
        "google cloud platform", "docker", "kubernetes", "k8s", "jenkins",
        "git", "github", "gitlab", "bitbucket", "ci/cd", "continuous integration",
        "terraform", "ansible", "linux", "unix", "helm", "prometheus",
        "grafana", "cloudformation", "nginx", "apache", "serverless",
        "aws lambda", "ec2", "s3", "ecs", "eks"
    ],
    "Databases & Storage": [
        "postgresql", "postgres", "mysql", "mongodb", "redis", "elasticsearch",
        "sqlite", "cassandra", "dynamodb", "oracle", "sql server", "firebase",
        "snowflake", "bigquery", "mariadb", "neo4j", "faiss", "pinecone",
        "milvus", "chromadb"
    ],
    "Big Data & Pipelines": [
        "apache spark", "spark", "pyspark", "hadoop", "kafka", "apache kafka",
        "airflow", "apache airflow", "databricks", "etl", "data warehousing",
        "dbt", "presto", "hive"
    ],
    "Engineering & Soft Skills": [
        "agile", "scrum", "kanban", "jira", "problem solving", "leadership",
        "communication", "team collaboration", "project management",
        "code review", "unit testing", "test driven development", "tdd",
        "system design", "software architecture", "critical thinking",
        "debugging", "stakeholder management"
    ]
}

# Flattened lookup list sorted by length descending so multi-word terms match first (e.g. "machine learning" before "learning")
ALL_SKILLS = []
for category, skills in SKILL_TAXONOMY.items():
    ALL_SKILLS.extend(skills)

ALL_SKILLS = sorted(list(set(ALL_SKILLS)), key=lambda s: len(s), reverse=True)

# Common education keywords & degrees
EDUCATION_KEYWORDS = [
    "bachelor", "bachelors", "bachelor's", "b.s.", "bs", "b.tech", "btech", "b.e.", "be",
    "b.a.", "ba", "bca",
    "master", "masters", "master's", "m.s.", "ms", "m.tech", "mtech", "m.e.", "me",
    "m.a.", "ma", "mca", "mba",
    "ph.d", "phd", "doctor of philosophy", "doctorate",
    "diploma", "associate degree", "high school"
]

EXPERIENCE_KEYWORDS = [
    "experience", "work history", "employment history", "professional experience",
    "work experience", "career summary", "internship", "professional background"
]
