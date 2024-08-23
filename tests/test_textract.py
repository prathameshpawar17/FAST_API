from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch('app.services.aws_textract.extract_text_from_image')
def test_extract_text(mock_extract):
    mock_extract.return_value = "Mocked extracted text"
    
    response = client.post("/textract/extract", files={"file": ("test.jpg", b"test content")})
    
    assert response.status_code == 200
    assert response.json() == {"extracted_text": "Mocked extracted text"}