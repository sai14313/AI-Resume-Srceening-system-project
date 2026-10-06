"""
NLP Matching Engine using Scikit-Learn TF-IDF, Cosine Similarity,
and Skill Overlap Analysis. Calculates candidate scores (0 - 100) and rankings.
"""

import re
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from extractor import extract_skills, clean_text


def preprocess_nlp_text(text: str) -> str:
    """
    Normalizes text for TF-IDF modeling by removing punctuation,
    converting to lowercase, and eliminating redundant tokens.
    """
    if not text:
        return ""
    text = text.lower()
    # Replace non-alphanumeric (keep spaces, dashes, plus)
    text = re.sub(r'[^a-zA-Z0-9\s+#.-]', ' ', text)
    # Normalize spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def compute_tfidf_similarities(job_description: str, resumes_texts: List[str]) -> List[float]:
    """
    Computes cosine similarity between Job Description and each resume
    using Scikit-Learn's TF-IDF Vectorizer with unigrams & bigrams.
    """
    if not job_description or not resumes_texts:
        return [0.0] * len(resumes_texts)

    cleaned_jd = preprocess_nlp_text(job_description)
    cleaned_resumes = [preprocess_nlp_text(t) for t in resumes_texts]

    corpus = [cleaned_jd] + cleaned_resumes

    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=5000
        )
        tfidf_matrix = vectorizer.fit_transform(corpus)

        # Vector 0 is Job Description, vectors 1..N are resumes
        jd_vector = tfidf_matrix[0:1]
        resume_vectors = tfidf_matrix[1:]

        similarities = cosine_similarity(jd_vector, resume_vectors).flatten()
        return [float(np.clip(s, 0.0, 1.0)) for s in similarities]
    except Exception as e:
        print(f"TF-IDF similarity calculation error: {e}")
        return [0.0] * len(resumes_texts)


def analyze_skill_match(jd_skills: List[str], candidate_skills: List[str]) -> Dict[str, Any]:
    """
    Compares candidate skills against job description required skills.
    Identifies matching skills, missing skills, and additional bonus skills.
    """
    jd_skills_lower = {s.lower(): s for s in jd_skills}
    candidate_skills_lower = {s.lower(): s for s in candidate_skills}

    matching_keys = set(jd_skills_lower.keys()).intersection(set(candidate_skills_lower.keys()))
    missing_keys = set(jd_skills_lower.keys()) - set(candidate_skills_lower.keys())
    extra_keys = set(candidate_skills_lower.keys()) - set(jd_skills_lower.keys())

    matching_skills = sorted([jd_skills_lower[k] for k in matching_keys])
    missing_skills = sorted([jd_skills_lower[k] for k in missing_keys])
    additional_skills = sorted([candidate_skills_lower[k] for k in extra_keys])

    if len(jd_skills) > 0:
        skill_score = len(matching_skills) / len(jd_skills)
    else:
        # If no explicit skills detected in JD, evaluate based on count of skills candidate has
        skill_score = min(1.0, len(candidate_skills) / 10.0)

    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "match_ratio": round(skill_score, 4),
        "total_required": len(jd_skills),
        "total_matched": len(matching_skills)
    }


def get_match_tier(score: float) -> Tuple[str, str, str]:
    """
    Returns visual badge tier, color, and icon based on match score.
    """
    if score >= 75.0:
        return "Exceptional Match", "#10b981", "🟢"
    elif score >= 55.0:
        return "Strong Match", "#3b82f6", "🔵"
    elif score >= 35.0:
        return "Moderate Match", "#f59e0b", "🟡"
    else:
        return "Low Match", "#ef4444", "🔴"


