from typing import List, Dict
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)

class SMSGateway:
    def __init__(self):
        self.message_store: Dict[str, List[Dict]] = {}
        self.failed_messages: List[Dict] = []

    async def send_sms(self, sender: str, receiver: str, content: str) -> bool:
        try:
            # Simulate network issues (1 in 5 chance of failure)
            if len(self.failed_messages) % 5 == 0:
                raise Exception("Network error")

            if receiver not in self.message_store:
                self.message_store[receiver] = []
            
            self.message_store[receiver].append({
                "sender": sender,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"SMS sent from {sender} to {receiver}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            self.failed_messages.append({
                "sender": sender,
                "receiver": receiver,
                "content": content
            })
            return False

    def get_inbox(self, phone_number: str) -> List[Dict]:
        return self.message_store.get(phone_number, [])

    async def retry_failed_messages(self):
        while True:
            if self.failed_messages:
                message = self.failed_messages.pop(0)
                success = await self.send_sms(message['sender'], message['receiver'], message['content'])
                if success:
                    logger.info(f"Retried sending message to {message['receiver']}")
                else:
                    logger.error(f"Retry failed for message to {message['receiver']}")
                    self.failed_messages.append(message)
            await asyncio.sleep(60)  # Retry every minute

sms_gateway = SMSGateway()