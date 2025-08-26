# Alix Agent System

## 🧩 Core Problem

In estate settlement, organizations receive large volumes of documents (death certificates, wills, deeds, tax forms, statements, etc.). Manually triaging and validating these is **time-consuming and error-prone**.

The challenge:

* Classify documents into a fixed taxonomy.
* Validate category-specific compliance rules (e.g., death certificates must contain `"Certificate of Death"` and `"Date of Death"`).
* Automate routing between these steps in a clean, testable way.

---

## 💡 My Approach

This solution is built as a **multi-agent system**:

1. **Router (Master Agent)**

   * Receives an input document.
   * Orchestrates flow: → Classification → Compliance → Output.

2. **Classification Agent**

   * Uses keyword & text parsing (with optional PDF parsing via `utils/pdf.py`).
   * Maps documents to taxonomy codes:

     * `01.0000-50` Death Certificate
     * `02.0300-50` Will/Trust
     * `03.0090-00` Property Deed
     * `04.5000-00` Financial Statement
     * `05.5000-70` Tax Document
     * `00.0000-00` Miscellaneous

3. **Compliance Agent**

   * Runs category-specific checks:

     * **Death Certificates** → must have `"Certificate of Death"` and `"Date of Death"`.
     * **Wills/Trusts** → must have `"Last Will and Testament"` or `"Trust Agreement"`.
   * Others auto-validate as `valid: true`.

4. **Models & Utils**

   * `models/types.py` → typed DTOs for `Document`, `ClassificationResult`, `ComplianceResult`.
   * `utils/pdf.py` → text extraction from mock PDFs.
   * `utils/llm.py` → placeholder for LLM classification fallback (not required but included for extensibility).

The design emphasizes **clear separation of concerns** (routing vs classification vs compliance) and **testability** (Pytest suite included).

---

## ⚙️ Setup

### 1. Clone & Navigate

```bash
git clone <your_repo_url>
cd alix_agent
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment

Copy the sample env:

```bash
cp .env.example .env
```
---

## 🧪 Running Tests

Execute the unit tests:

```bash
pytest -v
```

Covers:

* Classification logic
* Compliance validation
* API endpoints

---

## 🚀 Execution

### Run via CLI

Classify and validate mock documents:

```bash
python -m alix_agent.cli --input ./mock_pdfs
```

### Run via API

Start FastAPI server:

```bash
uvicorn alix_agent.api:app --reload
```

Endpoints:

* `GET /health` → health check
* `POST /classify` → upload a document for classification/validation

Example:

```bash
curl -X POST "http://127.0.0.1:8000/classify" \
  -F "file=@mock_pdfs/01_death_certificate_Eleanor_Bennett.pdf"
```

---

## ✅ Outcome

* Automated routing of estate documents.
* Deterministic classification + rule-based compliance checks.
* Fully testable with CLI + API interfaces.
