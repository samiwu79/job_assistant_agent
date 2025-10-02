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

## ⚙️ Installation
```bash
pip install -r requirements.txt