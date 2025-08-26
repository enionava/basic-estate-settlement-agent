import os
import uuid
import tempfile
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .router import process_pdf

app = FastAPI(title="Alix Agent API", version="1.0.0")

class ClassificationResponse(BaseModel):
    documentId: str = Field(..., description="UUID assigned during processing")
    filename: str = Field(..., description="Original uploaded filename")
    categoryCode: str = Field(..., description="Taxonomy code")
    confidence: float = Field(..., ge=0.0, le=1.0, description="0..1 confidence")
    valid: bool = Field(..., description="Compliance result")
    reason: Optional[str] = Field(None, description="Compliance failure reason, if any")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/classify", response_model=ClassificationResponse)
async def classify(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files are supported.")

    try:
        suffix = f"_{uuid.uuid4()}.pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to store upload: {e}")

    try:
        result = process_pdf(tmp_path)
        api_result = {
            "documentId": result["documentId"],
            "filename": file.filename,
            "categoryCode": result["categoryCode"],
            "confidence": result["confidence"],
            "valid": result["valid"],
            "reason": result.get("reason"),
        }
        return JSONResponse(content=api_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification failed: {e}")
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass