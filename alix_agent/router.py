import uuid
from typing import Dict, Any
from .utils.pdf import extract_text_from_pdf
from .models.types import Document, State
from .graph import APP

def process_pdf(path: str) -> Dict[str, Any]:
    doc: Document = {
        "documentId": str(uuid.uuid4()),
        "path": path,
        "extractedText": extract_text_from_pdf(path)
    }

    initial: State = {"doc": doc}
    final_state:State = APP.invoke(initial)
    out = {
        "documentId": doc["documentId"],
        "path": doc["path"],
        "categoryCode": final_state["classification"]["categoryCode"],
        "confidence": final_state["classification"]["confidence"],
        "reasons": final_state["classification"]["reasons"],
        "valid": final_state["compliance"]["valid"],
        "reason": final_state["compliance"].get("reason"),
    }
    return out