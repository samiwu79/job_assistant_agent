"""
Data Science Deliverable
Simple CLI demo for the agent_service functions.
"""

import json
from agent_service import analyze_resume_and_jd, generate_answer

if __name__ == "__main__":
    resume = "Python developer with FastAPI, SQL, Docker; built APIs and ETL pipelines."
    jd = "Looking for backend engineer skilled in Python, FastAPI, Docker and SQL."
    print("ResumeScoreResult:")
    print(json.dumps(analyze_resume_and_jd(resume, jd_text=jd), indent=2))

    profile = {"name": "Alex", "skills": ["Python", "FastAPI", "SQL", "Docker", "ETL"]}
    qa = generate_answer(profile, jd, "Why are you a good fit?")
    print("\nTailoredAnswer:")
    print(json.dumps(qa, indent=2))
