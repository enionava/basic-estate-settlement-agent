import sys
import pathlib
import pytest
import asyncio
from fastapi.testclient import TestClient

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

@pytest.fixture(scope="session", autouse=True)
def _win_selector_event_loop_policy():
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.fixture(scope="session")
def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]

@pytest.fixture(scope="session")
def data_dir(repo_root) -> pathlib.Path:
    return repo_root / "mock_pdfs"

@pytest.fixture(scope="session")
def death_cert_path(data_dir) -> pathlib.Path:
    return data_dir / "01_death_certificate_Eleanor_Bennett.pdf"

@pytest.fixture(scope="session")
def will_path(data_dir) -> pathlib.Path:
    return data_dir / "02_last_will_and_testament_Alice_Carter.pdf"

@pytest.fixture(scope="session")
def deed_path(data_dir) -> pathlib.Path:
    return data_dir / "03_warranty_deed_Maple_Avenue.pdf"

@pytest.fixture(scope="session")
def bank_stmt_path(data_dir) -> pathlib.Path:
    return data_dir / "04_bank_statement_RiverBank_Feb2025.pdf"

@pytest.fixture(scope="session")
def tax_form_path(data_dir) -> pathlib.Path:
    return data_dir / "05_tax_document_Form1041_snapshot_Eleanor_Bennett_Estate.pdf"

@pytest.fixture(scope="session")
def misc_letter_path(data_dir) -> pathlib.Path:
    return data_dir / "06_misc_correspondence_BlueSky_Insurance_Claim_Status.pdf"

@pytest.fixture(scope="session")
def death_cert_invalid_path(data_dir) -> pathlib.Path:
    return data_dir / "07_death_certificate_Eleanor_Bennett_dod_removed_invalid.pdf"

@pytest.fixture(scope="session")
def api_client():
    from alix_agent.api import app
    return TestClient(app)
