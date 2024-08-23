import boto3
from app.config import settings
from app.utils.logging import logger

textract_client = boto3.client(
    'textract',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

async def extract_text_from_image(image_bytes: bytes) -> str:
    try:
        response = textract_client.detect_document_text(Document={'Bytes': image_bytes})
        
        extracted_text = ""
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                extracted_text += item["Text"] + "\n"
        
        return extracted_text
    except Exception as e:
        logger.error(f"Error in AWS Textract: {str(e)}")
        raise