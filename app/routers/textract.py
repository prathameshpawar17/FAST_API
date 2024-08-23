from fastapi import APIRouter, UploadFile, File
from app.services.aws_textract import extract_text_from_image

router = APIRouter(prefix="/textract", tags=["textract"])

@router.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    contents = await file.read()
    extracted_text = await extract_text_from_image(contents)
    return {"extracted_text": extracted_text}