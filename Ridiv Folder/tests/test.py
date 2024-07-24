import pytest
from fastapi.testclient import TestClient
from lmain import app, rag_chain

client = TestClient(app)

def test_upload_pdf():
    with open("sample.pdf", "rb") as pdf:
        response = client.post("/upload_pdf/", files={"file": ("sample.pdf", pdf, "application/pdf")})
        assert response.status_code == 200
        assert response.json() == {"detail": "PDF uploaded and processed successfully"}
        assert rag_chain is not None

def test_upload_invalid_file():
    with open("sample.txt", "rb") as txt:
        response = client.post("/upload_pdf/", files={"file": ("sample.txt", txt, "text/plain")})
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid file format. Please upload a PDF file."}

def test_chat_before_upload():
    response = client.post("/chat", json={"message": "What is this document about?"})
    assert response.status_code == 400
    assert response.json() == {"detail": "No PDF has been uploaded yet"}

def test_chat_after_upload():
    with open("sample.pdf", "rb") as pdf:
        client.post("/upload_pdf/", files={"file": ("sample.pdf", pdf, "application/pdf")})
    response = client.post("/chat", json={"message": "What is this document about?"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_chat_no_message():
    with open("sample.pdf", "rb") as pdf:
        client.post("/upload_pdf/", files={"file": ("sample.pdf", pdf, "application/pdf")})
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "No message provided"}
