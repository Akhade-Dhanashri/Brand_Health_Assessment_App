from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Dict
import traceback
import json

from report_generator import generate_and_send_report
from models import Submission as DBSubmission, SessionLocal

app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health Check Route ---
@app.get("/")
async def root():
    return {"message": "✅ Brand Health Assessment API is running."}

# --- Request Schema ---
class Submission(BaseModel):
    name: str
    email: EmailStr
    company: str
    responses: Dict[str, int]

# --- Submission Endpoint ---
@app.post("/submit")
async def submit_form(data: Submission):
    try:
        print(f"📩 Received submission from: {data.name} ({data.email})")

        # Validate: Must have 12 answers
        answers = list(data.responses.values())
        if len(answers) != 12:
            return {"error": "Expected 12 responses"}

        total_score = sum(answers)
        percentage = round((total_score / 60) * 100)

        # Prepare clean form data
        form_dict = {
            "name": data.name.strip(),
            "email": data.email.strip(),
            "company": data.company.strip(),
            "responses": data.responses
        }

        # Generate PDF & send via email
        generate_and_send_report(form_dict)

        # Save to SQLite database
        with SessionLocal() as db:
            db_entry = DBSubmission(
                name=form_dict["name"],
                email=form_dict["email"],
                company=form_dict["company"],
                responses_json=json.dumps(form_dict["responses"]),
                score=total_score,
                percentage=percentage,
            )
            db.add(db_entry)
            db.commit()
            db.refresh(db_entry)

        return {
            "message": "✅ Report sent successfully",
            "score": total_score,
            "percentage": percentage
        }

    except Exception as e:
        print("❌ Error in /submit:", traceback.format_exc())
        return {"error": "Failed to send report or save to database"}
