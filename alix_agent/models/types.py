from typing import Literal, Optional, TypedDict, List, Dict

Category = Literal[
    "01.0000-50",  # Death Certificate
    "02.0300-50",  # Will or Trust
    "03.0090-00",  # Property Deed
    "04.5000-00",  # Financial Statement
    "05.5000-70",  # Tax Document
    "00.0000-00",  # Misc
]

class Document(TypedDict):
    documentId: str
    path: str
    extractedText: str

class ClassificationResult(TypedDict, total=False):
    categoryCode: Category
    confidence: float
    reasons: List[str]

class ComplianceResult(TypedDict, total=False):
    valid: bool
    reason: Optional[str]

class State(TypedDict, total=False):
    doc: Document
    classification: ClassificationResult
    compliance: ComplianceResult