def screen_resumes(
    job_description: str,
    parsed_candidates: List[Dict[str, Any]],
    weight_skills: float = 0.50,
    weight_tfidf: float = 0.35,
    weight_profile: float = 0.15,
    extra_required_skills: List[str] = None
) -> List[Dict[str, Any]]:
    """
    End-to-end screening pipeline:
    1. Extracts required skills from Job Description (and merges any extra custom skills).
    2. Runs TF-IDF Cosine Similarity across all candidate texts.
    3. Analyzes skill match & gaps.
    4. Computes calibrated 0 - 100 match score.
    5. Ranks candidates from highest to lowest score.
    """
    if not job_description or not parsed_candidates:
        return []

    jd_skills = extract_skills(job_description)
    if extra_required_skills:
        existing_lower = {s.lower() for s in jd_skills}
        for extra in extra_required_skills:
            if extra.strip() and extra.strip().lower() not in existing_lower:
                jd_skills.append(extra.strip())
                existing_lower.add(extra.strip().lower())

    resume_texts = [c.get("raw_text", "") for c in parsed_candidates]

    similarities = compute_tfidf_similarities(job_description, resume_texts)

    # Normalize weights so they sum to 1.0
    total_weights = weight_skills + weight_tfidf + weight_profile
    if total_weights <= 0:
        total_weights = 1.0
    w_skills = weight_skills / total_weights
    w_tfidf = weight_tfidf / total_weights
    w_profile = weight_profile / total_weights

    results = []
    for idx, candidate in enumerate(parsed_candidates):
        sim = similarities[idx]
        cand_skills = candidate.get("skills", [])
        skill_analysis = analyze_skill_match(jd_skills, cand_skills)

        # In natural text, cosine similarity between a 50-word JD and a 500-word resume
        # typically tops out around 0.35 - 0.45. We calibrate raw cosine sim by a 2.5x scaling
        # factor so a high-relevance resume achieves full semantic points.
        calibrated_sim = min(1.0, sim * 2.5)

        # Profile completeness factor (Degree, Experience)
        edu_list = candidate.get("education", [])
        has_degree = any("degree" in e.lower() or "bachelor" in e.lower() or "master" in e.lower() or "b.s." in e.lower() or "b.tech" in e.lower() or "btech" in e.lower() for e in edu_list)

        exp_data = candidate.get("experience", {})
        exp_years = exp_data.get("estimated_years", 0) or 0
        has_experience = exp_years >= 2.0 or exp_data.get("date_ranges_found", 0) >= 1

        profile_score = 0.3
        if has_degree:
            profile_score += 0.4
        if has_experience:
            profile_score += 0.3
        profile_score = min(1.0, profile_score)

        # Composite score from 0 to 100
        composite_score = (
            (skill_analysis["match_ratio"] * w_skills) +
            (calibrated_sim * w_tfidf) +
            (profile_score * w_profile)
        ) * 100.0

        final_score = round(float(np.clip(composite_score, 0.0, 100.0)), 1)
        tier_label, tier_color, tier_icon = get_match_tier(final_score)

        breakdown = {
            "skill_match_points": round(skill_analysis["match_ratio"] * w_skills * 100.0, 1),
            "content_sim_points": round(calibrated_sim * w_tfidf * 100.0, 1),
            "profile_factor_points": round(profile_score * w_profile * 100.0, 1),
            "raw_cosine_similarity": round(sim * 100.0, 2),
            "calibrated_content_alignment": round(calibrated_sim * 100.0, 1),
            "skill_coverage_pct": round(skill_analysis["match_ratio"] * 100.0, 1),
            "final_score": final_score
        }

        candidate_result = {
            **candidate,
            "match_score": final_score,
            "cosine_similarity": round(sim * 100.0, 2),
            "match_tier": tier_label,
            "tier_color": tier_color,
            "tier_icon": tier_icon,
            "score_breakdown": breakdown,
            "matching_skills": skill_analysis["matching_skills"],
            "missing_skills": skill_analysis["missing_skills"],
            "additional_skills": skill_analysis["additional_skills"],
            "skill_match_ratio": skill_analysis["match_ratio"],
            "required_skills_count": len(jd_skills),
            "matched_skills_count": len(skill_analysis["matching_skills"])
        }
        results.append(candidate_result)

    # Rank candidates from highest to lowest score
    results.sort(key=lambda x: x["match_score"], reverse=True)

    # Assign rank numbers (1-based)
    for rank_idx, cand in enumerate(results, start=1):
        cand["rank"] = rank_idx

    return results
