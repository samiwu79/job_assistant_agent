"""
Backend Deliverable
Minimal FastAPI app exposing Data Science functions via REST API.
Includes SQLite DB for user profiles and logging.
"""

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from agent_service import analyze_resume_and_jd, generate_answer

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("job-assistant")

# --- Database (SQLite for demo) ---
engine = create_engine("sqlite:///./app.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(200), unique=True)
    skills = Column(Text)
    experiences = Column(Text)

Base.metadata.create_all(bind=engine)

# --- Pydantic Schemas ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    skills: Optional[List[str]] = []
    experiences: Optional[List[str]] = []

class UserOut(UserCreate):
    id: int

class AnalyzeReq(BaseModel):
    resume_text: str
    jd_url: Optional[str] = None
    jd_text: Optional[str] = None

class AnswerReq(BaseModel):
    profile: dict
    jd_text: str
    question: str

# --- FastAPI app ---
app = FastAPI(title="Job Assistant API")

@app.get("/status")
def status():
    """Health check"""
    return {"ok": True}

@app.post("/api/users", response_model=UserOut)
def create_user(u: UserCreate):
    logger.info("POST /api/users %s", u.email)
    db = SessionLocal()
    if db.query(UserORM).filter_by(email=u.email).first():
        raise HTTPException(status_code=409, detail="Email exists")
    obj = UserORM(name=u.name, email=u.email,
                  skills=",".join(u.skills), experiences="||".join(u.experiences))
    db.add(obj); db.commit(); db.refresh(obj)
    return UserOut(id=obj.id, name=obj.name, email=obj.email,
                   skills=u.skills, experiences=u.experiences)

@app.get("/api/users/{uid}", response_model=UserOut)
def get_user(uid: int):
    logger.info("GET /api/users/%s", uid)
    db = SessionLocal(); obj = db.query(UserORM).get(uid)
    if not obj: raise HTTPException(status_code=404, detail="Not found")
    return UserOut(id=obj.id, name=obj.name, email=obj.email,
                   skills=obj.skills.split(",") if obj.skills else [],
                   experiences=obj.experiences.split("||") if obj.experiences else [])

@app.post("/api/resume/analyze")
def api_analyze(req: AnalyzeReq):
    logger.info("POST /api/resume/analyze")
    return analyze_resume_and_jd(req.resume_text, req.jd_url, req.jd_text)

@app.post("/api/generate/answer")
def api_answer(req: AnswerReq):
    logger.info("POST /api/generate/answer")
    return generate_answer(req.profile, req.jd_text, req.question)

@app.get("/")
def home():
    return {"message": "Welcome to Job Assistant API. Visit /docs for API spec."}
