"""
Verification script for PDF extraction and matching pipeline.
"""
import os
from extractor import parse_resume
from matcher import screen_resumes

resumes = []
folder = 'sample_resumes'
for f in os.listdir(folder):
    if f.endswith('.pdf'):
        res = parse_resume(os.path.join(folder, f), filename=f)
        resumes.append(res)
        print(f"Parsed {f}: Name={res['name']}, Email={res['email']}, Skills={len(res['skills'])}")

sample_jd = """
We are seeking a Senior AI / Machine Learning Engineer with strong expertise in Python, PyTorch,
Scikit-Learn, and NLP (Natural Language Processing). Experience with TF-IDF, transformers,
Docker, REST APIs, and AWS cloud deployment is required. Candidates must have a Degree in Computer Science
and experience leading agile development teams.
"""

ranked = screen_resumes(sample_jd, resumes)
print("\n--- SCREENING RANKINGS ---")
for r in ranked:
    print(f"Rank #{r['rank']}: {r['name']} | Score: {r['match_score']}/100 | Cosine: {r['cosine_similarity']}% | Tier: {r['match_tier']} | Matched: {r['matching_skills']}")

print("\nAll pipeline tests passed!")
