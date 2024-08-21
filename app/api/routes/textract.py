from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.textract import textract_service

router = APIRouter()

@router.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        extracted_text = textract_service.extract_text(contents)
        return {"extracted_text": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")