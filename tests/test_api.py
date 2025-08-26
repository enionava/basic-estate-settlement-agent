def test_health(api_client):
    r = api_client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_classify_pdf_api(api_client, death_cert_path):
    with open(death_cert_path, "rb") as f:
        r = api_client.post("/classify", files={"file": ("dc.pdf", f, "application/pdf")})
    assert r.status_code == 200
    data = r.json()
    assert data["categoryCode"] == "01.0000-50"
    assert data["valid"] is True
    assert "filename" in data
