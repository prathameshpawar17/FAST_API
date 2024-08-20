import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class TextractService:
    def __init__(self):
        self.client = boto3.client('textract', region_name='us-west-2')

    def extract_text(self, file_bytes):
        try:
            response = self.client.detect_document_text(Document={'Bytes': file_bytes})
            extracted_text = " ".join([item['Text'] for item in response['Blocks'] if item['BlockType'] == 'LINE'])
            logger.info("Text extracted successfully")
            return extracted_text
        except ClientError as e:
            logger.error(f"Error extracting text: {str(e)}")
            raise

textract_service = TextractService()