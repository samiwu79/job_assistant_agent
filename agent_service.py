"""
Data Science Deliverable
Core service functions: analyze_resume_and_jd & generate_answer.
These wrap scraping + scoring + prompt logic (currently simple keyword based).
"""

import re, json
from collections import Counter
from typing import List, Dict, Optional
from scraper import scrape_job_description

STOPWORDS = set("a an the and or for to of in on with without by from as is are be this that it".split())

def _tokens(text: str) -> List[str]:
    return [w for w in re.findall(r"[A-Za-z]+", text.lower()) if w not in STOPWORDS]

def _keywords(text: str, k: int = 20) -> List[str]:
    return [w for w, _ in Counter(_tokens(text)).most_common(k)]

def analyze_resume_and_jd(resume_text: str,
                          jd_url: Optional[str] = None,
                          jd_text: Optional[str] = None) -> Dict:
    """
    Analyze how well a resume matches a job description.
    return ResumeScoreResult JSON。
    """
    if not jd_text and not jd_url:
        raise ValueError("Provide jd_text or jd_url")
    if jd_url and not jd_text:
        jd_text = scrape_job_description(jd_url)
        if not jd_text:
            raise ValueError("JD scraping failed or timed out. Please provide jd_text directly for this site.")


    resume_kw = set(_keywords(resume_text, 30))
    jd_kw = _keywords(jd_text, 30)

    present = [w for w in jd_kw if w in resume_kw]
    missing = [w for w in jd_kw if w not in resume_kw][:8]
    score = int(round(100 * len(present) / max(1, len(jd_kw))))

    suggestions = []
    if missing:
        suggestions.append(f"Add keywords: {', '.join(missing[:5])}.")
    if present:
        suggestions.append(f"Keep & highlight: {', '.join(present[:5])}.")
    if score < 70:
        suggestions.append("Add measurable achievements to improve match.")

    return {
        "score": score,
        "missing_keywords": missing,
        "strengths": present[:8],
        "tailor_suggestions": suggestions
    }

def generate_answer(profile: Dict, jd_text: str, question: str) -> Dict:
    """
    Generate a tailored interview/application answer.
    return TailoredAnswer JSON。
    """
    skills = ", ".join(profile.get("skills", [])[:6])
    wants = ", ".join(_keywords(jd_text, 8)[:6])
    name = profile.get("name", "I")
    answer = f"{name} fits this job: skilled in {skills}. JD asks for {wants}, matching my experience."
    return {
        "question": question,
        "answer": answer,
        "rationale_bullets": [
            "Covers JD keywords",
            "Maps skills to role",
            "Shows delivery timeline"
        ]
    }
