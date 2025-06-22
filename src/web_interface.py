"""
Web interface for document processing
"""

from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import asyncio
import json

# Import existing API functionality
# Import API components
import sys
from pathlib import Path
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from api import extract_entities

app = FastAPI(title="Document Processing Web Interface")

# Setup templates and static files
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    """Serve the upload form"""
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_files(request: Request, files: List[UploadFile] = File(...)):
    """Process uploaded files and return results"""
    
    results = []
    
    for file in files:
        try:
            # Process each file using existing API logic
            result = await extract_entities(file)
            results.append({
                "filename": file.filename,
                "success": True,
                "data": result
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return templates.TemplateResponse("results.html", {
        "request": request,
        "results": results
    })

@app.get("/api/stats")
async def get_stats():
    """Get database statistics for web interface"""
    from vector_db import VectorDatabase
    db = VectorDatabase("api_vector_db")
    return db.get_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)