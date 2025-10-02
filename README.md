# job_assistant_agent# Job Assistant Agent – Data Science & Backend Minimal Submission

## 📌 Overview
This project is a minimal implementation of an **AI Job Assistant**.  
It covers:
- **Data Science**: Workflow design, JSON data contracts, prompt prototypes, core agent functions.
- **Backend**: Minimal FastAPI server, database (SQLite), logging, API endpoints.

---
## 🔑Instruction: Simulated Locally Project

For this submission the LLM (Large Language Model) calls are **simulated locally** instead of calling real OpenAI or DeepSeek APIs.

- **Reason:**  
  The development environment could not reliably reach the OpenAI/DeepSeek endpoints (Paid API key access issues).  

- **Approach:**  
  The project still follows an **agentic workflow**:  
  - Job descriptions are scraped or passed in as plain text.  
  - The `analyze_resume_and_jd()` and `generate_answer()` functions are implemented with the same interface a real LLM would use.  
  - Instead of calling the API, they use a lightweight local keyword–matching algorithm to generate structured JSON.  

- **Explaination:**  
  - The **data contract** (`schemas.json`) and **prompt templates** (`prompts.txt`) are already in place and tested.  
  - The backend and API are fully functional and can be switched to a real LLM simply by replacing the internal logic of `agent_service.py` (one function call).  

  - **How to Replace Local Logic with Real LLM**
  If API keys/network become available:
  In **agent_service.py**
```bash
import openai
def analyze_resume_and_jd(resume, jd_text):
    prompt = f"Compare resume with job: {jd_text}..."
    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}]
    )
    return resp.choices[0].message["content"]
```
The rest of the backend remains unchanged.

## ⚙️ Installation

- ** clone the project**
```bash
git clone <your-gitlab-url>
cd job_assistant_agent
```

- **  install dependencies **
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 🚀 Run the Server
```bash
uvicorn app:app --reload
```
Open in browser:
Health check: http://127.0.0.1:8000/status

## 📂 Project Structure

```graphql
job_assistant_agent/
├─ app.py               # FastAPI app with endpoints
├─ agent_service.py     # Core logic (resume analysis & answer generation)
├─ scraper.py           # Web scraping tool with retry & fallback
├─ schemas.json         # Data contracts
├─ prompts.txt          # Prompt templates (few-shot)
├─ requirements.txt
└─ test_agent.py        # Simple unit tests