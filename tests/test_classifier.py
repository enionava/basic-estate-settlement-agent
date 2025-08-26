from alix_agent.router import process_pdf

def test_classifies_death_certificate(death_cert_invalid_path):
    out = process_pdf(str(death_cert_invalid_path))
    assert out["categoryCode"] == "01.0000-50"
    assert 0.6 <= out["confidence"] <= 1.0

def test_classifies_will_or_trust(will_path):
    out = process_pdf(str(will_path))
    assert out["categoryCode"] == "02.0300-50"
    assert out["valid"] is True

def test_classifies_deed(deed_path):
    out = process_pdf(str(deed_path))
    assert out["categoryCode"] == "03.0090-00"
    assert out["valid"] is True

def test_classifies_bank_statement(bank_stmt_path):
    out = process_pdf(str(bank_stmt_path))
    assert out["categoryCode"] == "04.5000-00"
    assert out["valid"] is True

def test_classifies_tax_document(tax_form_path):
    out = process_pdf(str(tax_form_path))
    assert out["categoryCode"] == "05.5000-70"
    assert out["valid"] is True

def test_misc_letter(misc_letter_path):
    out = process_pdf(str(misc_letter_path))
    assert out["categoryCode"] in {"00.0000-00", "04.5000-00", "03.0090-00", "05.5000-70"}
    assert out["valid"] is True
