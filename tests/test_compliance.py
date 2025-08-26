from alix_agent.router import process_pdf

def test_death_certificate_requires_dod(death_cert_invalid_path):
    out = process_pdf(str(death_cert_invalid_path))
    assert out["categoryCode"] == "01.0000-50"
    assert out["valid"] is False
    assert out["reason"]