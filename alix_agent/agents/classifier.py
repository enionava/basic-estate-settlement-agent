import re
from typing import Dict, List, Tuple
from .compliance import CATEGORY_LABELS
from ..models.types import State, ClassificationResult, Category
from ..utils.llm import llm_tiebreak

LOWER_BANKS = [
    "bank of america", "chase", "wells fargo", "citibank", "us bank",
    "american express", "capital one"
]

LETTER_HINTS = [
    "dear ", "regards", "sincerely", "claim", "claim status", "policy",
    "adjuster", "coresspondence", "letter", "enclosed", "attachment", "ref #", "reference 3"
]

def _score_categories(text: str) -> Dict[str, Tuple[float, List[str]]]:
    t = text.lower()
    scores: Dict[str, Tuple[float, List[str]]] = {}

    def add(code: str, points: float, reason: str):
        s, r = scores.get(code, (0.0, []))
        scores[code] = (s + points, r + [reason])
    
    # --- Death Certificate ---
    has_cod = "certificate of death" in t
    has_dod = "date of death" in t

    # lone mention -> tiny bump only
    if has_cod:
        add("01.0000-50", 0.15, "Contains 'Certificate of Death'")

    # co-occurrence -> real signal
    if has_cod and has_dod:
        add("01.0000-50", 0.5, "Contains both 'Certificate of Death' and 'Date of Death'")

        # crude header check: phrase appears in first ~250 chars
        if t.find("certificate of death") != -1 and t.find("certificate of death") < 250:
            add("01.0000-50", 0.25, "Header-like placement of 'Certificate of Death'")

    # registrar/DOH as a weaker auxiliary
    if "department of health" in t or "registrar" in t:
        add("01.0000-50", 0.1, "Contains registrar/DOH")

    # --- Will/Trust ---
    if "last will and testament" in t:
        add("02.0300-50", 0.8, "Contains 'Last Will and Testament'")
    if "trust agreement" in t:
        add("02.0300-50", 0.8, "Contains 'Trust Agreement'")
    if "testamentary instrument" in t:
        add("02.0300-50", 0.25, "Contains 'Testamentary Instrument'")

    # --- Deed ---
    if "deed" in t or "quitclaim" in t or "warranty deed" in t:
        add("03.0090-00", 0.6, "Contains deed-related terms")
    if "recorded" in t and "county" in t:
        add("03.0090-00", 0.2, "Recorded in county")

    # --- Financial Statement ---
    if "statement" in t and any(b in t for b in LOWER_BANKS):
        add("04.5000-00", 0.7, "Bank statement terms + bank name")
    if re.search(r"ending balance|available balance", t):
        add("04.5000-00", 0.2, "Balance fields")

    # --- Tax ---
    if "form 1041" in t or "u.s. income tax return for estates and trusts" in t:
        add("05.5000-70", 0.8, "Tax form 1041")
    if "internal revenue service" in t or "irs" in t:
        add("05.5000-70", 0.2, "IRS indicators")

    # --- Negative signals to pull letters away from special cats ---
    if any(h in t for h in LETTER_HINTS):
        s, r = scores.get("01.0000-50", (0.0, []))
        if s > 0:
            scores["01.0000-50"] = (max(0.0, s - 0.25), r + ["Letter-like content (penalty)"])
        s2, r2 = scores.get("02.0300-50", (0.0, []))
        if s2 > 0:
            scores["02.0300-50"] = (max(0.0, s2 - 0.15), r2 + ["Letter-like content (penalty)"])

    # Fallback Misc
    add("00.0000-00", 0.1, "Default minimal score")

    for k, (pts, rs) in list(scores.items()):
        if pts > 1.0:
            scores[k] = (1.0, rs + ["Capped at 1.0"])

    return scores

def classify_node(state: State) -> State:
    text = state["doc"]["extractedText"]
    scores = _score_categories(text)

    top_code, (top_score, reasons) = max(scores.items(), key=lambda kv: kv[1][0])

    if top_score < 0.72:
        llm_code, llm_conf = llm_tiebreak(
            text,
            codes=list(CATEGORY_LABELS.keys())
        )
        if llm_code and llm_conf > top_score:
            top_code, top_score = llm_code, llm_conf
            reasons.append("LLM determined")
    
    result: ClassificationResult = {
        "categoryCode": top_code,
        "confidence": round(top_score, 2),
        "reasons": reasons
    }
    return {**state, "classification": result}
