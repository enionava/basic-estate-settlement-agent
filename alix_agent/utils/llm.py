import os
from typing import List, Tuple, Optional, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.messages import SystemMessage, HumanMessage

from dotenv import load_dotenv
load_dotenv()

from ..agents.compliance import CATEGORY_LABELS

def llm_tiebreak(
        text: str,
        codes: List[str],
        model: Optional[str] = None,
) -> Tuple[Optional[str], float]:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = model or os.getenv("OPENAI_MODEL", "gpt-5-mini")

    if not api_key and not base_url:
        return None, 0.0

    llm = ChatOpenAI(
        model=model,
        temperature=0,
        base_url=base_url,
        api_key=api_key
    )

    parser = JsonOutputParser()
    system = SystemMessage(content=(
        "You are a precise classifier. "
        "Return a JSON object with exactly one Key 'categoryCode' and value being one of the provided codes."
    ))
    human = HumanMessage(content=(
        "Text:\n---\n"
        f"{text}\n---\n"
        "Allowed categories:\n"+
        "\n".join([f"- {c}: {CATEGORY_LABELS[c]}" for c in codes]) +
        "\n\nGuidelines:\n"
        " - Base your choice on the document’s content and purpose (not just mentions).\n"
        " - If the document appears to be correspondence about documents (letters, notices,\n"
        "   emails) rather than the documents themselves, choose '00.0000-00' (Miscellaneous).\n"
        " - If uncertain, choose '00.0000-00'.\n\n"
        "Return JSON ONLY as: {\"categoryCode\": \"...\"}"
    ))
    resp = llm.invoke([system, human])
    try:
        data: Dict[str, Any] = parser.parse(resp.content)
        code = data.get("categoryCode")
        if code in codes:
            return code, 0.75
    except Exception:
        pass

    return None, 0.0

