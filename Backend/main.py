from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from report_generator import generate_report
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Submission(BaseModel):
    name: str
    email: str
    company: str
    contact: str
    responses: dict

@app.post("/submit")
async def submit_form(data: Submission):
    try:
        filename, filepath = generate_report(
            name=data.name,
            email=data.email,
            company=data.company,
            contact=data.contact,
            responses=data.responses
        )

        if os.path.exists(filepath):
            os.remove(filepath)

        return {"message": "Success"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
