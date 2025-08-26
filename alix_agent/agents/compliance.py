import re
from typing import Dict
from ..models.types import State, ComplianceResult, Category

CATEGORY_LABELS: Dict[str, str] = {
    "01.0000-50": "Death Certificate",
    "02.0300-50": "Will or Trust",
    "03.0090-00": "Property Deed",
    "04.5000-00": "Financial Statement",
    "05.5000-70": "Tax Document",
    "00.0000-00": "Miscellaneous",
}

def compliance_node(state: State) -> State:
    code: Category = state["classification"]["categoryCode"]
    text = state["doc"]["extractedText"].lower()

    valid = True
    reason = None

    if code == "01.0000-50":
        match = re.search(
            r"date\s+of\s+death\s*:\s*(\S.+)",
            text,
            flags=re.I
        )

        if match:
            has_dod_value = True
        else:
            has_dod_value = False

        ok = ("certificate of death" in text) and has_dod_value
        if not ok:
            valid = False
            reason = "Missing 'Certificate of Death' or 'Date of Death'"
    elif code == "02.0300-50":
        ok = ("last will and testament" in text) or ("trust agreement" in text)
        if not ok:
            valid = False
            reason = "Missing 'Last Will and Testament' or 'Trust Agreement'"
    else:
        valid = True
    
    result: ComplianceResult = {"valid": valid}
    if reason:
        result["reason"] = reason
    return {**state, "compliance": result}


