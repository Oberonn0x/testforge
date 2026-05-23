"""TestForge API — FastAPI application."""
import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.token_tracker import init_db, get_stats
from backend.pipeline import run_pipeline, jobs

app = FastAPI(title="TestForge", version="1.0.0", description="Multi-agent Automated Solidity Test Suite Builder")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.on_event("startup")
async def startup():
    await init_db()


class GenerateRequest(BaseModel):
    solidity_code: str


@app.post("/api/generate")
async def generate_from_json(req: GenerateRequest):
    job_id = await run_pipeline(req.solidity_code)
    return {"job_id": job_id, "status": "accepted"}


@app.post("/api/generate/upload")
async def generate_from_upload(file: UploadFile = File(...)):
    code = (await file.read()).decode("utf-8")
    job_id = await run_pipeline(code)
    return {"job_id": job_id, "status": "accepted"}


@app.get("/api/generate/{job_id}")
async def get_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return JSONResponse({"error": "Job not found"}, status_code=404)
    return job


@app.get("/api/stats")
async def stats():
    return await get_stats()


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("frontend/index.html") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "8000")))
