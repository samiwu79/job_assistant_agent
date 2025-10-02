"""
Data Science Deliverable
Basic tests for analyze_resume_and_jd and generate_answer.
"""

from agent_service import analyze_resume_and_jd, generate_answer

def test_all():
    resume = "Python FastAPI SQL"
    jd = "Looking for Python FastAPI backend"
    res = analyze_resume_and_jd(resume, jd_text=jd)
    assert "score" in res
    assert isinstance(res["score"], int)
    qa = generate_answer({"name": "Alex", "skills": ["Python","FastAPI"]}, jd, "Why fit?")
    assert "answer" in qa

if __name__ == "__main__":
    test_all()
    print("✅ Passed")
