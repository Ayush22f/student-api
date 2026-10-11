import csv
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

CSV_FILE = Path(__file__).parent / "q-fastapi.csv"

app = FastAPI()

# Allow GET requests from any origin (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Read the CSV once at startup, keeping the original row order
students = []
with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        students.append({
            "studentId": int(row["studentId"]),
            "class": row["class"].strip(),
        })


@app.get("/api")
def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
    if not class_:
        return {"students": students}
    wanted = set(class_)
    return {"students": [s for s in students if s["class"] in wanted]}